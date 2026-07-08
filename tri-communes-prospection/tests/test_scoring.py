"""Tests du moteur d'analyse par besoin et du chargement CSV."""

from pathlib import Path

import pytest

from tri_communes import (
    Commune,
    DocumentUrbanisme,
    analyser_commune,
    analyser_communes,
    charger_communes,
    ecrire_communes,
    ecrire_resultats,
    grouper_par_besoin,
)
from tri_communes.besoins import axe_planification, priorite_depuis_score

ANNEE = 2026


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
        document_urbanisme=DocumentUrbanisme.PLU,
        annee_approbation=2010,
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


# --- Axes de besoin -----------------------------------------------------------


def test_pos_caduc_planification_maximale():
    pos = commune_type(document_urbanisme=DocumentUrbanisme.POS, annee_approbation=1999)
    assert axe_planification(pos, ANNEE) == 100.0


def test_document_inconnu_axe_non_evaluable():
    inconnu = commune_type(document_urbanisme=DocumentUrbanisme.INCONNU)
    assert axe_planification(inconnu, ANNEE) is None


def test_competence_epci_reduit_la_planification():
    seule = commune_type(competence_plu_epci=False)
    transferee = commune_type(competence_plu_epci=True)
    assert axe_planification(transferee, ANNEE) < axe_planification(seule, ANNEE)


def test_forte_vacance_orientee_habitat():
    commune = commune_type(
        logements=1000,
        logements_vacants=140,       # 14 % de vacance…
        logements_prec=980,
        logements_vacants_prec=90,   # …en forte hausse
        document_urbanisme=DocumentUrbanisme.PLU,
        annee_approbation=2022,
    )
    analyse = analyser_commune(commune, annee_reference=ANNEE)
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
        document_urbanisme=DocumentUrbanisme.PLU,
        annee_approbation=2022,
    )
    analyse = analyser_commune(commune, annee_reference=ANNEE)
    assert analyse.besoin_principal == "revitalisation"


def test_vacance_commerciale_alimente_axe_commerce():
    sans = commune_type()
    avec = commune_type(taux_vacance_commerciale=20.0)
    assert (
        analyser_commune(avec, ANNEE).axes["commerce"]
        > analyser_commune(sans, ANNEE).axes["commerce"]
    )


def test_commune_sans_donnees_score_nul():
    vide = Commune(code_insee="99998", nom="Sans-Données")
    analyse = analyser_commune(vide, annee_reference=ANNEE)
    assert analyse.score_global == 0.0
    assert analyse.besoin_principal == ""


def test_priorites():
    assert priorite_depuis_score(80) == "À démarcher en priorité"
    assert priorite_depuis_score(50) == "À suivre"
    assert priorite_depuis_score(20) == "Faible intérêt"


def test_tri_global_decroissant():
    communes = [
        commune_type(nom="Calme", annee_approbation=2025),
        commune_type(
            nom="Urgente",
            document_urbanisme=DocumentUrbanisme.POS,
            annee_approbation=1998,
        ),
    ]
    analyses = analyser_communes(communes, annee_reference=ANNEE)
    assert [a.commune.nom for a in analyses] == ["Urgente", "Calme"]


def test_groupement_par_besoin():
    analyses = analyser_communes(
        [
            commune_type(
                nom="Planif",
                document_urbanisme=DocumentUrbanisme.POS,
                annee_approbation=1998,
            ),
            commune_type(
                nom="Habitat",
                logements_vacants=150,
                logements_vacants_prec=80,
                document_urbanisme=DocumentUrbanisme.PLU,
                annee_approbation=2023,
            ),
        ],
        annee_reference=ANNEE,
    )
    groupes = grouper_par_besoin(analyses)
    assert [a.commune.nom for a in groupes["planification"]] == ["Planif"]
    assert [a.commune.nom for a in groupes["habitat"]] == ["Habitat"]


# --- Chargement / écriture ------------------------------------------------------


def test_chargement_exemple_et_export(tmp_path: Path):
    exemple = Path(__file__).parent.parent / "data" / "communes_exemple.csv"
    communes = charger_communes(exemple)
    assert len(communes) == 15
    assert communes[0].nom == "Beaumont-sur-Ozanne"
    assert communes[0].document_urbanisme is DocumentUrbanisme.POS
    assert communes[3].taux_vacance_commerciale == pytest.approx(14.0)

    analyses = analyser_communes(communes, annee_reference=ANNEE)
    sortie = tmp_path / "resultats.csv"
    ecrire_resultats(analyses, sortie)
    lignes = sortie.read_text(encoding="utf-8").strip().splitlines()
    assert len(lignes) == 16  # en-tête + 15 communes
    assert lignes[0].startswith("rang,code_insee,nom,epci,besoin_principal")


def test_aller_retour_ecriture_lecture(tmp_path: Path):
    commune = commune_type(taux_vacance_commerciale=12.5, competence_plu_epci=True)
    fichier = tmp_path / "communes.csv"
    ecrire_communes([commune], fichier)
    relues = charger_communes(fichier)
    assert len(relues) == 1
    relue = relues[0]
    assert relue.nom == commune.nom
    assert relue.population == commune.population
    assert relue.taux_vacance_commerciale == pytest.approx(12.5)
    assert relue.competence_plu_epci is True
    assert relue.document_urbanisme is DocumentUrbanisme.PLU


def test_colonne_manquante_signalee(tmp_path: Path):
    fichier = tmp_path / "invalide.csv"
    fichier.write_text("code_insee\n99001\n", encoding="utf-8")
    with pytest.raises(ValueError, match="colonnes manquantes"):
        charger_communes(fichier)
