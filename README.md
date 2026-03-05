# FabIAna - Assistante Base de Connaissances

Assistant IA pour la gestion d'une base de connaissances de personnes et leurs compétences au sein de CampusFab, le fablab de l'Université de Toulouse.

**✨ Nouveau** : Base de données SQLite (campusfab.db) au lieu de JSON ! 🗄️

## 📁 Structure du Projet

```
ollama/
├── main.py                 # Point d'entrée de l'application
├── config.py              # Configuration globale
├── models.py              # Modèles et structures de données
├── database_sqlite.py     # Gestion BD SQLite ⭐ NOUVEAU
├── ai_service.py          # Intégration avec l'IA Ollama
├── search.py              # Moteur de recherche intelligent
├── ui.py                  # Interface utilisateur
├── migrate.py             # Migration JSON → SQLite ⭐ NOUVEAU
├── admin.py               # Administration BD ⭐ NOUVEAU
├── campusfab.db           # Base de données SQLite ⭐ NOUVEAU
├── README.md              # Ce fichier
├── DATABASE_MIGRATION.md  # Guide migration ⭐ NOUVEAU
└── requirements.txt       # Dépendances Python
```

## 🏗️ Architecture Modulaire

### 1. **config.py**
Configuration centralisée de l'application :
- Modèle IA utilisé
- Chemin de la base de données (campusfab.db)
- Paramètres d'IA

### 2. **models.py**
Definitions des structures de données :
- `Contact` : Représentation d'une personne
- `BesoinsAnalyse` : Résultats de l'analyse des besoins
- `ExtractionResult` : Résultats de l'extraction d'informations

### 3. **database_sqlite.py** ⭐
Gestion de la persistance SQLite :
- `charger_contacts()` : Charge tous les contacts
- `sauvegarder_contact()` : Ajoute ou met à jour un contact
- `obtenir_noms_contacts()` : Liste les noms disponibles
- `supprimer_contact()` : Supprime un contact
- `obtenir_statistiques()` : Stats de la BD

### 4. **ai_service.py**
Service d'intégration avec Ollama :
- `analyser_besoins()` : Analyse une demande utilisateur
- `extraire_informations()` : Extrait les infos d'une conversation

### 5. **search.py**
Moteur de recherche intelligent :
- `chercher_personnes()` : Trouve les personnes correspondant à des critères
- Note les résultats par pertinence

### 6. **ui.py**
Interface utilisateur et logique métier :
- `boucle_principale()` : Boucle interactive
- `afficher_contact()` : Affichage formaté des contacts
- Traitement des recherches et des saisies

### 7. **main.py**
Point d'entrée unique de l'application.

### 8. **migrate.py** ⭐
Migration des données JSON → SQLite :
- Convertit contacts.json en campusfab.db
- À lancer une seule fois

### 9. **admin.py** ⭐
Outil d'administration de la BD :
- Afficher les statistiques
- Lister/Détailler les contacts
- Supprimer/Nettoyer la BD
- Exporter en JSON

## 🚀 Installation et Utilisation

### Prérequis
- Python 3.8+
- Ollama avec le modèle `llama3:8b` installé

### Installation

```bash
# Cloner ou télécharger le projet
cd ollama

# Installer les dépendances
pip install -r requirements.txt
```

### Première Utilisation - Migration Données

Si vous avez un ancien fichier `contacts.json`, migrez-le vers SQLite :

```bash
# ⚠️ À faire UNE SEULE FOIS
python3 migrate.py
```

Cela va :
- ✅ Créer campusfab.db
- ✅ Importer les données de contacts.json
- ✅ Backup de contacts.json en contacts.json.backup

### Lancer l'Application

```bash
python3 main.py
```

### Administrer la Base de Données

```bash
python3 admin.py
```

Menu interactif pour gérer la BD.

## 🗄️ Base de Données SQLite

La migration vers SQLite apporte :

✅ **Performance** : 10-100x plus rapide  
✅ **Intégrité** : Constraints et validations  
✅ **Scalabilité** : Prête pour des milliers de contacts  
✅ **Atomicité** : Transactions ACID  
✅ **Monitoring** : Statistiques en temps réel

Pour plus de détails, consultez [DATABASE_MIGRATION.md](DATABASE_MIGRATION.md).

### Lancer l'application

```bash
python main.py
```

## 💡 Fonctionnalités

### 1. Ajouter une personne
Décrivez une personne naturellement et l'IA extrait les informations structurées.

```
Vous : Je voudrais enregistrer Jean qui est développeur Python avec 5 ans d'expérience
```

### 2. Chercher une personne
Recherchez des personnes selon des critères de compétences, métiers, passions, etc.

```
Vous : J'ai besoin de quelqu'un qui maîtrise la CAO
```

## 📊 Avantages de cette Architecture

✅ **Maintenabilité** : Chaque module a une responsabilité unique  
✅ **Scalabilité** : Facile d'ajouter de nouvelles fonctionnalités  
✅ **Testabilité** : Chaque module peut être testé indépendamment  
✅ **Réutilisabilité** : Les modules peuvent être importés séparément  
✅ **Compréhensibilité** : Code clair avec une structure logique  

## 🔄 Flux de l'Application

```
main.py
  ↓
ui.boucle_principale()
  ├─ Lecture de l'entrée utilisateur
  ├─ ai_service.extraire_informations()
  │   └─ Appel Ollama
  ├─ Vérification si recherche
  │   └─ search.chercher_personnes()
  ├─ Vérification si info contact
  │   └─ database.sauvegarder_contact()
  └─ Affichage des résultats
```

## 📝 Exemple d'Utilisation

```python
from models import Contact
from database import sauvegarder_contact
from search import chercher_personnes

# Créer un contact
contact = Contact(
    nom="Alice",
    métiers=["Développeuse"],
    competences=["Python", "JavaScript"],
    email="alice@example.com"
)

# Sauvegarder
sauvegarder_contact(contact)

# Chercher
resultats = chercher_personnes("quelqu'un qui code en Python")
for r in resultats:
    print(r.nom)
```

## 🛠️ Extensions Futures

- Ajouter des tests unitaires
- Créer une API REST
- Ajouter une interface web
- Implémenter un système de permissions
- Ajouter un historique des modifications
- Exporter les données (CSV, PDF)
