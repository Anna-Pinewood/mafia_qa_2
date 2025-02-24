"""Module for processing text data from PDF and txt files."""
import logging
import re
from pathlib import Path
from typing import List

import PyPDF2

from database.rule_fragment import RuleFragment, RuleLevel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def extract_pdf_text(data_path: str) -> str:
    """Extract text content from PDF file."""
    logger.info("Reading PDF file from: %s", data_path)
    pdf_path = Path(data_path)

    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text()

    logger.info("Successfully extracted %d characters from PDF", len(text))
    return text


def parse_hierarchy(paragraph_num: str, lines: List[str]) -> List[RuleLevel]:
    """Parse hierarchy levels from paragraph number and corresponding lines."""
    parts = paragraph_num.split('.')
    hierarchy = []

    for i in range(len(parts)):
        current_num = '.'.join(parts[:i+1])
        # Find matching line for current level
        for line in lines:
            if line.startswith(current_num + '.'):
                title = line[len(current_num + '. '):].strip()
                hierarchy.append(RuleLevel(
                    title=title,
                    paragraph_number=current_num,
                    heading_text=f"{current_num}. {title}"
                ))
                break

    return hierarchy[:-1]  # Exclude current level from hierarchy


def split_into_fragments(data_path: str) -> List[RuleFragment]:
    """Split PDF content into rule fragments."""
    logger.info("Starting to process document from: %s", data_path)

    text = extract_pdf_text(data_path)
    lines = [line.strip() for line in text.split('\n') if line.strip()]

    # Regular expression for paragraph numbers (e.g., "4.1.2.")
    paragraph_pattern = r'^\d+(?:\.\d+)*\.'

    fragments = []
    current_paragraph = None
    current_content = []

    for line in lines:
        match = re.match(paragraph_pattern, line)

        if match:
            # Save previous fragment if exists
            if current_paragraph and current_content:
                paragraph_num = current_paragraph.rstrip('.')
                hierarchy = parse_hierarchy(paragraph_num, lines)
                content = ' '.join(current_content)

                fragment = RuleFragment(
                    content=content,
                    paragraph=paragraph_num,
                    hierarchy=hierarchy,
                    embedding=None
                )
                fragments.append(fragment)
                logger.debug(
                    "Created fragment for paragraph %s", paragraph_num)

            current_paragraph = match.group(0)
            current_content = [line[len(current_paragraph):].strip()]
        else:
            if current_paragraph:  # Append to current paragraph content
                current_content.append(line)

    # Add last fragment
    if current_paragraph and current_content:
        paragraph_num = current_paragraph.rstrip('.')
        hierarchy = parse_hierarchy(paragraph_num, lines)
        fragment = RuleFragment(
            content=' '.join(current_content),
            paragraph=paragraph_num,
            hierarchy=hierarchy,
            embedding=None
        )
        fragments.append(fragment)

    logger.info("Successfully split document into %d fragments", len(fragments))
    return fragments


def load_txt_fragments(file_path: str, paragraph: str) -> List[RuleFragment]:
    """Lead comments from txt files.
    Expected:
    ```
    High level heading
    Statement 1
    Statement 2

    High level heading 2
    Statement 1

    High level heading 3
    ...
    ```
    """
    fragments = []
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = [line.strip('\n') for line in f.readlines()]

    current_heading = None
    i = 10
    for line in lines:
        line = line.strip()
        if not current_heading and line:
            current_heading = line
            continue
        if not line:  # blank line => reset heading
            current_heading = None
            continue
        if current_heading:
            fragments.append(
                RuleFragment(
                    content=f"{current_heading}\n{line}",
                    paragraph=f"{paragraph} {i}",
                    hierarchy=[RuleLevel(
                        title="",
                        paragraph_number="-",
                        heading_text=current_heading
                    )],
                    embedding=None
                )
            )
            i += 1
    return fragments
