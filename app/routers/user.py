from typing import List, Optional
from fastapi import APIRouter, HTTPException, status

from app.models import User


router = APIRouter(prefix="/user", tags=["user"])


@router.post("", status_code=status.HTTP_200_OK)
def create_user(user: User):
    """Create user"""
    from app.database import db
    user_id = db.create_user(user.model_dump(exclude_unset=True))
    return {"message": "User created", "id": user_id}


@router.post("/createWithArray", status_code=status.HTTP_200_OK)
def create_users_with_array_input(users: List[User]):
    """Creates list of users with given input array"""
    from app.database import db
    for user in users:
        db.create_user(user.model_dump(exclude_unset=True))
    return {"message": "Users created successfully"}


@router.post("/createWithList", status_code=status.HTTP_200_OK)
def create_users_with_list_input(users: List[User]):
    """Creates list of users with given input array"""
    return create_users_with_array_input(users)


@router.get("/login")
def login_user(username: str, password: str):
    """Logs user into the system"""
    from app.database import db
    user = db.get_user_by_credentials(username, password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username/password supplied")
    return {"message": "Logged in successfully", "session": f"session-{username}"}


@router.get("/logout")
def logout_user():
    """Logs out current logged in user session"""
    return {"message": "Logged out successfully"}


@router.get("/{username}", response_model=User)
def get_user_by_name(username: str):
    """Get user by user name"""
    from app.database import db
    user = db.get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{username}")
def update_user(username: str, user: User):
    """Updated user"""
    from app.database import db
    existing = db.get_user_by_username(username)
    if not existing:
        raise HTTPException(status_code=404, detail="User not found")
    db.update_user(username, user.model_dump(exclude_unset=True))
    return db.get_user_by_username(username)


@router.delete("/{username}")
def delete_user(username: str):
    """Delete user"""
    from app.database import db
    if not db.delete_user(username):
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}
