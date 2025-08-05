from agency_swarm.tools import BaseTool
from pydantic import Field
import os
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

class TavilySearchTool(BaseTool):
    """
    A tool that searches the web for latest AI trends using Tavily API.
    """
    query: str = Field(
        ..., description="Search query for AI trends"
    )
    search_depth: str = Field(
        default="basic",
        description="Level of search depth (basic/comprehensive)"
    )

    def run(self):
        """
        Search the web using Tavily API and return results.
        """
        try:
            client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
            
            # Validate search_depth
            if self.search_depth not in ["basic", "comprehensive"]:
                self.search_depth = "basic"
            
            # Set search parameters
            search_params = {
                "query": self.query,
                "search_depth": self.search_depth,
                "include_answer": True,
                "include_raw_content": False,
                "include_images": False
            }
            
            # Perform search
            response = client.search(**search_params)
            print("Tavily Search Tool - response: ", response)
            return response
            
        except Exception as e:
            print("Tavily Search Tool - error: ", e)
            return f"Error performing search: {str(e)}"

if __name__ == "__main__":
    # Test the tool
    searcher = TavilySearchTool(
        query="Latest developments in artificial intelligence 2024",
        search_depth="comprehensive"
    )
    print(searcher.run()) 