"""
Modèles et structures de données pour les contacts et analyses.
"""

from typing import List, Optional, Dict, Any
from dataclasses import dataclass, asdict, field


@dataclass
class Contact:
    """Représentation d'un contact."""
    nom: str
    métiers: List[str] = field(default_factory=list)
    passions: List[str] = field(default_factory=list)
    projets: List[str] = field(default_factory=list)
    competences: List[str] = field(default_factory=list)
    etudes: Optional[str] = None
    email: Optional[str] = None
    numero: Optional[str] = None
    laboratoire: Optional[str] = None
    autres_infos: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convertit le contact en dictionnaire."""
        return {k: v for k, v in asdict(self).items() if v is not None and v != []}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Contact":
        """Crée un contact à partir d'un dictionnaire."""
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


@dataclass
class BesoinsAnalyse:
    """Résultat de l'analyse des besoins de l'IA."""
    competences_necessaires: List[str]
    synonymes: List[str]


@dataclass
class ExtractionResult:
    """Résultat de l'extraction d'informations par l'IA."""
    est_recherche: bool
    est_modification: bool = False
    contact: Optional[Contact] = None
    infos_manquantes: bool = False
    question_a_poser: Optional[str] = None
    terme_recherche: Optional[str] = None
    error: Optional[str] = None
