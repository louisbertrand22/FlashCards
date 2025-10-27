# FlashCards Application

A Python-based flashcard application for creating and studying flashcards with difficulty-based review scheduling. **Now with both a web interface and an enhanced, colorful CLI interface!**

## Features

- **Web Interface**: Modern, responsive web application built with Flask
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

- Python 3.6 or higher
- Docker (optional, for containerized deployment)

## Installation

### Option 1: Standard Installation

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

### Option 2: Docker Installation

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

## File Structure

- `app.py`: Flask web application entry point
- `templates/`: HTML templates for the web interface
  - `base.html`: Base template with navigation
  - `index.html`: Dashboard with statistics
  - `cards.html`: View all flashcards
  - `create_card.html`: Create new flashcard form
  - `edit_card.html`: Edit flashcard difficulty
  - `study.html`: Interactive study mode
- `static/css/`: CSS stylesheets for the web interface
- `main.py`: Command-line interface and application entry point with enhanced UI
- `flashcard.py`: Flashcard class and difficulty level definitions
- `flashcard_manager.py`: Manager class for flashcard collection operations
- `ui_components.py`: UI utilities providing colors, formatting, and visual enhancements for CLI
- `flashcards.json`: Persistent storage file (created automatically)

## How Difficulty Affects Review Frequency

The difficulty level determines how often a flashcard appears for review:

- **Easy (1)**: Cards you find easy to remember - reviewed every 7 days
- **Medium (2)**: Cards of moderate difficulty - reviewed every 3 days
- **Hard (3)**: Cards you find difficult - reviewed daily

When you mark a card as reviewed during a study session, it's automatically rescheduled based on its difficulty level.

## Data Storage

Flashcards are stored in `flashcards.json` in the application directory. This file is automatically created and updated as you add, modify, or delete flashcards.

### Docker Volume Persistence

When using Docker, flashcard data is persisted using Docker volumes. The `docker-compose.yml` configuration automatically sets up a volume to ensure your flashcards are not lost when the container is restarted or updated.

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
docker run -d -p 5000:5000 -v flashcards-data:/app/flashcards.json ghcr.io/louisbertrand22/flashcards:latest
```

### Environment Variables

The Docker container supports the following environment variables:

- `FLASK_ENV`: Set to `development` for debug mode (default: `production`)
- `FLASK_SECRET_KEY`: Secret key for Flask sessions (auto-generated if not provided)

Example with environment variables:
```bash
docker run -d -p 5000:5000 \
  -e FLASK_ENV=production \
  -e FLASK_SECRET_KEY=your-secret-key-here \
  -v flashcards-data:/app/flashcards.json \
  ghcr.io/louisbertrand22/flashcards:latest
```

## License

MIT License - Feel free to use and modify as needed!