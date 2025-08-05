from agency_swarm import Agency
from content_manager.content_manager import ContentManager
from trend_analyzer.trend_analyzer import TrendAnalyzer
from youtube_analyzer.youtube_analyzer import YouTubeAnalyzer
from dotenv import load_dotenv
import time
import json

def run_demo():
    """
    Enhanced demonstration script for presenting the Content Creation Agency
    Including script generation functionality
    """
    print("\n=== Content Creation Agency Demo ===\n")
    
    # Initialize agents
    print("Initializing agents...")
    content_manager = ContentManager()
    trend_analyzer = TrendAnalyzer()
    youtube_analyzer = YouTubeAnalyzer()
    
    # Create agency
    agency = Agency(
        [
            content_manager,
            [content_manager, youtube_analyzer],
            [content_manager, trend_analyzer],
            [youtube_analyzer, trend_analyzer]
        ],
        shared_instructions="agency_manifesto.md",
        temperature=0.7
    )
    
    # Demo 1: Quick Content Ideation
    print("\n=== Demo 1: Content Topic Ideation ===")
    prompt1 = """
    I want to create a neural networks tutorial video. 
    Suggest one trending topic and a video format that would work well.
    Keep it brief and focused.
    """
    
    print("\nPrompt:", prompt1)
    print("\nGenerating response...")
    response1 = agency.get_completion(prompt1)
    print("\nResponse:", response1)
    
    time.sleep(3)  # Pause for presentation flow
    
    # Demo 2: YouTube Strategy
    print("\n=== Demo 2: YouTube Optimization ===")
    prompt2 = """
    Based on the topic suggested above:
    1. Suggest an engaging title
    2. Recommend key engagement strategies
    3. Suggest video length and pacing
    Keep it focused on maximizing viewer retention.
    """
    
    print("\nPrompt:", prompt2)
    print("\nGenerating response...")
    response2 = agency.get_completion(prompt2)
    print("\nResponse:", response2)
    
    time.sleep(3)  # Pause for presentation flow
    
    # Demo 3: Script Generation
    print("\n=== Demo 3: Script Generation ===")
    prompt3 = """
    Create a detailed script for the neural network tutorial video we discussed.
    Include:
    1. Introduction hook
    2. Main content sections
    3. Engagement points (where to add visuals/examples)
    4. Conclusion and call-to-action
    
    Format the script with clear sections and timing guidelines.
    Keep the total length around 10-12 minutes.
    """
    
    print("\nPrompt:", prompt3)
    print("\nGenerating script...")
    response3 = agency.get_completion(prompt3)
    print("\nGenerated Script:", response3)
    
    # Save the generated script
    try:
        script_filename = "generated_script.md"
        with open(script_filename, "w") as f:
            f.write("# Generated YouTube Script\n\n")
            f.write("Generated on: " + time.strftime("%Y-%m-%d %H:%M:%S") + "\n\n")
            f.write(response3)
        print(f"\nScript saved to {script_filename}")
    except Exception as e:
        print(f"\nError saving script: {str(e)}")
    
    time.sleep(3)  # Pause for presentation flow
    
    # Demo 4: Script Enhancement
    print("\n=== Demo 4: Script Enhancement ===")
    prompt4 = """
    Review the script we just created and suggest:
    1. Points where to add B-roll or visual effects
    2. Potential places for audience interaction
    3. One technical demo or example to include
    
    Keep suggestions specific and actionable.
    """
    
    print("\nPrompt:", prompt4)
    print("\nGenerating enhancements...")
    response4 = agency.get_completion(prompt4)
    print("\nEnhancement Suggestions:", response4)
    
    # Save the enhanced version
    try:
        with open(script_filename, "a") as f:
            f.write("\n\n## Enhancement Suggestions\n\n")
            f.write(response4)
        print(f"\nEnhancements added to {script_filename}")
    except Exception as e:
        print(f"\nError saving enhancements: {str(e)}")

def main():
    load_dotenv()
    try:
        run_demo()
    except Exception as e:
        print(f"\nError during demo: {str(e)}")
        print("\nTip: If you hit rate limits, wait a few minutes and try again.")

if __name__ == "__main__":
    main() 