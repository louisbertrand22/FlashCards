"""
Flashcard class representing a single flashcard with recto, verso, and difficulty level.
"""
import uuid
from datetime import datetime, timedelta
from enum import Enum


class DifficultyLevel(Enum):
    """Difficulty levels that determine review frequency."""
    EASY = 1      # Review every 7 days
    MEDIUM = 2    # Review every 3 days
    HARD = 3      # Review every 1 day
    
    def get_review_interval(self):
        """Get the review interval in days based on difficulty."""
        intervals = {
            DifficultyLevel.EASY: 7,
            DifficultyLevel.MEDIUM: 3,
            DifficultyLevel.HARD: 1
        }
        return intervals[self]


class Flashcard:
    """A flashcard with a front (recto), back (verso), and difficulty level."""
    
    def __init__(self, recto, verso, difficulty=DifficultyLevel.MEDIUM, card_id=None, category=None):
        """
        Initialize a flashcard.
        
        Args:
            recto (str): Front side of the card
            verso (str): Back side of the card
            difficulty (DifficultyLevel): Difficulty level of the card
            card_id (str): Unique identifier for the card
            category (str): Optional category for organizing cards
        """
        self.card_id = card_id or self._generate_id()
        self.recto = recto
        self.verso = verso
        self.difficulty = difficulty
        self.category = category
        self.created_at = datetime.now()
        self.last_reviewed = None
        self.next_review = datetime.now()
        self.review_count = 0
    
    def _generate_id(self):
        """Generate a unique ID for the flashcard."""
        return f"card_{uuid.uuid4().hex[:16]}"
    
    def mark_reviewed(self):
        """Mark the card as reviewed and schedule next review."""
        self.last_reviewed = datetime.now()
        self.review_count += 1
        interval_days = self.difficulty.get_review_interval()
        self.next_review = datetime.now() + timedelta(days=interval_days)
    
    def is_due_for_review(self):
        """Check if the card is due for review."""
        return datetime.now() >= self.next_review
    
    def update_difficulty(self, new_difficulty):
        """Update the difficulty level of the card."""
        if isinstance(new_difficulty, DifficultyLevel):
            self.difficulty = new_difficulty
            # Recalculate next review based on new difficulty
            if self.last_reviewed:
                interval_days = self.difficulty.get_review_interval()
                self.next_review = self.last_reviewed + timedelta(days=interval_days)
    
    def to_dict(self):
        """Convert flashcard to dictionary for serialization."""
        return {
            'card_id': self.card_id,
            'recto': self.recto,
            'verso': self.verso,
            'difficulty': self.difficulty.name,
            'category': self.category,
            'created_at': self.created_at.isoformat(),
            'last_reviewed': self.last_reviewed.isoformat() if self.last_reviewed else None,
            'next_review': self.next_review.isoformat(),
            'review_count': self.review_count
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create a flashcard from a dictionary."""
        difficulty = DifficultyLevel[data['difficulty']]
        card = cls(
            recto=data['recto'],
            verso=data['verso'],
            difficulty=difficulty,
            card_id=data['card_id'],
            category=data.get('category')  # Use .get() for backward compatibility
        )
        card.created_at = datetime.fromisoformat(data['created_at'])
        card.last_reviewed = datetime.fromisoformat(data['last_reviewed']) if data['last_reviewed'] else None
        card.next_review = datetime.fromisoformat(data['next_review'])
        card.review_count = data['review_count']
        return card
    
    def __str__(self):
        """String representation of the flashcard."""
        return f"Flashcard(recto='{self.recto}', difficulty={self.difficulty.name})"
    
    def __repr__(self):
        """Detailed representation of the flashcard."""
        return (f"Flashcard(id={self.card_id}, recto='{self.recto}', verso='{self.verso}', "
                f"difficulty={self.difficulty.name}, reviews={self.review_count})")
