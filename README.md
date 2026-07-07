# PROJET CORTÈGE

> *« Le successeur spirituel de Squad Busters que Supercell ne fera jamais : premium, équitable, construit avec sa communauté. »*

Un **action-roguelite à escouade** en coopération : votre cortège grossit en fusionnant ses membres — partir seul, finir à la tête d'une procession de légendes qui remplit l'écran. Le plaisir immédiat et chaotique de Squad Busters, avec l'agentivité en plus et le hasard subi en moins.

## Fiche d'identité

| | |
|---|---|
| Genre | Action-roguelite à escouade, vue top-down 3/4 |
| Joueurs | 1 à 4 en coopération (phase 1), PvP 8 escouades (phase 2, conditionnelle) |
| Plateforme | PC / Steam d'abord ; inputs compatibles mobile pour un portage ultérieur |
| Format de session | Runs de 20–30 min composées de manches de 3–4 min |
| Modèle | Premium (~15 €), cosmétiques optionnels, **zéro puissance vendue** |
| Moteur | **Godot 4.6 + GDScript typé** (décision tranchée — plan B Unity documenté, voir Roadmap technique) |
| Équipe cible | 2 à 4 personnes, 12–18 mois jusqu'à l'accès anticipé |

## Les quatre piliers

1. **La boule de neige.** La croissance visible : chaque coffre, chaque fusion rend le cortège plus gros, plus bruyant, plus spectaculaire.
2. **Du choix, pas du tirage.** Chaque coffre est un draft depuis un deck construit par le joueur. La variance crée la surprise, jamais l'injustice.
3. **Le chaos lisible.** L'écran peut être saturé, la décision doit rester claire en un coup d'œil.
4. **Le respect du joueur.** La progression récompense la maîtrise et la collection, jamais le portefeuille.

## L'univers en une phrase

Tous les récits de l'humanité vivent dans **la Grande Mémoire** ; quand une histoire cesse d'être racontée, **les Oublis** la dévorent. Vous êtes **le Conteur** : vous traversez les Ères pour rallumer les légendes — Héraclès, Jeanne d'Arc, Musashi, Gilgamesh — et elles marchent derrière vous.

## Documentation de design

| Document | Rôle |
|---|---|
| [GDD — Projet Cortège v0.3](docs/GDD_Projet_Cortege_v0.3.md) | **Document maître** : vision, piliers, boucles, systèmes clés, production, KPIs, risques |
| [Bible d'univers v0.2](docs/Bible_Univers_Cortege_v0.2.md) | Cosmologie, ton, garde-fous éditoriaux, bestiaire des Oublis, continents/Ères, roster des 16 figures |
| [Annexe systèmes v0.2](docs/Annexe_Boucles_Progression_Classement_v0.2.md) | Les cinq boucles de gameplay, progression (Ferveur/Encre), classement (le Panthéon, l'Épreuve hebdomadaire) |
| [Annexe équilibrage v0.1](docs/Annexe_Equilibrage_v0.1.md) | Chiffrage : étalon, règle des 100 points, les 16 figures, courbe adverse, économies, score |
| [Unités de base v0.1](docs/Unites_Base_Cortege_v0.1.md) | Fiches de travail des 16 figures : logique des tiers par type (mythique/historique/légendaire), pistes T2, questions ouvertes |

**Documents d'exécution** — comment ce jeu sort réellement :

| Document | Rôle |
|---|---|
| [Plan de production — scénarios & financement v0.1](docs/Plan_Production_Scenarios_v0.1.md) | **Quatre scénarios chiffrés** (solo, duo aidé, éditeur, communauté d'abord), cartographie des aides France/Europe (FAJV, CIJV, régions), matrice comparative, recommandation et plan des 90 premiers jours |
| [Roadmap technique v0.1](docs/Roadmap_Technique_v0.1.md) | Décision moteur (Godot 4.6, plan B Unity daté), architecture déterministe cible, jalon 0 « le Jouet » (3 semaines), backlog du vertical slice en 8 sprints, protocole de playtest de la gate |

Les versions obsolètes sont conservées dans [`docs/archive/`](docs/archive/).

## Code

| Dossier | Contenu |
|---|---|
| [`prototype/`](prototype/) | **Squelette Godot 4.4+ du jalon 0** : simulation déterministe à pas fixe (30 Hz) séparée de la présentation, flux RNG seedés (draft/spawns/dégâts), journal d'inputs (format replay), cortège en flux, draft 1-parmi-3, fusion T1→T3, vagues de Silences. S'ouvre dans Godot sans dépendance — voir [prototype/README.md](prototype/README.md) |
| [`tools/balance/`](tools/balance/) | Les deux outils annoncés par l'annexe équilibrage §10 : `cost_calculator.py` (règle des 100 points) et `ttk_simulator.py` (Monte-Carlo de la courbe adverse). Python 3, stdlib uniquement — voir [tools/balance/README.md](tools/balance/README.md). Premier verdict : la formule indicative sous-cote 13 figures sur 16 de façon *ordonnée par rôle* — ce sont les coefficients à recalibrer, pas les kits |

## Statut

**Jalon 0 engagé** (juillet 2026). Le design (GDD v0.3 + annexes), le plan d'exécution (scénarios de production, roadmap technique) et le squelette de prototype sont posés. Prochaines échéances, dans l'ordre du plan des 90 jours (Plan de production §5) :

1. **Jalon 0 « le Jouet »** (3 semaines) : la boule de neige validée manette en main — critère : se déplacer avec 15 figures est déjà agréable ;
2. **Dossier écriture FAJV** : dépôt à la commission du 21 septembre 2026 ;
3. **Gate du vertical slice** (~novembre 2026, GDD §12) : 70 % des playtesteurs relancent une run sans y être invités — c'est elle qui choisit le scénario de production.

*Les documents sont vivants : toute valeur chiffrée est une hypothèse de départ destinée au playtest.*
