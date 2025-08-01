from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid

class Project(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    status: Optional[str] = "Completed"
    description: str
    image_url: Optional[str] = None
    tech_stack: List[str] = []
    features: List[str] = []
    outcome: Optional[str] = None
    github_link: Optional[str] = None
    live_demo: Optional[str] = None
    order: int = 0
    featured: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ProjectCreate(BaseModel):
    title: str
    status: Optional[str] = "Completed"
    description: str
    image_url: Optional[str] = None
    tech_stack: List[str] = []
    features: List[str] = []
    outcome: Optional[str] = None
    github_link: Optional[str] = None
    live_demo: Optional[str] = None
    order: int = 0
    featured: bool = True

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    tech_stack: Optional[List[str]] = None
    features: Optional[List[str]] = None
    outcome: Optional[str] = None
    github_link: Optional[str] = None
    live_demo: Optional[str] = None
    order: Optional[int] = None
    featured: Optional[bool] = None