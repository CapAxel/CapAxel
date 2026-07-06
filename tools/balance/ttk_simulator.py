#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CORTÈGE — simulateur Monte-Carlo de TTK (annexe équilibrage §5 et §10).

Vérifie la courbe adverse §5.1 sans lancer le moteur : pour chaque jalon
(manche 1, 3, 6, dernière), simule N rencontres entre un cortège plausible
(composition en T1-eq, mélange de rôles tiré du roster réel) et la vague
standard budgétée en Silences-équivalents (30 PV, 4 DPS, VIT 85).

Règles simples, assumées comme telles :
  · pas fixe de 1/30 s (comme la simulation déterministe du jeu) ;
  · DPS agrégé, chaque figure cible l'un des 3 ennemis les plus proches
    (abstraction de la répartition « plus proche d'abord ») ;
  · les Cogneurs encaissent d'abord (provocation : 80 % de l'aggro) ;
  · soins d'aura (Jeanne d'Arc) et bouclier tournant (Himiko) appliqués ;
  · les ralentisseurs (Orphée, Sun Tzu, Dédale) freinent l'approche ennemie ;
  · les dégâts CONDITIONNELS (dos, flanc, distance…) ne sont PAS appliqués —
    le simulateur est volontairement conservateur.

Cibles §5.1 : TTK médian d'un Silence sous le feu du cortège ≤ 2 s ;
pertes de figures médiane = 0 (le cortège médian ne perd personne hors pic).

Usage :
    python ttk_simulator.py                    # N=1000, graine 20260706
    python ttk_simulator.py --seed 42 --runs 500 --verbose

Reproductible : même graine → mêmes résultats, dans l'esprit du déterminisme
gravé au GDD (replays = seed + inputs). Stdlib uniquement.
Code de sortie : 0 si tous les jalons tiennent leurs cibles, 1 sinon.
"""

from __future__ import annotations

import argparse
import bisect
import json
import os
import random
import statistics
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
FICHIER_FIGURES = os.path.join(ICI, "figures.json")

# ---------------------------------------------------------------- constantes
DT = 1.0 / 30.0                 # pas fixe — le même que la simulation du jeu
METRES_PAR_VIT = 0.04           # hypothèse : VIT 100 = 4 m/s (à caler sur le prototype)
DIST_SPAWN = 14.0               # distance d'apparition des paquets (m)
JITTER_SPAWN = 1.5              # dispersion d'apparition (m)
CONTACT = 1.5                   # portée mêlée
PRISE_MELEE = 2.0               # une figure de mêlée engage jusqu'à 2 m
INTERVALLE_PAQUETS = 2.5        # s entre deux paquets d'une même vague
T_MAX = 120.0                   # garde-fou : au-delà, la rencontre est un échec
PROB_PROVOCATION = 0.8          # part de l'aggro absorbée par les Cogneurs vivants
CIBLE_TTK = 2.0                 # §5.1 : un Silence tombe en ≤ 2 s
CIBLE_PERTES = 0                # §5.1 : aucune perte hors pic pour le cortège médian

# L'ennemi-étalon (§1) — relu depuis figures.json au chargement.
SILENCE = {"pv": 30.0, "dps": 4.0, "vit": 85.0}

# Jalons §5.1 : (nom, cortège cible en T1-eq, vague standard en Silences-eq)
JALONS = [
    ("Manche 1", 4, 8),
    ("Manche 3 (avant boss Ère I)", 9, 20),
    ("Manche 6 (Ère II)", 18, 38),
    ("Dernière manche", 35, 60),
]

# Composition plausible : poids de draft par rôle (hypothèse de méta médiane).
POIDS_ROLES = {"Cogneur": 22, "Tireur": 26, "Soutien": 16,
               "Filou": 16, "Récolteur": 12, "Bâtisseur": 8}

# Exposition à l'aggro qui « fuit » les Cogneurs (les corps-à-corps s'exposent plus).
EXPOSITION = {"Cogneur": 4.0, "Filou": 3.0, "Récolteur": 2.0,
              "Bâtisseur": 2.0, "Soutien": 1.5, "Tireur": 1.0}

# Ralentisseurs : facteur de VIT ennemie dans les 5 derniers mètres (abstraction
# des auras/fanions/murets qui canalisent l'approche). Cumulatif, plancher 0,5.
RALENTISSEURS = {"Orphée": 0.75, "Sun Tzu": 0.80, "Dédale": 0.70}

SOIN_AURA_PCT = 0.015           # Jeanne d'Arc : 1,5 % PV max/s (barème §3.2)
BOUCLIER_PV_PAR_S = 25.0 / 6.0  # Himiko : 25 PV / 6 s, appliqué au plus entamé


# ---------------------------------------------------------------- utilitaires
def _forcer_utf8() -> None:
    for flux in (sys.stdout, sys.stderr):
        try:
            flux.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


def charger_roster(chemin: str = FICHIER_FIGURES) -> tuple[dict, dict]:
    with open(chemin, encoding="utf-8") as fp:
        donnees = json.load(fp)
    silence = donnees["meta"].get("silence")
    if silence:
        SILENCE.update({"pv": float(silence["pv"]), "dps": float(silence["dps"]),
                        "vit": float(silence["vitesse"])})
    par_role: dict[str, list[dict]] = {}
    for figure in donnees["figures"]:
        par_role.setdefault(figure["role"], []).append(figure)
    return donnees, par_role


def composer_cortege(par_role: dict, taille: int, rng: random.Random) -> list[dict]:
    """Composition plausible en T1-eq : au moins 1 Cogneur, 1 Soutien dès 4 corps,
    le reste au poids de draft. Les doublons sont légitimes (un T2 = 3 T1-eq)."""
    composition: list[dict] = [rng.choice(par_role["Cogneur"])]
    if taille >= 4:
        composition.append(rng.choice(par_role["Soutien"]))
    roles, poids = zip(*POIDS_ROLES.items())
    while len(composition) < taille:
        role = rng.choices(roles, weights=poids, k=1)[0]
        composition.append(rng.choice(par_role[role]))
    return composition


# ---------------------------------------------------------------- simulation
def simuler_rencontre(composition: list[dict], nb_ennemis: int, rng: random.Random) -> dict:
    """Une rencontre cortège-vague au pas de 1/30 s. Rend TTK, durée, pertes."""
    # --- cortège (variance individuelle ±10 % sur le DPS : forme du jour)
    n_fig = len(composition)
    f_nom = [f["nom"] for f in composition]
    f_role = [f["role"] for f in composition]
    f_pvmax = [float(f["pv"]) for f in composition]
    f_pv = list(f_pvmax)
    f_dps = [f["dps"] * rng.uniform(0.9, 1.1) for f in composition]
    f_por = [max(float(f["portee_m"]), PRISE_MELEE) for f in composition]
    f_vivant = [True] * n_fig
    f_cible = [-1] * n_fig

    nb_jeanne = sum(1 for n in f_nom if n == "Jeanne d'Arc")
    nb_himiko = sum(1 for n in f_nom if n == "Himiko")
    facteur_lent = 1.0
    for nom in f_nom:
        if nom in RALENTISSEURS:
            facteur_lent *= RALENTISSEURS[nom]
    facteur_lent = max(facteur_lent, 0.5)

    # --- vague : paquets échelonnés (une vague n'arrive jamais d'un bloc)
    taille_paquet = max(4, min(8, round(nb_ennemis / 7)))
    e_spawn, e_dist = [], []
    for i in range(nb_ennemis):
        e_spawn.append((i // taille_paquet) * INTERVALLE_PAQUETS)
        e_dist.append(DIST_SPAWN + rng.uniform(0.0, JITTER_SPAWN))
    e_pv = [SILENCE["pv"]] * nb_ennemis
    e_vivant = [True] * nb_ennemis
    e_premier_coup = [-1.0] * nb_ennemis
    e_cible = [-1] * nb_ennemis
    vitesse_base = SILENCE["vit"] * METRES_PAR_VIT
    dps_silence = SILENCE["dps"]

    cogneurs = [j for j in range(n_fig) if f_role[j] == "Cogneur"]

    ttks: list[float] = []
    pertes = 0
    morts_ennemis = 0
    t = 0.0
    dernier_mort = 0.0

    while morts_ennemis < nb_ennemis and t < T_MAX and any(f_vivant):
        t += DT

        actifs = [i for i in range(nb_ennemis) if e_vivant[i] and e_spawn[i] <= t]
        if not actifs:
            continue

        # 1) approche — les ralentisseurs freinent les 5 derniers mètres
        for i in actifs:
            d = e_dist[i]
            if d > CONTACT:
                v = vitesse_base * (facteur_lent if d <= 5.0 else 1.0)
                e_dist[i] = max(CONTACT, d - v * DT)

        # tri par distance : sert au ciblage « parmi les 3 plus proches »
        tri = sorted(actifs, key=lambda i: e_dist[i])
        distances_triees = [e_dist[i] for i in tri]

        # 2) feu du cortège
        for j in range(n_fig):
            if not f_vivant[j]:
                continue
            c = f_cible[j]
            if c < 0 or not e_vivant[c] or e_dist[c] > f_por[j] + 0.3:
                borne = bisect.bisect_right(distances_triees, f_por[j])
                candidats = [i for i in tri[:borne] if e_vivant[i]][:3]
                if not candidats:
                    f_cible[j] = -1
                    continue
                c = f_cible[j] = rng.choice(candidats)
            if e_premier_coup[c] < 0.0:
                e_premier_coup[c] = t
            e_pv[c] -= f_dps[j] * DT
            if e_pv[c] <= 0.0:
                e_vivant[c] = False
                morts_ennemis += 1
                dernier_mort = t
                ttks.append(t - e_premier_coup[c])

        # 3) riposte ennemie — les Cogneurs encaissent d'abord (provocation)
        cogneurs_vivants = [j for j in cogneurs if f_vivant[j]]
        for i in actifs:
            if not e_vivant[i] or e_dist[i] > CONTACT + 0.05:
                continue
            c = e_cible[i]
            if c < 0 or not f_vivant[c]:
                if cogneurs_vivants and rng.random() < PROB_PROVOCATION:
                    c = rng.choice(cogneurs_vivants)
                else:
                    autres = [j for j in range(n_fig) if f_vivant[j] and f_role[j] != "Cogneur"] \
                        or [j for j in range(n_fig) if f_vivant[j]]
                    poids = [EXPOSITION[f_role[j]] for j in autres]
                    c = rng.choices(autres, weights=poids, k=1)[0]
                e_cible[i] = c
            f_pv[c] -= dps_silence * DT
            if f_pv[c] <= 0.0:
                f_vivant[c] = False
                pertes += 1
                cogneurs_vivants = [j for j in cogneurs if f_vivant[j]]

        # 4) soins — aura de Jeanne (tout le cortège groupé), bouclier d'Himiko
        if nb_jeanne:
            for j in range(n_fig):
                if f_vivant[j] and f_pv[j] < f_pvmax[j]:
                    f_pv[j] = min(f_pvmax[j], f_pv[j] + nb_jeanne * SOIN_AURA_PCT * f_pvmax[j] * DT)
        if nb_himiko:
            pire, pire_manque = -1, 0.0
            for j in range(n_fig):
                if f_vivant[j]:
                    manque = f_pvmax[j] - f_pv[j]
                    if manque > pire_manque:
                        pire, pire_manque = j, manque
            if pire >= 0:
                f_pv[pire] = min(f_pvmax[pire], f_pv[pire] + nb_himiko * BOUCLIER_PV_PAR_S * DT)

    balaye = morts_ennemis < nb_ennemis
    return {
        "ttk_median": statistics.median(ttks) if ttks else float("inf"),
        "duree": dernier_mort if not balaye else T_MAX,
        "pertes": pertes if not balaye else n_fig,
        "balaye": balaye,
        "dps_agrege": sum(f["dps"] for f in composition),
    }


def percentile(valeurs: list[float], p: float) -> float:
    tri = sorted(valeurs)
    k = max(0, min(len(tri) - 1, round(p / 100.0 * (len(tri) - 1))))
    return tri[k]


def simuler_jalon(nom: str, taille: int, vague: int, par_role: dict,
                  graine: int, indice: int, runs: int, verbose: bool) -> dict:
    ttk_medians, durees, pertes_liste, dps_liste = [], [], [], []
    balayages = 0
    exemple = None
    for r in range(runs):
        rng = random.Random(graine * 1_000_003 + indice * 10_007 + r)
        composition = composer_cortege(par_role, taille, rng)
        if exemple is None:
            exemple = [f["nom"] for f in composition]
        res = simuler_rencontre(composition, vague, rng)
        ttk_medians.append(res["ttk_median"])
        durees.append(res["duree"])
        pertes_liste.append(res["pertes"])
        dps_liste.append(res["dps_agrege"])
        balayages += res["balaye"]

    ttk_med = statistics.median(ttk_medians)
    duree_med = statistics.median(durees)
    pertes_med = statistics.median(pertes_liste)
    ok_ttk = ttk_med <= CIBLE_TTK
    ok_pertes = pertes_med <= CIBLE_PERTES
    verdict = ok_ttk and ok_pertes and balayages == 0

    print(f"=== {nom} — cortège {taille} T1-eq contre {vague} Silences-eq ===")
    print(f"  TTK médian d'un Silence sous le feu : {ttk_med:5.2f} s   (cible ≤ {CIBLE_TTK:.0f} s)      {'✓' if ok_ttk else '✗'}")
    print(f"  Pertes de figures (médiane)         : {pertes_med:5.0f}     (cible {CIBLE_PERTES} avant le pic) {'✓' if ok_pertes else '✗'}")
    print(f"  Durée totale de la vague (médiane)  : {duree_med:5.1f} s")
    if balayages:
        print(f"  ⚠ Cortège balayé dans {balayages}/{runs} rencontres")
    print(f"  Verdict : {'✓ le jalon tient ses cibles §5.1' if verdict else '✗ le jalon ne tient pas ses cibles §5.1'}")
    if verbose:
        dps_med = statistics.median(dps_liste)
        ttk_theorique = SILENCE["pv"] / (dps_med / 3.0)  # feu réparti sur ~3 cibles
        print(f"  · composition exemple : {', '.join(exemple)}")
        print(f"  · DPS agrégé médian du cortège : {dps_med:.1f} "
              f"(TTK théorique à feu réparti sur 3 cibles : {ttk_theorique:.2f} s)")
        print(f"  · TTK p10 / p90 : {percentile(ttk_medians, 10):.2f} / {percentile(ttk_medians, 90):.2f} s")
        print(f"  · pertes p90 : {percentile([float(p) for p in pertes_liste], 90):.0f} ; "
              f"durée p90 : {percentile(durees, 90):.1f} s")
        print(f"  · pression : vague {vague * SILENCE['pv']:.0f} PV / {vague * SILENCE['dps']:.0f} DPS ennemis "
              f"contre {dps_med:.0f} DPS de cortège")
    print()
    return {"nom": nom, "verdict": verdict, "ttk": ttk_med, "duree": duree_med, "pertes": pertes_med}


def main(argv: list[str] | None = None) -> int:
    _forcer_utf8()
    parseur = argparse.ArgumentParser(description="Monte-Carlo de TTK — courbe adverse CORTÈGE §5.1.")
    parseur.add_argument("--seed", type=int, default=20260706, help="graine du Monte-Carlo (défaut : 20260706)")
    parseur.add_argument("--runs", type=int, default=1000, help="rencontres simulées par jalon (défaut : 1000)")
    parseur.add_argument("--verbose", action="store_true", help="détails : composition, percentiles, pression")
    parseur.add_argument("--figures", default=FICHIER_FIGURES, help="chemin du fichier figures.json")
    args = parseur.parse_args(argv)

    _, par_role = charger_roster(args.figures)

    print("CORTÈGE — simulateur Monte-Carlo de TTK (courbe adverse, annexe équilibrage §5.1)")
    print(f"Graine : {args.seed} · {args.runs} rencontres par jalon · pas fixe 1/30 s · "
          f"Silence {SILENCE['pv']:.0f} PV / {SILENCE['dps']:.0f} DPS / VIT {SILENCE['vit']:.0f}")
    print("Dégâts conditionnels non appliqués (simulation conservatrice) ; élites hors périmètre.\n")

    resultats = []
    for indice, (nom, taille, vague) in enumerate(JALONS):
        resultats.append(simuler_jalon(nom, taille, vague, par_role,
                                       args.seed, indice, args.runs, args.verbose))

    reussis = sum(1 for r in resultats if r["verdict"])
    print(f"Bilan : {reussis}/{len(resultats)} jalons tiennent les cibles §5.1 "
          f"(TTK ≤ {CIBLE_TTK:.0f} s et pertes médianes = {CIBLE_PERTES}).")
    return 0 if reussis == len(resultats) else 1


if __name__ == "__main__":
    sys.exit(main())
