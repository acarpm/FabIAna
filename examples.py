#!/usr/bin/env python3
"""
Exemples d'utilisation de FabIAna comme librairie.
Montre comment avoir accès aux modules de manière programmatique.
"""

from models import Contact, BesoinsAnalyse
from database_sqlite import charger_contacts, sauvegarder_contact, obtenir_noms_contacts
from search import chercher_personnes
from ai_service import analyser_besoins, extraire_informations


# ============================================
# EXEMPLE 1 : Charger et afficher tous les contacts
# ============================================
def exemple_charger_contacts():
    """Charge et affiche tous les contacts."""
    print("\n=== EXEMPLE 1 : Charger les contacts ===")
    contacts = charger_contacts()
    print(f"Nombre de contacts : {len(contacts)}")
    for contact in contacts:
        print(f"  - {contact.nom}: {', '.join(contact.competences)}")


# ============================================
# EXEMPLE 2 : Créer et sauvegarder un contact
# ============================================
def exemple_creer_contact():
    """Crée un nouveau contact et le sauvegarde."""
    print("\n=== EXEMPLE 2 : Créer un contact ===")
    
    nouveau_contact = Contact(
        nom="Marie",
        métiers=["Designer UX/UI"],
        competences=["Figma", "Adobe XD", "Prototypage"],
        passions=["Design d'Interface", "Accessibilité Web"],
        email="marie@example.com",
        projets=["Refonte Interface CampusFab"]
    )
    
    print(f"Contact créé : {nouveau_contact.nom}")
    
    # Sauvegarder
    success = sauvegarder_contact(nouveau_contact)
    if success:
        print("✓ Contact sauvegardé avec succès")
    else:
        print("✗ Erreur lors de la sauvegarde")


# ============================================
# EXEMPLE 3 : Chercher des personnes avec compétences
# ============================================
def exemple_chercher_competence():
    """Cherche des personnes avec une compétence spécifique."""
    print("\n=== EXEMPLE 3 : Chercher par compétence ===")
    
    resultats = chercher_personnes("J'ai besoin de quelqu'un qui sait programmer")
    
    if resultats:
        print(f"Trouvé {len(resultats)} personne(s) :")
        for contact in resultats:
            print(f"  - {contact.nom}")
            print(f"    Compétences: {', '.join(contact.competences)}")
    else:
        print("Aucune personne trouvée")


# ============================================
# EXEMPLE 4 : Analyser les besoins avec l'IA
# ============================================
def exemple_analyser_besoins():
    """Analyse une demande avec l'IA."""
    print("\n=== EXEMPLE 4 : Analyser les besoins ===")
    
    demande = "J'ai besoin de quelqu'un expert en électronique et Arduino"
    print(f"Demande : {demande}")
    
    besoins = analyser_besoins(demande)
    print(f"Compétences identifiées : {besoins.competences_necessaires}")
    print(f"Synonymes : {besoins.synonymes}")


# ============================================
# EXEMPLE 5 : Modifier un contact existant
# ============================================
def exemple_modifier_contact():
    """Modifie un contact existant."""
    print("\n=== EXEMPLE 5 : Modifier un contact ===")
    
    # Charger les contacts
    contacts = charger_contacts()
    
    if contacts:
        # Prendre le premier contact
        contact = contacts[0]
        print(f"Contact original : {contact.nom}")
        print(f"Compétences avant : {contact.competences}")
        
        # Ajouter une compétence
        if "Nouvelle Compétence" not in contact.competences:
            contact.competences.append("Nouvelle Compétence")
        
        # Sauvegarder avec modification=True
        success = sauvegarder_contact(contact, est_modification=True)
        
        if success:
            print(f"Compétences après : {contact.competences}")
            print("✓ Contact mis à jour")
        else:
            print("✗ Erreur lors de la mise à jour")
    else:
        print("Aucun contact à modifier")


# ============================================
# EXEMPLE 6 : Lister les noms des contacts
# ============================================
def exemple_lister_noms():
    """Liste tous les noms des contacts."""
    print("\n=== EXEMPLE 6 : Lister les noms ===")
    
    noms = obtenir_noms_contacts()
    if noms:
        print("Contacts enregistrés :")
        for nom in noms:
            print(f"  - {nom}")
    else:
        print("Aucun contact enregistré")


# ============================================
# EXEMPLE 7 : Convertir Contact en dictionnaire
# ============================================
def exemple_contact_dict():
    """Montre comment convertir un contact en dictionnaire."""
    print("\n=== EXEMPLE 7 : Conversion Contact → Dict ===")
    
    contact = Contact(
        nom="Bob",
        competences=["Python"],
        métiers=["Développeur"]
    )
    
    contact_dict = contact.to_dict()
    
    print(f"Contact : {contact}")
    print(f"Dict : {contact_dict}")
    
    # Créer un contact depuis un dict
    contact2 = Contact.from_dict(contact_dict)
    print(f"Nouveau Contact : {contact2}")


# ============================================
# EXEMPLE 8 : Extraire les informations d'une conversation
# ============================================
def exemple_extraire_info():
    """Montre comment extraire les informations d'une conversation."""
    print("\n=== EXEMPLE 8 : Extraction d'informations ===")
    
    # Simuler une conversation
    historique = [
        {'role': 'user', 'content': "Je voudrais enregistrer quelqu'un"},
        {'role': 'assistant', 'content': 'Bien sûr ! Dites-moi son nom'},
        {'role': 'user', 'content': "Il s'appelle Thomas et il sait faire de la 3D"},
    ]
    
    print("Conversation :")
    for msg in historique:
        print(f"  {msg['role'].upper()} : {msg['content']}")
    
    # Extraire les infos
    result = extraire_informations(historique)
    
    if result.contact:
        print(f"\n✓ Extraction réussie :")
        print(f"  Nom : {result.contact.nom}")
        print(f"  Compétences : {result.contact.competences}")
        print(f"  Modification : {result.est_modification}")
    else:
        print(f"\n✗ Erreur : {result.error}")


# ============================================
# MAIN
# ============================================
if __name__ == "__main__":
    print("╔═════════════════════════════════════════════╗")
    print("║    EXEMPLES D'UTILISATION DE FABIANA    ║")
    print("╚═════════════════════════════════════════════╝")
    
    try:
        exemple_charger_contacts()
        # exemple_creer_contact()  # Décommenter pour créer un contact
        exemple_chercher_competence()
        # exemple_analyser_besoins()  # Nécessite Ollama
        # exemple_modifier_contact()  # Décommenter pour modifier
        exemple_lister_noms()
        exemple_contact_dict()
        # exemple_extraire_info()  # Nécessite Ollama
        
    except Exception as e:
        print(f"\n✗ Erreur : {e}")
        import traceback
        traceback.print_exc()
