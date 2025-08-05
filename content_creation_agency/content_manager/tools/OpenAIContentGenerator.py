from agency_swarm.tools import BaseTool
from pydantic import Field
import os
from openai import OpenAI
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

class OpenAIContentGenerator(BaseTool):
    """
    A tool that generates creative content ideas using OpenAI's latest GPT-4 model via chat completions API.
    """
    prompt: str = Field(
        ..., description="The creative brief or context for content generation"
    )
    temperature: float = Field(
        default=0.7,
        description="Creativity level for generation (0.0-1.0)",
        ge=0.0,
        le=1.0
    )

    def run(self):
        """
        Generate content ideas using OpenAI's chat completions API.
        """
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        try:
            logger.info(f"\n=== Starting Content Generation ===")
            logger.info(f"Prompt: {self.prompt}")
            logger.info(f"Temperature: {self.temperature}")

            response = client.chat.completions.create(
                model="gpt-4-0125-preview",
                messages=[
                    {"role": "system", "content": "You are a creative content strategist specializing in AI and technology content."},
                    {"role": "user", "content": self.prompt}
                ],
                temperature=self.temperature
            )
            
            content = response.choices[0].message.content

            logger.info(f"Content Generation Complete")
            logger.info(f"Response preview: {content[:200]}...")
            logger.info("=== End Content Generation ===\n")

            return content
            
        except Exception as e:
            logger.error(f"Error generating content: {str(e)}")
            raise

if __name__ == "__main__":
    # Test the tool
    generator = OpenAIContentGenerator(
        prompt="Generate 3 video ideas about artificial intelligence trends in 2024",
        temperature=0.7
    )
    print(generator.run()) 