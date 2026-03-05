"""
Moteur de recherche intelligent pour trouver les personnes idéales.
"""

from typing import List
from models import Contact
from database_sqlite import charger_contacts
from ai_service import analyser_besoins


def chercher_personnes(terme_recherche: str) -> List[Contact]:
    """Cherche intelligemment les personnes qui correspondent à une demande."""
    contacts = charger_contacts()

    # Analyser les besoins pour obtenir les compétences clés et synonymes
    besoins = analyser_besoins(terme_recherche)
    competences_cles = besoins.competences_necessaires
    synonymes = besoins.synonymes

    resultats = []

    for contact in contacts:
        score = 0

        # Chercher dans les compétences (priorité haute)
        for comp in contact.competences:
            comp_lower = comp.lower()
            for cle in competences_cles:
                if cle.lower() in comp_lower or comp_lower in cle.lower():
                    score += 3
                    break

        # Chercher dans les métiers (priorité moyenne)
        for metier in contact.métiers:
            metier_lower = metier.lower()
            for cle in competences_cles:
                if cle.lower() in metier_lower or metier_lower in cle.lower():
                    score += 2
                    break

        # Chercher dans les passions (priorité basse)
        for passion in contact.passions:
            passion_lower = passion.lower()
            for cle in competences_cles:
                if cle.lower() in passion_lower or passion_lower in cle.lower():
                    score += 1.5
                    break

        # Chercher dans les projets (priorité basse)
        for projet in contact.projets:
            projet_lower = projet.lower()
            for cle in competences_cles:
                if cle.lower() in projet_lower or projet_lower in cle.lower():
                    score += 1.5
                    break

        # Chercher avec les synonymes (score réduit mais compte)
        for syn in synonymes:
            syn_lower = syn.lower()
            for comp in contact.competences:
                if syn_lower in comp.lower():
                    score += 2
                    break
            for metier in contact.métiers:
                if syn_lower in metier.lower():
                    score += 1
                    break

        if score > 0:
            resultats.append((contact, score))

    # Trier par pertinence (score décroissant)
    resultats.sort(key=lambda x: x[1], reverse=True)
    return [contact for contact, _ in resultats]
