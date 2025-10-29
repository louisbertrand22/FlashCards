# FlashCards Application

A Python-based flashcard application for creating and studying flashcards with difficulty-based review scheduling. **Now with both a web interface and an enhanced, colorful CLI interface!**

## 🌐 Try it Online!

**[Launch FlashCards Web App](https://louisbertrand22.github.io/FlashCards/)** - No installation required! Uses your browser's local storage.

## Features

- **🔐 JWT Authentication**: Secure user authentication with JSON Web Tokens for multi-user support
- **🌐 RESTful API**: Complete API for flashcard management with JWT protection
- **Static Web App**: Pure client-side application hosted on GitHub Pages (no server required!)
- **Web Interface**: Modern, responsive web application built with Flask (for local/Docker deployment)
- **CLI Interface**: Beautiful, colorful command-line interface
- **Create Flashcards**: Create flashcards with a front side (recto) and back side (verso)
- **Difficulty Levels**: Assign difficulty levels that determine review frequency:
  - **Easy**: Review every 7 days
  - **Medium**: Review every 3 days
  - **Hard**: Review every 1 day
- **Smart Scheduling**: Flashcards are automatically scheduled for review based on their difficulty level
- **Study Mode**: Review flashcards that are due for study with interactive progress tracking
- **Statistics**: View colorful statistics about your flashcard collection
- **Persistence**: Flashcards are automatically saved to a JSON file
- **Enhanced UI/UX**: 
  - Color-coded difficulty badges (🟢 Easy, 🟡 Medium, 🔴 Hard)
  - Visual progress bars during study sessions
  - Icons and emojis for better visual hierarchy
  - Clear status indicators and feedback messages
  - Improved formatting and spacing

## Requirements

### For the Static Web App (GitHub Pages)
- Just a modern web browser! No installation needed.
- Visit: [https://louisbertrand22.github.io/FlashCards/](https://louisbertrand22.github.io/FlashCards/)

### For Local/Docker Deployment
- Python 3.6 or higher
- Docker (optional, for containerized deployment)

## Installation

### Option 1: Use the Online Version (Recommended for Quick Start)

Simply visit **[https://louisbertrand22.github.io/FlashCards/](https://louisbertrand22.github.io/FlashCards/)** in your web browser. Your flashcards are stored locally in your browser using localStorage, so they persist between sessions.

**Benefits:**
- No installation required
- Works offline once loaded
- Data stays private in your browser
- Same features as the Flask version

### Option 2: Standard Installation

1. Clone this repository:
```bash
git clone https://github.com/louisbertrand22/FlashCards.git
cd FlashCards
```

2. (Optional) For the web interface, install Flask:
```bash
pip install -r requirements.txt
```

Note: The CLI interface uses only Python standard library and requires no additional dependencies!

### Option 3: Docker Installation

Run the application using Docker:

```bash
# Pull the latest image from GitHub Container Registry
docker pull ghcr.io/louisbertrand22/flashcards:latest

# Run the container
docker run -d -p 5000:5000 --name flashcards ghcr.io/louisbertrand22/flashcards:latest
```

Or use Docker Compose for easy setup:

```bash
# Clone the repository (if not already done)
git clone https://github.com/louisbertrand22/FlashCards.git
cd FlashCards

# Start the application
docker-compose up -d

# Stop the application
docker-compose down
```

The Docker image is automatically built and published to GitHub Container Registry (ghcr.io) on every push to the main branch.

## Usage

### Web Interface (Recommended)

Run the web application:
```bash
python app.py
```

For development with debug mode enabled:
```bash
FLASK_ENV=development python app.py
```

Then open your browser and navigate to: `http://localhost:5000`

The web interface provides:
- Interactive dashboard with statistics
- Easy card creation and management
- Visual study mode with answer reveal
- Responsive design that works on desktop and mobile

### Command-Line Interface

Run the CLI application:
```bash
python main.py
```

### CLI Main Menu Options

1. **Create a new flashcard**: Add a flashcard with recto (front), verso (back), and difficulty level
2. **View all flashcards**: Display all your flashcards with their details
3. **Study flashcards**: Review flashcards that are due for study
4. **View statistics**: See statistics about your flashcard collection
5. **Update card difficulty**: Change the difficulty level of an existing card
6. **Delete a flashcard**: Remove a flashcard from your collection
7. **Exit**: Save and exit the application

### Example Workflow

**Web Interface:**
1. Start the web app: `python app.py`
2. Open your browser to `http://localhost:5000`
3. Click "Create Card" to add a new flashcard
4. Fill in the front side, back side, and select difficulty
5. View your cards on the "All Cards" page
6. Click "Study" when cards are due for review
7. The app will automatically schedule the next review based on difficulty

**CLI:**
1. Start the application: `python main.py`
2. Choose option 1 to create a new flashcard
3. Enter the front side (e.g., "What is the capital of France?")
4. Enter the back side (e.g., "Paris")
5. Select difficulty level (1 for Easy, 2 for Medium, 3 for Hard)
6. Use option 3 to study flashcards when they're due for review
7. The app will automatically schedule the next review based on difficulty

## JWT Authentication API

The application now includes a complete RESTful API with JWT authentication for multi-user support. See [JWT_API_DOCUMENTATION.md](JWT_API_DOCUMENTATION.md) for detailed API documentation including:

- User registration and authentication
- Token-based authorization
- Protected flashcard endpoints
- Token refresh mechanism
- Complete API reference with examples

**Key Features:**
- Secure password hashing with bcrypt
- Access tokens (1 hour expiration)
- Refresh tokens (30 day expiration)
- User-specific flashcard isolation
- Backward compatible with existing functionality

**Quick Example:**
```bash
# Register a user
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "password": "password123"}'

# Login and get token
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "password": "password123"}'

# Use token to create a card
curl -X POST http://localhost:5000/api/cards \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"recto": "Question", "verso": "Answer", "difficulty": "MEDIUM"}'
```

## File Structure

- `app.py`: Flask web application entry point with JWT integration
- `auth.py`: JWT authentication routes (register, login, refresh, user info)
- `api.py`: Protected API routes for flashcard management
- `auth_models.py`: User model with password hashing
- `user_manager.py`: User management and authentication logic
- `templates/`: HTML templates for the web interface
  - `base.html`: Base template with navigation
  - `index.html`: Dashboard with statistics
  - `cards.html`: View all flashcards
  - `create_card.html`: Create new flashcard form
  - `edit_card.html`: Edit flashcard difficulty
  - `study.html`: Interactive study mode
- `static/css/`: CSS stylesheets for the web interface
- `main.py`: Command-line interface and application entry point with enhanced UI
- `flashcard.py`: Flashcard class with user association support
- `flashcard_manager.py`: Manager class for flashcard collection operations
- `ui_components.py`: UI utilities providing colors, formatting, and visual enhancements for CLI
- `flashcards.json`: Persistent storage file (created automatically)
- `users.json`: User data storage (created automatically)
- `JWT_API_DOCUMENTATION.md`: Complete API documentation

## How Difficulty Affects Review Frequency

The difficulty level determines how often a flashcard appears for review:

- **Easy (1)**: Cards you find easy to remember - reviewed every 7 days
- **Medium (2)**: Cards of moderate difficulty - reviewed every 3 days
- **Hard (3)**: Cards you find difficult - reviewed daily

When you mark a card as reviewed during a study session, it's automatically rescheduled based on its difficulty level.

## Data Storage

Flashcards are stored in `flashcards.json` in the application directory. This file is automatically created and updated as you add, modify, or delete flashcards.

### Docker Volume Persistence

When using Docker, flashcard data is persisted using Docker volumes mounted to `/app/data` directory. The `docker-compose.yml` configuration automatically sets up a volume to ensure your flashcards are not lost when the container is restarted or updated.

The application automatically creates the data directory and stores `flashcards.json` in the configured location (default: current directory for local runs, `/app/data` for Docker).

## Docker Deployment

### Building Your Own Image

To build the Docker image locally:

```bash
docker build -t flashcards .
```

### Using GitHub Container Registry

The project includes a CI/CD pipeline that automatically builds and publishes Docker images to GitHub Container Registry (ghcr.io) when changes are pushed to the main branch.

**Available tags:**
- `latest` - Latest stable version from the main branch
- `main` - Latest build from the main branch
- `v*` - Semantic version tags (e.g., v1.0.0)
- Git SHA tags for specific commits

**Pull and run:**
```bash
docker pull ghcr.io/louisbertrand22/flashcards:latest
docker run -d -p 5000:5000 -v flashcards-data:/app/data ghcr.io/louisbertrand22/flashcards:latest
```

### Environment Variables

The Docker container supports the following environment variables:

- `FLASK_ENV`: Set to `development` for debug mode (default: `production`)
- `FLASK_SECRET_KEY`: Secret key for Flask sessions (default: `dev-secret-key-change-in-production`)
- `FLASHCARD_DATA_DIR`: Directory for storing flashcard data (default: `/app/data`)

Example with environment variables:
```bash
docker run -d -p 5000:5000 \
  -e FLASK_ENV=production \
  -e FLASK_SECRET_KEY=your-random-secret-key-here \
  -v flashcards-data:/app/data \
  ghcr.io/louisbertrand22/flashcards:latest
```

**Note:** For production deployments, always set a strong, random `FLASK_SECRET_KEY`.

## GitHub Pages Deployment

The project includes an automatic deployment to GitHub Pages. The static web version is deployed from the `docs/` directory.

**Live URL:** [https://louisbertrand22.github.io/FlashCards/](https://louisbertrand22.github.io/FlashCards/)

### How it Works

1. The static web app in the `docs/` directory uses pure HTML, CSS, and JavaScript
2. Data is stored in the browser's localStorage (no backend required)
3. GitHub Actions automatically deploys changes when pushed to the main branch
4. The app works offline once loaded in the browser

### Key Differences from Flask Version

The GitHub Pages version is a client-side only application:
- **Storage**: Uses browser localStorage instead of JSON files
- **Data Privacy**: All data stays in your browser, never sent to a server
- **No Backend**: Pure JavaScript implementation, no Python/Flask required
- **Same Features**: All core functionality (create, study, edit, delete cards) works identically

### Manual Deployment

If you fork this repository and want to enable GitHub Pages:

1. Go to your repository Settings
2. Navigate to Pages section
3. Under "Build and deployment", select:
   - **Source**: GitHub Actions
4. The workflow will automatically deploy on the next push to main

## License

MIT License - Feel free to use and modify as needed!