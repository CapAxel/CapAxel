"""Lecture du CSV de communes et écriture du CSV de résultats."""

from __future__ import annotations

import csv
from pathlib import Path

from .modeles import Commune, DocumentUrbanisme, ScoreCommune

COLONNES_REQUISES = {
    "code_insee",
    "nom",
    "population",
    "evolution_population_pct",
    "logements_autorises_3ans",
    "document_urbanisme",
}

VRAI = {"oui", "o", "1", "true", "vrai", "x"}


def _entier(valeur: str | None, defaut: int = 0) -> int:
    if valeur is None or not valeur.strip():
        return defaut
    return int(float(valeur.replace(",", ".")))


def _decimal(valeur: str | None) -> float | None:
    if valeur is None or not valeur.strip():
        return None
    return float(valeur.replace(",", "."))


def _booleen(valeur: str | None) -> bool:
    return bool(valeur) and valeur.strip().lower() in VRAI


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
                annee = _decimal(ligne.get("annee_approbation"))
                communes.append(
                    Commune(
                        code_insee=ligne["code_insee"].strip(),
                        nom=ligne["nom"].strip(),
                        population=_entier(ligne["population"]),
                        evolution_population_pct=_decimal(
                            ligne["evolution_population_pct"]
                        )
                        or 0.0,
                        logements_autorises_3ans=_entier(
                            ligne["logements_autorises_3ans"]
                        ),
                        document_urbanisme=DocumentUrbanisme.depuis_texte(
                            ligne["document_urbanisme"]
                        ),
                        annee_approbation=int(annee) if annee is not None else None,
                        competence_plu_epci=_booleen(ligne.get("competence_plu_epci")),
                        epci=(ligne.get("epci") or "").strip(),
                        distance_agence_km=_decimal(ligne.get("distance_agence_km")),
                    )
                )
            except (ValueError, KeyError) as erreur:
                raise ValueError(f"{chemin}, ligne {numero} : {erreur}") from erreur
    return communes


def ecrire_resultats(scores: list[ScoreCommune], chemin: str | Path) -> None:
    """Écrit le classement dans un CSV exploitable dans un tableur."""
    chemin = Path(chemin)
    criteres = list(scores[0].details) if scores else []
    with chemin.open("w", newline="", encoding="utf-8") as fichier:
        redacteur = csv.writer(fichier)
        redacteur.writerow(
            ["rang", "code_insee", "nom", "epci", "score", "priorite"]
            + [f"note_{nom}" for nom in criteres]
        )
        for rang, resultat in enumerate(scores, start=1):
            commune = resultat.commune
            redacteur.writerow(
                [
                    rang,
                    commune.code_insee,
                    commune.nom,
                    commune.epci,
                    resultat.score,
                    resultat.priorite,
                ]
                + [resultat.details[nom] for nom in criteres]
            )
