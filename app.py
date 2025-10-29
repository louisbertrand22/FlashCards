"""
Flask web application for the Flashcard application.
Provides a web-based interface for managing and studying flashcards.
"""
import os
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flashcard import DifficultyLevel
from flashcard_manager import FlashcardManager
from datetime import datetime

app = Flask(__name__)
# Use environment variable for secret key in production, fallback to default for development
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')

# Configure data directory for Docker volume persistence
data_dir = os.environ.get('FLASHCARD_DATA_DIR', '.')
if not os.path.exists(data_dir):
    os.makedirs(data_dir)
storage_file = os.path.join(data_dir, 'flashcards.json')

# Initialize flashcard manager
manager = FlashcardManager(storage_file=storage_file)


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
            flash('Both front and back sides are required!', 'error')
            return render_template('create_card.html')
        
        difficulty_level = DifficultyLevel[difficulty]
        card = manager.add_flashcard(recto, verso, difficulty_level, category=category)
        flash(f'Flashcard created successfully! (ID: {card.card_id})', 'success')
        return redirect(url_for('view_cards'))
    
    categories = manager.get_all_categories()
    return render_template('create_card.html', categories=categories)


@app.route('/cards/<card_id>/edit', methods=['GET', 'POST'])
def edit_card(card_id):
    """Edit a flashcard's difficulty."""
    card = manager.get_flashcard(card_id)
    
    if not card:
        flash('Card not found!', 'error')
        return redirect(url_for('view_cards'))
    
    if request.method == 'POST':
        difficulty = request.form.get('difficulty')
        if difficulty:
            difficulty_level = DifficultyLevel[difficulty]
            manager.update_card_difficulty(card_id, difficulty_level)
            flash('Card difficulty updated successfully!', 'success')
            return redirect(url_for('view_cards'))
    
    return render_template('edit_card.html', card=card)


@app.route('/cards/<card_id>/delete', methods=['POST'])
def delete_card(card_id):
    """Delete a flashcard."""
    if manager.remove_flashcard(card_id):
        flash('Flashcard deleted successfully!', 'success')
    else:
        flash('Card not found!', 'error')
    return redirect(url_for('view_cards'))


@app.route('/study')
def study():
    """Study mode - review due flashcards."""
    due_cards = manager.get_due_flashcards(shuffle=True)
    return render_template('study.html', cards=due_cards)


@app.route('/cards/<card_id>/review', methods=['POST'])
def mark_reviewed(card_id):
    """Mark a card as reviewed."""
    if manager.mark_card_reviewed(card_id):
        return jsonify({'success': True, 'message': 'Card marked as reviewed!'})
    else:
        return jsonify({'success': False, 'message': 'Card not found!'}), 404


@app.template_filter('format_datetime')
def format_datetime(value):
    """Format datetime for display."""
    if value is None:
        return 'Never'
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
