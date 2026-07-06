# CORTÈGE — Outils d'équilibrage

**Version 0.1 — Outillage annoncé par l'annexe équilibrage v0.1, §10**

> **Avertissement de méthode** (repris de l'annexe) : « Chaque nombre est fait pour être trahi — mais depuis une base cohérente. » Ces outils ne disent pas si le jeu est bon ; ils disent si les chiffres du papier se contredisent entre eux. C'est tout, et c'est déjà beaucoup : chaque contradiction attrapée ici est une semaine de playtest économisée.

Prérequis : Python 3.13, **stdlib uniquement** — aucun `pip install`. Tout se lance depuis ce dossier.

---

## 1. Les trois fichiers

| Fichier | Rôle |
|---|---|
| `figures.json` | Source de vérité locale : les 16 figures T1 (annexe §4.1–4.2) et la décomposition de leur utilité en éléments du barème §3.2. Les deux scripts le lisent — on ne modifie jamais un chiffre ailleurs qu'ici. |
| `cost_calculator.py` | Le « classeur de référence » (§10) : implémente la règle des 100 points (§3.2) et recalcule le coût de chaque figure à la modification. |
| `ttk_simulator.py` | Le « simulateur Python » (§10) : Monte-Carlo de TTK — cortège cible contre vagues budgétées — pour vérifier les tables du §5 sans lancer le moteur. |

**Le contrat des hypothèses.** L'annexe ne publie que des *extraits* du barème d'utilité. Chaque valeur qui ne vient pas de l'annexe porte `"hypothese": true` et un champ `justification` qui la rattache à une ancre publiée (exemple : Ulysse, ×1,6 dans le dos = 10 pts, ancré sur « dégâts conditionnels ×1,5 = 9 »). Quand le classeur de référence tranchera, on retire le drapeau — jamais avant.

---

## 2. `cost_calculator.py` — la règle des 100 points

```
python cost_calculator.py            # tableau lisible, décomposition par terme
python cost_calculator.py --json     # sortie machine (intégrable en CI)
python cost_calculator.py --base 25  # exploration : tester une constante de base
```

**Ce qu'il vérifie.** Pour chaque figure : `Coût ≈ PV/3 + DPS×3 + (POR−1,5)×2 + (VIT−100)/5 + Utilité`, avec drapeau ⚠ hors de 100 ± 10, et pour chaque déviant une suggestion chiffrée par stat (de combien bouger PV, DPS, POR, VIT ou l'utilité, seuls, pour revenir à 100) — chaque suggestion étant confrontée au profil de rôle §3.1 pour dire si elle est réaliste. **Code de sortie 1 si au moins une figure déborde** : le script est fait pour tourner en garde-fou avant chaque commit de `figures.json`.

**État au 6 juillet 2026 — résultat honnête, à verser au dossier de la v0.2 de l'annexe.** Avec la formule indicative telle qu'écrite et des hypothèses de barème raisonnables, **3 figures sur 16 tombent dans 100 ± 10** (les trois Cogneurs : Héraclès 92,7 · Boudicca 92,0 · Gilgamesh 97,3). Les treize autres sont *sous*-cotées, et le déficit est ordonné par rôle :

| Rôle | Coût moyen | Dispersion intra-rôle |
|---|---|---|
| Cogneur | 94,0 | 5,3 |
| Tireur | 78,7 | 8,7 |
| Filou | 76,0 | 1,7 |
| Récolteur | 65,5 | 0,3 |
| Bâtisseur | 62,2 | 2,3 |
| Soutien | 56,2 | 8,0 |

La lecture est nette : la dispersion **intra-rôle** est faible partout (≤ 8,7 points) — le roster est cohérent — mais l'écart **inter-rôles** atteint 38 points. Deux indices convergent : l'étalon nu lui-même (PV 100, DPS 10, utilité 0) ne vaut que 63,3 points par cette formule ; et aucune correction de stat ne peut combler l'écart d'un déviant sans sortir du profil de rôle §3.1. Conclusion : **ce sont les coefficients de la formule indicative qu'il faut retoucher** (l'annexe le prévoit : « coefficients à ajuster dans le classeur de référence »), vraisemblablement en revalorisant le barème d'utilité d'un facteur ~2,5–3 pour les rôles à kit (Soutien, Bâtisseur, Récolteur) — pas les kits eux-mêmes. L'option `--base` permet d'explorer une constante de base, mais elle ne résorbe pas à elle seule un étalement de 38 points.

---

## 3. `ttk_simulator.py` — la courbe adverse

```
python ttk_simulator.py                          # N=1000 par jalon, graine 20260706
python ttk_simulator.py --seed 42 --runs 500     # autre graine, autre volume
python ttk_simulator.py --verbose                # compositions, percentiles, pression
```

**Ce qu'il vérifie.** Pour chaque jalon du §5.1 (manche 1, 3, 6, dernière), N rencontres entre un cortège plausible (composition en T1-eq tirée du roster réel, mélange de rôles, au moins un Cogneur et un Soutien) et la vague standard en Silences-équivalents. Pas fixe de 1/30 s — le même que la simulation déterministe du jeu — et règles simples assumées : DPS agrégé, ciblage réparti sur les 3 ennemis les plus proches, provocation (les Cogneurs encaissent 80 % de l'aggro), soins d'aura et bouclier tournant appliqués, ralentisseurs sur l'approche, **dégâts conditionnels non appliqués** (simulation conservatrice : le jeu réel sera légèrement plus favorable au joueur). Même graine → mêmes résultats, au bit près — l'outil respecte la religion du déterminisme gravée au GDD.

Cibles mesurées : TTK médian d'un Silence sous le feu ≤ 2 s · pertes médianes = 0 avant le pic · durée de vague en sortie informative. **Code de sortie 1 si un jalon échoue.**

**État au 6 juillet 2026 (graine 20260706, N = 1000 ; confirmé graine 42) — 3 jalons sur 4 tiennent :**

| Jalon | TTK médian | Pertes médianes | Durée de vague | Verdict |
|---|---|---|---|---|
| Manche 1 (4 T1-eq vs 8) | **2,25 s** | 0 | 11,5 s | ✗ |
| Manche 3 (9 vs 20) | 1,40 s | 0 | 15,1 s | ✓ |
| Manche 6 (18 vs 38) | 1,08 s | 0 | 21,1 s | ✓ |
| Dernière (35 vs 60) | 0,70 s | 0 | 20,5 s | ✓ |

Le seul échec est instructif : en manche 1, un cortège de 4 ne développe qu'environ 29 DPS agrégés une fois qu'on y compte un Soutien à 3–4 DPS ; réparti sur 3 cibles, un Silence de 30 PV demande ~3 s de feu théorique, et la médiane mesurée tombe à 2,25 s. Personne ne meurt (pertes 0, robuste au p90) — la manche 1 n'est pas *dangereuse*, elle est *molle*. Trois sorties possibles pour la v0.2 de l'annexe : assumer un TTK de manche 1 à ~2,5 s (la montée en puissance n'en sera que plus sensible), affaiblir le Silence de manche 1 (24–26 PV), ou resserrer le ciblage de début de run (focus naturel quand il y a peu d'ennemis). C'est une décision de design, pas d'outillage — l'outil a fait son travail en la posant.

---

## 4. Faire vivre ces outils avec le playtest

1. **Toute valeur modifiée passe par `figures.json`** — jamais dans le code — puis les deux scripts sont relancés. C'est la règle de l'annexe : « on n'ajoute jamais une figure sans la faire passer à la caisse », et toute valeur modifiée est répercutée dans le classeur de référence.
2. **Les hypothèses meurent une par une.** Chaque session de playtest qui tranche une valeur du barème remplace `"hypothese": true` par `false` et met à jour la justification. Le jour où il ne reste plus de drapeaux, le barème est complet.
3. **Recaler les constantes du simulateur sur le prototype** dès qu'il existe : la conversion `VIT 100 = 4 m/s`, la distance d'apparition (14 m), la taille et la cadence des paquets, la part d'aggro des Cogneurs (80 %). Ce sont les hypothèses les plus fragiles — elles sont toutes en tête de `ttk_simulator.py`.
4. **Étendre, dans l'ordre de valeur** : les élites (Anachronisme ≈ 15 Silences, colonne §5.1 aujourd'hui hors périmètre) ; les dégâts conditionnels en uptime moyen mesuré en playtest ; les tiers T2/T3 (×3 PV/dégâts, ×2,5 soins, ×1,25 contrôles — §2) pour simuler de vrais cortèges fusionnés plutôt que des T1-eq ; enfin le pic de manche à ~90 % de capacité et la Brume à 10 % PV/s.
5. **Brancher en CI quand le dépôt aura une CI** : les deux scripts rendent un code de sortie non nul quand un garde-fou casse — un `git push` qui fait dévier une figure ou effondrer un jalon doit se voir.

---

*Document vivant. Les chiffres de l'état des lieux ci-dessus datent du 6 juillet 2026 (annexe v0.1, `figures.json` v0.1) : ils sont faits pour périmer — relancer les scripts fait foi.*
