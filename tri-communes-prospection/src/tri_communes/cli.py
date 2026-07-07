"""Interface en ligne de commande : `tri-communes <fichier.csv>`."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .chargement import charger_communes, ecrire_resultats
from .modeles import ScoreCommune
from .scoring import trier_communes


def _construire_parseur() -> argparse.ArgumentParser:
    parseur = argparse.ArgumentParser(
        prog="tri-communes",
        description=(
            "Trie les communes par intérêt de prospection pour un bureau "
            "d'étude en urbanisme (score de 0 à 100)."
        ),
    )
    parseur.add_argument("fichier", help="CSV des communes (voir README pour le format)")
    parseur.add_argument(
        "--sortie", metavar="CSV", help="exporte le classement dans ce fichier CSV"
    )
    parseur.add_argument(
        "--top", type=int, metavar="N", help="ne garde que les N meilleures communes"
    )
    parseur.add_argument(
        "--min-score",
        type=float,
        metavar="X",
        help="ne garde que les communes de score supérieur ou égal à X",
    )
    parseur.add_argument(
        "--poids",
        metavar="JSON",
        help="fichier JSON de pondérations par critère (renormalisées)",
    )
    parseur.add_argument(
        "--annee-reference",
        type=int,
        metavar="AAAA",
        help="année de référence pour l'âge des documents (défaut : année courante)",
    )
    return parseur


def _afficher_tableau(scores: list[ScoreCommune]) -> None:
    largeur_nom = max([len(s.commune.nom) for s in scores] + [len("Commune")])
    entete = (
        f"{'Rang':>4}  {'Commune':<{largeur_nom}}  {'INSEE':<5}  "
        f"{'Score':>5}  {'Doc.':<5}  Priorité"
    )
    print(entete)
    print("-" * len(entete))
    for rang, resultat in enumerate(scores, start=1):
        commune = resultat.commune
        print(
            f"{rang:>4}  {commune.nom:<{largeur_nom}}  {commune.code_insee:<5}  "
            f"{resultat.score:>5.1f}  {commune.document_urbanisme.value:<5}  "
            f"{resultat.priorite}"
        )


def main(argv: list[str] | None = None) -> int:
    args = _construire_parseur().parse_args(argv)

    poids = None
    if args.poids:
        poids = json.loads(Path(args.poids).read_text(encoding="utf-8"))

    try:
        communes = charger_communes(args.fichier)
        scores = trier_communes(communes, poids, args.annee_reference)
    except (ValueError, OSError) as erreur:
        print(f"Erreur : {erreur}", file=sys.stderr)
        return 1

    if args.min_score is not None:
        scores = [s for s in scores if s.score >= args.min_score]
    if args.top is not None:
        scores = scores[: args.top]

    if not scores:
        print("Aucune commune ne correspond aux filtres.", file=sys.stderr)
        return 1

    _afficher_tableau(scores)

    if args.sortie:
        ecrire_resultats(scores, args.sortie)
        print(f"\nClassement exporté dans {args.sortie}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
