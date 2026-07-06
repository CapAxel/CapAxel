# CORTÈGE — Annexe Équilibrage

**Version 0.1 — Document compagnon du GDD v0.3, de la bible v0.2 et de l'annexe systèmes v0.2**

> **Avertissement de méthode.** Tous les chiffres de ce document sont des hypothèses de départ pour le prototype. La vérité sortira du playtest : ce qui est engageant ici, ce sont les **rapports** (ratios de tiers, parts de score, profils de rôles), pas les valeurs absolues. Chaque nombre est fait pour être trahi — mais depuis une base cohérente.

---

## 1. L'étalon

Toutes les valeurs sont exprimées par rapport à **la figure-étalon** : un combattant T1 théorique de milieu de grille.

| Stat | Notation | Valeur étalon | Définition |
|---|---|---|---|
| Points de vie | PV | **100** | |
| Dégâts par seconde | DPS | **10** | dégâts d'un coup × cadence |
| Portée | POR | mêlée = 1,5 m | distance d'engagement |
| Vitesse | VIT | **100** | vitesse de déplacement de référence (= celle du Conteur) |

L'ennemi-étalon est **le Silence** : 30 PV, 4 DPS, VIT 85. Toutes les vagues se budgètent en « Silences-équivalents ».

---

## 2. Les tiers — la règle de fusion

**Conservation stricte, prime qualitative.** Fusionner ne perd jamais de puissance brute ; ce qu'on paie, c'est la couverture (trois corps récoltent, bloquent et encaissent à trois endroits ; un seul corps est à un seul endroit).

| Grandeur | Par fusion (T1→T2, T2→T3) |
|---|---|
| PV et dégâts | **× 3** |
| Soins et boucliers | **× 2,5** |
| Rayons, durées, contrôles (ralentissements, étourdissements) | **× 1,25** — le contrôle scale doucement, sinon il verrouille le jeu |
| T2 | + **trait de geste** (bonus mineur ≈ 10 points d'étalon) |
| T3 | + **branche de Légende** (A/B, voir §4.3) |

En T1-équivalents : **T2 ≈ 3**, **T3 ≈ 9**. Un cortège se mesure donc en T1-eq — c'est l'unité de toute la suite du document.

---

## 3. Les profils de rôles et le coût d'une figure

### 3.1 Multiplicateurs de rôle (appliqués à l'étalon, T1)

| Rôle | PV | DPS | POR | VIT | Signature du rôle |
|---|---|---|---|---|---|
| Cogneur | × 1,5–1,75 | × 0,9–1,1 | mêlée | 90 | prend l'attention, tient la ligne |
| Tireur | × 0,65–0,75 | × 0,9–1,2 | 7–10 m | 95–115 | dégâts à distance, fragile |
| Soutien | × 0,75–0,9 | × 0,3–0,4 | 5–6 m | 100 | soin/bouclier ≈ 60–80 % du DPS étalon en valeur |
| Récolteur | × 0,8–0,85 | × 0,5 | 4–5 m | 100–105 | + 40–100 % d'efficacité économique |
| Filou | × 0,7–0,8 | × 1,0–1,1 (× 1,4–1,6 conditionnel) | mêlée | 110–120 | dégâts situationnels, mobilité |
| Bâtisseur | × 0,85–0,9 | × 0,3 direct | 5–6 m | 95 | ses structures sont son vrai budget |

### 3.2 La règle des 100 points

Toute figure T1, convertie en points via le barème, doit tomber à **100 ± 10**. Formule indicative (coefficients à ajuster dans le classeur de référence) :

> Coût ≈ PV/3 + DPS×3 + (POR−1,5)×2 + (VIT−100)/5 + Utilité (barème)

**Barème d'utilité (extraits)** : provocation passive r 4 m = 8 pts · ralentissement −25 % r 5 m = 10 · soin 1,5 %/s en aura = 12 · bouclier tournant 25 PV/6 s = 10 · +1 Ferveur/s passive = 12 · révélation r 12 m = 8 · non-ciblage conditionnel = 10 · structure 120 PV/8 s = 12 · dégâts conditionnels ×1,5 = 9. Le barème complet vit dans le classeur — ce document fige le principe : **on n'ajoute jamais une figure sans la faire passer à la caisse.**

---

## 4. Les 16 figures chiffrées (T1)

### 4.1 Europe

| Figure | PV | DPS | POR | VIT | Le chiffre du kit |
|---|---|---|---|---|---|
| Héraclès | 170 | 10 (20 × 0,5/s) | mêlée | 90 | provocation passive r 4 m |
| Boudicca | 150 | 9 | mêlée | 110 | +2 %/s de VIT en combat (cap +30 %) ; ×1,5 sur la ligne de charge |
| Guillaume Tell | 70 | 12 | 8 m | 100 | marque : la cible subit +15 % de ses dégâts |
| Jeanne d'Arc | 90 | 4 | aura r 5 m | 100 | régénération 1,5 % PV max/s dans l'aura |
| Orphée | 75 | 3 | 6 m | 100 | ralentissement −25 % r 5 m |
| Marco Polo | 80 | 5 | 5 m | 105 | révèle r 12 m ; +40 % vitesse de ramassage |
| Ulysse | 70 | 11 | mêlée | 120 | ×1,6 dans le dos ; esquive propre (recharge 6 s) |
| Dédale | 85 | 3 | 6 m | 95 | muret 120 PV / 8 s, 2 charges (recharge 10 s) |

### 4.2 Asie

| Figure | PV | DPS | POR | VIT | Le chiffre du kit |
|---|---|---|---|---|---|
| Gilgamesh | 175 | 11 | mêlée | 90 | projection 2 m (1 coup sur 4) |
| Tomoe Gozen | 75 | 11 | 7 m | 115 | tir en mouvement sans malus |
| Arash | 65 | 9 | 10 m | 95 | +3 % de dégâts par mètre de distance (cap +60 %) |
| Himiko | 80 | 3 | 6 m | 100 | bouclier tournant 25 PV / 6 s (1 figure / 2 s) |
| Crésus | 85 | 5 | 4 m | 100 | +1 Ferveur/s passive ; rayon de ramassage ×1,5 |
| Hua Mulan | 75 | 10 | mêlée | 115 | non ciblée après 3 s sans attaquer ; ×1,4 de flanc |
| Miyamoto Musashi | 80 | 11 | mêlée | 110 | ×1,5 si un seul ennemi au contact ; dash offensif (5 s) |
| Sun Tzu | 90 | 3 | 6 m | 95 | fanion r 4 m : ennemis −20 % VIT, alliés +15 % ; 2 actifs max |

### 4.3 Les branches de Légende (T3)

Budget : une branche vaut **+20 à 30 % de la puissance effective du T3**, ou **une charge majeure par manche**. Trois gabarits : offensif conditionnel, défensif de zone, utilitaire à charge. Exemples chiffrés :

- **la Pomme** (Tell A) : critiques ×1,75 sur cible marquée — à ~60 % d'uptime de marque, ≈ +28 % de DPS.
- **le Second Carreau** (Tell B) : exécution des ennemis < 12 % PV max, recharge 4 s.
- **le Regard en arrière** (Orphée B) : 1 résurrection/manche, canalisation 2,5 s à tenir.
- **les Ailes** (Dédale B) : envol du cortège 2,5 s ; au-delà, brûlure 5 % PV max/s.
- **la Quête d'immortalité** (Gilgamesh B) : 1 relève/manche après 3 s au sol, retour à 40 % PV.

Le trait de geste (T2) vaut ~10 points : Tell recharge 25 % plus vite après un critique ; Héraclès étend sa provocation à r 5 m ; Crésus +0,5 Ferveur/s.

---

## 5. La courbe adverse

### 5.1 Montée en puissance parallèle

| Jalon (run EA, ~9–11 manches) | Cortège cible (T1-eq) | Vague standard (Silences-eq) | Élite |
|---|---|---|---|
| Manche 1 | 4 | 8 | — |
| Manche 3 (avant boss Ère I) | 9 | 20 | 1 Anachronisme (≈ 15 Silences) |
| Manche 6 (Ère II) | 18 | 38 | 1–2 Anachronismes |
| Dernière manche | 30–40 | 60 | 2 Anachronismes |

Règles : la vague standard pèse **~55 % de la capacité du cortège cible** (le combat courant est confortable), le pic de manche (2:00–3:00) monte à ~90 %, l'élite à ~120 %. **TTK cibles** : un Silence tombe en ≤ 2 s sous le feu du cortège médian ; le cortège médian ne perd pas de figure hors erreur avant la phase de pic ; la Brume inflige 10 % PV max/s (mise à mort douce, pas de mur).

### 5.2 Les boss — budget en temps, pas en PV

Un boss se chiffre par sa **durée cible** : PV = durée × DPS attendu du cortège au jalon. **Le Léthé** : 4 à 5 min, cortège cible fin d'Ère I ≈ 90–110 DPS → **≈ 25 000 PV**, exposés par fenêtres de 3 × 25 s par phase. **Défusion chiffrée** : 1,5 s cumulées dans l'eau = −1 tier (les récits perdus ne sont pas rendus) ; la surface sèche recule de 15 % par phase.

---

## 6. L'économie de Ferveur (in-run)

| Revenus | Valeur | Coûts | Valeur |
|---|---|---|---|
| Gisement | 10 (4–6 par manche) | **Volume** | **60, +20 par Volume déjà ouvert dans la manche** (remise à zéro entre manches) |
| Ennemi standard | 3 | Étal du marché | 80–160 |
| Élite | 45 | Péages d'événements | 40–80 |
| Coffre d'objectif | 30 | | |
| Chant des Sirènes | +120 (contre 1 figure absente 1 manche) | | |

**Invariant :** revenu médian **160–220 Ferveur/manche** → le joueur normal ouvre **2 Volumes par manche** ; le 3ᵉ (à 100) exige une prise de risque sous la Brume — c'est le « coffre de trop » institutionnalisé. Sur une run EA : 1 600–2 000 Ferveur gagnées, 18–25 drafts. Ces trois chiffres doivent bouger ensemble ou pas du tout.

---

## 7. L'économie d'Encre (méta)

### 7.1 Sources

| Source | Encre |
|---|---|
| Run victorieuse | 40 |
| Run perdue | 10 + 3 par manche franchie (max 34) |
| Haut fait (unique) | 20 |
| Éloge bronze / argent / or | 10 / 20 / 40 |
| Paliers de l'Épreuve (hebdo) | 15 / 30 / 50 |

Cible : **~70 Encre/h en début de partie** (hauts faits et Éloges en façade), ~45/h en régime établi.

### 7.2 Coûts

| Puits | Encre |
|---|---|
| Chronique (retour d'une figure) | 50 |
| Chapitre du Conteur n (n = 1…10) | 40 + 15 × (n−1) → de 40 à 175, total 1 075 |
| Planche du Recueil (cosmétique) | 25 |

**Vérification du plafond :** 4 Chroniques (200) + 10 Chapitres (1 075) ≈ 1 275 Encre ≈ **18 h à 70/h** — conforme au « 15–20 h » de l'annexe systèmes §2.3c. **Garde-fou gravé : tout déblocage de gameplay est atteignable en ≤ 20 h cumulées ; au-delà, l'Encre n'achète que du cosmétique.**

---

## 8. Le score de l'Épreuve — pondérations

| Composante | Formule | Part cible d'un run complet |
|---|---|---|
| **la Distance** | 1 000 / manche franchie + 3 000 / boss vaincu | ≈ 69 % (~15 000) |
| **l'Éclat** | 1 pt / Ferveur récoltée | ≈ 8 % (~1 800) |
| **la Geste** | liste fermée : boss sans Défusion 800 · manche parfaite 200 (cap 5) · 3 Volumes en une manche 100 (cap 3) · Astérion épargné 300 · run sans chute 1 000 | ≈ 13 % (~2 800 max) |
| **le Tempo** | (T_référence − T_réel) × 8, **plafonné à 1 500** | ≤ 7 % |

Départage d'égalité : Tempo, puis essai le plus précoce. **Affichage sans points :** la Fresque indique en quelle *version du récit* (1ᵉʳ, 2ᵉ ou 3ᵉ essai) le score a été réalisé — le prestige du premier jet, gratuit et cruel juste ce qu'il faut. Anti-abus : l'Éclat est mécaniquement borné par le contenu fini des manches et la Brume ; aucune composante ne récompense le temps passé à tourner en rond.

---

## 9. Les Ascensions — gabarit et premiers paliers

**Gabarit :** chaque palier ajoute ≤ +7 % de difficulté effective, et **renforce toujours l'adversité sans jamais retirer d'options au joueur** (exceptions terminales assumées : A19 « draft à 2 choix », A20 « une seule tentative par boss »).

| Palier | Modificateur |
|---|---|
| A1 | la Brume avance 15 % plus vite |
| A2 | Volumes +10 Ferveur au prix de base |
| A3 | +1 élite par Ère |
| A4 | les Censeurs apparaissent dès la manche 1 |
| A5 | soins et boucliers −20 % |

---

## 10. Protocole de validation

**Cibles de santé** (mesurées en alpha, corrigées chaque semaine) : taux de victoire à Ascension 0 après 10 runs : **55–65 %** · taux d'utilisation par figure (hors roster imposé) : **8–18 %** · répartition des branches A/B : **35–65** par figure · durée médiane de manche : **3:20–3:50** · médiane d'Ascension à J30 : **3–5** (repris du GDD §13).

**Outillage :** ce document fixe les rapports ; deux outils les feront vivre — **le classeur de référence** (implémente le barème des 100 points et recalcule le coût de chaque figure à la modification) et **un simulateur Python** (Monte-Carlo de TTK : cortège cible contre vagues budgétées, pour vérifier les tables du §5 sans lancer le moteur).

---

*Document vivant. Toute valeur modifiée doit être répercutée dans le classeur de référence ; toute nouvelle figure passe par la règle des 100 points avant d'entrer en playtest.*
