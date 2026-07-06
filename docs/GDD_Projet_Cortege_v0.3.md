# PROJET CORTÈGE — Game Design Document

**Version 0.3 — Document de travail**
*v0.3 : progression par continents (Europe / Asie), périmètre EA porté à 2 continents × 2 Ères, Épreuve au meilleur de 3. Documents compagnons : Bible d'univers v0.2, Annexe systèmes v0.2.*

---

## 1. Vision

**High concept.** Un action-roguelite en coopération où votre escouade grossit en fusionnant ses membres : partir seul, finir à la tête d'un cortège qui remplit l'écran. Le plaisir immédiat et chaotique de Squad Busters, avec l'agentivité en plus et le hasard subi en moins.

**Pitch en une phrase.** *« Le successeur spirituel de Squad Busters que Supercell ne fera jamais : premium, équitable, construit avec sa communauté. »*

**Fiche d'identité**

| | |
|---|---|
| Genre | Action-roguelite à escouade, vue top-down 3/4 |
| Joueurs | 1 à 4 en coopération (phase 1), PvP 8 escouades (phase 2, conditionnelle) |
| Plateforme | PC / Steam d'abord ; architecture d'inputs compatible mobile pour un portage ultérieur |
| Format de session | Runs de 20–30 min composées de manches de 3–4 min |
| Modèle | Premium (~15 €), cosmétiques optionnels, zéro puissance vendue |
| Équipe cible | 2 à 4 personnes, 12–18 mois jusqu'à l'accès anticipé |

**Les quatre piliers**

1. **La boule de neige.** Le fantasme central est la croissance visible : chaque coffre, chaque fusion rend le cortège plus gros, plus bruyant, plus spectaculaire. Si le joueur ne *sent* pas sa puissance grossir minute après minute, on a raté le jeu.
2. **Du choix, pas du tirage.** Chaque coffre est un draft depuis un deck que le joueur a construit. La variance crée la surprise, jamais l'injustice. C'est la correction directe du défaut n°1 de Squad Busters.
3. **Le chaos lisible.** L'écran peut être saturé, la décision doit rester claire en un coup d'œil. La lisibilité est une contrainte de design au même titre qu'une mécanique.
4. **Le respect du joueur.** La progression récompense la maîtrise et la collection, jamais le portefeuille. Ce pilier est aussi notre positionnement marketing : il est gravé publiquement et non négociable.

---

## 2. Cible et positionnement

**Cible primaire : les orphelins de Squad Busters.** Le jeu ferme ses serveurs mi-2026 en laissant une communauté active (subreddits, Discord d'anciens clubs) sans destination. Profil : 16–35 ans, attachés au *feel* du jeu (matchs courts, fusion, chaos joyeux) mais échaudés par le RNG des coffres, la progression type machine à sous et les évolutions payantes. Cette communauté est notre canal d'acquisition : recrutement direct des testeurs alpha sur leurs espaces, développement en public, crédit visible des contributeurs.

**Cible secondaire : les joueurs de roguelites coopératifs** (Vampire Survivors, Brotato, Deep Rock Galactic Survivor). Ils apportent le volume Steam ; le hook « draft + fusion + escouade » n'existe pas encore dans leur bibliothèque.

**Positionnement.** Aucun titre n'occupe le croisement exact : escouade qui grossit par fusion × draft maîtrisé × co-op courte session × premium équitable. Notre différence n'est pas le budget, c'est le contrat de confiance.

---

## 3. Boucle de jeu

**Boucle macro.** Menu → composition du roster (8 archétypes) → run sur carte à embranchements (les Ères du continent choisi : 2 à l'accès anticipé, 3 à la 1.0) → boss final → récompenses méta (monnaie de collection, défis) → nouvelle run.

**Boucle micro — une manche (3–4 min).** Entrer dans l'arène → explorer et récolter la ressource → ouvrir des coffres (draft 1 parmi 3) → fusionner et se renforcer → gérer l'objectif de la manche (vagues, escorte, chasse au trésor, survie) → extraction chronométrée. La manche reprend le rythme exact d'un match de Squad Busters : c'est l'ADN à préserver.

**Entre les manches — le routing.** Une carte à nœuds façon Slay the Spire relie les manches : combat standard, combat d'élite (récompense majorée), marché, événement narratif, sanctuaire (soin/réorganisation), nœud inconnu. Le choix d'itinéraire est le second espace de skill du jeu : le joueur arbitre en permanence risque contre récompense, ce que Squad Busters n'offrait jamais.

---

## 4. Systèmes clés

### 4.1 Roster et draft — la correction du RNG

Avant la run, le joueur compose un **roster de 8 archétypes** parmi sa collection. En jeu, chaque coffre propose **3 cartes tirées de ce roster**, avec une pondération de pitié garantissant l'accès aux fusions (jamais plus de N coffres sans revoir un archétype déjà possédé en double). Un unique **coffre sauvage** par acte propose des archétypes hors roster : la dose de surprise, contrôlée et localisée.

Résultat : la variance vit *dans* la partie, le contrôle vit *dans* la préparation. Le joueur qui perd sait pourquoi il a perdu.

### 4.2 La fusion

Trois exemplaires identiques fusionnent en tier supérieur (T1 → T2 → T3). La fiction porte la mécanique : chaque exemplaire est un *récit* de la même figure, et leur convergence fait grandir le mythe — **T1 le Personnage, T2 le Héros, T3 la Légende**. Au passage T3, le joueur **choisit entre deux versions du mythe** (branche A ou B) : la spécialisation remplace la loterie des évolutions de Squad Busters. La décision de timing reste un vrai dilemme : fusionner tôt donne la puissance immédiate, retenir garde la flexibilité de draft.

### 4.3 L'agentivité — trois entrées, pas une de plus

Déplacement, **esquive** (i-frames courtes, temps de recharge), et **Capacité de Cortège** : un ultime dont l'effet est déterminé par le « porte-étendard », l'unité T3 que le joueur désigne. Peu d'inputs, beaucoup de décisions — la grammaire reste portable sur mobile sans refonte, et le plafond de compétence vient du positionnement, du timing d'esquive, du choix de porte-étendard et du routing, pas des APM.

### 4.4 Économie in-run

Une ressource unique, la **Ferveur** — l'attention des vivants, qui filtre jusque dans la Grande Mémoire —, est récoltée sur les ennemis et les gisements ; elle ouvre les coffres et paie le marché. La tension récolte contre combat — s'exposer pour s'enrichir — est le meilleur héritage de Squad Busters et doit rester au centre de chaque arène.

---

## 5. Structure d'une run

Le joueur choisit un **continent de départ** (Europe ou Asie) ; une run traverse les Ères de ce continent — deux à l'accès anticipé, trois à la 1.0 —, chacune de 4 à 5 nœuds close par un boss. Durée cible : 18 à 25 minutes (EA), 25 à 30 (1.0). Compléter un continent (tous ses boss d'Ère vaincus) rouvre **les Routes** : l'autre continent s'ouvre, et les figures peuvent se mélanger — le **Cortège-Monde**, fantasme de fin de jeu. L'échec termine la run (règle roguelite), mais la monnaie de collection est conservée. Après la 1.0, une échelle d'**Ascensions** (modificateurs de difficulté cumulatifs) assure la rejouabilité des vétérans sans inflation de contenu.

---

## 6. Méta-progression

Ce que la progression débloque : nouveaux archétypes (par défis de gameplay, pas par grind pur), évolutions alternatives, reliques de départ (des *choix* de style de jeu, jamais des +X % bruts), cosmétiques. Ce qu'elle ne débloque jamais : de la puissance achetable, des minuteurs, de l'énergie. Collection cible : 16 figures à l'accès anticipé (8 par continent), ~40 à terme.

---

## 7. Archétypes — échantillon de rôles

Six rôles structurent le roster (« archétype » désigne ici l'unité jouable, incarnée par une figure historique ou mythique). Un exemple par rôle ci-dessous ; le casting complet des 16 figures de lancement, avec kits et branches, est détaillé dans la bible d'univers.

| Rôle | Figure (exemple) | Fantasme | Légende T3 — branche A / B |
|---|---|---|---|
| Cogneur | Héraclès *(mythe grec)* | tenir la ligne de front | la Peau du Lion (aura de garde) / la Massue d'Érymanthe (frappe de zone) |
| Tireur | Guillaume Tell *(légende suisse)* | précision à distance | la Pomme (critique garanti sur cible marquée) / le Second Carreau (exécution des cibles affaiblies) |
| Soutien | Jeanne d'Arc *(histoire, France)* | rallier et protéger | les Voix (aura de soin) / l'Étendard (ralliement offensif) |
| Récolteur | Crésus *(histoire, Lydie)* | accélérer l'économie | le Pactole (traînée qui convertit en Ferveur) / Riche comme Crésus (intérêts sur la réserve) |
| Filou | Ulysse *(mythe grec)* | ruse, mobilité, vol | Personne (le cortège perd l'aggro) / le Cheval (leurre monumental piégé) |
| Bâtisseur | Dédale *(mythe grec)* | contrôle de zone | le Labyrinthe (murs qui égarent) / les Ailes (bref envol du cortège) |

Chaque rôle possède une silhouette et une teinte propres : la composition d'un cortège doit se lire en une demi-seconde, y compris chez l'adversaire en PvP.

---

## 8. PvP — phase 2, strictement conditionnelle

Format « Bousculade » : 8 escouades dans une arène partagée, 4 minutes, extraction des survivants les plus riches. Les lobbies sont complétés par des bots crédibles dès le premier jour — un indé ne peut pas promettre un matchmaking instantané, il peut promettre des parties qui démarrent.

Règle de gouvernance : le PvP ne se lance **que si** les indicateurs PvE des §12–13 sont atteints. Le PvE est le produit ; le PvP est un mode. Inverser cet ordre est exactement l'erreur de calendrier qui a tué l'original.

---

## 9. UNIVERS — la Grande Mémoire *(arrêté en v0.2)*

**Décision.** Parmi les trois pistes étudiées en v0.1 (micro-monde, folklore, cuisine), la direction retenue est une évolution de la proposition « Cortège » : non plus les esprits du folklore, mais **les mythes et les héros de l'Histoire**. Les pistes écartées restent archivées dans la v0.1.

**Le monde.** Tous les récits que l'humanité s'est racontés vivent dans **la Grande Mémoire**, un pays stratifié en Ères. Quand une histoire cesse d'être racontée, **les Oublis** — créatures de brume et de rature — la dévorent. Le joueur incarne **le Conteur**, qui traverse les Ères pour rallumer les légendes : chaque figure recrutée rejoint son cortège, et la Ferveur fait tourner l'économie comme la fiction.

**Pourquoi ce choix est plus fort que le folklore seul :**

- **Reconnaissance maximale.** Tout le monde connaît Jeanne d'Arc, Héraclès ou Ulysse ; la joie du crossover — l'atout n°1 de Squad Busters — est reconstruite avec un budget de licence nul, le domaine public servant de catalogue.
- **Preuve de marché.** Le mélange héros historiques × figures mythiques est un fantasme de collection éprouvé (Fate/Grand Order, Smite, Civilization).
- **La fiction porte la fusion.** Trois exemplaires = trois récits d'une même figure ; leur convergence fait grandir le mythe (Personnage → Héros → Légende), et les branches T3 sont deux versions du mythe. Le système de tiers raconte littéralement comment l'Histoire devient légende.
- **Un pipeline auto-marketé.** Chaque acte est une époque-civilisation ; chaque mise à jour parle d'elle-même à une communauté culturelle.

**Garde-fous éditoriaux (non négociables).** Figures décédées avant ~1900 uniquement ; aucune divinité, prophète ou fondateur de religion vivante — les panthéons éteints (grec, nordique, égyptien) sont admissibles ; traitement héroïque-légendaire, jamais satirique ; figures à réception contestée exclues du lancement et soumises à une charte au cas par cas. Détail complet dans la bible d'univers.

➡ *Le monde, les Oublis, l'Acte I et le roster de lancement sont détaillés dans le document compagnon : **Bible d'univers v0.1**.*

---

## 10. Direction artistique

Style **art naïf / papier découpé / gouache**, inspiré des ex-voto et de l'imagerie d'Épinal — un langage visuel populaire, chaleureux, dans le domaine public, et à des années-lumière du rendu 3D toon de Supercell : impossible de nous accuser de copier, impossible de nous confondre. Rendu 2.5D en vue top-down 3/4. Chaque Ère emprunte en outre son motif décoratif à l'art populaire de sa culture — céramique à figures noires pour la Grèce, estampes pour le Japon, tapisserie pour l'Europe médiévale — sur la base graphique commune du papier découpé.

**Règles de lisibilité (non négociables) :**

- une silhouette unique par rôle, testée en aplat noir ;
- le tier se lit par la taille et l'ornementation (T3 = auréole, bannière), jamais par un chiffre flottant ;
- palette : cortège saturé et chaud, ennemis désaturés et froids, ressource en teinte unique réservée ;
- budget de particules par écran plafonné — le spectaculaire vient du *nombre* d'unités, pas du bruit visuel ;
- caméra fixe, zoom léger automatique quand le cortège grossit (la croissance se ressent aussi par le cadre).

**Audio.** Le cortège est un instrument : chaque héros ajoute une strate à la musique (percussions, chœurs, fifres). Plus l'escouade grossit, plus l'orchestration s'épaissit. La boule de neige doit s'*entendre*.

---

## 11. Modèle économique

Premium **14,99 €** en accès anticipé, **19,99 €** à la 1.0. Tout le contenu de jeu (régions, archétypes, modes) est gratuit après achat. Revenus complémentaires : packs cosmétiques optionnels et pack de soutien. Promesse publique, affichée sur la page Steam : *aucune puissance ne sera jamais vendue*. Face à une communauté brûlée par la monétisation de l'original, cette phrase est notre meilleur budget marketing.

---

## 12. Production et jalons (équipe de 2 à 4)

| Phase | Durée | Livrable | Critère de passage (gate) |
|---|---|---|---|
| Prototype (vertical slice, 1 acte) | 4 mois | le fun de la fusion validé manette en main | 70 % des playtesteurs relancent une run sans y être invités |
| Alpha fermée (vétérans Squad recrutés sur Reddit/Discord) | 3 mois | boucle complète, 10 archétypes | rétention J7 > 20 % sur la cohorte alpha |
| Accès anticipé Steam | +7 à 8 mois | 16 figures, 2 continents × 2 Ères, co-op 4 | rétention J30 > 8 %, évaluations > 85 % positives |
| 1.0 | +6 à 9 mois | Ascensions, 3ᵉ Ère par continent, roster ~24 | ventes couvrant 12 mois de runway |
| PvP « Bousculade » | conditionnelle | mode 8 escouades + bots | uniquement si toutes les gates précédentes sont vertes |

**Choix techniques.** Godot 4 (licence libre, export multiplateforme) ou Unity ; co-op via relais Steam en pair-à-pair pour éviter tout coût de serveur dédié — l'infrastructure ne doit jamais pouvoir couler le studio. Démo publique au Steam Néofest dès l'alpha stabilisée.

---

## 13. KPIs et critères d'arrêt

L'anti-leçon Supercell tient en une phrase : **ils ont scalé avant de valider ; nous validons avant chaque euro suivant.** Chaque phase a ses critères chiffrés — et une règle d'arrêt assumée : deux gates consécutives ratées malgré itération = pivot ou arrêt du projet, sans acharnement.

| Indicateur | Seuil alpha | Seuil accès anticipé |
|---|---|---|
| Rétention J1 / J7 / J30 | 45 % / 20 % / — | 40 % / 18 % / 8 % |
| Durée médiane de session | > 30 min | > 35 min |
| Taux de complétion d'une run (acte 1) | > 60 % | > 65 % |
| Diversité de roster (joueurs utilisant ≥ 6 archétypes) | > 50 % | > 60 % |
| Évaluations Steam positives | — | > 85 % |

La diversité de roster est notre indicateur de santé du draft : si tout le monde joue les 8 mêmes cartes, le système de la §4.1 a échoué.

---

## 14. Risques et mitigations

| Risque | Probabilité | Mitigation |
|---|---|---|
| Juridique — ressemblance avec Squad Busters | Moyenne | Les mécaniques ne sont pas protégeables, mais aucun archétype, nom ou asset ne doit évoquer Supercell ; relecture juridique avant toute annonce publique ; figures historiques et mythes = domaine public documenté |
| Sensibilités culturelles autour des figures | Moyenne | Charte éditoriale : décès avant ~1900, aucune figure de religion vivante, traitement légendaire jamais satirique, relecture par aire culturelle avant chaque nouvelle Ère |
| Coût/complexité du netcode | Moyenne | PvE co-op en relais Steam d'abord ; le PvP (et son infrastructure) n'existe qu'après validation |
| DA sous-financée face au marché | Haute | Le style papier découpé est volontairement économe ; test silhouettes/aplats avant toute production d'assets ; un(e) seul(e) artiste DA à temps plein vaut mieux que trois généralistes |
| Saturation du marché roguelite | Haute | Le croisement draft + cortège + co-op est un créneau vide ; démo Néofest et build-in-public pour exister avant la sortie |
| Communauté Squad trop dispersée d'ici la sortie | Moyenne | Présence immédiate sur leurs espaces dès le prototype ; l'alpha fermée EST l'outil de rétention communautaire |

---

*Document vivant. Annexes livrées : **Bible d'univers v0.2** (continents, Ères, roster) et **Annexe systèmes v0.2** (boucles, progression, classement). Prochaines annexes : tableau d'équilibrage T1–T3, wireframes UI du draft.*
