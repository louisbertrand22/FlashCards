"""
FlashcardManager class for managing a collection of flashcards.
"""
import json
import os
from flashcard import Flashcard, DifficultyLevel


class FlashcardManager:
    """Manages a collection of flashcards with persistence."""
    
    # Default filenames for storage and sample data
    DEFAULT_STORAGE_FILE = 'flashcards.json'
    SAMPLE_DATA_FILE = 'sample_flashcards.json'
    
    def __init__(self, storage_file=None):
        """
        Initialize the flashcard manager.
        
        Args:
            storage_file (str, optional): Path to the JSON file for storing flashcards.
                                          Defaults to DEFAULT_STORAGE_FILE ('flashcards.json') if None.
        """
        self.storage_file = storage_file if storage_file is not None else self.DEFAULT_STORAGE_FILE
        self.flashcards = []
        self.load_flashcards()
    
    def add_flashcard(self, recto, verso, difficulty=DifficultyLevel.MEDIUM):
        """
        Add a new flashcard.
        
        Args:
            recto (str): Front side of the card
            verso (str): Back side of the card
            difficulty (DifficultyLevel): Difficulty level
            
        Returns:
            Flashcard: The created flashcard
        """
        card = Flashcard(recto, verso, difficulty)
        self.flashcards.append(card)
        self.save_flashcards()
        return card
    
    def remove_flashcard(self, card_id):
        """
        Remove a flashcard by ID.
        
        Args:
            card_id (str): ID of the card to remove
            
        Returns:
            bool: True if removed, False if not found
        """
        for i, card in enumerate(self.flashcards):
            if card.card_id == card_id:
                self.flashcards.pop(i)
                self.save_flashcards()
                return True
        return False
    
    def get_flashcard(self, card_id):
        """
        Get a flashcard by ID.
        
        Args:
            card_id (str): ID of the card
            
        Returns:
            Flashcard or None: The flashcard if found
        """
        for card in self.flashcards:
            if card.card_id == card_id:
                return card
        return None
    
    def get_all_flashcards(self):
        """Get all flashcards."""
        return self.flashcards
    
    def get_due_flashcards(self):
        """Get all flashcards that are due for review."""
        return [card for card in self.flashcards if card.is_due_for_review()]
    
    def get_flashcards_by_difficulty(self, difficulty):
        """
        Get all flashcards of a specific difficulty.
        
        Args:
            difficulty (DifficultyLevel): The difficulty level
            
        Returns:
            list: List of flashcards with the specified difficulty
        """
        return [card for card in self.flashcards if card.difficulty == difficulty]
    
    def save_flashcards(self):
        """Save flashcards to the storage file."""
        data = [card.to_dict() for card in self.flashcards]
        with open(self.storage_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_flashcards(self):
        """Load flashcards from the storage file."""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r') as f:
                    data = json.load(f)
                    self.flashcards = [Flashcard.from_dict(card_data) for card_data in data]
            except (json.JSONDecodeError, KeyError):
                print(f"Warning: Could not load flashcards from {self.storage_file}")
                self.flashcards = []
        else:
            # Try to load sample data if this is the default storage file
            # and sample data exists (for initial deployment)
            storage_basename = os.path.basename(self.storage_file)
            if storage_basename == self.DEFAULT_STORAGE_FILE:
                sample_file = self.SAMPLE_DATA_FILE
                storage_dir = os.path.dirname(self.storage_file)
                if storage_dir:
                    sample_file = os.path.join(storage_dir, self.SAMPLE_DATA_FILE)
                
                if os.path.exists(sample_file):
                    try:
                        with open(sample_file, 'r') as f:
                            data = json.load(f)
                            self.flashcards = [Flashcard.from_dict(card_data) for card_data in data]
                        # Save to the main storage file for future use
                        self.save_flashcards()
                        print(f"Loaded {len(self.flashcards)} sample flashcards")
                    except (json.JSONDecodeError, KeyError):
                        print(f"Warning: Could not load sample flashcards from {sample_file}")
                        self.flashcards = []
                else:
                    self.flashcards = []
            else:
                # For non-default files (e.g., test files), start with empty list
                self.flashcards = []
    
    def update_card_difficulty(self, card_id, new_difficulty):
        """
        Update the difficulty of a flashcard.
        
        Args:
            card_id (str): ID of the card
            new_difficulty (DifficultyLevel): New difficulty level
            
        Returns:
            bool: True if updated, False if not found
        """
        card = self.get_flashcard(card_id)
        if card:
            card.update_difficulty(new_difficulty)
            self.save_flashcards()
            return True
        return False
    
    def mark_card_reviewed(self, card_id):
        """
        Mark a card as reviewed.
        
        Args:
            card_id (str): ID of the card
            
        Returns:
            bool: True if marked, False if not found
        """
        card = self.get_flashcard(card_id)
        if card:
            card.mark_reviewed()
            self.save_flashcards()
            return True
        return False
    
    def get_statistics(self):
        """
        Get statistics about the flashcard collection.
        
        Returns:
            dict: Dictionary with statistics
        """
        total = len(self.flashcards)
        due = len(self.get_due_flashcards())
        easy = len(self.get_flashcards_by_difficulty(DifficultyLevel.EASY))
        medium = len(self.get_flashcards_by_difficulty(DifficultyLevel.MEDIUM))
        hard = len(self.get_flashcards_by_difficulty(DifficultyLevel.HARD))
        
        total_reviews = sum(card.review_count for card in self.flashcards)
        
        return {
            'total_cards': total,
            'due_for_review': due,
            'easy_cards': easy,
            'medium_cards': medium,
            'hard_cards': hard,
            'total_reviews': total_reviews
        }
