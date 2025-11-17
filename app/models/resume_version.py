from sqlalchemy import Column, Integer, ForeignKey, DateTime, func, Text, String
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

class ResumeVersion(Base):
    __tablename__ = "resume_versions"

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False)
    version_number = Column(Integer, nullable=False)
    html_content = Column(Text, nullable=True)
    layout_json = Column(JSON, nullable=True)  # For future coordinate-based fields
    raw_file_path = Column(String, nullable=True)
    html_file_path = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    resume = relationship(
    "Resume",
    back_populates="versions",
    foreign_keys=[resume_id]
    )
