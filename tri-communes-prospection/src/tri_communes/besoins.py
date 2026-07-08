"""Analyse des besoins : un score 0-100 par axe, correspondant aux grandes
familles de missions du bureau d'étude.

Axes analysés :

- ``habitat``        : vacance de logement forte ou en hausse, parc ancien
                       → étude habitat, OPAH.
- ``commerce``       : vacance commerciale, tissu commercial faible ou en repli
                       → étude de redynamisation commerciale.
- ``croissance``     : croissance démographique, marché tendu, prix en hausse
                       → encadrement du développement, études pré-opérationnelles.
- ``revitalisation`` : déclin démographique et perte d'emplois → stratégie
                       globale de revitalisation (type Petites Villes de Demain).
- ``vieillissement`` : population âgée nombreuse et en forte progression
                       → adaptation du logement, OPAH autonomie, programmation.
- ``tourisme``       : pression touristique (résidences secondaires, lits
                       marchands) sans dispositif de gestion détecté → stratégie
                       d'accueil, régulation des meublés, logement des actifs.

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
    "vieillissement": "Adaptation au vieillissement",
    "tourisme": "Gestion de la pression touristique",
}

# Quand un office de tourisme est déjà présent, la commune gère déjà
# activement son tourisme : l'opportunité d'accompagnement chute.
FACTEUR_TOURISME_GERE = 0.35

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
    """Vacance de logement (niveau et tendance) et ancienneté du parc."""
    taux = commune.taux_vacance_logement
    evolution = commune.evolution_vacance_points
    parc_ancien = commune.part_logements_avant_1946
    return _en_score(
        _moyenne_ponderee(
            [
                (_palier(taux, 5.0, 15.0) if taux is not None else None, 0.45),
                # -1 point (résorption) → 0 ; +4 points (décrochage) → 1
                (
                    _palier(evolution, -1.0, 4.0) if evolution is not None else None,
                    0.3,
                ),
                # part de résidences principales d'avant 1946 : cible OPAH
                (
                    _palier(parc_ancien, 25.0, 60.0)
                    if parc_ancien is not None
                    else None,
                    0.25,
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
    """Développement à encadrer : croissance, marché tendu, prix, construction."""
    evolution_pop = commune.evolution_population_pct
    taux_vacance = commune.taux_vacance_logement
    evolution_prix = commune.evolution_prix_m2_pct
    construction = None
    if commune.logements_autorises_3ans is not None and commune.population:
        construction = commune.logements_autorises_3ans / commune.population * 1000.0
    return _en_score(
        _moyenne_ponderee(
            [
                (_palier(evolution_pop, 0.0, 8.0) if evolution_pop is not None else None, 0.4),
                # vacance ≤ 3 % = marché très tendu
                (
                    1.0 - _palier(taux_vacance, 3.0, 8.0)
                    if taux_vacance is not None
                    else None,
                    0.25,
                ),
                # médiane DVF en forte hausse sur ~4 ans = pression foncière
                (
                    _palier(evolution_prix, 0.0, 25.0)
                    if evolution_prix is not None
                    else None,
                    0.2,
                ),
                (_palier(construction, 0.0, 15.0) if construction is not None else None, 0.15),
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


def axe_vieillissement(commune: Commune) -> float | None:
    """Population âgée nombreuse et en progression : adaptation du parc."""
    part_65 = commune.part_65plus
    evolution = commune.evolution_part_65plus_points
    part_80 = commune.part_80plus
    return _en_score(
        _moyenne_ponderee(
            [
                # ~20 % de 65 ans et plus = moyenne nationale ; 35 % = très âgé
                (_palier(part_65, 20.0, 35.0) if part_65 is not None else None, 0.4),
                # progression de la part des 65+ entre deux recensements
                (_palier(evolution, 0.0, 4.0) if evolution is not None else None, 0.3),
                # le grand âge (80+) commande l'adaptation des logements
                (_palier(part_80, 6.0, 14.0) if part_80 is not None else None, 0.3),
            ]
        )
    )


def axe_tourisme(commune: Commune) -> float | None:
    """Pression touristique sans dispositif de gestion détecté.

    L'objectif est de repérer les communes qui subissent la pression
    (résidences secondaires, lits marchands) sans l'avoir encore organisée :
    la présence d'un office de tourisme — détectée via SIRENE — signale une
    gestion déjà en place et réduit fortement l'opportunité.
    """
    part_rs = commune.part_residences_secondaires
    evolution_rs = commune.evolution_res_secondaires_points
    lits = commune.lits_touristiques_pour_100_hab
    if lits is None and commune.lits_touristiques is None and part_rs is not None:
        # Absente du jeu INSEE des hébergements = pas d'offre marchande connue.
        lits = 0.0
    note = _moyenne_ponderee(
        [
            # 10 % de résidences secondaires = notable ; 40 % = très forte pression
            (_palier(part_rs, 10.0, 40.0) if part_rs is not None else None, 0.45),
            # part en hausse = pression qui s'installe
            (_palier(evolution_rs, 0.0, 5.0) if evolution_rs is not None else None, 0.25),
            # lits touristiques marchands rapportés à la population
            (_palier(lits, 5.0, 50.0) if lits is not None else None, 0.3),
        ]
    )
    if note is not None and commune.office_tourisme:
        note *= FACTEUR_TOURISME_GERE
    return _en_score(note)


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
        "vieillissement": axe_vieillissement(commune),
        "tourisme": axe_tourisme(commune),
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
