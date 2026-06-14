# Restaurant Review Platform API

A professional REST API for a restaurant review platform with automatic NLP sentiment analysis using TextBlob.

## Features
- User registration and JWT authentication
- CRUD for restaurants and reviews
- Automatic NLP analysis on reviews: sentiment polarity, subjectivity, key aspects extraction
- Average rating calculation for restaurants
- SQLite database (easy to swap to PostgreSQL)
- Well-structured, documented code

## Project Structure (Improved)
```
restaurant_review_api/
├── .env.example
├── .gitignore
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   └── nlp_service.py
├── tests/
│   ├── __init__.py
│   └── test_nlp.py
├── requirements.txt
├── README.md
├── .github/
│   └── workflows/
│       └── ci.yml      # GitHub Actions CI
└── restaurant.db       # (gitignored)
```

**Upcoming improvements (partially applied):**
- Better folder structure (routers/services planned)
- Environment configuration with `.env`
- GitHub Actions for CI/CD
- Enhanced security and error handling
- Pagination, advanced NLP (future)

## Installation
1. `cd restaurant_review_api`
2. `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and update secrets
4. `uvicorn app.main:app --reload`

## Testing & CI
- Local: `pytest tests/ -v`
- GitHub Actions automatically runs on push/PR

## Next Steps
See the tips in previous conversation for more enhancements.