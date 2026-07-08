"""Modèles de données : commune, indicateurs historiques et résultat d'analyse."""

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
    INCONNU = "?"  # Non renseigné

    @classmethod
    def depuis_texte(cls, texte: str) -> "DocumentUrbanisme":
        valeur = texte.strip().upper()
        if not valeur or valeur == "?":
            return cls.INCONNU
        for membre in cls:
            if membre.value.upper() == valeur:
                return membre
        raise ValueError(
            f"Document d'urbanisme inconnu : {texte!r} "
            f"(attendu : {', '.join(m.value for m in cls if m is not cls.INCONNU)})"
        )


@dataclass
class Commune:
    """Une commune et ses indicateurs, collectés (INSEE, SIRENE) ou saisis.

    Les champs « _prec » correspondent au recensement précédent (~5-6 ans
    avant) et « _anc » à celui d'avant (~10-11 ans), pour mesurer les
    trajectoires. Un champ à None signifie « donnée non disponible ».
    """

    code_insee: str
    nom: str
    epci: str = ""

    # Démographie (recensements INSEE successifs)
    population: int | None = None
    population_prec: int | None = None
    population_anc: int | None = None
    annee_recensement: int | None = None

    # Habitat (série historique INSEE : parc total, vacants, secondaires)
    logements: float | None = None
    logements_vacants: float | None = None
    residences_secondaires: float | None = None
    logements_prec: float | None = None
    logements_vacants_prec: float | None = None

    # Emploi au lieu de travail (recensement INSEE)
    emplois: float | None = None
    emplois_prec: float | None = None

    # Tissu économique (SIRENE via recherche-entreprises.api.gouv.fr)
    nb_etablissements: int | None = None
    nb_commerces: int | None = None

    # Données à saisir manuellement (pas d'open data national fiable)
    taux_vacance_commerciale: float | None = None  # en %, relevé terrain / CCI
    logements_autorises_3ans: int | None = None    # Sitadel
    document_urbanisme: DocumentUrbanisme = DocumentUrbanisme.INCONNU
    annee_approbation: int | None = None
    competence_plu_epci: bool = False

    # --- Indicateurs dérivés -------------------------------------------------

    @staticmethod
    def _evolution_pct(actuel: float | None, avant: float | None) -> float | None:
        if actuel is None or avant is None or avant <= 0:
            return None
        return (actuel - avant) / avant * 100.0

    @property
    def evolution_population_pct(self) -> float | None:
        """Évolution de la population entre les deux derniers recensements (%)."""
        return self._evolution_pct(self.population, self.population_prec)

    @property
    def evolution_population_longue_pct(self) -> float | None:
        """Évolution de la population sur ~10 ans (%)."""
        return self._evolution_pct(self.population, self.population_anc)

    @property
    def taux_vacance_logement(self) -> float | None:
        """Part de logements vacants dans le parc (%)."""
        if self.logements_vacants is None or not self.logements:
            return None
        return self.logements_vacants / self.logements * 100.0

    @property
    def taux_vacance_logement_prec(self) -> float | None:
        if self.logements_vacants_prec is None or not self.logements_prec:
            return None
        return self.logements_vacants_prec / self.logements_prec * 100.0

    @property
    def evolution_vacance_points(self) -> float | None:
        """Évolution du taux de vacance entre deux recensements (points de %)."""
        actuel, avant = self.taux_vacance_logement, self.taux_vacance_logement_prec
        if actuel is None or avant is None:
            return None
        return actuel - avant

    @property
    def evolution_emplois_pct(self) -> float | None:
        """Évolution de l'emploi au lieu de travail (%).

        Non calculée sous 20 emplois : sur de si petits effectifs, la
        variation entre deux recensements relève du bruit statistique.
        """
        if self.emplois_prec is not None and self.emplois_prec < 20:
            return None
        return self._evolution_pct(self.emplois, self.emplois_prec)

    @property
    def commerces_pour_1000_hab(self) -> float | None:
        if self.nb_commerces is None or not self.population:
            return None
        return self.nb_commerces / self.population * 1000.0


@dataclass
class AnalyseCommune:
    """Résultat de l'analyse : un score 0-100 par axe de besoin."""

    commune: Commune
    axes: dict[str, float | None] = field(default_factory=dict)
    besoin_principal: str = ""
    score_global: float = 0.0
    priorite: str = ""
