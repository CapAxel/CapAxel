# Tri des communes — prospection pour bureau d'étude en urbanisme

Outil de **scoring et de tri automatique des communes** selon leur intérêt à être démarchées par un bureau d'étude en urbanisme (élaboration ou révision de PLU, cartes communales, études pré-opérationnelles, AMO…).

L'idée : plutôt que de prospecter au hasard, on note chaque commune de 0 à 100 à partir de critères objectifs, puis on trie la liste pour concentrer l'effort commercial là où la probabilité d'un besoin d'étude est la plus forte.

## Méthodologie de scoring

Chaque commune reçoit une note de 0 à 1 sur cinq critères, combinés en un score global sur 100 via des pondérations configurables :

| Critère | Poids par défaut | Logique |
|---|---|---|
| **Document d'urbanisme** | 35 % | Le cœur du besoin. POS caduc ou RNU → très forte opportunité (élaboration d'un PLU probable). PLU ancien (pré-ALUR, > 13 ans) → révision attendue. PLU ou PLUi récent → faible besoin. Si la compétence PLU est transférée à l'EPCI, l'intérêt de démarcher la commune seule chute (le prospect devient l'intercommunalité). |
| **Dynamique de construction** | 20 % | Logements autorisés sur 3 ans rapportés à 1 000 habitants : une commune qui construit a besoin d'encadrer son développement. |
| **Dynamique démographique** | 15 % | Évolution de la population sur ~5 ans : la croissance crée des besoins (zonage, équipements, OAP). |
| **Taille de la commune** | 15 % | Courbe en cloche : les très petites communes ont peu de budget, les grandes villes ont des services internes ou attirent les gros cabinets. La cible idéale se situe entre ~500 et 5 000 habitants. |
| **Proximité de l'agence** | 15 % | Distance à l'agence : les réunions publiques et comités de pilotage rendent les missions lointaines moins rentables. |

Le score débouche sur une priorité de démarchage :

- **≥ 65 : à démarcher en priorité**
- **45 – 64 : à suivre** (relance, veille sur les délibérations)
- **< 45 : faible intérêt** pour l'instant

Les seuils et pondérations sont des valeurs de départ raisonnables pour un bureau d'étude généraliste : ajustez-les à votre positionnement via `--poids` (voir plus bas).

## Installation

Python ≥ 3.10, aucune dépendance externe pour le cœur de l'outil.

```bash
git clone <url-du-depot>
cd tri-communes-prospection
pip install -e .
```

## Utilisation

```bash
# Trier le fichier d'exemple et afficher le classement
tri-communes data/communes_exemple.csv

# Garder les 10 meilleures, exporter en CSV
tri-communes data/communes_exemple.csv --top 10 --sortie resultats.csv

# Ne garder que les communes au-dessus d'un score
tri-communes data/communes_exemple.csv --min-score 50

# Utiliser vos propres pondérations
tri-communes data/communes_exemple.csv --poids mes_poids.json
```

Exemple de fichier de pondérations (`mes_poids.json`) — les poids sont renormalisés automatiquement :

```json
{
  "document_urbanisme": 0.5,
  "dynamique_construction": 0.15,
  "dynamique_demographique": 0.1,
  "taille_commune": 0.1,
  "proximite_agence": 0.15
}
```

Sans installation, le module se lance aussi directement :

```bash
python -m tri_communes.cli data/communes_exemple.csv
```

## Format du fichier d'entrée

CSV avec en-tête, une ligne par commune :

| Colonne | Type | Description |
|---|---|---|
| `code_insee` | texte | Code INSEE de la commune |
| `nom` | texte | Nom de la commune |
| `population` | entier | Population municipale |
| `evolution_population_pct` | décimal | Évolution de la population sur ~5 ans, en % (ex. `3.2`, `-1.5`) |
| `logements_autorises_3ans` | entier | Logements autorisés (permis) sur les 3 dernières années |
| `document_urbanisme` | texte | `RNU`, `CC` (carte communale), `POS`, `PLU` ou `PLUi` |
| `annee_approbation` | entier | Année d'approbation du document en vigueur (vide si RNU) |
| `competence_plu_epci` | oui/non | La compétence PLU est-elle transférée à l'EPCI ? |
| `epci` | texte | Nom de l'EPCI (facultatif, informatif) |
| `distance_agence_km` | décimal | Distance route jusqu'à l'agence (vide = neutre) |

Le fichier `data/communes_exemple.csv` fournit un jeu de démonstration **entièrement fictif**.

## Où trouver les vraies données

Toutes les colonnes se remplissent depuis l'open data :

- **Population et évolution** : recensement INSEE (populations légales, via [insee.fr](https://www.insee.fr) ou l'API `geo.api.gouv.fr`).
- **Permis de construire / logements autorisés** : base **Sitadel** du SDES ([statistiques.developpement-durable.gouv.fr](https://www.statistiques.developpement-durable.gouv.fr)).
- **Document d'urbanisme en vigueur et son année** : **Géoportail de l'urbanisme** ([geoportail-urbanisme.gouv.fr](https://www.geoportail-urbanisme.gouv.fr)) et l'enquête **Sudocuh** (données annuelles publiées sur data.gouv.fr).
- **EPCI et compétence PLU** : base **BANATIC** ([banatic.interieur.gouv.fr](https://www.banatic.interieur.gouv.fr)) et `geo.api.gouv.fr` pour l'appartenance intercommunale.
- **Distance à l'agence** : n'importe quel calculateur d'itinéraires ; à défaut, distance à vol d'oiseau majorée de ~25 %.

## Structure du projet

```
src/tri_communes/
  modeles.py      # Dataclasses Commune / ScoreCommune, types de documents d'urbanisme
  scoring.py      # Notes par critère, pondérations, calcul et tri
  chargement.py   # Lecture / écriture CSV
  cli.py          # Interface en ligne de commande
data/
  communes_exemple.csv   # Jeu de données fictif de démonstration
tests/
  test_scoring.py        # Tests du moteur de scoring et du chargement
```

## Pistes d'évolution

- Connecteurs automatiques vers `geo.api.gouv.fr`, Sitadel et Sudocuh pour construire le CSV sans saisie manuelle.
- Prise en compte des délibérations de prescription (une révision déjà prescrite = appel d'offres imminent).
- Score « concurrence » : densité de bureaux d'étude déjà actifs sur le territoire.
- Export cartographique (GeoJSON) pour visualiser les cibles dans QGIS.
