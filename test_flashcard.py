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
    assert card.is_due_for_review() == True
    print("  ✓ New card is due for review")
    
    # Mark as reviewed
    card.mark_reviewed()
    assert card.review_count == 1
    assert card.last_reviewed is not None
    print("  ✓ Card marked as reviewed")
    
    # Should not be due immediately after review (3 day interval for MEDIUM)
    assert card.is_due_for_review() == False
    print("  ✓ Card not due immediately after review")
    
    # Simulate time passing
    card.next_review = datetime.now() - timedelta(days=1)
    assert card.is_due_for_review() == True
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
        test_serialization
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
