from pydantic import BaseModel
from typing import List, Optional

class Topic(BaseModel):
    name: str
    description: Optional[str] = None
    level: Optional[str] = "beginner"

class Curriculum(BaseModel):
    topics: List[Topic]
