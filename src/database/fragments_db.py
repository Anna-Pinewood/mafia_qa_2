import logging
from typing import List
from .text_processor import split_into_fragments
from .models.rule_fragment import RuleFragment
from .init_rag import init_collections

logger = logging.getLogger(__name__)

def load_fragments(fragments: List[RuleFragment]) -> None:
    """Store rule fragments in the database."""
    client = init_collections()
    collection = client.get_collection("rule_fragments")
    
    documents = []
    metadatas = []
    ids = []
    
    for i, fragment in enumerate(fragments):
        frag_dict = fragment.to_chroma_dict()
        documents.append(frag_dict["content"])
        metadatas.append(frag_dict["metadata"])
        ids.append(f"fragment_{i}")
    
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    logger.info(f"Stored {len(fragments)} fragments in the database")
