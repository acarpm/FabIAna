"""
Service d'intégration avec l'IA Ollama pour l'extraction et l'analyse d'informations.
"""

import json
from typing import List, Dict, Any
import ollama
from config import MODEL
from models import BesoinsAnalyse, ExtractionResult, Contact
from database_sqlite import obtenir_noms_contacts


def analyser_besoins(demande_utilisateur: str) -> BesoinsAnalyse:
    """Utilise l'IA pour analyser les compétences nécessaires pour une tâche."""
    prompt_analyse = f"""
    L'utilisateur a une demande : "{demande_utilisateur}"

    Analyse cette demande et retourne un JSON avec :
    - competences_necessaires: (liste des compétences/domaines nécessaires, sois large et inclusif)
    - synonymes: (liste de synonymes ou termes connexes)

    Exemple :
    Si la demande est "programmer", retourne :
    {{"competences_necessaires": ["Python", "JavaScript", "C++", "programmation", "développement", "code"], "synonymes": ["coder", "développer", "coding"]}}

    Sois inclusif et pense à tous les domaines connexes.
    """

    messages = [{'role': 'user', 'content': prompt_analyse}]

    try:
        response = ollama.chat(
            model=MODEL,
            format='json',
            messages=messages
        )
        data = json.loads(response['message']['content'])
        return BesoinsAnalyse(
            competences_necessaires=data.get('competences_necessaires', []),
            synonymes=data.get('synonymes', [])
        )
    except Exception:
        return BesoinsAnalyse(
            competences_necessaires=[demande_utilisateur.lower()],
            synonymes=[]
        )


def extraire_informations(historique_conversation: List[Dict[str, str]]) -> ExtractionResult:
    """
    Envoie l'historique à l'IA et récupère une analyse structurée.
    """
    # Obtenir la liste des contacts existants
    noms_contacts = obtenir_noms_contacts()
    liste_contacts_str = ", ".join(noms_contacts) if noms_contacts else "Aucun contact enregistré"

    system_prompt = f"""
        Tu es l'assistant de l'association CampusFab qui est un fablab sur l'Université de Toulouse. Ton nom est FabIAna. Ton rôle est d'extraire des informations sur les personnes pour en faire une base de connaisances.

        CONTACTS EXISTANTS : {liste_contacts_str}
        Si tu reconnais l'un de ces noms dans la conversation, ajoute "est_modification: true" à ta réponse.

        IMPORTANT : Si l'utilisateur demande à chercher/trouver ou action similaire à une personne pour une tâche, un projet ou avec une certaine compétence/métier/passion, tu dois TOUJOURS retourner :
        - est_recherche: true
        - terme_recherche: (résume la demande globale)

        Sinon, réponds UNIQUEMENT au format JSON avec les clés suivantes :
        - est_recherche: false
        - est_modification: (true si tu reconnais un contact existant, false sinon)
        - nom: (string)
        - etudes: (string ou null)
        - métiers: (liste de strings)
        - passions: (liste de strings)
        - projets: (liste de strings)
        - laboratoire: (string ou null)
        - competences: (liste de strings)
        - email: (string ou null)
        - numero: (string ou null)
        - autres_infos: (string ou null)
        - infos_manquantes: (booléen)
        - question_a_poser: (string ou null)
    """

    # On prépare les messages (Prompt Système + Historique)
    messages = [{'role': 'system', 'content': system_prompt}] + historique_conversation

    try:
        response = ollama.chat(
            model=MODEL,
            format='json',
            messages=messages
        )
        data = json.loads(response['message']['content'])
        
        # Créer un objet Contact si ce n'est pas une recherche
        contact = None
        if not data.get('est_recherche', False):
            contact = Contact.from_dict(data)
        
        return ExtractionResult(
            est_recherche=data.get('est_recherche', False),
            est_modification=data.get('est_modification', False),
            contact=contact,
            infos_manquantes=data.get('infos_manquantes', False),
            question_a_poser=data.get('question_a_poser'),
            terme_recherche=data.get('terme_recherche')
        )
    except Exception as e:
        return ExtractionResult(
            est_recherche=False,
            error=str(e)
        )
