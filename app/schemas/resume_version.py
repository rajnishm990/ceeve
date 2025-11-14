from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Any


class ResumeVersionBase(BaseModel):
    version_number: int
    html_content: Optional[str] = None
    layout_json: Optional[Any] = None


class ResumeVersionCreate(BaseModel):
    html_content: Optional[str]
    layout_json: Optional[Any]


class ResumeVersionRead(ResumeVersionBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
