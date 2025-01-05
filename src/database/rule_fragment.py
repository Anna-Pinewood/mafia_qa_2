from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from uuid import uuid4


class RuleLevel(BaseModel):
    title: str
    paragraph_number: Optional[str]  # e.g. "1" for section, None for top level
    heading_text: str


class RuleFragment(BaseModel):
    content: str  # The actual rule text
    paragraph: str  # e.g. "1.1"
    # Only parent levels, not including current paragraph
    hierarchy: List[RuleLevel]
    embedding: Optional[List[float]]
    fragment_id: str = Field(default_factory=lambda: str(uuid4()))

    def to_chroma_dict(self) -> Dict[str, Any]:
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
#     content="В игре принимают участие десять человек. Игроки случайным образом делятся на две команды...",
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
