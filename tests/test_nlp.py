"""
Unit tests for the NLPService in the Restaurant Review Platform.

These tests verify the automatic sentiment analysis and aspect extraction
using mocking to avoid NLTK data dependency issues in isolated environments.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from unittest.mock import patch, MagicMock
from app.nlp_service import NLPService

class MockBlob:
    """Mock for TextBlob to simulate behavior without external dependencies."""
    def __init__(self, text):
        self.sentiment = MagicMock()
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["excellent", "delicious", "amazing", "great"]):
            self.sentiment.polarity = 0.85
            self.sentiment.subjectivity = 0.75
        elif any(word in text_lower for word in ["worst", "terrible", "cold", "disappointing"]):
            self.sentiment.polarity = -0.75
            self.sentiment.subjectivity = 0.65
        else:
            self.sentiment.polarity = 0.1
            self.sentiment.subjectivity = 0.4
        
        self.noun_phrases = [
            MagicMock(string="great food"),
            MagicMock(string="excellent service"),
            MagicMock(string="pizza")
        ]

@patch('app.nlp_service.TextBlob', new=MockBlob)
def test_analyze_review_positive():
    """Test NLP analysis on a clearly positive review."""
    comment = "The food was absolutely delicious and the service was excellent!"
    result = NLPService.analyze_review(comment)
    
    assert "sentiment_polarity" in result
    assert "sentiment_subjectivity" in result
    assert "key_aspects" in result
    assert result["sentiment_polarity"] > 0.5
    assert isinstance(result["key_aspects"], list)

@patch('app.nlp_service.TextBlob', new=MockBlob)
def test_analyze_review_negative():
    """Test NLP analysis on a clearly negative review."""
    comment = "The worst experience ever. Food was cold and service was terrible."
    result = NLPService.analyze_review(comment)
    assert result["sentiment_polarity"] < -0.3

# ... (other tests abbreviated for brevity but full in repo)

@pytest.mark.parametrize("comment,expected_polarity_range", [
    ("Excellent food and great atmosphere!", (0.5, 1.0)),
    ("Terrible service, never coming back.", (-1.0, -0.3)),
    ("Okay meal, nothing special.", (-0.2, 0.2)),
])
@patch('app.nlp_service.TextBlob', new=MockBlob)
def test_analyze_review_parametrized(comment, expected_polarity_range):
    """Parametrized tests for different sentiment levels."""
    result = NLPService.analyze_review(comment)
    low, high = expected_polarity_range
    assert low <= result["sentiment_polarity"] <= high