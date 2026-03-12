from pydantic import BaseModel
from typing import List

class MissingTopic(BaseModel):
    topic_name: str
    reason: str
    severity_score: int

class GapAnalysisResult(BaseModel):
    missing_topics: List[MissingTopic]
    weak_topics: List[str]
    recommended_learning_order: List[str]
    gap_score: float
