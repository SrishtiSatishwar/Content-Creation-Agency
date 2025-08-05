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

def retry_on_rate_limit(max_retries=3, initial_wait=20):
    """Decorator to retry functions on rate limit errors with exponential backoff"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            wait_time = initial_wait
            
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if "Rate limit reached" in str(e) and retries < max_retries - 1:
                        print(f"\nRate limit reached. Waiting {wait_time} seconds before retry...")
                        time.sleep(wait_time)
                        retries += 1
                        wait_time *= 2  # Exponential backoff
                    else:
                        raise
            return func(*args, **kwargs)
        return wrapper
    return decorator

class TestAgentIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up agents and agency for all tests"""
        load_dotenv()
        
        # Initialize agents
        cls.content_manager = ContentManager()
        cls.trend_analyzer = TrendAnalyzer()
        cls.youtube_analyzer = YouTubeAnalyzer()
        
        # Create agency with communication flows
        cls.agency = Agency(
            [
                cls.content_manager,  # Content Manager is the entry point
                [cls.content_manager, cls.youtube_analyzer],  # Content Manager -> YouTube Analyzer
                [cls.content_manager, cls.trend_analyzer],  # Content Manager -> Trend Analyzer
                [cls.youtube_analyzer, cls.trend_analyzer]  # YouTube Analyzer -> Trend Analyzer
            ],
            shared_instructions="agency_manifesto.md",
            temperature=0.7,
            max_prompt_tokens=25000
        )
    
    def setUp(self):
        """Add delay between tests to avoid rate limits"""
        time.sleep(5)  # 5-second delay between tests
    
    @retry_on_rate_limit()
    def test_content_ideation_flow(self):
        """Test the complete content ideation flow between agents"""
        prompt = """
        I need content ideas for a new AI technology YouTube channel. Please:
        1. Analyze current AI video trends
        2. Check successful AI channels' performance
        3. Generate content ideas based on the analysis
        4. Create a content strategy
        """
        
        response = self.agency.get_completion(prompt)
        
        # Verify response contains key elements
        self.assertIn("trends", response.lower())
        self.assertIn("content ideas", response.lower())
        self.assertIn("strategy", response.lower())

    @retry_on_rate_limit()
    def test_competitor_analysis_flow(self):
        """Test competitor analysis flow between agents"""
        prompt = """
        Analyze these AI YouTube channels and suggest content improvements:
        - Channels: 
          - Two Minute Papers (UCbfYPyITQ-7l4upoX8nvctg)
          - Yannic Kilcher (UCZHmQk67mSJgfCCTn7xBfew)
        - Look for:
          - Popular video topics
          - Engagement patterns
          - Content gaps
        - Suggest specific content ideas based on the analysis
        """
        
        response = self.agency.get_completion(prompt)
        
        # Verify response contains key elements
        self.assertIn("engagement", response.lower())
        self.assertIn("topics", response.lower())
        self.assertIn("suggestions", response.lower())

    @retry_on_rate_limit()
    def test_trend_based_content_optimization(self):
        """Test how agents work together to optimize content based on trends"""
        prompt = """
        For an AI tutorial video about GPT-4:
        1. Analyze current GPT-4 related trends
        2. Check how other channels cover GPT-4
        3. Suggest optimal:
           - Title
           - Description
           - Tags
           - Thumbnail concepts
        4. Recommend best posting time based on competitor analysis
        """
        
        response = self.agency.get_completion(prompt)
        
        # Verify response contains key elements
        self.assertIn("title", response.lower())
        self.assertIn("description", response.lower())
        self.assertIn("tags", response.lower())
        self.assertIn("thumbnail", response.lower())

    @retry_on_rate_limit()
    def test_content_performance_analysis(self):
        """Test analysis of existing content performance"""
        prompt = """
        Analyze this AI channel's performance and suggest improvements:
        - Channel: Two Minute Papers (UCbfYPyITQ-7l4upoX8nvctg)
        - Focus on:
          - Best performing video types
          - Audience engagement patterns
          - Content gaps compared to competitors
          - Trend alignment
        Provide specific recommendations for future content.
        """
        
        response = self.agency.get_completion(prompt)
        
        # Verify response contains key elements
        self.assertIn("performance", response.lower())
        self.assertIn("engagement", response.lower())
        self.assertIn("recommendations", response.lower())

    @retry_on_rate_limit()
    def test_trend_emergency_response(self):
        """Test how agents handle breaking AI news/trends"""
        prompt = """
        Breaking: OpenAI just released GPT-5! (hypothetical scenario)
        1. Analyze current social media trends about this
        2. Check how top AI channels are covering it
        3. Suggest:
           - Immediate content ideas
           - Unique angles to cover
           - Best format and timing
        Create an urgent content strategy to capitalize on this trend.
        """
        
        response = self.agency.get_completion(prompt)
        
        # Verify response contains key elements
        self.assertIn("trends", response.lower())
        self.assertIn("content", response.lower())
        self.assertIn("strategy", response.lower())

    @retry_on_rate_limit()
    def test_cross_agent_data_sharing(self):
        """Test how agents share and utilize data from each other"""
        prompt = """
        Create a comprehensive report about AI video content:
        1. Get current AI video trends from Trend Analyzer
        2. Get top AI channel performance from YouTube Analyzer
        3. Have Content Manager combine these insights to:
           - Identify content opportunities
           - Suggest content strategy
           - Recommend optimization tactics
        """
        
        response = self.agency.get_completion(prompt)
        
        # Verify response contains insights from all agents
        self.assertIn("trends", response.lower())
        self.assertIn("performance", response.lower())
        self.assertIn("strategy", response.lower())

if __name__ == '__main__':
    unittest.main(verbosity=2) 