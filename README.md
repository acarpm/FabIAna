# FabIAna
Le système repose sur un agent IA local capable de gérer trois modes :

### 1. Saisie Intuitive & Interactive
L'IA agit comme un agent d'accueil. Elle ne se contente pas de stocker, elle analyse la complétude du profil. Si une information essentielle (ex: moyen de contact) est oubliée dans la conversation, l'IA relancera l'utilisateur pour enrichir la base.

### 2. Orientation de Projet (Matchmaking)
L'utilisateur décrit son idée ou son problème technique. Le système effectue une recherche vectorielle pour identifier les membres ayant les compétences adéquates et génère une recommandation personnalisée en expliquant *pourquoi* ce contact est pertinent.

### 3. Boucle de Rétroaction (Système de Réputation)
Pour garantir la qualité de l'entraide au sein du Fablab, les utilisateurs peuvent laisser des avis sur les échanges :
- **Réactivité :** Le contact répond-il rapidement ?
- **Efficacité :** L'aide a-t-elle permis d'avancer sur le projet ?
- **Savoir-être :** L'échange a-t-il été agréable ?
*Ces données permettent à l'IA de prioriser les membres les plus actifs et pédagogues dans ses recommandations futures.*

## 🛠️ Stack Technique visée
- **LLM :** Llama 3 (8B) via Ollama.
- **Orchestration :** LangChain ou LangGraph (pour gérer les questions de suivi de l'IA).
- **Base de données :** 
    - **ChromaDB :** Pour la recherche par compétences (Vector Store).
    - **SQLite :** Pour les profils détaillés et les notes de feedback.
- **Interface :** Streamlit ou Gradio (pour un prototypage rapide en Python).
