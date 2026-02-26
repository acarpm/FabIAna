import ollama
import json

# Configuration
MODEL = "llama3:8b"

def extraire_informations(historique_conversation):
    """
    Envoie l'historique à l'IA et récupère une analyse structurée en JSON.
    """
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
        - autres_infos: (string ou null, pour toute information que tu juges pertinente mais qui ne rentre pas dans les autres catégories)
        - infos_manquantes: (booléen, true s'il manque des informations que tu estimes importantes pour la base de connaissances. Tu peux demander des infomations autres que celles listées ci-dessus si tu penses que c'est nécessaire pour mieux comprendre la personne ou pour enrichir la base de connaissances, mais ce n'est pas obligatoire)
        - question_a_poser: (une question polie pour demander la/les info manquante, adaptée à la personne et au contexte, ou null si aucune question n'est nécessaire)
    """

    # On prépare les messages (Prompt Système + Historique)
    messages = [{'role': 'system', 'content': system_prompt}] + historique_conversation

    try:
        response = ollama.chat(
            model=MODEL,
            format='json',
            messages=messages
        )
        return json.loads(response['message']['content'])
    except Exception as e:
        return {"error": str(e)}

def main():
    print("====================================================")
    print("   FABIANA : Assistante Base de Connaissances       ")
    print("   CampusFab - Université de Toulouse               ")
    print("====================================================")
    print("(Tapez 'quitter' pour sortir)\n")

    # Cette liste va stocker les échanges pour que l'IA ait de la mémoire
    historique_conversation = []
    
    # On garde une trace de la fiche en cours de création
    fiche_actuelle = {}

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

        if "error" in analyse:
            print(f"Erreur technique : {analyse['error']}")
            continue

        # Mise à jour de la fiche actuelle avec les nouvelles données trouvées
        fiche_actuelle.update({k: v for k, v in analyse.items() if v is not None and k not in ['infos_manquantes', 'question_a_poser']})

        # --- LOGIQUE DE RÉPONSE ---
        
        # Si l'IA a une question à poser
        if analyse.get('infos_manquantes') and analyse.get('question_a_poser'):
            reponse_ia = analyse['question_a_poser']
            print(f"\nFabIAna : {reponse_ia}")
            # On ajoute la réponse de l'IA à l'historique pour la mémoire du prochain tour
            historique_conversation.append({'role': 'assistant', 'content': reponse_ia})
        
        else:
            print("\nFabIAna : Merci ! J'ai bien noté ces informations.")
            print("--- FICHE RÉCAPITULATIVE ---")
            print(json.dumps(fiche_actuelle, indent=2, ensure_ascii=False))
            print("----------------------------")
            
            # Ici on pourrait proposer de sauvegarder en base de données
            choix = input("Voulez-vous enregistrer ce membre ? (oui/non) : ")
            if choix.lower() == 'oui':
                print("Enregistrement en base de données... (Bientôt disponible)")
            
            # On réinitialise pour une nouvelle personne
            historique_conversation = []
            fiche_actuelle = {}
            print("\nPrête pour une nouvelle saisie !")

if __name__ == "__main__":
    main()