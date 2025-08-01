from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid

class Certificate(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    issuer: str
    year: str
    description: str
    order: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)

class CertificateCreate(BaseModel):
    title: str
    issuer: str
    year: str
    description: str
    order: int = 0

class CertificateUpdate(BaseModel):
    title: Optional[str] = None
    issuer: Optional[str] = None
    year: Optional[str] = None
    description: Optional[str] = None
    order: Optional[int] = None