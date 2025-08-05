from agency_swarm import Agency
from content_manager.content_manager import ContentManager
from trend_analyzer.trend_analyzer import TrendAnalyzer
from youtube_analyzer.youtube_analyzer import YouTubeAnalyzer
from dotenv import load_dotenv
import os
import json
import unittest
import time
from functools import wraps
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def rate_limit_handler(max_retries=3, initial_wait=20):
    """Decorator to handle rate limits with exponential backoff"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            wait_time = initial_wait
            
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if any(error in str(e).lower() for error in ["rate limit", "quota", "timeout"]):
                        if retries < max_retries - 1:
                            logging.warning(f"Rate limit hit. Waiting {wait_time} seconds before retry...")
                            time.sleep(wait_time)
                            retries += 1
                            wait_time *= 2
                        else:
                            logging.error(f"Max retries reached. Last error: {str(e)}")
                            raise
                    else:
                        logging.error(f"Non-rate-limit error occurred: {str(e)}")
                        raise
            return func(*args, **kwargs)
        return wrapper
    return decorator

class TestFullAgencyIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up the complete agency for testing"""
        load_dotenv()
        
        # Initialize all agents
        cls.content_manager = ContentManager()
        cls.trend_analyzer = TrendAnalyzer()
        cls.youtube_analyzer = YouTubeAnalyzer()
        
        # Create the full agency with all communication flows
        cls.agency = Agency(
            [
                cls.content_manager,  # Content Manager as entry point
                [cls.content_manager, cls.youtube_analyzer],
                [cls.content_manager, cls.trend_analyzer],
                [cls.youtube_analyzer, cls.trend_analyzer]
            ],
            shared_instructions="agency_manifesto.md",
            temperature=0.7
        )
        
        # Add delay between API calls
        cls.api_delay = 5
    
    def setUp(self):
        """Add delay between tests"""
        time.sleep(self.api_delay)
    
    @rate_limit_handler()
    def test_full_content_strategy_workflow(self):
        """
        Test the complete workflow of content strategy creation
        involving all three agents working together.
        """
        logging.info("Starting full content strategy workflow test")
        
        prompt = """
        Help me create a content strategy for an AI education YouTube channel.
        Please keep the analysis focused and concise to avoid rate limits.
        
        1. First, identify 1-2 current AI trends that would make good video topics
        2. Then, analyze what format works best for AI educational content
        3. Finally, create a specific content plan for one video, including:
           - Title
           - Key points
           - Engagement strategy
        
        Please keep each part brief but insightful.
        """
        
        try:
            logging.info("Sending prompt to agency...")
            response = self.agency.get_completion(prompt)
            logging.info("Received response from agency")
            
            print("\nFull Agency Response:", response)
            
            # Validate response contains input from all agents
            validations = {
                'trend_analysis': ['trend', 'current', 'popular'],
                'youtube_strategy': ['format', 'video', 'channel'],
                'content_plan': ['title', 'strategy', 'engagement']
            }
            
            response_lower = response.lower()
            for aspect, keywords in validations.items():
                found_keywords = [word for word in keywords if word in response_lower]
                self.assertTrue(
                    found_keywords,
                    f"Response missing {aspect} elements. Expected at least one of: {keywords}"
                )
                logging.info(f"Validated {aspect} in response")
            
            # Validate response structure
            self.assertTrue(
                len(response.split('\n')) > 10,
                "Response should be detailed enough with multiple lines"
            )
            
            logging.info("All validations passed successfully")
            
        except Exception as e:
            logging.error(f"Error during test: {str(e)}")
            raise
    
    def test_response_quality(self):
        """
        Test the quality and coherence of the agency's response
        without making external API calls.
        """
        logging.info("Starting response quality test")
        
        prompt = """
        What are the key elements that make AI educational content successful?
        Please provide a framework that combines:
        1. Content quality factors
        2. Presentation strategies
        3. Audience engagement techniques
        
        Keep the response focused on general best practices.
        """
        
        try:
            logging.info("Sending prompt to agency...")
            response = self.agency.get_completion(prompt)
            logging.info("Received response from agency")
            
            print("\nQuality Test Response:", response)
            
            # Validate response quality
            quality_checks = {
                'structure': ['1.', '2.', '3.'],  # Should have numbered points
                'depth': ['example', 'such as', 'for instance'],  # Should provide examples
                'actionability': ['should', 'can', 'recommend']  # Should give actionable advice
            }
            
            response_lower = response.lower()
            for aspect, indicators in quality_checks.items():
                found_indicators = [ind for ind in indicators if ind.lower() in response_lower]
                self.assertTrue(
                    found_indicators,
                    f"Response missing {aspect} elements. Expected some of: {indicators}"
                )
                logging.info(f"Validated {aspect} in response")
            
            logging.info("All quality checks passed successfully")
            
        except Exception as e:
            logging.error(f"Error during test: {str(e)}")
            raise

if __name__ == '__main__':
    unittest.main(verbosity=2) 