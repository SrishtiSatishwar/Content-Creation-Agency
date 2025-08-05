# Content Creation Agency

A collaborative AI agency for creating engaging AI-focused content through trend analysis, YouTube analytics, and data-driven content generation.

## Features

- **Content Manager**: Generates content ideas and creates scripts using OpenAI's GPT-4
- **Trend Analyzer**: Analyzes AI trends using web search, keyword extraction, and trend tracking
- **YouTube Analyzer**: Analyzes channel performance, audience engagement, and competitor content

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory with the following variables:
   ```
   # OpenAI API Key for content generation
   OPENAI_API_KEY=your_openai_api_key_here

   # Tavily API Key for web search
   TAVILY_API_KEY=your_tavily_api_key_here

   # YouTube API Key for analytics
   YOUTUBE_API_KEY=your_youtube_api_key_here
   ```

4. Run the agency:
   ```bash
   python agency.py
   ```

## Project Structure

```
content_creation_agency/
├── content_manager/
│   ├── tools/
│   │   ├── OpenAIContentGenerator.py
│   │   └── ScriptWriter.py
│   ├── content_manager.py
│   └── instructions.md
├── trend_analyzer/
│   ├── tools/
│   │   ├── TavilySearchTool.py
│   │   ├── KeywordExtractor.py
│   │   └── TrendAnalyzer.py
│   ├── trend_analyzer.py
│   └── instructions.md
├── youtube_analyzer/
│   ├── tools/
│   │   ├── ChannelAnalyzer.py
│   │   ├── VideoPerformanceAnalyzer.py
│   │   ├── CompetitorAnalyzer.py
│   │   └── CommentAnalyzer.py
│   ├── youtube_analyzer.py
│   └── instructions.md
├── agency.py
├── agency_manifesto.md
└── requirements.txt
```

## Usage

1. The Content Manager is the primary point of contact and coordinates with other agents
2. The Trend Analyzer provides insights about current AI trends and content opportunities
3. The YouTube Analyzer provides channel performance metrics and content gap analysis
4. All agents work together to create optimized content strategy

## API Keys

To use this agency, you'll need the following API keys:

1. **OpenAI API Key**: Get it from [OpenAI Platform](https://platform.openai.com/)
2. **Tavily API Key**: Get it from [Tavily](https://tavily.com/)
3. **YouTube API Key**: Get it from [Google Cloud Console](https://console.cloud.google.com/)

## Contributing

Feel free to submit issues and enhancement requests! 