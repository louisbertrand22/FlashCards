// FlashCards Application - Client-Side JavaScript

// Difficulty levels and their review intervals
const DIFFICULTY = {
    EASY: { days: 7, emoji: '🟢', color: 'success' },
    MEDIUM: { days: 3, emoji: '🟡', color: 'warning' },
    HARD: { days: 1, emoji: '🔴', color: 'danger' }
};

// Data storage using localStorage
class FlashcardManager {
    constructor() {
        this.storageKey = 'flashcards';
        this.cards = this.loadCards();
    }

    loadCards() {
        const data = localStorage.getItem(this.storageKey);
        return data ? JSON.parse(data) : [];
    }

    saveCards() {
        localStorage.setItem(this.storageKey, JSON.stringify(this.cards));
    }

    generateId() {
        return 'card_' + Date.now() + '_' + Math.random().toString(36).substring(2, 11);
    }

    addCard(front, back, difficulty) {
        const card = {
            id: this.generateId(),
            front: front,
            back: back,
            difficulty: difficulty,
            createdAt: new Date().toISOString(),
            lastReviewed: null,
            nextReview: new Date().toISOString(),
            reviewCount: 0
        };
        this.cards.push(card);
        this.saveCards();
        return card;
    }

    getAllCards() {
        return this.cards;
    }

    getCard(id) {
        return this.cards.find(card => card.id === id);
    }

    updateCardDifficulty(id, difficulty) {
        const card = this.getCard(id);
        if (card) {
            card.difficulty = difficulty;
            // Recalculate next review date based on new difficulty
            if (card.lastReviewed) {
                const lastReview = new Date(card.lastReviewed);
                const days = DIFFICULTY[difficulty].days;
                const nextReview = new Date(lastReview);
                nextReview.setDate(nextReview.getDate() + days);
                card.nextReview = nextReview.toISOString();
            }
            this.saveCards();
            return true;
        }
        return false;
    }

    deleteCard(id) {
        const index = this.cards.findIndex(card => card.id === id);
        if (index !== -1) {
            this.cards.splice(index, 1);
            this.saveCards();
            return true;
        }
        return false;
    }

    markReviewed(id) {
        const card = this.getCard(id);
        if (card) {
            const now = new Date();
            card.lastReviewed = now.toISOString();
            card.reviewCount++;
            
            // Calculate next review date
            const days = DIFFICULTY[card.difficulty].days;
            const nextReview = new Date(now);
            nextReview.setDate(nextReview.getDate() + days);
            card.nextReview = nextReview.toISOString();
            
            this.saveCards();
            return true;
        }
        return false;
    }

    getDueCards() {
        const now = new Date();
        return this.cards.filter(card => {
            const nextReview = new Date(card.nextReview);
            return nextReview <= now;
        });
    }

    getStatistics() {
        const total = this.cards.length;
        const due = this.getDueCards().length;
        const totalReviews = this.cards.reduce((sum, card) => sum + card.reviewCount, 0);
        
        const byDifficulty = {
            EASY: this.cards.filter(c => c.difficulty === 'EASY').length,
            MEDIUM: this.cards.filter(c => c.difficulty === 'MEDIUM').length,
            HARD: this.cards.filter(c => c.difficulty === 'HARD').length
        };

        const progress = total > 0 ? Math.round(((total - due) / total) * 100) : 0;

        return {
            total,
            due,
            totalReviews,
            byDifficulty,
            progress
        };
    }

    exportToJSON() {
        /**
         * Export flashcards to a JSON file for download
         */
        const dataStr = JSON.stringify(this.cards, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        const url = URL.createObjectURL(dataBlob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `flashcards-export-${new Date().toISOString().split('T')[0]}.json`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    }

    importFromJSON(jsonData) {
        /**
         * Import flashcards from JSON data
         * @param {string|object} jsonData - JSON string or parsed object
         * @returns {object} Result with success status and message
         */
        try {
            const data = typeof jsonData === 'string' ? JSON.parse(jsonData) : jsonData;
            
            if (!Array.isArray(data)) {
                return { success: false, message: 'Invalid format: Expected an array of flashcards' };
            }

            // Validate each card has required fields
            for (const card of data) {
                if (!card.front || !card.back || !card.difficulty) {
                    return { success: false, message: 'Invalid format: Cards must have front, back, and difficulty' };
                }
            }

            // Replace current cards with imported ones
            this.cards = data;
            this.saveCards();
            
            return { success: true, message: `Successfully imported ${data.length} flashcard(s)` };
        } catch (error) {
            return { success: false, message: `Import failed: ${error.message}` };
        }
    }
}

// Global manager instance
const manager = new FlashcardManager();

// View management
function showView(viewName) {
    // Hide all views
    document.querySelectorAll('.view').forEach(view => {
        view.classList.add('hidden');
    });

    // Show selected view
    const viewMap = {
        'dashboard': 'dashboard-view',
        'all-cards': 'all-cards-view',
        'create-card': 'create-card-view',
        'study': 'study-view'
    };

    const viewId = viewMap[viewName];
    if (viewId) {
        document.getElementById(viewId).classList.remove('hidden');
    }

    // Load content for the view
    switch(viewName) {
        case 'dashboard':
            loadDashboard();
            break;
        case 'all-cards':
            loadAllCards();
            break;
        case 'study':
            loadStudyMode();
            break;
    }

    // Close mobile menu
    const navbarCollapse = document.getElementById('navbarNav');
    if (navbarCollapse.classList.contains('show')) {
        const bsCollapse = new bootstrap.Collapse(navbarCollapse);
        bsCollapse.hide();
    }
}

// Alert management
function showAlert(message, type = 'success') {
    const alertContainer = document.getElementById('alert-container');
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.role = 'alert';
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    alertContainer.appendChild(alert);

    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        alert.remove();
    }, 5000);
}

// Dashboard functions
function loadDashboard() {
    const stats = manager.getStatistics();

    // Update statistics
    document.getElementById('stat-total-cards').textContent = stats.total;
    document.getElementById('stat-due-cards').textContent = stats.due;
    document.getElementById('stat-total-reviews').textContent = stats.totalReviews;
    document.getElementById('stat-progress').textContent = stats.progress + '%';
    
    document.getElementById('stat-easy-cards').textContent = stats.byDifficulty.EASY;
    document.getElementById('stat-medium-cards').textContent = stats.byDifficulty.MEDIUM;
    document.getElementById('stat-hard-cards').textContent = stats.byDifficulty.HARD;

    // Update quick actions
    const quickActions = document.getElementById('quick-actions');
    if (stats.due > 0) {
        quickActions.innerHTML = `
            <button class="btn btn-warning btn-lg" onclick="showView('study')">
                🎯 Study Now (${stats.due} cards due)
            </button>
            <button class="btn btn-primary btn-lg" onclick="showView('create-card')">
                📝 Create New Card
            </button>
            <button class="btn btn-secondary btn-lg" onclick="showView('all-cards')">
                📚 View All Cards
            </button>
        `;
    } else {
        quickActions.innerHTML = `
            <button class="btn btn-success btn-lg" disabled>
                ✅ All caught up!
            </button>
            <button class="btn btn-primary btn-lg" onclick="showView('create-card')">
                📝 Create New Card
            </button>
            <button class="btn btn-secondary btn-lg" onclick="showView('all-cards')">
                📚 View All Cards
            </button>
        `;
    }

    // Show/hide welcome message
    const welcomeMsg = document.getElementById('welcome-message');
    if (stats.total === 0) {
        welcomeMsg.style.display = 'block';
    } else {
        welcomeMsg.style.display = 'none';
    }
}

// All cards functions
function loadAllCards() {
    const cards = manager.getAllCards();
    const container = document.getElementById('cards-container');

    if (cards.length === 0) {
        container.innerHTML = `
            <div class="col-md-12">
                <div class="alert alert-info text-center">
                    <h4>No flashcards yet</h4>
                    <p class="mb-0">
                        <a href="#" onclick="showView('create-card')" class="alert-link">Create your first card</a> 
                        to get started!
                    </p>
                </div>
            </div>
        `;
        return;
    }

    container.innerHTML = cards.map(card => {
        const difficulty = DIFFICULTY[card.difficulty];
        const isDue = new Date(card.nextReview) <= new Date();
        const nextReviewDate = formatDate(card.nextReview);
        const lastReviewDate = card.lastReviewed ? formatDate(card.lastReviewed) : 'Never';

        return `
            <div class="col-md-6 mb-4">
                <div class="card flashcard ${isDue ? 'border-warning' : ''}">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <span class="badge bg-${difficulty.color}">
                            ${difficulty.emoji} ${card.difficulty}
                        </span>
                        <small class="text-muted">ID: ${card.id.slice(-8)}</small>
                    </div>
                    <div class="card-body">
                        <h5 class="card-title">📝 Front:</h5>
                        <p class="card-text">${escapeHtml(card.front)}</p>
                        <h5 class="card-title mt-3">💡 Back:</h5>
                        <p class="card-text">${escapeHtml(card.back)}</p>
                        
                        <div class="card-meta mt-3">
                            <small>
                                <strong>Next Review:</strong> ${nextReviewDate}<br>
                                <strong>Last Reviewed:</strong> ${lastReviewDate}<br>
                                <strong>Review Count:</strong> ${card.reviewCount}
                            </small>
                        </div>
                    </div>
                    <div class="card-footer d-flex gap-2">
                        <button class="btn btn-sm btn-primary" onclick="editCard('${card.id}')">
                            ✏️ Edit
                        </button>
                        <button class="btn btn-sm btn-danger" onclick="confirmDelete('${card.id}')">
                            🗑️ Delete
                        </button>
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

// Create card functions
document.getElementById('create-card-form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const front = document.getElementById('card-front').value.trim();
    const back = document.getElementById('card-back').value.trim();
    const difficulty = document.getElementById('card-difficulty').value;

    if (!front || !back) {
        showAlert('Both front and back sides are required!', 'danger');
        return;
    }

    manager.addCard(front, back, difficulty);
    showAlert('Flashcard created successfully!', 'success');
    
    // Reset form
    this.reset();
    
    // Go back to all cards view
    showView('all-cards');
});

// Study mode functions
let currentStudyIndex = 0;
let studyCards = [];
let isAnswerRevealed = false;

function loadStudyMode() {
    studyCards = manager.getDueCards();
    currentStudyIndex = 0;
    isAnswerRevealed = false;

    const container = document.getElementById('study-container');

    if (studyCards.length === 0) {
        container.innerHTML = `
            <div class="row">
                <div class="col-md-12">
                    <div class="alert alert-success text-center">
                        <h3>✅ All Caught Up!</h3>
                        <p class="mb-0">You don't have any flashcards due for review right now.</p>
                        <p class="mt-2 mb-0">
                            <a href="#" onclick="showView('create-card')" class="alert-link">Create more cards</a> 
                            or check back later!
                        </p>
                    </div>
                </div>
            </div>
        `;
        return;
    }

    showStudyCard();
}

function showStudyCard() {
    if (currentStudyIndex >= studyCards.length) {
        // Study session complete
        document.getElementById('study-container').innerHTML = `
            <div class="row">
                <div class="col-md-12">
                    <div class="alert alert-success text-center">
                        <h3>🎉 Study Session Complete!</h3>
                        <p>You've reviewed ${studyCards.length} flashcard${studyCards.length > 1 ? 's' : ''}!</p>
                        <button class="btn btn-primary" onclick="showView('dashboard')">
                            Back to Dashboard
                        </button>
                    </div>
                </div>
            </div>
        `;
        return;
    }

    const card = studyCards[currentStudyIndex];
    const difficulty = DIFFICULTY[card.difficulty];
    const progress = ((currentStudyIndex + 1) / studyCards.length * 100).toFixed(0);

    document.getElementById('study-container').innerHTML = `
        <div class="row">
            <div class="col-md-8 offset-md-2">
                <div class="mb-3">
                    <div class="d-flex justify-content-between align-items-center mb-2">
                        <span>Progress: ${currentStudyIndex + 1} / ${studyCards.length}</span>
                        <span class="badge bg-${difficulty.color}">${difficulty.emoji} ${card.difficulty}</span>
                    </div>
                    <div class="progress">
                        <div class="progress-bar bg-info" style="width: ${progress}%"></div>
                    </div>
                </div>

                <div class="card study-card">
                    <div class="card-body">
                        <h5 class="card-title mb-3">Question:</h5>
                        <div class="flashcard-content">
                            <p class="lead">${escapeHtml(card.front)}</p>
                        </div>

                        <div id="answer-section" class="mt-4 ${isAnswerRevealed ? '' : 'hidden'}">
                            <h5 class="card-title mb-3">Answer:</h5>
                            <div class="flashcard-content">
                                <p class="lead">${escapeHtml(card.back)}</p>
                            </div>
                        </div>

                        <div class="d-grid gap-2 mt-4">
                            <button id="reveal-btn" class="btn btn-primary btn-lg" onclick="revealAnswer()">
                                👁️ Reveal Answer
                            </button>
                            <div id="review-buttons" class="hidden">
                                <button class="btn btn-success btn-lg w-100 mb-2" onclick="markReviewedAndNext('${card.id}')">
                                    ✅ Mark as Reviewed
                                </button>
                                <button class="btn btn-secondary" onclick="nextCard()">
                                    ⏭️ Skip
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;

    isAnswerRevealed = false;
}

function revealAnswer() {
    document.getElementById('answer-section').classList.remove('hidden');
    document.getElementById('reveal-btn').classList.add('hidden');
    document.getElementById('review-buttons').classList.remove('hidden');
    isAnswerRevealed = true;
}

function markReviewedAndNext(cardId) {
    manager.markReviewed(cardId);
    currentStudyIndex++;
    showStudyCard();
}

function nextCard() {
    currentStudyIndex++;
    showStudyCard();
}

// Edit card functions
function editCard(cardId) {
    const card = manager.getCard(cardId);
    if (!card) return;

    document.getElementById('edit-card-id').value = cardId;
    document.getElementById('edit-difficulty').value = card.difficulty;

    const modal = new bootstrap.Modal(document.getElementById('editModal'));
    modal.show();
}

function saveCardEdit() {
    const cardId = document.getElementById('edit-card-id').value;
    const difficulty = document.getElementById('edit-difficulty').value;

    if (manager.updateCardDifficulty(cardId, difficulty)) {
        showAlert('Card difficulty updated successfully!', 'success');
        loadAllCards();
        
        const modal = bootstrap.Modal.getInstance(document.getElementById('editModal'));
        modal.hide();
    } else {
        showAlert('Failed to update card!', 'danger');
    }
}

// Delete card functions
function confirmDelete(cardId) {
    if (confirm('Are you sure you want to delete this flashcard? This action cannot be undone.')) {
        if (manager.deleteCard(cardId)) {
            showAlert('Flashcard deleted successfully!', 'success');
            loadAllCards();
        } else {
            showAlert('Failed to delete card!', 'danger');
        }
    }
}

// Utility functions
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatDate(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = date - now;
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays < 0) {
        return 'Overdue';
    } else if (diffDays === 0) {
        return 'Today';
    } else if (diffDays === 1) {
        return 'Tomorrow';
    } else {
        return date.toLocaleDateString('en-US', { 
            year: 'numeric', 
            month: 'short', 
            day: 'numeric' 
        });
    }
}

// Import/Export functions
function exportFlashcards() {
    try {
        manager.exportToJSON();
        showAlert('Flashcards exported successfully!', 'success');
    } catch (error) {
        showAlert('Export failed: ' + error.message, 'danger');
    }
}

function triggerImportFile() {
    document.getElementById('import-file-input').click();
}

function handleImportFile(event) {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function(e) {
        try {
            const result = manager.importFromJSON(e.target.result);
            if (result.success) {
                showAlert(result.message, 'success');
                // Refresh current view
                const currentView = document.querySelector('.view:not(.hidden)').id;
                if (currentView === 'dashboard-view') {
                    loadDashboard();
                } else if (currentView === 'all-cards-view') {
                    loadAllCards();
                }
            } else {
                showAlert(result.message, 'danger');
            }
        } catch (error) {
            showAlert('Import failed: ' + error.message, 'danger');
        }
    };
    reader.readAsText(file);
    
    // Reset file input so the same file can be selected again
    event.target.value = '';
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    showView('dashboard');
});
