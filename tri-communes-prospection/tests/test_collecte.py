"""Tests de la collecte (API simulées, aucun appel réseau)."""

import pytest

from tri_communes import collecter_commune, fusionner_donnees_manuelles
from tri_communes.modeles import Commune, DocumentUrbanisme
from tri_communes import collecte


def _observation(mesure: str, annee: str, valeur: float, **dims) -> dict:
    return {
        "dimensions": {"RP_MEASURE": mesure, "TIME_PERIOD": annee, **dims},
        "measures": {"OBS_VALUE_NIVEAU": {"value": valeur}},
    }


REPONSES = {
    "geo.api.gouv.fr/communes/01053": {
        "nom": "Bourg-en-Bresse",
        "epci": {"nom": "CA du Bassin de Bourg-en-Bresse"},
    },
    "DS_RP_SERIE_HISTORIQUE": {
        "observations": [
            _observation("POP", "2012", 40171),
            _observation("POP", "2017", 41527),
            _observation("POP", "2023", 42372),
            _observation("DWELLINGS", "2017", 23415.0, OCS="_T"),
            _observation("DWELLINGS", "2017", 2509.8, OCS="DW_VAC"),
            _observation("DWELLINGS", "2023", 23844.7, OCS="_T"),
            _observation("DWELLINGS", "2023", 2290.7, OCS="DW_VAC"),
            _observation("DWELLINGS", "2023", 584.2, OCS="DW_SEC_DW_OCC"),
        ]
    },
    "DS_RP_EMPLOI_LT_PRINC": {
        "observations": [
            _observation("NBEMP", "2017", 31914.9, SEX="_T"),
            _observation("NBEMP", "2017", 17321.8, SEX="F"),
            _observation("NBEMP", "2023", 33552.5, SEX="_T"),
            _observation("NBEMP", "2023", 18243.0, SEX="F"),
        ]
    },
    "recherche-entreprises": [
        {"total_results": 9800},  # tous établissements
        {"total_results": 2950},  # section G (commerce)
    ],
}


@pytest.fixture
def api_simulee(monkeypatch):
    sirene_appels = iter(REPONSES["recherche-entreprises"])

    def faux_obtenir_json(url, parametres=None):
        if "geo.api.gouv.fr/communes/" in url:
            return REPONSES["geo.api.gouv.fr/communes/01053"]
        if "DS_RP_SERIE_HISTORIQUE" in url:
            return REPONSES["DS_RP_SERIE_HISTORIQUE"]
        if "DS_RP_EMPLOI_LT_PRINC" in url:
            return REPONSES["DS_RP_EMPLOI_LT_PRINC"]
        if "recherche-entreprises" in url:
            return next(sirene_appels)
        raise AssertionError(f"URL inattendue : {url}")

    monkeypatch.setattr(collecte, "_obtenir_json", faux_obtenir_json)
    monkeypatch.setattr(collecte.time, "sleep", lambda _: None)


def test_collecte_commune_complete(api_simulee):
    commune = collecter_commune("01053")
    assert commune.nom == "Bourg-en-Bresse"
    assert commune.epci == "CA du Bassin de Bourg-en-Bresse"
    assert commune.population == 42372
    assert commune.population_prec == 41527
    assert commune.population_anc == 40171
    assert commune.annee_recensement == 2023
    assert commune.logements == pytest.approx(23844.7)
    assert commune.logements_vacants == pytest.approx(2290.7)
    assert commune.logements_vacants_prec == pytest.approx(2509.8)
    assert commune.emplois == pytest.approx(33552.5)   # total = max des ventilations
    assert commune.emplois_prec == pytest.approx(31914.9)
    assert commune.nb_etablissements == 9800
    assert commune.nb_commerces == 2950
    # Les indicateurs dérivés se calculent directement sur les données collectées
    assert commune.taux_vacance_logement == pytest.approx(9.6, abs=0.1)


def test_fusion_conserve_les_colonnes_manuelles():
    collectee = Commune(code_insee="01053", nom="Bourg-en-Bresse")
    ancienne = Commune(
        code_insee="01053",
        nom="Bourg-en-Bresse",
        document_urbanisme=DocumentUrbanisme.PLU,
        annee_approbation=2015,
        competence_plu_epci=True,
        taux_vacance_commerciale=12.0,
        logements_autorises_3ans=300,
    )
    fusionnees = fusionner_donnees_manuelles([collectee], [ancienne])
    resultat = fusionnees[0]
    assert resultat.document_urbanisme is DocumentUrbanisme.PLU
    assert resultat.annee_approbation == 2015
    assert resultat.competence_plu_epci is True
    assert resultat.taux_vacance_commerciale == pytest.approx(12.0)
    assert resultat.logements_autorises_3ans == 300
