"""
FlashcardManager class for managing a collection of flashcards.
"""
import json
import os
import random
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
    
    def add_flashcard(self, recto, verso, difficulty=DifficultyLevel.MEDIUM, category=None, user_id=None):
        """
        Add a new flashcard.
        
        Args:
            recto (str): Front side of the card
            verso (str): Back side of the card
            difficulty (DifficultyLevel): Difficulty level
            category (str): Optional category for organizing cards
            user_id (str): Optional user ID for multi-user support
            
        Returns:
            Flashcard: The created flashcard
        """
        card = Flashcard(recto, verso, difficulty, category=category, user_id=user_id)
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
    
    def get_all_flashcards(self, user_id=None):
        """
        Get all flashcards, optionally filtered by user.
        
        Args:
            user_id (str): Optional user ID to filter by
            
        Returns:
            list: List of flashcards
        """
        if user_id is None:
            return self.flashcards
        return [card for card in self.flashcards if card.user_id == user_id]
    
    def get_due_flashcards(self, shuffle=False, user_id=None):
        """
        Get all flashcards that are due for review.
        
        Args:
            shuffle (bool): If True, return cards in random order
            user_id (str): Optional user ID to filter by
            
        Returns:
            list: List of due flashcards
        """
        due_cards = [card for card in self.flashcards if card.is_due_for_review()]
        if user_id is not None:
            due_cards = [card for card in due_cards if card.user_id == user_id]
        if shuffle:
            random.shuffle(due_cards)
        return due_cards
    
    def get_flashcards_by_difficulty(self, difficulty):
        """
        Get all flashcards of a specific difficulty.
        
        Args:
            difficulty (DifficultyLevel): The difficulty level
            
        Returns:
            list: List of flashcards with the specified difficulty
        """
        return [card for card in self.flashcards if card.difficulty == difficulty]
    
    def get_flashcards_by_category(self, category):
        """
        Get all flashcards of a specific category.
        
        Args:
            category (str): The category name
            
        Returns:
            list: List of flashcards with the specified category
        """
        return [card for card in self.flashcards if card.category == category]
    
    def get_all_categories(self):
        """
        Get all unique categories from flashcards.
        
        Returns:
            list: Sorted list of unique category names (excluding None)
        """
        categories = set()
        for card in self.flashcards:
            if card.category:
                categories.add(card.category)
        return sorted(list(categories))
    
    def save_flashcards(self):
        """Save flashcards to the storage file."""
        try:
            data = [card.to_dict() for card in self.flashcards]
            with open(self.storage_file, 'w') as f:
                json.dump(data, f, indent=2)
        except PermissionError:
            print(f"Error: Permission denied when trying to write to {self.storage_file}")
            print("Please check file permissions or choose a different location.")
        except OSError as e:
            print(f"Error: Could not save flashcards to {self.storage_file}: {e}")
            print("Please check that the directory exists and is writable.")
    
    def load_flashcards(self):
        """Load flashcards from the storage file."""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.flashcards = [Flashcard.from_dict(card_data) for card_data in data]
            except (json.JSONDecodeError, KeyError):
                print(f"Warning: Could not load flashcards from {self.storage_file}")
                self.flashcards = []
            except PermissionError:
                print(f"Error: Permission denied when trying to read from {self.storage_file}")
                print("Please check file permissions.")
                self.flashcards = []
            except OSError as e:
                print(f"Error: Could not load flashcards from {self.storage_file}: {e}")
                self.flashcards = []
        else:
            # Try to load sample data if this is the default storage file
            # and sample data exists (for initial deployment)
            storage_basename = os.path.basename(self.storage_file)
            if storage_basename == self.DEFAULT_STORAGE_FILE:
                # Look for sample file in the same directory as this Python module
                # This ensures it works both when storage is in current dir and in /app/data
                module_dir = os.path.dirname(os.path.abspath(__file__))
                sample_file = os.path.join(module_dir, self.SAMPLE_DATA_FILE)
                
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
                    except PermissionError:
                        print(f"Error: Permission denied when trying to read from {sample_file}")
                        self.flashcards = []
                    except OSError as e:
                        print(f"Error: Could not load sample flashcards from {sample_file}: {e}")
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
    
    def mark_card_reviewed(self, card_id, success=True):
        """
        Mark a card as reviewed.
        
        Args:
            card_id (str): ID of the card
            success (bool): Whether the review was successful (default: True)
            
        Returns:
            bool: True if marked, False if not found
        """
        card = self.get_flashcard(card_id)
        if card:
            card.mark_reviewed(success)
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
        
        # Calculate overall success rate
        total_successes = sum(sum(card.review_history) for card in self.flashcards if card.review_history)
        total_review_history = sum(len(card.review_history) for card in self.flashcards)
        overall_success_rate = (total_successes / total_review_history * 100) if total_review_history > 0 else 0
        
        # Find best streak
        best_streak = max((card.success_streak for card in self.flashcards), default=0)
        
        # Count cards with active streaks
        cards_with_streaks = sum(1 for card in self.flashcards if card.success_streak > 0)
        
        return {
            'total_cards': total,
            'due_for_review': due,
            'easy_cards': easy,
            'medium_cards': medium,
            'hard_cards': hard,
            'total_reviews': total_reviews,
            'overall_success_rate': round(overall_success_rate, 1),
            'best_streak': best_streak,
            'cards_with_streaks': cards_with_streaks
        }
