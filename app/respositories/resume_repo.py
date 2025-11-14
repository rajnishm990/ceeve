# app/repositories/resume_repo.py
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.resume import Resume
from app.models.resume_version import ResumeVersion
from datetime import datetime


class ResumeRepository:
    """
    Resume CRUD & higher-level helpers.
    """

    @staticmethod
    def create(db: Session, *, user_id: int, title: str, file_name: Optional[str] = None, shareable_slug: Optional[str] = None) -> Resume:
        resume = Resume(
            user_id=user_id,
            title=title,
            file_name=file_name,
            shareable_slug=shareable_slug,
            created_at=datetime.utcnow()
        )
        db.add(resume)
        db.commit()
        db.refresh(resume)
        return resume

    @staticmethod
    def get(db: Session, resume_id: int) -> Optional[Resume]:
        return db.query(Resume).filter(Resume.id == resume_id).first()

    @staticmethod
    def list_for_user(db: Session, user_id: int) -> List[Resume]:
        return db.query(Resume).filter(Resume.user_id == user_id).order_by(Resume.created_at.desc()).all()

    @staticmethod
    def delete(db: Session, resume: Resume) -> None:
        db.delete(resume)
        db.commit()

    @staticmethod
    def set_active_version(db: Session, resume: Resume, version: ResumeVersion) -> Resume:
        """
        Set a ResumeVersion as the active_version for a resume.
        Commits and returns refreshed Resume instance.
        """
        resume.active_version_id = version.id
        resume.updated_at = datetime.utcnow()
        db.add(resume)
        db.commit()
        db.refresh(resume)
        return resume

    @staticmethod
    def update_title(db: Session, resume: Resume, new_title: str) -> Resume:
        resume.title = new_title
        resume.updated_at = datetime.utcnow()
        db.add(resume)
        db.commit()
        db.refresh(resume)
        return resume

    @staticmethod
    def set_shareable_slug(db: Session, resume: Resume, slug: str) -> Resume:
        resume.shareable_slug = slug
        resume.updated_at = datetime.utcnow()
        db.add(resume)
        db.commit()
        db.refresh(resume)
        return resume
