from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
import uvicorn
import json
from . import models, schemas, auth, nlp_service
from .models import SessionLocal, init_db

# Initialize DB
init_db()

app = FastAPI(
    title="Restaurant Review Platform API",
    description="API for restaurant reviews with automatic NLP sentiment analysis",
    version="1.0.0"
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/register", response_model=schemas.Token)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = auth.get_password_hash(user.password)
    new_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login to get access token."""
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/restaurants/", response_model=schemas.RestaurantResponse)
def create_restaurant(
    restaurant: schemas.RestaurantCreate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    """Create a new restaurant (authenticated)."""
    current_user = auth.get_current_user(db, token)
    db_restaurant = models.Restaurant(
        name=restaurant.name,
        address=restaurant.address,
        cuisine_type=restaurant.cuisine_type
    )
    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)
    return db_restaurant

@app.get("/restaurants/", response_model=List[schemas.RestaurantResponse])
def get_restaurants(db: Session = Depends(get_db)):
    """Get all restaurants."""
    restaurants = db.query(models.Restaurant).all()
    return restaurants

@app.post("/reviews/", response_model=schemas.ReviewResponse)
def create_review(
    review: schemas.ReviewCreate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    """Create a review with automatic NLP analysis."""
    current_user = auth.get_current_user(db, token)
    
    restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == review.restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    # Perform NLP analysis
    analysis = nlp_service.NLPService.analyze_review(review.comment)
    
    db_review = models.Review(
        user_id=current_user.id,
        restaurant_id=review.restaurant_id,
        rating=review.rating,
        comment=review.comment,
        sentiment_polarity=analysis["sentiment_polarity"],
        sentiment_subjectivity=analysis["sentiment_subjectivity"],
        key_aspects=json.dumps(analysis["key_aspects"]) if analysis["key_aspects"] else None
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    
    nlp_service.NLPService.update_restaurant_rating(restaurant, db)
    
    return db_review

@app.get("/restaurants/{restaurant_id}/reviews", response_model=List[schemas.ReviewResponse])
def get_restaurant_reviews(restaurant_id: int, db: Session = Depends(get_db)):
    """Get reviews for a specific restaurant."""
    reviews = db.query(models.Review).filter(models.Review.restaurant_id == restaurant_id).all()
    return reviews

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)