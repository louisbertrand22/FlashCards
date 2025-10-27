"""
Command-line interface for the Flashcard application.
"""
from flashcard import DifficultyLevel
from flashcard_manager import FlashcardManager


class FlashcardCLI:
    """Command-line interface for managing flashcards."""
    
    def __init__(self):
        """Initialize the CLI with a flashcard manager."""
        self.manager = FlashcardManager()
        self.running = True
    
    def display_menu(self):
        """Display the main menu."""
        print("\n" + "=" * 50)
        print("          FLASHCARD APPLICATION")
        print("=" * 50)
        print("\n[1] Create a new flashcard")
        print("[2] View all flashcards")
        print("[3] Study flashcards (review due cards)")
        print("[4] View statistics")
        print("[5] Update card difficulty")
        print("[6] Delete a flashcard")
        print("[7] Exit")
        print("-" * 50)
    
    def create_flashcard(self):
        """Create a new flashcard through user input."""
        print("\n--- Create New Flashcard ---")
        recto = input("Enter the front side (recto): ").strip()
        if not recto:
            print("Error: Front side cannot be empty!")
            return
        
        verso = input("Enter the back side (verso): ").strip()
        if not verso:
            print("Error: Back side cannot be empty!")
            return
        
        print("\nSelect difficulty level:")
        print("[1] Easy (review every 7 days)")
        print("[2] Medium (review every 3 days)")
        print("[3] Hard (review every 1 day)")
        
        difficulty_choice = input("Enter choice (1-3) [default: 2]: ").strip()
        
        difficulty_map = {
            '1': DifficultyLevel.EASY,
            '2': DifficultyLevel.MEDIUM,
            '3': DifficultyLevel.HARD,
            '': DifficultyLevel.MEDIUM  # default
        }
        
        difficulty = difficulty_map.get(difficulty_choice, DifficultyLevel.MEDIUM)
        
        card = self.manager.add_flashcard(recto, verso, difficulty)
        print(f"\n✓ Flashcard created successfully!")
        print(f"  ID: {card.card_id}")
        print(f"  Difficulty: {card.difficulty.name}")
    
    def view_all_flashcards(self):
        """Display all flashcards."""
        cards = self.manager.get_all_flashcards()
        
        if not cards:
            print("\nNo flashcards found. Create one first!")
            return
        
        print(f"\n--- All Flashcards ({len(cards)} total) ---")
        for i, card in enumerate(cards, 1):
            due_status = "✓ Due" if card.is_due_for_review() else "○ Not due"
            print(f"\n{i}. [{due_status}] {card.difficulty.name}")
            print(f"   Recto: {card.recto}")
            print(f"   Verso: {card.verso}")
            print(f"   Reviews: {card.review_count}")
            print(f"   ID: {card.card_id}")
    
    def study_flashcards(self):
        """Review flashcards that are due."""
        due_cards = self.manager.get_due_flashcards()
        
        if not due_cards:
            print("\n✓ No flashcards due for review right now!")
            return
        
        print(f"\n--- Study Session ({len(due_cards)} cards due) ---")
        
        for i, card in enumerate(due_cards, 1):
            print(f"\n\nCard {i}/{len(due_cards)} [{card.difficulty.name}]")
            print("-" * 50)
            print(f"Front: {card.recto}")
            input("\nPress Enter to reveal the back side...")
            print(f"Back: {card.verso}")
            print("-" * 50)
            
            response = input("\nDid you remember? (y/n) [y]: ").strip().lower()
            
            if response in ['y', 'yes', '']:
                self.manager.mark_card_reviewed(card.card_id)
                print("✓ Marked as reviewed!")
            else:
                print("Card will remain in review queue.")
            
            if i < len(due_cards):
                continue_study = input("\nContinue to next card? (y/n) [y]: ").strip().lower()
                if continue_study in ['n', 'no']:
                    break
        
        print("\n✓ Study session complete!")
    
    def view_statistics(self):
        """Display statistics about the flashcard collection."""
        stats = self.manager.get_statistics()
        
        print("\n--- Flashcard Statistics ---")
        print(f"Total flashcards: {stats['total_cards']}")
        print(f"Due for review: {stats['due_for_review']}")
        print(f"Total reviews completed: {stats['total_reviews']}")
        print("\nBy difficulty:")
        print(f"  Easy: {stats['easy_cards']}")
        print(f"  Medium: {stats['medium_cards']}")
        print(f"  Hard: {stats['hard_cards']}")
    
    def update_difficulty(self):
        """Update the difficulty of a flashcard."""
        cards = self.manager.get_all_flashcards()
        
        if not cards:
            print("\nNo flashcards found!")
            return
        
        self.view_all_flashcards()
        
        card_id = input("\nEnter the card ID to update: ").strip()
        card = self.manager.get_flashcard(card_id)
        
        if not card:
            print("Error: Card not found!")
            return
        
        print(f"\nCurrent difficulty: {card.difficulty.name}")
        print("\nSelect new difficulty level:")
        print("[1] Easy (review every 7 days)")
        print("[2] Medium (review every 3 days)")
        print("[3] Hard (review every 1 day)")
        
        choice = input("Enter choice (1-3): ").strip()
        
        difficulty_map = {
            '1': DifficultyLevel.EASY,
            '2': DifficultyLevel.MEDIUM,
            '3': DifficultyLevel.HARD
        }
        
        new_difficulty = difficulty_map.get(choice)
        
        if new_difficulty:
            self.manager.update_card_difficulty(card_id, new_difficulty)
            print(f"\n✓ Difficulty updated to {new_difficulty.name}!")
        else:
            print("Error: Invalid choice!")
    
    def delete_flashcard(self):
        """Delete a flashcard."""
        cards = self.manager.get_all_flashcards()
        
        if not cards:
            print("\nNo flashcards found!")
            return
        
        self.view_all_flashcards()
        
        card_id = input("\nEnter the card ID to delete: ").strip()
        
        confirm = input(f"Are you sure you want to delete this card? (yes/no): ").strip().lower()
        
        if confirm == 'yes':
            if self.manager.remove_flashcard(card_id):
                print("\n✓ Flashcard deleted successfully!")
            else:
                print("Error: Card not found!")
        else:
            print("Deletion cancelled.")
    
    def run(self):
        """Run the main application loop."""
        print("\nWelcome to the Flashcard Application!")
        
        while self.running:
            try:
                self.display_menu()
                choice = input("\nEnter your choice (1-7): ").strip()
                
                if choice == '1':
                    self.create_flashcard()
                elif choice == '2':
                    self.view_all_flashcards()
                elif choice == '3':
                    self.study_flashcards()
                elif choice == '4':
                    self.view_statistics()
                elif choice == '5':
                    self.update_difficulty()
                elif choice == '6':
                    self.delete_flashcard()
                elif choice == '7':
                    print("\nThank you for using Flashcard Application. Goodbye!")
                    self.running = False
                else:
                    print("\nInvalid choice! Please enter a number between 1 and 7.")
            
            except KeyboardInterrupt:
                print("\n\nExiting... Goodbye!")
                self.running = False
            except Exception as e:
                print(f"\nAn error occurred: {e}")
                print("Please try again.")


def main():
    """Main entry point for the application."""
    cli = FlashcardCLI()
    cli.run()


if __name__ == '__main__':
    main()
