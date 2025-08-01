from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid

class Education(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    degree: str
    institution: str
    period: str
    grade: str
    location: Optional[str] = None
    order: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)

class EducationCreate(BaseModel):
    degree: str
    institution: str
    period: str
    grade: str
    location: Optional[str] = None
    order: int = 0

class EducationUpdate(BaseModel):
    degree: Optional[str] = None
    institution: Optional[str] = None
    period: Optional[str] = None
    grade: Optional[str] = None
    location: Optional[str] = None
    order: Optional[int] = None