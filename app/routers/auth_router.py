from fastapi import APIRouter , Depends , HTTPException, status 
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user import UserCreate , UserRead 
from app.services import auth_service 
from app.respositories import user_repo 

router = APIRouter() 

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