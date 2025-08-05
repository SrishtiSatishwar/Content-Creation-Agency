from agency_swarm.tools import BaseTool
from pydantic import Field
import os
from dotenv import load_dotenv
import logging
from textblob import TextBlob

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

class SentimentAnalyzer(BaseTool):
    """
    A tool to analyze the sentiment of text content.
    Returns a sentiment score (polarity between -1 and 1) and subjectivity score (0 to 1).
    """
    
    text: str = Field(
        ...,
        description="The text content to analyze for sentiment."
    )
    context: str = Field(
        ..., description="The context in which the text will be used (e.g., social media, blog, etc.)."
    )
    
    def run(self):
        """
        Analyze the sentiment of the provided text using TextBlob.
        Returns a JSON string containing sentiment polarity and subjectivity scores.
        """
        try:
            logger.info(f"\n=== Starting Sentiment Analysis ===")
            logger.info(f"Text length: {len(self.text)} characters")
            logger.info(f"Context: {self.context}")

            blob = TextBlob(self.text)
            sentiment = blob.sentiment
            
            result = {
                "polarity": sentiment.polarity,  # Range: -1 (negative) to 1 (positive)
                "subjectivity": sentiment.subjectivity,  # Range: 0 (objective) to 1 (subjective)
                "assessment": self._get_sentiment_assessment(sentiment.polarity)
            }
            
            analysis = str(result)

            logger.info(f"Sentiment Analysis Complete")
            logger.info(f"Analysis preview: {analysis[:200]}...")
            logger.info("=== End Sentiment Analysis ===\n")

            return analysis

        except Exception as e:
            logger.error(f"Error in sentiment analysis: {str(e)}")
            raise
    
    def _get_sentiment_assessment(self, polarity: float) -> str:
        """Helper method to convert polarity score to human-readable assessment."""
        if polarity > 0.5:
            return "Very Positive"
        elif polarity > 0:
            return "Slightly Positive"
        elif polarity == 0:
            return "Neutral"
        elif polarity > -0.5:
            return "Slightly Negative"
        else:
            return "Very Negative"

if __name__ == "__main__":
    # Test the tool
    test_texts = [
        "I absolutely love this product! It's amazing and life-changing!",
        "This is okay, but could be better.",
        "I'm very disappointed with the terrible service and poor quality."
    ]
    
    analyzer = SentimentAnalyzer(
        text=test_texts[0],
        context="social media"
    )
    print(f"Testing positive text: {analyzer.run()}\n")
    
    analyzer = SentimentAnalyzer(
        text=test_texts[1],
        context="blog"
    )
    print(f"Testing neutral text: {analyzer.run()}\n")
    
    analyzer = SentimentAnalyzer(
        text=test_texts[2],
        context="social media"
    )
    print(f"Testing negative text: {analyzer.run()}\n") 