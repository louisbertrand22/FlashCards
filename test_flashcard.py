#!/usr/bin/env python3
"""
Test script for the flashcard application.
Tests core functionality without requiring user interaction.
"""
import os
import json
from datetime import datetime, timedelta
from flashcard import Flashcard, DifficultyLevel
from flashcard_manager import FlashcardManager


def test_flashcard_creation():
    """Test creating flashcards with different difficulty levels."""
    print("Test 1: Creating flashcards...")
    
    # Test Easy card
    card1 = Flashcard("What is 2+2?", "4", DifficultyLevel.EASY)
    assert card1.recto == "What is 2+2?"
    assert card1.verso == "4"
    assert card1.difficulty == DifficultyLevel.EASY
    assert card1.review_count == 0
    print("  ✓ Easy flashcard created")
    
    # Test Medium card
    card2 = Flashcard("What is Python?", "A programming language", DifficultyLevel.MEDIUM)
    assert card2.difficulty == DifficultyLevel.MEDIUM
    print("  ✓ Medium flashcard created")
    
    # Test Hard card
    card3 = Flashcard("What is a monad?", "A monoid in the category of endofunctors", DifficultyLevel.HARD)
    assert card3.difficulty == DifficultyLevel.HARD
    print("  ✓ Hard flashcard created")
    
    print("✓ Test 1 passed!\n")
    return True


def test_difficulty_intervals():
    """Test that difficulty levels have correct review intervals."""
    print("Test 2: Testing difficulty intervals...")
    
    assert DifficultyLevel.EASY.get_review_interval() == 7
    print("  ✓ Easy: 7 days")
    
    assert DifficultyLevel.MEDIUM.get_review_interval() == 3
    print("  ✓ Medium: 3 days")
    
    assert DifficultyLevel.HARD.get_review_interval() == 1
    print("  ✓ Hard: 1 day")
    
    print("✓ Test 2 passed!\n")
    return True


def test_flashcard_review():
    """Test flashcard review functionality."""
    print("Test 3: Testing flashcard review...")
    
    card = Flashcard("Test question", "Test answer", DifficultyLevel.MEDIUM)
    
    # Initially should be due for review
    assert card.is_due_for_review()
    print("  ✓ New card is due for review")
    
    # Mark as reviewed
    card.mark_reviewed()
    assert card.review_count == 1
    assert card.last_reviewed is not None
    print("  ✓ Card marked as reviewed")
    
    # Should not be due immediately after review (3 day interval for MEDIUM)
    assert not card.is_due_for_review()
    print("  ✓ Card not due immediately after review")
    
    # Simulate time passing
    card.next_review = datetime.now() - timedelta(days=1)
    assert card.is_due_for_review()
    print("  ✓ Card becomes due after interval")
    
    print("✓ Test 3 passed!\n")
    return True


def test_flashcard_manager():
    """Test flashcard manager functionality."""
    print("Test 4: Testing flashcard manager...")
    
    # Use a test file
    test_file = 'test_flashcards.json'
    
    # Clean up if exists
    if os.path.exists(test_file):
        os.remove(test_file)
    
    # Create manager
    manager = FlashcardManager(test_file)
    
    # Add cards
    card1 = manager.add_flashcard("Question 1", "Answer 1", DifficultyLevel.EASY)
    card2 = manager.add_flashcard("Question 2", "Answer 2", DifficultyLevel.HARD)
    
    assert len(manager.get_all_flashcards()) == 2
    print("  ✓ Added 2 flashcards")
    
    # Test persistence
    manager2 = FlashcardManager(test_file)
    assert len(manager2.get_all_flashcards()) == 2
    print("  ✓ Flashcards persisted to file")
    
    # Test get due cards
    due_cards = manager2.get_due_flashcards()
    assert len(due_cards) == 2  # Both should be due initially
    print("  ✓ Found due flashcards")
    
    # Mark one as reviewed
    manager2.mark_card_reviewed(card1.card_id)
    due_cards = manager2.get_due_flashcards()
    assert len(due_cards) == 1  # Only one should be due now
    print("  ✓ Review status updated correctly")
    
    # Test statistics
    stats = manager2.get_statistics()
    assert stats['total_cards'] == 2
    assert stats['easy_cards'] == 1
    assert stats['hard_cards'] == 1
    assert stats['total_reviews'] == 1
    print("  ✓ Statistics calculated correctly")
    
    # Test update difficulty
    manager2.update_card_difficulty(card1.card_id, DifficultyLevel.HARD)
    updated_card = manager2.get_flashcard(card1.card_id)
    assert updated_card.difficulty == DifficultyLevel.HARD
    print("  ✓ Difficulty updated successfully")
    
    # Test remove card
    manager2.remove_flashcard(card1.card_id)
    assert len(manager2.get_all_flashcards()) == 1
    print("  ✓ Card removed successfully")
    
    # Clean up
    if os.path.exists(test_file):
        os.remove(test_file)
    
    print("✓ Test 4 passed!\n")
    return True


def test_serialization():
    """Test flashcard serialization and deserialization."""
    print("Test 5: Testing serialization...")
    
    # Create a card
    original = Flashcard("Test Q", "Test A", DifficultyLevel.MEDIUM)
    original.mark_reviewed()
    
    # Convert to dict
    data = original.to_dict()
    assert 'recto' in data
    assert 'verso' in data
    assert 'difficulty' in data
    print("  ✓ Card serialized to dict")
    
    # Recreate from dict
    restored = Flashcard.from_dict(data)
    assert restored.recto == original.recto
    assert restored.verso == original.verso
    assert restored.difficulty == original.difficulty
    assert restored.review_count == original.review_count
    print("  ✓ Card deserialized from dict")
    
    print("✓ Test 5 passed!\n")
    return True


def test_category_functionality():
    """Test category functionality."""
    print("Test 6: Testing category functionality...")
    
    # Use a test file
    test_file = 'test_flashcards_category.json'
    
    # Clean up if exists
    if os.path.exists(test_file):
        os.remove(test_file)
    
    # Create manager
    manager = FlashcardManager(test_file)
    
    # Add cards with categories
    card1 = manager.add_flashcard("Python question", "Python answer", DifficultyLevel.EASY, category="Programming")
    card2 = manager.add_flashcard("History question", "History answer", DifficultyLevel.MEDIUM, category="History")
    card3 = manager.add_flashcard("Math question", "Math answer", DifficultyLevel.HARD, category="Math")
    card4 = manager.add_flashcard("Another Python question", "Another Python answer", DifficultyLevel.EASY, category="Programming")
    card5 = manager.add_flashcard("No category question", "No category answer", DifficultyLevel.MEDIUM)
    
    assert len(manager.get_all_flashcards()) == 5
    print("  ✓ Added 5 flashcards with categories")
    
    # Test get by category
    programming_cards = manager.get_flashcards_by_category("Programming")
    assert len(programming_cards) == 2
    print("  ✓ Retrieved cards by category")
    
    # Test get all categories
    categories = manager.get_all_categories()
    assert len(categories) == 3
    assert "Programming" in categories
    assert "History" in categories
    assert "Math" in categories
    print("  ✓ Retrieved all categories")
    
    # Test persistence with category
    manager2 = FlashcardManager(test_file)
    assert len(manager2.get_all_flashcards()) == 5
    restored_card = manager2.get_flashcard(card1.card_id)
    assert restored_card.category == "Programming"
    print("  ✓ Categories persisted to file")
    
    # Test backward compatibility with None category
    no_cat_cards = [c for c in manager2.get_all_flashcards() if c.category is None]
    assert len(no_cat_cards) == 1
    print("  ✓ Backward compatibility with None category")
    
    # Clean up
    if os.path.exists(test_file):
        os.remove(test_file)
    
    print("✓ Test 6 passed!\n")
    return True


def test_shuffle_functionality():
    """Test shuffle functionality for due cards."""
    print("Test 7: Testing shuffle functionality...")
    
    # Use a test file
    test_file = 'test_flashcards_shuffle.json'
    
    # Clean up if exists
    if os.path.exists(test_file):
        os.remove(test_file)
    
    # Create manager with multiple cards
    manager = FlashcardManager(test_file)
    
    # Add 10 cards that are all due for review
    card_ids = []
    for i in range(10):
        card = manager.add_flashcard(f"Question {i}", f"Answer {i}", DifficultyLevel.EASY)
        card_ids.append(card.card_id)
    
    # Get due cards multiple times without shuffle - should be same order
    due_cards_1 = manager.get_due_flashcards(shuffle=False)
    due_cards_2 = manager.get_due_flashcards(shuffle=False)
    
    order_1 = [card.card_id for card in due_cards_1]
    order_2 = [card.card_id for card in due_cards_2]
    
    assert order_1 == order_2
    print("  ✓ Non-shuffled cards maintain order")
    
    # Get due cards with shuffle multiple times
    # With 10 cards, the probability of getting the same order is 1/10! which is extremely low
    shuffled_orders = []
    for _ in range(5):
        shuffled_cards = manager.get_due_flashcards(shuffle=True)
        shuffled_order = [card.card_id for card in shuffled_cards]
        shuffled_orders.append(shuffled_order)
    
    # Check that at least one shuffle produced a different order
    # (very unlikely all 5 would be the same with 10 cards)
    unique_orders = len(set(tuple(order) for order in shuffled_orders))
    assert unique_orders > 1
    print(f"  ✓ Shuffle produces different orders ({unique_orders} unique orders in 5 attempts)")
    
    # Verify all shuffled results contain the same cards (just in different order)
    for shuffled_order in shuffled_orders:
        assert set(shuffled_order) == set(card_ids)
    print("  ✓ Shuffled results contain all cards")
    
    # Clean up
    if os.path.exists(test_file):
        os.remove(test_file)
    
    print("✓ Test 7 passed!\n")
    return True


def test_category_filtered_study():
    """Test getting due flashcards filtered by category."""
    print("Test 8: Testing category-filtered study mode...")
    
    # Use a test file
    test_file = 'test_flashcards_study_filter.json'
    
    # Clean up if exists
    if os.path.exists(test_file):
        os.remove(test_file)
    
    # Create manager with cards in different categories
    manager = FlashcardManager(test_file)
    
    # Add cards with different categories, all due for review
    card1 = manager.add_flashcard("Python Q1", "Python A1", DifficultyLevel.EASY, category="Programming")
    card2 = manager.add_flashcard("Python Q2", "Python A2", DifficultyLevel.MEDIUM, category="Programming")
    card3 = manager.add_flashcard("Python Q3", "Python A3", DifficultyLevel.HARD, category="Programming")
    card4 = manager.add_flashcard("History Q1", "History A1", DifficultyLevel.EASY, category="History")
    card5 = manager.add_flashcard("History Q2", "History A2", DifficultyLevel.MEDIUM, category="History")
    card6 = manager.add_flashcard("Math Q1", "Math A1", DifficultyLevel.EASY, category="Math")
    card7 = manager.add_flashcard("No category Q", "No category A", DifficultyLevel.EASY)
    
    assert len(manager.get_all_flashcards()) == 7
    print("  ✓ Added 7 flashcards with various categories")
    
    # Test getting all due cards (should be all 7 initially)
    all_due = manager.get_due_flashcards()
    assert len(all_due) == 7
    print("  ✓ All cards are due for review")
    
    # Test filtering by category
    programming_due = [c for c in all_due if c.category == "Programming"]
    assert len(programming_due) == 3
    print("  ✓ 3 Programming cards are due")
    
    history_due = [c for c in all_due if c.category == "History"]
    assert len(history_due) == 2
    print("  ✓ 2 History cards are due")
    
    math_due = [c for c in all_due if c.category == "Math"]
    assert len(math_due) == 1
    print("  ✓ 1 Math card is due")
    
    no_category_due = [c for c in all_due if c.category is None]
    assert len(no_category_due) == 1
    print("  ✓ 1 card with no category is due")
    
    # Mark some Programming cards as reviewed
    manager.mark_card_reviewed(card1.card_id)
    manager.mark_card_reviewed(card2.card_id)
    
    # Check that only 1 Programming card is still due
    all_due_after = manager.get_due_flashcards()
    programming_due_after = [c for c in all_due_after if c.category == "Programming"]
    assert len(programming_due_after) == 1
    print("  ✓ Only 1 Programming card is due after reviewing 2")
    
    # Other categories should still have same count
    history_due_after = [c for c in all_due_after if c.category == "History"]
    assert len(history_due_after) == 2
    print("  ✓ History cards unchanged (still 2 due)")
    
    # Total due should be 5 now (7 - 2 reviewed)
    assert len(all_due_after) == 5
    print("  ✓ Total due cards reduced correctly")
    
    # Clean up
    if os.path.exists(test_file):
        os.remove(test_file)
    
    print("✓ Test 8 passed!\n")
    return True


def test_review_history():
    """Test review history tracking with success/failure."""
    print("Test 9: Testing review history...")
    
    card = Flashcard("Test Q", "Test A", DifficultyLevel.MEDIUM)
    
    # Initially empty review history
    assert len(card.review_history) == 0
    assert card.success_streak == 0
    print("  ✓ Initial review history is empty")
    
    # Mark as reviewed successfully
    card.mark_reviewed(success=True)
    assert len(card.review_history) == 1
    assert card.review_history[0] == True
    assert card.success_streak == 1
    print("  ✓ Successful review recorded")
    
    # Another successful review
    card.mark_reviewed(success=True)
    assert len(card.review_history) == 2
    assert card.review_history[1] == True
    assert card.success_streak == 2
    print("  ✓ Success streak increments")
    
    # Failed review
    card.mark_reviewed(success=False)
    assert len(card.review_history) == 3
    assert card.review_history[2] == False
    assert card.success_streak == 0
    print("  ✓ Failed review resets streak")
    
    # Test success rate calculation
    success_rate = card.get_success_rate()
    assert success_rate == 2/3  # 2 successes out of 3 reviews
    print(f"  ✓ Success rate calculated: {success_rate:.2%}")
    
    print("✓ Test 9 passed!\n")
    return True


def test_mandatory_review_cycle():
    """Test mandatory 2-week review cycle."""
    print("Test 10: Testing mandatory 2-week review cycle...")
    
    card = Flashcard("Test Q", "Test A", DifficultyLevel.EASY)
    
    # Initially no mandatory review
    assert card.last_mandatory_review is None
    print("  ✓ Initial state: no mandatory review")
    
    # New card should be due for initial review
    assert card.is_due_for_review()
    print("  ✓ New card is due for review")
    
    # Mark as reviewed
    card.mark_reviewed(success=True)
    assert not card.is_due_for_review()  # Not due yet (7 day interval for EASY)
    print("  ✓ Card not due immediately after review")
    
    # Simulate 2 weeks passing from creation
    card.created_at = datetime.now() - timedelta(days=15)
    card.last_mandatory_review = None  # Reset to test mandatory review
    assert card.is_due_for_review()
    print("  ✓ Card is due after 2 weeks (mandatory review)")
    
    # Mark as reviewed again - this should set last_mandatory_review
    card.mark_reviewed(success=True)
    assert card.last_mandatory_review is not None
    print("  ✓ Mandatory review timestamp recorded")
    
    # Even if normal interval hasn't passed, card should be due after 2 weeks from mandatory
    card.next_review = datetime.now() + timedelta(days=5)  # Set far in future
    card.last_mandatory_review = datetime.now() - timedelta(days=15)  # But 15 days ago
    assert card.is_due_for_review()
    print("  ✓ Mandatory 2-week cycle overrides normal interval")
    
    print("✓ Test 10 passed!\n")
    return True


def test_auto_difficulty_adjustment():
    """Test automatic difficulty adjustment based on performance."""
    print("Test 11: Testing auto difficulty adjustment...")
    
    # Test: HARD card with consistent success should become MEDIUM
    card = Flashcard("Test Q", "Test A", DifficultyLevel.HARD)
    
    # Simulate 5 successful reviews (needed for auto-adjust)
    for _ in range(5):
        card.mark_reviewed(success=True)
    
    # Should have adjusted from HARD to MEDIUM (80%+ success rate)
    assert card.difficulty == DifficultyLevel.MEDIUM
    print("  ✓ HARD card auto-adjusted to MEDIUM after consistent success")
    
    # Test: EASY card with poor performance should become MEDIUM
    card2 = Flashcard("Test Q2", "Test A2", DifficultyLevel.EASY)
    
    # Simulate mixed reviews with 40% or less success rate
    for i in range(5):
        card2.mark_reviewed(success=(i < 2))  # Only 2 successes out of 5 = 40%
    
    # Should have adjusted from EASY to MEDIUM
    assert card2.difficulty == DifficultyLevel.MEDIUM
    print("  ✓ EASY card auto-adjusted to MEDIUM after poor performance")
    
    # Test: MEDIUM card stays if performance is moderate
    card3 = Flashcard("Test Q3", "Test A3", DifficultyLevel.MEDIUM)
    
    # Simulate moderate performance (60% success rate)
    for i in range(5):
        card3.mark_reviewed(success=(i < 3))  # 3 successes out of 5 = 60%
    
    # Should remain MEDIUM (not 80%+ or ≤40%)
    assert card3.difficulty == DifficultyLevel.MEDIUM
    print("  ✓ MEDIUM card remains MEDIUM with moderate performance")
    
    print("✓ Test 11 passed!\n")
    return True


def test_adaptive_intervals():
    """Test adaptive review intervals based on success/failure."""
    print("Test 12: Testing adaptive review intervals...")
    
    card = Flashcard("Test Q", "Test A", DifficultyLevel.MEDIUM)
    
    # Failed review should reduce interval
    card.mark_reviewed(success=False)
    next_review_after_fail = card.next_review
    # Medium is 3 days, failed should be 1-2 days (halved, min 1)
    expected_max = datetime.now() + timedelta(days=2)
    assert card.next_review <= expected_max
    print("  ✓ Failed review reduces next interval")
    
    # Build up a success streak
    card2 = Flashcard("Test Q2", "Test A2", DifficultyLevel.MEDIUM)
    for _ in range(3):
        card2.mark_reviewed(success=True)
    
    # With streak of 3+, interval should be extended
    assert card2.success_streak >= 3
    # Medium is 3 days, with streak bonus should be 4-5 days
    expected_min = datetime.now() + timedelta(days=3)
    assert card2.next_review >= expected_min
    print("  ✓ Success streak extends interval")
    
    print("✓ Test 12 passed!\n")
    return True


def test_new_statistics():
    """Test new statistics with review history."""
    print("Test 13: Testing new statistics...")
    
    # Use a test file
    test_file = 'test_flashcards_stats.json'
    
    # Clean up if exists
    if os.path.exists(test_file):
        os.remove(test_file)
    
    # Create manager
    manager = FlashcardManager(test_file)
    
    # Add cards
    card1 = manager.add_flashcard("Q1", "A1", DifficultyLevel.EASY)
    card2 = manager.add_flashcard("Q2", "A2", DifficultyLevel.MEDIUM)
    
    # Review cards with mixed results
    manager.mark_card_reviewed(card1.card_id, success=True)
    manager.mark_card_reviewed(card1.card_id, success=True)
    manager.mark_card_reviewed(card1.card_id, success=True)
    manager.mark_card_reviewed(card2.card_id, success=True)
    manager.mark_card_reviewed(card2.card_id, success=False)
    
    stats = manager.get_statistics()
    
    # Check new statistics
    assert 'overall_success_rate' in stats
    assert 'best_streak' in stats
    assert 'cards_with_streaks' in stats
    
    assert stats['overall_success_rate'] == 80.0  # 4 successes / 5 total = 80%
    assert stats['best_streak'] == 3  # card1 has streak of 3
    assert stats['cards_with_streaks'] == 1  # only card1 has active streak (card2 failed last review)
    print("  ✓ New statistics calculated correctly")
    
    # Clean up
    if os.path.exists(test_file):
        os.remove(test_file)
    
    print("✓ Test 13 passed!\n")
    return True


def test_backward_compatibility():
    """Test that old flashcards without new fields load correctly."""
    print("Test 14: Testing backward compatibility...")
    
    # Create a flashcard dict in old format (without new fields)
    old_format_data = {
        'card_id': 'test_card_123',
        'recto': 'Old Question',
        'verso': 'Old Answer',
        'difficulty': 'MEDIUM',
        'category': 'Test',
        'created_at': datetime.now().isoformat(),
        'last_reviewed': None,
        'next_review': datetime.now().isoformat(),
        'review_count': 0
    }
    
    # Load from old format
    card = Flashcard.from_dict(old_format_data)
    
    # Check that new fields have default values
    assert card.review_history == []
    assert card.last_mandatory_review is None
    assert card.success_streak == 0
    print("  ✓ Old format loads with default values for new fields")
    
    # Should be able to use new features
    card.mark_reviewed(success=True)
    assert len(card.review_history) == 1
    assert card.success_streak == 1
    print("  ✓ Old flashcards can use new features after loading")
    
    # Serialization should include new fields
    new_data = card.to_dict()
    assert 'review_history' in new_data
    assert 'last_mandatory_review' in new_data
    assert 'success_streak' in new_data
    print("  ✓ Reserialization includes new fields")
    
    print("✓ Test 14 passed!\n")
    return True


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("           FLASHCARD APPLICATION TEST SUITE")
    print("=" * 60)
    print()
    
    tests = [
        test_flashcard_creation,
        test_difficulty_intervals,
        test_flashcard_review,
        test_flashcard_manager,
        test_serialization,
        test_category_functionality,
        test_shuffle_functionality,
        test_category_filtered_study,
        test_review_history,
        test_mandatory_review_cycle,
        test_auto_difficulty_adjustment,
        test_adaptive_intervals,
        test_new_statistics,
        test_backward_compatibility
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except AssertionError as e:
            print(f"✗ Test failed: {e}\n")
            failed += 1
        except Exception as e:
            print(f"✗ Test error: {e}\n")
            failed += 1
    
    print("=" * 60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    exit(0 if success else 1)
