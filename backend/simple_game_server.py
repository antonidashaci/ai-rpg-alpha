#!/usr/bin/env python3
"""
Ultra-simple HTTP server for AI-RPG-Alpha
Just get it working without complex imports
"""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import sys
import os
import mimetypes

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ai.gemini_client import GeminiClient

class SimpleGameHandler(BaseHTTPRequestHandler):
    """Simple HTTP request handler"""
    
    def __init__(self, *args, **kwargs):
        self.ai_client = GeminiClient()
        super().__init__(*args, **kwargs)
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/':
            self.serve_file('frontend/index.html')
        elif parsed_path.path == '/health':
            self.send_json_response({
                "status": "healthy",
                "version": "0.2.0"
            })
        else:
            # Serve static files
            file_path = parsed_path.path.lstrip('/')
            if file_path.startswith('frontend/'):
                self.serve_file(file_path)
            else:
                frontend_path = f'frontend/{file_path}'
                if os.path.exists(frontend_path):
                    self.serve_file(frontend_path)
                else:
                    self.send_error(404)
    
    def serve_file(self, file_path):
        """Serve a static file"""
        try:
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    content = f.read()
                
                mime_type, _ = mimetypes.guess_type(file_path)
                if mime_type is None:
                    mime_type = 'application/octet-stream'
                
                self.send_response(200)
                self.send_header('Content-Type', mime_type)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-Length', str(len(content)))
                self.end_headers()
                self.wfile.write(content)
            else:
                self.send_error(404)
        except Exception as e:
            print(f"Error serving file {file_path}: {e}")
            self.send_error(500)
    
    def do_POST(self):
        """Handle POST requests"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/turn':
            try:
                # Read request
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                request_data = json.loads(post_data.decode('utf-8'))
                
                print(f"Request received: {request_data}")
                
                # Extract data
                player_name = request_data.get('player_name', 'Adventurer')
                choice = request_data.get('choice', 'start')
                scenario = request_data.get('scenario', 'northern_realms')
                
                # Simple context based on scenario
                scenario_contexts = {
                    'northern_realms': {
                        'setting': 'epic fantasy realm with dragons and magic',
                        'tone': 'heroic and adventurous',
                        'starting_location': 'the village of Ironhold'
                    },
                    'whispering_town': {
                        'setting': 'mysterious New England town with cosmic horror elements',
                        'tone': 'eerie and unsettling',
                        'starting_location': 'the outskirts of Arkham'
                    },
                    'neo_tokyo': {
                        'setting': 'cyberpunk future with neon lights and corporate control',
                        'tone': 'gritty and high-tech',
                        'starting_location': 'the Shibuya Undercity'
                    }
                }
                
                context = scenario_contexts.get(scenario, scenario_contexts['northern_realms'])
                
                # Generate response
                story_response = self.ai_client.generate_story_response(
                    player_name=player_name,
                    choice=choice,
                    context={
                        'setting': context['setting'],
                        'tone': context['tone'],
                        'location': context['starting_location'],
                        'turn_number': 1,
                        'risk_level': 'calm'
                    }
                )
                
                self.send_json_response(story_response)
                
            except Exception as e:
                print(f"ERROR: {str(e)}")
                import traceback
                traceback.print_exc()
                
                # Send error as JSON instead of HTML
                error_response = {
                    'narrative': 'Something went wrong with the game server. Please try again.',
                    'choices': ['Try again', 'Restart game'],
                    'metadata': {'error': str(e)}
                }
                self.send_json_response(error_response)
        else:
            self.send_error(404)
    
    def send_json_response(self, data):
        """Send JSON response"""
        response = json.dumps(data)
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(response.encode('utf-8'))

def run_server(port=8000):
    """Run the server"""
    try:
        httpd = HTTPServer(('127.0.0.1', port), SimpleGameHandler)
        print(f"🎮 AI-RPG-Alpha Simple Server")
        print(f"🌐 Running at: http://127.0.0.1:{port}")
        print(f"🎯 Ready to play!")
        print("=" * 40)
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
    except Exception as e:
        print(f"❌ Server error: {e}")

if __name__ == "__main__":
    run_server() 