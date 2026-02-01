from pydantic import BaseModel
from typing import Optional

class FeedbackRequest(BaseModel):
    classificacao: str
    feedback: str
    motivo: Optional[str] = None