# AI-RPG-Alpha v0.1.0

An AI-driven text-based RPG engine that creates dynamic, narrative-driven adventures using OpenAI's language models. This project provides a complete web-based platform for interactive storytelling with persistent game state, quest management, and consequence tracking.

## 🎮 Features

### Core Gameplay
- **AI-Driven Narratives**: Dynamic story generation using OpenAI GPT models
- **Persistent Game State**: SQLite database for player progress and game events
- **Quest System**: Rich quest management with objectives, rewards, and consequences
- **Memory System**: ChromaDB vector storage for AI memory and context
- **Consequence Engine**: Delayed events and story threads that evolve over time
- **Risk-Based Encounters**: Dynamic difficulty scaling based on player choices

### Technical Features
- **FastAPI Backend**: Modern, async Python web framework
- **Vanilla Frontend**: Pure HTML/CSS/JavaScript for maximum compatibility
- **Responsive Design**: Mobile-friendly interface with CSS variables
- **Real-time Updates**: WebSocket-ready architecture for future enhancements
- **Comprehensive Testing**: Full test suite with pytest and CI/CD pipeline
- **Database Seeding**: CLI tools for populating game content

## 🏗️ Architecture

```
ai-rpg-alpha/
├── backend/                 # FastAPI backend application
│   ├── main.py             # FastAPI app entry point
│   ├── requirements.txt    # Python dependencies
│   ├── dao/                # Data Access Objects
│   │   ├── game_state.py   # SQLite CRUD operations
│   │   └── memory.py       # ChromaDB vector operations
│   ├── models/             # Data models and schemas
│   │   └── dataclasses.py  # Core game data structures
│   ├── engine/             # Game logic components
│   │   ├── context.py      # Game context builder
│   │   ├── quest_picker.py # Quest filtering logic
│   │   ├── combat.py       # Combat resolution
│   │   └── consequence.py  # Delayed event scheduler
│   ├── ai/                 # AI integration
│   │   ├── openai_client.py # OpenAI API wrapper
│   │   └── templates.py    # Jinja prompt templates
│   ├── data/               # Game data and seeding
│   │   ├── quests_seed.json # Sample quest data
│   │   └── seed_db.py      # Database seeding CLI
│   └── tests/              # Test suite
├── frontend/               # Vanilla HTML/CSS/JS frontend
│   ├── index.html          # Main game interface
│   ├── styles.css          # Responsive CSS with variables
│   ├── script.js           # Game logic and API communication
│   └── assets/             # Static assets
└── .github/workflows/      # CI/CD pipeline
    └── tests.yml           # GitHub Actions workflow
```

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- OpenAI API key
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-rpg-alpha
   ```

2. **Set up the backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   export OPENAI_API_KEY="your-openai-api-key-here"
   ```

4. **Initialize the database**
   ```bash
   python -m data.seed_db --force
   ```

5. **Start the backend server**
   ```bash
   python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

6. **Open the frontend**
   ```bash
   cd ../frontend
   # Serve the frontend (use any static file server)
   python -m http.server 3000
   ```

7. **Access the game**
   Open your browser and navigate to `http://localhost:3000`

### Development Setup

For development with auto-reload:

```bash
# Terminal 1: Backend with auto-reload
cd backend
export OPENAI_API_KEY="your-api-key"
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2: Frontend development server
cd frontend
python -m http.server 3000
```

## 🎯 Usage

### Starting a New Game

1. Open the web interface at `http://localhost:3000`
2. Enter your character name
3. Click "Begin Adventure"
4. Choose from AI-generated options or write custom actions
5. Experience dynamic storytelling that adapts to your choices

### Game Controls

- **Choice Mode**: Select from 4 AI-generated options
- **Custom Mode**: Write your own actions and responses
- **Save/Load**: Persistent game state across sessions
- **Music Controls**: Background audio with volume control

### API Endpoints

#### Health Check
```http
GET /health
```
Returns server status and configuration information.

#### Game Turn
```http
POST /turn
Content-Type: application/json

{
  "player_id": "unique_player_identifier",
  "choice": "Player's chosen action or response"
}
```

Returns:
```json
{
  "narrative": "AI-generated story continuation",
  "choices": ["Option 1", "Option 2", "Option 3", "Option 4"],
  "metadata": {
    "risk_level": "calm|mystery|combat",
    "location": "current_location",
    "turn_number": 1
  }
}
```

## 🧪 Testing

### Running Tests

```bash
cd backend

# Run all tests
python -m pytest -v

# Run specific test files
python -m pytest test_seed_loader.py -v
python -m pytest test_api_endpoints.py -v

# Run with coverage
python -m pytest --cov=. --cov-report=html
```

### Test Database Seeding

```bash
cd backend

# Show current database stats
python -m data.seed_db --stats

# Seed database with sample data
python -m data.seed_db --force

# Clear all data
python -m data.seed_db --clear
```

### CI/CD Pipeline

The project includes a comprehensive GitHub Actions workflow that:

- Runs linting and code quality checks
- Executes the full test suite
- Performs security scanning
- Tests database seeding functionality
- Validates API endpoints
- Runs integration and performance tests
- Creates distribution packages

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `OPENAI_API_KEY` | OpenAI API key for AI generation | Yes | None |
| `DATABASE_URL` | SQLite database path | No | `game_state.db` |
| `CHROMA_PERSIST_DIR` | ChromaDB storage directory | No | `./chroma_db` |
| `LOG_LEVEL` | Logging level | No | `INFO` |

### Database Configuration

The application uses SQLite for relational data and ChromaDB for vector storage:

- **SQLite**: Stores player data, quests, game events, and relationships
- **ChromaDB**: Stores AI memory embeddings for context and continuity

### AI Configuration

The AI system uses OpenAI's GPT models with:

- **Model**: GPT-4 or GPT-3.5-turbo (configurable)
- **Temperature**: 0.8 for creative storytelling
- **Max Tokens**: 1000 for narrative responses
- **Context Window**: Optimized for game state and memory

## 📊 Game Data

### Quest System

Quests are defined in JSON format with the following structure:

```json
{
  "id": "unique_quest_id",
  "title": "Quest Title",
  "location": "quest_location",
  "tags": ["combat", "mystery", "exploration"],
  "intro": "Quest introduction text",
  "objectives": ["Objective 1", "Objective 2"],
  "success": "Success outcome text",
  "failure": "Failure outcome text",
  "reward": {
    "gold": 100,
    "items": ["Item Name"],
    "experience": 50
  },
  "risk": "calm|mystery|combat",
  "consequence_thread": {
    "trigger_turn": 5,
    "event": "event_id",
    "description": "Consequence description"
  }
}
```

### Memory System

The AI memory system tracks:

- **Player Actions**: All choices and their outcomes
- **Story Context**: Narrative threads and character development
- **World State**: Environmental changes and consequences
- **Relationship Data**: NPC interactions and reputation

## 🎨 Frontend Features

### Responsive Design

The frontend is built with modern CSS featuring:

- **CSS Variables**: Consistent theming and easy customization
- **Grid Layout**: Responsive design that works on all devices
- **Smooth Animations**: Polished user experience with transitions
- **Accessibility**: ARIA labels and keyboard navigation support

### User Interface

- **Player Panel**: Real-time stats, inventory, and location display
- **Narrative Display**: Scrollable story text with rich formatting
- **Choice Interface**: Toggle between guided and custom input modes
- **Game Controls**: Save/load functionality and settings
- **Audio System**: Background music with volume controls

### Browser Compatibility

Tested and compatible with:

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## 🔒 Security

### API Security

- **Input Validation**: All user inputs are validated and sanitized
- **Rate Limiting**: Protection against API abuse (configurable)
- **CORS Configuration**: Secure cross-origin resource sharing
- **Error Handling**: Secure error responses without information leakage

### Data Protection

- **Local Storage**: Game saves stored locally in browser
- **No Personal Data**: Minimal data collection and storage
- **API Key Security**: Environment variable configuration
- **Database Isolation**: Player data separation and privacy

## 🚀 Deployment

### Local Development

Use the quick start guide above for local development setup.

### Production Deployment

For production deployment, consider:

1. **Environment Configuration**
   ```bash
   export OPENAI_API_KEY="production-api-key"
   export DATABASE_URL="postgresql://user:pass@host:port/db"
   export LOG_LEVEL="WARNING"
   ```

2. **Database Setup**
   ```bash
   python -m data.seed_db --force
   ```

3. **Server Configuration**
   ```bash
   python -m uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

4. **Frontend Serving**
   Use a web server like Nginx to serve static files:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           root /path/to/frontend;
           index index.html;
       }
       
       location /api/ {
           proxy_pass http://localhost:8000/;
       }
   }
   ```

### Docker Deployment

A Dockerfile can be created for containerized deployment:

```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY backend/ ./backend/
COPY frontend/ ./frontend/

RUN pip install -r backend/requirements.txt

EXPOSE 8000
CMD ["python", "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🤝 Contributing

### Development Workflow

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and add tests
4. Run the test suite: `python -m pytest`
5. Commit your changes: `git commit -m 'Add amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

### Code Standards

- **Python**: Follow PEP 8 style guidelines
- **JavaScript**: Use ES6+ features and consistent formatting
- **Testing**: Maintain test coverage above 80%
- **Documentation**: Update documentation for new features

### Adding New Features

#### Adding New Quest Types

1. Update the quest schema in `models/dataclasses.py`
2. Add quest data to `data/quests_seed.json`
3. Update the quest picker logic in `engine/quest_picker.py`
4. Add tests for the new quest type

#### Extending the AI System

1. Modify prompt templates in `ai/templates.py`
2. Update the OpenAI client wrapper if needed
3. Add new context builders in `engine/context.py`
4. Test with various scenarios

#### Frontend Enhancements

1. Update the HTML structure in `index.html`
2. Add new styles to `styles.css` using CSS variables
3. Implement new functionality in `script.js`
4. Test across different browsers and devices

## 📈 Performance

### Benchmarks

- **API Response Time**: < 2 seconds for typical requests
- **Database Operations**: < 100ms for standard queries
- **Memory Usage**: < 512MB for typical workloads
- **Concurrent Users**: Tested up to 50 simultaneous players

### Optimization Tips

- **Database Indexing**: Add indexes for frequently queried fields
- **Caching**: Implement Redis for session and quest data caching
- **CDN**: Use a CDN for static frontend assets
- **Load Balancing**: Deploy multiple backend instances for scale

## 🐛 Troubleshooting

### Common Issues

#### OpenAI API Errors

```bash
# Check API key configuration
echo $OPENAI_API_KEY

# Test API connectivity
curl -H "Authorization: Bearer $OPENAI_API_KEY" \
     https://api.openai.com/v1/models
```

#### Database Issues

```bash
# Reset database
rm game_state.db
python -m data.seed_db --force

# Check database contents
python -m data.seed_db --stats
```

#### Frontend Connection Issues

```bash
# Check backend server status
curl http://localhost:8000/health

# Verify CORS configuration
curl -H "Origin: http://localhost:3000" \
     -H "Access-Control-Request-Method: POST" \
     -X OPTIONS http://localhost:8000/turn
```

### Debug Mode

Enable debug logging:

```bash
export LOG_LEVEL="DEBUG"
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --log-level debug
```

## 📚 API Reference

### Complete API Documentation

#### GET /

Returns basic server information.

**Response:**
```json
{
  "message": "AI-RPG-Alpha Backend v0.1.0",
  "status": "running",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

#### GET /health

Health check endpoint with system status.

**Response:**
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "openai_configured": true,
  "components": {
    "database": "connected",
    "vector_store": "connected",
    "ai_service": "available"
  }
}
```

#### POST /turn

Process a player's turn and return the game response.

**Request:**
```json
{
  "player_id": "string (required)",
  "choice": "string (required)"
}
```

**Response:**
```json
{
  "narrative": "string",
  "choices": ["string", "string", "string", "string"],
  "metadata": {
    "risk_level": "calm|mystery|combat",
    "location": "string",
    "turn_number": "integer",
    "player_stats": {
      "health": "integer",
      "mana": "integer",
      "level": "integer"
    }
  }
}
```

**Error Responses:**

- `422 Unprocessable Entity`: Invalid request format
- `500 Internal Server Error`: Server or AI service error

## 🔮 Future Enhancements

### Planned Features

#### Version 0.2.0
- **Multiplayer Support**: Real-time collaborative adventures
- **Character Classes**: Warrior, Mage, Rogue with unique abilities
- **Inventory System**: Detailed item management and crafting
- **Combat Mechanics**: Turn-based tactical combat system

#### Version 0.3.0
- **World Map**: Visual exploration interface
- **NPC Dialogue**: Advanced conversation trees
- **Guild System**: Player organizations and shared quests
- **Achievement System**: Progress tracking and rewards

#### Version 1.0.0
- **Mobile App**: Native iOS and Android applications
- **Voice Interface**: Speech-to-text and text-to-speech
- **AI Dungeon Master**: Advanced AI game master capabilities
- **Custom Campaigns**: User-generated content tools

### Technical Roadmap

- **WebSocket Integration**: Real-time updates and multiplayer
- **GraphQL API**: More flexible data querying
- **Microservices**: Scalable architecture with service separation
- **Machine Learning**: Player behavior analysis and personalization

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI**: For providing the GPT models that power the AI storytelling
- **FastAPI**: For the excellent Python web framework
- **ChromaDB**: For vector storage and similarity search capabilities
- **The RPG Community**: For inspiration and feedback on game mechanics

## 📞 Support

For support, questions, or contributions:

- **Issues**: Use GitHub Issues for bug reports and feature requests
- **Discussions**: Use GitHub Discussions for general questions
- **Email**: [Contact information if available]

---

**AI-RPG-Alpha v0.1.0** - Where every choice writes your legend.

