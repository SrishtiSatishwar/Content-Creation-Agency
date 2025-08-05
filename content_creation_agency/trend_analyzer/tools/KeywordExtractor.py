from agency_swarm.tools import BaseTool
from pydantic import Field
from collections import Counter
import json
import re

class KeywordExtractor(BaseTool):
    """
    A tool that extracts keywords from text content using basic text processing.
    """
    text: str = Field(
        ..., description="Text content to analyze"
    )
    max_keywords: int = Field(
        default=10,
        description="Maximum number of keywords to extract",
        gt=0
    )

    def run(self):
        """
        Extract keywords from the provided text using basic text processing.
        """
        try:
            # Basic stop words
            stop_words = {'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're",
                         "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he',
                         'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's",
                         'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which',
                         'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are',
                         'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do',
                         'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because',
                         'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against',
                         'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below',
                         'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again',
                         'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how',
                         'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such',
                         'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very',
                         's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've",
                         'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't",
                         'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn',
                         "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma',
                         'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan',
                         "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't",
                         'won', "won't", 'wouldn', "wouldn't"}
            
            # Clean and tokenize text
            text = self.text.lower()
            # Remove punctuation and split into words
            words = re.findall(r'\b\w+\b', text)
            
            # Filter words
            keywords = [word for word in words 
                       if len(word) > 2  # Only keep words longer than 2 characters
                       and word not in stop_words]
            
            # Count keyword frequencies
            keyword_freq = Counter(keywords)
            
            # Get top keywords
            top_keywords = dict(keyword_freq.most_common(self.max_keywords))
            print("Keyword Extractor - top_keywords: ", top_keywords)
            return json.dumps({
                "keywords": top_keywords,
                "total_keywords_found": len(keywords)
            })
            
        except Exception as e:
            print("Keyword Extractor - error: ", e)
            return json.dumps({
                "error": f"Error extracting keywords: {str(e)}",
                "keywords": {},
                "total_keywords_found": 0
            })

if __name__ == "__main__":
    # Test the tool
    test_text = """
    Artificial intelligence has made significant strides in 2024. 
    Machine learning models are becoming more sophisticated, and neural networks 
    are revolutionizing how we process data. Deep learning continues to push 
    the boundaries of what's possible in AI.
    """
    extractor = KeywordExtractor(text=test_text, max_keywords=5)
    print(extractor.run()) 