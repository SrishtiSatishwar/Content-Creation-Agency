from agency_swarm.tools import BaseTool
from pydantic import Field
from pytrends.request import TrendReq
import pandas as pd
import json
from datetime import datetime
import time
import random

class TrendAnalyzer(BaseTool):
    """
    A tool that analyzes keyword trends using pytrends.
    """
    keywords: list = Field(
        ..., description="List of keywords to analyze"
    )
    timeframe: str = Field(
        default='today 12-m',
        description="Time period for analysis (e.g., 'today 3-m', 'today 12-m', '2023-01-01 2024-01-01')"
    )

    def _try_request_with_backoff(self, pytrends, max_retries=3):
        """Helper function to handle rate limiting with exponential backoff"""
        for attempt in range(max_retries):
            try:
                # Build payload with a single keyword first
                keywords_to_analyze = self.keywords[:5] if len(self.keywords) > 5 else self.keywords
                if not keywords_to_analyze:
                    raise ValueError("No valid keywords to analyze")

                # Build payload
                pytrends.build_payload(
                    keywords_to_analyze,
                    cat=0,
                    timeframe=self.timeframe,
                    geo='',
                    gprop=''
                )

                # Get interest over time with error handling
                try:
                    interest_over_time_df = pytrends.interest_over_time()
                except Exception as e:
                    print(f"Warning: Could not get interest over time data: {str(e)}")
                    interest_over_time_df = pd.DataFrame()

                # Get related queries with error handling
                try:
                    related_queries = pytrends.related_queries()
                    print("Trend Analyzer - related_queries: ", related_queries)
                except Exception as e:
                    print(f"Warning: Could not get related queries: {str(e)}")
                    related_queries = {kw: None for kw in keywords_to_analyze}
                print("Trend Analyzer - interest_over_time_df: ", interest_over_time_df)
                return interest_over_time_df, related_queries

            except Exception as e:
                if "response with code 429" in str(e) and attempt < max_retries - 1:
                    # Calculate delay with exponential backoff and jitter
                    delay = (2 ** attempt) + random.uniform(0, 1)
                    print(f"Trend Analyzer - EXP BACKOFF sleeping for {delay} seconds")
                    time.sleep(delay)
                    continue
                else:
                    raise e

        raise Exception("Max retries exceeded")

    def run(self):
        """
        Analyze trends for the provided keywords using Google Trends.
        """
        print("Trend Analyzer - running")
        try:
            if not self.keywords:
                print("Trend Analyzer - no keywords provided for analysis")
                return json.dumps({
                    "error": "No keywords provided for analysis",
                    "timestamp": datetime.now().isoformat()
                })

            # Initialize pytrends with longer timeout but without retry configuration
            pytrends = TrendReq(hl='en-US', tz=360, timeout=(10, 25))
            
            # Ensure we have at least one keyword and no more than 5
            keywords_to_analyze = self.keywords[:5] if len(self.keywords) > 5 else self.keywords
            if not keywords_to_analyze:
                print("Trend Analyzer - no valid keywords to analyze")
                return json.dumps({
                    "error": "No valid keywords to analyze",
                    "timestamp": datetime.now().isoformat()
                })

            try:
                # Try request with backoff
                interest_over_time_df, related_queries = self._try_request_with_backoff(pytrends)

                # Process interest over time data
                interest_data = {}
                if not interest_over_time_df.empty:
                    # Convert the index to string format
                    interest_over_time_df.index = interest_over_time_df.index.strftime('%Y-%m-%d')
                    for column in interest_over_time_df.columns:
                        if column != 'isPartial':
                            interest_data[column] = interest_over_time_df[column].to_dict()

                # Process related queries with better error handling
                processed_queries = {}
                for kw in keywords_to_analyze:
                    queries = related_queries.get(kw)
                    if queries is not None:
                        top_df = queries.get('top', pd.DataFrame())
                        rising_df = queries.get('rising', pd.DataFrame())
                        
                        processed_queries[kw] = {
                            "top": top_df.to_dict('records') if not top_df.empty else [],
                            "rising": rising_df.to_dict('records') if not rising_df.empty else []
                        }
                    else:
                        processed_queries[kw] = {"top": [], "rising": []}

            except Exception as e:
                print("Trend Analyzer - error: ", e)
                return json.dumps({
                    "error": f"Error fetching trend data: {str(e)}",
                    "timestamp": datetime.now().isoformat(),
                    "analyzed_keywords": keywords_to_analyze
                })

            # Create the final result
            trend_data = {
                "interest_over_time": interest_data,
                "related_queries": processed_queries,
                "timestamp": datetime.now().isoformat(),
                "analyzed_keywords": keywords_to_analyze,
                "note": "Data shows relative search interest (0-100) over the specified timeframe."
            }
            print("Trend Analyzer - trend_data: ", trend_data)
            return json.dumps(trend_data, indent=2)

        except Exception as e:
            error_data = {
                "error": f"Error analyzing trends: {str(e)}",
                "timestamp": datetime.now().isoformat(),
                "attempted_keywords": self.keywords[:5] if self.keywords else []
            }
            print("Trend Analyzer - error_data: ", error_data)
            return json.dumps(error_data)

if __name__ == "__main__":
    # Test the tool
    analyzer = TrendAnalyzer(
        keywords=["artificial intelligence", "machine learning", "deep learning"],
        timeframe="today 3-m"
    )
    print(analyzer.run()) 