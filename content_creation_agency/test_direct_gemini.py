#!/usr/bin/env python3
"""
Test script to verify Direct Gemini implementation
"""

import os
import sys
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_google_api_key():
    """Test that Google API key is available"""
    print("Testing Google API key...")
    
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("✗ GOOGLE_API_KEY not found in environment variables")
        return False
    
    print(f"✓ GOOGLE_API_KEY found: {api_key[:10]}...")
    return True

def test_gemini_import():
    """Test that Gemini can be imported and configured"""
    print("\nTesting Gemini import and configuration...")
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
        model = genai.GenerativeModel('gemini-1.5-pro')
        print("✓ Gemini imported and configured successfully")
        return True
    except Exception as e:
        print(f"✗ Failed to import/configure Gemini: {e}")
        return False

def test_direct_gemini_response():
    """Test that we can get a response from Gemini directly"""
    print("\nTesting direct Gemini response...")
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        response = model.generate_content("Hello, can you help me create a video script?")
        print(f"✓ Direct Gemini response received: {response.text[:100]}...")
        return True
    except Exception as e:
        print(f"✗ Failed to get direct Gemini response: {e}")
        return False

def test_flask_app_import():
    """Test that the Flask app can be imported"""
    print("\nTesting Flask app import...")
    
    try:
        # This will test if the app can be imported without errors
        import app_gemini_direct
        print("✓ Direct Gemini Flask app imported successfully")
        return True
    except Exception as e:
        print(f"✗ Failed to import Direct Gemini Flask app: {e}")
        return False

def main():
    """Main test function"""
    print("=== Direct Gemini Setup Test ===\n")
    
    # Test API key
    if not test_google_api_key():
        print("\nPlease set your GOOGLE_API_KEY in the .env file")
        return False
    
    # Test Gemini import
    if not test_gemini_import():
        print("\nGemini import test failed")
        return False
    
    # Test direct Gemini response
    if not test_direct_gemini_response():
        print("\nDirect Gemini response test failed")
        return False
    
    # Test Flask app import
    if not test_flask_app_import():
        print("\nFlask app import test failed")
        return False
    
    print("\n=== All tests passed! ===")
    print("You can now run the Direct Gemini version with: python app_gemini_direct.py")
    print("This version runs on port 8002 and uses ONLY Gemini - no OpenAI!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 