#!/usr/bin/env python3
"""
Demo script showing the flashcard application in action.
Creates sample flashcards and demonstrates the functionality.
"""
import os
from flashcard import DifficultyLevel
from flashcard_manager import FlashcardManager
from ui_components import ui, Colors


def demo():
    """Run a demonstration of the flashcard application."""
    print(ui.header("FLASHCARD APPLICATION DEMO", 60))
    
    # Use a demo file
    demo_file = 'demo_flashcards.json'
    
    # Clean up if exists
    if os.path.exists(demo_file):
        os.remove(demo_file)
    
    # Create manager
    print(ui.info("Creating flashcard manager..."))
    manager = FlashcardManager(demo_file)
    print()
    
    # Create sample flashcards
    print(ui.subheader("Adding Sample Flashcards", 60))
    
    cards_data = [
        ("What is the capital of France?", "Paris", DifficultyLevel.EASY),
        ("What is 15 x 12?", "180", DifficultyLevel.MEDIUM),
        ("What is the time complexity of quicksort?", "O(n log n) average, O(n²) worst", DifficultyLevel.HARD),
        ("Who wrote 'Romeo and Juliet'?", "William Shakespeare", DifficultyLevel.EASY),
        ("What is the formula for the Pythagorean theorem?", "a² + b² = c²", DifficultyLevel.MEDIUM),
    ]
    
    for recto, verso, difficulty in cards_data:
        card = manager.add_flashcard(recto, verso, difficulty)
        print(ui.success(f"Created {ui.difficulty_badge(difficulty.name)} card: '{recto}'"))
    
    print()
    print(ui.colorize(f"✨ Total cards created: {len(manager.get_all_flashcards())}", Colors.BRIGHT_MAGENTA))
    
    # Display statistics
    print(ui.subheader("STATISTICS", 60))
    stats = manager.get_statistics()
    print(ui.stat_line("Total flashcards", stats['total_cards'], Colors.BRIGHT_CYAN))
    print(ui.stat_line("Due for review", stats['due_for_review'], Colors.BRIGHT_YELLOW))
    print(ui.stat_line("Easy cards", f"{stats['easy_cards']} (reviewed every 7 days)", Colors.BRIGHT_GREEN))
    print(ui.stat_line("Medium cards", f"{stats['medium_cards']} (reviewed every 3 days)", Colors.BRIGHT_YELLOW))
    print(ui.stat_line("Hard cards", f"{stats['hard_cards']} (reviewed every 1 day)", Colors.BRIGHT_RED))
    print()
    
    # Show all cards
    print(ui.subheader("ALL FLASHCARDS", 60))
    for i, card in enumerate(manager.get_all_flashcards(), 1):
        due_status = ui.colorize("✓ Due", Colors.BRIGHT_GREEN) if card.is_due_for_review() else ui.dim("○ Not due")
        print(f"\n{ui.colorize(str(i), Colors.BRIGHT_CYAN)}. {ui.difficulty_badge(card.difficulty.name)} [{due_status}]")
        print(f"   {ui.colorize('Front:', Colors.YELLOW)} {card.recto}")
        print(f"   {ui.colorize('Back:', Colors.YELLOW)} {card.verso}")
    
    print(ui.subheader("SIMULATING REVIEW SESSION", 60))
    
    # Mark some cards as reviewed
    due_cards = manager.get_due_flashcards()
    print(f"\n{ui.colorize(f'Cards due for review: {len(due_cards)}', Colors.BRIGHT_YELLOW)}")
    
    if due_cards:
        card = due_cards[0]
        print(f"\n{ui.colorize('Reviewing card:', Colors.CYAN)} {ui.bold(card.recto)}")
        print(f"{ui.colorize('Answer:', Colors.GREEN)} {ui.bold(card.verso)}")
        manager.mark_card_reviewed(card.card_id)
        print(ui.success("Marked as reviewed!"))
        print(ui.colorize(f"Next review scheduled in {card.difficulty.get_review_interval()} day(s)", Colors.CYAN))
    
    print(ui.subheader("UPDATED STATISTICS", 60))
    stats = manager.get_statistics()
    print(ui.stat_line("Total flashcards", stats['total_cards'], Colors.BRIGHT_CYAN))
    print(ui.stat_line("Due for review", stats['due_for_review'], Colors.BRIGHT_YELLOW))
    print(ui.stat_line("Total reviews completed", stats['total_reviews'], Colors.BRIGHT_GREEN))
    
    print(ui.subheader("DEMO COMPLETE!", 60))
    print()
    print(ui.colorize(f"📁 Demo data saved to: {demo_file}", Colors.BRIGHT_CYAN))
    print(ui.colorize("🚀 You can run 'python main.py' to use the interactive application!", Colors.BRIGHT_MAGENTA))
    print()


if __name__ == '__main__':
    demo()
