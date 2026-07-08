"""Tests du moteur d'analyse par besoin et du chargement CSV."""

from pathlib import Path

import pytest

from tri_communes import (
    Commune,
    analyser_commune,
    analyser_communes,
    charger_communes,
    ecrire_communes,
    ecrire_resultats,
    grouper_par_besoin,
)
from tri_communes.besoins import priorite_depuis_score


def commune_type(**surcharges) -> Commune:
    base = dict(
        code_insee="99999",
        nom="Testville",
        population=1500,
        population_prec=1450,
        population_anc=1400,
        annee_recensement=2023,
        logements=700,
        logements_vacants=45,
        residences_secondaires=20,
        logements_prec=670,
        logements_vacants_prec=40,
        emplois=300.0,
        emplois_prec=290.0,
        nb_etablissements=150,
        nb_commerces=15,
        logements_autorises_3ans=20,
    )
    base.update(surcharges)
    return Commune(**base)


# --- Indicateurs dérivés ------------------------------------------------------


def test_indicateurs_derives():
    commune = commune_type()
    assert commune.evolution_population_pct == pytest.approx(3.448, abs=0.01)
    assert commune.taux_vacance_logement == pytest.approx(6.43, abs=0.01)
    assert commune.evolution_vacance_points == pytest.approx(0.46, abs=0.01)
    assert commune.commerces_pour_1000_hab == pytest.approx(10.0)


def test_indicateurs_absents_donnent_none():
    vide = Commune(code_insee="99998", nom="Sans-Données")
    assert vide.evolution_population_pct is None
    assert vide.taux_vacance_logement is None
    assert vide.evolution_emplois_pct is None


def test_evolution_emplois_ignoree_sur_petits_effectifs():
    petite = commune_type(emplois=12.0, emplois_prec=15.0)
    assert petite.evolution_emplois_pct is None


# --- Axes de besoin -----------------------------------------------------------


def test_forte_vacance_orientee_habitat():
    commune = commune_type(
        logements=1000,
        logements_vacants=140,       # 14 % de vacance…
        logements_prec=980,
        logements_vacants_prec=90,   # …en forte hausse
    )
    analyse = analyser_commune(commune)
    assert analyse.besoin_principal == "habitat"
    assert analyse.axes["habitat"] > 70


def test_declin_orient_revitalisation():
    commune = commune_type(
        population=1200,
        population_prec=1310,
        population_anc=1450,
        emplois=200.0,
        emplois_prec=260.0,
        logements_vacants=50,
    )
    analyse = analyser_commune(commune)
    assert analyse.besoin_principal == "revitalisation"


def test_croissance_orientee_developpement():
    commune = commune_type(
        population=1700,
        population_prec=1520,        # +11,8 %
        logements_vacants=15,        # marché tendu (2,1 %)
        logements_vacants_prec=16,
        logements_autorises_3ans=40,
    )
    analyse = analyser_commune(commune)
    assert analyse.besoin_principal == "croissance"
    assert analyse.axes["croissance"] > 80


def test_vacance_commerciale_alimente_axe_commerce():
    sans = commune_type()
    avec = commune_type(taux_vacance_commerciale=20.0)
    assert (
        analyser_commune(avec).axes["commerce"]
        > analyser_commune(sans).axes["commerce"]
    )


def test_densite_commerciale_ignoree_sous_1000_habitants():
    village = commune_type(population=300, population_prec=300, nb_commerces=0)
    analyse = analyser_commune(village)
    # Sans vacance commerciale relevée ni signal emploi net, l'axe commerce
    # ne doit pas saturer pour un village sans commerce.
    assert analyse.axes["commerce"] < 50


def test_commune_sans_donnees_score_nul():
    vide = Commune(code_insee="99998", nom="Sans-Données")
    analyse = analyser_commune(vide)
    assert analyse.score_global == 0.0
    assert analyse.besoin_principal == ""


def test_priorites():
    assert priorite_depuis_score(80) == "À démarcher en priorité"
    assert priorite_depuis_score(50) == "À suivre"
    assert priorite_depuis_score(20) == "Faible intérêt"


def test_tri_global_decroissant():
    communes = [
        commune_type(nom="Stable"),
        commune_type(
            nom="Sinistrée",
            logements_vacants=120,
            logements_vacants_prec=70,
            taux_vacance_commerciale=20.0,
        ),
    ]
    analyses = analyser_communes(communes)
    assert [a.commune.nom for a in analyses] == ["Sinistrée", "Stable"]


def test_groupement_par_besoin():
    analyses = analyser_communes(
        [
            commune_type(
                nom="Habitat",
                logements_vacants=150,
                logements_vacants_prec=80,
            ),
            commune_type(
                nom="Croissance",
                population=1700,
                population_prec=1520,
                logements_vacants=15,
                logements_vacants_prec=16,
                logements_autorises_3ans=40,
            ),
        ]
    )
    groupes = grouper_par_besoin(analyses)
    assert [a.commune.nom for a in groupes["habitat"]] == ["Habitat"]
    assert [a.commune.nom for a in groupes["croissance"]] == ["Croissance"]


# --- Chargement / écriture ------------------------------------------------------


def test_chargement_exemple_et_export(tmp_path: Path):
    exemple = Path(__file__).parent.parent / "data" / "communes_exemple.csv"
    communes = charger_communes(exemple)
    assert len(communes) == 15
    assert communes[0].nom == "Beaumont-sur-Ozanne"
    assert communes[3].taux_vacance_commerciale == pytest.approx(14.0)

    analyses = analyser_communes(communes)
    sortie = tmp_path / "resultats.csv"
    ecrire_resultats(analyses, sortie)
    lignes = sortie.read_text(encoding="utf-8").strip().splitlines()
    assert len(lignes) == 16  # en-tête + 15 communes
    assert lignes[0].startswith("rang,code_insee,nom,epci,besoin_principal")


def test_aller_retour_ecriture_lecture(tmp_path: Path):
    commune = commune_type(taux_vacance_commerciale=12.5)
    fichier = tmp_path / "communes.csv"
    ecrire_communes([commune], fichier)
    relues = charger_communes(fichier)
    assert len(relues) == 1
    relue = relues[0]
    assert relue.nom == commune.nom
    assert relue.population == commune.population
    assert relue.taux_vacance_commerciale == pytest.approx(12.5)
    assert relue.logements_autorises_3ans == 20


def test_colonne_manquante_signalee(tmp_path: Path):
    fichier = tmp_path / "invalide.csv"
    fichier.write_text("code_insee\n99001\n", encoding="utf-8")
    with pytest.raises(ValueError, match="colonnes manquantes"):
        charger_communes(fichier)
