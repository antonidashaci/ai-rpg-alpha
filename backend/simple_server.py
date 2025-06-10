#!/usr/bin/env python3
"""
Simple HTTP server for AI-RPG-Alpha
"""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import sys
import os
import mimetypes

# Add current directory to path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ai.gemini_client import GeminiClient
from models.scenario_system import ScenarioManager, ScenarioConfig, QuestProgression

class GameRequestHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the game API"""
    
    def __init__(self, *args, **kwargs):
        self.ai_client = GeminiClient()
        self.active_scenarios = {}  # player_id -> ScenarioManager
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
            # Serve the main index.html file
            self.serve_file('frontend/index.html')
        elif parsed_path.path == '/health':
            self.send_json_response({
                "status": "healthy",
                "version": "0.1.0",
                "gemini_configured": True,
                "components": {
                    "ai_client": "connected"
                }
            })
        else:
            # Try to serve static files from frontend directory
            file_path = parsed_path.path.lstrip('/')
            if file_path.startswith('frontend/'):
                self.serve_file(file_path)
            else:
                # Try to serve from frontend directory
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
                
                # Get MIME type
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
                # Read request body
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                request_data = json.loads(post_data.decode('utf-8'))
                
                # Extract player info and choice
                player_id = request_data.get('player_id', 'Player')
                player_name = request_data.get('player_name', 'Adventurer')
                player_data = request_data.get('player_data', {})
                choice = request_data.get('choice', 'start')
                selected_scenario = request_data.get('scenario', 'northern_realms')
                
                print(f"Processing turn: Player={player_name}, Choice={choice}, Scenario={selected_scenario}")
                
                # Initialize or get scenario manager
                if player_id not in self.active_scenarios:
                    self.active_scenarios[player_id] = ScenarioManager(selected_scenario)
                
                scenario_manager = self.active_scenarios[player_id]
                
                # Update quest progression (initialize if needed)
                if not hasattr(scenario_manager, 'quest_arc') or scenario_manager.quest_arc is None:
                    from models.scenario_system import QuestProgression
                    scenario_manager.quest_arc = QuestProgression.get_scenario_quest_arc(selected_scenario)
                scenario_manager.quest_arc.turn_count += 1
                
                # Generate story response with scenario context
                if choice.lower() in ["start", "begin", "begin my adventure", "begin adventure"]:
                    # First turn - use scenario starting location and stats
                    context = scenario_manager.get_context_for_ai()
                    context.update({
                        'turn_number': 1,
                        'risk_level': 'calm',
                        'player_data': player_data,
                        'is_first_turn': True
                    })
                    story_response = self.ai_client.generate_story_response(
                        player_name=player_name,
                        choice=f"starting their {scenario_manager.scenario_data.genre.lower()} adventure",
                        context=context
                    )
                else:
                    # Regular turn with full scenario context
                    context = scenario_manager.get_context_for_ai()
                    context.update({
                        'turn_number': scenario_manager.quest_arc.turn_count,
                        'risk_level': 'mystery' if scenario_manager.quest_arc.turn_count > 5 else 'calm',
                        'player_data': player_data
                    })
                    
                    # Apply cosmic horror effects if applicable
                    if scenario_manager.sanity_state and scenario_manager.sanity_state.current_sanity < 70:
                        choice = scenario_manager.sanity_state.distort_reality(choice)
                    
                    story_response = self.ai_client.generate_story_response(
                        player_name=player_name,
                        choice=choice,
                        context=context
                    )
                    
                    # Apply sanity effects to response if cosmic horror
                    if scenario_manager.sanity_state:
                        story_response['narrative'] = scenario_manager.sanity_state.distort_reality(
                            story_response['narrative']
                        )
                
                # Send response
                response = {
                    'narrative': story_response['narrative'],
                    'choices': story_response['choices'],
                    'metadata': story_response['metadata']
                }
                
                self.send_json_response(response)
                
            except Exception as e:
                print(f"ERROR in /turn endpoint: {str(e)}")
                print(f"Request data: {request_data}")
                import traceback
                traceback.print_exc()
                self.send_error(500, str(e))
        else:
            self.send_error(404)
    
    def send_json_response(self, data):
        """Send a JSON response with proper headers"""
        response = json.dumps(data)
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(response.encode('utf-8'))
    
    def log_message(self, format, *args):
        """Custom log message to reduce output"""
        print(f"[{self.date_time_string()}] {format % args}")

def run_server(port=8000):
    """Run the HTTP server"""
    server_address = ('127.0.0.1', port)
    
    try:
        httpd = HTTPServer(server_address, GameRequestHandler)
        print(f"AI-RPG-Alpha Backend Server starting...")
        print(f"Server running at: http://127.0.0.1:{port}")
        print(f"Health check: http://127.0.0.1:{port}/health")
        print(f"Press Ctrl+C to stop the server")
        print("=" * 50)
        
        httpd.serve_forever()
        
    except KeyboardInterrupt:
        print("\nShutting down server...")
        httpd.shutdown()
    except Exception as e:
        print(f"Error starting server: {e}")

if __name__ == "__main__":
    run_server() 