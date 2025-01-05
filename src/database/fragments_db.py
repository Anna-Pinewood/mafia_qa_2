from typing import List, Optional, Dict, Any
import chromadb
from langchain_community.vectorstores import Chroma
from langchain_core.embeddings import Embeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
import json
from database.rule_fragment import RuleFragment
import logging
from chromadb.config import Settings
from tqdm import tqdm
from consts import (CHROMA_CLIENT_AUTHN_PROVIDER, CHROMA_PASSWORD,
                    CHROMA_USER,
                    CHROMA_PORT,
                    CHROMA_HOST,
                    EMBEDDING_MODEL_NAME)

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
        if self._embeddings is None:
            logger.info("Loading embeddings model... It may take some time.")
            self._embeddings = HuggingFaceEmbeddings(
                model_name=self._embedding_model_name,
                model_kwargs={'device': 'cpu'},  # Changed from 'cuda' to 'cpu'
                encode_kwargs={'normalize_embeddings': True}
            )
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
                f"Added rule fragment {fragment.paragraph} to vector store")

        except Exception as e:
            logger.error(f"Failed to add rule fragment: {str(e)}")
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
            logger.error(f"Failed to search rules: {str(e)}")
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
                f"Getting embeddings and loading into vector store... It may take a while.")
            self.rules_vectorstore.add_texts(
                texts=texts,
                metadatas=metadatas,
                ids=ids
            )
            logger.info(f"Added {len(fragments)} rule fragments in batch")

        except Exception as e:
            logger.error(f"Failed to batch add rule fragments: {str(e)}")
            raise

    def get_collection_stats(self) -> Dict[str, int]:
        """Get statistics about the collections."""
        try:
            rules_count = self.rules_vectorstore._collection.count()

            return {
                "rule_fragments": rules_count,
            }

        except Exception as e:
            logger.error(f"Failed to get collection stats: {str(e)}")
            raise

    def clear_rules_collection(self) -> None:
        """Clear only the rule fragments collection."""
        try:
            rule_ids = self.rules_vectorstore._collection.get()["ids"]
            if rule_ids:
                self.rules_vectorstore._collection.delete(ids=rule_ids)
                logger.info("Cleared rule fragments collection")
        except Exception as e:
            logger.error(f"Failed to clear rules collection: {str(e)}")
            raise

    @staticmethod
    def process_fragment(fragment: Dict[str, Any]) -> str:
        begin = fragment['metadata']['full_path']
        content = fragment['content']
        return f"{begin}\n{content}"
