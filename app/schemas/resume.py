from pydantic import BaseModel , Field
from datetime import datetime 
from typing import Optional , Any
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from app.schemas.resume_version import ResumeVersionRead


class ResumeBase(BaseModel):
    title: str 


class ResumeCreate(ResumeBase):
    file_name: Optional[str]= None


class ResumeRead(ResumeBase):
    id: int 
    file_name: Optional[str] = None 
    shareable_link: Optional[str] = Field(alias="shareable_slug")
    created_at : datetime 
    updated_at: Optional[datetime]
    versions: List[ResumeVersionRead] = []

    class Config:
        orm_mode = True
