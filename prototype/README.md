# CORTÈGE — Prototype (jalon 0, « le Jouet »)

Squelette jouable du test le moins cher du pilier n°1 (« la boule de neige », GDD §1) : un cortège qui suit le Conteur, ramasse la Ferveur, ouvre des Volumes, drafte et fusionne — face à des vagues de Silences. **Critère de sortie du jalon 0 (Roadmap technique §3) : se déplacer avec 15 figures doit déjà être agréable, sans objectif de jeu.**

## Installer et lancer

1. Télécharger **Godot 4.4 ou plus récent** (version standard, pas .NET) : <https://godotengine.org/download>
2. Ouvrir Godot → *Importer* → sélectionner `prototype/project.godot`.
3. Lancer avec **F5**.

Aucune dépendance, aucun addon, aucun asset binaire : tout est dessiné par code.

## Contrôles

| Entrée | Action |
|---|---|
| ZQSD / WASD / flèches / stick gauche | déplacer le Conteur (le cortège suit) |
| Espace / A (manette) | esquive (élan bref, recharge 2 s — anneau autour du Conteur) |
| E / X (manette) | ouvrir un Volume proche (coût : 60 Ferveur, +20 par Volume déjà ouvert dans la manche) |
| 1 / 2 / 3 ou clic | choisir une carte du draft |
| R | recommencer (même seed → même monde, la reproductibilité se constate à la main) |

## Ce qui est implémenté

- **Simulation à pas fixe 30 Hz, séparée de la présentation** : `src/sim/` ne touche ni à la scène, ni à l'horloge murale, ni au RNG global ; `src/view/` et `src/ui/` lisent l'état et interpolent entre deux ticks. C'est la traduction directe de l'exigence du Panthéon (annexe systèmes §3.6, Roadmap technique §2).
- **Flux RNG nommés et seedés séparément** (`draft` / `spawns` / `degats`) : consommer du hasard en combat ne décalera jamais le draft.
- **Journal d'inputs** (`src/sim/input_recorder.gd`) : chaque tick est journalisé (vecteur quantifié + actions) ; le format replay seed + inputs existe dès le premier jour. En fin de run, le replay est écrit dans `user://replay_last.json`.
- **Le cortège en flux** : suivi de chaîne + séparation (banc de poissons) ; une figure au contact tient sa ligne — le déplacement est le verbe de combat (annexe systèmes §1.1).
- **Draft 1-parmi-3** depuis un roster de 8 figures, **fusion** 3 identiques → tier supérieur (×3 PV/dégâts, ×1,25 rayons — annexe équilibrage §2), en cascade jusqu'au T3, plafond de 24 figures avec conversion de l'excédent en Ferveur.
- **Économie in-run** : gisements de Ferveur, butin des Silences, coût des Volumes croissant dans la manche (annexe §6).
- **Les Silences** (étalon : 30 PV, 4 DPS, VIT 85 — annexe §1) par vagues budgétées en Silences-équivalents ; provocation de Héraclès (r 4 m) et aura de soin de Jeanne (1,5 % PV max/s, r 5 m) comme premiers kits.
- **Stats des 16 figures** dans `data/figures.json`, copie conforme de l'annexe équilibrage §4.
- **Relecture de replay et test de déterminisme** (`src/sim/replay_player.gd`, `src/sim/state_hash.gd`, `src/run_harness.gd`) : une run pilotée par un bot déterministe est journalisée puis **rejouée depuis seed + inputs** ; les empreintes d'état doivent coïncider tick à tick. C'est le test « qui casse » de la roadmap, branché en CI (`.github/workflows/ci.yml`).
- **Benchmark du tick** à charge nominale (24 figures + 300 Oublis, budget 4 ms — roadmap §1.4). Premier verdict honnête : **~3,8 ms de moyenne, p95 au-dessus du budget** dès le squelette — les boucles ennemis×figures en O(n²) coûtent leur prix en GDScript ; la grille spatiale prévue avec le module virgule fixe n'est pas une option, c'est le chemin.

## Ce qui n'est PAS implémenté (assumé)

Pas de virgule fixe (flottants — suffisant sur une machine ; la bascule 32.32 est la première tâche du Jalon 0, Roadmap §1.3 — l'empreinte d'état actuelle, `hash()` sur flottants, n'est donc stable que pour un même binaire), pas de pitié au draft, pas de Capacité de Cortège, 14 des 16 kits réduits à leurs stats, pas de Brume, pas de manches structurées (lecture/montée/pic/extraction), pas d'audio, pas de pathfinding. Le temps s'arrête pendant le draft — choix de jouet à requestionner (Roadmap, risque du sprint 3). Le pilote du selftest meurt vers la manche 3-4 : la couverture des fusions en profondeur (T3) attend la pondération de pitié, qui densifiera mécaniquement les doublons.

## Vérifications headless (celles de la CI)

```
godot --headless --path prototype --import          # d'abord : cache des class_name
godot --headless --path prototype -- --selftest     # déterminisme record → replay (exit 1 si divergence)
godot --headless --path prototype -- --selftest=900 --seed=7   # variantes : durée en ticks, seed
godot --headless --path prototype -- --replay=user://replay_last.json  # rejoue un replay, imprime l'empreinte
godot --headless --path prototype -- --bench        # coût du tick à charge nominale vs budget 4 ms
```

## Correspondance code ↔ design

| Code | Document |
|---|---|
| `src/sim/sim_world.gd` (constantes en tête) | annexe équilibrage §1, §2, §5.1, §6 ; annexe systèmes §2.2 |
| `src/sim/rng_service.gd`, `input_recorder.gd` | annexe systèmes §3.6 ; Roadmap technique §2 |
| `src/sim/replay_player.gd`, `state_hash.gd`, `src/run_harness.gd` | annexe systèmes §3.6 (re-simulation, golden replays) ; Roadmap §2–3 |
| `src/sim/sim_draft.gd` | GDD §4.1 |
| `src/sim/sim_figure.gd` | annexe équilibrage §2 et §4 ; bible §3 (Personnage/Héros/Légende) |
| `src/view/figure_view.gd` | GDD §10 (une silhouette par rôle, tier par taille/auréole) |
| `data/figures.json` | annexe équilibrage §4.1–4.2 |

## Les 5 prochaines choses à coder

1. **La grille spatiale** sur les boucles ennemis×figures — le benchmark la réclame déjà (p95 > 4 ms à charge nominale) ; elle préfigure celle du module virgule fixe.
2. **La bascule en virgule fixe 32.32** (Roadmap §1.3) — et avec elle, une empreinte d'état enfin multiplateforme.
3. **La dramaturgie de manche** (3 min 45 : lecture / montée / pic / extraction + la Brume qui avance) — annexe systèmes §1.2.
4. **La pondération de pitié du draft** (jamais plus de N Volumes sans revoir un doublon possédé) — GDD §4.1 ; elle donnera au passage la couverture T2/T3 au selftest.
5. **L'esquive comme décision** : i-frames réelles sur les figures pendant l'élan, et le « juice » de fusion (tween d'échelle, strate musicale) — le pilier 1 doit s'entendre.
