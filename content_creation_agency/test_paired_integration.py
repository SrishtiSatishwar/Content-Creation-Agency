from agency_swarm import Agency
from content_manager.content_manager import ContentManager
from trend_analyzer.trend_analyzer import TrendAnalyzer
from youtube_analyzer.youtube_analyzer import YouTubeAnalyzer
from dotenv import load_dotenv
import os
import json
import unittest
import time

class TestPairedAgentIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up for all tests"""
        load_dotenv()
        
        # Initialize all agents but we'll pair them differently in each test
        cls.content_manager = ContentManager()
        cls.trend_analyzer = TrendAnalyzer()
        cls.youtube_analyzer = YouTubeAnalyzer()
    
    def setUp(self):
        """Add delay between tests to avoid rate limits"""
        time.sleep(5)
    
    def test_content_manager_trend_analyzer_pair(self):
        """Test integration between Content Manager and Trend Analyzer"""
        print("\nTesting Content Manager <-> Trend Analyzer Integration")
        
        # Create agency with just these two agents
        agency = Agency(
            [
                self.content_manager,  # Content Manager as entry point
                [self.content_manager, self.trend_analyzer]  # Direct communication flow
            ],
            shared_instructions="agency_manifesto.md",
            temperature=0.7
        )
        
        # Simple prompt that requires both agents
        prompt = """
        What are the current trending topics in AI technology? 
        Based on these trends, suggest 3 content ideas that would be engaging.
        """
        
        response = agency.get_completion(prompt)
        print("\nResponse:", response)
        
        # Basic validation
        self.assertIn("trend", response.lower())
        self.assertIn("content", response.lower())
        
    def test_youtube_trend_analyzer_pair(self):
        """Test integration between YouTube Analyzer and Trend Analyzer"""
        print("\nTesting YouTube Analyzer <-> Trend Analyzer Integration")
        
        # Create agency with just these two agents
        agency = Agency(
            [
                self.youtube_analyzer,  # YouTube Analyzer as entry point
                [self.youtube_analyzer, self.trend_analyzer]  # Direct communication flow
            ],
            shared_instructions="agency_manifesto.md",
            temperature=0.7
        )
        
        # Modified prompt to be less dependent on API success
        prompt = """
        For AI technology content on YouTube:
        1. What type of AI content typically performs well?
        2. What engagement strategies would you recommend?
        
        Please provide general insights without needing to analyze specific channels.
        """
        
        try:
            response = agency.get_completion(prompt)
            print("\nResponse:", response)
            
            # More flexible validation
            self.assertTrue(
                any(word in response.lower() for word in ["content", "video", "channel", "strategy"])
            )
        except Exception as e:
            print(f"\nError during test: {str(e)}")
            raise

    def test_content_manager_youtube_analyzer_pair(self):
        """Test integration between Content Manager and YouTube Analyzer"""
        print("\nTesting Content Manager <-> YouTube Analyzer Integration")
        
        # Create agency with just these two agents
        agency = Agency(
            [
                self.content_manager,  # Content Manager as entry point
                [self.content_manager, self.youtube_analyzer]  # Direct communication flow
            ],
            shared_instructions="agency_manifesto.md",
            temperature=0.7
        )
        
        # Prompt that requires both agents to work together but doesn't rely on API calls
        prompt = """
        I want to create AI-focused YouTube content. Please:
        1. Suggest a video format that would work well
        2. Outline key points to cover
        3. Recommend engagement strategies
        
        Focus on general recommendations without needing to analyze specific channels.
        """
        
        try:
            response = agency.get_completion(prompt)
            print("\nResponse:", response)
            
            # Basic validation
            self.assertIn("content", response.lower())
            self.assertIn("video", response.lower())
            self.assertIn("suggest", response.lower())
        except Exception as e:
            print(f"\nError during test: {str(e)}")
            raise

if __name__ == '__main__':
    unittest.main(verbosity=2) 