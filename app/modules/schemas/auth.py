from pydantic import BaseModel, EmailStr, Field

class LoginSchema(BaseModel):
    email: EmailStr = Field(..., description="Email pengguna")
    password: str = Field(..., min_length=6, description="Kata sandi pengguna")

class RegisterSchema(BaseModel):
    name: str = Field(..., description="Nama lengkap pengguna")
    email: EmailStr = Field(..., description="Email pengguna")
    password: str = Field(..., min_length=6, description="Kata sandi pengguna")
    password_confirmation: str = Field(..., min_length=6, description="Konfirmasi kata sandi pengguna")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "john.doe@example.com",
                "password": "password123",
                "password_confirmation": "password123"
            }
        }

class TokenSchema(BaseModel):
    access_token: str = Field(..., description="Token akses yang digunakan untuk otentikasi")
    token_type: str = Field(..., description="Jenis token, biasanya 'bearer'")
    user: dict = Field(..., description="Informasi pengguna yang telah diautentikasi")