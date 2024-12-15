from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class QnAPair(BaseModel):
    question: str
    answer: str
    related_paragraphs: List[str]  # ["1.1", "1.2"]
    embedding: Optional[List[float]]

    def to_chroma_dict(self) -> Dict[str, Any]:
        return {
            "content": f"Q: {self.question}\nA: {self.answer}",
            "metadata": {
                "related_paragraphs": self.related_paragraphs
            }
        }


# Example
# qna = QnAPair(
#     question="Сколько всего игроков участвует в игре?",
#     answer="В игре принимают участие десять человек.",
#     related_paragraphs=["1.1"]
# )
