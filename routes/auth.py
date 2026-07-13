from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database.connection import db
from schemas.user_schema import User

class Login(BaseModel):
    email: str
    password: str

router = APIRouter()

@router.post("/register")
def register(user: User):

    db.users.insert_one(user.model_dump())

    return {
        "message": "User Registered Successfully"
    }

@router.post("/login")
def login(user: Login):

    existing_user = db.users.find_one({
    "email": user.email,
    "password": user.password
})

    if not existing_user:
        raise HTTPException(
    status_code=401,
    detail="Invalid Email or Password"
    )

    return {
    "message": "Login Successful",
    "user": {
        "full_name": existing_user["full_name"],
        "email": existing_user["email"],
        "user_type": existing_user["user_type"]
    }
}