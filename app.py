"""
Flask web application for the Flashcard application.
Provides a web-based interface for managing and studying flashcards.
"""
import os
import sys
from datetime import timedelta
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session
from flask_babel import Babel, gettext, lazy_gettext
from flask_jwt_extended import JWTManager
from flashcard import DifficultyLevel
from flashcard_manager import FlashcardManager
from datetime import datetime

app = Flask(__name__)
# Use environment variable for secret key in production, fallback to default for development
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')

# Configure JWT
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', app.secret_key)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
jwt = JWTManager(app)

# Configure Babel
app.config['BABEL_DEFAULT_LOCALE'] = 'fr'
app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'

def get_locale():
    # Try to get language from session, then from Accept-Language header
    return session.get('language', request.accept_languages.best_match(['en', 'fr']) or 'fr')

babel = Babel(app, locale_selector=get_locale)

# Configure data directory for Docker volume persistence
data_dir = os.environ.get('FLASHCARD_DATA_DIR', '.')

# Ensure data directory exists and is valid
try:
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    elif not os.path.isdir(data_dir):
        print(f"Error: {data_dir} exists but is not a directory")
        print("Please specify a valid directory path in FLASHCARD_DATA_DIR environment variable")
        sys.exit(1)
except PermissionError:
    print(f"Error: Permission denied when trying to create directory {data_dir}")
    print("Please check permissions or choose a different location")
    sys.exit(1)
except OSError as e:
    print(f"Error: Could not create data directory {data_dir}: {e}")
    print("Please check that the path is valid and accessible")
    sys.exit(1)

storage_file = os.path.join(data_dir, 'flashcards.json')

# Initialize flashcard manager
manager = FlashcardManager(storage_file=storage_file)

# Register blueprints for JWT authentication and API
from auth import auth_bp
from api import api_bp
app.register_blueprint(auth_bp)
app.register_blueprint(api_bp)


@app.route('/')
def index():
    """Home page with dashboard and statistics."""
    stats = manager.get_statistics()
    return render_template('index.html', stats=stats)


@app.route('/cards')
def view_cards():
    """View all flashcards."""
    category_filter = request.args.get('category')
    if category_filter:
        cards = manager.get_flashcards_by_category(category_filter)
    else:
        cards = manager.get_all_flashcards()
    categories = manager.get_all_categories()
    return render_template('cards.html', cards=cards, categories=categories, selected_category=category_filter)


@app.route('/cards/new', methods=['GET', 'POST'])
def create_card():
    """Create a new flashcard."""
    if request.method == 'POST':
        recto = request.form.get('recto', '').strip()
        verso = request.form.get('verso', '').strip()
        difficulty = request.form.get('difficulty', 'MEDIUM')
        category = request.form.get('category', '').strip() or None
        
        if not recto or not verso:
            flash(gettext('Both front and back sides are required!'), 'error')
            return render_template('create_card.html')
        
        difficulty_level = DifficultyLevel[difficulty]
        card = manager.add_flashcard(recto, verso, difficulty_level, category=category)
        flash(gettext('Flashcard created successfully! (ID: %(card_id)s)', card_id=card.card_id), 'success')
        return redirect(url_for('view_cards'))
    
    categories = manager.get_all_categories()
    return render_template('create_card.html', categories=categories)


@app.route('/cards/<card_id>/edit', methods=['GET', 'POST'])
def edit_card(card_id):
    """Edit a flashcard's difficulty."""
    card = manager.get_flashcard(card_id)
    
    if not card:
        flash(gettext('Card not found!'), 'error')
        return redirect(url_for('view_cards'))
    
    if request.method == 'POST':
        difficulty = request.form.get('difficulty')
        if difficulty:
            difficulty_level = DifficultyLevel[difficulty]
            manager.update_card_difficulty(card_id, difficulty_level)
            flash(gettext('Card difficulty updated successfully!'), 'success')
            return redirect(url_for('view_cards'))
    
    return render_template('edit_card.html', card=card)


@app.route('/cards/<card_id>/delete', methods=['POST'])
def delete_card(card_id):
    """Delete a flashcard."""
    if manager.remove_flashcard(card_id):
        flash(gettext('Flashcard deleted successfully!'), 'success')
    else:
        flash(gettext('Card not found!'), 'error')
    return redirect(url_for('view_cards'))


@app.route('/study')
def study():
    """Study mode - review due flashcards."""
    category_filter = request.args.get('category')
    
    # Get all due cards
    all_due_cards = manager.get_due_flashcards(shuffle=True)
    
    # Filter by category if specified
    if category_filter:
        due_cards = [card for card in all_due_cards if card.category == category_filter]
    else:
        due_cards = all_due_cards
    
    categories = manager.get_all_categories()
    return render_template('study.html', cards=due_cards, categories=categories, selected_category=category_filter)


@app.route('/cards/<card_id>/review', methods=['POST'])
def mark_reviewed(card_id):
    """Mark a card as reviewed."""
    data = request.get_json() or {}
    success = data.get('success', True)  # Default to True for backward compatibility
    
    if manager.mark_card_reviewed(card_id, success=success):
        # Get updated card info for response
        card = manager.get_flashcard(card_id)
        response_data = {
            'success': True,
            'message': gettext('Card marked as reviewed!') if success else gettext('Card needs more practice.'),
            'streak': card.success_streak if card else 0
        }
        return jsonify(response_data)
    else:
        return jsonify({'success': False, 'message': gettext('Card not found!')}), 404


@app.template_filter('format_datetime')
def format_datetime(value):
    """Format datetime for display."""
    if value is None:
        return gettext('Never')
    if isinstance(value, str):
        value = datetime.fromisoformat(value)
    return value.strftime('%Y-%m-%d %H:%M')


@app.template_filter('difficulty_color')
def difficulty_color(difficulty):
    """Get color for difficulty level."""
    colors = {
        'EASY': 'success',
        'MEDIUM': 'warning',
        'HARD': 'danger'
    }
    return colors.get(difficulty, 'secondary')


@app.template_filter('difficulty_emoji')
def difficulty_emoji(difficulty):
    """Get emoji for difficulty level."""
    emojis = {
        'EASY': '🟢',
        'MEDIUM': '🟡',
        'HARD': '🔴'
    }
    return emojis.get(difficulty, '⚪')


if __name__ == '__main__':
    # Debug mode should only be enabled in development
    # Set FLASK_ENV=development to enable debug mode
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
