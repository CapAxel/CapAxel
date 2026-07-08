"""Collecte automatique des données historiques d'une commune.

Sources interrogées (open data, sans clé d'API) :

- **geo.api.gouv.fr** : nom officiel et EPCI d'appartenance.
- **API Melodi de l'INSEE**, jeu ``DS_RP_SERIE_HISTORIQUE`` : population et
  parc de logements (total, vacants, résidences secondaires) à chaque
  recensement depuis 1968.
- **API Melodi**, jeu ``DS_RP_EMPLOI_LT_PRINC`` : emploi au lieu de travail
  aux derniers recensements.
- **recherche-entreprises.api.gouv.fr** (SIRENE) : nombre d'établissements
  actifs et nombre de commerces (section NAF G). Ces comptages sont plafonnés
  à 10 000 par l'API — sans incidence sur les communes ciblées en prospection.

Restent à saisir à la main (pas d'open data national fiable) : la vacance
commerciale relevée et les logements autorisés (Sitadel).
"""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Callable

from .chargement import COLONNES_MANUELLES
from .modeles import Commune

URL_GEO = "https://geo.api.gouv.fr"
URL_MELODI = "https://api.insee.fr/melodi/data"
URL_SIRENE = "https://recherche-entreprises.api.gouv.fr/search"

DELAI_ENTRE_REQUETES = 0.15  # secondes ; l'API SIRENE tolère 7 requêtes/s
TENTATIVES = 3


class ErreurCollecte(RuntimeError):
    """Échec de collecte pour une commune (réseau ou code INSEE inconnu)."""


def _obtenir_json(url: str, parametres: dict | None = None) -> dict | list:
    if parametres:
        # Certains paramètres (GEO) peuvent être répétés : doseq les gère.
        url = f"{url}?{urllib.parse.urlencode(parametres, doseq=True)}"
    requete = urllib.request.Request(
        url, headers={"User-Agent": "tri-communes-prospection/0.2"}
    )
    derniere_erreur: Exception | None = None
    for tentative in range(TENTATIVES):
        try:
            with urllib.request.urlopen(requete, timeout=30) as reponse:
                return json.load(reponse)
        except urllib.error.HTTPError as erreur:
            if erreur.code == 404:
                raise ErreurCollecte(f"Ressource introuvable : {url}") from erreur
            derniere_erreur = erreur
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as erreur:
            derniere_erreur = erreur
        time.sleep(1.5 * (tentative + 1))
    raise ErreurCollecte(f"Échec après {TENTATIVES} tentatives : {url}") from derniere_erreur


# --- Connecteurs -------------------------------------------------------------


def _identite(code_insee: str) -> dict:
    donnees = _obtenir_json(
        f"{URL_GEO}/communes/{code_insee}", {"fields": "nom,epci"}
    )
    return {
        "nom": donnees.get("nom", ""),
        "epci": (donnees.get("epci") or {}).get("nom", ""),
    }


def _serie_historique(code_insee: str) -> dict:
    """Population et logements aux trois derniers recensements."""
    donnees = _obtenir_json(
        f"{URL_MELODI}/DS_RP_SERIE_HISTORIQUE",
        {"GEO": f"COM-{code_insee}", "maxResult": 2000},
    )
    populations: dict[int, float] = {}
    logements: dict[tuple[int, str], float] = {}
    for observation in donnees.get("observations", []):
        dimensions = observation.get("dimensions", {})
        valeur = (
            observation.get("measures", {})
            .get("OBS_VALUE_NIVEAU", {})
            .get("value")
        )
        if valeur is None:
            continue
        annee = int(dimensions.get("TIME_PERIOD", 0))
        mesure = dimensions.get("RP_MEASURE")
        if mesure == "POP":
            populations[annee] = valeur
        elif mesure == "DWELLINGS":
            logements[(annee, dimensions.get("OCS", ""))] = valeur

    annees = sorted(populations)
    resultat: dict = {}
    if annees:
        derniere = annees[-1]
        resultat["annee_recensement"] = derniere
        resultat["population"] = int(round(populations[derniere]))
        if len(annees) >= 2:
            resultat["population_prec"] = int(round(populations[annees[-2]]))
        if len(annees) >= 3:
            resultat["population_anc"] = int(round(populations[annees[-3]]))

    annees_logements = sorted({annee for annee, _ in logements})
    if annees_logements:
        derniere = annees_logements[-1]
        resultat["logements"] = logements.get((derniere, "_T"))
        resultat["logements_vacants"] = logements.get((derniere, "DW_VAC"))
        resultat["residences_secondaires"] = logements.get(
            (derniere, "DW_SEC_DW_OCC")
        )
        if len(annees_logements) >= 2:
            avant = annees_logements[-2]
            resultat["logements_prec"] = logements.get((avant, "_T"))
            resultat["logements_vacants_prec"] = logements.get((avant, "DW_VAC"))
    return resultat


def _emplois(code_insee: str) -> dict:
    """Emploi total au lieu de travail aux deux derniers recensements.

    Le total (toutes ventilations confondues) est la plus grande valeur NBEMP
    observée pour chaque millésime.
    """
    donnees = _obtenir_json(
        f"{URL_MELODI}/DS_RP_EMPLOI_LT_PRINC",
        {"GEO": f"COM-{code_insee}", "maxResult": 2000},
    )
    totaux: dict[int, float] = {}
    for observation in donnees.get("observations", []):
        dimensions = observation.get("dimensions", {})
        if dimensions.get("RP_MEASURE") != "NBEMP":
            continue
        valeur = (
            observation.get("measures", {})
            .get("OBS_VALUE_NIVEAU", {})
            .get("value")
        )
        if valeur is None:
            continue
        annee = int(dimensions.get("TIME_PERIOD", 0))
        totaux[annee] = max(totaux.get(annee, 0.0), valeur)

    annees = sorted(totaux)
    resultat: dict = {}
    if annees:
        resultat["emplois"] = totaux[annees[-1]]
        if len(annees) >= 2:
            resultat["emplois_prec"] = totaux[annees[-2]]
    return resultat


def _nombre_etablissements(code_insee: str, **filtres) -> int:
    donnees = _obtenir_json(
        URL_SIRENE,
        {"code_commune": code_insee, "per_page": 1, "page": 1, **filtres},
    )
    return int(donnees.get("total_results", 0))


# --- Collecte ----------------------------------------------------------------


def collecter_commune(code_insee: str) -> Commune:
    """Collecte toutes les données disponibles pour une commune."""
    identite = _identite(code_insee)
    time.sleep(DELAI_ENTRE_REQUETES)
    historique = _serie_historique(code_insee)
    time.sleep(DELAI_ENTRE_REQUETES)
    emplois = _emplois(code_insee)
    time.sleep(DELAI_ENTRE_REQUETES)
    nb_etablissements = _nombre_etablissements(code_insee)
    time.sleep(DELAI_ENTRE_REQUETES)
    nb_commerces = _nombre_etablissements(
        code_insee, section_activite_principale="G"
    )

    return Commune(
        code_insee=code_insee,
        nom=identite["nom"],
        epci=identite["epci"],
        nb_etablissements=nb_etablissements,
        nb_commerces=nb_commerces,
        **historique,
        **emplois,
    )


def codes_du_departement(departement: str) -> list[str]:
    """Liste les codes INSEE des communes d'un département."""
    donnees = _obtenir_json(
        f"{URL_GEO}/departements/{departement}/communes", {"fields": "code"}
    )
    return [commune["code"] for commune in donnees]


def fusionner_donnees_manuelles(
    collectees: list[Commune], existantes: list[Commune]
) -> list[Commune]:
    """Reporte les colonnes saisies à la main d'un fichier précédent.

    Permet de relancer la collecte sans perdre le travail de qualification
    (document d'urbanisme, vacance commerciale relevée, etc.).
    """
    par_code = {commune.code_insee: commune for commune in existantes}
    for commune in collectees:
        ancienne = par_code.get(commune.code_insee)
        if ancienne is None:
            continue
        for champ in COLONNES_MANUELLES:
            setattr(commune, champ, getattr(ancienne, champ))
    return collectees


def collecter_communes(
    codes: list[str],
    rappel: Callable[[str, int, int], None] | None = None,
) -> tuple[list[Commune], list[tuple[str, str]]]:
    """Collecte une liste de communes ; renvoie (réussites, échecs).

    ``rappel(code, index, total)`` est appelé avant chaque commune pour
    afficher la progression.
    """
    communes: list[Commune] = []
    echecs: list[tuple[str, str]] = []
    total = len(codes)
    for index, code in enumerate(codes, start=1):
        if rappel:
            rappel(code, index, total)
        try:
            communes.append(collecter_commune(code))
        except ErreurCollecte as erreur:
            echecs.append((code, str(erreur)))
        time.sleep(DELAI_ENTRE_REQUETES)
    return communes, echecs
