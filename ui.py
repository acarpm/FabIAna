"""
Interface utilisateur et logique d'interaction principale.
"""

from typing import List, Dict
from ai_service import extraire_informations
from database_sqlite import sauvegarder_contact
from search import chercher_personnes
from models import Contact


def afficher_entete():
    """Affiche l'en-tête de l'application."""
    print("====================================================")
    print("   FABIANA : Assistante Base de Connaissances       ")
    print("   CampusFab - Université de Toulouse               ")
    print("====================================================")
    print("(Tapez 'quitter' pour sortir)")
    print("\nModes d'utilisation :")
    print("1. AJOUTER : Décrivez une personne pour l'enregistrer")
    print("2. CHERCHER : Dites 'j'ai besoin de quelqu'un qui...' pour trouver quelqu'un")
    print("   Exemple : 'J'ai besoin de quelqu'un qui sait Python'")
    print("            'Peux-tu me trouver une personne avec des compétences en CAO ?'\n")


def afficher_contact(contact: Contact, index: int = 1):
    """Affiche les informations d'un contact."""
    print(f"\n  {index}. {contact.nom}")
    if contact.competences:
        print(f"     💼 Compétences : {', '.join(contact.competences)}")
    if contact.métiers:
        print(f"     🎯 Métiers : {', '.join(contact.métiers)}")
    if contact.passions:
        print(f"     ❤️  Passions : {', '.join(contact.passions)}")
    if contact.projets:
        print(f"     🚀 Projets : {', '.join(contact.projets)}")
    if contact.email:
        print(f"     📧 Email : {contact.email}")
    if contact.numero:
        print(f"     📱 Téléphone : {contact.numero}")


def afficher_resultats_recherche(resultats: List[Contact], terme: str):
    """Affiche les résultats de recherche."""
    if resultats:
        print(f"\nFabIAna : J'ai trouvé {len(resultats)} personne(s) idéale(s) pour '{terme}' :")
        for i, contact in enumerate(resultats, 1):
            afficher_contact(contact, i)
    else:
        print(f"\nFabIAna : Hmm, je n'ai trouvé personne directement avec '{terme}', mais continuer à ajouter des personnes enrichira ma base de connaissances ! 👍")


def demander_enregistrement(fiche_actuelle: Dict) -> bool:
    """Demande à l'utilisateur s'il souhaite enregistrer la fiche."""
    import json
    print("\n--- FICHE RÉCAPITULATIVE ---")
    print(json.dumps(fiche_actuelle, indent=2, ensure_ascii=False))
    print("----------------------------")
    
    choix = input("Voulez-vous enregistrer ce membre ? (oui/non) : ")
    return choix.lower() == 'oui'


def traiter_recherche(analyse, historique_conversation: List) -> bool:
    """
    Traite une demande de recherche.
    Retourne True si la recherche a été effectuée.
    """
    if not analyse.est_recherche:
        return False
    
    terme = analyse.terme_recherche or ''
    resultats = chercher_personnes(terme)
    afficher_resultats_recherche(resultats, terme)
    
    # Réinitialiser pour une nouvelle recherche
    historique_conversation.clear()
    return True


def traiter_information_contact(analyse, historique_conversation: List) -> bool:
    """
    Traite l'extraction d'informations de contact.
    Retourne True si des informations ont été traitées.
    """
    if not analyse.contact:
        return False
    
    if analyse.error:
        print(f"Erreur technique : {analyse.error}")
        return False

    # Si l'IA a une question à poser
    if analyse.infos_manquantes and analyse.question_a_poser:
        print(f"\nFabIAna : {analyse.question_a_poser}")
        historique_conversation.append({'role': 'assistant', 'content': analyse.question_a_poser})
    else:
        verbe = "enrichi" if analyse.est_modification else "noté"
        print(f"\nFabIAna : Merci ! J'ai bien {verbe} ces informations.")
        
        fiche_dict = analyse.contact.to_dict()
        
        if demander_enregistrement(fiche_dict):
            if sauvegarder_contact(analyse.contact, est_modification=analyse.est_modification):
                action = "mis à jour" if analyse.est_modification else "enregistré"
                print(f"✓ {analyse.contact.nom} {action} avec succès !")
            else:
                print("✗ Erreur lors de l'enregistrement.")

        # On réinitialise pour une nouvelle personne
        historique_conversation.clear()
        print("\nPrête pour une nouvelle saisie !")
    
    return True


def boucle_principale():
    """Boucle principale de l'application."""
    afficher_entete()
    
    historique_conversation = []
    
    while True:
        user_input = input("\nVous : ")

        if user_input.lower() in ['quitter', 'exit', 'stop']:
            print("FabIAna : Au revoir ! À bientôt au Fablab.")
            break

        # Ajouter le message de l'utilisateur à l'historique
        historique_conversation.append({'role': 'user', 'content': user_input})

        print("FabIAna réfléchit...")

        # Appel à l'IA
        analyse = extraire_informations(historique_conversation)

        # Traiter les différents cas
        if traiter_recherche(analyse, historique_conversation):
            continue
        
        if traiter_information_contact(analyse, historique_conversation):
            continue
