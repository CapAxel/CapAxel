"""Modèles de données : commune, indicateurs historiques et résultat d'analyse."""

from __future__ import annotations

from dataclasses import dataclass, field


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
    residences_secondaires_prec: float | None = None
    part_logements_avant_1946: float | None = None  # % des rés. principales

    # Vieillissement (structure par âge, recensement INSEE)
    part_65plus: float | None = None       # % de la population, dernier RP
    part_65plus_prec: float | None = None  # même part au RP précédent
    part_80plus: float | None = None       # % de la population, dernier RP

    # Emploi au lieu de travail (recensement INSEE)
    emplois: float | None = None
    emplois_prec: float | None = None

    # Tissu économique (SIRENE via recherche-entreprises.api.gouv.fr)
    nb_etablissements: int | None = None
    nb_commerces: int | None = None

    # Tourisme (INSEE DS_TOUR_CAP + détection SIRENE)
    lits_touristiques: int | None = None    # lits en hébergements marchands
    office_tourisme: bool | None = None     # un office de tourisme est présent

    # Marché immobilier (DVF, mutations géolocalisées)
    prix_m2: float | None = None            # médiane €/m², millésime récent
    prix_m2_prec: float | None = None       # médiane €/m², ~4 ans avant

    # Données à saisir manuellement (pas d'open data national fiable)
    taux_vacance_commerciale: float | None = None  # en %, relevé terrain / CCI
    logements_autorises_3ans: int | None = None    # Sitadel

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

    @property
    def part_residences_secondaires(self) -> float | None:
        """Part de résidences secondaires dans le parc (%)."""
        if self.residences_secondaires is None or not self.logements:
            return None
        return self.residences_secondaires / self.logements * 100.0

    @property
    def part_residences_secondaires_prec(self) -> float | None:
        if self.residences_secondaires_prec is None or not self.logements_prec:
            return None
        return self.residences_secondaires_prec / self.logements_prec * 100.0

    @property
    def evolution_res_secondaires_points(self) -> float | None:
        """Évolution de la part de résidences secondaires (points de %)."""
        actuel = self.part_residences_secondaires
        avant = self.part_residences_secondaires_prec
        if actuel is None or avant is None:
            return None
        return actuel - avant

    @property
    def evolution_part_65plus_points(self) -> float | None:
        """Évolution de la part des 65 ans et plus (points de %)."""
        if self.part_65plus is None or self.part_65plus_prec is None:
            return None
        return self.part_65plus - self.part_65plus_prec

    @property
    def lits_touristiques_pour_100_hab(self) -> float | None:
        if self.lits_touristiques is None or not self.population:
            return None
        return self.lits_touristiques / self.population * 100.0

    @property
    def evolution_prix_m2_pct(self) -> float | None:
        """Évolution de la médiane de prix au m² entre deux millésimes DVF (%)."""
        return self._evolution_pct(self.prix_m2, self.prix_m2_prec)


@dataclass
class AnalyseCommune:
    """Résultat de l'analyse : un score 0-100 par axe de besoin."""

    commune: Commune
    axes: dict[str, float | None] = field(default_factory=dict)
    besoin_principal: str = ""
    score_global: float = 0.0
    priorite: str = ""
