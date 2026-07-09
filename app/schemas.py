from pydantic import BaseModel, EmailStr


# ---------- Signup ----------

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


# ---------- Login ----------

class UserLogin(BaseModel):
    email: EmailStr
    password: str


# ---------- Response ----------

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True