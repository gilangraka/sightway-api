from pydantic import BaseModel, EmailStr, Field

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: str = Field(..., min_length=2)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
