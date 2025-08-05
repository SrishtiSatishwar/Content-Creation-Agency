from agency_swarm.tools import BaseTool
from pydantic import Field
import json
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
import pandas as pd

class TrendVisualizer(BaseTool):
    """
    A tool that creates visualizations of trend data and saves them as image files.
    """
    trend_data: dict = Field(
        ..., description="Dictionary containing trend data to visualize"
    )
    visualization_type: str = Field(
        default='line',
        description="Type of visualization (line, bar, heatmap)"
    )
    output_dir: str = Field(
        default='visualizations',
        description="Directory to save visualization files"
    )

    def run(self):
        """
        Create visualizations from trend data and save them as image files.
        """
        try:
            # Create output directory if it doesn't exist
            os.makedirs(self.output_dir, exist_ok=True)

            # Set style
            plt.style.use('default')  # Use default style instead of seaborn
            sns.set_theme(style="whitegrid")  # Set seaborn theme

            results = {
                "timestamp": datetime.now().isoformat(),
                "visualization_type": self.visualization_type,
                "generated_files": []
            }

            # Process interest over time data
            if "interest_over_time" in self.trend_data:
                interest_data = self.trend_data["interest_over_time"]
                if interest_data:
                    # Create DataFrame from interest data
                    df = pd.DataFrame(interest_data)
                    df.index = pd.to_datetime(df.index)

                    # Create line plot
                    plt.figure(figsize=(12, 6))
                    for column in df.columns:
                        plt.plot(df.index, df[column], label=column, marker='o')

                    plt.title('Interest Over Time')
                    plt.xlabel('Date')
                    plt.ylabel('Interest')
                    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
                    plt.tight_layout()

                    # Save plot
                    filename = f"{self.output_dir}/interest_over_time_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                    plt.savefig(filename, dpi=300, bbox_inches='tight')
                    plt.close()
                    results["generated_files"].append(filename)

            # Process keyword presence data if available
            if "keyword_presence" in self.trend_data:
                keyword_data = self.trend_data["keyword_presence"]
                if keyword_data:
                    # Create bar plot for keyword presence
                    plt.figure(figsize=(10, 6))
                    keywords = list(keyword_data.keys())
                    values = list(keyword_data.values())

                    sns.barplot(x=keywords, y=values)
                    plt.title('Keyword Presence Analysis')
                    plt.xlabel('Keywords')
                    plt.ylabel('Frequency')
                    plt.xticks(rotation=45)
                    plt.tight_layout()

                    # Save plot
                    filename = f"{self.output_dir}/keyword_presence_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                    plt.savefig(filename, dpi=300, bbox_inches='tight')
                    plt.close()
                    results["generated_files"].append(filename)

            # Create heatmap if data is suitable
            if self.visualization_type == 'heatmap' and "interest_over_time" in self.trend_data:
                interest_data = self.trend_data["interest_over_time"]
                if interest_data:
                    df = pd.DataFrame(interest_data)
                    
                    plt.figure(figsize=(12, 8))
                    sns.heatmap(df.corr(), annot=True, cmap='coolwarm', center=0)
                    plt.title('Correlation Heatmap of Trends')
                    plt.tight_layout()

                    # Save heatmap
                    filename = f"{self.output_dir}/correlation_heatmap_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                    plt.savefig(filename, dpi=300, bbox_inches='tight')
                    plt.close()
                    results["generated_files"].append(filename)
            print("Trend Visualizer - results: ", results)
            return json.dumps(results, indent=2)

        except Exception as e:
            error_data = {
                "error": f"Error creating visualizations: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
            print("Trend Visualizer - error_data: ", error_data)
            return json.dumps(error_data)

if __name__ == "__main__":
    # Test data
    test_data = {
        "interest_over_time": {
            "AI": {"2024-01-01": 75, "2024-01-02": 80, "2024-01-03": 85},
            "Machine Learning": {"2024-01-01": 65, "2024-01-02": 70, "2024-01-03": 75}
        },
        "keyword_presence": {
            "artificial intelligence": 10,
            "machine learning": 8,
            "deep learning": 6
        }
    }
    
    visualizer = TrendVisualizer(
        trend_data=test_data,
        visualization_type='line',
        output_dir='visualizations'
    )
    print(visualizer.run()) 