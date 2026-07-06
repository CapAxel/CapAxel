# CORTÈGE — Roadmap Technique

**Version 0.1 — Document compagnon du GDD v0.3**
*Tranche le « Choix techniques » du GDD §12, traduit l'exigence de déterminisme de l'annexe systèmes §3.6/§4.1 en architecture exécutable, et découpe le chemin jusqu'au vertical slice. S'appuie sur l'étude technique « Godot 4.x ou Unity ? » du 06/07/2026 (citée ci-après « Étude moteur »).*

> **Règle de lecture.** Ce document contient trois types d'énoncés : des **décisions** (tranchées, avec leur critère de réversibilité), des **contraintes** (non négociables, héritées du GDD et des annexes) et des **hypothèses** (chiffrées pour être testées). Rien ici n'est une intention : tout est daté, mesurable, ou les deux.

---

## 1. DÉCISION MOTEUR

### 1.1 La décision

**Godot 4.6.x, branche stable, build officiel, GDScript typé.** Décision effective au lancement du Jalon 0 (13 juillet 2026) ; le plan B (§1.4) reste armé jusqu'à la fin du sprint 4 du slice.

Le raisonnement tient en trois phrases, développées dans l'Étude moteur :

1. **Le critère éliminatoire n'élimine personne.** Ni Godot ni Unity n'offre de déterminisme flottant multiplateforme fiable — le `FloatMode.Deterministic` de Burst est limité au 64 bits et le déterminisme inter-architectures est « sur la roadmap » depuis des années (Étude moteur §2.1). Dans les deux moteurs, la stratégie éprouvée est identique : une simulation maison en **virgule fixe entière**, déterministe *par construction*, que le moteur ne fait que dessiner. Une fois ce fait posé, l'argument technique principal en faveur d'Unity s'évapore.
2. **Le profil de risque tranche.** Pour un studio de 2–4 personnes vendant à 15 €, le risque mortel n'est pas technique, il est structurel : Unity Pro à ~2 310 $/siège/an dès 200 k$ de revenus — un coût indexé sur notre succès — et un éditeur qui a déjà changé les règles unilatéralement une fois (Runtime Fee, 2023–2024). Godot MIT supprime cette classe de risque entièrement. Pour un jeu dont le pilier n°4 est « le respect du joueur » et le positionnement « le contrat de confiance », dépendre d'un éditeur qui a rompu le sien serait aussi une incohérence de marque (Étude moteur §2.4).
3. **Le Panthéon coûte quasi zéro en Godot.** La re-simulation serveur des scores (annexe systèmes §3.6) devient un export headless Linux de ~50 Mo qui rejoue seed + inputs et compare des hash — la seule infrastructure de la phase 1, rendue économiquement triviale (Étude moteur §2.6).

### 1.2 Le tableau comparatif — sur NOS critères

Repris de l'Étude moteur §3, pondérations Cortège :

| Critère (pondération) | Godot 4.6.x | Unity 6.3 LTS | Verdict |
|---|---|---|---|
| **Déterminisme multiplateforme** (éliminatoire) | rien de natif ; sim fixed-point maison, re-sim headless triviale | rien de natif ; Burst réel mais 64-bit seulement, cross-arch « roadmap » | **Égalité** — chantier maison dans les deux cas |
| **Foules 2.5D** (moyen) | MultiMesh/RenderingServer : 10 000+ entités ; hybride nœuds + MultiMesh = notre profil exact | GameObjects + instancing suffisent ; DOTS surdimensionné | **Égalité pratique** si sim/rendu séparés |
| **Steam co-op P2P 4 j + SDR** (haut) | GodotSteam 4.20 (GDExtension) + SteamMultiplayerPeer, relais Valve inclus ; netfox en confort | Steamworks.NET/Facepunch + NGO, plus de précédents — mais couche Steam également communautaire | **Unity +** (maturité), Godot suffisant |
| **Coût / licence / gouvernance** (haut) | MIT, 0 €, gouvernance verrouillée, W4 Games pour consoles | 0 € puis ~9 200 $/an à 4 sièges dès 200 k$ ; précédent de rupture unilatérale | **Godot ++** |
| **Portage mobile ultérieur** (moyen, conditionnel) | viable 2026 (jeux livrés, crash < 1 %, plugins Fondation) **si GDScript/GDExtension** ; C# expérimental | étalon-or, sans réserve | **Unity +**, Godot viable |
| **Pérennité / vitesse d'itération à 2–4** (haut) | éditeur léger, temps de build quasi nuls, headless gratuit en CI | compilations = friction connue ; builds serveur plus lourds | **Godot +** |

Deux critères où Unity garde l'avantage (maturité Steam, mobile), aucun où cet avantage est bloquant pour notre périmètre ; deux critères à forte pondération où Godot domine structurellement. La décision n'est pas serrée.

### 1.3 La stack retenue

| Couche | Choix | Précision |
|---|---|---|
| Moteur | **Godot 4.6.x** (4.6.3 à ce jour) | mineures 4.6.x adoptées, **gel de version avant chaque jalon**, 4.7 réévaluée uniquement entre deux phases |
| Langage | **GDScript typé** (typage statique obligatoire, vérifié en revue) | **pas de C# au chemin critique** — il fermerait le portage mobile (export .NET expérimental, Étude moteur §2.5) |
| Noyau de simulation | **module fixed-point 32.32 maison**, zéro import moteur : tick fixe 30 Hz, RNG xoshiro par flux, collisions cercle + grille spatiale, hash d'état par tick | frontière d'API **gelée dès le Jalon 0** ; bascule des boucles chaudes en **GDExtension C++** si budget tick > 4 ms (décision au sprint 4) |
| Rendu foules | nœuds scène pour les ≤ 24 figures ; **MultiMesh/RenderingServer** pour Oublis et projectiles | le rendu *lit* la sim et interpole entre ticks ; jamais l'inverse |
| Steam | **GodotSteam 4.20+** (GDExtension, dépôt Codeberg) + **SteamMultiplayerPeer** | derrière une interface transport maison ; **ENetMultiplayerPeer** en fallback dev/LAN |
| Netcode co-op (alpha) | host authoritatif, échange d'inputs sur sim déterministe (lockstep à délai fixe) | **netfox** en réserve si la latence exige de la prédiction |
| Tests | **gdUnit4** + gdUnit4-action | suite « golden replays » tri-OS en CI (voir §2.4) |
| CI | GitHub Actions : import headless → tests → exports Win/Linux → upload branche beta Steam via steamcmd | le même export headless Linux servira de service de re-simulation |
| Addons confort | Phantom Camera (zoom automatique du cortège, GDD §10), Beehave (IA des Oublis) | **tous les addons sont vendorés et épinglés** dans le dépôt — un dépôt tiers qui disparaît ne casse rien |

### 1.4 Le plan B — documenté, armé, daté

**Le plan B est Unity 6.3 LTS**, et il est bon marché *par construction* : le noyau fixed-point ne dépend d'aucun moteur, il se porte en C# pur ; rendu GameObjects + GPU instancing ; réseau Netcode for GameObjects + Facepunch.Steamworks ; ~9 000–10 000 $/an de licences à provisionner au plan de financement dès maintenant (Étude moteur §5).

| Question | Réponse |
|---|---|
| **Critère objectif de déclenchement** | à la fin du **sprint 4** (25 septembre 2026), le tick de simulation en charge nominale (24 figures + 300 Oublis + 60 projectiles) dépasse encore **2 × le budget de 4 ms** *après* typage strict complet et premier passage GDExtension des boucles chaudes — **ou** blocage GodotSteam/SDR non contournable constaté au spike du sprint 1 |
| **Coût estimé de la bascule** | 6 à 10 semaines pour un périmètre prototype : UI, scènes, shaders, pipeline d'assets sont perdus ; la sim (portée, pas repensée), le format replay, les golden replays et tout le design chiffré survivent |
| **Date limite de non-retour** | **25 septembre 2026** (fin du sprint 4). Au-delà, le coût de bascule dépasse le coût de contournement : on finit le slice en Godot quoi qu'il arrive, et la question ne se rouvre qu'au gate |
| **Plan B′ (mur perf uniquement)** | rester Godot, sim en C# .NET — seulement si le portage mobile est repoussé sine die *en plus* du mur perf ; deux conditions simultanées, donc improbable : **le plan B principal reste Unity** |

Le micro-benchmark qui alimente ce critère est **la première tâche du Jalon 0** (semaine 1) — on ne construit rien au-dessus d'un budget non mesuré.

---

## 2. ARCHITECTURE CIBLE

### 2.1 Le principe — tout découle du Panthéon

L'annexe systèmes §3.6 dit : *« Anti-triche quasi gratuit, fantômes gratuits, replays gratuits — à condition de l'exiger dès le prototype. »* Chaque bloc ci-dessous est la conséquence directe d'une promesse du Panthéon :

- **L'Épreuve hebdomadaire seedée** exige que la même seed + les mêmes inputs produisent le même état chez tous les joueurs, sur toutes les machines → simulation à pas fixe, virgule fixe entière, zéro dépendance au moteur.
- **Les fantômes de cortège** (§3.5) exigent qu'un replay soit *rejouable en direct* à côté d'une partie vivante → le replay est la liste complète des déterminants de l'état : seed + inputs, rien d'autre.
- **L'anti-triche par re-simulation** exige qu'un serveur reproduise bit à bit une run cliente → mêmes binaires de sim en headless, hash d'état comparés.
- **Le draft équitable** (GDD §4.1) exige que les propositions de coffres soient identiques pour tous à seed égale *quel que soit le déroulé du combat* → flux RNG séparés : consommer du hasard en dégâts ne doit jamais décaler le hasard du draft.

### 2.2 Le schéma

```
                        ┌──────────────────────────────────────────────┐
                        │            PRÉSENTATION (Godot)              │
                        │  scènes, MultiMesh, audio, UI, Phantom Cam   │
                        │  interpole entre les ticks N-1 et N          │
                        │  NE MODIFIE JAMAIS l'état de simulation      │
                        └──────────────▲───────────────────────────────┘
                                       │ lecture seule (snapshots)
      inputs joueur                    │
  ┌─────────────────┐   commandes   ┌──┴───────────────────────────────┐
  │ COUCHE D'INPUT  │──────────────▶│      NOYAU DE SIMULATION         │
  │ clavier/souris/ │  horodatées   │  GDScript typé, fixed-point      │
  │ manette/tactile │  au tick      │  32.32, tick fixe 30 Hz          │
  └─────────────────┘               │  zéro import moteur              │
                                    │                                  │
  ┌─────────────────┐               │  ┌────────────────────────────┐  │
  │ REPLAY          │◀─────────────▶│  │ RNG xoshiro256** seedés    │  │
  │ seed maîtresse  │  enregistre / │  │  · flux DRAFT              │  │
  │ + inputs/ticks  │  rejoue       │  │  · flux APPARITIONS        │  │
  └───────┬─────────┘               │  │  · flux DÉGÂTS             │  │
          │                         │  └────────────────────────────┘  │
          │ upload score+replay     │  hash d'état émis à chaque tick  │
          ▼                         └──────────────▲───────────────────┘
  ┌─────────────────────────┐                      │ mêmes binaires
  │ SERVICE SCORES/REPLAYS  │   re-simulation      │
  │ (phase alpha — HTTPS,   │──────────────────────┘
  │ stockage, classements)  │   Godot headless Linux (~50 Mo)
  └─────────────────────────┘   échantillon aléatoire + scores aberrants

  CO-OP (phase alpha) : SteamMultiplayerPeer (SDR) — les 4 joueurs
  échangent uniquement leurs INPUTS ; chaque client simule tout,
  lockstep à délai fixe. Fallback dev/LAN : ENetMultiplayerPeer.
```

### 2.3 Les blocs, un par un

**a) La boucle de simulation à pas fixe.** 30 ticks/s, budget 4 ms/tick (hypothèse à valider au benchmark de la semaine 1). La présentation tourne à la fréquence de l'écran et interpole les positions entre les deux derniers snapshots — la croissance du cortège reste soyeuse à 144 Hz sans qu'un seul calcul de gameplay dépende du framerate. Règle gravée, vérifiée en revue de code sur ce seul critère : **la sim n'importe rien du moteur** — pas de `Node`, pas de `randi()`, pas de `sin()` libm (tables trigonométriques fixed-point maison), pas d'itération de dictionnaire non ordonnée.

**b) Les flux RNG séparés.** Une seed maîtresse (64 bits) dérive trois générateurs xoshiro256** indépendants : **draft** (propositions des Volumes, coffre sauvage, pitié), **apparitions** (composition et position des vagues, gisements), **dégâts** (variance des coups, critiques). Conséquence directe pour l'Épreuve : deux joueurs sur la même seed voient les mêmes pages se tourner au même Volume, même si l'un a donné trois fois plus de coups que l'autre. C'est la §3.6 rendue mécanique.

**c) Le format de replay.** Un en-tête (version de sim, seed maîtresse, roster, hash de config d'équilibrage) + la liste des inputs horodatés en ticks : `(tick: u32, input: u8, données: u16)`. Trois entrées de jeu seulement (GDD §4.3) plus les choix discrets (draft, routing, fusion, porte-étendard) : une run de 25 minutes ≈ 45 000 ticks dont une minorité porte un input — **cible < 50 Ko par replay, compressé**. Un score soumis = ce fichier ; un fantôme = ce fichier rejoué à côté de votre partie ; une vérification anti-triche = ce fichier re-simulé en headless. Trois promesses du Panthéon, un seul format.

**d) Le hash d'état par tick.** La sim émet en continu un hash (xxHash de l'état sérialisé) ; en CI, les *golden replays* — des runs de référence enregistrées — sont rejoués sur Linux, Windows et macOS et les hash comparés tick à tick. **Le déterminisme devient un test qui casse, pas une intention** — c'est la traduction exécutable du « dès le prototype, pas un patch » de la §3.6.

**e) Le service scores/replays** — la seule infrastructure serveur de la phase 1 (annexe systèmes §4.1). Un service HTTPS minimal (réception score + replay, classements, distribution des fantômes) et un worker de re-simulation : le même export headless Linux que la CI, qui rejoue un échantillon aléatoire plus tout score aberrant. Mis en ligne **à l'alpha**, pas au slice — mais le format qu'il consomme est gelé dès le sprint 1, et la CI joue son rôle de preuve d'ici là.

**f) Le co-op relais Steam** — phase alpha, pas prototype (conforme GDD §12 : le slice valide le fun, l'alpha valide la boucle complète). Grâce au lockstep sur sim déterministe, le netcode n'échange que des inputs (~quelques octets/tick/joueur) : pas de réplication d'état, pas de serveur dédié, le SDR de Valve fait le NAT traversal et le chiffrement. L'interface transport maison rend GodotSteam remplaçable et permet le fallback ENet en une ligne. Un **spike d'une semaine au sprint 1** purge l'inconnu GodotSteam tôt (mitigation n°3 de l'Étude moteur §4).

**g) Portabilité mobile — des contraintes, pas du travail.** On ne porte rien au slice ; on s'interdit de fermer la porte : trois entrées de jeu maximum (déjà un principe de design, GDD §4.3 — la grammaire est portable par construction), couche d'input abstraite (la sim reçoit des *commandes*, jamais des événements clavier), UI ancrée et scalable (thème unique, tailles en unités relatives, zones de toucher ≥ 48 px dès la conception), et l'interdit du C# (§1.3). Le coût aujourd'hui est nul ; le coût de s'en apercevoir en 2027 ne le serait pas.

---

## 3. JALON 0 — « LE JOUET » (3 semaines : 13 juillet → 31 juillet 2026)

**Le pari.** Le pilier n°1 — la boule de neige — est le fantasme central : *« si le joueur ne sent pas sa puissance grossir minute après minute, on a raté le jeu »* (GDD §1). C'est aussi le pilier le moins cher à tester : il n'a besoin ni d'ennemis, ni d'objectifs, ni de méta. Le Jalon 0 construit **un jouet, pas un jeu** : un Conteur qui se déplace, un cortège qui suit en flux (le banc de poissons de l'annexe systèmes §1.1), des exemplaires à ramasser au sol, des fusions qui éclatent quand trois récits convergent — et le juice minimal qui rend ça vivant.

**Contenu (et rien d'autre) :**

| Semaine | Livrable |
|---|---|
| 1 | micro-benchmark du budget tick (500 entités fixed-point à 30 Hz, mesuré avant toute feature — alimente le critère plan B §1.4) ; squelette du noyau sim : tick fixe, fixed-point 32.32, API gelée ; déplacement du Conteur + cortège en flux (séparation, cohésion, suivi) |
| 2 | ramassage d'exemplaires posés au sol ; fusion 3 → 1 avec son moment de gloire (flash, onde, silhouette qui grandit, strate musicale ajoutée — l'audio du GDD §10 en version 3 pistes) ; interpolation présentation/sim propre |
| 3 | juice : zoom automatique léger quand le cortège grossit (Phantom Camera), variations de silhouettes par rôle (capsules teintées suffisent — pas d'assets), bruit de foule proportionnel à la taille ; golden replay n°1 enregistré et branché en CI tri-OS |

**Critère de sortie — un seul, binaire :** se déplacer avec **15 figures** est déjà agréable **sans aucun objectif de jeu**. Le test : chaque membre de l'équipe (et 3–4 proches naïfs) tient le pad 5 minutes ; si personne ne lâche un sourire ou un « oh » à une fusion, le feel n'y est pas. **Si ce n'est pas agréable, on itère ici — pas plus loin.** Chaque semaine passée à améliorer le flux du cortège au Jalon 0 en économise trois au slice ; l'inverse n'est pas vrai. Le Jalon 0 peut s'étendre à 5 semaines maximum avant de poser la question qui fâche (le *feel* du cortège est-il le bon fantasme ?) — au-delà, c'est un signal de pivot au sens du GDD §13, pas un problème technique.

**Ce que le Jalon 0 prouve en secret :** le benchmark tick (plan B), le déterminisme en CI dès le premier commit (§3.6), et la séparation sim/présentation sous charge réelle. Le jouet est aussi le banc d'essai de toute l'architecture du §2.

---

## 4. BACKLOG DU VERTICAL SLICE (8 sprints × 2 semaines : 3 août → 20 novembre 2026)

**Périmètre du slice** (gate GDD §12 : *70 % des playtesteurs relancent une run sans y être invités*) : **une Ère** — la Grèce des aèdes, « le Chant interrompu » (bible §7) — parcourue en carte à nœuds, **7 figures Europe** (Héraclès, Guillaume Tell, Jeanne d'Arc, Ulysse en départ ; Orphée, Marco Polo, Dédale débloquées d'office pour le playtest), **3 types de nœuds** (combat standard : la Plage d'Ilion ; combat d'élite : les Thermopyles ; événement : l'Oracle de Delphes), **le Léthé simplifié** (2 phases, Défusion incluse — c'est la signature du jeu, elle est non négociable même simplifiée), et **l'Éloge funèbre en version texte**. Toutes les valeurs chiffrées sortent de l'annexe équilibrage v0.1, sans exception : le classeur de référence est la source, le code est le miroir.

### Sprint 1 (03–14/08) — Fondations et spike Steam

*Objectif : le socle du §2 existe en vrai, l'inconnu GodotSteam est purgé.*

- **T1.1** Flux RNG séparés (draft/apparitions/dégâts) — *accepté si :* deux runs sur la même seed avec des combats différents produisent des propositions de draft identiques (test gdUnit4).
- **T1.2** Format replay v1 (en-tête + inputs en ticks) + enregistrement/relecture — *accepté si :* un replay rejoué produit le même hash final ; taille < 50 Ko pour 25 min simulées.
- **T1.3** CI complète : import headless, tests, golden replays tri-OS, export Win/Linux — *accepté si :* un commit qui casse le déterminisme fait échouer la CI en < 15 min.
- **T1.4** Spike GodotSteam (1 semaine, timeboxé) : lobby, échange d'inputs entre 2 machines via SDR — *accepté si :* démo jetable fonctionnelle OU blocage documenté (entrée du critère plan B).
- **T1.5** Télémétrie v0 : événements horodatés en JSON local (voir §5.2) — *accepté si :* une run produit un fichier lisible par le script d'analyse.

**Risque du sprint :** le spike Steam déborde sur les fondations — mitigation : timebox strict, une personne dédiée, les autres ne l'attendent pas.

### Sprint 2 (17–28/08) — Le combat

*Objectif : on se bat, et le chaos est lisible.*

- **T2.1** Trois familles d'Oublis : Silences (nuée mêlée), Ratures (tireurs + zones barrées), Censeurs (scellent gisements/Volumes) — stats bible §6 / annexe équilibrage §1 — *accepté si :* TTK d'un Silence ≤ 2 s sous cortège médian (test simulé).
- **T2.2** Trois figures jouables : Héraclès, Tell, Jeanne (stats annexe §4.1) — *accepté si :* chaque figure passe la règle des 100 points dans le classeur.
- **T2.3** Esquive du Conteur (i-frames courtes, recharge) + scission brève du cortège — *accepté si :* fenêtre d'i-frames vérifiable en replay tick à tick.
- **T2.4** Rendu de masse MultiMesh (300 Oublis + projectiles) — *accepté si :* 60 fps stables sur la machine de référence (GTX 1060 / équivalent portable) avec 24 figures + 300 Oublis.
- **T2.5** Lisibilité v1 : palette cortège chaud / ennemis froids, test silhouettes en aplat noir (GDD §10) — *accepté si :* un observateur nomme le rôle de chaque figure en < 0,5 s sur capture.

**Risque du sprint :** le chaos illisible — mitigation : le test d'aplat est un ticket, pas une opinion.

### Sprint 3 (31/08–11/09) — Draft, fusion, Ferveur

*Objectif : la boucle manche complète — récolter, drafter, fusionner.*

- **T3.1** Volumes + draft 1 parmi 3 depuis le roster, pondération de pitié (GDD §4.1) — *accepté si :* jamais plus de N coffres sans revoir un archétype possédé en double (test statistique sur 10 000 tirages du flux draft).
- **T3.2** Fusion T1→T2→T3 avec règles de l'annexe §2 (× 3 PV/dégâts, × 2,5 soins, × 1,25 contrôles) — *accepté si :* les valeurs en jeu correspondent au classeur à ± 0 (générées, pas recopiées).
- **T3.3** Économie de Ferveur : gisements, drops, coût des Volumes 60 + 20 (annexe §6) — *accepté si :* le revenu médian d'une manche jouée normalement tombe dans 160–220.
- **T3.4** Choix de branche T3 (A/B) sur les 3 figures existantes, en écran de choix simple — *accepté si :* les deux branches de Tell produisent les DPS prévus (annexe §4.3).
- **T3.5** Plafond 24 figures + conversion de l'excédent en Ferveur — *accepté si :* testable en replay.

**Risque du sprint :** le draft casse le rythme du combat — mitigation : le temps monde ne s'arrête pas pendant le draft (comme Squad Busters), à tester dès la première itération.

### Sprint 4 (14–25/09) — La manche complète — ⚠ gate plan B

*Objectif : la dramaturgie 3 min 45 de l'annexe systèmes §1.2 tient debout.*

- **T4.1** Objectif de manche « vagues » avec courbe adverse budgétée en Silences-eq (annexe §5.1 : vague ~55 % du cortège, pic ~90 %) — *accepté si :* le cortège médian ne perd pas de figure hors erreur avant le pic (mesuré en playtest interne).
- **T4.2** La Brume : limite mouvante, 10 % PV max/s, avance à l'horloge de la manche — *accepté si :* la phase d'extraction crée une urgence mesurable (télémétrie : 80 % des sorties dans les 45 dernières secondes).
- **T4.3** Le dernier Volume exposé (« le coffre de trop ») — *accepté si :* placé de sorte qu'il coûte un passage dans la zone menacée par la Brume.
- **T4.4** Enchaînement manche → écran de transition → manche suivante, état du cortège persistant — *accepté si :* un replay couvre une run de 3 manches sans divergence de hash.
- **T4.5** **Revue plan B** : budget tick mesuré en charge nominale, décision Go/No-Go Godot documentée — *accepté si :* la décision est écrite, chiffrée, signée (dernier jour du sprint, 25/09).

**Risque du sprint :** c'est LE sprint du critère plan B — si le tick dépasse 2 × 4 ms après optimisations, on bascule (§1.4). Mitigation : les boucles chaudes identifiées au profiling du sprint 2 ont déjà leur port GDExtension esquissé.

### Sprint 5 (28/09–09/10) — Le routing et les 3 nœuds

*Objectif : la run existe — la carte à embranchements devient le second espace de skill (GDD §3).*

- **T5.1** Carte à nœuds de l'Ère (4–5 nœuds + boss, embranchements) — *accepté si :* au moins 2 chemins distincts par run, générés par le flux apparitions (seed → même carte pour tous).
- **T5.2** Nœud élite : les Thermopyles — défilé étroit, 1 Anachronisme (kit miroir Cogneur), récompense majorée (annexe §5.1 : élite ≈ 120 % de la capacité) — *accepté si :* taux de victoire interne 40–60 % au premier essai.
- **T5.3** Nœud événement : l'Oracle de Delphes — 3 prophéties voilées, modificateur de run (bible §7) — *accepté si :* 3 prophéties implémentées, tirées du flux draft.
- **T5.4** Figures 4 et 5 : Ulysse, Orphée (stats annexe §4.1) — *accepté si :* règle des 100 points.
- **T5.5** Défaite = fin de run, écran sommaire provisoire — *accepté si :* la boucle macro se referme sans crash sur 20 runs consécutives.

**Risque du sprint :** la variété perçue entre deux runs est trop faible avec 3 types de nœuds — mitigation : la variance vient du draft et de l'Oracle, pas du nombre de nœuds ; on le vérifie au playtest interne avant d'ajouter du contenu.

### Sprint 6 (12/10–23/10) — Le Léthé simplifié

*Objectif : la signature du jeu — l'oubli mécanisé — en 2 phases.*

- **T6.1** Arène du delta : eau qui monte par paliers, surface sèche −15 %/phase (annexe §5.2) — *accepté si :* lisible en un coup d'œil (test aplat).
- **T6.2** **La Défusion** : 1,5 s cumulées dans l'eau = −1 tier — *accepté si :* la perte est spectaculaire ET lisible (la Légende *redevient* visiblement Héros), vérifiable en replay.
- **T6.3** Phases 1 (les Méandres + Noyés) et 3 (la Crue, fenêtres de dégâts 3 × 25 s) — la phase 2 (Noyés illustres) est coupée du slice — *accepté si :* durée du combat 4–5 min pour un cortège cible fin d'Ère (~25 000 PV de boss, annexe §5.2).
- **T6.4** Capacité de Cortège v1 (la grande geste du porte-étendard) pour les 5 figures existantes — *accepté si :* la 3ᵉ entrée de jeu est utilisée dans > 70 % des tentatives de boss (télémétrie).
- **T6.5** Récompense : une Réminiscence (relique simple) + transition vers l'Éloge — *accepté si :* la boucle victoire se referme.

**Risque du sprint :** la Défusion frustre au lieu de motiver — c'est un risque de design, pas de code. Mitigation : playtest interne dédié mi-sprint ; la variable d'ajustement est le temps d'immersion (1,5 s), jamais la suppression de la mécanique.

### Sprint 7 (26/10–06/11) — L'Éloge, la télémétrie, le rythme

*Objectif : la fin de run donne envie de raconter — et de relancer.*

- **T7.1** **L'Éloge funèbre en version texte** : génération du récit de run depuis la télémétrie de sim (« Au troisième jour, Héraclès devint Légende… », annexe systèmes §1.4), stats en marge — *accepté si :* 10 runs produisent 10 récits distincts et justes (les faits cités sont vérifiables dans le replay).
- **T7.2** Figures 6 et 7 : Dédale, Marco Polo — *accepté si :* règle des 100 points ; les 6 rôles sont couverts sauf Récolteur ou Bâtisseur selon arbitrage (7 figures pour 6 rôles).
- **T7.3** Télémétrie v1 complète (liste §5.2) + script d'agrégation — *accepté si :* le tableau de bord du playtest sort en une commande.
- **T7.4** Écran de fin → bouton « nouvelle run » sans friction (< 5 s pour relancer) — *accepté si :* chronométré. C'est l'instrument de mesure du gate : la relance doit être *possible* sans être *suggérée*.
- **T7.5** Passe audio : strates musicales par taille de cortège (5 paliers), assourdissement près des Silences — *accepté si :* un testeur yeux fermés estime la taille de son cortège à ± 4.

**Risque du sprint :** l'Éloge généré sonne mécanique — mitigation : gabarits de phrases écrits par l'humain qui tient la plume de la bible, remplis par la machine ; jamais l'inverse.

### Sprint 8 (09–20/11) — Équilibrage, polish, build de gate

*Objectif : le slice est jouable par des inconnus sans nous dans la pièce.*

- **T8.1** Passe d'équilibrage complète contre les cibles de l'annexe §10 (victoire A0 : 55–65 % après 10 runs, durée de manche 3:20–3:50) — *accepté si :* mesuré sur ≥ 40 runs internes.
- **T8.2** Onboarding minimal : 3 écrans de contrôle, pas de tutoriel (les orphelins de Squad Busters connaissent la grammaire) — *accepté si :* un naïf atteint la manche 2 sans aide verbale.
- **T8.3** Stabilité : 0 crash sur 50 runs consécutives (soak test automatisé en headless, inputs aléatoires seedés) — *accepté si :* le soak passe 3 nuits de suite.
- **T8.4** Build de gate : export Windows signé, distribution testeurs (Steam playtest privé ou build direct), consentement télémétrie — *accepté si :* installation < 5 min chez un testeur distant.
- **T8.5** Golden replays v2 : 5 runs de référence couvrant draft, boss, Défusion, Éloge — gelés comme oracle de non-régression pour l'alpha.

**Risque du sprint :** le polish mange l'équilibrage (ou l'inverse) — mitigation : T8.1 est verrouillé en semaine 1 du sprint, le polish n'a que la semaine 2, et la liste de la dette (§6) est affichée au mur pour refuser tout ajout.

---

## 5. DEFINITION OF DONE & PROTOCOLE DE PLAYTEST

### 5.1 Definition of Done du slice

Le slice est « done » quand **tout** ceci est vrai :

1. Une run complète (4–5 nœuds + Léthé) se joue au pad et au clavier-souris, victoire et défaite comprises, sans crash ni aide verbale.
2. Les 7 figures passent la règle des 100 points ; les cibles de santé de l'annexe §10 (victoire, durée de manche) sont dans les fourchettes sur ≥ 40 runs mesurées.
3. **Le déterminisme est prouvé, pas promis** : la CI golden replays tri-OS est verte depuis ≥ 4 semaines consécutives, et une run jouée sur la machine A rejouée sur la machine B produit le même hash final.
4. Chaque run produit un replay < 50 Ko rejouable et un Éloge funèbre texte dont chaque fait est vérifiable dans ce replay.
5. La télémétrie complète (§5.2) est active, consentie, et son tableau de bord sort en une commande.
6. Le build s'installe chez un inconnu en < 5 min et le soak test de 50 runs passe 3 nuits de suite.

### 5.2 Le protocole de playtest — mesurer « relance sans y être invité »

**Cohorte.** **16 testeurs minimum, en deux vagues de 8** (semaines du 23/11 et du 30/11) — la vague 2 permet de corriger un défaut évident révélé par la vague 1 sans invalider la mesure. Recrutement conforme au GDD §2 : moitié orphelins de Squad Busters (subreddits, Discords d'anciens clubs — c'est aussi le début de la relation communautaire), moitié joueurs de roguelites (Vampire Survivors, Brotato). Aucun ami de l'équipe dans la cohorte de mesure.

**Le rituel de mesure.** Session à distance, 60 minutes, écran partagé, l'observateur se tait. Consigne unique : *« Joue une run, on discutera après. »* À la fin de la première run (victoire ou défaite), l'observateur dit exactement : *« Merci, c'est tout ce qu'il nous fallait — on peut discuter quand tu veux. »* — puis ne dit plus rien pendant 90 secondes. **La relance compte si le testeur lance une nouvelle run de lui-même dans ces 90 secondes** (ou demande explicitement à continuer). Le gate GDD §12 : **≥ 70 % de relance** (soit ≥ 12/16). Entre 50 et 70 % : on itère 4 semaines sur les retours et on refait une vague complète. Sous 50 % deux vagues de suite : règle d'arrêt du GDD §13 — pivot ou arrêt, sans acharnement.

**Télémétrie minimale — câblée dès le prototype** (v0 au sprint 1, v1 au sprint 7), locale, anonyme, consentie, un JSON par run :

| Événement | Champs | Ce qu'il mesure |
|---|---|---|
| `run_start` / `run_end` | seed, roster, durée, issue, manche atteinte | complétion (cible GDD §13 : > 60 %) |
| `draft_pick` | propositions, choix, temps de décision | santé du draft, figures ignorées |
| `fusion` / `branche_t3` | figure, tier, timing dans la manche | dilemme « fusionner ou attendre » réel ? |
| `node_choice` | options, choix, élites évitées/prises | le routing est-il un espace de skill ? |
| `mort_figure` / `defusion` | cause, phase | courbe de difficulté, frustration Léthé |
| `eloge_vu` | durée d'affichage, partage/copie | l'Éloge est-il lu ou zappé ? |
| `relance` | délai depuis `run_end`, spontanée o/n | **LA métrique du gate** |

Le fichier est relevé après la session ; aucune infrastructure serveur n'est requise pour le slice — le service scores/replays (§2.3e) n'entre en scène qu'à l'alpha.

---

## 6. LA DETTE ASSUMÉE — ce que le slice ne fait PAS

Cette liste protège les 4 mois. Elle est affichée, elle est publique en interne, et tout ajout à son périmètre passe par un arbitrage écrit — pas par un « tant qu'on y est ». Chaque ligne est *de la dette*, pas *de l'oubli* : l'architecture du §2 garantit que rien ci-dessous n'exige de réécriture pour arriver plus tard.

| On ne fait pas | Pourquoi c'est tenable | Quand |
|---|---|---|
| **Pas de netcode ni de co-op** — le slice est strictement solo | le lockstep n'échange que des inputs : la sim déterministe EST la préparation du co-op ; le spike du sprint 1 a purgé l'inconnu | alpha |
| **Pas de service scores/replays en ligne** — replays locaux + CI seulement | le format replay est gelé au sprint 1 ; le service n'est qu'un réceptacle du même fichier | alpha |
| **Pas d'Épreuve hebdomadaire ni de Panthéon** | tout ce qui la rend possible (seed partagée, replay, hash) est prouvé en CI dès le slice | alpha |
| **Pas de 2ᵉ continent, pas d'Asie, pas d'Ère II** — une seule Ère grecque | le pipeline de contenu (nœuds, familles d'Oublis, boss) est le livrable caché du slice | alpha → EA |
| **Pas de méta-progression** — ni Chroniques, ni Encre, ni Chapitres, ni Éloges de maîtrise, ni Ascensions : les 7 figures sont données | le gate mesure l'envie de relancer *une run*, pas une économie méta ; brancher l'Encre sur `run_end` est trivial ensuite | alpha |
| **Pas de Bibliothèque (hub)** — menu sec : roster → run → Éloge → menu | le hub est de la présentation pure, zéro impact sim | alpha |
| **Pas de 8ᵉ figure, pas de coffre sauvage, pas de marché ni de sanctuaire** (3 types de nœuds seulement) | la densité décisionnelle du slice vient du draft + Oracle ; on ajoute des nœuds quand le gate a validé le cœur | alpha |
| **Pas de phase 2 du Léthé** (les Noyés illustres) ni d'Astérion | teasing et générosité narrative — précieux, non nécessaires au fun de la fusion | alpha/EA |
| **Pas de DA de production** — capsules teintées, silhouettes par rôle, un seul décor ; le papier découpé attend | le test d'aplat (T2.5) valide la *lisibilité*, pas la beauté ; produire des assets avant le gate est le gaspillage type | après le gate |
| **Pas d'Éloge illustré ni partageable** — texte seul | le générateur de récit est le travail dur ; l'image-carte virale (annexe §3.5) est une couche au-dessus | EA |
| **Pas de localisation** — français uniquement | cohorte de test francophone ; l'anglais arrive avec le Néofest | alpha/EA |
| **Pas de mobile, pas de build console** — Windows (+ export Linux en CI) | les contraintes de portabilité (§2.3g) sont respectées, c'est tout ce qu'on se doit | 2027+ |
| **Pas d'options d'accessibilité avancées ni de remapping complet** — presets pad/clavier | la couche d'input abstraite (§2.3g) rend le remapping mécanique plus tard | alpha |
| **Pas de PvP, évidemment** | GDD §8 : strictement conditionnel, après toutes les gates | phase 2 |

**La règle qui chapeaute tout :** si une idée géniale surgit pendant le slice, elle rejoint le backlog de l'alpha avec une ligne de justification — le slice n'a qu'un seul client, le gate des 70 %.

---

## Récapitulatif du calendrier

| Jalon | Dates | Sortie |
|---|---|---|
| **Jalon 0 — le Jouet** | 13/07 → 31/07/2026 | 15 figures agréables sans objectif, benchmark tick, CI déterminisme verte |
| **Sprints 1–4** | 03/08 → 25/09/2026 | fondations, combat, draft/fusion, manche complète — **revue plan B le 25/09 (non-retour)** |
| **Sprints 5–8** | 28/09 → 20/11/2026 | routing, Léthé, Éloge, build de gate |
| **Playtest de gate** | 23/11 → 04/12/2026 | 16 testeurs, 2 vagues — **gate : ≥ 70 % de relance spontanée** |
| Gate verte → | décembre 2026 | lancement de l'alpha fermée (GDD §12) : co-op relais Steam, service scores, 10 archétypes |

---

*Document vivant. Les hypothèses chiffrées (budget tick 4 ms, replay < 50 Ko, machine de référence) sont mesurées au Jalon 0 et corrigées ici même ; toute modification de l'architecture du §2 exige une revue au regard de l'annexe systèmes §3.6 — le Panthéon est le client de cette roadmap. Prochaine révision : après la revue plan B du 25/09/2026.*
