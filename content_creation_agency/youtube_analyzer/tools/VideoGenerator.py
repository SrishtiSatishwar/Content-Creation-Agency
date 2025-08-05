from agency_swarm.tools import BaseTool
from pydantic import Field
import os
from dotenv import load_dotenv
import logging
import time
from pathlib import Path
from google import genai
from google.genai import types

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

class VideoGenerator(BaseTool):
    """
    A tool that generates videos using Google's Veo 2 API with the current Google GenAI client.
    Takes a script and generates a video with specified style and duration.
    Saves the video to the videos directory and returns the path.
    """
    script: str = Field(
        ..., description="The script content to generate video from"
    )
    style: str = Field(
        default="educational",
        description="The style of the video (e.g., educational, entertaining, professional)"
    )
    duration: str = Field(
        default="5 minutes",
        description="The target duration of the video (will be converted to seconds)"
    )
    no_faces: bool = Field(
        default=True,
        description="Whether to prevent generation of faces in the video"
    )
    aspect_ratio: str = Field(
        default="16:9",
        description="Video aspect ratio (16:9 or 9:16)"
    )

    def _parse_duration(self, duration_str):
        """Convert duration string to seconds"""
        duration_str = duration_str.lower().strip()
        if "second" in duration_str:
            return int(duration_str.split()[0])
        elif "minute" in duration_str:
            minutes = int(duration_str.split()[0])
            return min(minutes * 60, 8)  # Cap at 8 seconds (Veo 2 limit)
        else:
            return 5  # Default to 5 seconds

    def run(self):
        """
        Generate a video using Veo 2 API with the current Google GenAI client.
        Saves the video to the videos directory and returns the path.
        """
        try:
            logger.info(f"\n=== Starting Video Generation ===")
            logger.info(f"Script length: {len(self.script)} characters")
            logger.info(f"Style: {self.style}")
            logger.info(f"Duration: {self.duration}")
            logger.info(f"No faces: {self.no_faces}")
            logger.info(f"Aspect ratio: {self.aspect_ratio}")

            # Get API key from environment
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("GOOGLE_API_KEY not found in environment variables")

            # Initialize Google GenAI client
            client = genai.Client(api_key=api_key)
            
            # Convert duration to seconds
            duration_seconds = self._parse_duration(self.duration)
            
            # Prepare the prompt
            prompt = f"""Create a {self.style} video with the following script:
            {self.script}
            
            Important instructions:
            - Duration should be approximately {self.duration}
            - DO NOT generate or show any human faces
            - Use abstract visuals, animations, and text overlays
            - Focus on concepts and ideas rather than people
            - Use professional transitions and effects
            - Maintain a {self.style} tone throughout
            """

            logger.info(f"Making request to Veo 2 API...")
            logger.info(f"Prompt: {prompt[:200]}...")
            logger.info("This will take 2-3 minutes...")

            # Generate video using the current API
            operation = client.models.generate_videos(
                model="veo-2.0-generate-001",  # Current Veo 2 model name
                prompt=prompt,
                config=types.GenerateVideosConfig(
                    person_generation="dont_allow" if self.no_faces else "allow_adult",
                    aspect_ratio=self.aspect_ratio,
                    duration_seconds=duration_seconds,
                    number_of_videos=1,
                    enhance_prompt=True
                ),
            )
            
            logger.info("Operation started. Polling for completion...")
            
            # Poll for completion
            while not operation.done:
                logger.info("Still generating... (checking again in 20 seconds)")
                time.sleep(20)
                operation = client.operations.get(operation)
            
            logger.info("Video generation completed!")
            
            # Create videos directory if it doesn't exist
            videos_dir = Path("content_creation_agency/videos")
            videos_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate unique filename based on timestamp
            timestamp = int(time.time())
            video_filename = f"video_{timestamp}.mp4"
            video_path = videos_dir / video_filename
            
            # Save generated videos
            if operation.response and operation.response.generated_videos:
                for n, generated_video in enumerate(operation.response.generated_videos):
                    # Download the video file
                    client.files.download(file=generated_video.video)
                    generated_video.video.save(str(video_path))
                    
                    logger.info(f"✅ Video saved as: {video_path}")
                    logger.info(f"📁 File size: {len(generated_video.video.video_bytes) / (1024*1024):.1f} MB")
                
                logger.info("=== End Video Generation ===\n")
                
                return {
                    "status": "success",
                    "video_path": str(video_path),
                    "file_size_mb": len(generated_video.video.video_bytes) / (1024*1024),
                    "duration_seconds": duration_seconds,
                    "aspect_ratio": self.aspect_ratio
                }
            else:
                logger.error("❌ No video data found in response")
                raise Exception("No video data found in response")

        except Exception as e:
            logger.error(f"❌ Error generating video: {e}")
            logger.error("\nTroubleshooting:")
            logger.error("1. Make sure your GOOGLE_API_KEY is valid")
            logger.error("2. Ensure you have access to Veo 2 in Google AI Studio")
            logger.error("3. Check your API quota/billing is sufficient")
            logger.error("4. Try again in a few minutes if resources are constrained")
            raise

if __name__ == "__main__":
    # Test the tool
    generator = VideoGenerator(
        script="""Welcome to our educational video about artificial intelligence.
        
        In this video, we'll explore:
        - What is AI?
        - How does machine learning work?
        - Real-world applications of AI
        
        Let's dive into the fascinating world of artificial intelligence!""",
        style="educational",
        duration="5 seconds",
        no_faces=True,
        aspect_ratio="16:9"
    )
    result = generator.run()
    print(f"Video saved to: {result['video_path']}") 