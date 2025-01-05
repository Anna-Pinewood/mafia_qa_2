"""RAG interface for interacting with stored fragments database."""
import logging
from typing import Any, Dict, List

import chromadb
import torch
from chromadb.config import Settings
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from tqdm import tqdm

from consts import (CHROMA_CLIENT_AUTHN_PROVIDER, CHROMA_HOST, CHROMA_PASSWORD,
                    CHROMA_PORT, CHROMA_USER, EMBEDDING_MODEL_NAME)
from database.rule_fragment import RuleFragment

logger = logging.getLogger(__name__)


class RAGInterface:
    def __init__(
        self,
        embedding_model_name: str = EMBEDDING_MODEL_NAME
    ):
        """Initialize RAG interface with ChromaDB and embedding model."""
        self._embedding_model_name = embedding_model_name
        self._embeddings = None
        self.client = chromadb.HttpClient(
            host=CHROMA_HOST,
            port=CHROMA_PORT,
            settings=Settings(
                chroma_client_auth_provider=CHROMA_CLIENT_AUTHN_PROVIDER,
                chroma_client_auth_credentials=f"{CHROMA_USER}:{CHROMA_PASSWORD}"
            )
        )

        # Initialize vectorstores for different collections
        self.rules_vectorstore = Chroma(
            collection_name="rule_fragments",
            embedding_function=self.embeddings,
            client=self.client,
        )

    @property
    def embeddings(self):
        """Lazy load embeddings model."""
        if self._embeddings is None:
            logger.info("Loading embeddings model... It may take some time.")
            device = 'cuda' if torch.cuda.is_available() else 'cpu'
            self._embeddings = HuggingFaceEmbeddings(
                model_name=self._embedding_model_name,
                model_kwargs={'device': device},
                encode_kwargs={'normalize_embeddings': True}
            )
            logger.info("Using device: %s", device)
        return self._embeddings

    def healthcheck(self):
        return f"Chroma heartbeat: {self.client.heartbeat()}"

    def add_rule_fragment(self, fragment: RuleFragment) -> None:
        """Add a single rule fragment to the vector store."""
        try:
            chroma_dict = fragment.to_chroma_dict()

            # Add to vector store
            self.rules_vectorstore.add_texts(
                texts=[chroma_dict["content"]],
                metadatas=[chroma_dict["metadata"]],
                ids=[chroma_dict["paragraph"]]
            )
            logger.info(
                "Added rule fragment %s to vector store", fragment.paragraph)

        except Exception as e:
            logger.error("Failed to add rule fragment: %s", str(e))
            raise

    def search_rules(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """Search for relevant rule fragments."""
        try:
            results = self.rules_vectorstore.similarity_search_with_relevance_scores(
                query,
                k=k
            )

            formatted_results = []
            for doc, score in results:
                formatted_results.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "relevance_score": score
                })

            return formatted_results

        except Exception as e:
            logger.error("Failed to search rules: %s", str(e))
            raise

    def batch_add_rule_fragments(self, fragments: List[RuleFragment]) -> None:
        """Add multiple rule fragments in batch."""
        try:
            texts = []
            metadatas = []
            ids = []

            for fragment in tqdm(fragments):
                chroma_dict = fragment.to_chroma_dict()
                texts.append(chroma_dict["content"])
                metadatas.append(chroma_dict["metadata"])
                ids.append(chroma_dict["paragraph"])

            logger.info(
                "Getting embeddings and loading into vector store... It may take a while.")
            self.rules_vectorstore.add_texts(
                texts=texts,
                metadatas=metadatas,
                ids=ids
            )
            logger.info("Added %d rule fragments in batch", len(fragments))

        except Exception as e:
            logger.error("Failed to batch add rule fragments: %s", str(e))
            raise

    def get_collection_stats(self) -> Dict[str, int]:
        """Get statistics about the collections."""
        try:
            rules_count = self.rules_vectorstore._collection.count()

            return {
                "rule_fragments": rules_count,
            }

        except Exception as e:
            logger.error("Failed to get collection stats: %s", str(e))
            raise

    def clear_rules_collection(self) -> None:
        """Clear only the rule fragments collection."""
        try:
            rule_ids = self.rules_vectorstore._collection.get()["ids"]
            if rule_ids:
                self.rules_vectorstore._collection.delete(ids=rule_ids)
                logger.info("Cleared rule fragments collection")
        except Exception as e:
            logger.error("Failed to clear rules collection: %s", str(e))
            raise

    @staticmethod
    def process_fragment(fragment: Dict[str, Any]) -> str:
        """Format fragment for display."""
        begin = fragment['metadata']['full_path']
        content = fragment['content']
        return f"{begin}\n{content}"
