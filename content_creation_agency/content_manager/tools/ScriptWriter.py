from agency_swarm.tools import BaseTool
from pydantic import Field
import os
from pathlib import Path
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

class ScriptWriter(BaseTool):
    """
    A tool that creates and edits script drafts in Markdown format.
    The tool saves the script to a file and returns the complete script content.
    """
    content: str = Field(
        ..., description="The complete script content in markdown format"
    )
    file_name: str = Field(
        ..., description="Name of the file to save the script"
    )

    def run(self):
        """
        Write or edit a script file in markdown format and return the complete content.
        The complete script content is returned to be displayed in the UI.
        """
        try:
            logger.info(f"\n=== Starting Script Writing ===")
            logger.info(f"Content length: {len(self.content)} characters")
            logger.info(f"File name: {self.file_name}")

            # Get the absolute path to the content_creation_agency directory
            base_dir = Path(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
            scripts_dir = base_dir / "scripts"
            
            # Ensure the scripts directory exists
            scripts_dir.mkdir(parents=True, exist_ok=True)

            # Add .md extension if not present
            if not self.file_name.endswith('.md'):
                self.file_name += '.md'

            # Create full file path
            file_path = scripts_dir / self.file_name

            # Write content to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(self.content)

            # Return the complete script content
            # This will be displayed in the UI
            logger.info(f"Script Writing Complete")
            logger.info(f"Script preview: {self.content[:200]}...")
            logger.info("=== End Script Writing ===\n")
            return self.content

        except Exception as e:
            logger.error(f"Error saving script: {str(e)}")
            raise

if __name__ == "__main__":
    # Test the tool
    writer = ScriptWriter(
        content="# Test Script\n\nThis is a test script in markdown format.",
        file_name="test_script"
    )
    print(writer.run()) 