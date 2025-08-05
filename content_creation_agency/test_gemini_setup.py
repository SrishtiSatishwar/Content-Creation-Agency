#!/usr/bin/env python3
"""
Test script to verify Gemini agent setup
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_gemini_imports():
    """Test that all Gemini agents can be imported"""
    print("Testing Gemini agent imports...")
    
    try:
        from content_manager_gemini.content_manager_gemini import ContentManagerGemini
        print("✓ ContentManagerGemini imported successfully")
    except Exception as e:
        print(f"✗ Failed to import ContentManagerGemini: {e}")
        return False
    
    try:
        from trend_analyzer_gemini.trend_analyzer_gemini import TrendAnalyzerGemini
        print("✓ TrendAnalyzerGemini imported successfully")
    except Exception as e:
        print(f"✗ Failed to import TrendAnalyzerGemini: {e}")
        return False
    
    try:
        from youtube_analyzer_gemini.youtube_analyzer_gemini import YouTubeAnalyzerGemini
        print("✓ YouTubeAnalyzerGemini imported successfully")
    except Exception as e:
        print(f"✗ Failed to import YouTubeAnalyzerGemini: {e}")
        return False
    
    return True

def test_gemini_initialization():
    """Test that Gemini agents can be initialized"""
    print("\nTesting Gemini agent initialization...")
    
    try:
        from content_manager_gemini.content_manager_gemini import ContentManagerGemini
        content_manager = ContentManagerGemini()
        print("✓ ContentManagerGemini initialized successfully")
    except Exception as e:
        print(f"✗ Failed to initialize ContentManagerGemini: {e}")
        return False
    
    try:
        from trend_analyzer_gemini.trend_analyzer_gemini import TrendAnalyzerGemini
        trend_analyzer = TrendAnalyzerGemini()
        print("✓ TrendAnalyzerGemini initialized successfully")
    except Exception as e:
        print(f"✗ Failed to initialize TrendAnalyzerGemini: {e}")
        return False
    
    try:
        from youtube_analyzer_gemini.youtube_analyzer_gemini import YouTubeAnalyzerGemini
        youtube_analyzer = YouTubeAnalyzerGemini()
        print("✓ YouTubeAnalyzerGemini initialized successfully")
    except Exception as e:
        print(f"✗ Failed to initialize YouTubeAnalyzerGemini: {e}")
        return False
    
    return True

def test_google_api_key():
    """Test that Google API key is available"""
    print("\nTesting Google API key...")
    
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("✗ GOOGLE_API_KEY not found in environment variables")
        return False
    
    print(f"✓ GOOGLE_API_KEY found: {api_key[:10]}...")
    return True

def main():
    """Main test function"""
    print("=== Gemini Setup Test ===\n")
    
    # Test API key
    if not test_google_api_key():
        print("\nPlease set your GOOGLE_API_KEY in the .env file")
        return False
    
    # Test imports
    if not test_gemini_imports():
        print("\nImport tests failed")
        return False
    
    # Test initialization
    if not test_gemini_initialization():
        print("\nInitialization tests failed")
        return False
    
    print("\n=== All tests passed! ===")
    print("You can now run the Gemini version with: python app_gemini.py")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 