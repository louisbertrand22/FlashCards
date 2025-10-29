# Quick Start Guide: JWT Authentication

This guide will help you get started with the JWT authentication API in the FlashCards application.

## Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

## Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the Flask application:**
   ```bash
   python app.py
   ```
   
   The server will start on `http://localhost:5000`

## First Steps

### 1. Register a New User

```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "myusername",
    "password": "mypassword123"
  }'
```

**Response:**
```json
{
  "message": "User registered successfully",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "username": "myusername"
}
```

### 2. Login and Get Tokens

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "myusername",
    "password": "mypassword123"
  }'
```

**Response:**
```json
{
  "message": "Login successful",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "username": "myusername"
}
```

**Important:** Save the `access_token` - you'll need it for all subsequent requests!

### 3. Create Your First Flashcard

```bash
curl -X POST http://localhost:5000/api/cards \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE" \
  -d '{
    "recto": "What is JWT?",
    "verso": "JSON Web Token - a standard for securely transmitting information",
    "difficulty": "MEDIUM",
    "category": "Authentication"
  }'
```

**Response:**
```json
{
  "message": "Flashcard created successfully",
  "card": {
    "card_id": "card_abc123",
    "recto": "What is JWT?",
    "verso": "JSON Web Token - a standard for securely transmitting information",
    "difficulty": "MEDIUM",
    "category": "Authentication",
    ...
  }
}
```

### 4. View Your Flashcards

```bash
curl -X GET http://localhost:5000/api/cards \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

### 5. Study Due Cards

```bash
curl -X GET http://localhost:5000/api/cards/due \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

### 6. Review a Card

After studying, mark a card as reviewed:

```bash
curl -X POST http://localhost:5000/api/cards/CARD_ID/review \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE" \
  -d '{
    "success": true
  }'
```

### 7. View Your Statistics

```bash
curl -X GET http://localhost:5000/api/stats \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

## Python Example

Here's a complete Python example:

```python
import requests

BASE_URL = "http://localhost:5000/api"

# 1. Register
response = requests.post(f"{BASE_URL}/auth/register", json={
    "username": "pythonuser",
    "password": "python123"
})
print("Registration:", response.json())

# 2. Login
response = requests.post(f"{BASE_URL}/auth/login", json={
    "username": "pythonuser",
    "password": "python123"
})
tokens = response.json()
access_token = tokens["access_token"]
print("Login successful!")

# 3. Create a card
headers = {"Authorization": f"Bearer {access_token}"}
response = requests.post(f"{BASE_URL}/cards", headers=headers, json={
    "recto": "What is Python?",
    "verso": "A high-level programming language",
    "difficulty": "EASY",
    "category": "Programming"
})
card = response.json()["card"]
print(f"Card created: {card['card_id']}")

# 4. Get all cards
response = requests.get(f"{BASE_URL}/cards", headers=headers)
cards = response.json()["cards"]
print(f"Total cards: {len(cards)}")

# 5. Get statistics
response = requests.get(f"{BASE_URL}/stats", headers=headers)
stats = response.json()
print(f"Statistics: {stats}")
```

## JavaScript/Node.js Example

```javascript
const axios = require('axios');

const BASE_URL = 'http://localhost:5000/api';

async function main() {
  try {
    // 1. Register
    await axios.post(`${BASE_URL}/auth/register`, {
      username: 'jsuser',
      password: 'javascript123'
    });
    console.log('Registration successful!');

    // 2. Login
    const loginResponse = await axios.post(`${BASE_URL}/auth/login`, {
      username: 'jsuser',
      password: 'javascript123'
    });
    const accessToken = loginResponse.data.access_token;
    console.log('Login successful!');

    // 3. Create a card
    const headers = { Authorization: `Bearer ${accessToken}` };
    const cardResponse = await axios.post(`${BASE_URL}/cards`, {
      recto: 'What is Node.js?',
      verso: 'A JavaScript runtime built on Chrome\'s V8 engine',
      difficulty: 'MEDIUM',
      category: 'Programming'
    }, { headers });
    console.log('Card created:', cardResponse.data.card.card_id);

    // 4. Get all cards
    const cardsResponse = await axios.get(`${BASE_URL}/cards`, { headers });
    console.log('Total cards:', cardsResponse.data.total);

    // 5. Get statistics
    const statsResponse = await axios.get(`${BASE_URL}/stats`, { headers });
    console.log('Statistics:', statsResponse.data);

  } catch (error) {
    console.error('Error:', error.response?.data || error.message);
  }
}

main();
```

## Common Tasks

### Update Card Difficulty

```bash
curl -X PUT http://localhost:5000/api/cards/CARD_ID \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE" \
  -d '{"difficulty": "HARD"}'
```

### Delete a Card

```bash
curl -X DELETE http://localhost:5000/api/cards/CARD_ID \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

### Filter Cards by Category

```bash
curl -X GET "http://localhost:5000/api/cards?category=Programming" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

### Get All Categories

```bash
curl -X GET http://localhost:5000/api/categories \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

### Refresh Your Access Token

When your access token expires (after 1 hour), use the refresh token:

```bash
curl -X POST http://localhost:5000/api/auth/refresh \
  -H "Authorization: Bearer YOUR_REFRESH_TOKEN_HERE"
```

## Difficulty Levels

- **EASY**: Review every 7 days
- **MEDIUM**: Review every 3 days  
- **HARD**: Review daily

The system uses spaced repetition to help you learn effectively!

## Production Deployment

For production, set these environment variables:

```bash
export FLASK_SECRET_KEY="your-strong-random-secret-key"
export JWT_SECRET_KEY="your-jwt-secret-key"
export FLASHCARD_DATA_DIR="/secure/path/to/data"
```

Never use the default keys in production!

## Troubleshooting

### "Invalid or expired token"
Your access token has expired. Use the refresh endpoint to get a new one.

### "Unauthorized access to this card"
You're trying to access a card that belongs to another user.

### "Username already exists"
Choose a different username during registration.

## Need Help?

- **Full API Documentation**: See [JWT_API_DOCUMENTATION.md](JWT_API_DOCUMENTATION.md)
- **Repository**: [https://github.com/louisbertrand22/FlashCards](https://github.com/louisbertrand22/FlashCards)
- **Issues**: Create an issue on GitHub

## Next Steps

1. Create more flashcards with different difficulty levels
2. Study cards that are due for review
3. Track your progress with statistics
4. Organize cards into categories
5. Build a client application using the API

Happy learning! 📚
