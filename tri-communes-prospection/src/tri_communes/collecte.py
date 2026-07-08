"""Collecte automatique des données historiques d'une commune.

Sources interrogées (open data, sans clé d'API) :

- **geo.api.gouv.fr** : nom officiel et EPCI d'appartenance.
- **API Melodi de l'INSEE**, jeu ``DS_RP_SERIE_HISTORIQUE`` : population et
  parc de logements (total, vacants, résidences secondaires) à chaque
  recensement depuis 1968.
- **API Melodi**, jeu ``DS_RP_EMPLOI_LT_PRINC`` : emploi au lieu de travail
  aux derniers recensements.
- **API Melodi**, jeu ``DS_RP_POPULATION_PRINC`` : structure par âge
  (parts des 65 ans et plus, des 80 ans et plus) aux derniers recensements.
- **API Melodi**, jeu ``DS_RP_LOGEMENT_PRINC`` : période d'achèvement des
  résidences principales (part du parc d'avant 1946).
- **API Melodi**, jeu ``DS_TOUR_CAP`` : lits en hébergements touristiques
  marchands (hôtels, campings, autres hébergements collectifs).
- **recherche-entreprises.api.gouv.fr** (SIRENE) : nombre d'établissements
  actifs, nombre de commerces (section NAF G) et présence d'un office de
  tourisme. Ces comptages sont plafonnés à 10 000 par l'API — sans incidence
  sur les communes ciblées en prospection.
- **files.data.gouv.fr/geo-dvf** : mutations foncières par commune, dont on
  tire la médiane de prix au m² (maisons et appartements) sur deux
  millésimes pour mesurer la pression immobilière.

Restent à saisir à la main (pas d'open data national fiable) : la vacance
commerciale relevée et les logements autorisés (Sitadel).
"""

from __future__ import annotations

import csv
import io
import json
import statistics
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date
from typing import Callable

from .chargement import COLONNES_MANUELLES
from .modeles import Commune

URL_GEO = "https://geo.api.gouv.fr"
URL_MELODI = "https://api.insee.fr/melodi/data"
URL_SIRENE = "https://recherche-entreprises.api.gouv.fr/search"
URL_DVF = "https://files.data.gouv.fr/geo-dvf/latest/csv"

PREMIER_MILLESIME_DVF = 2021  # les fichiers « latest » ne remontent pas plus tôt

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


def _telecharger_texte(url: str) -> str | None:
    """Télécharge un fichier texte ; renvoie None si la ressource n'existe pas."""
    requete = urllib.request.Request(
        url, headers={"User-Agent": "tri-communes-prospection/0.4"}
    )
    derniere_erreur: Exception | None = None
    for tentative in range(TENTATIVES):
        try:
            with urllib.request.urlopen(requete, timeout=60) as reponse:
                return reponse.read().decode("utf-8")
        except urllib.error.HTTPError as erreur:
            if erreur.code == 404:
                return None
            derniere_erreur = erreur
        except (urllib.error.URLError, TimeoutError) as erreur:
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
            resultat["residences_secondaires_prec"] = logements.get(
                (avant, "DW_SEC_DW_OCC")
            )
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


def _structure_par_age(code_insee: str) -> dict:
    """Parts des 65 ans et plus et des 80 ans et plus, deux derniers recensements."""
    donnees = _obtenir_json(
        f"{URL_MELODI}/DS_RP_POPULATION_PRINC",
        {"GEO": f"COM-{code_insee}", "maxResult": 2000},
    )
    valeurs: dict[tuple[int, str], float] = {}
    for observation in donnees.get("observations", []):
        dimensions = observation.get("dimensions", {})
        if dimensions.get("RP_MEASURE") != "POP" or dimensions.get("SEX") != "_T":
            continue
        age = dimensions.get("AGE")
        if age not in ("Y_GE65", "Y_GE80", "_T"):
            continue
        valeur = (
            observation.get("measures", {})
            .get("OBS_VALUE_NIVEAU", {})
            .get("value")
        )
        if valeur is not None:
            valeurs[(int(dimensions.get("TIME_PERIOD", 0)), age)] = valeur

    annees = sorted({annee for annee, _ in valeurs})
    resultat: dict = {}

    def _part(annee: int, age: str) -> float | None:
        total = valeurs.get((annee, "_T"))
        cible = valeurs.get((annee, age))
        if not total or cible is None:
            return None
        return round(cible / total * 100.0, 1)

    if annees:
        derniere = annees[-1]
        resultat["part_65plus"] = _part(derniere, "Y_GE65")
        resultat["part_80plus"] = _part(derniere, "Y_GE80")
        if len(annees) >= 2:
            resultat["part_65plus_prec"] = _part(annees[-2], "Y_GE65")
    return resultat


def _parc_ancien(code_insee: str) -> dict:
    """Part des résidences principales achevées avant 1946 (%).

    Pour chaque millésime, on retient la valeur la plus agrégée disponible
    (toutes les autres ventilations à « _T ») ; la nomenclature des périodes
    varie selon les millésimes (Y_LT1946 ou Y_LT1919 + Y1919T1945).
    """
    donnees = _obtenir_json(
        f"{URL_MELODI}/DS_RP_LOGEMENT_PRINC",
        {"GEO": f"COM-{code_insee}", "maxResult": 5000},
    )
    valeurs: dict[tuple[int, str], float] = {}
    for observation in donnees.get("observations", []):
        dimensions = observation.get("dimensions", {})
        if (
            dimensions.get("RP_MEASURE") != "DWELLINGS"
            or dimensions.get("OCS") != "DW_MAIN"
        ):
            continue
        periode = dimensions.get("BUILD_END")
        if periode not in ("Y_LT1946", "Y_LT1919", "Y1919T1945", "_T"):
            continue
        ventile = any(
            valeur not in ("_T", "_Z")
            for cle, valeur in dimensions.items()
            if cle not in ("GEO", "FREQ", "TIME_PERIOD", "RP_MEASURE", "OCS", "BUILD_END")
        )
        if ventile:
            continue
        valeur = (
            observation.get("measures", {})
            .get("OBS_VALUE_NIVEAU", {})
            .get("value")
        )
        if valeur is not None:
            annee = int(dimensions.get("TIME_PERIOD", 0))
            # Des combinaisons neutres en doublon (« _Z ») peuvent valoir 0 :
            # on retient la valeur la plus agrégée, donc la plus grande.
            cle = (annee, periode)
            valeurs[cle] = max(valeurs.get(cle, 0.0), valeur)

    for annee in sorted({a for a, _ in valeurs}, reverse=True):
        total = valeurs.get((annee, "_T"))
        avant_1946 = valeurs.get((annee, "Y_LT1946"))
        if avant_1946 is None and (annee, "Y_LT1919") in valeurs:
            avant_1946 = valeurs[(annee, "Y_LT1919")] + valeurs.get(
                (annee, "Y1919T1945"), 0.0
            )
        if total and avant_1946 is not None:
            return {"part_logements_avant_1946": round(avant_1946 / total * 100.0, 1)}
    return {}


def _lits_touristiques(code_insee: str) -> dict:
    """Lits en hébergements touristiques marchands (hôtels, campings, autres)."""
    try:
        donnees = _obtenir_json(
            f"{URL_MELODI}/DS_TOUR_CAP",
            {"GEO": f"COM-{code_insee}", "maxResult": 2000},
        )
    except ErreurCollecte:
        return {}  # les communes sans hébergement marchand sont absentes du jeu
    lits: dict[str, float] = {}
    for observation in donnees.get("observations", []):
        dimensions = observation.get("dimensions", {})
        if dimensions.get("TOUR_MEASURE") != "BEDPLACE":
            continue
        if dimensions.get("L_STAY", "_T") != "_T":
            continue
        if dimensions.get("UNIT_LOC_RANKING", "_T") != "_T":
            continue
        activite = dimensions.get("ACTIVITY", "")
        if activite not in ("I551", "I552", "I553"):  # familles de niveau 1
            continue
        valeur = (
            observation.get("measures", {})
            .get("OBS_VALUE_NIVEAU", {})
            .get("value")
        )
        if valeur is not None:
            lits[activite] = max(lits.get(activite, 0.0), valeur)
    if not lits:
        return {}
    return {"lits_touristiques": int(round(sum(lits.values())))}


def _office_tourisme(code_insee: str) -> bool:
    """Un établissement « office de tourisme » actif existe dans la commune."""
    donnees = _obtenir_json(
        URL_SIRENE,
        {
            "q": "office de tourisme",
            "code_commune": code_insee,
            "per_page": 1,
            "page": 1,
        },
    )
    return int(donnees.get("total_results", 0)) > 0


def _mediane_prix_m2(code_insee: str, annee: int) -> float | None:
    """Médiane du prix au m² des ventes de maisons et d'appartements (DVF)."""
    departement = code_insee[:3] if code_insee.startswith("97") else code_insee[:2]
    contenu = _telecharger_texte(
        f"{URL_DVF}/{annee}/communes/{departement}/{code_insee}.csv"
    )
    if contenu is None:
        return None

    # Une mutation occupe plusieurs lignes (une par local) qui répètent la
    # même valeur foncière : on agrège les surfaces par mutation.
    mutations: dict[str, tuple[float, float]] = {}
    for ligne in csv.DictReader(io.StringIO(contenu)):
        if ligne.get("nature_mutation") != "Vente":
            continue
        if ligne.get("type_local") not in ("Maison", "Appartement"):
            continue
        try:
            valeur = float(ligne["valeur_fonciere"])
            surface = float(ligne["surface_reelle_bati"])
        except (KeyError, TypeError, ValueError):
            continue
        if valeur <= 0 or surface <= 0:
            continue
        identifiant = ligne.get("id_mutation", "")
        _, surface_cumulee = mutations.get(identifiant, (valeur, 0.0))
        mutations[identifiant] = (valeur, surface_cumulee + surface)

    prix = [
        valeur / surface
        for valeur, surface in mutations.values()
        if surface >= 10 and 250 <= valeur / surface <= 20000
    ]
    if len(prix) < 5:  # trop peu de ventes pour une médiane fiable
        return None
    return round(statistics.median(prix), 0)


def _prix_immobilier(code_insee: str) -> dict:
    """Médianes de prix au m² sur le millésime DVF récent et ~4 ans avant."""
    resultat: dict = {}
    annee = date.today().year
    while annee >= PREMIER_MILLESIME_DVF:
        mediane = _mediane_prix_m2(code_insee, annee)
        if mediane is not None:
            resultat["prix_m2"] = mediane
            break
        annee -= 1
    if "prix_m2" in resultat:
        annee_prec = max(annee - 4, PREMIER_MILLESIME_DVF)
        if annee_prec < annee:
            time.sleep(DELAI_ENTRE_REQUETES)
            resultat["prix_m2_prec"] = _mediane_prix_m2(code_insee, annee_prec)
    return resultat


# --- Collecte ----------------------------------------------------------------


def collecter_commune(code_insee: str) -> Commune:
    """Collecte toutes les données disponibles pour une commune."""
    identite = _identite(code_insee)
    time.sleep(DELAI_ENTRE_REQUETES)
    historique = _serie_historique(code_insee)
    time.sleep(DELAI_ENTRE_REQUETES)
    emplois = _emplois(code_insee)
    time.sleep(DELAI_ENTRE_REQUETES)
    ages = _structure_par_age(code_insee)
    time.sleep(DELAI_ENTRE_REQUETES)
    parc_ancien = _parc_ancien(code_insee)
    time.sleep(DELAI_ENTRE_REQUETES)
    tourisme = _lits_touristiques(code_insee)
    time.sleep(DELAI_ENTRE_REQUETES)
    nb_etablissements = _nombre_etablissements(code_insee)
    time.sleep(DELAI_ENTRE_REQUETES)
    nb_commerces = _nombre_etablissements(
        code_insee, section_activite_principale="G"
    )
    time.sleep(DELAI_ENTRE_REQUETES)
    office = _office_tourisme(code_insee)
    time.sleep(DELAI_ENTRE_REQUETES)
    prix = _prix_immobilier(code_insee)

    return Commune(
        code_insee=code_insee,
        nom=identite["nom"],
        epci=identite["epci"],
        nb_etablissements=nb_etablissements,
        nb_commerces=nb_commerces,
        office_tourisme=office,
        **historique,
        **emplois,
        **ages,
        **parc_ancien,
        **tourisme,
        **prix,
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
