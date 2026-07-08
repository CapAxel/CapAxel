"""Analyse des besoins : un score 0-100 par axe, correspondant aux grandes
familles de missions du bureau d'étude.

Axes analysés :

- ``habitat``        : vacance de logement forte ou en hausse → étude habitat, OPAH.
- ``commerce``       : vacance commerciale, tissu commercial faible ou en repli
                       → étude de redynamisation commerciale.
- ``croissance``     : croissance démographique et marché tendu → encadrement
                       du développement, études pré-opérationnelles.
- ``revitalisation`` : déclin démographique et perte d'emplois → stratégie
                       globale de revitalisation (type Petites Villes de Demain).

Chaque note élémentaire vaut entre 0 et 1 ; un axe est la moyenne pondérée de
ses notes, ramenée sur 100. Quand une donnée manque, la note correspondante
est écartée et les autres sont renormalisées ; si tout manque, l'axe vaut None
(« non évaluable ») plutôt qu'un faux zéro.
"""

from __future__ import annotations

from .modeles import AnalyseCommune, Commune

LIBELLES_AXES: dict[str, str] = {
    "habitat": "Étude habitat / OPAH",
    "commerce": "Redynamisation commerciale",
    "croissance": "Encadrement du développement",
    "revitalisation": "Stratégie de revitalisation",
}

SEUIL_PRIORITAIRE = 65.0
SEUIL_A_SUIVRE = 45.0


def _borner(valeur: float) -> float:
    return max(0.0, min(1.0, valeur))


def _palier(valeur: float, bas: float, haut: float) -> float:
    """Note linéaire : 0 quand valeur ≤ bas, 1 quand valeur ≥ haut."""
    if haut == bas:
        return 0.0
    return _borner((valeur - bas) / (haut - bas))


def _moyenne_ponderee(
    notes: list[tuple[float | None, float]], poids_plein: float = 0.7
) -> float | None:
    """Moyenne pondérée en ignorant les notes manquantes (renormalisation).

    Quand les signaux disponibles pèsent moins de ``poids_plein``, le résultat
    est tempéré proportionnellement : un axe ne peut pas saturer sur la seule
    foi d'un signal secondaire quand les données principales manquent.
    """
    disponibles = [(note, poids) for note, poids in notes if note is not None]
    total = sum(poids for _, poids in disponibles)
    if total <= 0:
        return None
    moyenne = sum(note * poids for note, poids in disponibles) / total
    return moyenne * min(1.0, total / poids_plein)


# --- Axes de besoin ---------------------------------------------------------


def axe_habitat(commune: Commune) -> float | None:
    """Vacance de logement : niveau (5 % normal → 15 % critique) et tendance."""
    taux = commune.taux_vacance_logement
    evolution = commune.evolution_vacance_points
    return _en_score(
        _moyenne_ponderee(
            [
                (_palier(taux, 5.0, 15.0) if taux is not None else None, 0.6),
                # -1 point (résorption) → 0 ; +4 points (décrochage) → 1
                (
                    _palier(evolution, -1.0, 4.0) if evolution is not None else None,
                    0.4,
                ),
            ]
        )
    )


def axe_commerce(commune: Commune) -> float | None:
    """Fragilité du tissu commercial.

    La vacance commerciale relevée (terrain, CCI) pèse le plus lourd quand elle
    est connue ; à défaut, densité commerciale et trajectoire de l'emploi
    servent de signaux indirects.
    """
    vacance = commune.taux_vacance_commerciale
    # La densité commerciale n'est un signal que pour les bourgs : un village
    # de 300 habitants sans commerce n'est pas un centre à redynamiser.
    densite = (
        commune.commerces_pour_1000_hab
        if commune.population is not None and commune.population >= 1000
        else None
    )
    evolution_emplois = commune.evolution_emplois_pct
    return _en_score(
        _moyenne_ponderee(
            [
                # 5 % de locaux vides = marché sain ; 20 % = centre sinistré
                (_palier(vacance, 5.0, 20.0) if vacance is not None else None, 0.5),
                # moins de ~8 commerces / 1 000 hab = offre faible
                (
                    1.0 - _palier(densite, 0.0, 8.0) if densite is not None else None,
                    0.2,
                ),
                # emplois en repli entre deux recensements
                (
                    _palier(-evolution_emplois, 0.0, 10.0)
                    if evolution_emplois is not None
                    else None,
                    0.3,
                ),
            ]
        )
    )


def axe_croissance(commune: Commune) -> float | None:
    """Développement à encadrer : croissance, marché tendu, construction."""
    evolution_pop = commune.evolution_population_pct
    taux_vacance = commune.taux_vacance_logement
    construction = None
    if commune.logements_autorises_3ans is not None and commune.population:
        construction = commune.logements_autorises_3ans / commune.population * 1000.0
    return _en_score(
        _moyenne_ponderee(
            [
                (_palier(evolution_pop, 0.0, 8.0) if evolution_pop is not None else None, 0.5),
                # vacance ≤ 3 % = marché très tendu
                (
                    1.0 - _palier(taux_vacance, 3.0, 8.0)
                    if taux_vacance is not None
                    else None,
                    0.3,
                ),
                (_palier(construction, 0.0, 15.0) if construction is not None else None, 0.2),
            ]
        )
    )


def axe_revitalisation(commune: Commune) -> float | None:
    """Déclin structurel : population et emplois en baisse."""
    evolution_pop = commune.evolution_population_pct
    evolution_longue = commune.evolution_population_longue_pct
    evolution_emplois = commune.evolution_emplois_pct
    return _en_score(
        _moyenne_ponderee(
            [
                (
                    _palier(-evolution_pop, 0.0, 8.0)
                    if evolution_pop is not None
                    else None,
                    0.4,
                ),
                (
                    _palier(-evolution_longue, 0.0, 12.0)
                    if evolution_longue is not None
                    else None,
                    0.2,
                ),
                (
                    _palier(-evolution_emplois, 0.0, 10.0)
                    if evolution_emplois is not None
                    else None,
                    0.4,
                ),
            ]
        )
    )


def _en_score(note: float | None) -> float | None:
    return None if note is None else round(note * 100.0, 1)


# --- Analyse globale ---------------------------------------------------------


def _facteur_taille(commune: Commune) -> float:
    """Modère le score global selon la capacité budgétaire probable.

    Les très petites communes portent rarement des études seules ; les grandes
    villes ont des services internes ou attirent les grands cabinets.
    """
    pop = commune.population
    if pop is None:
        return 0.9
    if pop < 200:
        return 0.75
    if pop < 500:
        return 0.85
    if pop <= 20000:
        return 1.0
    return 0.85


def priorite_depuis_score(score: float) -> str:
    if score >= SEUIL_PRIORITAIRE:
        return "À démarcher en priorité"
    if score >= SEUIL_A_SUIVRE:
        return "À suivre"
    return "Faible intérêt"


def analyser_commune(commune: Commune) -> AnalyseCommune:
    """Calcule le score de chaque axe de besoin et le profil global."""
    axes: dict[str, float | None] = {
        "habitat": axe_habitat(commune),
        "commerce": axe_commerce(commune),
        "croissance": axe_croissance(commune),
        "revitalisation": axe_revitalisation(commune),
    }

    evalues = {nom: score for nom, score in axes.items() if score is not None}
    if evalues:
        besoin_principal = max(evalues, key=lambda nom: evalues[nom])
        meilleur = evalues[besoin_principal]
        moyenne = sum(evalues.values()) / len(evalues)
        score_global = (0.7 * meilleur + 0.3 * moyenne) * _facteur_taille(commune)
    else:
        besoin_principal = ""
        score_global = 0.0

    return AnalyseCommune(
        commune=commune,
        axes=axes,
        besoin_principal=besoin_principal,
        score_global=round(score_global, 1),
        priorite=priorite_depuis_score(score_global),
    )


def analyser_communes(communes: list[Commune]) -> list[AnalyseCommune]:
    """Analyse toutes les communes, triées par intérêt global décroissant."""
    analyses = [analyser_commune(c) for c in communes]
    return sorted(analyses, key=lambda a: (-a.score_global, a.commune.nom))


def grouper_par_besoin(
    analyses: list[AnalyseCommune],
) -> dict[str, list[AnalyseCommune]]:
    """Regroupe les analyses par besoin principal (ordre des LIBELLES_AXES)."""
    groupes: dict[str, list[AnalyseCommune]] = {}
    for nom_axe in LIBELLES_AXES:
        membres = [a for a in analyses if a.besoin_principal == nom_axe]
        if membres:
            groupes[nom_axe] = membres
    sans_donnees = [a for a in analyses if not a.besoin_principal]
    if sans_donnees:
        groupes[""] = sans_donnees
    return groupes
