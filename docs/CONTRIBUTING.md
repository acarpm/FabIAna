# Guide de Contribution et Développement

## 🔧 Ajouter une Nouvelle Fonctionnalité

### 1. Ajouter un nouveau modèle de données
Modifiez `models.py` :
```python
from dataclasses import dataclass, field

@dataclass
class MonModele:
    champ1: str
    champ2: list = field(default_factory=list)
```

### 2. Ajouter une nouvelle fonction métier
Créez un nouveau module `nom_feature.py` ou ajoutez dans le module existant pertinent.

Respectez la séparation des responsabilités :
- **database.py** : Opérations sur la BD
- **ai_service.py** : Intégration IA
- **search.py** : Recherche et filtrage
- **ui.py** : Affichage et interaction utilisateur

### 3. Mettre à jour l'interface
Modifiez `ui.py` pour ajouter les appels à votre nouvelle fonction.

## 🧪 Tester votre code

```bash
# Compiler pour vérifier la syntaxe
python3 -m py_compile *.py

# Importer et tester manuellement
python3
>>> from models import Contact
>>> c = Contact(nom="Test")
>>> print(c)
```

## 📚 Conventions de Code

- **Noms de fonctions** : snake_case (`ma_fonction`)
- **Noms de classes** : PascalCase (`MaClasse`)
- **Constantes** : UPPER_CASE (`MA_CONSTANTE`)
- **Docstrings** : Utilisez le format Google
- **Types** : Utilisez les type hints

## 🔐 Bonnes Pratiques

1. Une fonction = une responsabilité
2. Utilisez les type hints
3. Documentez avec des docstrings
4. Gérez les exceptions explicitement
5. Validez les entrées utilisateur
6. Ne modifiez pas les fichiers configs directement en prod

## 📦 Ajouter une Dépendance

1. Modifiez `requirements.txt`
2. Installez localement : `pip install -r requirements.txt`
3. Mentionnez-le dans le README

## 🐛 Déboguer

Les logs sont affichés directement. Pour plus de détails :

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("Message de debug")
logger.error("Message d'erreur")
```

## 📈 Performance

- Les fichiers JSON sont rechargés à chaque opération
- Pour 1000+ contacts, envisagez une BD (SQLite, PostgreSQL)
- Le cache IA peut être implémenté dans `ai_service.py`

## 🔄 Refactoring

Si vous divisez un module trop gros :
1. Créez un nouveau module
2. Déplacez les fonctions
3. Mettez à jour les imports dans les autres modules
4. Testez le code complet

## 📞 Support

Consultez le README.md pour la documentation générale.
