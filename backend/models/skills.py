from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid

class SkillCategory(BaseModel):
    name: str
    items: List[str]
    order: int = 0

class Skills(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    categories: List[SkillCategory]
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class SkillsUpdate(BaseModel):
    categories: Optional[List[SkillCategory]] = None