from typing import Optional 
from sqlalchemy.orm import Session
from app.models.user import User 


class UserRepository:
    """
    CRUD for User model
    """
    @staticmethod
    def get_by_id(db:Session , user_id:int) -> Optional[User]:
        return db.query(User).filter(User.id==user_id).first()

    @staticmethod
    def get_by_email(db:Session , email:str) -> Optional[User]:
        return db.query(User).filter(User.email==email).first()
    
    @staticmethod
    def get_by_username(db:Session , username:str) -> Optional[User]:
        return db.query(User).filter(User.username==username).first()
    
    @staticmethod
    def create(db: Session, *, username: str, email: str, password_hash: str)->str:
        new_user = User(username=username, email=email, password_hash=password_hash)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user 
    
    @staticmethod
    def delete(db:Session, user:User) -> None:
        db.delete(user)
        db.commit()


