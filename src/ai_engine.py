import ollama
import json

def extraire_informations(texte_utilisateur):
    # Le "System Prompt" définit le rôle de l'IA
    system_prompt = """
    Tu es l'assistant de l'association CampusFab qui est un fablab sur l'Université de Toulouse. Ton nom est FabIAna. Ton rôle est d'extraire des informations sur les personnes pour en faire une base de connaisances.
    Réponds UNIQUEMENT au format JSON avec les clés suivantes :
    - nom: (string)
    - etudes: (string ou null)
    - métiers: (liste de strings)
    - passions: (liste de strings)
    - projets: (liste de strings)
    - laboratoire: (string ou null)
    - competences: (liste de strings)
    - email: (string ou null)
    - numero: (string ou null)
    - infos_manquantes: (booléen, true s'il manque des informations que tu estimes importantes pour la base de connaissances)
    - question_a_poser: (une question polie pour demander la/les info manquante, adaptée à la personne et au contexte, ou null si aucune question n'est nécessaire)
    """

    response = ollama.chat(
        model='llama3',
        format='json', # On force Llama 3 à répondre en JSON
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': texte_utilisateur},
        ]
    )
    
    # On transforme la réponse texte en dictionnaire Python
    return json.loads(response['message']['content'])

# --- TEST ---
phrase = "J'ai rencontré Alexandru Carp, il est étudiant en génie électrique et il gère trop en Arduino."
resultat = extraire_informations(phrase)

print(json.dumps(resultat, indent=2, ensure_ascii=False))