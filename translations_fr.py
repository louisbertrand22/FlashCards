"""
French translations for the CLI interface.
"""

# French translations dictionary
FR = {
    # Main menu
    "FLASHCARD APPLICATION": "APPLICATION FLASHCARDS",
    "Create a new flashcard": "Créer une nouvelle carte mémoire",
    "View all flashcards": "Voir toutes les cartes mémoire",
    "Study flashcards (review due cards)": "Réviser les cartes (révision des cartes dues)",
    "View statistics": "Voir les statistiques",
    "Update card difficulty": "Modifier la difficulté d'une carte",
    "Delete a flashcard": "Supprimer une carte mémoire",
    "Exit": "Quitter",
    
    # Create flashcard
    "Create New Flashcard": "Créer une nouvelle carte mémoire",
    "Enter the front side (recto)": "Entrez le côté recto (question)",
    "Front side cannot be empty!": "Le côté recto ne peut pas être vide !",
    "Enter the back side (verso)": "Entrez le côté verso (réponse)",
    "Back side cannot be empty!": "Le côté verso ne peut pas être vide !",
    "Existing categories:": "Catégories existantes :",
    "Enter category (optional, press Enter to skip)": "Entrez la catégorie (optionnel, appuyez sur Entrée pour ignorer)",
    "Select difficulty level:": "Sélectionnez le niveau de difficulté :",
    "Easy (review every 7 days)": "Facile (révision tous les 7 jours)",
    "Medium (review every 3 days)": "Moyen (révision tous les 3 jours)",
    "Hard (review every 1 day)": "Difficile (révision quotidienne)",
    "Enter choice (1-3)": "Entrez votre choix (1-3)",
    "Flashcard created successfully!": "Carte mémoire créée avec succès !",
    "ID:": "ID :",
    "Category:": "Catégorie :",
    "Difficulty:": "Difficulté :",
    
    # View all flashcards
    "All Flashcards": "Toutes les cartes mémoire",
    "total": "total",
    "No flashcards found. Create one first!": "Aucune carte mémoire trouvée. Créez-en une d'abord !",
    "Due": "À réviser",
    "Not due": "Pas encore",
    "Recto:": "Recto :",
    "Verso:": "Verso :",
    "Reviews:": "Révisions :",
    "success": "succès",
    
    # Study flashcards
    "Study Session": "Session de révision",
    "cards due": "cartes à réviser",
    "Category Selection": "Sélection de catégorie",
    "Available categories:": "Catégories disponibles :",
    "All categories (review all due cards)": "Toutes les catégories (réviser toutes les cartes dues)",
    "due": "à réviser",
    "No flashcards due for review right now!": "Aucune carte à réviser pour le moment !",
    "No flashcards found!": "Aucune carte mémoire trouvée !",
    "Select category": "Sélectionner la catégorie",
    "Studying category:": "Révision de la catégorie :",
    "Cards will be presented in random order": "Les cartes seront présentées dans un ordre aléatoire",
    "No flashcards due for review in category": "Aucune carte à réviser dans la catégorie",
    "Card": "Carte",
    "Front:": "Recto :",
    "Press Enter to reveal the back side...": "Appuyez sur Entrée pour révéler le verso...",
    "Back:": "Verso :",
    "Did you remember?": "Vous en souvenez-vous ?",
    "Marked as reviewed successfully!": "Marquée comme révisée avec succès !",
    "Success streak:": "Série de succès :",
    "Marked as review needed. This card will be reviewed sooner.": "Marquée comme nécessitant une révision. Cette carte sera révisée plus tôt.",
    "Continue to next card?": "Continuer vers la carte suivante ?",
    "Study session complete!": "Session de révision terminée !",
    
    # View statistics
    "Flashcard Statistics": "Statistiques des cartes mémoire",
    "Total flashcards": "Total de cartes mémoire",
    "Due for review": "À réviser",
    "Total reviews completed": "Total de révisions effectuées",
    "Overall success rate": "Taux de réussite global",
    "Best success streak": "Meilleure série de succès",
    "Cards with active streaks": "Cartes avec séries actives",
    "By difficulty:": "Par difficulté :",
    "Easy": "Facile",
    "Medium": "Moyen",
    "Hard": "Difficile",
    
    # Update difficulty
    "Enter the card ID to update": "Entrez l'ID de la carte à modifier",
    "Card not found!": "Carte non trouvée !",
    "Current difficulty:": "Difficulté actuelle :",
    "Select new difficulty level:": "Sélectionnez le nouveau niveau de difficulté :",
    "Difficulty updated to": "Difficulté mise à jour à",
    "Invalid choice!": "Choix invalide !",
    
    # Delete flashcard
    "Enter the card ID to delete": "Entrez l'ID de la carte à supprimer",
    "Are you sure you want to delete this card?": "Êtes-vous sûr de vouloir supprimer cette carte ?",
    "Flashcard deleted successfully!": "Carte mémoire supprimée avec succès !",
    "Deletion cancelled.": "Suppression annulée.",
    
    # Main loop
    "Welcome to the Flashcard Application!": "Bienvenue dans l'application FlashCards !",
    "Enter your choice": "Entrez votre choix",
    "Thank you for using Flashcard Application. Goodbye!": "Merci d'avoir utilisé l'application FlashCards. Au revoir !",
    "Exiting... Goodbye!": "Fermeture... Au revoir !",
    "Invalid choice! Please enter a number between 1 and 7.": "Choix invalide ! Veuillez entrer un nombre entre 1 et 7.",
    "An error occurred:": "Une erreur s'est produite :",
    "Please try again.": "Veuillez réessayer.",
}

def _(text):
    """Get French translation of text."""
    return FR.get(text, text)
