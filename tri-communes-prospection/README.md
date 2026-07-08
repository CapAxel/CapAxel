# Tri des communes — prospection pour bureau d'étude en urbanisme

Outil de **collecte de données historiques** et de **tri automatique des communes par type de besoin**, pour cibler la prospection commerciale d'un bureau d'étude en urbanisme.

Le principe, en deux temps :

1. **`tri-communes collecter`** interroge l'open data (INSEE, SIRENE, DVF) et construit un fichier CSV par commune : population aux trois derniers recensements, parc de logements et **vacance de logement** (niveau et historique), **résidences secondaires** (niveau et historique), **ancienneté du parc**, **structure par âge** (65+, 80+), **emplois au lieu de travail** (deux recensements), **établissements actifs et commerces**, **lits touristiques marchands**, présence d'un **office de tourisme**, **médiane des prix au m²** sur deux millésimes DVF.
2. **`tri-communes trier`** analyse ce fichier et note chaque commune de 0 à 100 sur **six axes de besoin**, chacun correspondant à une famille de missions du bureau d'étude, puis regroupe les communes par besoin principal.

## Les six axes de besoin

| Axe | Mission type | Signaux utilisés |
|---|---|---|
| **Étude habitat / OPAH** | Étude habitat, OPAH, lutte contre la vacance | Taux de vacance de logement (5 % normal → 15 % critique), son évolution entre deux recensements, part du parc d'avant 1946 |
| **Redynamisation commerciale** | Étude de redynamisation, FISAC/ORT | Vacance commerciale relevée (si saisie), densité commerciale des bourgs ≥ 1 000 hab, emplois en repli |
| **Encadrement du développement** | OAP, études pré-opérationnelles, programmation | Croissance démographique, marché du logement tendu (vacance faible), prix au m² en forte hausse (DVF), rythme de construction |
| **Stratégie de revitalisation** | Petites Villes de Demain, stratégie territoriale | Déclin démographique (court et long terme), perte d'emplois |
| **Adaptation au vieillissement** | OPAH autonomie, adaptation du parc, programmation d'équipements | Part des 65 ans et plus (20 % → 35 %), sa progression entre deux recensements, part des 80 ans et plus |
| **Gestion de la pression touristique** | Stratégie d'accueil, régulation des meublés, logement des actifs | Part de résidences secondaires (10 % → 40 %) et son évolution, lits touristiques marchands pour 100 habitants — **fortement réduit si un dispositif de gestion existe déjà** (office de tourisme détecté via SIRENE) |

Chaque note élémentaire manquante est écartée et les autres renormalisées ; un axe qui ne repose que sur des signaux secondaires est tempéré, et un axe sans aucune donnée est affiché « non évaluable » plutôt que faussement nul. Deux garde-fous supplémentaires : les évolutions d'emploi sont ignorées sous 20 emplois (bruit statistique) et la densité commerciale n'est un signal que pour les bourgs d'au moins 1 000 habitants.

Le **besoin principal** d'une commune est son axe le mieux noté. Le **score global** (70 % meilleur axe + 30 % moyenne des axes, modulé par la taille de la commune — capacité budgétaire probable) débouche sur une priorité : **≥ 65 à démarcher en priorité**, **45–64 à suivre**, **< 45 faible intérêt**.

## Installation

Python ≥ 3.10, aucune dépendance externe.

```bash
git clone <url-du-depot>
cd tri-communes-prospection
pip install -e .
```

## Utilisation

### 1. Collecter les données

```bash
# Toutes les communes d'un département
tri-communes collecter --departement 01 --sortie communes.csv

# Ou une liste de codes INSEE
tri-communes collecter --codes 01053,01004,01093 --sortie communes.csv
```

La collecte interroge, **sans aucune clé d'API** :

- **geo.api.gouv.fr** — nom officiel, EPCI d'appartenance ;
- **API Melodi de l'INSEE** (`DS_RP_SERIE_HISTORIQUE`) — population et parc de logements (total, vacants, résidences secondaires) à chaque recensement ;
- **API Melodi** (`DS_RP_EMPLOI_LT_PRINC`) — emploi au lieu de travail aux derniers recensements ;
- **API Melodi** (`DS_RP_POPULATION_PRINC`) — parts des 65 ans et plus et des 80 ans et plus, deux derniers recensements ;
- **API Melodi** (`DS_RP_LOGEMENT_PRINC`) — part des résidences principales achevées avant 1946 ;
- **API Melodi** (`DS_TOUR_CAP`) — lits en hébergements touristiques marchands (hôtels, campings, autres) ;
- **recherche-entreprises.api.gouv.fr** (SIRENE) — établissements actifs, commerces (section NAF G ; comptages plafonnés à 10 000 par l'API) et présence d'un office de tourisme dans la commune ;
- **files.data.gouv.fr/geo-dvf** — mutations foncières par commune : médiane du prix au m² des ventes de maisons et d'appartements sur le millésime le plus récent et ~4 ans avant (calculée à partir de 5 ventes minimum).

Sur la détection de la gestion touristique : l'outil considère qu'une commune « gère déjà » son tourisme quand un établissement « office de tourisme » actif y est immatriculé. C'est un bon marqueur d'organisation en place, mais il peut rater une commune couverte par l'office intercommunal d'une commune voisine : la colonne `office_tourisme` du CSV est éditable (`oui`/`non`) pour corriger au cas par cas (attention, une nouvelle collecte la recalcule).

### 2. Compléter si possible ce qui n'existe pas en open data

Dans le CSV produit, deux colonnes facultatives affinent l'analyse :

- `taux_vacance_commerciale` (en %) — relevé terrain, CCI ;
- `logements_autorises_3ans` — base Sitadel du SDES.

Si vous relancez la collecte sur le même fichier de sortie, **ces colonnes saisies à la main sont conservées**.

### 3. Trier par besoin

```bash
# Regroupement par besoin principal (défaut)
tri-communes trier communes.csv

# Classement global unique avec le détail des quatre axes
tri-communes trier communes.csv --liste

# Filtres et export
tri-communes trier communes.csv --top 20 --min-score 50 --sortie resultats.csv
```

Un jeu de démonstration **entièrement fictif** est fourni : `tri-communes trier data/communes_exemple.csv`.

## Format du fichier de communes

Produit par `collecter`, éditable dans un tableur. Seules `code_insee` et `nom` sont obligatoires : toute donnée absente est traitée comme « non disponible ».

| Colonne | Remplie par | Description |
|---|---|---|
| `code_insee`, `nom`, `epci` | collecte | Identité de la commune |
| `population`, `population_prec`, `population_anc`, `annee_recensement` | collecte | Population aux trois derniers recensements |
| `logements`, `logements_vacants`, `residences_secondaires` | collecte | Parc au dernier recensement |
| `logements_prec`, `logements_vacants_prec`, `residences_secondaires_prec` | collecte | Parc au recensement précédent (→ évolutions) |
| `part_logements_avant_1946` | collecte | Part des résidences principales d'avant 1946, en % |
| `part_65plus`, `part_65plus_prec`, `part_80plus` | collecte | Structure par âge, en % de la population |
| `emplois`, `emplois_prec` | collecte | Emploi au lieu de travail, deux derniers recensements |
| `nb_etablissements`, `nb_commerces` | collecte | Tissu économique actuel (SIRENE) |
| `lits_touristiques` | collecte | Lits en hébergements touristiques marchands (INSEE) |
| `office_tourisme` | collecte (éditable) | Un office de tourisme est immatriculé dans la commune |
| `prix_m2`, `prix_m2_prec` | collecte | Médiane €/m² (DVF), millésime récent et ~4 ans avant |
| `taux_vacance_commerciale` | manuel | Vacance des locaux commerciaux, en % |
| `logements_autorises_3ans` | manuel | Logements autorisés sur 3 ans (Sitadel) |

## Structure du projet

```
src/tri_communes/
  modeles.py      # Commune, indicateurs dérivés (taux, évolutions), AnalyseCommune
  collecte.py     # Connecteurs open data (geo.api.gouv.fr, Melodi INSEE, SIRENE, DVF)
  besoins.py      # Les six axes de besoin, score global, regroupement
  chargement.py   # Lecture / écriture CSV
  cli.py          # Sous-commandes « collecter » et « trier »
data/
  communes_exemple.csv   # Jeu de données fictif de démonstration
tests/
  test_scoring.py        # Tests des axes de besoin et du chargement
  test_collecte.py       # Tests de la collecte (API simulées)
```

## Pistes d'évolution

- Connecteur Sitadel (logements autorisés) pour supprimer les dernières saisies manuelles.
- Score « concurrence » : densité de bureaux d'étude déjà actifs sur le territoire.
- Meilleure détection de la gestion touristique (stations classées, offices intercommunaux).
- Export cartographique (GeoJSON) pour visualiser les cibles par besoin dans QGIS.
