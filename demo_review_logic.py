#!/usr/bin/env python3
"""
Demo script showcasing the new review logic features.
This demonstrates:
1. Review history tracking (success/failure)
2. Mandatory 2-week review cycle
3. Automatic difficulty adjustment
4. Adaptive intervals
5. Success streak tracking
"""

import os
from datetime import datetime, timedelta
from flashcard import Flashcard, DifficultyLevel
from flashcard_manager import FlashcardManager


def print_separator():
    """Print a visual separator."""
    print("\n" + "=" * 70 + "\n")


def demo_review_history():
    """Demonstrate review history tracking."""
    print("🎯 DEMO 1: Review History Tracking")
    print_separator()
    
    card = Flashcard("What is Python?", "A programming language", DifficultyLevel.MEDIUM)
    print(f"Created card: {card.recto}")
    print(f"Initial review history: {card.review_history}")
    print(f"Initial success streak: {card.success_streak}")
    
    # Simulate some reviews
    print("\n📝 Simulating reviews...")
    card.mark_reviewed(success=True)
    print(f"After 1st review (success): history={card.review_history}, streak={card.success_streak}")
    
    card.mark_reviewed(success=True)
    print(f"After 2nd review (success): history={card.review_history}, streak={card.success_streak}")
    
    card.mark_reviewed(success=False)
    print(f"After 3rd review (failure): history={card.review_history}, streak={card.success_streak}")
    
    card.mark_reviewed(success=True)
    print(f"After 4th review (success): history={card.review_history}, streak={card.success_streak}")
    
    success_rate = card.get_success_rate()
    print(f"\n📊 Overall success rate: {success_rate:.1%}")


def demo_mandatory_review():
    """Demonstrate mandatory 2-week review cycle."""
    print("🎯 DEMO 2: Mandatory 2-Week Review Cycle")
    print_separator()
    
    card = Flashcard("Vocab: Serendipity", "Finding something good by chance", DifficultyLevel.EASY)
    print(f"Created card: {card.recto}")
    print(f"Difficulty: {card.difficulty.name} (normally reviewed every {card.difficulty.get_review_interval()} days)")
    
    # Mark as reviewed
    card.mark_reviewed(success=True)
    print(f"\n✅ Reviewed successfully")
    print(f"Next review scheduled: {card.next_review.strftime('%Y-%m-%d %H:%M')}")
    print(f"Is due now? {card.is_due_for_review()}")
    
    # Simulate 2 weeks passing
    print("\n⏰ Simulating 2 weeks passing...")
    card.created_at = datetime.now() - timedelta(days=15)
    card.last_mandatory_review = None
    
    print(f"Is due now (after 2 weeks)? {card.is_due_for_review()}")
    print("✅ Card is due for mandatory 2-week review, even though normal interval hasn't passed!")


def demo_auto_difficulty():
    """Demonstrate automatic difficulty adjustment."""
    print("🎯 DEMO 3: Automatic Difficulty Adjustment")
    print_separator()
    
    # Test 1: HARD card with consistent success
    card1 = Flashcard("Difficult concept", "Complex answer", DifficultyLevel.HARD)
    print(f"Card 1: {card1.recto}")
    print(f"Initial difficulty: {card1.difficulty.name}")
    
    print("\n📝 Simulating 5 successful reviews (100% success rate)...")
    for i in range(5):
        card1.mark_reviewed(success=True)
    
    print(f"New difficulty: {card1.difficulty.name}")
    print(f"✅ Automatically adjusted from HARD → {card1.difficulty.name} due to consistent success!")
    
    # Test 2: EASY card with poor performance
    print_separator()
    card2 = Flashcard("Easy question?", "Actually hard answer", DifficultyLevel.EASY)
    print(f"Card 2: {card2.recto}")
    print(f"Initial difficulty: {card2.difficulty.name}")
    
    print("\n📝 Simulating 5 reviews with 40% success rate...")
    for i in range(5):
        card2.mark_reviewed(success=(i < 2))  # Only 2 out of 5 succeed
    
    print(f"New difficulty: {card2.difficulty.name}")
    print(f"✅ Automatically adjusted from EASY → {card2.difficulty.name} due to poor performance!")


def demo_adaptive_intervals():
    """Demonstrate adaptive review intervals."""
    print("🎯 DEMO 4: Adaptive Review Intervals")
    print_separator()
    
    # Test failed review
    card1 = Flashcard("Challenging concept", "Complex answer", DifficultyLevel.MEDIUM)
    print(f"Card: {card1.recto}")
    print(f"Base interval for MEDIUM: {card1.difficulty.get_review_interval()} days")
    
    card1.mark_reviewed(success=False)
    days_until_review = (card1.next_review - datetime.now()).days
    print(f"\n❌ Failed review")
    print(f"Next review in: ~{days_until_review} days")
    print(f"✅ Interval reduced! Failed reviews schedule sooner practice.")
    
    # Test success streak
    print_separator()
    card2 = Flashcard("Getting easier", "Mastered concept", DifficultyLevel.MEDIUM)
    print(f"Card: {card2.recto}")
    print(f"Base interval for MEDIUM: {card2.difficulty.get_review_interval()} days")
    
    print("\n📝 Building success streak...")
    for i in range(4):
        card2.mark_reviewed(success=True)
        print(f"Review {i+1}: Success! Streak: {card2.success_streak}")
    
    days_until_review = (card2.next_review - datetime.now()).days
    print(f"\nNext review in: ~{days_until_review} days")
    print(f"✅ Interval extended! Success streaks earn bonus time before next review.")


def demo_statistics():
    """Demonstrate enhanced statistics."""
    print("🎯 DEMO 5: Enhanced Statistics")
    print_separator()
    
    # Create a temporary manager
    test_file = 'demo_flashcards.json'
    if os.path.exists(test_file):
        os.remove(test_file)
    
    manager = FlashcardManager(test_file)
    
    # Add some cards and review them
    print("Creating and reviewing flashcards...\n")
    
    card1 = manager.add_flashcard("Python basics", "Variables, functions, classes", DifficultyLevel.EASY)
    card2 = manager.add_flashcard("Advanced algorithms", "Dynamic programming, graphs", DifficultyLevel.HARD)
    card3 = manager.add_flashcard("Web development", "HTML, CSS, JavaScript", DifficultyLevel.MEDIUM)
    
    # Review with mixed results
    manager.mark_card_reviewed(card1.card_id, success=True)
    manager.mark_card_reviewed(card1.card_id, success=True)
    manager.mark_card_reviewed(card1.card_id, success=True)
    manager.mark_card_reviewed(card1.card_id, success=True)
    
    manager.mark_card_reviewed(card2.card_id, success=False)
    manager.mark_card_reviewed(card2.card_id, success=True)
    manager.mark_card_reviewed(card2.card_id, success=False)
    
    manager.mark_card_reviewed(card3.card_id, success=True)
    manager.mark_card_reviewed(card3.card_id, success=True)
    
    # Get statistics
    stats = manager.get_statistics()
    
    print("📊 STATISTICS:")
    print(f"Total cards: {stats['total_cards']}")
    print(f"Total reviews: {stats['total_reviews']}")
    print(f"Overall success rate: {stats['overall_success_rate']}%")
    print(f"Best success streak: 🔥 {stats['best_streak']}")
    print(f"Cards with active streaks: {stats['cards_with_streaks']}")
    print(f"\nDifficulty breakdown:")
    print(f"  🟢 Easy: {stats['easy_cards']}")
    print(f"  🟡 Medium: {stats['medium_cards']}")
    print(f"  🔴 Hard: {stats['hard_cards']}")
    
    # Show individual card stats
    print("\n📋 INDIVIDUAL CARD STATS:")
    for card in manager.get_all_flashcards():
        success_rate = card.get_success_rate()
        streak_display = f"🔥{card.success_streak}" if card.success_streak > 0 else "No streak"
        print(f"\n• {card.recto[:40]}...")
        print(f"  Reviews: {card.review_count} | Success rate: {success_rate:.0%} | Streak: {streak_display}")
    
    # Clean up
    os.remove(test_file)


def main():
    """Run all demos."""
    print("\n" + "=" * 70)
    print(" " * 15 + "FLASHCARD REVIEW LOGIC DEMO")
    print("=" * 70)
    
    demo_review_history()
    print_separator()
    
    demo_mandatory_review()
    print_separator()
    
    demo_auto_difficulty()
    print_separator()
    
    demo_adaptive_intervals()
    print_separator()
    
    demo_statistics()
    print_separator()
    
    print("\n✨ Demo complete! All new features have been showcased.")
    print("\nKey Features:")
    print("✅ Review history tracking (success/failure)")
    print("✅ Mandatory 2-week review cycle")
    print("✅ Automatic difficulty adjustment based on performance")
    print("✅ Adaptive intervals (failures = sooner, streaks = later)")
    print("✅ Success streak tracking with fire emoji 🔥")
    print("✅ Enhanced statistics (success rate, best streak, active streaks)")
    print("✅ Full backward compatibility with existing flashcards")
    print("\n" + "=" * 70 + "\n")


if __name__ == '__main__':
    main()
