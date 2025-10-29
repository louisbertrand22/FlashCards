# JWT Authentication API Documentation

This document provides comprehensive documentation for the JWT-based authentication API implemented in the FlashCards application.

## Table of Contents

1. [Overview](#overview)
2. [Authentication Endpoints](#authentication-endpoints)
3. [Flashcard API Endpoints](#flashcard-api-endpoints)
4. [Error Handling](#error-handling)
5. [Security Considerations](#security-considerations)
6. [Examples](#examples)

## Overview

The FlashCards application now supports JWT (JSON Web Token) based authentication, allowing multiple users to securely manage their own flashcard collections. The API provides:

- User registration and authentication
- JWT token-based authorization
- User-specific flashcard management
- Token refresh mechanism
- Secure password storage using bcrypt

### Base URL

All API endpoints are prefixed with `/api`:

- Authentication endpoints: `/api/auth/*`
- Flashcard endpoints: `/api/*`

### Authentication

Most endpoints require authentication using JWT tokens. Include the access token in the Authorization header:

```
Authorization: Bearer <your_access_token>
```

### Token Expiration

- **Access Token**: Expires after 1 hour
- **Refresh Token**: Expires after 30 days

Use the refresh endpoint to obtain a new access token before it expires.

## Authentication Endpoints

### Register a New User

Creates a new user account.

**Endpoint:** `POST /api/auth/register`

**Request Body:**
```json
{
  "username": "johndoe",
  "password": "securepassword123"
}
```

**Validation:**
- Username: minimum 3 characters
- Password: minimum 6 characters
- Username must be unique

**Success Response (201 Created):**
```json
{
  "message": "User registered successfully",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "username": "johndoe"
}
```

**Error Responses:**
- `400 Bad Request`: Missing or invalid fields
- `409 Conflict`: Username already exists

---

### Login

Authenticate and receive JWT tokens.

**Endpoint:** `POST /api/auth/login`

**Request Body:**
```json
{
  "username": "johndoe",
  "password": "securepassword123"
}
```

**Success Response (200 OK):**
```json
{
  "message": "Login successful",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "username": "johndoe"
}
```

**Error Responses:**
- `400 Bad Request`: Missing username or password
- `401 Unauthorized`: Invalid credentials

---

### Refresh Token

Obtain a new access token using a refresh token.

**Endpoint:** `POST /api/auth/refresh`

**Headers:**
```
Authorization: Bearer <your_refresh_token>
```

**Success Response (200 OK):**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Error Responses:**
- `401 Unauthorized`: Invalid or expired refresh token

---

### Get Current User

Retrieve information about the authenticated user.

**Endpoint:** `GET /api/auth/me`

**Headers:**
```
Authorization: Bearer <your_access_token>
```

**Success Response (200 OK):**
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "username": "johndoe",
  "created_at": "2024-01-15T10:30:00"
}
```

**Error Responses:**
- `401 Unauthorized`: Missing or invalid token
- `404 Not Found`: User not found

## Flashcard API Endpoints

All flashcard endpoints require authentication with an access token.

### Get All Cards

Retrieve all flashcards for the authenticated user.

**Endpoint:** `GET /api/cards`

**Query Parameters:**
- `category` (optional): Filter by category name

**Headers:**
```
Authorization: Bearer <your_access_token>
```

**Success Response (200 OK):**
```json
{
  "cards": [
    {
      "card_id": "card_abc123",
      "recto": "What is Python?",
      "verso": "A high-level programming language",
      "difficulty": "MEDIUM",
      "category": "Programming",
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "created_at": "2024-01-15T10:30:00",
      "last_reviewed": null,
      "next_review": "2024-01-15T10:30:00",
      "review_count": 0,
      "review_history": [],
      "success_streak": 0
    }
  ],
  "total": 1
}
```

---

### Create a Card

Create a new flashcard.

**Endpoint:** `POST /api/cards`

**Headers:**
```
Authorization: Bearer <your_access_token>
```

**Request Body:**
```json
{
  "recto": "What is JWT?",
  "verso": "JSON Web Token - a standard for securely transmitting information",
  "difficulty": "MEDIUM",
  "category": "Security"
}
```

**Fields:**
- `recto` (required): Front side of the card
- `verso` (required): Back side of the card
- `difficulty` (required): One of `EASY`, `MEDIUM`, or `HARD`
- `category` (optional): Category name for organization

**Success Response (201 Created):**
```json
{
  "message": "Flashcard created successfully",
  "card": {
    "card_id": "card_xyz789",
    "recto": "What is JWT?",
    "verso": "JSON Web Token - a standard for securely transmitting information",
    "difficulty": "MEDIUM",
    "category": "Security",
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    ...
  }
}
```

**Error Responses:**
- `400 Bad Request`: Missing required fields or invalid difficulty
- `401 Unauthorized`: Missing or invalid token

---

### Get a Specific Card

Retrieve details of a specific flashcard.

**Endpoint:** `GET /api/cards/<card_id>`

**Headers:**
```
Authorization: Bearer <your_access_token>
```

**Success Response (200 OK):**
```json
{
  "card": {
    "card_id": "card_xyz789",
    ...
  }
}
```

**Error Responses:**
- `403 Forbidden`: Card belongs to another user
- `404 Not Found`: Card not found

---

### Update Card Difficulty

Update a flashcard's difficulty level.

**Endpoint:** `PUT /api/cards/<card_id>`

**Headers:**
```
Authorization: Bearer <your_access_token>
```

**Request Body:**
```json
{
  "difficulty": "HARD"
}
```

**Success Response (200 OK):**
```json
{
  "message": "Card difficulty updated successfully",
  "card": {
    ...
  }
}
```

**Error Responses:**
- `400 Bad Request`: Missing or invalid difficulty
- `403 Forbidden`: Card belongs to another user
- `404 Not Found`: Card not found

---

### Delete a Card

Delete a flashcard.

**Endpoint:** `DELETE /api/cards/<card_id>`

**Headers:**
```
Authorization: Bearer <your_access_token>
```

**Success Response (200 OK):**
```json
{
  "message": "Flashcard deleted successfully"
}
```

**Error Responses:**
- `403 Forbidden`: Card belongs to another user
- `404 Not Found`: Card not found

---

### Review a Card

Mark a card as reviewed with success/failure status.

**Endpoint:** `POST /api/cards/<card_id>/review`

**Headers:**
```
Authorization: Bearer <your_access_token>
```

**Request Body:**
```json
{
  "success": true
}
```

**Fields:**
- `success` (optional, default: true): Whether the review was successful

**Success Response (200 OK):**
```json
{
  "message": "Card marked as reviewed",
  "card": {
    ...
  },
  "streak": 3
}
```

---

### Get Due Cards

Retrieve all flashcards due for review.

**Endpoint:** `GET /api/cards/due`

**Query Parameters:**
- `category` (optional): Filter by category
- `shuffle` (optional): Set to `true` to randomize order

**Headers:**
```
Authorization: Bearer <your_access_token>
```

**Success Response (200 OK):**
```json
{
  "cards": [...],
  "total": 5
}
```

---

### Get Statistics

Retrieve statistics about the user's flashcards.

**Endpoint:** `GET /api/stats`

**Headers:**
```
Authorization: Bearer <your_access_token>
```

**Success Response (200 OK):**
```json
{
  "total_cards": 25,
  "due_for_review": 8,
  "easy_cards": 10,
  "medium_cards": 12,
  "hard_cards": 3,
  "total_reviews": 150,
  "overall_success_rate": 82.5,
  "best_streak": 15,
  "cards_with_streaks": 7
}
```

---

### Get Categories

Retrieve all unique categories for the user's flashcards.

**Endpoint:** `GET /api/categories`

**Headers:**
```
Authorization: Bearer <your_access_token>
```

**Success Response (200 OK):**
```json
{
  "categories": ["Programming", "Math", "History", "Science"]
}
```

## Error Handling

### Common Error Responses

**400 Bad Request:**
```json
{
  "error": "Description of what went wrong"
}
```

**401 Unauthorized:**
```json
{
  "msg": "Missing Authorization Header"
}
```

**403 Forbidden:**
```json
{
  "error": "Unauthorized access to this card"
}
```

**404 Not Found:**
```json
{
  "error": "Card not found"
}
```

**409 Conflict:**
```json
{
  "error": "Username already exists"
}
```

## Security Considerations

### Password Security

- Passwords are hashed using bcrypt with automatic salt generation
- Minimum password length: 6 characters
- Passwords are never stored or transmitted in plain text

### Token Security

- Use HTTPS in production to protect tokens in transit
- Store tokens securely on the client side (avoid localStorage for sensitive data)
- Access tokens expire after 1 hour for security
- Use the refresh token to obtain new access tokens

### Environment Variables

Configure these environment variables for production:

```bash
FLASK_SECRET_KEY=<your-strong-random-secret-key>
JWT_SECRET_KEY=<your-jwt-secret-key>
FLASHCARD_DATA_DIR=/path/to/secure/data/directory
```

## Examples

### Complete Authentication Flow

```bash
# 1. Register a new user
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "johndoe", "password": "securepass123"}'

# 2. Login and get tokens
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "johndoe", "password": "securepass123"}'

# Response includes access_token and refresh_token
# Save the access_token for subsequent requests

# 3. Create a flashcard
curl -X POST http://localhost:5000/api/cards \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{
    "recto": "What is REST?",
    "verso": "Representational State Transfer",
    "difficulty": "MEDIUM",
    "category": "Web Development"
  }'

# 4. Get all your cards
curl -X GET http://localhost:5000/api/cards \
  -H "Authorization: Bearer <access_token>"

# 5. Get due cards
curl -X GET http://localhost:5000/api/cards/due \
  -H "Authorization: Bearer <access_token>"

# 6. Review a card
curl -X POST http://localhost:5000/api/cards/<card_id>/review \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{"success": true}'

# 7. Get statistics
curl -X GET http://localhost:5000/api/stats \
  -H "Authorization: Bearer <access_token>"

# 8. Refresh access token when it expires
curl -X POST http://localhost:5000/api/auth/refresh \
  -H "Authorization: Bearer <refresh_token>"
```

### Python Client Example

```python
import requests

BASE_URL = "http://localhost:5000/api"

# Register
response = requests.post(f"{BASE_URL}/auth/register", json={
    "username": "johndoe",
    "password": "securepass123"
})
print(response.json())

# Login
response = requests.post(f"{BASE_URL}/auth/login", json={
    "username": "johndoe",
    "password": "securepass123"
})
tokens = response.json()
access_token = tokens["access_token"]

# Create a card
headers = {"Authorization": f"Bearer {access_token}"}
response = requests.post(f"{BASE_URL}/cards", json={
    "recto": "What is Python?",
    "verso": "A high-level programming language",
    "difficulty": "EASY",
    "category": "Programming"
}, headers=headers)
print(response.json())

# Get all cards
response = requests.get(f"{BASE_URL}/cards", headers=headers)
print(response.json())

# Get statistics
response = requests.get(f"{BASE_URL}/stats", headers=headers)
print(response.json())
```

### JavaScript/Fetch Example

```javascript
const BASE_URL = 'http://localhost:5000/api';

// Register
async function register(username, password) {
  const response = await fetch(`${BASE_URL}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  });
  return await response.json();
}

// Login
async function login(username, password) {
  const response = await fetch(`${BASE_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  });
  const data = await response.json();
  // Store token for future requests
  localStorage.setItem('access_token', data.access_token);
  return data;
}

// Create a card
async function createCard(recto, verso, difficulty, category) {
  const token = localStorage.getItem('access_token');
  const response = await fetch(`${BASE_URL}/cards`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ recto, verso, difficulty, category })
  });
  return await response.json();
}

// Get all cards
async function getCards() {
  const token = localStorage.getItem('access_token');
  const response = await fetch(`${BASE_URL}/cards`, {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  return await response.json();
}

// Usage
await register('johndoe', 'securepass123');
await login('johndoe', 'securepass123');
await createCard('What is JWT?', 'JSON Web Token', 'MEDIUM', 'Security');
const cards = await getCards();
console.log(cards);
```

## Backward Compatibility

The application maintains full backward compatibility:

- Existing flashcards without user_id continue to work
- The web UI (templates) continues to function without authentication
- CLI interface remains unchanged
- New JWT API endpoints are separate from existing web routes

This allows gradual migration to the authenticated API while maintaining existing functionality.
