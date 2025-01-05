"""Model for a fragment of a rule."""
from typing import Any, Dict, List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field


class RuleLevel(BaseModel):
    """Represents a level in the hierarchy of a rule.
    E.g. '6. Нарушения' -> '6.1. Фолы' -> '6.1.1. Фол присуждается...'
    """
    title: str
    paragraph_number: Optional[str]  # e.g. "1" for section, None for top level
    heading_text: str


class RuleFragment(BaseModel):
    """Represents a fragment of a rule."""
    content: str  # The actual rule text
    paragraph: str  # e.g. "1.1"
    # Only parent levels, not including current paragraph
    hierarchy: List[RuleLevel]
    embedding: Optional[List[float]]
    fragment_id: str = Field(default_factory=lambda: str(uuid4()))

    def to_chroma_dict(self) -> Dict[str, Any]:
        """Convert to a dictionary for storage in the vector store."""
        return {
            "content": self.content,
            "paragraph": self.paragraph,
            "hierarchy": [level.model_dump_json() for level in self.hierarchy],
            "metadata": {
                "paragraph": self.paragraph,
                "full_path": " > ".join(level.heading_text for level in self.hierarchy)
            }
        }

# Example usage
# rule_fragment = RuleFragment(
#     content=("В игре принимают участие десять человек."
#               "Игроки случайным образом делятся на две команды..."),
#     paragraph="1.1.1",
#     hierarchy=[
#         RuleLevel(
#             title="Базовые правила",
#             paragraph_number="1",
#             heading_text="1. Базовые правила"
#         ),
#         RuleLevel(
#             title="Основные понятия",
#             paragraph_number="1.1",
#             heading_text="1.1. Основные понятия"
#         )
#     ]
# )
