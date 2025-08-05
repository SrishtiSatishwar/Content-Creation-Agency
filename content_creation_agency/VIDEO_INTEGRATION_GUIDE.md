# Video Generation Integration Guide

This guide explains how to use the video generation feature in the Content Creation Agency. The system now uses Google's Veo 2 API with the current Google GenAI client for reliable video generation.

## Overview

The video generation feature allows you to create videos from scripts using Google's Veo 2 AI model. The system supports:
- Text-to-video generation
- Customizable video styles and durations
- Face-free content generation (complies with content policies)
- Multiple aspect ratios (16:9, 9:16)
- Automatic video saving and file management

## API Endpoints

All three backend versions support video generation:

### 1. Original OpenAI Framework (Port 8000)
```bash
POST http://localhost:8000/api/generate-video
```

### 2. Gemini Agency-Swarm Framework (Port 8001)
```bash
POST http://localhost:8001/api/generate-video
```

### 3. Direct Gemini Framework (Port 8002)
```bash
POST http://localhost:8002/api/generate-video
```

## Request Format

```json
{
  "script": "Your video script content here...",
  "style": "educational",
  "duration": "5 seconds",
  "no_faces": true,
  "aspect_ratio": "16:9"
}
```

### Parameters

- **script** (required): The text content to generate video from
- **style** (optional): Video style - "educational", "entertaining", "professional" (default: "educational")
- **duration** (optional): Video duration - "5 seconds", "8 seconds" (default: "5 seconds")
- **no_faces** (optional): Prevent face generation (default: true)
- **aspect_ratio** (optional): "16:9" or "9:16" (default: "16:9")

## Response Format

```json
{
  "status": "success",
  "video_path": "content_creation_agency/videos/video_1750870932.mp4",
  "file_size_mb": 4.0,
  "duration_seconds": 5,
  "aspect_ratio": "16:9",
  "message": "Video generated successfully",
  "timestamp": "2024-06-25T10:02:12.345678"
}
```

## Frontend Integration

### JavaScript Example

```javascript
async function generateVideo(script, style = 'educational', duration = '5 seconds') {
  try {
    const response = await fetch('http://localhost:8002/api/generate-video', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        script: script,
        style: style,
        duration: duration,
        no_faces: true,
        aspect_ratio: '16:9'
      })
    });

    const result = await response.json();
    
    if (result.status === 'success') {
      console.log('Video generated:', result.video_path);
      console.log('File size:', result.file_size_mb, 'MB');
      return result;
    } else {
      throw new Error(result.error);
    }
  } catch (error) {
    console.error('Video generation failed:', error);
    throw error;
  }
}

// Usage example
generateVideo(
  "Welcome to our educational video about artificial intelligence. In this video, we'll explore what AI is and how it works.",
  "educational",
  "5 seconds"
).then(result => {
  // Handle successful video generation
  displayVideo(result.video_path);
}).catch(error => {
  // Handle error
  showError(error.message);
});
```

### React Component Example

```jsx
import React, { useState } from 'react';

function VideoGenerator({ script, onVideoGenerated }) {
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState(null);

  const generateVideo = async () => {
    setIsGenerating(true);
    setError(null);

    try {
      const response = await fetch('http://localhost:8002/api/generate-video', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          script: script,
          style: 'educational',
          duration: '5 seconds',
          no_faces: true,
          aspect_ratio: '16:9'
        })
      });

      const result = await response.json();
      
      if (result.status === 'success') {
        onVideoGenerated(result);
      } else {
        setError(result.error);
      }
    } catch (error) {
      setError(error.message);
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div>
      <button 
        onClick={generateVideo} 
        disabled={isGenerating}
      >
        {isGenerating ? 'Generating Video...' : 'Generate Video'}
      </button>
      
      {error && <div className="error">{error}</div>}
      
      {isGenerating && (
        <div className="loading">
          Video generation in progress... This may take 2-3 minutes.
        </div>
      )}
    </div>
  );
}
```

## Environment Variables

Make sure your `.env` file contains:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

The system uses the Google GenAI API with Veo 2 model, which requires:
- A valid Google API key
- Access to Veo 2 in Google AI Studio
- Sufficient API quota/billing

## Video Storage

Generated videos are automatically saved to:
```
content_creation_agency/videos/
```

Files are named with timestamps for uniqueness:
```
video_1750870932.mp4
```

## Technical Details

### Video Generation Process

1. **Script Processing**: The system enhances your script with style-specific instructions
2. **API Request**: Sends request to Google's Veo 2 API using the current GenAI client
3. **Polling**: Monitors generation progress (takes 2-3 minutes)
4. **Download**: Downloads the generated video file
5. **Storage**: Saves to the videos directory with metadata

### Supported Features

- **Duration**: 5-8 seconds (Veo 2 limit)
- **Aspect Ratios**: 16:9 (landscape), 9:16 (portrait)
- **Face Generation**: Can be disabled for content policy compliance
- **Prompt Enhancement**: Automatically improves prompts for better results
- **Error Handling**: Comprehensive error messages and troubleshooting

## Troubleshooting

### Common Issues

1. **API Key Error**
   - Ensure `GOOGLE_API_KEY` is set in your `.env` file
   - Verify the key is valid and has Veo 2 access

2. **Quota Exceeded**
   - Check your Google AI Studio quota
   - Wait a few minutes before retrying

3. **Generation Timeout**
   - Video generation takes 2-3 minutes
   - The system automatically polls for completion

4. **File Not Found**
   - Videos are saved in `content_creation_agency/videos/`
   - Check the returned `video_path` in the response

### Error Messages

- `"GOOGLE_API_KEY not found"`: Set your API key in `.env`
- `"No video data found"`: Generation failed, try again
- `"Operation timeout"`: Generation took too long, retry

## Best Practices

1. **Script Length**: Keep scripts concise (100-500 characters work best)
2. **Style Consistency**: Use consistent style descriptions
3. **Face-Free Content**: Enable `no_faces: true` for broader distribution
4. **Error Handling**: Always handle potential errors in frontend code
5. **User Feedback**: Show progress indicators during generation

## Testing

Test the video generation with a simple script:

```bash
curl -X POST http://localhost:8002/api/generate-video \
  -H "Content-Type: application/json" \
  -d '{
    "script": "A beautiful sunset over the ocean with gentle waves",
    "style": "educational",
    "duration": "5 seconds"
  }'
```

This should return a successful response with the video path and metadata. 