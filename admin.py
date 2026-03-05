#!/usr/bin/env python3
"""
Outil d'administration de la base de données CampusFab.
Permet de gérer, afficher et nettoyer la BD SQLite.
"""

import sqlite3
import os
from config import DATABASE_PATH
from database_sqlite import (
    initialiser_base_donnees,
    charger_contacts,
    supprimer_contact,
    obtenir_statistiques,
)
from models import Contact


def afficher_menu():
    """Affiche le menu principal."""
    print("\n╔════════════════════════════════════════════════════════════╗")
    print("║        ADMINISTRATION BASE DE DONNÉES - CAMPUSFAB         ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print("\n1. 📊 Afficher les statistiques")
    print("2. 👥 Lister tous les contacts")
    print("3. 🔍 Afficher un contact détaillé")
    print("4. 🗑️  Supprimer un contact")
    print("5. 🧹 Nettoyer la base de données")
    print("6. 💾 Exporter en JSON")
    print("7. ℹ️  Informations BD")
    print("8. ❌ Quitter")
    print()


def afficher_statistiques():
    """Affiche les statistiques de la BD."""
    try:
        stats = obtenir_statistiques()
        print("\n📊 STATISTIQUES")
        print("=" * 50)
        print(f"Contacts          : {stats['nb_contacts']}")
        print(f"Compétences total : {stats['nb_competences']}")
        print(f"Métiers total     : {stats['nb_metiers']}")
        if stats['nb_contacts'] > 0:
            print(f"Compétences/contact : {stats['nb_competences'] // stats['nb_contacts']:.1f}")
    except Exception as e:
        print(f"✗ Erreur : {e}")


def lister_contacts():
    """Liste tous les contacts."""
    try:
        contacts = charger_contacts()
        if not contacts:
            print("\n✓ Aucun contact enregistré")
            return
        
        print(f"\n👥 CONTACTS ({len(contacts)})")
        print("=" * 50)
        for i, contact in enumerate(contacts, 1):
            print(f"{i}. {contact.nom}")
            if contact.competences:
                print(f"   💼 {', '.join(contact.competences[:3])}")
            if contact.email:
                print(f"   📧 {contact.email}")
    except Exception as e:
        print(f"✗ Erreur : {e}")


def afficher_contact_detail():
    """Affiche les détails d'un contact."""
    try:
        contacts = charger_contacts()
        if not contacts:
            print("✓ Aucun contact enregistré")
            return
        
        print("\nContacts disponibles :")
        for i, c in enumerate(contacts, 1):
            print(f"  {i}. {c.nom}")
        
        choix = input("\nNuméro du contact : ").strip()
        try:
            idx = int(choix) - 1
            if 0 <= idx < len(contacts):
                contact = contacts[idx]
                print(f"\n📋 DÉTAILS - {contact.nom}")
                print("=" * 50)
                print(f"Email        : {contact.email or 'N/A'}")
                print(f"Téléphone    : {contact.numero or 'N/A'}")
                print(f"Études       : {contact.etudes or 'N/A'}")
                print(f"Labo         : {contact.laboratoire or 'N/A'}")
                print(f"Autres infos : {contact.autres_infos or 'N/A'}")
                print(f"\n💼 Compétences ({len(contact.competences)})")
                for comp in contact.competences:
                    print(f"  • {comp}")
                print(f"\n🎯 Métiers ({len(contact.métiers)})")
                for metier in contact.métiers:
                    print(f"  • {metier}")
                print(f"\n❤️  Passions ({len(contact.passions)})")
                for passion in contact.passions:
                    print(f"  • {passion}")
                print(f"\n🚀 Projets ({len(contact.projets)})")
                for projet in contact.projets:
                    print(f"  • {projet}")
            else:
                print("✗ Index invalide")
        except ValueError:
            print("✗ Entrée invalide")
    except Exception as e:
        print(f"✗ Erreur : {e}")


def supprimer_contact_menu():
    """Supprime un contact."""
    try:
        contacts = charger_contacts()
        if not contacts:
            print("✓ Aucun contact enregistré")
            return
        
        print("\nContacts disponibles :")
        for i, c in enumerate(contacts, 1):
            print(f"  {i}. {c.nom}")
        
        choix = input("\nNuméro du contact à supprimer : ").strip()
        try:
            idx = int(choix) - 1
            if 0 <= idx < len(contacts):
                contact = contacts[idx]
                confirmation = input(f"\nConfirmer la suppression de {contact.nom} ? (oui/non) : ").strip().lower()
                if confirmation == 'oui':
                    if supprimer_contact(contact.nom):
                        print(f"✓ {contact.nom} supprimé")
                    else:
                        print(f"✗ Erreur lors de la suppression")
                else:
                    print("Annulé")
            else:
                print("✗ Index invalide")
        except ValueError:
            print("✗ Entrée invalide")
    except Exception as e:
        print(f"✗ Erreur : {e}")


def nettoyer_base():
    """Nettoie la base de données."""
    try:
        confirmation = input("Êtes-vous sûr de vouloir vider la base de données ? (oui/non) : ").strip().lower()
        if confirmation == 'oui':
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()
            cursor.execute('DELETE FROM contacts')
            cursor.execute('DELETE FROM competences')
            cursor.execute('DELETE FROM metiers')
            cursor.execute('DELETE FROM passions')
            cursor.execute('DELETE FROM projets')
            conn.commit()
            conn.close()
            print("✓ Base de données vidée")
        else:
            print("Annulé")
    except Exception as e:
        print(f"✗ Erreur : {e}")


def exporter_json():
    """Exporte la BD en JSON."""
    try:
        import json
        contacts = charger_contacts()
        donnees = [c.to_dict() for c in contacts]
        
        filename = "export_campusfab.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(donnees, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Exporté vers {filename} ({len(contacts)} contacts)")
    except Exception as e:
        print(f"✗ Erreur : {e}")


def info_bd():
    """Affiche les infos sur la BD."""
    try:
        if os.path.exists(DATABASE_PATH):
            size = os.path.getsize(DATABASE_PATH) / 1024  # KB
            print(f"\n💾 INFORMATIONS BD")
            print("=" * 50)
            print(f"Chemin       : {DATABASE_PATH}")
            print(f"Taille       : {size:.2f} KB")
            
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            print(f"Tables       : {len(tables)}")
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
                count = cursor.fetchone()[0]
                print(f"  • {table[0]}: {count} lignes")
            conn.close()
        else:
            print("✓ Aucune BD existante (sera créée au premier démarrage)")
    except Exception as e:
        print(f"✗ Erreur : {e}")


def main():
    """Boucle principale."""
    initialiser_base_donnees()
    
    while True:
        afficher_menu()
        choix = input("Choix : ").strip()
        
        if choix == '1':
            afficher_statistiques()
        elif choix == '2':
            lister_contacts()
        elif choix == '3':
            afficher_contact_detail()
        elif choix == '4':
            supprimer_contact_menu()
        elif choix == '5':
            nettoyer_base()
        elif choix == '6':
            exporter_json()
        elif choix == '7':
            info_bd()
        elif choix == '8':
            print("\nAu revoir ! À bientôt au Fablab.")
            break
        else:
            print("✗ Choix invalide")


if __name__ == "__main__":
    main()
