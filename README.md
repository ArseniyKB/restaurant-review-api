# Restaurant Review Platform API

A professional REST API for a restaurant review platform with automatic NLP sentiment analysis using TextBlob.

## Features
- User registration and JWT authentication
- CRUD for restaurants and reviews
- Automatic NLP analysis on reviews: sentiment polarity, subjectivity, key aspects extraction
- Average rating calculation for restaurants
- SQLite database (easy to swap to PostgreSQL)
- Well-structured, documented code with full docstrings
- Unit tests for NLP service

## Quick Start
```bash
git clone https://github.com/ArseniyKB/restaurant-review-api.git
cd restaurant-review-api
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Swagger UI: http://localhost:8000/docs

## Testing
```bash
pytest tests/ -v
```

Built professionally with FastAPI + SQLAlchemy.