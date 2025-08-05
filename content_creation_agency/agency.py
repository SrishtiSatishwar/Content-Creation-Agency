from agency_swarm import Agency
from content_manager.content_manager import ContentManager
from trend_analyzer.trend_analyzer import TrendAnalyzer
from youtube_analyzer.youtube_analyzer import YouTubeAnalyzer
from dotenv import load_dotenv
import traceback

load_dotenv()

print("\n=== Initializing Content Creation Agency ===")

try:
    # Initialize agents
    print("\nInitializing agents...")
    content_manager = ContentManager()
    trend_analyzer = TrendAnalyzer()
    youtube_analyzer = YouTubeAnalyzer()
    print("All agents initialized successfully")

    # Create agency with communication flows
    print("\nSetting up agency communication flows...")
    agency = Agency(
        [
            content_manager,  # Content Manager is the entry point for user communication
            [content_manager, youtube_analyzer],  # Content Manager can communicate with YouTube Analyzer
            [content_manager, trend_analyzer],  # Content Manager can communicate with Trend Analyzer
            [youtube_analyzer, trend_analyzer]  # YouTube Analyzer can communicate with Trend Analyzer
        ],
        shared_instructions="agency_manifesto.md",
        temperature=0.7,
        max_prompt_tokens=25000
    )
    print("Agency setup complete")

    def log_communication(sender, receiver, message):
        print(f"\n=== Communication: {sender} -> {receiver} ===")
        print(f"Message preview: {message[:200]}...")
        print("=== End Communication ===\n")

    # Add communication logging
    agency.on_message = log_communication

    print("=== Content Creation Agency Initialization Complete ===\n")

except Exception as e:
    error_msg = f"Error initializing agency: {str(e)}\n{traceback.format_exc()}"
    print(f"ERROR: {error_msg}")
    raise

if __name__ == "__main__":
    try:
        print("\n=== Starting Agency Demo ===")
        agency.run_demo()
        print("=== Agency Demo Complete ===\n")
    except Exception as e:
        error_msg = f"Error running agency demo: {str(e)}\n{traceback.format_exc()}"
        print(f"ERROR: {error_msg}")
        raise 