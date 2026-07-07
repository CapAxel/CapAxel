"""Modèles de données : commune à évaluer et résultat de scoring."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class DocumentUrbanisme(str, Enum):
    """Type de document d'urbanisme en vigueur dans la commune."""

    RNU = "RNU"    # Règlement national d'urbanisme (aucun document local)
    CC = "CC"      # Carte communale
    POS = "POS"    # Plan d'occupation des sols (caduc depuis 2020)
    PLU = "PLU"    # Plan local d'urbanisme communal
    PLUI = "PLUi"  # Plan local d'urbanisme intercommunal

    @classmethod
    def depuis_texte(cls, texte: str) -> "DocumentUrbanisme":
        valeur = texte.strip().upper()
        if not valeur:
            return cls.RNU
        for membre in cls:
            if membre.value.upper() == valeur:
                return membre
        raise ValueError(
            f"Document d'urbanisme inconnu : {texte!r} "
            f"(attendu : {', '.join(m.value for m in cls)})"
        )


@dataclass
class Commune:
    """Une commune candidate au démarchage."""

    code_insee: str
    nom: str
    population: int
    evolution_population_pct: float        # évolution sur ~5 ans, en %
    logements_autorises_3ans: int          # logements autorisés sur 3 ans (Sitadel)
    document_urbanisme: DocumentUrbanisme
    annee_approbation: int | None = None   # année d'approbation du document en vigueur
    competence_plu_epci: bool = False      # compétence PLU transférée à l'EPCI
    epci: str = ""
    distance_agence_km: float | None = None


@dataclass
class ScoreCommune:
    """Résultat du scoring d'une commune."""

    commune: Commune
    score: float                                # score global, 0 à 100
    details: dict[str, float] = field(default_factory=dict)  # note 0-1 par critère
    priorite: str = ""
