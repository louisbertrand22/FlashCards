#!/usr/bin/env python3
"""
Test script for JWT authentication functionality.
"""
import os
import json
import sys
from auth_models import User
from user_manager import UserManager


def test_user_creation():
    """Test creating users with password hashing."""
    print("Test 1: Creating users with password hashing...")
    
    # Test user creation
    user = User(username="testuser", password_hash=User.hash_password("password123"))
    assert user.username == "testuser"
    assert user.user_id is not None
    assert user.password_hash is not None
    print("  ✓ User created with hashed password")
    
    # Test password verification
    assert user.verify_password("password123")
    print("  ✓ Correct password verified")
    
    assert not user.verify_password("wrongpassword")
    print("  ✓ Wrong password rejected")
    
    print("✓ Test 1 passed!\n")
    return True


def test_user_serialization():
    """Test user serialization and deserialization."""
    print("Test 2: Testing user serialization...")
    
    # Create a user
    original = User(username="testuser", password_hash=User.hash_password("password123"))
    
    # Convert to dict
    data = original.to_dict()
    assert 'user_id' in data
    assert 'username' in data
    assert 'password_hash' in data
    print("  ✓ User serialized to dict")
    
    # Recreate from dict
    restored = User.from_dict(data)
    assert restored.username == original.username
    assert restored.user_id == original.user_id
    assert restored.password_hash == original.password_hash
    print("  ✓ User deserialized from dict")
    
    # Verify password still works
    assert restored.verify_password("password123")
    print("  ✓ Password verification works after deserialization")
    
    print("✓ Test 2 passed!\n")
    return True


def test_user_manager():
    """Test user manager functionality."""
    print("Test 3: Testing user manager...")
    
    # Use a test file
    test_file = 'test_users.json'
    
    # Clean up if exists
    if os.path.exists(test_file):
        os.remove(test_file)
    
    # Create manager
    manager = UserManager(test_file)
    
    # Create users
    user1 = manager.create_user("alice", "password123")
    user2 = manager.create_user("bob", "password456")
    
    assert user1 is not None
    assert user2 is not None
    assert user1.username == "alice"
    assert user2.username == "bob"
    print("  ✓ Created 2 users")
    
    # Test duplicate username
    user3 = manager.create_user("alice", "differentpassword")
    assert user3 is None
    print("  ✓ Duplicate username rejected")
    
    # Test persistence
    manager2 = UserManager(test_file)
    alice = manager2.get_user("alice")
    assert alice is not None
    assert alice.username == "alice"
    print("  ✓ Users persisted to file")
    
    # Test authentication
    auth_user = manager2.authenticate_user("alice", "password123")
    assert auth_user is not None
    assert auth_user.username == "alice"
    print("  ✓ User authenticated with correct password")
    
    auth_user2 = manager2.authenticate_user("alice", "wrongpassword")
    assert auth_user2 is None
    print("  ✓ Authentication failed with wrong password")
    
    auth_user3 = manager2.authenticate_user("nonexistent", "password")
    assert auth_user3 is None
    print("  ✓ Authentication failed for non-existent user")
    
    # Test get user by ID
    user_by_id = manager2.get_user_by_id(user1.user_id)
    assert user_by_id is not None
    assert user_by_id.username == "alice"
    print("  ✓ User retrieved by ID")
    
    # Clean up
    if os.path.exists(test_file):
        os.remove(test_file)
    
    print("✓ Test 3 passed!\n")
    return True


def test_flashcard_user_association():
    """Test flashcard association with users."""
    print("Test 4: Testing flashcard user association...")
    
    from flashcard import Flashcard, DifficultyLevel
    from flashcard_manager import FlashcardManager
    
    # Use a test file
    test_file = 'test_flashcards_jwt.json'
    
    # Clean up if exists
    if os.path.exists(test_file):
        os.remove(test_file)
    
    # Create manager
    manager = FlashcardManager(test_file)
    
    # Create flashcards for different users
    card1 = manager.add_flashcard("Question 1", "Answer 1", DifficultyLevel.EASY, user_id="user1")
    card2 = manager.add_flashcard("Question 2", "Answer 2", DifficultyLevel.MEDIUM, user_id="user1")
    card3 = manager.add_flashcard("Question 3", "Answer 3", DifficultyLevel.HARD, user_id="user2")
    
    assert card1.user_id == "user1"
    assert card2.user_id == "user1"
    assert card3.user_id == "user2"
    print("  ✓ Flashcards created with user associations")
    
    # Get cards for user1
    user1_cards = manager.get_all_flashcards(user_id="user1")
    assert len(user1_cards) == 2
    assert all(card.user_id == "user1" for card in user1_cards)
    print("  ✓ Retrieved cards for user1")
    
    # Get cards for user2
    user2_cards = manager.get_all_flashcards(user_id="user2")
    assert len(user2_cards) == 1
    assert user2_cards[0].user_id == "user2"
    print("  ✓ Retrieved cards for user2")
    
    # Get all cards (no filter)
    all_cards = manager.get_all_flashcards()
    assert len(all_cards) == 3
    print("  ✓ Retrieved all cards without filter")
    
    # Test persistence with user_id
    manager2 = FlashcardManager(test_file)
    restored_card = manager2.get_flashcard(card1.card_id)
    assert restored_card.user_id == "user1"
    print("  ✓ User association persisted to file")
    
    # Test backward compatibility (cards without user_id)
    card4 = manager2.add_flashcard("Question 4", "Answer 4", DifficultyLevel.MEDIUM)
    assert card4.user_id is None
    print("  ✓ Backward compatibility: cards without user_id supported")
    
    # Clean up
    if os.path.exists(test_file):
        os.remove(test_file)
    
    print("✓ Test 4 passed!\n")
    return True


def test_due_cards_user_filter():
    """Test getting due cards filtered by user."""
    print("Test 5: Testing due cards with user filtering...")
    
    from flashcard import Flashcard, DifficultyLevel
    from flashcard_manager import FlashcardManager
    
    # Use a test file
    test_file = 'test_flashcards_due_jwt.json'
    
    # Clean up if exists
    if os.path.exists(test_file):
        os.remove(test_file)
    
    # Create manager
    manager = FlashcardManager(test_file)
    
    # Add cards for different users (all initially due)
    card1 = manager.add_flashcard("Q1", "A1", DifficultyLevel.EASY, user_id="user1")
    card2 = manager.add_flashcard("Q2", "A2", DifficultyLevel.EASY, user_id="user1")
    card3 = manager.add_flashcard("Q3", "A3", DifficultyLevel.EASY, user_id="user2")
    card4 = manager.add_flashcard("Q4", "A4", DifficultyLevel.EASY, user_id="user2")
    card5 = manager.add_flashcard("Q5", "A5", DifficultyLevel.EASY, user_id="user2")
    
    # Get due cards for user1
    user1_due = manager.get_due_flashcards(user_id="user1")
    assert len(user1_due) == 2
    assert all(card.user_id == "user1" for card in user1_due)
    print("  ✓ Retrieved due cards for user1")
    
    # Get due cards for user2
    user2_due = manager.get_due_flashcards(user_id="user2")
    assert len(user2_due) == 3
    assert all(card.user_id == "user2" for card in user2_due)
    print("  ✓ Retrieved due cards for user2")
    
    # Mark some cards as reviewed
    manager.mark_card_reviewed(card1.card_id)
    manager.mark_card_reviewed(card3.card_id)
    
    # Check due cards again
    user1_due_after = manager.get_due_flashcards(user_id="user1")
    assert len(user1_due_after) == 1  # Only card2 should be due
    print("  ✓ User1 due cards updated after review")
    
    user2_due_after = manager.get_due_flashcards(user_id="user2")
    assert len(user2_due_after) == 2  # card4 and card5 should be due
    print("  ✓ User2 due cards updated after review")
    
    # Get all due cards (no filter)
    all_due = manager.get_due_flashcards()
    assert len(all_due) == 3  # card2, card4, card5
    print("  ✓ Retrieved all due cards without filter")
    
    # Clean up
    if os.path.exists(test_file):
        os.remove(test_file)
    
    print("✓ Test 5 passed!\n")
    return True


def test_api_integration():
    """Test API integration with Flask app."""
    print("Test 6: Testing API integration...")
    
    try:
        from app import app
        app.config['TESTING'] = True
        client = app.test_client()
        
        # Test registration
        response = client.post('/api/auth/register', 
                              json={'username': 'testuser', 'password': 'password123'})
        assert response.status_code == 201
        data = json.loads(response.data)
        assert 'user_id' in data
        assert data['username'] == 'testuser'
        print("  ✓ User registration works")
        
        # Test duplicate registration
        response = client.post('/api/auth/register',
                              json={'username': 'testuser', 'password': 'password456'})
        assert response.status_code == 409
        print("  ✓ Duplicate registration rejected")
        
        # Test login
        response = client.post('/api/auth/login',
                              json={'username': 'testuser', 'password': 'password123'})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'access_token' in data
        assert 'refresh_token' in data
        access_token = data['access_token']
        print("  ✓ User login works")
        
        # Test login with wrong password
        response = client.post('/api/auth/login',
                              json={'username': 'testuser', 'password': 'wrongpassword'})
        assert response.status_code == 401
        print("  ✓ Login with wrong password rejected")
        
        # Test protected endpoint without token
        response = client.get('/api/cards')
        assert response.status_code == 401
        print("  ✓ Protected endpoint requires authentication")
        
        # Test protected endpoint with token
        headers = {'Authorization': f'Bearer {access_token}'}
        response = client.get('/api/cards', headers=headers)
        assert response.status_code == 200
        print("  ✓ Protected endpoint accessible with token")
        
        # Test creating a card
        response = client.post('/api/cards',
                              json={'recto': 'Test Q', 'verso': 'Test A', 'difficulty': 'MEDIUM'},
                              headers=headers)
        assert response.status_code == 201
        data = json.loads(response.data)
        assert 'card' in data
        card_id = data['card']['card_id']
        print("  ✓ Card creation works")
        
        # Test getting user's cards
        response = client.get('/api/cards', headers=headers)
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['total'] == 1
        print("  ✓ Getting user's cards works")
        
        # Test getting stats
        response = client.get('/api/stats', headers=headers)
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['total_cards'] == 1
        print("  ✓ Getting stats works")
        
        # Clean up test files
        import glob
        for f in glob.glob('test_*.json'):
            if os.path.exists(f):
                os.remove(f)
        
        print("✓ Test 6 passed!\n")
        return True
        
    except Exception as e:
        print(f"  ✗ API integration test failed: {e}")
        return False


def test_legacy_card_access():
    """Test that legacy cards (without user_id) are accessible by authenticated users."""
    print("Test 7: Testing legacy card access...")
    
    try:
        from app import app
        from api import manager as api_manager  # Use the same manager instance as the API
        from flashcard import DifficultyLevel
        
        # Set up Flask test client
        app.config['TESTING'] = True
        client = app.test_client()
        
        # Create a legacy card (without user_id) using the API's manager
        legacy_card = api_manager.add_flashcard("Legacy Q", "Legacy A", DifficultyLevel.MEDIUM)
        legacy_card_id = legacy_card.card_id
        
        # Verify it has no user_id
        assert legacy_card.user_id is None
        print("  ✓ Legacy card created without user_id")
        
        # Register and login a user
        client.post('/api/auth/register', json={'username': 'testuser2', 'password': 'password123'})
        response = client.post('/api/auth/login', json={'username': 'testuser2', 'password': 'password123'})
        access_token = json.loads(response.data)['access_token']
        headers = {'Authorization': f'Bearer {access_token}'}
        
        # Try to access the legacy card
        response = client.get(f'/api/cards/{legacy_card_id}', headers=headers)
        assert response.status_code == 200
        print("  ✓ Authenticated user can access legacy card")
        
        # Try to update the legacy card
        response = client.put(f'/api/cards/{legacy_card_id}',
                             json={'difficulty': 'HARD'},
                             headers=headers)
        assert response.status_code == 200
        print("  ✓ Authenticated user can update legacy card")
        
        # Try to review the legacy card
        response = client.post(f'/api/cards/{legacy_card_id}/review',
                              json={'success': True},
                              headers=headers)
        assert response.status_code == 200
        print("  ✓ Authenticated user can review legacy card")
        
        # Try to delete the legacy card
        response = client.delete(f'/api/cards/{legacy_card_id}', headers=headers)
        assert response.status_code == 200
        print("  ✓ Authenticated user can delete legacy card")
        
        print("✓ Test 7 passed!\n")
        return True
        
    except Exception as e:
        import traceback
        print(f"  ✗ Legacy card access test failed: {e}")
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all JWT authentication tests."""
    print("=" * 60)
    print("      JWT AUTHENTICATION TEST SUITE")
    print("=" * 60)
    print()
    
    tests = [
        test_user_creation,
        test_user_serialization,
        test_user_manager,
        test_flashcard_user_association,
        test_due_cards_user_filter,
        test_api_integration,
        test_legacy_card_access
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
    sys.exit(0 if success else 1)
