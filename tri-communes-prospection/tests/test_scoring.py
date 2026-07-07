"""Tests du moteur de scoring et du chargement CSV."""

from pathlib import Path

import pytest

from tri_communes import (
    Commune,
    DocumentUrbanisme,
    calculer_score,
    charger_communes,
    ecrire_resultats,
    trier_communes,
)
from tri_communes.scoring import (
    POIDS_DEFAUT,
    note_document_urbanisme,
    note_proximite_agence,
    priorite_depuis_score,
)

ANNEE = 2026


def commune_type(**surcharges) -> Commune:
    base = dict(
        code_insee="99999",
        nom="Testville",
        population=1500,
        evolution_population_pct=3.0,
        logements_autorises_3ans=20,
        document_urbanisme=DocumentUrbanisme.PLU,
        annee_approbation=2010,
        competence_plu_epci=False,
        distance_agence_km=30.0,
    )
    base.update(surcharges)
    return Commune(**base)


def test_pos_caduc_plus_interessant_que_plu_recent():
    pos = commune_type(document_urbanisme=DocumentUrbanisme.POS, annee_approbation=1999)
    plu_recent = commune_type(annee_approbation=2024)
    assert (
        calculer_score(pos, annee_reference=ANNEE).score
        > calculer_score(plu_recent, annee_reference=ANNEE).score
    )


def test_competence_epci_reduit_l_interet():
    seule = commune_type(competence_plu_epci=False)
    transferee = commune_type(competence_plu_epci=True)
    assert (
        calculer_score(transferee, annee_reference=ANNEE).score
        < calculer_score(seule, annee_reference=ANNEE).score
    )


def test_plui_recent_note_faible():
    plui = commune_type(
        document_urbanisme=DocumentUrbanisme.PLUI,
        annee_approbation=2024,
        competence_plu_epci=True,
    )
    assert note_document_urbanisme(plui, ANNEE) == pytest.approx(0.05)


def test_notes_bornees_entre_0_et_1():
    extreme = commune_type(
        population=100000,
        evolution_population_pct=50.0,
        logements_autorises_3ans=99999,
        distance_agence_km=500.0,
    )
    resultat = calculer_score(extreme, annee_reference=ANNEE)
    assert all(0.0 <= note <= 1.0 for note in resultat.details.values())
    assert 0.0 <= resultat.score <= 100.0


def test_distance_inconnue_est_neutre():
    assert note_proximite_agence(commune_type(distance_agence_km=None)) == 0.5


def test_priorites():
    assert priorite_depuis_score(80) == "À démarcher en priorité"
    assert priorite_depuis_score(50) == "À suivre"
    assert priorite_depuis_score(20) == "Faible intérêt"


def test_poids_personnalises_renormalises():
    commune = commune_type()
    defaut = calculer_score(commune, annee_reference=ANNEE)
    doubles = {nom: 2 * p for nom, p in POIDS_DEFAUT.items()}
    double = calculer_score(commune, poids=doubles, annee_reference=ANNEE)
    assert double.score == defaut.score


def test_poids_inconnu_rejete():
    with pytest.raises(ValueError):
        calculer_score(commune_type(), poids={"critere_inexistant": 1.0})


def test_tri_decroissant():
    communes = [
        commune_type(nom="Molle", annee_approbation=2025, evolution_population_pct=-2),
        commune_type(
            nom="Dynamique",
            document_urbanisme=DocumentUrbanisme.POS,
            annee_approbation=1998,
            evolution_population_pct=8,
        ),
    ]
    scores = trier_communes(communes, annee_reference=ANNEE)
    assert [s.commune.nom for s in scores] == ["Dynamique", "Molle"]
    assert scores[0].score >= scores[1].score


def test_chargement_exemple_et_export(tmp_path: Path):
    exemple = Path(__file__).parent.parent / "data" / "communes_exemple.csv"
    communes = charger_communes(exemple)
    assert len(communes) == 14
    assert communes[0].nom == "Beaumont-sur-Ozanne"
    assert communes[0].document_urbanisme is DocumentUrbanisme.POS

    scores = trier_communes(communes, annee_reference=ANNEE)
    sortie = tmp_path / "resultats.csv"
    ecrire_resultats(scores, sortie)
    lignes = sortie.read_text(encoding="utf-8").strip().splitlines()
    assert len(lignes) == 15  # en-tête + 14 communes
    assert lignes[0].startswith("rang,code_insee,nom")


def test_colonne_manquante_signalee(tmp_path: Path):
    fichier = tmp_path / "invalide.csv"
    fichier.write_text("code_insee,nom\n99001,Trouville\n", encoding="utf-8")
    with pytest.raises(ValueError, match="colonnes manquantes"):
        charger_communes(fichier)
