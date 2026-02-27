import sqlite3
import json
import os

# Nom du fichier de base de données
DB_PATH = "data/campusfab.db"

def initialiser_bdd():
    """Crée le dossier data et la table si ils n'existent pas."""
    # Créer le dossier data s'il n'existe pas
    if not os.path.exists('data'):
        os.makedirs('data')
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Création de la table avec tous les champs de ton prompt
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS membres (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            etudes TEXT,
            metiers TEXT,        -- Liste stockée en JSON
            passions TEXT,       -- Liste stockée en JSON
            projets TEXT,        -- Liste stockée en JSON
            laboratoire TEXT,
            competences TEXT,    -- Liste stockée en JSON
            email TEXT,
            numero TEXT,
            autres_infos TEXT,
            date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def sauvegarder_membre(fiche):
    """Prend le dictionnaire extrait par l'IA et l'enregistre en BDD."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # On transforme les listes Python en chaînes JSON pour SQLite
    cursor.execute('''
        INSERT INTO membres (
            nom, etudes, metiers, passions, projets, 
            laboratoire, competences, email, numero, autres_infos
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        fiche.get('nom'),
        fiche.get('etudes'),
        json.dumps(fiche.get('métiers', [])), # Note le 'é' de métiers
        json.dumps(fiche.get('passions', [])),
        json.dumps(fiche.get('projets', [])),
        fiche.get('laboratoire'),
        json.dumps(fiche.get('competences', [])),
        fiche.get('email'),
        fiche.get('numero'),
        fiche.get('autres_infos')
    ))
    
    conn.commit()
    conn.close()