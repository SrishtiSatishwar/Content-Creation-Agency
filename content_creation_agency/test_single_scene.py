import os
import time
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

def test_single_scene():
    """
    Test generating a single scene video to verify the system works.
    """
    try:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        client = genai.Client(api_key=api_key)
        scenes_dir = Path("content_creation_agency/scenes")
        scenes_dir.mkdir(parents=True, exist_ok=True)
        
        # Simple test prompt (people-free)
        test_prompt = "Abstract digital visualization of artificial intelligence concepts with flowing data streams and neural network patterns, educational style. NO people, faces, or human figures. Use abstract visuals, animations, and text overlays only."
        
        logger.info(f"Testing with prompt: {test_prompt}")
        
        # Generate video using Veo 2
        operation = client.models.generate_videos(
            model="veo-2.0-generate-001",
            prompt=test_prompt,
            config=types.GenerateVideosConfig(
                person_generation="dont_allow",
                aspect_ratio="16:9",
                duration_seconds=5,
                number_of_videos=1,
                enhance_prompt=True
            ),
        )
        
        logger.info("Test video generation started. Polling for completion...")
        
        # Poll for completion
        while not operation.done:
            logger.info("Still generating... (checking again in 20 seconds)")
            time.sleep(20)
            operation = client.operations.get(operation)
        
        logger.info("Test video generation completed!")
        
        # Save the video
        if operation.response and operation.response.generated_videos:
            logger.info(f"Found {len(operation.response.generated_videos)} generated videos")
            
            for n, generated_video in enumerate(operation.response.generated_videos):
                test_filename = f"test_scene_{int(time.time())}.mp4"
                test_path = scenes_dir / test_filename
                
                logger.info(f"Downloading test video to {test_path}")
                
                try:
                    # Download and save the video
                    client.files.download(file=generated_video.video)
                    generated_video.video.save(str(test_path))
                    
                    logger.info(f"✅ Test video saved as: {test_path}")
                    logger.info(f"📁 File size: {len(generated_video.video.video_bytes) / (1024*1024):.1f} MB")
                    
                    return True
                    
                except Exception as save_error:
                    logger.error(f"❌ Error saving test video: {save_error}")
                    return False
        else:
            logger.error("❌ No video data found in response")
            logger.error(f"Response: {operation.response}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error in test: {e}")
        return False

if __name__ == "__main__":
    success = test_single_scene()
    if success:
        print("✅ Test successful! Check the scenes directory for the test video.")
    else:
        print("❌ Test failed. Check the logs above.") 