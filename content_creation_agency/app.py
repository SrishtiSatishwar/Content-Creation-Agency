from flask import Flask, request, jsonify
from flask_cors import CORS
from agency_swarm import Agency
from content_manager.content_manager import ContentManager
from trend_analyzer.trend_analyzer import TrendAnalyzer
from youtube_analyzer.youtube_analyzer import YouTubeAnalyzer
from dotenv import load_dotenv
import os
from datetime import datetime
import uuid
import traceback
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure CORS
CORS(app, 
     resources={r"/api/*": {
         "origins": ["http://localhost:3000"],
         "methods": ["GET", "POST", "OPTIONS"],
         "allow_headers": ["Content-Type"]
     }},
     supports_credentials=True)

logger.info("=== Initializing Content Creation Agency ===")

try:
    # Initialize agents
    logger.info("Initializing agents...")
    content_manager = ContentManager()
    trend_analyzer = TrendAnalyzer()
    youtube_analyzer = YouTubeAnalyzer()
    logger.info("All agents initialized successfully")

    # Create agency with communication flows
    logger.info("Setting up agency communication flows...")
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

    def log_communication(sender, receiver, message):
        logger.info(f"\n=== Communication: {sender} -> {receiver} ===")
        logger.info(f"Message preview: {message[:200]}...")
        logger.info("=== End Communication ===\n")

    # Add communication logging
    agency.on_message = log_communication
    logger.info("Agency setup complete")

except Exception as e:
    logger.error(f"Error initializing agency: {str(e)}\n{traceback.format_exc()}")
    raise

# In-memory storage for chat sessions
chat_sessions = {}

@app.route('/api/chat', methods=['POST', 'OPTIONS'])
def chat():
    """
    Endpoint to handle chat interactions with the agency.
    Expects a JSON payload with 'message' and optional 'sessionId' fields.
    """
    if request.method == 'OPTIONS':
        return '', 200

    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'No message provided'}), 400

        logger.info(f"\n=== Processing Chat Request ===")
        logger.info(f"Message: {data['message'][:200]}...")

        # Get or create session ID
        session_id = data.get('sessionId')
        if not session_id or session_id not in chat_sessions:
            session_id = str(uuid.uuid4())
            chat_sessions[session_id] = []
            logger.info(f"Created new session: {session_id}")

        # Create message object
        user_message = {
            'id': str(uuid.uuid4()),
            'content': data['message'],
            'role': 'user',
            'timestamp': datetime.utcnow().isoformat()
        }

        # Add user message to session history
        chat_sessions[session_id].append(user_message)
        logger.info(f"Added user message to session {session_id}")

        # Get response from agency
        logger.info("Requesting response from agency...")
        response = agency.get_completion(data['message'])
        logger.info(f"Agency response received: {response[:200]}...")

        # Create response message object
        assistant_message = {
            'id': str(uuid.uuid4()),
            'content': response,
            'role': 'assistant',
            'timestamp': datetime.utcnow().isoformat()
        }

        # Add assistant message to session history
        chat_sessions[session_id].append(assistant_message)
        logger.info(f"Added assistant message to session {session_id}")
        
        logger.info("=== Chat Request Processing Complete ===\n")
        
        return jsonify({
            'response': response,
            'sessionId': session_id,
            'messageId': assistant_message['id'],
            'timestamp': assistant_message['timestamp'],
            'status': 'success'
        })

    except Exception as e:
        error_msg = f"Error in chat endpoint: {str(e)}\n{traceback.format_exc()}"
        logger.error(error_msg)
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/api/chat/history/<session_id>', methods=['GET', 'OPTIONS'])
def get_chat_history(session_id):
    """
    Endpoint to retrieve chat history for a specific session.
    """
    if request.method == 'OPTIONS':
        return '', 200

    try:
        if session_id not in chat_sessions:
            return jsonify({'error': 'Session not found'}), 404

        return jsonify({
            'history': chat_sessions[session_id],
            'status': 'success'
        })

    except Exception as e:
        error_msg = f"Error in chat history endpoint: {str(e)}\n{traceback.format_exc()}"
        logger.error(error_msg)
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/api/chat/session', methods=['POST', 'OPTIONS'])
def create_session():
    """
    Endpoint to create a new chat session.
    """
    if request.method == 'OPTIONS':
        return '', 200

    try:
        session_id = str(uuid.uuid4())
        chat_sessions[session_id] = []
        logger.info(f"Created new chat session: {session_id}")
        
        return jsonify({
            'sessionId': session_id,
            'status': 'success'
        })

    except Exception as e:
        error_msg = f"Error in create session endpoint: {str(e)}\n{traceback.format_exc()}"
        logger.error(error_msg)
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/api/generate-video', methods=['POST', 'OPTIONS'])
def generate_video():
    """
    Endpoint to generate a video from a script using the VideoGenerator tool.
    Expects a JSON payload with 'script' and optional 'style', 'duration' fields.
    """
    if request.method == 'OPTIONS':
        return '', 200

    try:
        data = request.get_json()
        if not data or 'script' not in data:
            return jsonify({'error': 'No script provided'}), 400

        logger.info(f"\n=== Processing Video Generation Request ===")
        logger.info(f"Script length: {len(data['script'])} characters")

        # Import the VideoGenerator tool
        from youtube_analyzer.tools.VideoGenerator import VideoGenerator

        # Extract parameters
        script = data['script']
        style = data.get('style', 'educational')
        duration = data.get('duration', '5 seconds')
        no_faces = data.get('no_faces', True)
        aspect_ratio = data.get('aspect_ratio', '16:9')

        logger.info(f"Style: {style}")
        logger.info(f"Duration: {duration}")
        logger.info(f"No faces: {no_faces}")
        logger.info(f"Aspect ratio: {aspect_ratio}")

        # Create video generator instance
        video_generator = VideoGenerator(
            script=script,
            style=style,
            duration=duration,
            no_faces=no_faces,
            aspect_ratio=aspect_ratio
        )

        # Generate the video
        logger.info("Starting video generation...")
        result = video_generator.run()
        logger.info(f"Video generation completed: {result['video_path']}")

        return jsonify({
            'status': 'success',
            'video_path': result['video_path'],
            'file_size_mb': result.get('file_size_mb', 0),
            'duration_seconds': result.get('duration_seconds', 5),
            'aspect_ratio': result.get('aspect_ratio', '16:9'),
            'message': 'Video generated successfully',
            'timestamp': datetime.utcnow().isoformat()
        })

    except Exception as e:
        error_msg = f"Error in video generation: {str(e)}\n{traceback.format_exc()}"
        logger.error(error_msg)
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint to verify the API is running.
    """
    return jsonify({
        'status': 'healthy',
        'message': 'Content Creation Agency API is running'
    })

if __name__ == '__main__':
    # Get port from environment variable or default to 8000
    port = int(os.getenv('PORT', 8000))
    logger.info(f"Starting Flask app on port {port}")
    # Run the Flask app
    app.run(host='0.0.0.0', port=port, debug=True) 