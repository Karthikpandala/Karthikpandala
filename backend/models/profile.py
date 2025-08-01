from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime
import uuid

class ContactInfo(BaseModel):
    email: str
    phone: str
    github: str
    linkedin: str

class Profile(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    tagline: str
    bio: str
    profile_image_url: Optional[str] = None
    contact: ContactInfo
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    tagline: Optional[str] = None
    bio: Optional[str] = None
    profile_image_url: Optional[str] = None
    contact: Optional[ContactInfo] = None