from pydantic import BaseModel

class User(BaseModel):
    full_name: str
    phone_number: str
    email: str
    password: str
    user_type: str