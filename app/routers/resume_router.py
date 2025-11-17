from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.resume_service import create_resume_with_initial_version, add_new_version_and_set_active
from app.services.file_service import save_uploaded_file
from app.schemas.resume import ResumeCreate, ResumeRead

router = APIRouter()

@router.post("/resumes", response_model=ResumeRead)
def create_resume(payload: ResumeCreate, db: Session = Depends(get_db), current_user_id: int = 1):
    resume, ver = create_resume_with_initial_version(db, user_id=current_user_id, title=payload.title, file_name=payload.file_name)
    # return resume object — Pydantic will include versions
    return resume

@router.post("/resumes/{resume_id}/upload")
def upload_resume_file(resume_id: int, file: UploadFile = File(...), db: Session = Depends(get_db), current_user_id: int = 1):
    # Save uploaded file locally for now
    local_path = save_uploaded_file(file, file.filename)
    # Create new version and set active, html_content empty until conversion finishes
    ver = add_new_version_and_set_active(db, resume_id=resume_id, html_content="", raw_file_path=local_path)
    return {"message": "uploaded", "version_id": ver.id}
