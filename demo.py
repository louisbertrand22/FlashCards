#!/usr/bin/env python3
"""
Demo script showing the flashcard application in action.
Creates sample flashcards and demonstrates the functionality.
"""
import os
from flashcard import DifficultyLevel
from flashcard_manager import FlashcardManager


def demo():
    """Run a demonstration of the flashcard application."""
    print("=" * 60)
    print("         FLASHCARD APPLICATION DEMO")
    print("=" * 60)
    print()
    
    # Use a demo file
    demo_file = 'demo_flashcards.json'
    
    # Clean up if exists
    if os.path.exists(demo_file):
        os.remove(demo_file)
    
    # Create manager
    print("Creating flashcard manager...")
    manager = FlashcardManager(demo_file)
    print()
    
    # Create sample flashcards
    print("Adding sample flashcards...")
    print()
    
    cards_data = [
        ("What is the capital of France?", "Paris", DifficultyLevel.EASY),
        ("What is 15 x 12?", "180", DifficultyLevel.MEDIUM),
        ("What is the time complexity of quicksort?", "O(n log n) average, O(n²) worst", DifficultyLevel.HARD),
        ("Who wrote 'Romeo and Juliet'?", "William Shakespeare", DifficultyLevel.EASY),
        ("What is the formula for the Pythagorean theorem?", "a² + b² = c²", DifficultyLevel.MEDIUM),
    ]
    
    for recto, verso, difficulty in cards_data:
        card = manager.add_flashcard(recto, verso, difficulty)
        print(f"  ✓ Created {difficulty.name} card: '{recto}'")
    
    print()
    print(f"Total cards created: {len(manager.get_all_flashcards())}")
    print()
    
    # Display statistics
    print("-" * 60)
    print("STATISTICS")
    print("-" * 60)
    stats = manager.get_statistics()
    print(f"Total flashcards: {stats['total_cards']}")
    print(f"Due for review: {stats['due_for_review']}")
    print(f"Easy cards: {stats['easy_cards']} (reviewed every 7 days)")
    print(f"Medium cards: {stats['medium_cards']} (reviewed every 3 days)")
    print(f"Hard cards: {stats['hard_cards']} (reviewed every 1 day)")
    print()
    
    # Show all cards
    print("-" * 60)
    print("ALL FLASHCARDS")
    print("-" * 60)
    for i, card in enumerate(manager.get_all_flashcards(), 1):
        print(f"\n{i}. [{card.difficulty.name}]")
        print(f"   Front: {card.recto}")
        print(f"   Back: {card.verso}")
        print(f"   Due: {'Yes' if card.is_due_for_review() else 'No'}")
    
    print()
    print("-" * 60)
    print("SIMULATING REVIEW SESSION")
    print("-" * 60)
    
    # Mark some cards as reviewed
    due_cards = manager.get_due_flashcards()
    print(f"\nCards due for review: {len(due_cards)}")
    
    if due_cards:
        card = due_cards[0]
        print(f"\nReviewing card: '{card.recto}'")
        print(f"Answer: '{card.verso}'")
        manager.mark_card_reviewed(card.card_id)
        print("✓ Marked as reviewed!")
        print(f"Next review scheduled in {card.difficulty.get_review_interval()} day(s)")
    
    print()
    print("-" * 60)
    print("UPDATED STATISTICS")
    print("-" * 60)
    stats = manager.get_statistics()
    print(f"Total flashcards: {stats['total_cards']}")
    print(f"Due for review: {stats['due_for_review']}")
    print(f"Total reviews completed: {stats['total_reviews']}")
    
    print()
    print("-" * 60)
    print("DEMO COMPLETE!")
    print("-" * 60)
    print()
    print(f"Demo data saved to: {demo_file}")
    print("You can run 'python main.py' to use the interactive application!")
    print()


if __name__ == '__main__':
    demo()
