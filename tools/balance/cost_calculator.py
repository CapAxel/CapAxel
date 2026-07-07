#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CORTÈGE — la règle des 100 points (annexe équilibrage §3.2).

Le « classeur de référence » promis par l'annexe §10 : recalcule le coût de
chaque figure T1 selon la formule indicative

    Coût ≈ PV/3 + DPS×3 + (POR − 1,5)×2 + (VIT − 100)/5 + Utilité (barème)

et vérifie que toute figure tombe à 100 ± 10. On n'ajoute jamais une figure
sans la faire passer à la caisse.

Usage :
    python cost_calculator.py            # tableau lisible
    python cost_calculator.py --json     # sortie machine
    python cost_calculator.py --base 25  # tester une constante de base (exploration)

Code de sortie : 0 si les 16 figures sont dans 100 ± 10, 1 sinon.
Stdlib uniquement — aucune dépendance.
"""

from __future__ import annotations

import argparse
import json
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
FICHIER_FIGURES = os.path.join(ICI, "figures.json")

CIBLE = 100.0
TOLERANCE = 10.0

# Profils de rôle §3.1, convertis en valeurs absolues depuis l'étalon PV 100 / DPS 10.
# Servent à juger si une suggestion de correction reste DANS le profil du rôle.
PROFILS_ROLE = {
    "Cogneur":   {"pv": (150, 175), "dps": (9, 11),  "por": (1.5, 1.5), "vit": (90, 90)},
    "Tireur":    {"pv": (65, 75),   "dps": (9, 12),  "por": (7, 10),    "vit": (95, 115)},
    "Soutien":   {"pv": (75, 90),   "dps": (3, 4),   "por": (5, 6),     "vit": (100, 100)},
    "Récolteur": {"pv": (80, 85),   "dps": (5, 5),   "por": (4, 5),     "vit": (100, 105)},
    "Filou":     {"pv": (70, 80),   "dps": (10, 11), "por": (1.5, 1.5), "vit": (110, 120)},
    "Bâtisseur": {"pv": (85, 90),   "dps": (3, 3),   "por": (5, 6),     "vit": (95, 95)},
}


def _forcer_utf8() -> None:
    """Console Windows : force l'UTF-8 pour les ✓ ✗ ⚠ et les accents."""
    for flux in (sys.stdout, sys.stderr):
        try:
            flux.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


def charger_figures(chemin: str = FICHIER_FIGURES) -> dict:
    with open(chemin, encoding="utf-8") as fp:
        return json.load(fp)


def decomposer(figure: dict, base: float = 0.0) -> dict:
    """Applique la formule indicative §3.2 et rend chaque terme séparément."""
    t_pv = figure["pv"] / 3.0
    t_dps = figure["dps"] * 3.0
    t_por = (figure["portee_m"] - 1.5) * 2.0
    t_vit = (figure["vitesse"] - 100.0) / 5.0
    t_uti = float(sum(e["points"] for e in figure["utilite"]))
    total = base + t_pv + t_dps + t_por + t_vit + t_uti
    return {
        "base": base,
        "pv": t_pv,
        "dps": t_dps,
        "por": t_por,
        "vit": t_vit,
        "utilite": t_uti,
        "total": total,
        "ecart": total - CIBLE,
        "dans_fourchette": abs(total - CIBLE) <= TOLERANCE,
    }


def suggerer_corrections(figure: dict, ecart: float) -> list[dict]:
    """Pour un déviant : de combien bouger CHAQUE stat, seule, pour revenir à 100.

    Chaque piste est confrontée au profil de rôle §3.1 — si aucune ne tient
    dans le profil, l'écart relève de la formule ou du barème, pas de la figure.
    """
    correction = -ecart  # points de coût à ajouter (positif si sous-coté)
    profil = PROFILS_ROLE[figure["role"]]
    pistes = [
        # (étiquette, delta de stat, valeur actuelle, clé de profil, unité)
        ("PV", correction * 3.0, figure["pv"], "pv", "PV"),
        ("DPS", correction / 3.0, figure["dps"], "dps", "DPS"),
        ("POR", correction / 2.0, figure["portee_m"], "por", "m"),
        ("VIT", correction * 5.0, figure["vitesse"], "vit", "VIT"),
        ("Utilité", correction, None, None, "pts de barème"),
    ]
    resultats = []
    for etiquette, delta, actuel, cle, unite in pistes:
        if cle is None:  # l'utilité n'a pas de borne de profil — bornée par le bon sens
            resultats.append({
                "stat": etiquette,
                "delta": round(delta, 1),
                "nouvelle_valeur": None,
                "dans_profil_role": True,
                "detail": f"Utilité {delta:+.1f} {unite}",
            })
            continue
        nouvelle = actuel + delta
        borne_basse, borne_haute = profil[cle]
        faisable = borne_basse <= nouvelle <= borne_haute
        resultats.append({
            "stat": etiquette,
            "delta": round(delta, 1),
            "nouvelle_valeur": round(nouvelle, 1),
            "dans_profil_role": faisable,
            "detail": (
                f"{etiquette} {delta:+.1f} → {nouvelle:.1f} {unite} "
                f"({'dans' if faisable else 'HORS'} profil {figure['role']} "
                f"[{borne_basse}–{borne_haute}])"
            ),
        })
    return resultats


def analyser(donnees: dict, base: float = 0.0) -> list[dict]:
    lignes = []
    for figure in donnees["figures"]:
        deco = decomposer(figure, base)
        ligne = {
            "nom": figure["nom"],
            "role": figure["role"],
            "pv": figure["pv"],
            "dps": figure["dps"],
            "portee_m": figure["portee_m"],
            "vitesse": figure["vitesse"],
            "decomposition": deco,
            "cout": round(deco["total"], 2),
            "ecart": round(deco["ecart"], 2),
            "dans_fourchette": deco["dans_fourchette"],
            "hypotheses_bareme": [e["element"] for e in figure["utilite"] if e.get("hypothese")],
            "suggestions": [] if deco["dans_fourchette"] else suggerer_corrections(figure, deco["ecart"]),
        }
        lignes.append(ligne)
    return lignes


def imprimer_tableau(lignes: list[dict], base: float) -> None:
    etalon_nu = base + 100 / 3.0 + 10 * 3.0  # PV 100, DPS 10, POR mêlée, VIT 100, utilité 0
    print("CORTÈGE — règle des 100 points (annexe équilibrage §3.2)")
    print(f"Formule : Coût ≈ PV/3 + DPS×3 + (POR−1,5)×2 + (VIT−100)/5 + Utilité — cible {CIBLE:.0f} ± {TOLERANCE:.0f}")
    if base:
        print(f"Constante de base expérimentale : +{base:g} (exploration, hors annexe)")
    print(f"Note de cohérence : l'étalon nu (PV 100, DPS 10, mêlée, VIT 100, utilité 0) vaut {etalon_nu:.1f} pts par cette formule.")
    print()

    entete = (f"{'Figure':<18} {'Rôle':<10} {'PV/3':>6} {'DPS×3':>6} {'POR':>6} "
              f"{'VIT':>6} {'Util':>5} {'Coût':>7} {'Écart':>7}  État")
    print(entete)
    print("─" * len(entete))
    for l in lignes:
        d = l["decomposition"]
        drapeau = " ✓ " if l["dans_fourchette"] else "⚠ ✗"
        print(f"{l['nom']:<18} {l['role']:<10} {d['pv']:>6.1f} {d['dps']:>6.1f} {d['por']:>6.1f} "
              f"{d['vit']:>6.1f} {d['utilite']:>5.0f} {d['total']:>7.1f} {d['ecart']:>+7.1f}  {drapeau}")
    print("─" * len(entete))

    conformes = [l for l in lignes if l["dans_fourchette"]]
    deviants = [l for l in lignes if not l["dans_fourchette"]]
    print(f"\nBilan : {len(conformes)}/{len(lignes)} figures dans la fourchette {CIBLE:.0f} ± {TOLERANCE:.0f}.")

    # Moyennes par rôle — pour voir si l'écart est une affaire de figures ou de rôles.
    par_role: dict[str, list[float]] = {}
    for l in lignes:
        par_role.setdefault(l["role"], []).append(l["cout"])
    print("\nCoût moyen par rôle (dispersion intra-rôle entre parenthèses) :")
    for role, couts in sorted(par_role.items(), key=lambda kv: -sum(kv[1]) / len(kv[1])):
        moyenne = sum(couts) / len(couts)
        etendue = max(couts) - min(couts)
        print(f"  {role:<10} {moyenne:>6.1f}  (étendue {etendue:.1f} sur {len(couts)} figures)")

    if deviants:
        print("\nSuggestions de correction (une seule stat bougée à la fois, confrontée au profil de rôle §3.1) :")
        for l in deviants:
            print(f"\n  ⚠ {l['nom']} ({l['role']}) : coût {l['cout']:.1f}, écart {l['ecart']:+.1f}")
            faisables = [s for s in l["suggestions"] if s["dans_profil_role"] and s["stat"] != "Utilité"]
            for s in l["suggestions"]:
                marque = "→" if s["dans_profil_role"] else "✗"
                print(f"      {marque} {s['detail']}")
            if not faisables:
                print("      ∅ Aucune stat ne peut combler l'écart en restant dans le profil de rôle :")
                print("        l'écart relève de la FORMULE ou du BARÈME d'utilité, pas de la figure elle-même.")
        print("\nLecture d'ensemble : si les déviants sont groupés par rôle avec une faible dispersion")
        print("intra-rôle, le roster est cohérent — ce sont les coefficients de la formule indicative")
        print("(« à ajuster dans le classeur de référence », §3.2) qu'il faut retoucher, pas les kits.")


def main(argv: list[str] | None = None) -> int:
    _forcer_utf8()
    parseur = argparse.ArgumentParser(description="Règle des 100 points — classeur de référence CORTÈGE.")
    parseur.add_argument("--json", action="store_true", help="sortie machine (JSON) au lieu du tableau")
    parseur.add_argument("--base", type=float, default=0.0,
                         help="constante de base expérimentale ajoutée à la formule (défaut : 0, formule de l'annexe)")
    parseur.add_argument("--figures", default=FICHIER_FIGURES, help="chemin du fichier figures.json")
    args = parseur.parse_args(argv)

    donnees = charger_figures(args.figures)
    lignes = analyser(donnees, base=args.base)

    if args.json:
        sortie = {
            "formule": donnees["meta"]["formule_cout"],
            "cible": CIBLE,
            "tolerance": TOLERANCE,
            "base_experimentale": args.base,
            "conformes": sum(1 for l in lignes if l["dans_fourchette"]),
            "total": len(lignes),
            "figures": lignes,
        }
        print(json.dumps(sortie, ensure_ascii=False, indent=2))
    else:
        imprimer_tableau(lignes, args.base)

    return 0 if all(l["dans_fourchette"] for l in lignes) else 1


if __name__ == "__main__":
    sys.exit(main())
