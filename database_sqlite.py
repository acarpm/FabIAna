"""
Gestion de la base de données SQLite pour CampusFab.
Remplace database.py (JSON) par une vraie BD relationnelle.
"""

import sqlite3
import os
from typing import List, Optional
from models import Contact
from config import DATABASE_PATH


def initialiser_base_donnees():
    """Crée les tables si elles n'existent pas."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Table des contacts
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT UNIQUE NOT NULL,
            email TEXT,
            numero TEXT,
            etudes TEXT,
            laboratoire TEXT,
            autres_infos TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Table des compétences (relation many-to-many)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS competences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contact_id INTEGER NOT NULL,
            competence TEXT NOT NULL,
            FOREIGN KEY (contact_id) REFERENCES contacts(id) ON DELETE CASCADE,
            UNIQUE(contact_id, competence)
        )
    ''')
    
    # Table des métiers
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS metiers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contact_id INTEGER NOT NULL,
            metier TEXT NOT NULL,
            FOREIGN KEY (contact_id) REFERENCES contacts(id) ON DELETE CASCADE,
            UNIQUE(contact_id, metier)
        )
    ''')
    
    # Table des passions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS passions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contact_id INTEGER NOT NULL,
            passion TEXT NOT NULL,
            FOREIGN KEY (contact_id) REFERENCES contacts(id) ON DELETE CASCADE,
            UNIQUE(contact_id, passion)
        )
    ''')
    
    # Table des projets
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contact_id INTEGER NOT NULL,
            projet TEXT NOT NULL,
            FOREIGN KEY (contact_id) REFERENCES contacts(id) ON DELETE CASCADE,
            UNIQUE(contact_id, projet)
        )
    ''')
    
    conn.commit()
    conn.close()


def charger_contacts() -> List[Contact]:
    """Charge tous les contacts depuis la BD SQLite."""
    initialiser_base_donnees()
    
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        cursor.execute('SELECT * FROM contacts ORDER BY nom')
        rows = cursor.fetchall()
        
        contacts = []
        for row in rows:
            contact_id = row['id']
            
            # Charger les éléments liés
            cursor.execute('SELECT competence FROM competences WHERE contact_id = ?', (contact_id,))
            competences = [c[0] for c in cursor.fetchall()]
            
            cursor.execute('SELECT metier FROM metiers WHERE contact_id = ?', (contact_id,))
            metiers = [m[0] for m in cursor.fetchall()]
            
            cursor.execute('SELECT passion FROM passions WHERE contact_id = ?', (contact_id,))
            passions = [p[0] for p in cursor.fetchall()]
            
            cursor.execute('SELECT projet FROM projets WHERE contact_id = ?', (contact_id,))
            projets = [pr[0] for pr in cursor.fetchall()]
            
            # Créer l'objet Contact
            contact = Contact(
                nom=row['nom'],
                email=row['email'],
                numero=row['numero'],
                etudes=row['etudes'],
                laboratoire=row['laboratoire'],
                autres_infos=row['autres_infos'],
                competences=competences,
                métiers=metiers,
                passions=passions,
                projets=projets
            )
            contacts.append(contact)
        
        return contacts
    
    except Exception as e:
        print(f"Erreur lors du chargement des contacts : {e}")
        return []
    
    finally:
        conn.close()


def sauvegarder_contact(contact: Contact, est_modification: bool = False) -> bool:
    """Ajoute ou met à jour un contact dans la BD SQLite."""
    initialiser_base_donnees()
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    try:
        # Vérifier si le contact existe
        cursor.execute('SELECT id FROM contacts WHERE nom = ?', (contact.nom,))
        existing = cursor.fetchone()
        
        if existing and est_modification:
            contact_id = existing[0]
            
            # Mettre à jour les champs simples
            cursor.execute('''
                UPDATE contacts 
                SET email = ?, numero = ?, etudes = ?, 
                    laboratoire = ?, autres_infos = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (contact.email, contact.numero, contact.etudes, 
                  contact.laboratoire, contact.autres_infos, contact_id))
            
            # Fusionner les listes (ajouter sans doublon)
            _fusionner_listes(cursor, contact_id, contact)
            
        elif existing:
            # Contact existe mais pas en modification = remplacer
            contact_id = existing[0]
            
            # Supprimer les anciens éléments
            cursor.execute('DELETE FROM competences WHERE contact_id = ?', (contact_id,))
            cursor.execute('DELETE FROM metiers WHERE contact_id = ?', (contact_id,))
            cursor.execute('DELETE FROM passions WHERE contact_id = ?', (contact_id,))
            cursor.execute('DELETE FROM projets WHERE contact_id = ?', (contact_id,))
            
            # Mettre à jour les champs
            cursor.execute('''
                UPDATE contacts 
                SET email = ?, numero = ?, etudes = ?, 
                    laboratoire = ?, autres_infos = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (contact.email, contact.numero, contact.etudes, 
                  contact.laboratoire, contact.autres_infos, contact_id))
            
            # Ajouter les nouveaux éléments
            _ajouter_listes(cursor, contact_id, contact)
            
        else:
            # Nouveau contact
            cursor.execute('''
                INSERT INTO contacts (nom, email, numero, etudes, laboratoire, autres_infos)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (contact.nom, contact.email, contact.numero, contact.etudes,
                  contact.laboratoire, contact.autres_infos))
            
            contact_id = cursor.lastrowid
            _ajouter_listes(cursor, contact_id, contact)
        
        conn.commit()
        return True
    
    except Exception as e:
        print(f"Erreur lors de la sauvegarde : {e}")
        conn.rollback()
        return False
    
    finally:
        conn.close()


def _ajouter_listes(cursor: sqlite3.Cursor, contact_id: int, contact: Contact):
    """Ajoute les listes (compétences, métiers, etc) pour un contact."""
    for competence in contact.competences:
        cursor.execute(
            'INSERT OR IGNORE INTO competences (contact_id, competence) VALUES (?, ?)',
            (contact_id, competence)
        )
    
    for metier in contact.métiers:
        cursor.execute(
            'INSERT OR IGNORE INTO metiers (contact_id, metier) VALUES (?, ?)',
            (contact_id, metier)
        )
    
    for passion in contact.passions:
        cursor.execute(
            'INSERT OR IGNORE INTO passions (contact_id, passion) VALUES (?, ?)',
            (contact_id, passion)
        )
    
    for projet in contact.projets:
        cursor.execute(
            'INSERT OR IGNORE INTO projets (contact_id, projet) VALUES (?, ?)',
            (contact_id, projet)
        )


def _fusionner_listes(cursor: sqlite3.Cursor, contact_id: int, contact: Contact):
    """Fusionne les listes (ajout sans doublon) pour une modification."""
    # Charger les anciens éléments
    cursor.execute('SELECT competence FROM competences WHERE contact_id = ?', (contact_id,))
    competences_existantes = {c[0] for c in cursor.fetchall()}
    
    cursor.execute('SELECT metier FROM metiers WHERE contact_id = ?', (contact_id,))
    metiers_existants = {m[0] for m in cursor.fetchall()}
    
    cursor.execute('SELECT passion FROM passions WHERE contact_id = ?', (contact_id,))
    passions_existantes = {p[0] for p in cursor.fetchall()}
    
    cursor.execute('SELECT projet FROM projets WHERE contact_id = ?', (contact_id,))
    projets_existants = {pr[0] for pr in cursor.fetchall()}
    
    # Ajouter les nouveaux sans doublon
    for competence in contact.competences:
        if competence not in competences_existantes:
            cursor.execute(
                'INSERT INTO competences (contact_id, competence) VALUES (?, ?)',
                (contact_id, competence)
            )
    
    for metier in contact.métiers:
        if metier not in metiers_existants:
            cursor.execute(
                'INSERT INTO metiers (contact_id, metier) VALUES (?, ?)',
                (contact_id, metier)
            )
    
    for passion in contact.passions:
        if passion not in passions_existantes:
            cursor.execute(
                'INSERT INTO passions (contact_id, passion) VALUES (?, ?)',
                (contact_id, passion)
            )
    
    for projet in contact.projets:
        if projet not in projets_existants:
            cursor.execute(
                'INSERT INTO projets (contact_id, projet) VALUES (?, ?)',
                (contact_id, projet)
            )


def obtenir_noms_contacts() -> List[str]:
    """Retourne une liste des noms de contacts."""
    contacts = charger_contacts()
    return [c.nom for c in contacts if c.nom]


def supprimer_contact(nom: str) -> bool:
    """Supprime un contact par son nom."""
    initialiser_base_donnees()
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute('DELETE FROM contacts WHERE nom = ?', (nom,))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Erreur lors de la suppression : {e}")
        return False
    finally:
        conn.close()


def obtenir_statistiques() -> dict:
    """Retourne des statistiques sur la base de données."""
    initialiser_base_donnees()
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute('SELECT COUNT(*) FROM contacts')
        nb_contacts = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM competences')
        nb_competences = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM metiers')
        nb_metiers = cursor.fetchone()[0]
        
        return {
            'nb_contacts': nb_contacts,
            'nb_competences': nb_competences,
            'nb_metiers': nb_metiers
        }
    finally:
        conn.close()
