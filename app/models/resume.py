from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(100), nullable=False)
    file_name = Column(String(200))
    shareable_slug = Column(String(100), unique=True, nullable=True)
    active_version_id = Column(Integer, ForeignKey("resume_versions.id", use_alter=True, name="fk_active_version_id"), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", backref="resumes")
    versions = relationship("ResumeVersion", back_populates="resume", cascade="all, delete-orphan")
    active_version = relationship("ResumeVersion",foreign_keys=[active_version_id],uselist=False,post_update=True)
