# CORTÈGE — Unités de base

**Version 0.1 — Document de travail**
*Extraction du roster de lancement depuis la Bible d'univers v0.2 et l'Annexe Équilibrage v0.1, pour approfondir les figures une par une.*

---

## 1. Intention du document

Ce fichier isole les **16 figures prévues au lancement** afin de travailler plus finement leurs kits, leurs fantasmes de jeu, leurs branches de Légende et leur équilibrage.

Il sert de pont entre :

- la **Bible d'univers**, qui définit l'origine, le ton et les branches mythiques ;
- l'**Annexe Équilibrage**, qui chiffre les profils T1 ;
- le futur prototype, qui devra valider le ressenti réel des unités.

Chaque fiche ci-dessous garde volontairement les informations courtes. Le but est de pouvoir itérer ensuite figure par figure sans diluer le GDD.

---

## 2. Rôles

| Rôle | Fonction attendue | Question de design |
|---|---|---|
| **Cogneur** | tenir la ligne, attirer l'attention, absorber la pression | Est-ce que le joueur sent que cette figure protège le cortège ? |
| **Tireur** | tuer à distance, prioriser les cibles, sécuriser les combats | Est-ce que sa portée change vraiment le positionnement ? |
| **Soutien** | réparer, protéger, ralentir ou stabiliser le groupe | Est-ce qu'il sauve des situations sans rendre le jeu passif ? |
| **Récolteur** | accélérer l'économie de Ferveur et la lecture de carte | Est-ce qu'il crée une vraie tentation économique ? |
| **Filou** | mobilité, aggro, dégâts conditionnels, prises de risque | Est-ce qu'il récompense le placement actif ? |
| **Bâtisseur** | contrôler l'espace, canaliser les ennemis, créer des zones | Est-ce que ses structures se lisent et se jouent vite ? |

---

## 3. Logique des tiers et apparition des compétences

> **Note de cohérence (à réconcilier).** Cette section propose une logique de tiers **variable selon le type de figure** (mythique / historique / légendaire — le pouvoir apparaissant à T1, T2 ou T3 selon le cas). Cela entre en **tension directe avec l'Annexe Équilibrage §2**, qui pose une règle de fusion **uniforme** : T1 = kit de base, T2 = amplification générale + trait de geste (~10 pts d'étalon), T3 = branche de Légende (A/B), les identités ne bifurquant qu'au T3 (cf. aussi Bible §8, « Règle des tiers »). Les deux approches doivent être arbitrées avant le prototype : soit l'annexe et la bible s'alignent sur cette logique variable, soit ce document s'aligne sur la règle uniforme. En l'état, elle est signalée, pas tranchée.

Les tiers ne doivent pas suivre une règle uniforme du type "T1 sans pouvoir, T2 passif, T3 actif". Pour ajouter de la profondeur stratégique, **le moment où une compétence apparaît dépend de la nature de la figure**.

L'objectif n'est pas seulement d'augmenter les chiffres à chaque fusion. Chaque tier doit rendre la figure **plus elle-même** : plus humaine, plus héroïque, puis plus légendaire.

| Type de figure | T1 | T2 | T3 | Risque d'équilibrage |
|---|---|---|---|---|
| **Mythique** | Peut avoir une compétence distinctive dès le départ | Améliore ou stabilise cette mécanique | Déclenche une grande geste spectaculaire | Trop forte trop tôt si les stats ne compensent pas |
| **Historique** | Commence plus simple, plus physique ou plus fiable | Débloque son rôle symbolique ou tactique | Devient une légende de champ de bataille | T1 trop fade si elle n'a pas assez de présence |
| **Légendaire / folklore** | Spécialisée autour d'un geste ou d'une condition | Rend cette condition plus exploitable | Transforme le geste en moment iconique | Trop dépendante du contexte si la condition est rare |

### Principes

1. **Les mythiques peuvent tricher plus tôt.** Ulysse, Orphée, Dédale ou Gilgamesh peuvent avoir une mécanique spéciale dès le T1, mais avec des stats plus fragiles, plus lentes ou plus spécialisées.
2. **Les historiques deviennent légendaires progressivement.** Jeanne d'Arc, Boudicca, Marco Polo ou Sun Tzu peuvent commencer avec un kit plus terrestre, puis débloquer leur aura, leur stratégie ou leur geste au T2/T3.
3. **Le T3 doit être visible.** Une Légende T3 doit produire un événement automatique ou semi-automatique clair : bannière levée, charge, volée, labyrinthe, flèche monumentale, zone tactique, résurrection.
4. **Les pouvoirs ne doivent pas tous être permanents.** Certains peuvent être des auras, d'autres des déclenchements sous pression, des cooldowns automatiques, des effets liés à la position, ou des réponses à un événement précis.
5. **La fusion change le gameplay.** Une fusion ne doit jamais être seulement "+PV/+DPS". Elle doit ajouter une décision, une fenêtre de puissance, une nouvelle lecture de terrain ou une nouvelle priorité.

Exemple directeur : **Jeanne d'Arc** peut commencer T1 comme une combattante de bannière assez simple, devenir T2 une vraie porte-étendard qui améliore l'attaque du groupe, puis T3 déclencher automatiquement une grande charge visuelle qui accélère et protège brièvement les alliés.

---

## 4. Europe

### Héraclès

| Champ | Valeur |
|---|---|
| Statut | Départ Europe |
| Rôle | Cogneur |
| Origine | Mythe grec |
| Fantasme | Le pilier de mêlée qui attire les coups et tient la ligne |
| Kit T1 | Coups lourds et lents ; provocation passive dans un rayon de 4 m |
| T2 pressenti | Provocation renforcée ; réduction des dégâts reçus quand plusieurs ennemis le ciblent |
| T3 A | **La Peau du Lion** : aura de garde, réduit les dégâts subis par le cortège proche |
| T3 B | **La Massue d'Érymanthe** : frappe de zone qui étourdit |
| Stats T1 | 170 PV · 10 DPS · mêlée · VIT 90 |

**À approfondir.** Héraclès doit probablement être la première unité "lisible" du jeu : simple, massif, immédiatement compréhensible. Son risque est d'être trop passif si sa provocation fait tout le travail sans décision de placement.

### Guillaume Tell

| Champ | Valeur |
|---|---|
| Statut | Départ Europe |
| Rôle | Tireur |
| Origine | Légende suisse, XIVe siècle |
| Fantasme | Le tireur précis qui choisit une cible et la fait tomber |
| Kit T1 | Arbalétrier de précision ; marque sa cible, qui subit +15 % de ses dégâts |
| T2 pressenti | Recharge plus vite ou améliore sa marque après un tir parfait |
| T3 A | **La Pomme** : critiques garantis ou fortement amplifiés sur cible marquée |
| T3 B | **Le Second Carreau** : exécution des ennemis affaiblis |
| Stats T1 | 70 PV · 12 DPS · portée 8 m · VIT 100 |

**À approfondir.** Tell est un bon candidat pour enseigner la priorisation mono-cible. Il faudra décider si la marque est automatique, cyclique, ou influencée par l'orientation du cortège.

### Jeanne d'Arc

| Champ | Valeur |
|---|---|
| Statut | Départ Europe |
| Rôle | Soutien |
| Origine | Histoire, France, 1412-1431 |
| Fantasme | La bannière qui rallie et garde le groupe debout |
| Kit T1 | Combattante de bannière simple ; présence correcte en mêlée, pas encore de pouvoir majeur |
| T2 pressenti | Devient porte-étendard : aura offensive qui augmente les dégâts ou le courage des alliés proches |
| T3 A | **Les Voix** : grande protection automatique sous pression, soin renforcé + dissipation des effets néfastes |
| T3 B | **L'Étendard** : charge visuelle brève, vitesse et dégâts massifs ; les alliés proches ne peuvent pas tomber pendant quelques secondes |
| Stats T1 | 90 PV · 4 DPS · aura r 5 m · VIT 100 |

**À approfondir.** Jeanne doit illustrer la montée historique vers le légendaire : T1 humaine et fiable, T2 inspirante, T3 spectaculaire. Son effet de protection ne doit pas annuler la tension ; il doit créer une fenêtre courte où le joueur ose traverser la vague.

### Ulysse

| Champ | Valeur |
|---|---|
| Statut | Départ Europe |
| Rôle | Filou |
| Origine | Mythe grec |
| Fantasme | Le rusé qui contourne, esquive et fait perdre l'aggro |
| Kit T1 | Frappes sournoises dans le dos ; esquive propre |
| T2 pressenti | Esquive plus fréquente ou meilleure fenêtre de dégâts après perte d'aggro |
| T3 A | **Personne** : le cortège perd l'aggro quelques secondes |
| T3 B | **Le Cheval** : leurre monumental qui provoque puis éclate |
| Stats T1 | 70 PV · 11 DPS · mêlée · VIT 120 |

**À approfondir.** Ulysse peut devenir la figure qui enseigne le repositionnement offensif. Il faudra vérifier que les dégâts "dans le dos" existent vraiment dans une simulation de cortège, sans devenir illisibles.

### Boudicca

| Champ | Valeur |
|---|---|
| Statut | Chronique Europe |
| Rôle | Cogneur |
| Origine | Histoire, Bretons Iceni, Ier siècle |
| Fantasme | La charge qui transforme le cortège en percée brutale |
| Kit T1 | Guerrière sur char ; dégâts en ligne droite ; accélère au fil du combat |
| T2 pressenti | Cri de guerre qui donne une courte accélération au cortège après une charge réussie |
| T3 A | **La Reine des Iceni** : cri de charge, vitesse + attaque pour tout le cortège |
| T3 B | **L'Incendiaire de Londinium** : le char laisse une traînée de feu |
| Stats T1 | 150 PV · 9 DPS · mêlée · VIT 110 |

**À approfondir.** Boudicca est une cogneuse plus dynamique qu'Héraclès. Elle doit créer des trajectoires, pas seulement des dégâts : charge, ligne, traversée, feu au sol.

### Orphée

| Champ | Valeur |
|---|---|
| Statut | Chronique Europe |
| Rôle | Soutien |
| Origine | Mythe grec |
| Fantasme | La musique qui ralentit, charme et retient les pertes |
| Kit T1 | Lyre qui ralentit les ennemis alentour |
| T2 pressenti | Ralentissement plus stable ; les ennemis affectés infligent moins de dégâts |
| T3 A | **Le Chant qui charme** : retourne brièvement un ennemi standard contre les siens |
| T3 B | **Le Regard en arrière** : une fois par manche, ramène la dernière figure perdue sous condition |
| Stats T1 | 75 PV · 3 DPS · portée 6 m · VIT 100 |

**À approfondir.** Orphée porte des mécaniques très fortes : contrôle et résurrection. Il faudra borner son impact pour éviter qu'il devienne obligatoire dans tous les rosters.

### Marco Polo

| Champ | Valeur |
|---|---|
| Statut | Chronique Europe |
| Rôle | Récolteur |
| Origine | Histoire, Venise, XIIIe siècle |
| Fantasme | L'explorateur qui révèle la carte et enrichit la route |
| Kit T1 | Explorateur mobile avec ramassage légèrement accéléré |
| T2 pressenti | Révèle les gisements et Volumes proches ; améliore la lecture de carte |
| T3 A | **Le Devisement du monde** : révèle toute la carte de l'acte + un nœud caché bonus |
| T3 B | **La Route de la soie** : marchés moins chers et objet exotique supplémentaire |
| Stats T1 | 80 PV · 5 DPS · portée 5 m · VIT 105 |

**À approfondir.** Marco Polo est plus "information et routing" que pur revenu. Il peut être très précieux si les cartes et marchés offrent de vraies décisions.

### Dédale

| Champ | Valeur |
|---|---|
| Statut | Chronique Europe |
| Rôle | Bâtisseur |
| Origine | Mythe grec |
| Fantasme | L'architecte qui plie l'arène à son avantage |
| Kit T1 | Pose des murets temporaires qui canalisent les ennemis |
| T2 pressenti | Murets plus intelligents, plus durables ou capables de ralentir les ennemis qui les contournent |
| T3 A | **Le Labyrinthe** : les murs désorientent les ennemis |
| T3 B | **Les Ailes** : bref envol du cortège, avec brûlure si maintenu trop longtemps |
| Stats T1 | 85 PV · 3 DPS · portée 6 m · VIT 95 |

**À approfondir.** Dédale est probablement une unité à haut risque de complexité. Ses murs doivent être utiles sans bloquer le cortège, sans casser le pathfinding et sans rendre l'écran confus.

---

## 5. Asie

### Gilgamesh

| Champ | Valeur |
|---|---|
| Statut | Départ Asie |
| Rôle | Cogneur |
| Origine | Mythe mésopotamien |
| Fantasme | Le roi-colosse qui projette et refuse de tomber |
| Kit T1 | Colosse offensif ; coups qui projettent périodiquement les ennemis |
| T2 pressenti | Projection plus fiable ; désigne une figure proche qui profite de sa présence |
| T3 A | **L'Ami d'Enkidou** : lie Gilgamesh à une autre figure, bonus côte à côte |
| T3 B | **La Quête d'immortalité** : se relève une fois par manche après une chute |
| Stats T1 | 175 PV · 11 DPS · mêlée · VIT 90 |

**À approfondir.** Gilgamesh est le cogneur offensif de référence. Son lien à "Enkidou" peut devenir une excellente mécanique de formation si elle reste simple à lire.

### Tomoe Gozen

| Champ | Valeur |
|---|---|
| Statut | Départ Asie |
| Rôle | Tireur |
| Origine | Histoire/légende, Japon, XIIe siècle |
| Fantasme | L'archère mobile qui tue sans s'arrêter |
| Kit T1 | Cavalière-archère ; tire en mouvement sans malus |
| T2 pressenti | Gagne cadence ou précision quand le cortège reste en mouvement |
| T3 A | **L'Onna-musha** : cadence et vitesse accrues, insensible aux ralentissements |
| T3 B | **La Dernière Charge** : bascule en lancière de mêlée au contact |
| Stats T1 | 75 PV · 11 DPS · portée 7 m · VIT 115 |

**À approfondir.** Tomoe doit se distinguer des autres tireurs par l'uptime en mouvement. Elle peut devenir une figure très agréable si le jeu pousse souvent à kiter.

### Himiko

| Champ | Valeur |
|---|---|
| Statut | Départ Asie |
| Rôle | Soutien |
| Origine | Histoire/légende, Japon, IIIe siècle |
| Fantasme | La reine-chamane qui protège et anticipe |
| Kit T1 | Rituels qui posent un bouclier tournant sur les figures |
| T2 pressenti | Bouclier plus fréquent ou priorité automatique sur les figures les plus menacées |
| T3 A | **Le Miroir de bronze** : les boucliers renvoient une partie des projectiles |
| T3 B | **L'Oracle de Yamatai** : révèle les nœuds voisins et le prochain draft |
| Stats T1 | 80 PV · 3 DPS · portée 6 m · VIT 100 |

**À approfondir.** Himiko mélange protection et information. Il faudra décider si elle est une alternative défensive à Jeanne ou une unité plus stratégique orientée prévision.

### Miyamoto Musashi

| Champ | Valeur |
|---|---|
| Statut | Départ Asie |
| Rôle | Filou |
| Origine | Histoire, Japon, 1584-1645 |
| Fantasme | Le duelliste qui excelle quand il isole une cible |
| Kit T1 | Duelliste solide ; bonus en un-contre-un |
| T2 pressenti | Débloque le dash offensif ou une parade courte après esquive réussie |
| T3 A | **Niten Ichi-ryu** : deux sabres, chaque dash frappe deux fois |
| T3 B | **Le Vide** : esquive au bon tempo, pare et renvoie le coup |
| Stats T1 | 80 PV · 11 DPS · mêlée · VIT 110 |

**À approfondir.** Musashi est la figure la plus "skill timing" du roster actuel. Il faudra voir si le jeu peut réellement reconnaître et récompenser le duel au milieu d'une foule.

### Arash

| Champ | Valeur |
|---|---|
| Statut | Chronique Asie |
| Rôle | Tireur |
| Origine | Mythe perse |
| Fantasme | L'archer dont la distance devient puissance |
| Kit T1 | Plus la cible est loin, plus la flèche frappe fort |
| T2 pressenti | Tir chargé à longue distance ; meilleure pénétration si la trajectoire reste dégagée |
| T3 A | **La Flèche-Frontière** : tir chargé qui traverse l'arène |
| T3 B | **Le Dernier Souffle** : sous 30 % de vie, dégâts doublés et portée sans limite |
| Stats T1 | 65 PV · 9 DPS · portée 10 m · VIT 95 |

**À approfondir.** Arash force une question de caméra et d'échelle : sa portée doit être assez grande pour se sentir mythique, sans tirer hors de l'espace lisible.

### Crésus

| Champ | Valeur |
|---|---|
| Statut | Chronique Asie |
| Rôle | Récolteur |
| Origine | Histoire, Lydie, VIe siècle av. J.-C. |
| Fantasme | La richesse qui transforme chaque risque en économie |
| Kit T1 | Récolteur fragile ; rayon de ramassage augmenté |
| T2 pressenti | Génère de la Ferveur passive ou convertit une partie des combats en économie |
| T3 A | **Le Pactole** : traînée dorée, ennemis vaincus dessus donnent de la Ferveur bonus |
| T3 B | **Riche comme Crésus** : la réserve non dépensée produit des intérêts |
| Stats T1 | 85 PV · 5 DPS · portée 4 m · VIT 100 |

**À approfondir.** Crésus est le récolteur le plus pur. Son danger est mathématique : s'il est trop rentable, il devient obligatoire ; s'il ne l'est pas assez, il paraît faible.

### Hua Mulan

| Champ | Valeur |
|---|---|
| Statut | Chronique Asie |
| Rôle | Filou |
| Origine | Légende chinoise |
| Fantasme | La combattante qui disparaît, flanque et s'améliore avec la durée |
| Kit T1 | Se fond parmi les ennemis tant qu'elle n'attaque pas ; dégâts de flanc |
| T2 pressenti | Meilleure sortie de furtivité ; bonus de flanc plus stable après repositionnement |
| T3 A | **Douze années de guerre** : gagne un cran de vétérance cumulable à chaque manche survécue |
| T3 B | **Le Reflet** : crée un double autonome |
| Stats T1 | 75 PV · 10 DPS · mêlée · VIT 115 |

**À approfondir.** Mulan a un potentiel de snowball interne très fort avec la vétérance. Il faudra décider si cette progression dure une run entière ou seulement une Ère.

### Sun Tzu

| Champ | Valeur |
|---|---|
| Statut | Chronique Asie |
| Rôle | Bâtisseur |
| Origine | Histoire/tradition, Chine |
| Fantasme | Le stratège qui gagne par terrain choisi |
| Kit T1 | Stratège fragile ; attaque ou soutien léger à distance |
| T2 pressenti | Débloque les fanions qui ralentissent les ennemis et accélèrent les alliés |
| T3 A | **Le Terrain choisi** : fanions fortifiés, défense alliée accrue et ennemis affaiblis |
| T3 B | **Vaincre sans combattre** : les ennemis standard démoralisés fuient vers la Brume |
| Stats T1 | 90 PV · 3 DPS · portée 6 m · VIT 95 |

**À approfondir.** Sun Tzu doit rendre le placement préventif intéressant. Son kit peut devenir excellent pour les joueurs expérimentés, mais il faudra éviter qu'il paraisse invisible aux nouveaux.

---

## 6. Vue synthétique

| Figure | Continent | Type | Statut | Rôle | PV | DPS | Portée | VIT |
|---|---|---|---|---|---:|---:|---|---:|
| Héraclès | Europe | Mythique | Départ | Cogneur | 170 | 10 | mêlée | 90 |
| Guillaume Tell | Europe | Légendaire | Départ | Tireur | 70 | 12 | 8 m | 100 |
| Jeanne d'Arc | Europe | Historique | Départ | Soutien | 90 | 4 | aura r 5 m | 100 |
| Ulysse | Europe | Mythique | Départ | Filou | 70 | 11 | mêlée | 120 |
| Boudicca | Europe | Historique | Chronique | Cogneur | 150 | 9 | mêlée | 110 |
| Orphée | Europe | Mythique | Chronique | Soutien | 75 | 3 | 6 m | 100 |
| Marco Polo | Europe | Historique | Chronique | Récolteur | 80 | 5 | 5 m | 105 |
| Dédale | Europe | Mythique | Chronique | Bâtisseur | 85 | 3 | 6 m | 95 |
| Gilgamesh | Asie | Mythique | Départ | Cogneur | 175 | 11 | mêlée | 90 |
| Tomoe Gozen | Asie | Historique/légendaire | Départ | Tireur | 75 | 11 | 7 m | 115 |
| Himiko | Asie | Historique/légendaire | Départ | Soutien | 80 | 3 | 6 m | 100 |
| Miyamoto Musashi | Asie | Historique | Départ | Filou | 80 | 11 | mêlée | 110 |
| Arash | Asie | Mythique | Chronique | Tireur | 65 | 9 | 10 m | 95 |
| Crésus | Asie | Historique | Chronique | Récolteur | 85 | 5 | 4 m | 100 |
| Hua Mulan | Asie | Légendaire | Chronique | Filou | 75 | 10 | mêlée | 115 |
| Sun Tzu | Asie | Historique/tradition | Chronique | Bâtisseur | 90 | 3 | 6 m | 95 |

---

## 7. Points à approfondir ensuite

1. **Fiches complètes par figure.** Attaque de base, cadence, zone, ciblage, comportement IA, animation clé, feedback sonore.
2. **Progression T1/T2/T3 individualisée.** Définir pour chaque figure à quel tier apparaissent ses compétences, selon son type : mythique, historique, légendaire ou hybride.
3. **Traits T2.** Le T2 ne doit pas être un simple bonus mineur automatique : il doit souvent révéler le rôle ou stabiliser la mécanique principale.
4. **Branches T3 chiffrées et visibles.** Chaque branche doit produire un vrai moment de gameplay, idéalement lisible à l'écran, avec un budget comparable : +20 à +30 % de puissance effective du T3, ou une charge majeure par manche.
5. **Règles de déclenchement.** Décider quels pouvoirs sont permanents, automatiques sur cooldown, déclenchés sous pression, liés à une condition de position, ou liés à la Grande Geste.
6. **Règles de ciblage.** Beaucoup de kits dépendent de notions comme flanc, dos, cible marquée, duel ou distance ; il faut les définir tôt.
7. **Lisibilité visuelle.** Une silhouette par rôle, puis une signature par figure ; le joueur doit identifier la composition d'un cortège en moins d'une seconde.
8. **Priorité prototype.** Tester d'abord 6 figures couvrant tous les rôles : un Cogneur, un Tireur, un Soutien, un Récolteur, un Filou, un Bâtisseur.
9. **Alternatives de figures.** Plus tard, étudier la possibilité d'avoir une alternative à certains personnages : même rôle ou même fonction stratégique, mais autre figure, autre culture, autre tempo de déblocage ou autre style de compétence. Cette piste peut aider à éviter qu'une figure devienne obligatoire, tout en donnant plus de choix de roster.

---

## 8. Questions ouvertes

- Le continent de départ doit-il offrir seulement 4 rôles au départ, ou faut-il que chaque continent ait les 6 rôles accessibles très vite ?
- Les Récolteurs doivent-ils être absents du départ pour créer un objectif de Chronique, ou présents tôt pour enseigner l'économie ?
- Les Bâtisseurs sont-ils compatibles avec un jeu très rapide de 3 à 4 minutes par manche ?
- Les effets de position comme "dans le dos", "de flanc" ou "un seul ennemi au contact" sont-ils assez lisibles dans un cortège massif ?
- Les branches T3 doivent-elles toujours opposer deux styles très différents, ou parfois deux nuances d'un même fantasme ?
- Pour chaque figure, le pouvoir principal doit-il apparaître au T1, au T2 ou au T3 ?
- Les figures mythiques doivent-elles systématiquement payer leurs pouvoirs précoces par des stats plus basses, ou seulement quand le pouvoir modifie fortement le gameplay ?
- Faut-il prévoir, à terme, des personnages alternatifs pour certaines fonctions clés afin qu'un joueur puisse remplacer une figure sans perdre complètement un rôle ?

---

*Document vivant. Prochaine étape naturelle : choisir 6 figures pour le prototype jouable et écrire leurs fiches complètes T1 / T2 / T3.*
