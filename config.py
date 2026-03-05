"""
Configuration globale de l'application FabIAna.
"""

# Modèle IA utilisé
MODEL = "llama3:8b"

# Base de données SQLite
DATABASE_PATH = "campusfab.db"

# Ancien fichier JSON (archivé)
CONTACTS_FILE = "contacts.json"

# Configuration de l'IA
AI_CONFIG = {
    "temperature": 0.7,
    "format": "json"
}
