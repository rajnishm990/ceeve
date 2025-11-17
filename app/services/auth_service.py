from datetime import datetime , timedelta
from typing import Optional 
from passlib.context import CryptContext 
from jose import jwt , JWTError 
from app.core.config import settings
from app.respositories.user_repo import UserRepository
from sqlalchemy.orm import Session 


pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = settings.JWT_ALGORITHM
SECRET_KEY = settings.JWT_SECRET
ACCESS_TOKEN_EXPIRE_MINUTES = settings.JWT_EXPIRY_MINUTES

def hash_password(password:str) -> str:
    return pwd_ctx.hash(password)

def verify_password(plain:str, hashed:str) -> bool:
    return pwd_ctx.verify(plain,hashed)

def create_access_token(data:dict , expires_delta: Optional[timedelta]=None) :
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def authenticate_user(db:Session, email:str , password:str):
    user = UserRepository.get_by_email(db , email=email)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user

def create_user(db:Session , username:str , email:str , password: str):
    if UserRepository.get_by_email(db, email=email):
        raise ValueError("Email already in use")
    if UserRepository.get_by_username(db, username):
        raise ValueError("Username already in use")
    hashed = hash_password(password)
    user = UserRepository.create(db, username=username, email=email, password_hash=hashed)
    return user

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None