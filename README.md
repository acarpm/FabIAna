# 📚🤖 Base de Connaissances IA – Gestion des Contacts CampusFab

## 🚀 Description du projet

Ce projet vise à développer une **base de connaissances interactive** intégrant une **Intelligence Artificielle (LLM)** afin de faciliter l’enregistrement et la recherche d’informations sur les personnes en lien avec l’association CampusFab (Fablab UT).

L’application sera installée **localement** sur une machine équipée d’un **accélérateur/processeur IA (GPU, NPU, etc.)** pour faire tourner un modèle de langage (LLM) en local.

---

## 🎯 Objectif

Créer un logiciel permettant de :

- 📌 Enregistrer efficacement des informations sur des personnes
- 🔎 Rechercher des profils selon leurs compétences, projets ou centres d’intérêt
- 💬 Interagir via un chat intelligent pour simplifier la saisie et la consultation des données
- 🔐 Garantir que les données restent locales (aucun envoi vers des serveurs externes)

---

## 🏫 Contexte

Au sein de **CampusFab (Fablab UT)**, nous accueillons régulièrement :

- Des étudiants
- Des passionnés
- Des porteurs de projets
- Des experts techniques

Ces personnes :
- Possèdent des compétences variées
- Participent à de nombreux projets
- Souhaitent contribuer à la communauté

### ❗ Problème actuel

Les informations sur ces personnes :

- ❌ Ne sont pas stockées de manière structurée
- ❌ Ne sont pas facilement accessibles
- ❌ Ne sont pas partagées uniformément entre les membres

👉 D’où la nécessité d’une base de connaissances centralisée et intelligente.

---

## 🧠 Rôle de l’IA (LLM)

L’intégration d’un **modèle de langage (LLM)** permet :

- Une saisie naturelle via un chat
- Une structuration automatique des informations
- Une recherche intelligente en langage naturel

### 💬 Exemple d’utilisation

Utilisateur :
> "J'ai connu Alexandru Carp ! Il est étudiant en génie électrique et informatique industrielle. Il aime bien travailler sur des projets d’informatique embarquée."

L’IA va automatiquement :

- Identifier le nom
- Extraire le domaine d’études
- Détecter les compétences
- Enregistrer les centres d’intérêt
- Structurer les données dans la base

Sans formulaire complexe ✨

---

## 🏗️ Architecture Générale

```
Utilisateur
    ↓
Interface Chat
    ↓
LLM local
    ↓
Module d'extraction d'informations
    ↓
Base de données structurée
```

---

## ⚙️ Fonctionnalités prévues

### 📝 Enregistrement intelligent
- Ajout de personnes via discussion naturelle
- Correction et enrichissement automatique des fiches

### 🔍 Recherche intelligente
Exemples :
- "Qui s’y connaît en informatique embarquée ?"
- "Qui a déjà travaillé sur un projet Arduino ?"
- "Liste les étudiants en génie électrique"

### 📊 Gestion des profils
Chaque personne peut contenir :
- Nom
- Formation
- Compétences
- Projets réalisés
- Disponibilité
- Niveau d’expertise
- Notes internes

---

## 💻 Installation prévue

Le logiciel sera conçu pour fonctionner :

- 🖥️ En local
- 🔐 Sans connexion obligatoire à Internet
- ⚡ Sur machine équipée d’un accélérateur IA (GPU recommandé)

### Technologies envisagées (exemple)

- Backend : Python
- LLM local : (à définir — ex: Llama, Mistral, etc.)
- Base de données : SQLite / PostgreSQL
- Interface : Web locale (Flask, FastAPI ou autre)

---

## 🔒 Confidentialité & Éthique

- Les données restent locales
- Aucun partage externe sans consentement
- Respect du RGPD
- Transparence sur le fonctionnement de l’IA

---

## 📈 Vision à long terme

- Amélioration continue du modèle
- Statistiques sur les compétences disponibles
- Mise en relation automatique de profils avec des projets
- Export sécurisé des données
- Interface multi-utilisateurs

---

## 🤝 Contribution

Ce projet est développé par l’association CampusFab.

Toute contribution est la bienvenue :

- Développement backend
- Interface utilisateur
- Optimisation LLM
- Sécurité des données
- Documentation

---

## 📜 Licence

À définir (MIT, GPL, etc.)

---

## ✨ Résumé

Ce projet vise à créer une **base de connaissances intelligente, locale et sécurisée**, permettant à CampusFab de :

- Mieux valoriser les compétences
- Faciliter la collaboration
- Centraliser les informations
- Simplifier la gestion des contacts grâce à l’IA

---

💡 *Une communauté forte commence par une meilleure organisation de ses talents.*
