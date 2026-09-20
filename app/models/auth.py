from pydantic import BaseModel, EmailStr, Field

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=3)

class LoginResponse(BaseModel):
    user_id: int
    message: str