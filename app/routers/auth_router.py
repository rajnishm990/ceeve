from fastapi import APIRouter , Depends , HTTPException, status 
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user import UserCreate , UserRead 
from app.services import auth_service 
from app.respositories import user_repo 

router = APIRouter() 

@router.post("/signup", response_model=UserRead)
def signup(payload: UserCreate, db: Session = Depends(get_db)):
    try:
        user = auth_service.create_user(db, username=payload.username, email=payload.email, password=payload.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return user

@router.post("/login")
def login(form_data: UserCreate, db: Session = Depends(get_db)):
    # minimal login illustrating token generation - you should use OAuth2PasswordRequestForm in production
    user = auth_service.authenticate_user(db, email=form_data.email, password=form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = auth_service.create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}
For production, use OAuth2PasswordRequestForm and proper token response model. This is a simple start to test signup/login.

b) app/routers/resume_router.py
python
Copy code
# app/routers/resume_router.py
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