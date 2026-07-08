"""Lecture / écriture des fichiers CSV (communes et résultats d'analyse)."""

from __future__ import annotations

import csv
from pathlib import Path

from .besoins import LIBELLES_AXES
from .modeles import AnalyseCommune, Commune

# Ordre des colonnes du CSV de communes. Seules code_insee et nom sont
# obligatoires : toute donnée absente est simplement « non disponible ».
COLONNES = [
    "code_insee",
    "nom",
    "epci",
    "population",
    "population_prec",
    "population_anc",
    "annee_recensement",
    "logements",
    "logements_vacants",
    "residences_secondaires",
    "logements_prec",
    "logements_vacants_prec",
    "residences_secondaires_prec",
    "part_logements_avant_1946",
    "part_65plus",
    "part_65plus_prec",
    "part_80plus",
    "emplois",
    "emplois_prec",
    "nb_etablissements",
    "nb_commerces",
    "lits_touristiques",
    "office_tourisme",
    "prix_m2",
    "prix_m2_prec",
    "taux_vacance_commerciale",
    "logements_autorises_3ans",
]

COLONNES_REQUISES = {"code_insee", "nom"}

# Colonnes saisies à la main : préservées lors d'une nouvelle collecte.
COLONNES_MANUELLES = [
    "taux_vacance_commerciale",
    "logements_autorises_3ans",
]


def _entier(valeur: str | None) -> int | None:
    if valeur is None or not valeur.strip():
        return None
    return int(round(float(valeur.replace(",", "."))))


def _decimal(valeur: str | None) -> float | None:
    if valeur is None or not valeur.strip():
        return None
    return float(valeur.replace(",", "."))


def _booleen(valeur: str | None) -> bool | None:
    if valeur is None or not valeur.strip():
        return None
    return valeur.strip().lower() in {"oui", "o", "1", "true", "vrai", "x"}


def charger_communes(chemin: str | Path) -> list[Commune]:
    """Charge un fichier CSV de communes (voir README pour le format)."""
    chemin = Path(chemin)
    with chemin.open(newline="", encoding="utf-8-sig") as fichier:
        lecteur = csv.DictReader(fichier)
        if lecteur.fieldnames is None:
            raise ValueError(f"{chemin} : fichier vide ou sans en-tête.")
        manquantes = COLONNES_REQUISES - set(lecteur.fieldnames)
        if manquantes:
            raise ValueError(
                f"{chemin} : colonnes manquantes : {', '.join(sorted(manquantes))}"
            )

        communes: list[Commune] = []
        for numero, ligne in enumerate(lecteur, start=2):
            try:
                communes.append(
                    Commune(
                        code_insee=ligne["code_insee"].strip(),
                        nom=ligne["nom"].strip(),
                        epci=(ligne.get("epci") or "").strip(),
                        population=_entier(ligne.get("population")),
                        population_prec=_entier(ligne.get("population_prec")),
                        population_anc=_entier(ligne.get("population_anc")),
                        annee_recensement=_entier(ligne.get("annee_recensement")),
                        logements=_decimal(ligne.get("logements")),
                        logements_vacants=_decimal(ligne.get("logements_vacants")),
                        residences_secondaires=_decimal(
                            ligne.get("residences_secondaires")
                        ),
                        logements_prec=_decimal(ligne.get("logements_prec")),
                        logements_vacants_prec=_decimal(
                            ligne.get("logements_vacants_prec")
                        ),
                        residences_secondaires_prec=_decimal(
                            ligne.get("residences_secondaires_prec")
                        ),
                        part_logements_avant_1946=_decimal(
                            ligne.get("part_logements_avant_1946")
                        ),
                        part_65plus=_decimal(ligne.get("part_65plus")),
                        part_65plus_prec=_decimal(ligne.get("part_65plus_prec")),
                        part_80plus=_decimal(ligne.get("part_80plus")),
                        emplois=_decimal(ligne.get("emplois")),
                        emplois_prec=_decimal(ligne.get("emplois_prec")),
                        nb_etablissements=_entier(ligne.get("nb_etablissements")),
                        nb_commerces=_entier(ligne.get("nb_commerces")),
                        lits_touristiques=_entier(ligne.get("lits_touristiques")),
                        office_tourisme=_booleen(ligne.get("office_tourisme")),
                        prix_m2=_decimal(ligne.get("prix_m2")),
                        prix_m2_prec=_decimal(ligne.get("prix_m2_prec")),
                        taux_vacance_commerciale=_decimal(
                            ligne.get("taux_vacance_commerciale")
                        ),
                        logements_autorises_3ans=_entier(
                            ligne.get("logements_autorises_3ans")
                        ),
                    )
                )
            except (ValueError, KeyError) as erreur:
                raise ValueError(f"{chemin}, ligne {numero} : {erreur}") from erreur
    return communes


def _formater(valeur) -> str:
    if valeur is None:
        return ""
    if isinstance(valeur, float):
        return f"{valeur:.1f}".rstrip("0").rstrip(".")
    return str(valeur)


def ecrire_communes(communes: list[Commune], chemin: str | Path) -> None:
    """Écrit le fichier de communes (sortie de la collecte, éditable à la main)."""
    with Path(chemin).open("w", newline="", encoding="utf-8") as fichier:
        redacteur = csv.writer(fichier)
        redacteur.writerow(COLONNES)
        for commune in communes:
            redacteur.writerow(
                [_formater(getattr(commune, colonne)) for colonne in COLONNES]
            )


def ecrire_resultats(analyses: list[AnalyseCommune], chemin: str | Path) -> None:
    """Écrit le classement analysé dans un CSV exploitable dans un tableur."""
    with Path(chemin).open("w", newline="", encoding="utf-8") as fichier:
        redacteur = csv.writer(fichier)
        redacteur.writerow(
            ["rang", "code_insee", "nom", "epci", "besoin_principal", "score_global", "priorite"]
            + [f"score_{axe}" for axe in LIBELLES_AXES]
        )
        for rang, analyse in enumerate(analyses, start=1):
            commune = analyse.commune
            redacteur.writerow(
                [
                    rang,
                    commune.code_insee,
                    commune.nom,
                    commune.epci,
                    LIBELLES_AXES.get(analyse.besoin_principal, ""),
                    analyse.score_global,
                    analyse.priorite,
                ]
                + [_formater(analyse.axes.get(axe)) for axe in LIBELLES_AXES]
            )
