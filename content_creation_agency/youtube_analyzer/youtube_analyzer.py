from agency_swarm import Agent
import json
import traceback
import time

class YouTubeAnalyzer(Agent):
    def __init__(self):
        print("\n=== YouTube Analyzer Agent Initialization ===")
        self.initialization_time = time.time()
        self.message_count = 0
        self.last_message_time = None
        
        super().__init__(
            name="YouTube Analyzer",
            description="Analyzes YouTube channel performance, audience demographics, and competitor content to identify opportunities and gaps.",
            instructions="./instructions.md",
            tools_folder="./tools",
            temperature=0.5,
            max_prompt_tokens=25000
        )
        
        # Log available tools
        print("\nAvailable Tools:")
        for tool in self.tools:
            print(f"- {tool.__class__.__name__}")
        
        print(f"YouTube Analyzer Agent initialized successfully at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("=== End YouTube Analyzer Initialization ===\n")

    def _process_message(self, message):
        """
        Override the message processing to add logging
        """
        self.message_count += 1
        self.last_message_time = time.time()
        
        print(f"\n=== YouTube Analyzer Processing Message #{self.message_count} ===")
        print(f"Time since initialization: {self.last_message_time - self.initialization_time:.2f} seconds")
        print(f"Received message: {message[:200]}...")  # Print first 200 chars of message
        
        try:
            # Log available tools before processing
            print("\nAvailable Tools for this message:")
            for tool in self.tools:
                print(f"- {tool.__class__.__name__}")
            
            # Process the message using parent class method
            print("\nProcessing message with parent class...")
            response = super()._process_message(message)
            
            print("\nYouTube Analyzer Response:")
            print(f"Response type: {type(response)}")
            print(f"Response preview: {str(response)[:200]}...")
            
            # Validate response format
            if not isinstance(response, str):
                print("WARNING: Response is not a string")
                response = str(response)
            
            if not response.startswith("YouTube Analysis Results:"):
                print("WARNING: Response does not follow required format")
                response = "YouTube Analysis Results:\n" + response
            
            if not response.endswith("Analysis Complete"):
                print("WARNING: Response does not end with 'Analysis Complete'")
                response += "\nAnalysis Complete"
            
            # Log message processing steps
            print("\nMessage Processing Steps:")
            if hasattr(self, '_processing_steps'):
                for step in self._processing_steps:
                    print(f"- {step}")
            
            print(f"=== End YouTube Analyzer Processing (Message #{self.message_count}) ===\n")
            return response
            
        except Exception as e:
            error_msg = f"Error in YouTube Analyzer: {str(e)}\n{traceback.format_exc()}"
            print(f"ERROR: {error_msg}")
            return f"YouTube Analysis Results:\nError occurred during analysis: {str(e)}\nAnalysis Complete"

    def get_state(self):
        """
        Returns the current state of the YouTube Analyzer
        """
        return {
            "initialization_time": self.initialization_time,
            "message_count": self.message_count,
            "last_message_time": self.last_message_time,
            "available_tools": [tool.__class__.__name__ for tool in self.tools]
        }