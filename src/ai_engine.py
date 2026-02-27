import ollama
import json
# On importe nos fonctions de base de données
from database import initialiser_bdd, sauvegarder_membre

# Configuration
MODEL = "llama3:8b"

def extraire_informations(historique_conversation):
    system_prompt = """

        Tu es FabIAna, l'assistante intelligente du Fablab CampusFab (Université de Toulouse).
        Ton rôle est d'extraire des informations précises pour la base de connaissances.

        RÈGLES D'EXTRACTION :
        - 'nom' : Extrais le nom et le prenom complet (Prénom et NOM). Ignore les titres comme "Tréso" ou "Président" ici.
        - 'metiers' : Inclus les rôles dans l'association/societe/labo si il y en a (ex: Trésorier).
        - 'competences' : Liste TOUTES les compétences techniques mentionnées (langages, info, outils, machines, logiciels). 
           Si quelqu'un dit qu'il "gère" ou "aime travailler sur" un outil technique, c'est une compétence.
        - 'autres_infos' : Doit contenir les réseaux sociaux (GitHub, LinkedIn), les dates d'arrivée, et tout détail historique.
        - 'etudes' : Précise l'année et la filière.

        Réponds UNIQUEMENT au format JSON avec ces clés :
        {
            "nom": string, "etudes": string, "métiers": [string], "passions": [string],
            "projets": [string], "laboratoire": string, "competences": [string],
            "email": string, "numero": string, "autres_infos": string,
            "infos_manquantes": boolean, "question_a_poser": string
        }
        

        Si le message de l'utilisateur semble incohérent ou hors sujet, n'hésite pas à demander des clarifications.
    """

    messages = [{'role': 'system', 'content': system_prompt}] + historique_conversation

    try:
        response = ollama.chat(model=MODEL, format='json', messages=messages)
        return json.loads(response['message']['content'])
    except Exception as e:
        return {"error": str(e)}

def main():
    # 1. On prépare la base de données au lancement
    initialiser_bdd()

    print("====================================================")
    print("   FABIANA : Assistante Base de Connaissances       ")
    print("   CampusFab - Université de Toulouse               ")
    print("====================================================")
    print("(Tapez 'quitter' pour sortir)\n")

    historique_conversation = []
    fiche_actuelle = {}

    while True:
        user_input = input("\nVous : ")

        if user_input.lower() in ['quitter', 'exit', 'stop']:
            print("FabIAna : Au revoir ! À bientôt au Fablab.")
            break

        historique_conversation.append({'role': 'user', 'content': user_input})
        print("FabIAna réfléchit...")

        analyse = extraire_informations(historique_conversation)

        if "error" in analyse:
            print(f"Erreur technique : {analyse['error']}")
            continue

        # Mise à jour intelligente de la fiche
        for k, v in analyse.items():
            if v is not None and k not in ['infos_manquantes', 'question_a_poser']:
                fiche_actuelle[k] = v

        if analyse.get('infos_manquantes') and analyse.get('question_a_poser'):
            reponse_ia = analyse['question_a_poser']
            print(f"\nFabIAna : {reponse_ia}")
            historique_conversation.append({'role': 'assistant', 'content': reponse_ia})
        
        else:
            print("\nFabIAna : Merci ! J'ai bien noté ces informations.")
            print("--- FICHE RÉCAPITULATIVE ---")
            print(json.dumps(fiche_actuelle, indent=2, ensure_ascii=False))
            print("----------------------------")
            
            choix = input("Voulez-vous enregistrer ce membre en BDD ? (oui/non) : ")
            if choix.lower() == 'oui':
                # 2. On sauvegarde réellement !
                try:
                    sauvegarder_membre(fiche_actuelle)
                    print("✅ Informations enregistrées avec succès dans data/campusfab.db")
                except Exception as e:
                    print(f"❌ Erreur lors de l'enregistrement : {e}")
            
            # Reset pour la suite
            historique_conversation = []
            fiche_actuelle = {}
            print("\nPrête pour une nouvelle saisie !")

if __name__ == "__main__":
    main()