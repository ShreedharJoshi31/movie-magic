from pydantic import BaseModel

# Pydantic model for creating a user (Signup)
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    location: str

    class Config:
        orm_mode = True

# Pydantic model for returning user info (used in response)
class UserOut(BaseModel):
    id: int
    username: str
    email: str
    location: str

    class Config:
        orm_mode = True

# Pydantic model for login (only email and password)
class UserLogin(BaseModel):
    email: str
    password: str
