"""
API routes for flashcard operations with JWT authentication.
"""
import os
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flashcard import DifficultyLevel
from flashcard_manager import FlashcardManager

api_bp = Blueprint('api', __name__, url_prefix='/api')

# Configure data directory for flashcard storage
data_dir = os.environ.get('FLASHCARD_DATA_DIR', '.')
if not os.path.exists(data_dir):
    os.makedirs(data_dir)
storage_file = os.path.join(data_dir, 'flashcards.json')

# Initialize flashcard manager
manager = FlashcardManager(storage_file=storage_file)


@api_bp.route('/cards', methods=['GET'])
@jwt_required()
def get_cards():
    """
    Get all flashcards for the authenticated user.
    
    Query parameters:
        category (optional): Filter by category
    
    Returns:
        JSON response with list of flashcards
    """
    current_user_id = get_jwt_identity()
    category_filter = request.args.get('category')
    
    if category_filter:
        cards = [card for card in manager.get_flashcards_by_category(category_filter) 
                 if card.user_id == current_user_id]
    else:
        cards = manager.get_all_flashcards(user_id=current_user_id)
    
    return jsonify({
        'cards': [card.to_dict() for card in cards],
        'total': len(cards)
    }), 200


@api_bp.route('/cards', methods=['POST'])
@jwt_required()
def create_card():
    """
    Create a new flashcard for the authenticated user.
    
    Expected JSON body:
    {
        "recto": "Front side text",
        "verso": "Back side text",
        "difficulty": "EASY|MEDIUM|HARD",
        "category": "Category name" (optional)
    }
    
    Returns:
        JSON response with created flashcard
    """
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Invalid request body'}), 400
    
    recto = data.get('recto', '').strip()
    verso = data.get('verso', '').strip()
    difficulty = data.get('difficulty', 'MEDIUM')
    category = data.get('category', '').strip() or None
    
    # Validation
    if not recto or not verso:
        return jsonify({'error': 'Both front and back sides are required'}), 400
    
    try:
        difficulty_level = DifficultyLevel[difficulty]
    except KeyError:
        return jsonify({'error': 'Invalid difficulty level. Must be EASY, MEDIUM, or HARD'}), 400
    
    # Create card associated with user
    card = manager.add_flashcard(recto, verso, difficulty_level, category=category, user_id=current_user_id)
    
    return jsonify({
        'message': 'Flashcard created successfully',
        'card': card.to_dict()
    }), 201


@api_bp.route('/cards/<card_id>', methods=['GET'])
@jwt_required()
def get_card(card_id):
    """
    Get a specific flashcard by ID.
    
    Returns:
        JSON response with flashcard details
    """
    current_user_id = get_jwt_identity()
    card = manager.get_flashcard(card_id)
    
    if not card:
        return jsonify({'error': 'Card not found'}), 404
    
    # Verify ownership
    if card.user_id != current_user_id:
        return jsonify({'error': 'Unauthorized access to this card'}), 403
    
    return jsonify({'card': card.to_dict()}), 200


@api_bp.route('/cards/<card_id>', methods=['PUT'])
@jwt_required()
def update_card(card_id):
    """
    Update a flashcard's difficulty.
    
    Expected JSON body:
    {
        "difficulty": "EASY|MEDIUM|HARD"
    }
    
    Returns:
        JSON response with success message
    """
    current_user_id = get_jwt_identity()
    card = manager.get_flashcard(card_id)
    
    if not card:
        return jsonify({'error': 'Card not found'}), 404
    
    # Verify ownership
    if card.user_id != current_user_id:
        return jsonify({'error': 'Unauthorized access to this card'}), 403
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid request body'}), 400
    
    difficulty = data.get('difficulty')
    if not difficulty:
        return jsonify({'error': 'Difficulty is required'}), 400
    
    try:
        difficulty_level = DifficultyLevel[difficulty]
    except KeyError:
        return jsonify({'error': 'Invalid difficulty level. Must be EASY, MEDIUM, or HARD'}), 400
    
    manager.update_card_difficulty(card_id, difficulty_level)
    
    return jsonify({
        'message': 'Card difficulty updated successfully',
        'card': manager.get_flashcard(card_id).to_dict()
    }), 200


@api_bp.route('/cards/<card_id>', methods=['DELETE'])
@jwt_required()
def delete_card(card_id):
    """
    Delete a flashcard.
    
    Returns:
        JSON response with success message
    """
    current_user_id = get_jwt_identity()
    card = manager.get_flashcard(card_id)
    
    if not card:
        return jsonify({'error': 'Card not found'}), 404
    
    # Verify ownership
    if card.user_id != current_user_id:
        return jsonify({'error': 'Unauthorized access to this card'}), 403
    
    manager.remove_flashcard(card_id)
    
    return jsonify({'message': 'Flashcard deleted successfully'}), 200


@api_bp.route('/cards/<card_id>/review', methods=['POST'])
@jwt_required()
def review_card(card_id):
    """
    Mark a card as reviewed.
    
    Expected JSON body:
    {
        "success": true|false
    }
    
    Returns:
        JSON response with success message and updated card info
    """
    current_user_id = get_jwt_identity()
    card = manager.get_flashcard(card_id)
    
    if not card:
        return jsonify({'error': 'Card not found'}), 404
    
    # Verify ownership
    if card.user_id != current_user_id:
        return jsonify({'error': 'Unauthorized access to this card'}), 403
    
    data = request.get_json() or {}
    success = data.get('success', True)
    
    manager.mark_card_reviewed(card_id, success=success)
    updated_card = manager.get_flashcard(card_id)
    
    return jsonify({
        'message': 'Card marked as reviewed' if success else 'Card needs more practice',
        'card': updated_card.to_dict(),
        'streak': updated_card.success_streak
    }), 200


@api_bp.route('/cards/due', methods=['GET'])
@jwt_required()
def get_due_cards():
    """
    Get all flashcards due for review for the authenticated user.
    
    Query parameters:
        category (optional): Filter by category
        shuffle (optional): Shuffle the results (true/false)
    
    Returns:
        JSON response with list of due flashcards
    """
    current_user_id = get_jwt_identity()
    category_filter = request.args.get('category')
    shuffle = request.args.get('shuffle', 'false').lower() == 'true'
    
    # Get all due cards for user
    all_due_cards = manager.get_due_flashcards(shuffle=shuffle, user_id=current_user_id)
    
    # Filter by category if specified
    if category_filter:
        due_cards = [card for card in all_due_cards if card.category == category_filter]
    else:
        due_cards = all_due_cards
    
    return jsonify({
        'cards': [card.to_dict() for card in due_cards],
        'total': len(due_cards)
    }), 200


@api_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_stats():
    """
    Get statistics for the authenticated user's flashcards.
    
    Returns:
        JSON response with statistics
    """
    current_user_id = get_jwt_identity()
    
    # Get user's cards
    user_cards = manager.get_all_flashcards(user_id=current_user_id)
    
    # Calculate statistics
    total = len(user_cards)
    due = len([card for card in user_cards if card.is_due_for_review()])
    easy = len([card for card in user_cards if card.difficulty == DifficultyLevel.EASY])
    medium = len([card for card in user_cards if card.difficulty == DifficultyLevel.MEDIUM])
    hard = len([card for card in user_cards if card.difficulty == DifficultyLevel.HARD])
    
    total_reviews = sum(card.review_count for card in user_cards)
    
    # Calculate overall success rate
    total_successes = sum(sum(card.review_history) for card in user_cards if card.review_history)
    total_review_history = sum(len(card.review_history) for card in user_cards)
    overall_success_rate = (total_successes / total_review_history * 100) if total_review_history > 0 else 0
    
    # Find best streak
    best_streak = max((card.success_streak for card in user_cards), default=0)
    
    # Count cards with active streaks
    cards_with_streaks = sum(1 for card in user_cards if card.success_streak > 0)
    
    return jsonify({
        'total_cards': total,
        'due_for_review': due,
        'easy_cards': easy,
        'medium_cards': medium,
        'hard_cards': hard,
        'total_reviews': total_reviews,
        'overall_success_rate': round(overall_success_rate, 1),
        'best_streak': best_streak,
        'cards_with_streaks': cards_with_streaks
    }), 200


@api_bp.route('/categories', methods=['GET'])
@jwt_required()
def get_categories():
    """
    Get all unique categories for the authenticated user's flashcards.
    
    Returns:
        JSON response with list of categories
    """
    current_user_id = get_jwt_identity()
    user_cards = manager.get_all_flashcards(user_id=current_user_id)
    
    categories = set()
    for card in user_cards:
        if card.category:
            categories.add(card.category)
    
    return jsonify({
        'categories': sorted(list(categories))
    }), 200
