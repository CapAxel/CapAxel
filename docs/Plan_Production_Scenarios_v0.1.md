# CORTÈGE — Plan de Production : Scénarios & Financement

**Version 0.1 — Document compagnon du GDD v0.3**
*Répond à la question que le GDD §12 laisse ouverte : « comment ce jeu sort-il réellement ? » — quatre scénarios chiffrés, une cartographie du financement France/Europe, une recommandation tranchée et un plan des 90 premiers jours. Document frère : Roadmap technique v0.1 (en cours d'écriture).*

---

## 0. Préambule — ce que ce document tranche, et comment le lire

Le GDD §12 fixe le **quoi** et le **quand** : prototype 4 mois → alpha 3 mois → accès anticipé +7-8 mois → 1.0 +6-9 mois, chaque phase fermée par une gate chiffrée (70 % de relance de run, rétention J7 > 20 %, J30 > 8 % et 85 % d'évaluations positives, ventes couvrant 12 mois de runway). Ces gates ne sont **pas renégociées ici** — elles sont l'ossature commune des quatre scénarios. Ce document tranche le reste : **qui** travaille, **avec quel argent**, **au prix de quelles coupes**, et **quand on change de plan**.

Trois règles de lecture :

1. **Tous les chiffres sont datés du 6 juillet 2026** et issus d'une recherche sourcée (notes de bas de page). Toute décision d'engagement — dépôt de dossier, signature, embauche — exige une re-vérification à date.
2. **Les scénarios ne sont pas exclusifs.** Ce sont des postures de départ ; la réalité sera un hybride, et le §4 dit lequel. Chaque scénario indique ses points de jonction avec les autres.
3. **La contrainte d'architecture du GDD §12 et de l'annexe systèmes §3.6** — simulation déterministe à pas fixe dès le prototype — est un invariant de tous les scénarios : elle ne coûte presque rien au jour 1 et vaut de l'or en pitch (replays, Épreuve seedée, anti-triche) comme en dossier d'aide (brique R&D crédible pour un statut JEI[^jei]).

Le calendrier de référence, si la gate du prototype passe et que le financement suit : **slice novembre 2026 → alpha février-mars 2027 → accès anticipé T4 2027 → 1.0 mi-2028.** Cette fenêtre n'est pas arbitraire : les serveurs de Squad Busters ferment entre mi-2026 et fin 2026[^sb], et la communauté orpheline — notre cible primaire (GDD §2) — reste adressable 6 à 12 mois. **Un accès anticipé après mi-2028 rate la fenêtre.** C'est le juge de paix de tout ce qui suit.

---

## 1. Les quatre scénarios

### S1 — « la Lanterne seule » *(bootstrap solo)*

*Le Conteur part sans cortège : un dev seul, un emploi ou des économies à côté, des prestations ponctuelles pour ce qu'une personne ne sait pas faire.*

**Équipe.** 1 personne à 0,5-0,7 ETP (soirs/week-ends, ou temps partiel sur économies) : design + code + intégration. Prestations ponctuelles : art 2D (~45 jours), audio (~20 jours + 12 min de musique), relecture juridique et culturelle.

**Calendrier.** Le jalon « slice 4 mois » du GDD devient **7-9 mois** à mi-temps → slice printemps 2027, alpha été 2027, **accès anticipé T2-T3 2028** (limite haute de la fenêtre Squad Busters), 1.0 courant 2029.

**Budget (cash, hors coût de vie — celui-ci est porté par l'emploi ou les économies).**

| Poste | Montant |
|---|---|
| Rémunération | 0 € (coût d'opportunité assumé, non budgété) |
| Art 2D externalisé (~45 j × 320 €/j[^malt]) | 15 000 € |
| Audio : sound design ~20 j + 12 min de musique à ~350 €/min[^audio] | 12 000 € |
| Sensitivity reading (1 continent)[^sensi] | 1 500 € |
| Matériel/logiciels (Godot gratuit ; Steam Direct, plugins, capture) | 3 500 € |
| Marketing (visuels clés, aide au trailer) | 2 000 € |
| Localisation EN/DE/ES (~10 k mots à 0,10-0,15 $/mot[^loc]) | 3 000 € |
| Juridique/compta (relecture pré-annonce — GDD §14 —, micro-entreprise) | 3 000 € |
| Imprévu (20 % — le taux le plus haut des quatre : pas de filet) | 8 000 € |
| **Total** | **≈ 48 000 €** |

**Plan de financement.** Économies personnelles (~30-40 k€ à provisionner) + **aide à l'écriture FAJV** déposée en tant qu'auteur personne physique, *sans société* — le GDD et la bible constituent déjà le dossier de bible de conception[^fajv] — + revenus de l'emploi. La Bourse French Tech (30 k€) devient accessible dès qu'une société existe[^bft].

**Périmètre coupé — assumé et précis.** Le « 2 continents × 2 Ères, 16 figures, co-op 4 » de l'EA n'est pas finançable seul. EA S1 : **1 continent (l'Europe) × 2 Ères, 8-10 figures, co-op 2 joueurs**, l'Épreuve hebdomadaire **maintenue** (elle est quasi gratuite grâce au déterminisme et c'est l'aimant communautaire), l'Asie et le co-op 4 promis pour la 1.0. Le Cortège-Monde disparaît de l'EA — c'est la coupe la plus douloureuse, elle est réversible.

**Risques propres.** Épuisement (le tueur n°1 du solo à côté d'un emploi) ; calendrier qui glisse hors de la fenêtre Squad Busters ; angle mort art/marketing ; aucun regard critique quotidien. **Mitigations :** gates du GDD §13 appliquées à soi-même sans pitié (deux gates ratées = arrêt) ; build-in-public dès le mois 2 pour créer le regard extérieur ; le style papier découpé, volontairement économe (GDD §10), est précisément dimensionné pour ce scénario.

**Ce scénario est le vôtre si…** vous avez un emploi stable ou 18 mois d'économies, une discipline de fer, et que vous acceptez de sortir plus petit plus tard plutôt que de dépendre de qui que ce soit. C'est aussi le **tronc commun des 4 premiers mois** de tous les autres scénarios (§4).

---

### S2 — « les Deux Récits » *(duo aidé par la puissance publique)*

*Deux récits de la même figure convergent : un profil code/design + un profil art/DA, à temps plein, financés par le stack d'aides françaises — sans éditeur, sans dilution.*

**Équipe.** 2 ETP fondateurs : dev-designer + artiste-DA (la mitigation exacte du risque « DA sous-financée » du GDD §14 : *un(e) seul(e) artiste DA à temps plein vaut mieux que trois généralistes*). Prestations : audio, musique, sensitivity reading, trailer.

**Calendrier.** Le calendrier de référence du GDD tient : slice à M4 (novembre 2026 si départ juillet), alpha M7, **accès anticipé M14-15 (T4 2027)**, 1.0 M22-24 (mi-2028). Seule latence ajoutée : ~2 mois entre dépôt FAJV et commission[^fajv] — absorbable si les dossiers partent pendant le développement, pas avant.

**Budget (24 mois, jusqu'à la 1.0).**

| Poste | Montant |
|---|---|
| Rémunération 2 ETP × 24 mois (~3 500 € chargé/mois — salaires de fondateurs, sous le marché) | 170 000 € |
| Audio : sound design ~40 j + 25 min de musique[^audio] | 25 000 € |
| Art complémentaire (animation, VFX ponctuels) | 10 000 € |
| Sensitivity reading (2 continents : aires grecque/nordique, japonaise/mésopotamienne)[^sensi] | 4 000 € |
| Matériel/logiciels | 8 000 € |
| Marketing (trailer pro, capsules Steam, Néofest, 1-2 salons) | 15 000 € |
| Localisation EFIGS + zh simplifié à la 1.0[^loc] | 12 000 € |
| Juridique/compta (création société, contrats de cession, expert-comptable 24 mois) | 14 000 € |
| Imprévu (15 %) | 40 000 € |
| **Total** | **≈ 300 000 €** |

**Plan de financement — séquencé.**

| Quand | Source | Montant |
|---|---|---|
| M0 (avant société) | Aide à l'écriture FAJV (auteur personne physique, 100 % des coûts éligibles)[^fajv] | 15-25 k€ |
| M0-24 | **ARE des deux fondateurs** (allocation chômage maintenue en création d'entreprise) — hors budget société, couvre une partie du coût de vie | équiv. 40-70 k€ |
| M3 (société créée) | Bourse French Tech (Bpifrance)[^bft] | 30 k€ |
| M4-6 (dossier + slice comme preuve) | Pré-production FAJV (50 % des dépenses de prototypage, moyenne constatée ~80 k€)[^fajv] | 60-80 k€ |
| M8-12 | Aide régionale (IdF ou Nouvelle-Aquitaine : jusqu'à 150 k€ — voir §2.3) | 60-100 k€ |
| M12+ puis annuel | **CIJV : 30 % des dépenses éligibles** (seuil 100 k€ de coût atteint par la masse salariale)[^cijv] | 70-90 k€ (décalé) |
| M15+ | Revenus de l'accès anticipé | le solde |

**Le point dur, gravé :** le total des aides publiques est plafonné à **50 % du coût du jeu**[^fajv] — sur 300 k€, c'est 150 k€ de subventions maximum ; le CIJV, crédit d'impôt notifié hors *de minimis*, s'ajoute par-dessus[^cijv]. Le plan ci-dessus sature ce plafond : c'est voulu, et c'est pour cela que l'apport personnel + ARE + revenus EA restent indispensables. Le régime *de minimis* (300 k€ / 3 exercices glissants) ne mord pas à cette échelle.

**Périmètre.** Si les aides atteignent 130-150 k€ : **le périmètre EA complet du GDD tient** (2 continents × 2 Ères, 16 figures, co-op 4). Si la région ne suit pas (< 100 k€ d'aides totales) : repli sur 2 continents × **1 Ère + la 2ᵉ Ère livrée pendant l'EA** — on préserve le choix de continent et le Cortège-Monde plutôt que la longueur de run.

**Risques propres.** Dépendance au calendrier des commissions (3-4 dépôts/an, ~2 mois de latence — un dossier raté = 4-6 mois perdus) ; conflit de cofondateurs (le tueur n°1 des duos) ; trésorerie en dents de scie (versements 75/25, CIJV décalé d'un an). **Mitigations :** pacte d'associés dès la création ; déposer à *chaque* session sans attendre la perfection du dossier ; ligne de préfinancement du CIJV (des banques et Bpifrance préfinancent les crédits d'impôt agréés).

**Ce scénario est le vôtre si…** vous avez trouvé *la bonne* deuxième personne (artiste-DA engagé·e au projet, pas un prestataire), que l'un de vous au moins a des droits ARE, et que garder 100 % de l'IP et des revenus vaut la paperasse. C'est le scénario au meilleur rapport contrôle/risque du tableau §3.

---

### S3 — « le Mécène » *(vertical slice → signature éditeur)*

*Un mécène de la Grande Mémoire avance la Ferveur — contre une part du récit.*

**Équipe.** Phase 1 (slice, M0-5) : 2-3 personnes en mode S1/S2. Phase 2 (post-signature) : **3-4 ETP** (dev, artiste, + game/level designer, + mi-temps production/commu), prestations audio.

**Calendrier.** Slice M4-5 → **démarchage M5-8** (compter 3-4 mois de pitch, réponses lentes) → signature M8 → accès anticipé **M16-18 (début-mi 2028)**, 1.0 +7-8 mois. Le pitch ne part **que** slice en main : le marché 2025-2026 ne signe plus sur concept — vertical slice, trailer et traction mesurable sont le ticket d'entrée[^pitch].

**Budget (jusqu'à la 1.0, ~26 mois).**

| Poste | Montant |
|---|---|
| Phase slice autofinancée (mode S2 : ARE + écriture FAJV + économies) | 40-60 k€ |
| Rémunération 3,5 ETP × 18 mois (~4 200 € chargé/mois — vrais salaires, pas des salaires de fondateurs) | 265 000 € |
| Prestations audio/musique/sensitivity | 35 000 € |
| Matériel/logiciels | 10 000 € |
| Marketing | porté par l'éditeur |
| Localisation | portée par l'éditeur (usage du marché) |
| Juridique (avocat spécialisé pour le contrat : non négociable) + compta | 18 000 € |
| Imprévu (12 % — l'éditeur absorbe une partie des chocs) | 45 000 € |
| **Total** | **≈ 420-430 k€** |

**Plan de financement.** L'avance éditeur est la colonne vertébrale : moyenne constatée **318 k$** tous deals, **460 k$** pour les deals avec avance — mais la réalité de la majorité des indés est **< 50 k$**[^gdc] ; hypothèse de travail CORTÈGE avec slice + traction : **200-350 k€**, complétée par le CIJV (cumulable — l'agrément exige que la société porte le jeu) et, si la société conserve ≥ 50 % de l'IP, la production FAJV reste ouverte[^fajv]. Termes à défendre, chiffres du marché à l'appui : **≥ 60 % dev** après recoupement (moyenne : 60/40 ; 55 % dev avec avance), et surtout **partage pendant le recoupement** — 58 % des contrats l'obtiennent, exiger d'en être[^gdc].

**Cibles réalistes (audit à refaire à date) :** Team17 — l'éditeur de *Sworn*, action-roguelite co-op 4 joueurs arthurien, le comparable structurel le plus proche ; Dear Villagers (Montpellier — proximité et culture CNC) ; tinyBuild (« facile à streamer » : le chaos lisible coche la case) ; Devolver/Playstack en tir long[^pubs]. **Firestoke a fermé en août 2025 : retiré des cibles** — et son cas rappelle que la solvabilité de l'éditeur fait partie de la due diligence[^firestoke].

**Périmètre.** Le périmètre EA complet du GDD, **plus** un vrai budget marketing et la localisation — c'est l'apport réel de l'éditeur, au-delà du chèque. Risque de périmètre inverse : l'éditeur qui pousse du contenu contractuel (roadmap imposée) contre les gates du §13.

**Risques propres.** 3-4 mois de démarchage à fonds perdus si personne ne signe (30-50 % des slices ne signent pas) ; clauses toxiques (recoup intégral avant premier euro — 42 % des deals[^gdc] —, IP cédée, sequel rights) ; dépendance à la santé financière d'un tiers dans une strate d'éditeurs fragilisée. **Mitigations :** ne jamais pitcher sans plan B (le dossier FAJV production part *en parallèle* du démarchage) ; lignes rouges écrites avant le premier rendez-vous : IP conservée, partage pendant recoup, gates du §13 opposables ; avocat spécialisé au premier term sheet.

**Ce scénario est le vôtre si…** l'ambition prime sur le contrôle : vous voulez le périmètre complet, un marketing professionnel, une équipe payée au marché — et vous acceptez de céder 40-45 % du revenu net et une part de la gouvernance pour l'obtenir.

---

### S4 — « la Place publique » *(la communauté d'abord)*

*La Fresque avant le jeu : on bâtit la veillée en public, et c'est elle qui paie le Conteur.*

**Équipe.** 1,5-2 ETP (le second peut être à mi-temps : art ou commu). La particularité n'est pas l'équipe, c'est **l'ordre des livrables** : une démo publique très tôt, tout le développement en public.

**Calendrier.** Slice M4 → **démo publique M5-6** (avant même l'alpha fermée du GDD — assumé : la démo EST l'outil de recrutement de l'alpha) → campagne wishlists + Discord M5-12 → **Kickstarter M8-9** → Steam Néofest M10-12 → **accès anticipé M13-14 (fin 2027)**, périmètre réduit → 1.0 payée par l'EA, M24-26.

**Budget (cash jusqu'à l'EA).**

| Poste | Montant |
|---|---|
| Rémunération 1,5 ETP × 14 mois (~3 000 € chargé/mois) | 63 000 € |
| Art externalisé (démo et EA réduites) | 20 000 € |
| Audio (la strate musicale du cortège est un argument viral : ne pas la couper) | 15 000 € |
| Marketing (trailer + vidéo Kickstarter 5-8 k€, capsules, presse) | 10 000 € |
| Localisation EN/DE/ES/FR (démo + EA) | 4 000 € |
| Juridique/compta (société tôt : Kickstarter l'exige en pratique) | 8 000 € |
| Contreparties et frais Kickstarter (~15-20 % de la collecte) | 8 000 € |
| Imprévu (15 %) | 19 000 € |
| **Total pré-EA** | **≈ 147 000 €** |

**Plan de financement.** ARE + écriture FAJV + Bourse French Tech (le socle S2 en réduit) + **Kickstarter objectif 35-60 k€** + revenus EA. Lucidité imposée par les chiffres : Kickstarter jeu vidéo 2025 = 443 campagnes financées pour ~26 M$, dont **~55 seulement au-dessus de 100 k$**[^ks] — c'est un outil de *validation et de marketing*, pas un pilier de financement ; et le Néofest **amplifie une traction existante, il n'en crée pas** (gain médian : +322 wishlists si on arrive avec < 1 000, +1 006 entre 1 et 10 k, +5 215 au-delà de 10 k ; corrélation momentum/gain r = 0,825)[^nextfest]. D'où l'ordre du calendrier : communauté d'abord, festival ensuite.

**L'atout spécifique CORTÈGE :** la cible primaire est *déjà rassemblée* (Discord officiel Squad Busters ~85 k membres au dernier relevé, subreddits actifs[^sb]) et *déjà en deuil* — fermeture des serveurs mi/fin 2026. Le message « premium, équitable, construit avec sa communauté » (README) est taillé pour elle, et le pilier 4 du GDD est le pitch Kickstarter entier. Vocabulaire verrouillé : « successeur spirituel » est sûr, tout usage d'assets ou de noms Supercell ne l'est pas (GDD §14).

**Périmètre coupé.** EA : **1 continent × 2 Ères + l'Épreuve hebdomadaire dès le jour 1** — dans ce scénario, l'Épreuve n'est pas une feature, c'est *le produit communautaire* (rendez-vous hebdomadaire, Fresque, fantômes : de la rétention sociale quasi gratuite grâce au déterminisme). Le 2ᵉ continent devient la promesse publique de la roadmap EA, financée par les ventes.

**Risques propres.** Développer en public expose les gates ratées ; un Kickstarter raté est un signal négatif public ; la communauté peut tirer le design (le pilier « décisions tranchées » du corpus doit tenir face aux sondages Discord) ; conversion wishlist dégradée par le prix — médiane semaine 1 à 0,15× les wishlists, qui **tombe à 0,10× au-dessus de 10 $**[^wl] : à 14,99 €, il faut ~10 000 wishlists pour espérer ~1 000 ventes semaine 1, seuil de survie du scénario. **Mitigations :** ne lancer le Kickstarter qu'avec ≥ 3 000 followers/wishlists (les campagnes réussies arrivent pré-financées socialement[^ks]) ; charte de gouvernance communautaire publiée (« on écoute tout, on ne vote rien ») ; tester le prix en EA — 12,99 € de lancement est une option si les données wishlists sont molles.

**Ce scénario est le vôtre si…** parler en public vous coûte peu, que la fenêtre Squad Busters vous semble l'actif n°1 du projet, et que vous préférez 10 000 wishlists à 100 000 € de subventions comme preuve d'existence.

---

## 2. Le financement France/Europe — cartographie 2026

### 2.1 Le stack CNC

| Dispositif | Pour qui | Taux/plafond | Effort de dossier | Calendrier |
|---|---|---|---|---|
| **FAJV écriture** | auteur **personne physique** (pas besoin de société), formation ou expérience JV exigée | 100 % des coûts éligibles ; ordre de grandeur : dizaines de k€ | Moyen — bible de conception + note d'intention : **le corpus CORTÈGE existant couvre 80 % du dossier** | Dépôts : **21 sept. 2026**, 18 janv. 2027, 27 avr. 2027 ; commission ~2 mois après[^fajv] |
| **FAJV pré-production** | société française, capitaux majoritairement européens ; jeu conçu et écrit en français | 50 % des dépenses de prototypage ; plafond ~200 k€ (*de minimis*) ; moyenne constatée ~80 k€ | Élevé — budget détaillé, planning, société constituée ; prototype à démarrer sous 3 mois après commission | idem |
| **FAJV production** | idem + la société conserve **≥ 50 % des droits IP** | 50 % ; total aides publiques ≤ 50 % du coût définitif | Élevé + ISAN, formation VHSS, bilan carbone Jyros (depuis mars 2025) | idem |
| **CIJV** | société soumise à l'IS, agrément CNC (barème culturel — le thème mythes & légendes est un atout objectif) | **30 % des dépenses éligibles**, plafond 6 M€/an ; **seuil : coût ≥ 100 k€** | Élevé mais rentabilité maximale ; prorogé jusqu'en 2031 | Agrément provisoire à demander tôt ; crédit perçu avec 12-18 mois de décalage[^cijv] |

### 2.2 Le reste du stack national

- **Bourse French Tech (Bpifrance)** : jusqu'à 30 k€, société récente, dossier léger — le premier chèque post-création[^bft].
- **ARE / ARCE** : le financement le plus sous-estimé — l'allocation chômage maintenue pendant la création d'entreprise couvre le coût de vie des fondateurs 18-24 mois. Aucun dossier CNC ne finance la vie des gens ; l'ARE si.
- **Statut JEI** : exonérations de cotisations patronales si ≥ 20 % des dépenses en R&D (durci en 2025). Un studio « pur design » y est inéligible ; **la simulation déterministe, la re-simulation anti-triche et le netcode relay sont précisément la brique qui porte un dossier R&D**[^jei]. À instruire à la création de la société.
- **Europe Créative MEDIA (dev. jeux vidéo)** : jusqu'à 200 k€ à 60 %, budget 2026 porté à 10 M€ — mais appel 2026 clos, et le critère habituel « un jeu déjà commercialisé » le réserve de fait au *second* projet du studio[^media]. À garder pour l'après-CORTÈGE, pas pour le plan de base.

### 2.3 Les régions — le siège social est une décision de financement

| Région | Plafond | Notes |
|---|---|---|
| Île-de-France | **150 k€**, subvention sans remboursement depuis 2025 | budget dev ≥ 50 k€ ; ≥ 50 % des dépenses en IdF ; auto-entrepreneurs inéligibles ; session 2026 : dépôts jusqu'au 29 mai (passée — viser 2027)[^idf] |
| Nouvelle-Aquitaine | **150 k€**, ≤ 50 % | dispositif dédié production JV |
| Occitanie, Grand-Est, AURA, Hauts-de-France | variable | dispositifs génériques ou via fonds image ; à auditer au moment du choix du siège |

Jusqu'à **150 k€ d'écart selon l'adresse du siège** : la domiciliation se décide avec ce tableau sous les yeux, pas après.

### 2.4 Cumul et chemin administratif

**Règles de cumul :** FAJV pré-prod/prod, aides régionales et Bourse French Tech relèvent du ***de minimis* : 300 k€ max sur 3 exercices glissants** ; le total des aides publiques est plafonné à **50 % du coût du jeu** ; le **CIJV est hors *de minimis*** et se cumule par-dessus[^fajv][^cijv]. À l'échelle CORTÈGE (300-450 k€ de coût), la contrainte active est le plafond de 50 %, pas le *de minimis*.

**Le chemin, dans l'ordre :**

1. **Maintenant (sans société)** : dossier **écriture FAJV** en tant qu'auteur — dépôt du 21 septembre 2026.
2. **À la gate du slice (M4)** : si verte, création de **SAS/SASU** (pas de micro-entreprise : inéligible aux aides régionales et au CIJV), choix du siège selon §2.3, pacte d'associés si duo. Coût : 2-3 k€ avec accompagnement.
3. **Société + slice en main** : Bourse French Tech, puis dossier **pré-production FAJV** (dépôt janvier 2027, réponse mars) et demande d'**agrément provisoire CIJV**.
4. **En parcours** : dossier régional (session 2027), statut JEI, ISAN, formation VHSS, bilan carbone Jyros le moment venu.

---

## 3. Matrice comparative

| Critère | S1 Lanterne seule | S2 Deux Récits | S3 Mécène | S4 Place publique |
|---|---|---|---|---|
| Coût total cash (→ 1.0) | ~48 k€ | ~300 k€ | ~420-430 k€ | ~200 k€ (147 pré-EA + solde sur ventes) |
| Argent externe non dilutif | 15-45 k€ | 130-150 k€ + CIJV | avance 200-350 k€ (recoupable) | 65-120 k€ |
| Délai vers l'EA | 24-27 mois (T2-T3 2028) — **limite de fenêtre** | 14-15 mois (T4 2027) | 16-18 mois (début-mi 2028) | 13-14 mois (fin 2027) |
| Risque d'échec (jeu jamais sorti) | Élevé (épuisement, glissement) | Moyen (commissions, duo) | Moyen-élevé (pas de signature = 4 mois perdus) | Moyen (KS raté, traction insuffisante) |
| Contrôle créatif | Total | Total | Partagé (roadmap, jalons contractuels) | Fort, sous pression communautaire |
| Revenu conservé | 100 % (− 30 % Steam) | 100 % (− Steam) | 55-60 % après recoup (− Steam) | 100 % (− Steam, − ~20 % de la part KS) |
| Périmètre EA | 1 continent, co-op 2 | GDD complet (si aides) | GDD complet + marketing | 1 continent + Épreuve J1 |
| Probabilité de sortie effective* | ~35 % | ~55 % | ~45 % (30-50 % de signature × exécution) | ~50 % |

*\*Estimations internes à débattre — ordonnancement plus fiable que valeurs absolues. La médiane Steam rappelle l'enjeu : ~47,5 % des sorties 2025 vendent moins de 100 copies, et seuls 1,8 % dépassent 100 000[^median] ; sortir ne suffit pas, mais ne pas sortir est pire.*

---

## 4. La recommandation — le chemin du Conteur

**Décision recommandée : démarrer en S1 armé des méthodes de S4, et laisser la gate du slice choisir le scénario de croisière.** Argument en trois temps :

1. **Les 4 premiers mois sont identiques dans les quatre scénarios** : une personne (ou deux) construit le slice déterministe, dépose l'écriture FAJV, relève les communautés Squad Busters et commence à parler en public. Choisir un scénario définitif aujourd'hui, c'est acheter de l'incertitude sans rien gagner : **le slice est l'actif qui donne le choix** — preuve pour la commission FAJV, actif de pitch éditeur, matière de la démo publique.
2. **La gate du GDD §12 (70 % de relance) est le meilleur instrument de décision déjà écrit.** Elle a été conçue pour valider le fun ; elle sert ici, gratuitement, de comité d'investissement.
3. **S2 est le scénario de croisière par défaut** (meilleur rapport contrôle/risque, périmètre complet atteignable, fenêtre tenue), **S4 n'est pas un scénario alternatif mais une couche permanente** (le build-in-public coûte ~10 % du temps et assure la cible primaire), et **S3 est l'option de secours financée** si les aides échouent ou si l'ambition monte.

**Les points de bascule, avec critères objectifs :**

| Moment | Critère mesuré | Si vert | Si rouge |
|---|---|---|---|
| **M4 — gate du slice** (nov. 2026) | ≥ 70 % de relance de run (GDD §12) + envie intacte | Création de société, dossiers S2 (Bourse FT, pré-prod FAJV janv. 2027, agrément CIJV) | Une itération de 6-8 semaines, puis re-test ; **deux échecs = pivot ou arrêt** (GDD §13, sans acharnement) |
| **M6-7 — traction publique** | ≥ 3 000 wishlists/followers cumulés après 2 mois de démo publique | Renforcer S4 (préparer Kickstarter/Néofest en amplificateurs[^nextfest]) | S4 rétrogradé en simple communication ; tout miser sur S2 |
| **M8-9 — verdict des aides** | ≥ 100 k€ d'aides acquises (FT + pré-prod + trajectoire régionale) | S2 confirmé jusqu'à l'EA, périmètre GDD complet | **Bascule S3** : le slice part en pitch (Team17, Dear Villagers, tinyBuild), lignes rouges du §1-S3 imprimées |
| **M12-14 — gate alpha** | Rétention J7 > 20 % (GDD §12) + trésorerie ≥ 8 mois | Cap sur l'EA T4 2027 | Réduire le périmètre EA au format S4 (1 continent + Épreuve) plutôt que décaler la date : **la fenêtre prime sur le périmètre** |

Une phrase à graver, symétrique de l'anti-leçon Supercell du GDD §13 : **on ne choisit pas un financement, on gagne le droit d'en choisir un — et c'est le slice qui le gagne.**

---

## 5. Les 90 premiers jours — semaine par semaine

*Exécutable par une personne seule à partir du lundi 6 juillet 2026. Trois fils : **[dev]** (aligné sur le jalon « vertical slice 4 mois » du GDD §12 — le détail d'implémentation vit dans la Roadmap technique v0.1, document compagnon : ne pas dupliquer ici), **[admin]** (financement), **[commu]** (S4 en couche). Charge cible : 80 % dev, 20 % le reste.*

| Sem. | Actions |
|---|---|
| **S1** (6-12 juil.) | [dev] Décision moteur actée (Godot 4 sauf objection de la Roadmap technique) ; projet initialisé, **boucle de simulation à pas fixe + flux RNG seedés séparés (draft/apparitions/dégâts) dès le premier commit** — l'invariant du §0. [admin] Lire le règlement écriture FAJV ; lister les pièces manquantes du dossier. [commu] Relevé manuel des communautés Squad Busters (Discord, subreddits) : tailles, modérateurs, ton — chiffres à figer avant la fermeture des serveurs[^sb]. |
| **S2** | [dev] Cortège en flux (le Conteur + 3 figures qui suivent), déplacement, caméra fixe. [admin] Rédaction du dossier écriture FAJV à partir du GDD/bible (note d'intention + bible de conception). |
| **S3** | [dev] Combat minimal : Silences en nuée, TTK selon l'étalon PV100/DPS10 de l'annexe équilibrage §1. [commu] Réserver les noms (Steam, Discord, réseaux, domaine) — sans annonce. |
| **S4** | [dev] Ferveur : récolte, gisements, la tension s'exposer/récolter. **Premier replay reproduit : même seed + mêmes inputs = même run, vérifié par hash d'état.** [admin] Relecture du dossier FAJV par un tiers. |
| **S5** | [dev] Volumes et draft 1-parmi-3 depuis un roster de 8 (la pitié attend) ; 4 figures jouables approximées (Héraclès, Tell, Jeanne, Ulysse — stats T1 de l'annexe §4.1). [commu] Choisir l'angle du build-in-public (devlog écrit ou vidéo) ; rien publier encore. |
| **S6** | [dev] Fusion T1→T2→T3 (×3 PV/dégâts, annexe §2), lisibilité par taille/ornement. Premier test du « fantasme boule de neige » : est-ce que grossir fait plaisir ? |
| **S7** | [dev] Manche complète 3-4 min : dramaturgie de l'annexe systèmes §1.2 (lecture/montée/pic/extraction), la Brume qui avance. [admin] Ajustements finaux du dossier écriture. |
| **S8** | [dev] Esquive + Capacité de Cortège (version brute) — les trois entrées du GDD §4.3 sont complètes. [commu] Publication du **premier devlog** : « pourquoi un successeur spirituel premium » — le pilier 4 comme manifeste. Mesurer la réponse des espaces Squad. |
| **S9** | [dev] Carte à nœuds minimale (3-4 types) reliant 3 manches + boss placeholder : la boucle run existe. [admin] Créer l'espace de suivi des aides (tableau : dispositif/état/échéance). |
| **S10** | [dev] **Premier playtest externe** (5-8 personnes, protocole : observer, ne pas expliquer). Mesure brute du taux de relance. [commu] Devlog 2 : la fusion et le déterminisme (les replays comme feature, pas comme technique). |
| **S11** | [dev] Itération sur les retours S10 — en priorité le *feel* de la croissance (pilier 1 : si ça ne grossit pas de façon jubilatoire, rien d'autre ne compte). |
| **S12** | [admin] **Dépôt du dossier écriture FAJV — session du 21 septembre 2026** (butoir dur de ce plan ; commission ~novembre). [dev] Audio placeholder : la strate musicale par figure, même grossière — la boule de neige doit s'entendre (GDD §10). |
| **S13** (fin sept.) | [dev] Deuxième playtest (10-12 personnes, dont 3-4 vétérans Squad recrutés via les relevés de S1). **Revue des 90 jours** : trajectoire vers la gate M4 (70 % de relance), état des fils admin/commu, décision d'échéancier pour la création de société (§2.4, étape 2). [commu] Devlog 3 + premières images fixes du papier découpé si l'artiste (S2) est identifié·e. |

À M4 (début novembre 2026) : gate du slice, et le tableau du §4 prend le relais.

---

## Notes et sources

[^fajv]: CNC, [Fonds d'Aide au Jeu Vidéo](https://www.cnc.fr/professionnels/aides-et-financements/jeu-video/fonds-daide-au-jeu-video-fajv_191468) ; recoupé avec [les-aides.fr (pré-production)](https://les-aides.fr/aide/I5M_3w/cnc/jeu-video-fajv-aide-a-la-pre-production-de-jeu-video.html) et [F.initiatives](https://www.f-initiatives.com/grants/fonds-daide-au-jeu-video-fajv-cnc/) (soutien moyen ~80 k€/phase). Écriture : auteurs personnes physiques, 100 % des coûts. Pré-prod : 50 %, ~200 k€ max sous *de minimis*. Production : IP ≥ 50 %, aides publiques totales ≤ 50 % du coût. Dépôts 2026-2027 : 21/09/26, 18/01/27, 27/04/27, 20/09/27 ; commission ~2 mois après dépôt.
[^cijv]: CNC, [Crédit d'impôt jeu vidéo](https://www.cnc.fr/professionnels/aides-et-financements/jeu-video/credit-dimpot-jeu-video_121078) : 30 % des dépenses éligibles, seuil 100 k€ de coût, agrément CNC (barème culturel), prorogé jusqu'en 2031 ([ViaExperts, PLF 2025](https://viaexperts.fr/plf2025-le-gouvernement-favorable-a-la-prolongation-du-credit-dimpot-jeu-video-cijv-jusquen-2031/)). Hors *de minimis*, cumulable avec le FAJV.
[^idf]: Région Île-de-France, [Fonds d'aide à la création de jeu vidéo](https://www.iledefrance.fr/aides-et-appels-a-projets/fonds-daide-la-creation-de-jeu-video) : jusqu'à 150 k€, subvention sans clause de remboursement depuis 2025 ; 38 dossiers déposés en 2025.
[^bft]: Bpifrance, Bourse French Tech : jusqu'à 30 k€, régime *de minimis* ([les-aides.fr](https://les-aides.fr/actualites/dp8/aides-a-l-innovation-comment-financer-un-projet-innovant.html)).
[^jei]: Statut JEI : condition ≥ 20 % de dépenses R&D depuis 2025 ([service-public](https://entreprendre.service-public.gouv.fr/vosdroits/F31188), [URSSAF](https://www.urssaf.fr/accueil/employeur/beneficier-exonerations/exonerations-secteur-activite/jeunes-entreprises-innovantes.html)). L'éligibilité d'un studio JV se plaide sur les briques techniques (simulation déterministe, re-simulation anti-triche) — interprétation, à valider avec un conseil.
[^media]: Europe Créative MEDIA, appel « Video Games and Immersive Content Development » : max 200 k€ à 60 % ; budget 2026 porté à 10 M€, appel clos — cycle 2027 ([EGDF](https://www.egdf.eu/documentation/i-creative-europe/closed-creative-europe-calls/crea-media-2026-devvgim-video-games-and-immersive-content-development/)). Critère de track record (un jeu déjà commercialisé) à confirmer.
[^gdc]: GameDiscoverCo, analyse de 130+ contrats d'édition ([partie 1](https://newsletter.gamediscover.co/p/what-makes-for-a-good-game-publishing), [partie 2](https://newsletter.gamediscover.co/p/what-should-a-game-publishing-agreement)) : avance moyenne 318 k$ (460 k$ pour les deals avec avance), partage moyen 60/40 dev/éditeur (55 % dev avec avance), 42 % des deals à recoup intégral avant premier dollar. Réalité majoritaire des indés : avance < 50 k$ ([PC Gamer](https://www.pcgamer.com/what-a-good-and-bad-indie-game-publishing-deal-looks-like/)).
[^pubs]: Panorama éditeurs : [FirstLook.gg](https://firstlook.gg/blog/indie-game-publishers/), [rogueliker](https://rogueliker.com/coop-roguelikes/) (Team17/*Sworn*), [Plug In Digital/Dear Villagers](https://en.wikipedia.org/wiki/Plug_In_Digital). Liste à re-auditer avant tout démarchage.
[^firestoke]: Fermeture de Firestoke, août 2025 ([This Week in Videogames](https://thisweekinvideogames.com/news/indie-publisher-firestoke-shutting-down/)).
[^wl]: GameDiscoverCo, [« The state of Steam wishlist conversions »](https://newsletter.gamediscover.co/p/the-state-of-steam-wishlist-conversions) (sorties sept. 2024-sept. 2025) : conversion médiane semaine 1 ≈ 0,15× les wishlists ; ≈ 0,10× au-dessus de 10 $.
[^nextfest]: How To Market A Game, [benchmarks Next Fest, fév. 2026, 182 répondants](https://howtomarketagame.com/2025/03/26/benchmarks-how-many-wishlists-can-i-get-from-steam-next-fest/) : gains médians +322 / +1 006 / +5 215 / +12 882 wishlists selon la traction pré-festival ; r = 0,825.
[^ks]: ICO Partners / Thomas Bidaux, [« Kickstarter & Video Games in 2025 »](https://medium.com/icopartners/kickstarter-and-video-games-in-2025-90f15c2fd7bd) : 443 campagnes JV financées, ~26 M$ collectés, ~55 projets > 100 k$.
[^median]: Statistiques Steam agrégées 2024-2025 (seconde main, cohérentes entre agrégateurs) : revenu médian ~250 $, 47,5 % des sorties 2025 < 100 copies, 1,8 % > 100 000 copies ([Icon Era](https://icon-era.com/statistics/steam-game-statistics/)). Segmentation VG Insights 2024 : une petite équipe qui réussit = 20-200 k copies ([rapport](https://app.sensortower.com/vgi/assets/reports/VGI_Global_Indie_Games_Market_Report_2024.pdf)).
[^sb]: Supercell, [FAQ officielle d'arrêt de Squad Busters](https://supercell.com/en/news/squad-busters-faq/) (annonce du 30/10/2025) : fin du développement actif, serveurs maintenus « entre mi-2026 et fin 2026 ». Discord officiel ~84 600 membres ([discord.do](https://discord.do/squad-busters/), date de relevé incertaine — à relever manuellement, action S1 du plan 90 jours).
[^malt]: [Baromètre Malt illustration](https://www.malt.fr/t/barometre-tarifs/web-graphic-design/illustrateur) : TJM médian ~320-350 €/j (Paris 346 €).
[^audio]: Sound design : ~300-800 €/j, moyenne Malt 335 €/j ([Handaloop](https://www.handaloop.fr/sound-designer-freelance-tarifs-et-specialisations-2025/)). Musique : quelques centaines d'€/minute en milieu indé ([thomasbrunet.fr](https://thomasbrunet.fr/2023/07/31/combien-coute-un-compositeur-de-musique-de-jeu-video/)) — budgéter la cession de droits.
[^sensi]: Sensitivity reading / consultation culturelle : ~0,01 $/mot, forfaits consultation ~240 $, lecture approfondie dès 490 $ ([James Mendez Hodes](https://jamesmendezhodes.com/sensitivity), [Salt & Sage](https://www.saltandsagebooks.com/prices/)) — quelques centaines à ~2 000 € par aire culturelle.
[^loc]: Localisation : 0,10-0,15 $/mot source ([LocalizeDirect](https://www.localizedirect.com/posts/top-languages-for-game-localization)) ; CORTÈGE étant peu textuel (~10-20 k mots plausibles), EFIGS ≈ 5-12 k€.

---

*Document vivant. Les montants d'aides et les calendriers de commissions sont relevés au 6 juillet 2026 et se périment vite : re-vérifier chaque chiffre avant tout dépôt de dossier ou signature. Prochaines révisions attendues : v0.2 après la gate du slice (novembre 2026), avec les scénarios recalés sur les résultats réels — gate, traction, commission d'écriture.*
