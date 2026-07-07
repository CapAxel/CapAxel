"""Moteur de scoring : notes par critère, pondérations et tri des communes.

Chaque critère renvoie une note entre 0 et 1 ; le score global est la moyenne
pondérée de ces notes, ramenée sur 100. Les pondérations par défaut reflètent
le fait que l'état du document d'urbanisme est le meilleur prédicteur d'un
besoin d'étude à court terme.
"""

from __future__ import annotations

from datetime import date

from .modeles import Commune, DocumentUrbanisme, ScoreCommune

POIDS_DEFAUT: dict[str, float] = {
    "document_urbanisme": 0.35,
    "dynamique_construction": 0.20,
    "dynamique_demographique": 0.15,
    "taille_commune": 0.15,
    "proximite_agence": 0.15,
}

SEUIL_PRIORITAIRE = 65.0
SEUIL_A_SUIVRE = 45.0

# Facteur appliqué quand la compétence PLU est à l'EPCI : la commune ne
# commande plus seule son document, le vrai prospect devient l'intercommunalité.
FACTEUR_COMPETENCE_EPCI = 0.4


def _borner(valeur: float) -> float:
    return max(0.0, min(1.0, valeur))


def note_document_urbanisme(commune: Commune, annee_reference: int) -> float:
    """Opportunité liée au document d'urbanisme en vigueur.

    POS caduc ou RNU : élaboration d'un PLU très probable. PLU pré-ALUR
    (> 13 ans) : révision attendue. Document récent : besoin faible.
    """
    doc = commune.document_urbanisme
    age = (
        annee_reference - commune.annee_approbation
        if commune.annee_approbation is not None
        else None
    )

    if doc is DocumentUrbanisme.POS:
        note = 1.0
    elif doc is DocumentUrbanisme.RNU:
        note = 0.95
    elif doc is DocumentUrbanisme.CC:
        # Une carte communale ancienne pousse souvent au passage en PLU.
        note = 0.85 if age is None or age >= 10 else 0.6
    elif doc is DocumentUrbanisme.PLU:
        if age is None or age >= 13:
            note = 0.9
        elif age >= 9:  # l'évaluation obligatoire à 9 ans rouvre le sujet
            note = 0.7
        elif age >= 6:
            note = 0.4
        else:
            note = 0.15
    else:  # PLUi : la révision se joue à l'échelle de l'EPCI
        if age is None or age >= 9:
            note = 0.5
        elif age >= 6:
            note = 0.3
        else:
            note = 0.05

    if commune.competence_plu_epci and doc is not DocumentUrbanisme.PLUI:
        note *= FACTEUR_COMPETENCE_EPCI

    return _borner(note)


def note_dynamique_demographique(commune: Commune) -> float:
    """Croissance de population sur ~5 ans : -2 % → 0, +8 % → 1."""
    return _borner((commune.evolution_population_pct + 2.0) / 10.0)


def note_dynamique_construction(commune: Commune) -> float:
    """Logements autorisés sur 3 ans pour 1 000 habitants : 0 → 0, 15 → 1."""
    if commune.population <= 0:
        return 0.0
    taux = commune.logements_autorises_3ans / commune.population * 1000.0
    return _borner(taux / 15.0)


def note_taille_commune(commune: Commune) -> float:
    """Courbe en cloche : la cible idéale fait entre ~500 et 5 000 habitants."""
    pop = commune.population
    if pop < 200:
        return 0.2
    if pop < 500:
        return 0.5
    if pop < 1000:
        return 0.8
    if pop <= 5000:
        return 1.0
    if pop <= 20000:
        return 0.7
    return 0.4


def note_proximite_agence(commune: Commune) -> float:
    """Distance à l'agence : ≤ 20 km → 1, ≥ 120 km → 0, inconnue → 0.5."""
    distance = commune.distance_agence_km
    if distance is None:
        return 0.5
    return _borner(1.0 - (distance - 20.0) / 100.0)


CRITERES = {
    "document_urbanisme": None,  # traité à part (a besoin de l'année de référence)
    "dynamique_construction": note_dynamique_construction,
    "dynamique_demographique": note_dynamique_demographique,
    "taille_commune": note_taille_commune,
    "proximite_agence": note_proximite_agence,
}


def _normaliser_poids(poids: dict[str, float] | None) -> dict[str, float]:
    if poids is None:
        return dict(POIDS_DEFAUT)
    inconnus = set(poids) - set(POIDS_DEFAUT)
    if inconnus:
        raise ValueError(
            f"Critères inconnus dans les pondérations : {', '.join(sorted(inconnus))}"
        )
    complets = {**POIDS_DEFAUT, **poids}
    total = sum(complets.values())
    if total <= 0:
        raise ValueError("La somme des pondérations doit être strictement positive.")
    return {nom: valeur / total for nom, valeur in complets.items()}


def priorite_depuis_score(score: float) -> str:
    if score >= SEUIL_PRIORITAIRE:
        return "À démarcher en priorité"
    if score >= SEUIL_A_SUIVRE:
        return "À suivre"
    return "Faible intérêt"


def calculer_score(
    commune: Commune,
    poids: dict[str, float] | None = None,
    annee_reference: int | None = None,
) -> ScoreCommune:
    """Calcule le score global (0-100) et le détail par critère d'une commune."""
    poids_normalises = _normaliser_poids(poids)
    annee = annee_reference if annee_reference is not None else date.today().year

    details = {"document_urbanisme": note_document_urbanisme(commune, annee)}
    for nom, fonction in CRITERES.items():
        if fonction is not None:
            details[nom] = fonction(commune)

    score = 100.0 * sum(details[nom] * poids_normalises[nom] for nom in details)
    return ScoreCommune(
        commune=commune,
        score=round(score, 1),
        details={nom: round(valeur, 3) for nom, valeur in details.items()},
        priorite=priorite_depuis_score(score),
    )


def trier_communes(
    communes: list[Commune],
    poids: dict[str, float] | None = None,
    annee_reference: int | None = None,
) -> list[ScoreCommune]:
    """Score toutes les communes et les renvoie triées par intérêt décroissant."""
    scores = [calculer_score(c, poids, annee_reference) for c in communes]
    return sorted(scores, key=lambda s: (-s.score, s.commune.nom))
