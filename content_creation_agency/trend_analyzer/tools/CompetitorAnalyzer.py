from agency_swarm.tools import BaseTool
from pydantic import Field
import json
from datetime import datetime
import requests
import os
from dotenv import load_dotenv
import time

load_dotenv()

class CompetitorAnalyzer(BaseTool):
    """
    A tool that analyzes competitor content and trends using web search and analysis.
    """
    competitors: list = Field(
        ..., description="List of competitor names or websites to analyze"
    )
    industry_keywords: list = Field(
        ..., description="List of industry-specific keywords to track"
    )
    analysis_timeframe: str = Field(
        default='last_month',
        description="Timeframe for analysis (last_week, last_month, last_quarter)"
    )

    def _search_competitor(self, competitor, tavily_api_key):
        """Helper function to search for competitor information"""
        search_url = "https://api.tavily.com/search"
        
        # Create a more focused search query
        timeframe_map = {
            'last_week': 'past 7 days',
            'last_month': 'past 30 days',
            'last_quarter': 'past 90 days'
        }
        time_str = timeframe_map.get(self.analysis_timeframe, 'past 30 days')
        
        # Combine keywords into a search string
        keyword_str = ' OR '.join(self.industry_keywords)
        
        search_params = {
            "api_key": tavily_api_key,
            "query": f"({competitor}) ({keyword_str}) news announcements updates {time_str}",
            "search_depth": "advanced",
            "include_domains": [],
            "exclude_domains": [],
            "max_results": 10
        }

        try:
            response = requests.get(search_url, params=search_params)
            response.raise_for_status()  # Raise an exception for bad status codes
            search_data = response.json()
            print("Competitor Analyzer - search_data: ", search_data)
            
            if not search_data.get('results'):
                # Try a broader search if no results found
                search_params["query"] = f"{competitor} {time_str} news updates"
                time.sleep(1)  # Add a small delay between requests
                response = requests.get(search_url, params=search_params)
                response.raise_for_status()
                search_data = response.json()
            print("Competitor Analyzer - search_data: ", search_data)
            return search_data
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Search request failed: {str(e)}")

    def run(self):
        """
        Analyze competitors based on web presence and content trends.
        """
        print("Competitor Analyzer - running")
        try:
            # Initialize results dictionary
            results = {
                "timestamp": datetime.now().isoformat(),
                "competitors_analyzed": self.competitors,
                "analysis_timeframe": self.analysis_timeframe,
                "competitor_insights": {}
            }

            # Get Tavily API key for web search
            tavily_api_key = os.getenv('TAVILY_API_KEY')
            if not tavily_api_key:
                print("Competitor Analyzer - error: Tavily API key not found in environment variables")
                return json.dumps({
                    "error": "Tavily API key not found in environment variables",
                    "timestamp": datetime.now().isoformat()
                })

            # Analyze each competitor
            for competitor in self.competitors:
                competitor_data = {
                    "content_analysis": {},
                    "keyword_presence": {},
                    "recent_activities": []
                }

                try:
                    search_data = self._search_competitor(competitor, tavily_api_key)

                    if search_data.get('results'):
                        # Process search results
                        for result in search_data['results']:
                            # Extract relevant information
                            activity = {
                                "title": result.get('title', ''),
                                "snippet": result.get('snippet', ''),
                                "url": result.get('url', ''),
                                "date": result.get('published_date', ''),
                                "relevance_score": result.get('relevance_score', 0)
                            }
                            
                            # Only include results with good relevance
                            if activity["relevance_score"] > 0.5:
                                competitor_data["recent_activities"].append(activity)

                        # Analyze keyword presence in results
                        for keyword in self.industry_keywords:
                            keyword_count = sum(
                                1 for result in search_data['results']
                                if (
                                    keyword.lower() in result.get('title', '').lower() or
                                    keyword.lower() in result.get('snippet', '').lower()
                                )
                            )
                            competitor_data["keyword_presence"][keyword] = keyword_count

                        # Add content analysis summary
                        competitor_data["content_analysis"] = {
                            "total_results_found": len(search_data['results']),
                            "relevant_activities": len(competitor_data["recent_activities"]),
                            "most_mentioned_keywords": sorted(
                                competitor_data["keyword_presence"].items(),
                                key=lambda x: x[1],
                                reverse=True
                            )[:3]
                        }
                    else:
                        competitor_data["search_status"] = "No relevant results found"

                except Exception as e:
                    competitor_data["search_error"] = str(e)

                results["competitor_insights"][competitor] = competitor_data

            # Add summary statistics
            results["summary"] = {
                "total_competitors_analyzed": len(self.competitors),
                "competitors_with_data": sum(
                    1 for comp in results["competitor_insights"].values()
                    if comp.get("recent_activities")
                ),
                "total_activities_found": sum(
                    len(comp.get("recent_activities", []))
                    for comp in results["competitor_insights"].values()
                )
            }
            print("Competitor Analyzer - results: ", results)
            return json.dumps(results, indent=2)

        except Exception as e:
            error_data = {
                "error": f"Error analyzing competitors: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
            print("Competitor Analyzer - error_data: ", error_data)
            return json.dumps(error_data)

if __name__ == "__main__":
    # Test the tool
    analyzer = CompetitorAnalyzer(
        competitors=["OpenAI", "Anthropic", "Google AI"],
        industry_keywords=["artificial intelligence", "large language models", "AI safety"],
        analysis_timeframe="last_month"
    )
    print(analyzer.run()) 