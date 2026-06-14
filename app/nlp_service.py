from textblob import TextBlob
from typing import Dict

class NLPService:
    """Service for automatic NLP analysis of reviews."""
    
    @staticmethod
    def analyze_review(comment: str) -> Dict:
        """
        Perform sentiment analysis and basic key aspect extraction.
        
        Args:
            comment: The review text
            
        Returns:
            Dictionary with sentiment and aspects
        """
        blob = TextBlob(comment)
        
        # Sentiment analysis
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        # Simple key aspects extraction (noun phrases)
        aspects = [phrase.string for phrase in blob.noun_phrases if len(phrase.string) > 2]
        if len(aspects) > 5:
            aspects = aspects[:5]
        
        return {
            "sentiment_polarity": round(polarity, 2),
            "sentiment_subjectivity": round(subjectivity, 2),
            "key_aspects": aspects
        }
    
    @staticmethod
    def update_restaurant_rating(restaurant, db):
        """Update average rating for a restaurant based on reviews."""
        if not restaurant.reviews:
            return 0.0
        avg_rating = sum(r.rating for r in restaurant.reviews) / len(restaurant.reviews)
        restaurant.average_rating = round(avg_rating, 2)
        db.commit()
        return restaurant.average_rating