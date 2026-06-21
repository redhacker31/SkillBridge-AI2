from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.auth import hash_password, verify_password

def register_user(db: Session, user_data: UserCreate) -> User:
    """
    Register a new user.
    Raises HTTPException if the email already exists.
    """
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email address already exists.",
        )
    
    # Hash password
    hashed_password = hash_password(user_data.password)
    
    # Create new User object
    db_user = User(
        full_name=user_data.full_name,
        email=user_data.email,
        password_hash=hashed_password,
    )
    
    # Save to database
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

def authenticate_user(db: Session, email: str, password: str) -> User | None:
    """
    Authenticate a user by email and password.
    Returns the User model instance if valid, otherwise None.
    """
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    
    if not verify_password(password, user.password_hash):
        return None
        
    return user
