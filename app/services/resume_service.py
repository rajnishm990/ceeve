import secrets 
import string 
from sqlalchemy.orm import Session 
from typing import Optional 
from app.respositories.resume_repo import ResumeRepository
from app.respositories.resume_version_repo import ResumeVersionRepository 
from datetime import datetime 

SLUG_ALPHABET = string.ascii_letters + string.digits 

def _generate_slug(prefix:Optional[str]=None , length: int = 8):
    token = ''.join(secrets.choice(SLUG_ALPHABET) for _ in range(length))
    if prefix:
        return f"{prefix}-{token}"
    return token

def create_resume_with_initial_version(db: Session, user_id: int, title: str, file_name: Optional[str] = None):
    """
    Creates a Resume and an initial empty version (v1), sets it active.
    Returns (resume, version)
    """
    # create resume
    resume = ResumeRepository.create(db, user_id=user_id, title=title, file_name=file_name)
    # create initial version number 1
    ver = ResumeVersionRepository.add_version(db, resume_id=resume.id, version_number=1, html_content="")
    # set active
    resumed = ResumeRepository.set_active_version(db, resume=resume, version=ver)
    return resumed, ver

def add_new_version_and_set_active(db: Session, resume_id: int, html_content: str, raw_file_path: Optional[str] = None, html_file_path: Optional[str] = None):
    """
    Adds a new version (auto increments) and marks it as active.
    """
    latest = ResumeVersionRepository.latest_for_resume(db, resume_id=resume_id)
    next_ver = (latest.version_number + 1) if latest else 1
    ver = ResumeVersionRepository.add_version(
        db,
        resume_id=resume_id,
        version_number=next_ver,
        html_content=html_content,
        raw_file_path=raw_file_path,
        html_file_path=html_file_path
    )
    # set active
    resume = ResumeRepository.get(db, resume_id)
    if not resume:
        raise ValueError("Resume not found")
    ResumeRepository.set_active_version(db, resume=resume, version=ver)
    return ver

def ensure_shareable_slug(db: Session, resume_id: int, prefix: Optional[str] = None) -> str:
    """
    Ensure resume has unique shareable_slug. If not, generate and set one.
    """
    resume = ResumeRepository.get(db, resume_id)
    if not resume:
        raise ValueError("Resume not found")
    if resume.shareable_slug:
        return resume.shareable_slug

    # try until unique
    for _ in range(5):
        slug = _generate_slug(prefix)
        # quick uniqueness check
        found = db.query(type(resume)).filter_by(shareable_slug=slug).first()
        if not found:
            ResumeRepository.set_shareable_slug(db, resume, slug)
            return slug
    # fallback longer random slug
    slug = _generate_slug(prefix, length=16)
    ResumeRepository.set_shareable_slug(db, resume, slug)
    return slug
