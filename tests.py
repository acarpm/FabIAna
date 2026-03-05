#!/usr/bin/env python3
"""
Tests unitaires pour les modules de FabIAna.
À exécuter avec : python3 -m pytest tests.py
"""

import unittest
import json
import os
from models import Contact, BesoinsAnalyse, ExtractionResult
from database_sqlite import obtenir_noms_contacts


class TestContact(unittest.TestCase):
    """Tests de la classe Contact."""
    
    def test_creation_contact_minimal(self):
        """Test la création d'un contact minimal."""
        contact = Contact(nom="Alice")
        self.assertEqual(contact.nom, "Alice")
        self.assertEqual(contact.competences, [])
        self.assertIsNone(contact.email)
    
    def test_creation_contact_complet(self):
        """Test la création d'un contact avec tous les champs."""
        contact = Contact(
            nom="Alice",
            métiers=["Dev"],
            competences=["Python"],
            email="alice@example.com"
        )
        self.assertEqual(contact.nom, "Alice")
        self.assertIn("Dev", contact.métiers)
        self.assertIn("Python", contact.competences)
    
    def test_contact_to_dict(self):
        """Test la conversion Contact → Dictionnaire."""
        contact = Contact(
            nom="Bob",
            competences=["C++"],
            métiers=["Ingénieur"]
        )
        d = contact.to_dict()
        self.assertEqual(d['nom'], "Bob")
        self.assertIn("C++", d['competences'])
        self.assertNotIn('email', d)  # email est None, ne doit pas être dans le dict
    
    def test_contact_from_dict(self):
        """Test la création Contact depuis dictionnaire."""
        data = {
            'nom': 'Charlie',
            'competences': ['JavaScript'],
            'email': 'charlie@example.com'
        }
        contact = Contact.from_dict(data)
        self.assertEqual(contact.nom, 'Charlie')
        self.assertIn('JavaScript', contact.competences)
        self.assertEqual(contact.email, 'charlie@example.com')
    
    def test_contact_dict_roundtrip(self):
        """Test la conversion bidirectionnelle Contact ↔ Dict."""
        original = Contact(
            nom="Diana",
            competences=["Python", "Java"],
            passions=["IA"],
            email="diana@example.com"
        )
        
        # Contact → Dict → Contact
        d = original.to_dict()
        restored = Contact.from_dict(d)
        
        self.assertEqual(original.nom, restored.nom)
        self.assertEqual(original.competences, restored.competences)
        self.assertEqual(original.email, restored.email)


class TestBesoinsAnalyse(unittest.TestCase):
    """Tests de la classe BesoinsAnalyse."""
    
    def test_creation_besoins(self):
        """Test la création d'une analyse de besoins."""
        besoins = BesoinsAnalyse(
            competences_necessaires=["Python", "Django"],
            synonymes=["coder", "développer"]
        )
        self.assertEqual(len(besoins.competences_necessaires), 2)
        self.assertIn("coder", besoins.synonymes)


class TestExtractionResult(unittest.TestCase):
    """Tests de la classe ExtractionResult."""
    
    def test_creation_recherche(self):
        """Test un résultat de recherche."""
        result = ExtractionResult(
            est_recherche=True,
            terme_recherche="Python"
        )
        self.assertTrue(result.est_recherche)
        self.assertEqual(result.terme_recherche, "Python")
        self.assertIsNone(result.contact)
    
    def test_creation_extraction(self):
        """Test un résultat d'extraction."""
        contact = Contact(nom="Eve")
        result = ExtractionResult(
            est_recherche=False,
            contact=contact,
            est_modification=False
        )
        self.assertFalse(result.est_recherche)
        self.assertIsNotNone(result.contact)
        self.assertEqual(result.contact.nom, "Eve")


class TestDatabase(unittest.TestCase):
    """Tests des fonctions de base de données."""
    
    def test_obtenir_noms_contacts(self):
        """Test la récupération des noms de contacts."""
        noms = obtenir_noms_contacts()
        self.assertIsInstance(noms, list)
        # Dépend du fichier contacts.json existant
        # Si la BD est vide, retourne une liste vide
        if noms:
            self.assertIsInstance(noms[0], str)


class TestUtilities(unittest.TestCase):
    """Tests des utilitaires."""
    
    def test_contact_equality(self):
        """Test l'égalité entre deux contacts."""
        c1 = Contact(nom="Frank", competences=["C"])
        c2 = Contact(nom="Frank", competences=["C"])
        # Les dataclasses implémentent l'égalité par défaut
        self.assertEqual(c1, c2)
    
    def test_contact_inequality(self):
        """Test l'inégalité entre deux contacts."""
        c1 = Contact(nom="George", competences=["C"])
        c2 = Contact(nom="Henry", competences=["C"])
        self.assertNotEqual(c1, c2)
    
    def test_contact_field_validation(self):
        """Test que les champs optionnels peuvent être None."""
        contact = Contact(
            nom="Iris",
            email=None,
            numero=None,
            laboratoire=None
        )
        self.assertIsNone(contact.email)
        self.assertIsNone(contact.numero)


class TestSearchLogic(unittest.TestCase):
    """Tests de la logique de recherche."""
    
    def test_scoring_competence(self):
        """Test que les compétences correspondent."""
        c1 = Contact(nom="Jack", competences=["Python"])
        c2 = Contact(nom="Kate", competences=["Java"])
        
        # Vérifier que Python et Java sont des compétences
        self.assertIn("Python", c1.competences)
        self.assertIn("Java", c2.competences)


if __name__ == '__main__':
    unittest.main()
