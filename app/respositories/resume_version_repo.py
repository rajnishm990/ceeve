# app/repositories/resume_version_repo.py
from typing import List, Optional, Any
from sqlalchemy.orm import Session
from app.models.resume_version import ResumeVersion
from datetime import datetime


class ResumeVersionRepository:
    """
    CRUD for ResumeVersion.
    """

    @staticmethod
    def add_version(db: Session, *, resume_id: int, version_number: int, html_content: Optional[str] = None,
                    layout_json: Optional[Any] = None, raw_file_path: Optional[str] = None,
                    html_file_path: Optional[str] = None) -> ResumeVersion:
        ver = ResumeVersion(
            resume_id=resume_id,
            version_number=version_number,
            html_content=html_content,
            layout_json=layout_json,
            raw_file_path=raw_file_path,
            html_file_path=html_file_path,
            created_at=datetime.utcnow()
        )
        db.add(ver)
        db.commit()
        db.refresh(ver)
        return ver

    @staticmethod
    def get(db: Session, version_id: int) -> Optional[ResumeVersion]:
        return db.query(ResumeVersion).filter(ResumeVersion.id == version_id).first()

    @staticmethod
    def list_for_resume(db: Session, resume_id: int) -> List[ResumeVersion]:
        return db.query(ResumeVersion).filter(ResumeVersion.resume_id == resume_id).order_by(ResumeVersion.version_number.desc()).all()

    @staticmethod
    def latest_for_resume(db: Session, resume_id: int) -> Optional[ResumeVersion]:
        return db.query(ResumeVersion).filter(ResumeVersion.resume_id == resume_id).order_by(ResumeVersion.version_number.desc()).first()
