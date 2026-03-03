
import ollama
import json
import os

# Configuration
MODEL = "llama3:8b"
CONTACTS_FILE = "contacts.json"

def charger_contacts():
    """Charge les contacts existants depuis le fichier JSON."""
    if os.path.exists(CONTACTS_FILE):
        try:
            with open(CONTACTS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Erreur lors du chargement des contacts : {e}")
            return []
    return []

def sauvegarder_contact(contact, est_modification=False):
    """Ajoute ou met à jour un contact dans le fichier JSON."""
    contacts = charger_contacts()
    contact_nom = contact.get('nom', '')

    # Chercher si le contact existe déjà (par nom)
    contact_existe_index = -1
    for i, c in enumerate(contacts):
        if c.get('nom', '').lower() == contact_nom.lower():
            contact_existe_index = i
            break

    if contact_existe_index >= 0 and est_modification:
        # MODIFICATION : fusionner les données au lieu de les remplacer
        contact_existant = contacts[contact_existe_index]

        # Fusionner les listes (compétences, métiers, etc)
        for cle in ['competences', 'métiers', 'passions', 'projets']:
            if cle in contact and contact[cle]:
                if cle not in contact_existant:
                    contact_existant[cle] = []
                # Ajouter les nouveaux éléments sans doublon
                for item in contact[cle]:
                    if item not in contact_existant[cle]:
                        contact_existant[cle].append(item)

        # Mettre à jour les champs simples (email, etc)
        for cle in ['email', 'numero', 'etudes', 'laboratoire', 'autres_infos']:
            if cle in contact and contact[cle]:
                contact_existant[cle] = contact[cle]

        contacts[contact_existe_index] = contact_existant
    elif contact_existe_index >= 0:
        # Contact existe mais pas en modification = remplacer
        contacts[contact_existe_index] = contact
    else:
        # Nouveau contact
        contacts.append(contact)

    try:
        with open(CONTACTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(contacts, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Erreur lors de la sauvegarde : {e}")
        return False

def analyser_besoins(demande_utilisateur):
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
        return json.loads(response['message']['content'])
    except:
        return {"competences_necessaires": [demande_utilisateur.lower()], "synonymes": []}

def obtenir_liste_contacts_pour_ia():
    """Retourne une liste simple des noms de contacts pour que l'IA puisse les chercher."""
    contacts = charger_contacts()
    return [c.get('nom', '') for c in contacts if c.get('nom')]

def chercher_personnes(terme_recherche):
    """Cherche intelligemment les personnes qui correspondent à une demande."""
    contacts = charger_contacts()

    # Analyser les besoins pour obtenir les compétences clés et synonymes
    besoins = analyser_besoins(terme_recherche)
    competences_cles = besoins.get('competences_necessaires', [])
    synonymes = besoins.get('synonymes', [])

    resultats = []

    for contact in contacts:
        score = 0
        details_match = []

        # Compétences du contact
        competences_contact = contact.get('competences', [])
        metiers_contact = contact.get('métiers', [])
        passions_contact = contact.get('passions', [])
        projets_contact = contact.get('projets', [])
        etudes_contact = contact.get('etudes', '')

        # Chercher dans les compétences (priorité haute)
        for comp in competences_contact:
            comp_lower = comp.lower()
            for cle in competences_cles:
                if cle.lower() in comp_lower or comp_lower in cle.lower():
                    score += 3
                    details_match.append(f"Compétence: {comp}")
                    break

        # Chercher dans les métiers (priorité moyenne)
        for metier in metiers_contact:
            metier_lower = metier.lower()
            for cle in competences_cles:
                if cle.lower() in metier_lower or metier_lower in cle.lower():
                    score += 2
                    details_match.append(f"Métier: {metier}")
                    break

        # Chercher dans les passions (priorité basse)
        for passion in passions_contact:
            passion_lower = passion.lower()
            for cle in competences_cles:
                if cle.lower() in passion_lower or passion_lower in cle.lower():
                    score += 1.5
                    details_match.append(f"Passion: {passion}")
                    break

        # Chercher dans les projets (priorité basse)
        for projet in projets_contact:
            projet_lower = projet.lower()
            for cle in competences_cles:
                if cle.lower() in projet_lower or projet_lower in cle.lower():
                    score += 1.5
                    break

        # Chercher avec les synonymes (score réduit mais compte)
        for syn in synonymes:
            syn_lower = syn.lower()
            for comp in competences_contact:
                if syn_lower in comp.lower():
                    score += 2
                    break
            for metier in metiers_contact:
                if syn_lower in metier.lower():
                    score += 1
                    break

        if score > 0:
            resultats.append((contact, score, details_match))

    # Trier par pertinence (score décroissant)
    resultats.sort(key=lambda x: x[1], reverse=True)
    return [contact for contact, _, _ in resultats]

def extraire_informations(historique_conversation):
    """
    Envoie l'historique à l'IA et récupère une analyse structurée en JSON.
    """
    # Obtenir la liste des contacts existants
    contacts_existants = obtenir_liste_contacts_pour_ia()
    liste_contacts_str = ", ".join(contacts_existants) if contacts_existants else "Aucun contact enregistré"

    system_prompt = f"""
        Tu es l'assistant de l'association CampusFab qui est un fablab sur l'Université de Toulouse. Ton nom est FabIAna. Ton rôle est d'extraire des informations sur les personnes pour en faire une base de connaisances.

        CONTACTS EXISTANTS : {liste_contacts_str}
        Si tu reconnais l'un de ces noms dans la conversation, ajoute "est_modification: true" à ta réponse.

        IMPORTANT : Si l'utilisateur demande à chercher/trouver une personne pour une tâche, un projet ou avec une certaine compétence/métier/passion, tu dois TOUJOURS retourner :
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
        return json.loads(response['message']['content'])
    except Exception as e:
        return {"error": str(e)}

def main():
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

        # --- GESTION DES RECHERCHES ---
        if analyse.get('est_recherche'):
            terme = analyse.get('terme_recherche', '')
            resultats = chercher_personnes(terme)

            if resultats:
                print(f"\nFabIAna : J'ai trouvé {len(resultats)} personne(s) idéale(s) pour '{terme}' :")
                for i, contact in enumerate(resultats, 1):
                    nom = contact.get('nom', 'Inconnu')
                    competences = contact.get('competences', [])
                    metiers = contact.get('métiers', [])
                    passions = contact.get('passions', [])
                    projets = contact.get('projets', [])
                    email = contact.get('email')
                    numero = contact.get('numero')

                    print(f"\n  {i}. {nom}")
                    if competences:
                        print(f"     💼 Compétences : {', '.join(competences)}")
                    if metiers:
                        print(f"     🎯 Métiers : {', '.join(metiers)}")
                    if passions:
                        print(f"     ❤️  Passions : {', '.join(passions)}")
                    if projets:
                        print(f"     🚀 Projets : {', '.join(projets)}")
                    if email:
                        print(f"     📧 Email : {email}")
                    if numero:
                        print(f"     📱 Téléphone : {numero}")
            else:
                print(f"\nFabIAna : Hmm, je n'ai trouvé personne directement avec '{terme}', mais continuer à ajouter des personnes enrichira ma base de connaissances ! 👍")

            # Réinitialiser pour une nouvelle recherche
            historique_conversation = []
            fiche_actuelle = {}
            continue

        # Mise à jour de la fiche actuelle avec les nouvelles données trouvées
        fiche_actuelle.update({k: v for k, v in analyse.items() if v is not None and k not in ['infos_manquantes', 'question_a_poser', 'est_recherche', 'terme_recherche', 'est_modification']})

        # --- LOGIQUE DE RÉPONSE ---

        # Si l'IA a une question à poser
        if analyse.get('infos_manquantes') and analyse.get('question_a_poser'):
            reponse_ia = analyse['question_a_poser']
            print(f"\nFabIAna : {reponse_ia}")
            # On ajoute la réponse de l'IA à l'historique pour la mémoire du prochain tour
            historique_conversation.append({'role': 'assistant', 'content': reponse_ia})

        else:
            est_modification = analyse.get('est_modification', False)
            verbe = "enrichi" if est_modification else "noté"
            print(f"\nFabIAna : Merci ! J'ai bien {verbe} ces informations.")
            print("--- FICHE RÉCAPITULATIVE ---")
            print(json.dumps(fiche_actuelle, indent=2, ensure_ascii=False))
            print("----------------------------")

            # Ici on pourrait proposer de sauvegarder en base de données
            choix = input("Voulez-vous enregistrer ce membre ? (oui/non) : ")
            if choix.lower() == 'oui':
                if sauvegarder_contact(fiche_actuelle, est_modification=est_modification):
                    action = "mis à jour" if est_modification else "enregistré"
                    print(f"✓ {fiche_actuelle.get('nom', 'Contact')} {action} avec succès !")
                else:
                    print("✗ Erreur lors de l'enregistrement.")

            # On réinitialise pour une nouvelle personne
            historique_conversation = []
            fiche_actuelle = {}
            print("\nPrête pour une nouvelle saisie !")

if __name__ == "__main__":
    main() 
