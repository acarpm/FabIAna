# Architecture de FabIAna

## 📐 Diagramme de Dépendances

```
main.py
  └─ ui.py (Interface Utilisateur)
      ├─ ai_service.py (Service IA)
      │   ├─ config.py
      │   ├─ models.py
      │   └─ database.py
      ├─ search.py (Moteur de Recherche)
      │   ├─ models.py
      │   ├─ database.py
      │   └─ ai_service.py
      └─ database.py (Base de Données)
          └─ models.py
              └─ config.py
```

## 🔀 Flux d'Exécution

### Cas 1 : Ajouter un Contact

```
1. ui.boucle_principale()
   - Lit l'entrée utilisateur
   
2. ai_service.extraire_informations()
   - Envoie la conversation à Ollama
   - Reçoit une structure JSON structurée
   - Crée un objet Contact
   
3. ui.demander_enregistrement()
   - Affiche la fiche
   - Demande confirmation
   
4. database.sauvegarder_contact()
   - Charge contacts.json
   - Fusionne ou ajoute le contact
   - Sauvegarde dans contacts.json
```

### Cas 2 : Chercher un Contact

```
1. ui.boucle_principale()
   - Lit : "J'ai besoin de quelqu'un qui sait Python"
   
2. ai_service.extraire_informations()
   - Détecte est_recherche=true
   - Retourne terme_recherche
   
3. search.chercher_personnes()
   - ai_service.analyser_besoins()
     - IA analyse les compétences nécessaires
   - database.charger_contacts()
     - Charge tous les contacts
   - Scoring (algorithme de pertinence)
   - Retourne résultats triés
   
4. ui.afficher_resultats_recherche()
   - Affiche les résultats
```

## 📊 Modèles de Données

### Contact
```python
Contact
├── nom: str (clé unique)
├── études: str | None
├── métiers: list[str]
├── passions: list[str]
├── projets: list[str]
├── compétences: list[str]
├── email: str | None
├── numero: str | None
├── laboratoire: str | None
└── autres_infos: str | None
```

### BesoinsAnalyse
```python
BesoinsAnalyse
├── compétences_nécessaires: list[str]
└── synonymes: list[str]
```

### ExtractionResult
```python
ExtractionResult
├── est_recherche: bool
├── est_modification: bool
├── contact: Contact | None
├── infos_manquantes: bool
├── question_a_poser: str | None
├── terme_recherche: str | None
└── error: str | None
```

## 🎯 Responsabilités par Module

| Module | Responsabilité | Dépend de |
|--------|-----------------|-----------|
| main.py | Point d'entrée | ui |
| config.py | Configuration | aucun |
| models.py | Structures de données | aucun |
| database.py | Persistance (JSON) | models, config |
| ai_service.py | Intégration Ollama | models, database, config |
| search.py | Recherche intelligente | models, database, ai_service |
| ui.py | Interface utilisateur | Tous |

## 💾 Format de Stockage (contacts.json)

```json
[
  {
    "nom": "Alice",
    "métiers": ["Développeuse"],
    "competences": ["Python", "JavaScript"],
    "passions": ["IA"],
    "projets": [],
    "email": "alice@example.com",
    "numero": "06...",
    "etudes": "Master Informatique",
    "laboratoire": null,
    "autres_infos": "Aime le café"
  }
]
```

## 🧮 Algorithme de Recherche

Le scoring utilise une pondération par catégorie :

```
Score = Σ (Correspondance × Poids)

Où :
- Compétences : poids = 3
- Métiers : poids = 2
- Passions : poids = 1.5
- Projets : poids = 1.5
- Synonymes : poids = 1-2

Les résultats sont triés par score décroissant.
```

## 📈 Points d'Extension

### Pour ajouter une nouvelle source de données
1. Créer `new_source.py`
2. Implémenter `charger_from_source()`
3. Convertir en List[Contact]
4. Merger dans database.py

### Pour ajouter un nouveau champ à Contact
1. Ajouter le champ à `models.py` dans la classe Contact
2. Mettre à jour le prompt IA dans `ai_service.py`
3. Les autres modules s'adaptent automatiquement via dataclass

### Pour changer la base de données
1. Créer `database_sql.py` ou `database_mongodb.py`
2. Implémenter les mêmes interfaces que `database.py`
3. Changer l'import dans `ui.py`

## ⚙️ Configuration Recommandée pour la Production

```python
# config.py - Mode Production
MODEL = "llama3:70b"  # Plus puissant
CONTACTS_FILE = "/var/data/contacts.json"  # Chemin sécurisé
AI_CONFIG = {
    "temperature": 0.3,  # Plus précis
    "timeout": 30
}
```

## 🔒 Sécurité

- Validation des entrées utilisateur : À implémenter
- Sauvegarde des fichiers : Utiliser des transactions
- Gestion d'erreurs : À renforcer
- Authentification/Autorisation : À ajouter

## 📊 Scalabilité

| Nombre de contacts | Recommandation |
|-------------------|-----------------|
| < 100 | JSON suffisant |
| 100 - 10k | SQLite recommandé |
| 10k - 1M | PostgreSQL |
| > 1M | Elasticsearch + PostgreSQL |

## 🎓 Améliorations Futures

1. **Persistance** : Migrer vers SQLite/PostgreSQL
2. **API** : FastAPI pour interface programmatique
3. **Frontend** : Interface web avec React
4. **Cache** : Redis pour les recherches fréquentes
5. **Événements** : Système de notification
6. **Versioning** : Historique des modifications
7. **Analytics** : Suivi des recherches/usages
