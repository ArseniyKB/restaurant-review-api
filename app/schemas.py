from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

class UserCreate(BaseModel):
    """Schema for user registration."""
    email: EmailStr
    password: str
    full_name: Optional[str] = None

class Token(BaseModel):
    """JWT token response."""
    access_token: str
    token_type: str = "bearer"

class RestaurantCreate(BaseModel):
    """Schema for creating restaurant."""
    name: str
    address: Optional[str] = None
    cuisine_type: Optional[str] = None

class RestaurantResponse(BaseModel):
    """Response schema for restaurant."""
    id: int
    name: str
    address: Optional[str]
    cuisine_type: Optional[str]
    average_rating: float
    
    class Config:
        from_attributes = True

class ReviewCreate(BaseModel):
    """Schema for creating review."""
    restaurant_id: int
    rating: float
    comment: str

class ReviewResponse(BaseModel):
    """Response schema for review including NLP analysis."""
    id: int
    user_id: int
    restaurant_id: int
    rating: float
    comment: str
    created_at: datetime
    sentiment_polarity: float
    sentiment_subjectivity: float
    key_aspects: Optional[str]
    
    class Config:
        from_attributes = True