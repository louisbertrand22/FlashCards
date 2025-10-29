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
    
    def __init__(self, recto, verso, difficulty=DifficultyLevel.MEDIUM, card_id=None, category=None, user_id=None):
        """
        Initialize a flashcard.
        
        Args:
            recto (str): Front side of the card
            verso (str): Back side of the card
            difficulty (DifficultyLevel): Difficulty level of the card
            card_id (str): Unique identifier for the card
            category (str): Optional category for organizing cards
            user_id (str): Optional user ID for multi-user support
        """
        self.card_id = card_id or self._generate_id()
        self.recto = recto
        self.verso = verso
        self.difficulty = difficulty
        self.category = category
        self.user_id = user_id
        self.created_at = datetime.now()
        self.last_reviewed = None
        self.next_review = datetime.now()
        self.review_count = 0
        self.review_history = []  # List of bool: True for success, False for failure
        self.last_mandatory_review = None  # Track when last mandatory 2-week review occurred
        self.success_streak = 0  # Track consecutive successful reviews
    
    def _generate_id(self):
        """Generate a unique ID for the flashcard."""
        return f"card_{uuid.uuid4().hex[:16]}"
    
    def mark_reviewed(self, success=True):
        """
        Mark the card as reviewed and schedule next review.
        
        Args:
            success (bool): Whether the review was successful (default: True)
        """
        now = datetime.now()
        self.last_reviewed = now
        self.review_count += 1
        self.review_history.append(success)
        
        # Check if this qualifies as a mandatory review (2-week cycle)
        if self.last_mandatory_review is None:
            # First review after 2 weeks from creation
            if now >= self.created_at + timedelta(days=14):
                self.last_mandatory_review = now
        else:
            # Check if 2 weeks passed since last mandatory review
            if now >= self.last_mandatory_review + timedelta(days=14):
                self.last_mandatory_review = now
        
        # Update success streak
        if success:
            self.success_streak += 1
        else:
            self.success_streak = 0
        
        # Auto-adjust difficulty based on recent performance
        self._auto_adjust_difficulty()
        
        # Calculate next review interval
        interval_days = self._calculate_review_interval(success)
        self.next_review = now + timedelta(days=interval_days)
    
    def is_due_for_review(self):
        """
        Check if the card is due for review.
        Considers both difficulty-based interval and mandatory 2-week review cycle.
        """
        # Check regular difficulty-based review
        if datetime.now() >= self.next_review:
            return True
        
        # Check mandatory 2-week review cycle
        if self.last_mandatory_review is None:
            # If never had a mandatory review, check if 2 weeks passed since creation
            return datetime.now() >= self.created_at + timedelta(days=14)
        else:
            # Check if 2 weeks passed since last mandatory review
            return datetime.now() >= self.last_mandatory_review + timedelta(days=14)
    
    def _calculate_review_interval(self, success):
        """
        Calculate the next review interval based on success and performance.
        
        Args:
            success (bool): Whether the review was successful
            
        Returns:
            int: Number of days until next review
        """
        base_interval = self.difficulty.get_review_interval()
        
        # If failed, review sooner (halve the interval, minimum 1 day)
        if not success:
            return max(1, base_interval // 2)
        
        # If succeeded with a good streak, extend the interval slightly
        if self.success_streak >= 3:
            # After 3+ successes, add 1-2 days to interval (but don't exceed 14 days)
            bonus = min(2, self.success_streak // 3)
            return min(14, base_interval + bonus)
        
        return base_interval
    
    def _auto_adjust_difficulty(self):
        """
        Automatically adjust difficulty based on recent review performance.
        Looks at last 5 reviews to determine if difficulty should change.
        """
        # Need at least 5 reviews to auto-adjust
        if len(self.review_history) < 5:
            return
        
        recent_reviews = self.review_history[-5:]
        success_rate = sum(recent_reviews) / len(recent_reviews)
        
        # If consistently successful (80%+), make it easier
        if success_rate >= 0.8 and self.difficulty != DifficultyLevel.EASY:
            if self.difficulty == DifficultyLevel.HARD:
                self.difficulty = DifficultyLevel.MEDIUM
            elif self.difficulty == DifficultyLevel.MEDIUM:
                self.difficulty = DifficultyLevel.EASY
        
        # If struggling (40% or less), make it harder
        elif success_rate <= 0.4 and self.difficulty != DifficultyLevel.HARD:
            if self.difficulty == DifficultyLevel.EASY:
                self.difficulty = DifficultyLevel.MEDIUM
            elif self.difficulty == DifficultyLevel.MEDIUM:
                self.difficulty = DifficultyLevel.HARD
    
    def get_success_rate(self):
        """
        Calculate the success rate for this card.
        
        Returns:
            float: Success rate (0.0 to 1.0), or None if no reviews yet
        """
        if not self.review_history:
            return None
        return sum(self.review_history) / len(self.review_history)
    
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
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat(),
            'last_reviewed': self.last_reviewed.isoformat() if self.last_reviewed else None,
            'next_review': self.next_review.isoformat(),
            'review_count': self.review_count,
            'review_history': self.review_history,
            'last_mandatory_review': self.last_mandatory_review.isoformat() if self.last_mandatory_review else None,
            'success_streak': self.success_streak
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
            category=data.get('category'),  # Use .get() for backward compatibility
            user_id=data.get('user_id')  # Use .get() for backward compatibility
        )
        card.created_at = datetime.fromisoformat(data['created_at'])
        card.last_reviewed = datetime.fromisoformat(data['last_reviewed']) if data['last_reviewed'] else None
        card.next_review = datetime.fromisoformat(data['next_review'])
        card.review_count = data['review_count']
        # Handle new fields with backward compatibility
        card.review_history = data.get('review_history', [])
        card.last_mandatory_review = datetime.fromisoformat(data['last_mandatory_review']) if data.get('last_mandatory_review') else None
        card.success_streak = data.get('success_streak', 0)
        return card
    
    def __str__(self):
        """String representation of the flashcard."""
        return f"Flashcard(recto='{self.recto}', difficulty={self.difficulty.name})"
    
    def __repr__(self):
        """Detailed representation of the flashcard."""
        return (f"Flashcard(id={self.card_id}, recto='{self.recto}', verso='{self.verso}', "
                f"difficulty={self.difficulty.name}, reviews={self.review_count})")
