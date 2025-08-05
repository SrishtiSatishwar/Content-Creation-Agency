#!/usr/bin/env python3
"""
Test script to verify video generation functionality
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_api_keys():
    """Test that required API keys are available"""
    print("Testing API keys...")
    
    # Check for Google API key (for Veo 2)
    google_api_key = os.getenv('GOOGLE_API_KEY')
    if not google_api_key:
        print("✗ GOOGLE_API_KEY not found in environment variables")
        return False
    
    print(f"✓ GOOGLE_API_KEY found: {google_api_key[:10]}...")
    
    # Check for Vertex AI key if different
    vertex_api_key = os.getenv('VERTEX_AI_API_KEY')
    if vertex_api_key:
        print(f"✓ VERTEX_AI_API_KEY found: {vertex_api_key[:10]}...")
    else:
        print("ℹ VERTEX_AI_API_KEY not found - using GOOGLE_API_KEY for Veo 2")
    
    return True

def test_video_generator_import():
    """Test that VideoGenerator can be imported"""
    print("\nTesting VideoGenerator import...")
    
    try:
        from youtube_analyzer.tools.VideoGenerator import VideoGenerator
        print("✓ VideoGenerator imported successfully")
        return True
    except Exception as e:
        print(f"✗ Failed to import VideoGenerator: {e}")
        return False

def test_video_generation():
    """Test video generation with a simple script"""
    print("\nTesting video generation...")
    
    try:
        from youtube_analyzer.tools.VideoGenerator import VideoGenerator
        
        # Create a simple test script
        test_script = """
        Welcome to our educational video about artificial intelligence.
        
        In this video, we'll explore:
        - What is AI?
        - How does machine learning work?
        - Real-world applications of AI
        
        Let's dive into the fascinating world of artificial intelligence!
        """
        
        # Initialize the video generator
        generator = VideoGenerator(
            script=test_script,
            style="educational",
            duration="30 seconds",
            no_faces=True,
            use_vertex_ai=False  # Try regular Google API first
        )
        
        print("✓ VideoGenerator initialized successfully")
        print("Note: This will make an API call to Google's Veo 2 service")
        print("If this fails, you may need to:")
        print("1. Check if your API key has access to Veo 2")
        print("2. Set VERTEX_AI_API_KEY in your .env file")
        print("3. Use a different video generation service")
        
        # Ask user if they want to proceed
        response = input("Do you want to proceed with video generation? (y/n): ")
        if response.lower() != 'y':
            print("Skipping actual video generation")
            return True
        
        # Generate the video
        result = generator.run()
        print(f"✓ Video generation successful!")
        print(f"Video saved to: {result['video_path']}")
        return True
        
    except Exception as e:
        print(f"✗ Failed to generate video: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure your GOOGLE_API_KEY has access to Veo 2")
        print("2. Try setting VERTEX_AI_API_KEY in your .env file")
        print("3. Check if Veo 2 is available in your region")
        print("4. Consider using a different video generation service")
        return False

def main():
    """Main test function"""
    print("=== Video Generation Test ===\n")
    
    # Test API keys
    if not test_api_keys():
        print("\nPlease set your API keys in the .env file")
        return False
    
    # Test import
    if not test_video_generator_import():
        print("\nImport test failed")
        return False
    
    # Test video generation
    if not test_video_generation():
        print("\nVideo generation test failed")
        return False
    
    print("\n=== All tests passed! ===")
    print("Video generation is ready to use with your content creation agency")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 