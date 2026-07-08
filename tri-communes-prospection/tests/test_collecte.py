"""Tests de la collecte (API simulées, aucun appel réseau)."""

import pytest

from tri_communes import collecter_commune, fusionner_donnees_manuelles
from tri_communes.modeles import Commune
from tri_communes import collecte


def _observation(mesure: str, annee: str, valeur: float, **dims) -> dict:
    return {
        "dimensions": {"RP_MEASURE": mesure, "TIME_PERIOD": annee, **dims},
        "measures": {"OBS_VALUE_NIVEAU": {"value": valeur}},
    }


def _csv_dvf(prix_m2: float) -> str:
    lignes = ["id_mutation,nature_mutation,valeur_fonciere,type_local,surface_reelle_bati"]
    for i in range(6):
        lignes.append(f"m{i},Vente,{prix_m2 * 100:.0f},Maison,100")
    lignes.append("m9,Vente,50000,Dépendance,0")  # ignorée (pas un logement)
    return "\n".join(lignes)


REPONSES_MELODI = {
    "DS_RP_SERIE_HISTORIQUE": {
        "observations": [
            _observation("POP", "2012", 40171),
            _observation("POP", "2017", 41527),
            _observation("POP", "2023", 42372),
            _observation("DWELLINGS", "2017", 23415.0, OCS="_T"),
            _observation("DWELLINGS", "2017", 2509.8, OCS="DW_VAC"),
            _observation("DWELLINGS", "2017", 608.0, OCS="DW_SEC_DW_OCC"),
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
    "DS_RP_POPULATION_PRINC": {
        "observations": [
            _observation("POP", "2017", 41527, SEX="_T", AGE="_T"),
            _observation("POP", "2017", 7475, SEX="_T", AGE="Y_GE65"),
            _observation("POP", "2023", 42372, SEX="_T", AGE="_T"),
            _observation("POP", "2023", 8898, SEX="_T", AGE="Y_GE65"),
            _observation("POP", "2023", 2966, SEX="_T", AGE="Y_GE80"),
            # Une ventilation par sexe qui doit être ignorée
            _observation("POP", "2023", 5100, SEX="F", AGE="Y_GE65"),
        ]
    },
    "DS_RP_LOGEMENT_PRINC": {
        "observations": [
            _observation("DWELLINGS", "2023", 20969.8, OCS="DW_MAIN", BUILD_END="_T"),
            _observation(
                "DWELLINGS", "2023", 4200.0, OCS="DW_MAIN", BUILD_END="Y_LT1946"
            ),
            # Une ventilation par taille qui doit être ignorée
            _observation(
                "DWELLINGS", "2023", 900.0, OCS="DW_MAIN", BUILD_END="Y_LT1946", TDW="1"
            ),
        ]
    },
    "DS_TOUR_CAP": {
        "observations": [
            _observation("", "2026", 800.0, TOUR_MEASURE="BEDPLACE", ACTIVITY="I551"),
            _observation("", "2026", 450.0, TOUR_MEASURE="BEDPLACE", ACTIVITY="I552"),
            # Sous-famille qui ne doit pas être doublement comptée
            _observation("", "2026", 300.0, TOUR_MEASURE="BEDPLACE", ACTIVITY="I552A"),
        ]
    },
}


@pytest.fixture
def api_simulee(monkeypatch):
    def faux_obtenir_json(url, parametres=None):
        parametres = parametres or {}
        if "geo.api.gouv.fr/communes/" in url:
            return {
                "nom": "Bourg-en-Bresse",
                "epci": {"nom": "CA du Bassin de Bourg-en-Bresse"},
            }
        for jeu, reponse in REPONSES_MELODI.items():
            if jeu in url:
                return reponse
        if "recherche-entreprises" in url:
            if parametres.get("q") == "office de tourisme":
                return {"total_results": 2}
            if parametres.get("section_activite_principale") == "G":
                return {"total_results": 2950}
            return {"total_results": 9800}
        raise AssertionError(f"URL inattendue : {url}")

    def faux_telecharger_texte(url):
        if "/2021/" in url:
            return _csv_dvf(1600.0)
        if "/2025/" in url:
            return _csv_dvf(2000.0)
        return None  # millésimes indisponibles (année en cours, etc.)

    monkeypatch.setattr(collecte, "_obtenir_json", faux_obtenir_json)
    monkeypatch.setattr(collecte, "_telecharger_texte", faux_telecharger_texte)
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
    assert commune.residences_secondaires_prec == pytest.approx(608.0)
    assert commune.emplois == pytest.approx(33552.5)   # total = max des ventilations
    assert commune.emplois_prec == pytest.approx(31914.9)
    assert commune.nb_etablissements == 9800
    assert commune.nb_commerces == 2950
    # Structure par âge : parts calculées sur le total du même jeu de données
    assert commune.part_65plus == pytest.approx(21.0, abs=0.1)
    assert commune.part_65plus_prec == pytest.approx(18.0, abs=0.1)
    assert commune.part_80plus == pytest.approx(7.0, abs=0.1)
    # Parc ancien : agrégat DW_MAIN uniquement, ventilations ignorées
    assert commune.part_logements_avant_1946 == pytest.approx(20.0, abs=0.1)
    # Tourisme : familles de niveau 1 seulement, office détecté
    assert commune.lits_touristiques == 1250
    assert commune.office_tourisme is True
    # DVF : millésime récent trouvé (2025) et comparaison ~4 ans avant (2021)
    assert commune.prix_m2 == pytest.approx(2000.0)
    assert commune.prix_m2_prec == pytest.approx(1600.0)
    assert commune.evolution_prix_m2_pct == pytest.approx(25.0)


def test_fusion_conserve_les_colonnes_manuelles():
    collectee = Commune(code_insee="01053", nom="Bourg-en-Bresse")
    ancienne = Commune(
        code_insee="01053",
        nom="Bourg-en-Bresse",
        taux_vacance_commerciale=12.0,
        logements_autorises_3ans=300,
    )
    fusionnees = fusionner_donnees_manuelles([collectee], [ancienne])
    resultat = fusionnees[0]
    assert resultat.taux_vacance_commerciale == pytest.approx(12.0)
    assert resultat.logements_autorises_3ans == 300
