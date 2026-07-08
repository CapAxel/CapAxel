"""Interface en ligne de commande.

Deux sous-commandes :

- ``tri-communes collecter`` : récupère les données open data des communes
  (INSEE, SIRENE) et produit / met à jour le fichier CSV de travail.
- ``tri-communes trier`` : analyse le CSV et classe les communes par type
  de besoin et par intérêt de démarchage.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .besoins import LIBELLES_AXES, analyser_communes, grouper_par_besoin
from .chargement import charger_communes, ecrire_communes, ecrire_resultats
from .collecte import (
    codes_du_departement,
    collecter_communes,
    fusionner_donnees_manuelles,
)
from .modeles import AnalyseCommune


def _construire_parseur() -> argparse.ArgumentParser:
    parseur = argparse.ArgumentParser(
        prog="tri-communes",
        description=(
            "Collecte les données historiques des communes (INSEE, SIRENE) et "
            "les classe par type de besoin pour cibler la prospection d'un "
            "bureau d'étude en urbanisme."
        ),
    )
    sous = parseur.add_subparsers(dest="commande")

    collecter = sous.add_parser(
        "collecter", help="collecter les données open data des communes"
    )
    cibles = collecter.add_mutually_exclusive_group(required=True)
    cibles.add_argument(
        "--departement", metavar="DEP", help="toutes les communes d'un département"
    )
    cibles.add_argument(
        "--codes", metavar="INSEE[,INSEE…]", help="codes INSEE séparés par des virgules"
    )
    collecter.add_argument(
        "--sortie",
        default="communes.csv",
        metavar="CSV",
        help="fichier de sortie (défaut : communes.csv) ; s'il existe, les "
        "colonnes saisies à la main sont conservées",
    )

    trier = sous.add_parser(
        "trier", help="analyser un CSV et classer les communes par besoin"
    )
    trier.add_argument("fichier", help="CSV des communes (produit par « collecter »)")
    trier.add_argument(
        "--liste",
        action="store_true",
        help="classement global unique au lieu du regroupement par besoin",
    )
    trier.add_argument(
        "--sortie", metavar="CSV", help="exporte le classement dans ce fichier CSV"
    )
    trier.add_argument(
        "--top", type=int, metavar="N", help="ne garde que les N meilleures communes"
    )
    trier.add_argument(
        "--min-score",
        type=float,
        metavar="X",
        help="ne garde que les communes de score global ≥ X",
    )
    return parseur


# --- Sous-commande collecter --------------------------------------------------


def _executer_collecte(args: argparse.Namespace) -> int:
    if args.departement:
        codes = codes_du_departement(args.departement)
        print(f"{len(codes)} communes dans le département {args.departement}.")
    else:
        codes = [code.strip() for code in args.codes.split(",") if code.strip()]

    def progression(code: str, index: int, total: int) -> None:
        print(f"[{index}/{total}] collecte de {code}…", flush=True)

    communes, echecs = collecter_communes(codes, rappel=progression)

    sortie = Path(args.sortie)
    if sortie.exists():
        try:
            existantes = charger_communes(sortie)
            communes = fusionner_donnees_manuelles(communes, existantes)
            print(f"Colonnes manuelles reprises depuis {sortie}.")
        except ValueError as erreur:
            print(f"Avertissement : fusion impossible ({erreur})", file=sys.stderr)

    ecrire_communes(communes, sortie)
    print(f"\n{len(communes)} communes écrites dans {sortie}.")
    if echecs:
        print(f"{len(echecs)} échec(s) :", file=sys.stderr)
        for code, raison in echecs:
            print(f"  - {code} : {raison}", file=sys.stderr)
    print(
        "Complétez si possible les colonnes taux_vacance_commerciale et\n"
        "logements_autorises_3ans, puis lancez : tri-communes trier " + str(sortie)
    )
    return 1 if echecs and not communes else 0


# --- Sous-commande trier --------------------------------------------------------


def _score(valeur: float | None) -> str:
    return f"{valeur:5.1f}" if valeur is not None else "    -"


def _afficher_liste(analyses: list[AnalyseCommune]) -> None:
    largeur = max([len(a.commune.nom) for a in analyses] + [len("Commune")])
    entete = (
        f"{'Rang':>4}  {'Commune':<{largeur}}  {'INSEE':<5}  {'Global':>6}  "
        f"{'Habitat':>7} {'Commerce':>8} {'Croiss.':>7} {'Revita.':>7}  "
        f"Besoin principal"
    )
    print(entete)
    print("-" * len(entete))
    for rang, analyse in enumerate(analyses, start=1):
        axes = analyse.axes
        print(
            f"{rang:>4}  {analyse.commune.nom:<{largeur}}  "
            f"{analyse.commune.code_insee:<5}  {analyse.score_global:>6.1f}  "
            f"{_score(axes.get('habitat')):>7} "
            f"{_score(axes.get('commerce')):>8} {_score(axes.get('croissance')):>7} "
            f"{_score(axes.get('revitalisation')):>7}  "
            f"{LIBELLES_AXES.get(analyse.besoin_principal, 'données insuffisantes')}"
        )


def _afficher_par_besoin(analyses: list[AnalyseCommune]) -> None:
    groupes = grouper_par_besoin(analyses)
    for nom_axe, membres in groupes.items():
        libelle = LIBELLES_AXES.get(nom_axe, "Données insuffisantes")
        print(f"\n━━━ {libelle} ({len(membres)} commune(s)) ━━━")
        largeur = max([len(a.commune.nom) for a in membres] + [len("Commune")])
        print(
            f"{'Commune':<{largeur}}  {'INSEE':<5}  {'Besoin':>6}  {'Global':>6}  Priorité"
        )
        for analyse in membres:
            score_axe = analyse.axes.get(nom_axe)
            print(
                f"{analyse.commune.nom:<{largeur}}  {analyse.commune.code_insee:<5}  "
                f"{_score(score_axe):>6}  {analyse.score_global:>6.1f}  {analyse.priorite}"
            )


def _executer_tri(args: argparse.Namespace) -> int:
    try:
        communes = charger_communes(args.fichier)
        analyses = analyser_communes(communes)
    except (ValueError, OSError) as erreur:
        print(f"Erreur : {erreur}", file=sys.stderr)
        return 1

    if args.min_score is not None:
        analyses = [a for a in analyses if a.score_global >= args.min_score]
    if args.top is not None:
        analyses = analyses[: args.top]
    if not analyses:
        print("Aucune commune ne correspond aux filtres.", file=sys.stderr)
        return 1

    if args.liste:
        _afficher_liste(analyses)
    else:
        _afficher_par_besoin(analyses)

    if args.sortie:
        ecrire_resultats(analyses, args.sortie)
        print(f"\nClassement exporté dans {args.sortie}")
    return 0


def main(argv: list[str] | None = None) -> int:
    arguments = list(sys.argv[1:] if argv is None else argv)
    # Rétrocompatibilité : « tri-communes fichier.csv » équivaut à « trier ».
    if arguments and arguments[0] not in {"collecter", "trier", "-h", "--help"}:
        arguments.insert(0, "trier")

    args = _construire_parseur().parse_args(arguments)
    if args.commande == "collecter":
        return _executer_collecte(args)
    if args.commande == "trier":
        return _executer_tri(args)
    _construire_parseur().print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
