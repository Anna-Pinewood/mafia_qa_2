import sys
import logging
from consts import DATA_COMMENTS, DATA_RULES
from fragments_db import RAGInterface
from text_processor import split_into_fragments, load_txt_fragments
import fire

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def fill_rule_fragments_collection(
        pdf_rules_path: str = DATA_RULES,
        txt_comments_path: str = DATA_COMMENTS):
    rag = RAGInterface()  # uses rule_fragments collection

    # Check if 'rule_fragments' collection exists
    try:
        collection_stats = rag.get_collection_stats()
        existing_rules_count = collection_stats.get("rule_fragments", 0)
        if existing_rules_count > 0:
            logger.info(
                "rule_fragments collection is not empty. Collection stats: %s. Exiting.", collection_stats)
            sys.exit(0)
        else:
            logger.info(
                "rule_fragments collection exists but is empty or new. Filling...")

    except Exception as e:
        logger.info(
            "rule_fragments collection does not exist. Creating and filling...")

    # Parse PDF
    pdf_fragments = split_into_fragments(data_path=pdf_rules_path)
    # Parse TXT
    txt_fragments = load_txt_fragments(
        txt_comments_path,
        paragraph="Комментарий СК ФСМ")
    # Combine
    all_fragments = pdf_fragments + txt_fragments
    logger.info(
        f"Total fragments to add: {len(all_fragments)}")
    logger.info("Example fragment: %s", all_fragments[0])

    # Add fragments to DB
    rag.batch_add_rule_fragments(all_fragments)
    logger.info("Database filling completed.")


if __name__ == "__main__":
    logger.info("Entering script...")
    fire.Fire(fill_rule_fragments_collection)
    """
    Example usage:
    ```
    python init_rag_new.py \
    --pdf_rules_path=data/official_rules_fsm.pdf \
    --txt_comments_path=data/fsm_comments.txt
    ```
    """
