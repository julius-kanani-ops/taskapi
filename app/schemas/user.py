from uuid import UUID
from pydantic import BaseModel, ConfigDict
from datetime import datetime



class UserBase(BaseModel):
    
    email: str
    phone_number: str | None = None


class UserCreate(UserBase):
    
    password: str


class UserResponse(UserBase):
    
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    
    email: str | None = None
    password: str | None = None
    is_active: bool | None = None
    phone_number: str | None = None


class TokenResponse(BaseModel):
    
    access_token: str
    token_type: str
