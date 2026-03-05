#!/usr/bin/env python3
"""
Script de migration : convertit contacts.json (JSON) → campusfab.db (SQLite)
À exécuter une seule fois pour migrer les données existantes.
"""

import json
import os
from models import Contact
from database_sqlite import sauvegarder_contact, initialiser_base_donnees
from config import CONTACTS_FILE, DATABASE_PATH


def migrer_donnees():
    """Migre les données de JSON vers SQLite."""
    
    # Initialiser la BD
    initialiser_base_donnees()
    
    # Vérifier si le fichier JSON existe
    if not os.path.exists(CONTACTS_FILE):
        print(f"✓ Aucun fichier {CONTACTS_FILE} trouvé. BD SQLite initialisée vide.")
        return
    
    print(f"🔄 Lecture de {CONTACTS_FILE}...")
    
    try:
        with open(CONTACTS_FILE, 'r', encoding='utf-8') as f:
            donnees = json.load(f)
        
        if not donnees:
            print(f"✓ {CONTACTS_FILE} est vide.")
            return
        
        print(f"📥 Migration de {len(donnees)} contact(s)...")
        
        migres = 0
        erreurs = 0
        
        for data in donnees:
            try:
                contact = Contact.from_dict(data)
                success = sauvegarder_contact(contact, est_modification=False)
                
                if success:
                    print(f"  ✓ {contact.nom}")
                    migres += 1
                else:
                    print(f"  ✗ Erreur : {contact.nom}")
                    erreurs += 1
            except Exception as e:
                print(f"  ✗ Erreur : {e}")
                erreurs += 1
        
        print(f"\n{'='*50}")
        print(f"Migration terminée !")
        print(f"  ✓ {migres} contact(s) migré(s)")
        print(f"  ✗ {erreurs} erreur(s)")
        print(f"{'='*50}")
        
        # Backup du fichier JSON
        backup_path = f"{CONTACTS_FILE}.backup"
        os.rename(CONTACTS_FILE, backup_path)
        print(f"\n💾 Sauvegarde : {CONTACTS_FILE} → {backup_path}")
        print(f"📊 Base de données SQLite : {DATABASE_PATH}")
        
    except json.JSONDecodeError as e:
        print(f"✗ Erreur lecture JSON : {e}")
    except Exception as e:
        print(f"✗ Erreur migration : {e}")


if __name__ == "__main__":
    print("╔════════════════════════════════════════════════════════════╗")
    print("║         Migration JSON → SQLite (CampusFab)               ║")
    print("╚════════════════════════════════════════════════════════════╝\n")
    
    migrer_donnees()
