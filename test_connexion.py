import ollama

try:
    print("Connexion à Llama 3 en cours...")
    response = ollama.chat(model='llama3:8b', messages=[
        {'role': 'user', 'content': 'Dis "Système prêt" en une phrase.'},
    ])
    print("Réponse de l'IA :", response['message']['content'])
    print("\n✅ Tout est configuré correctement !")
except Exception as e:
    print("\n❌ Erreur : Assure-tu qu'Ollama est bien lancé.")
    print(e)