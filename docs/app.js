// FlashCards Application - Client-Side JavaScript

// French translations
const FR = {
    'Both front and back sides are required!': 'Les côtés recto et verso sont obligatoires !',
    'Flashcard created successfully!': 'Carte mémoire créée avec succès !',
    'Card difficulty updated successfully!': 'Difficulté de la carte mise à jour avec succès !',
    'Failed to update card!': 'Échec de la mise à jour de la carte !',
    'Flashcard deleted successfully!': 'Carte mémoire supprimée avec succès !',
    'Failed to delete card!': 'Échec de la suppression de la carte !',
    'Are you sure you want to delete this card?': 'Êtes-vous sûr de vouloir supprimer cette carte ?',
    'Front:': 'Recto :',
    'Back:': 'Verso :',
    'Category:': 'Catégorie :',
    'Reviews:': 'Révisions :',
    'Last reviewed:': 'Dernière révision :',
    'Next review:': 'Prochaine révision :',
    'Never': 'Jamais',
    'Edit Difficulty': 'Modifier la difficulté',
    'Delete': 'Supprimer',
    'Study Now': 'Réviser maintenant',
    'cards due': 'cartes à réviser',
    'All caught up!': 'Tout est à jour !',
    'Create New Card': 'Créer une nouvelle carte',
    'View All Cards': 'Voir toutes les cartes',
    'No cards available': 'Aucune carte disponible',
    'You don\'t have any flashcards yet.': 'Vous n\'avez pas encore de cartes mémoire.',
    'Create your first card to get started!': 'Créez votre première carte pour commencer !',
    'All Categories': 'Toutes les catégories',
    'Filter': 'Filtrer',
    'card(s) due for review': 'carte(s) à réviser',
    'in category': 'dans la catégorie',
    'Reveal Answer': 'Révéler la réponse',
    'I Remembered': 'Je me souviens',
    'I Didn\'t Remember': 'Je ne me souviens pas',
    'All caught up! No cards due for review.': 'Tout est à jour ! Aucune carte à réviser.',
    'Return to Dashboard': 'Retour au tableau de bord',
    'Card': 'Carte',
    'of': 'sur',
    'Due for Review': 'À réviser',
    'Not Due': 'Pas encore',
    'Easy': 'Facile',
    'Medium': 'Moyen',
    'Hard': 'Difficile',
    'Great job!': 'Excellent travail !',
    'You\'ve completed all due flashcards for now.': 'Vous avez terminé toutes les cartes à réviser pour le moment.',
    'Cards are presented in random order. Click on a card to reveal the answer, then mark if you remembered it.': 'Les cartes sont présentées dans un ordre aléatoire. Cliquez sur une carte pour révéler la réponse, puis indiquez si vous vous en souvenez.',
    'You don\'t have any flashcards due for review right now.': 'Vous n\'avez aucune carte à réviser pour le moment.'
};

function _(text) {
    return FR[text] || text;
}

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

    shuffleArray(array) {
        // Fisher-Yates shuffle algorithm
        const shuffled = [...array]; // Create a copy to avoid mutating the original
        for (let i = shuffled.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
        }
        return shuffled;
    }

    addCard(front, back, difficulty, category = null) {
        const card = {
            id: this.generateId(),
            front: front,
            back: back,
            difficulty: difficulty,
            category: category,
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

    getDueCards(shuffle = false) {
        const now = new Date();
        const dueCards = this.cards.filter(card => {
            const nextReview = new Date(card.nextReview);
            return nextReview <= now;
        });
        
        if (shuffle) {
            return this.shuffleArray(dueCards);
        }
        
        return dueCards;
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

    getCardsByCategory(category) {
        return this.cards.filter(card => card.category === category);
    }

    getAllCategories() {
        const categories = new Set();
        this.cards.forEach(card => {
            if (card.category) {
                categories.add(card.category);
            }
        });
        return Array.from(categories).sort();
    }
}

// Global manager instance
const manager = new FlashcardManager();

// Utility function to escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

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
                🎯 ${_('Study Now')} (${stats.due} ${_('cards due')})
            </button>
            <button class="btn btn-primary btn-lg" onclick="showView('create-card')">
                📝 ${_('Create New Card')}
            </button>
            <button class="btn btn-secondary btn-lg" onclick="showView('all-cards')">
                📚 ${_('View All Cards')}
            </button>
        `;
    } else {
        quickActions.innerHTML = `
            <button class="btn btn-success btn-lg" disabled>
                ✅ ${_('All caught up!')}
            </button>
            <button class="btn btn-primary btn-lg" onclick="showView('create-card')">
                📝 ${_('Create New Card')}
            </button>
            <button class="btn btn-secondary btn-lg" onclick="showView('all-cards')">
                📚 ${_('View All Cards')}
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
let currentCategoryFilter = null;

function loadAllCards(categoryFilter = null) {
    currentCategoryFilter = categoryFilter;
    const cards = categoryFilter ? manager.getCardsByCategory(categoryFilter) : manager.getAllCards();
    const categories = manager.getAllCategories();
    const container = document.getElementById('cards-container');
    const filterContainer = document.getElementById('category-filter-container');

    // Render category filter
    if (categories.length > 0) {
        filterContainer.innerHTML = `
            <div class="mb-3">
                <label class="form-label">Filter by Category:</label>
                <div class="btn-group" role="group">
                    <button class="btn btn-sm ${!categoryFilter ? 'btn-primary' : 'btn-outline-primary'}" onclick="loadAllCards(null)">
                        All
                    </button>
                    ${categories.map(cat => `
                        <button class="btn btn-sm ${categoryFilter === cat ? 'btn-primary' : 'btn-outline-primary'}" onclick="loadAllCards('${cat}')">
                            ${escapeHtml(cat)}
                        </button>
                    `).join('')}
                </div>
            </div>
        `;
    } else {
        filterContainer.innerHTML = '';
    }

    if (cards.length === 0) {
        container.innerHTML = `
            <div class="col-md-12">
                <div class="alert alert-info text-center">
                    <h4>No flashcards${categoryFilter ? ' in this category' : ''} yet</h4>
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
        const lastReviewDate = card.lastReviewed ? formatDate(card.lastReviewed) : _('Never');

        return `
            <div class="col-md-6 mb-4">
                <div class="card flashcard ${isDue ? 'border-warning' : ''}">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <div>
                            <span class="badge bg-${difficulty.color}">
                                ${difficulty.emoji} ${card.difficulty}
                            </span>
                            ${card.category ? `<span class="badge bg-info">📁 ${escapeHtml(card.category)}</span>` : ''}
                        </div>
                        <small class="text-muted">ID: ${card.id.slice(-8)}</small>
                    </div>
                    <div class="card-body">
                        <h5 class="card-title">📝 ${_('Front:')}</h5>
                        <p class="card-text">${escapeHtml(card.front)}</p>
                        <h5 class="card-title mt-3">💡 ${_('Back:')}</h5>
                        <p class="card-text">${escapeHtml(card.back)}</p>
                        
                        <div class="card-meta mt-3">
                            <small>
                                <strong>${_('Next review:')}</strong> ${nextReviewDate}<br>
                                <strong>${_('Last reviewed:')}</strong> ${lastReviewDate}<br>
                                <strong>${_('Reviews:')}</strong> ${card.reviewCount}
                            </small>
                        </div>
                    </div>
                    <div class="card-footer d-flex gap-2">
                        <button class="btn btn-sm btn-primary" onclick="editCard('${card.id}')">
                            ✏️ ${_('Edit Difficulty')}
                        </button>
                        <button class="btn btn-sm btn-danger" onclick="confirmDelete('${card.id}')">
                            🗑️ ${_('Delete')}
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
    const category = document.getElementById('card-category').value.trim() || null;

    if (!front || !back) {
        showAlert(_('Both front and back sides are required!'), 'danger');
        return;
    }

    manager.addCard(front, back, difficulty, category);
    showAlert(_('Flashcard created successfully!'), 'success');
    
    // Reset form
    this.reset();
    
    // Update category datalist
    updateCategoryDatalist();
    
    // Go back to all cards view
    showView('all-cards');
});

// Study mode functions
let currentStudyIndex = 0;
let studyCards = [];
let isAnswerRevealed = false;
let selectedStudyCategory = null;

function loadStudyMode() {
    const categories = manager.getAllCategories();
    const categoryFilterContainer = document.getElementById('study-category-filter');
    
    // Show category filter if there are categories
    if (categories.length > 0) {
        // Count due cards per category
        const allDueCards = manager.getDueCards(false);
        const categoryCounts = {};
        allDueCards.forEach(card => {
            if (card.category) {
                categoryCounts[card.category] = (categoryCounts[card.category] || 0) + 1;
            }
        });
        
        categoryFilterContainer.innerHTML = `
            <div class="col-md-8">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">📁 Select Category</h5>
                        <div class="row g-3">
                            <div class="col-auto">
                                <select class="form-select" id="study-category-select" onchange="filterStudyByCategory()">
                                    <option value="">All Categories</option>
                                    ${categories.map(cat => `
                                        <option value="${cat}" ${selectedStudyCategory === cat ? 'selected' : ''}>
                                            ${cat} (${categoryCounts[cat] || 0} due)
                                        </option>
                                    `).join('')}
                                </select>
                            </div>
                            ${selectedStudyCategory ? `
                                <div class="col-auto">
                                    <button class="btn btn-secondary" onclick="clearStudyCategoryFilter()">Clear Filter</button>
                                </div>
                            ` : ''}
                        </div>
                    </div>
                </div>
            </div>
        `;
    } else {
        categoryFilterContainer.innerHTML = '';
    }
    
    // Get cards based on selected category
    const allDueCards = manager.getDueCards(false);
    if (selectedStudyCategory) {
        const filteredCards = allDueCards.filter(card => card.category === selectedStudyCategory);
        studyCards = manager.shuffleArray(filteredCards);
    } else {
        studyCards = manager.getDueCards(true); // Enable shuffle
    }
    
    currentStudyIndex = 0;
    isAnswerRevealed = false;

    const container = document.getElementById('study-container');

    if (studyCards.length === 0) {
        const message = selectedStudyCategory 
            ? `${_('You don\'t have any flashcards due for review right now.')}`
            : _('You don\'t have any flashcards due for review right now.');
        
        container.innerHTML = `
            <div class="row">
                <div class="col-md-12">
                    <div class="alert alert-success text-center">
                        <h3>✅ ${_('All caught up!')}</h3>
                        <p class="mb-0">${message}</p>
                        <p class="mt-2 mb-0">
                            <a href="#" onclick="showView('create-card')" class="alert-link">${_('Create New Card')}</a>
                        </p>
                    </div>
                </div>
            </div>
        `;
        return;
    }

    showStudyCard();
}

function filterStudyByCategory() {
    const select = document.getElementById('study-category-select');
    selectedStudyCategory = select.value || null;
    loadStudyMode();
}

function clearStudyCategoryFilter() {
    selectedStudyCategory = null;
    loadStudyMode();
}

function showStudyCard() {
    if (currentStudyIndex >= studyCards.length) {
        // Study session complete
        document.getElementById('study-container').innerHTML = `
            <div class="row">
                <div class="col-md-12">
                    <div class="alert alert-success text-center">
                        <h3>🎉 ${_('Great job!')}</h3>
                        <p>${_('You\'ve completed all due flashcards for now.')}</p>
                        <button class="btn btn-primary" onclick="showView('dashboard')">
                            ${_('Return to Dashboard')}
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
                <div class="alert alert-info text-center mb-4">
                    🔀 ${_('Cards are presented in random order. Click on a card to reveal the answer, then mark if you remembered it.')}
                </div>
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
                                👁️ ${_('Reveal Answer')}
                            </button>
                            <div id="review-buttons" class="hidden">
                                <button class="btn btn-success btn-lg w-100 mb-2" onclick="markReviewedAndNext('${card.id}')">
                                    ✅ ${_('I Remembered')}
                                </button>
                                <button class="btn btn-secondary" onclick="nextCard()">
                                    ⏭️ ${_('I Didn\'t Remember')}
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
        showAlert(_('Card difficulty updated successfully!'), 'success');
        loadAllCards(currentCategoryFilter);
        
        const modal = bootstrap.Modal.getInstance(document.getElementById('editModal'));
        modal.hide();
    } else {
        showAlert(_('Failed to update card!'), 'danger');
    }
}

// Delete card functions
function confirmDelete(cardId) {
    if (confirm(_('Are you sure you want to delete this card?'))) {
        if (manager.deleteCard(cardId)) {
            showAlert(_('Flashcard deleted successfully!'), 'success');
            loadAllCards(currentCategoryFilter);
        } else {
            showAlert(_('Failed to delete card!'), 'danger');
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

function updateCategoryDatalist() {
    const categories = manager.getAllCategories();
    const datalist = document.getElementById('category-suggestions');
    datalist.innerHTML = categories.map(cat => `<option value="${escapeHtml(cat)}">`).join('');
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    updateCategoryDatalist();
    showView('dashboard');
});
