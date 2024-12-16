import chromadb
from chromadb.config import Settings
import logging
from consts import (CHROMA_PASSWORD,
                    CHROMA_USER,
                    CHROMA_PORT,
                    CHROMA_HOST,
                    CHROMA_CLIENT_AUTHN_PROVIDER,
                    path_project
                    )

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def init_collections():
    try:
        client = chromadb.HttpClient(
            host=CHROMA_HOST,
            port=CHROMA_PORT,
            settings=Settings(
                chroma_client_auth_provider=CHROMA_CLIENT_AUTHN_PROVIDER,
                chroma_client_auth_credentials=f"{CHROMA_USER}:{CHROMA_PASSWORD}",
            )
        )
        logger.info("Connected. Chroma heartbeat: %s", client.heartbeat())

        existing = {col.name: col for col in client.list_collections()}
        logger.debug(f"Found existing collections: {list(existing.keys())}")

        if 'qna_pairs' not in existing:
            client.create_collection(
                name="qna_pairs",
                metadata={"description": "QnA pairs collection"}
            )
            logger.info("Created qna_pairs collection")

        if 'rule_fragments' not in existing:
            client.create_collection(
                name="rule_fragments",
                metadata={"description": "Rule fragments collection"}
            )
            logger.info("Created rule_fragments collection")

        return client

    except Exception as e:
        logger.error(f"Failed to initialize collections: {str(e)}")
        raise


if __name__ == "__main__":
    client = init_collections()
    logger.info(
        f"Available collections: {[col.name for col in client.list_collections()]}")
