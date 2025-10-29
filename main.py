"""
Command-line interface for the Flashcard application.
"""
import random
from flashcard import DifficultyLevel
from flashcard_manager import FlashcardManager
from ui_components import ui, Colors


class FlashcardCLI:
    """Command-line interface for managing flashcards."""
    
    def __init__(self):
        """Initialize the CLI with a flashcard manager."""
        self.manager = FlashcardManager()
        self.running = True
    
    def display_menu(self):
        """Display the main menu."""
        print(ui.header("FLASHCARD APPLICATION", 60))
        print(ui.menu_option(1, "Create a new flashcard", "📝"))
        print(ui.menu_option(2, "View all flashcards", "📚"))
        print(ui.menu_option(3, "Study flashcards (review due cards)", "🎯"))
        print(ui.menu_option(4, "View statistics", "📊"))
        print(ui.menu_option(5, "Update card difficulty", "⚙️"))
        print(ui.menu_option(6, "Delete a flashcard", "🗑️"))
        print(ui.menu_option(7, "Exit", "👋"))
        print(ui.separator(60))
    
    def create_flashcard(self):
        """Create a new flashcard through user input."""
        print(ui.subheader("Create New Flashcard", 60))
        recto = input(ui.prompt("Enter the front side (recto)")).strip()
        if not recto:
            print(ui.error("Front side cannot be empty!"))
            return
        
        verso = input(ui.prompt("Enter the back side (verso)")).strip()
        if not verso:
            print(ui.error("Back side cannot be empty!"))
            return
        
        # Category input
        categories = self.manager.get_all_categories()
        if categories:
            print(f"\n{ui.bold('Existing categories:')} {', '.join(categories)}")
        category = input(ui.prompt("Enter category (optional, press Enter to skip)")).strip()
        category = category if category else None
        
        print("\n" + ui.bold("Select difficulty level:"))
        print(ui.menu_option(1, "Easy (review every 7 days)", "🟢"))
        print(ui.menu_option(2, "Medium (review every 3 days)", "🟡"))
        print(ui.menu_option(3, "Hard (review every 1 day)", "🔴"))
        
        difficulty_choice = input(ui.prompt("Enter choice (1-3)", "2")).strip()
        
        difficulty_map = {
            '1': DifficultyLevel.EASY,
            '2': DifficultyLevel.MEDIUM,
            '3': DifficultyLevel.HARD,
            '': DifficultyLevel.MEDIUM  # default
        }
        
        difficulty = difficulty_map.get(difficulty_choice, DifficultyLevel.MEDIUM)
        
        card = self.manager.add_flashcard(recto, verso, difficulty, category=category)
        print(f"\n{ui.success('Flashcard created successfully!')}")
        print(f"  {ui.colorize('ID:', Colors.CYAN)} {card.card_id}")
        if card.category:
            print(f"  {ui.colorize('Category:', Colors.CYAN)} 📁 {card.category}")
        print(f"  {ui.colorize('Difficulty:', Colors.CYAN)} {ui.difficulty_badge(card.difficulty.name)}")
    
    def view_all_flashcards(self):
        """Display all flashcards."""
        cards = self.manager.get_all_flashcards()
        
        if not cards:
            print(ui.info("No flashcards found. Create one first!"))
            return
        
        print(ui.subheader(f"All Flashcards ({len(cards)} total)", 60))
        for i, card in enumerate(cards, 1):
            if card.is_due_for_review():
                due_status = ui.colorize("✓ Due", Colors.BRIGHT_GREEN)
            else:
                due_status = ui.colorize("○ Not due", Colors.DIM)
            
            category_badge = f" 📁 {card.category}" if card.category else ""
            print(f"\n{ui.colorize(str(i), Colors.BRIGHT_CYAN)}. [{due_status}] {ui.difficulty_badge(card.difficulty.name)}{category_badge}")
            print(f"   {ui.colorize('Recto:', Colors.YELLOW)} {card.recto}")
            print(f"   {ui.colorize('Verso:', Colors.YELLOW)} {card.verso}")
            print(f"   {ui.colorize('Reviews:', Colors.CYAN)} {card.review_count}")
            print(f"   {ui.dim(f'ID: {card.card_id}')}")
    
    def study_flashcards(self):
        """Review flashcards that are due."""
        # Get all due cards first
        all_due_cards = self.manager.get_due_flashcards(shuffle=False)
        
        if not all_due_cards:
            print(ui.success("No flashcards due for review right now!"))
            return
        
        # Check if there are categories to filter by
        categories = self.manager.get_all_categories()
        selected_category = None
        
        if categories:
            print(ui.subheader("Category Selection", 60))
            print(f"{ui.bold('Available categories:')}")
            print(ui.menu_option(0, "All categories (review all due cards)", "📚"))
            for i, cat in enumerate(categories, 1):
                # Count due cards in this category
                cat_due_count = len([c for c in all_due_cards if c.category == cat])
                print(ui.menu_option(i, f"{cat} ({cat_due_count} due)", "📁"))
            
            choice = input(ui.prompt(f"Select category (0-{len(categories)})", "0")).strip()
            
            # Parse choice
            if choice.isdigit():
                choice_num = int(choice)
                if 1 <= choice_num <= len(categories):
                    selected_category = categories[choice_num - 1]
                    print(f"\n{ui.info(f'Studying category: 📁 {selected_category}')}")
        
        # Filter cards by category if selected
        if selected_category:
            due_cards = [card for card in all_due_cards if card.category == selected_category]
        else:
            due_cards = all_due_cards
        
        # Shuffle the cards
        random.shuffle(due_cards)
        
        if not due_cards:
            print(ui.warning(f"No flashcards due for review in category '{selected_category}'!"))
            return
        
        print(ui.subheader(f"Study Session ({len(due_cards)} cards due)", 60))
        print(ui.info("📝 Cards will be presented in random order"))
        
        for i, card in enumerate(due_cards, 1):
            # Show progress
            progress = ui.progress_bar(i - 1, len(due_cards), 40)
            print(f"\n{progress}")
            
            print(f"\n{ui.bold(f'Card {i}/{len(due_cards)}')} {ui.difficulty_badge(card.difficulty.name)}")
            print(ui.separator(60))
            print(f"{ui.colorize('Front:', Colors.BRIGHT_YELLOW)} {ui.bold(card.recto)}")
            input(ui.colorize("\n▶ Press Enter to reveal the back side...", Colors.BRIGHT_CYAN))
            print(f"{ui.colorize('Back:', Colors.BRIGHT_GREEN)} {ui.bold(card.verso)}")
            print(ui.separator(60))
            
            response = input(ui.prompt("Did you remember? (y/n)", "y")).strip().lower()
            
            if response in ['y', 'yes', '']:
                self.manager.mark_card_reviewed(card.card_id)
                print(ui.success("Marked as reviewed!"))
            else:
                print(ui.warning("Card will remain in review queue."))
            
            if i < len(due_cards):
                continue_study = input(ui.prompt("Continue to next card? (y/n)", "y")).strip().lower()
                if continue_study in ['n', 'no']:
                    break
        
        # Final progress
        progress = ui.progress_bar(len(due_cards), len(due_cards), 40)
        print(f"\n{progress}")
        print(ui.success("Study session complete!"))
    
    def view_statistics(self):
        """Display statistics about the flashcard collection."""
        stats = self.manager.get_statistics()
        
        print(ui.subheader("Flashcard Statistics", 60))
        print(ui.stat_line("Total flashcards", stats['total_cards'], Colors.BRIGHT_CYAN))
        print(ui.stat_line("Due for review", stats['due_for_review'], Colors.BRIGHT_YELLOW))
        print(ui.stat_line("Total reviews completed", stats['total_reviews'], Colors.BRIGHT_GREEN))
        
        print(f"\n{ui.colorize(ui.bold('By difficulty:'), Colors.BRIGHT_WHITE)}")
        print(ui.stat_line("  🟢 Easy", stats['easy_cards'], Colors.BRIGHT_GREEN))
        print(ui.stat_line("  🟡 Medium", stats['medium_cards'], Colors.BRIGHT_YELLOW))
        print(ui.stat_line("  🔴 Hard", stats['hard_cards'], Colors.BRIGHT_RED))
    
    def update_difficulty(self):
        """Update the difficulty of a flashcard."""
        cards = self.manager.get_all_flashcards()
        
        if not cards:
            print(ui.info("No flashcards found!"))
            return
        
        self.view_all_flashcards()
        
        card_id = input(ui.prompt("Enter the card ID to update")).strip()
        card = self.manager.get_flashcard(card_id)
        
        if not card:
            print(ui.error("Card not found!"))
            return
        
        print(f"\n{ui.colorize('Current difficulty:', Colors.CYAN)} {ui.difficulty_badge(card.difficulty.name)}")
        print("\n" + ui.bold("Select new difficulty level:"))
        print(ui.menu_option(1, "Easy (review every 7 days)", "🟢"))
        print(ui.menu_option(2, "Medium (review every 3 days)", "🟡"))
        print(ui.menu_option(3, "Hard (review every 1 day)", "🔴"))
        
        choice = input(ui.prompt("Enter choice (1-3)")).strip()
        
        difficulty_map = {
            '1': DifficultyLevel.EASY,
            '2': DifficultyLevel.MEDIUM,
            '3': DifficultyLevel.HARD
        }
        
        new_difficulty = difficulty_map.get(choice)
        
        if new_difficulty:
            self.manager.update_card_difficulty(card_id, new_difficulty)
            print(f"\n{ui.success(f'Difficulty updated to {new_difficulty.name}!')}")
        else:
            print(ui.error("Invalid choice!"))
    
    def delete_flashcard(self):
        """Delete a flashcard."""
        cards = self.manager.get_all_flashcards()
        
        if not cards:
            print(ui.info("No flashcards found!"))
            return
        
        self.view_all_flashcards()
        
        card_id = input(ui.prompt("Enter the card ID to delete")).strip()
        
        confirm = input(ui.colorize("⚠️  Are you sure you want to delete this card? (yes/no): ", Colors.BRIGHT_RED)).strip().lower()
        
        if confirm == 'yes':
            if self.manager.remove_flashcard(card_id):
                print(ui.success("Flashcard deleted successfully!"))
            else:
                print(ui.error("Card not found!"))
        else:
            print(ui.info("Deletion cancelled."))
    
    def run(self):
        """Run the main application loop."""
        print(ui.colorize("\n✨ Welcome to the Flashcard Application! ✨", Colors.BRIGHT_MAGENTA))
        
        while self.running:
            try:
                self.display_menu()
                choice = input(ui.prompt("Enter your choice (1-7)")).strip()
                
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
                    print(ui.colorize("\n✨ Thank you for using Flashcard Application. Goodbye! ✨\n", Colors.BRIGHT_MAGENTA))
                    self.running = False
                else:
                    print(ui.error("Invalid choice! Please enter a number between 1 and 7."))
            
            except KeyboardInterrupt:
                print(ui.colorize("\n\n👋 Exiting... Goodbye!\n", Colors.BRIGHT_YELLOW))
                self.running = False
            except Exception as e:
                print(ui.error(f"An error occurred: {e}"))
                print(ui.warning("Please try again."))


def main():
    """Main entry point for the application."""
    cli = FlashcardCLI()
    cli.run()


if __name__ == '__main__':
    main()
