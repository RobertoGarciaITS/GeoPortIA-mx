from pathlib import Path

from app.inegi.vacancies import count_demand, load_vacancies_csv


def test_vacancy_fixture_counts_skill_and_geography():
    path = Path(__file__).resolve().parents[3] / "data" / "sample" / "sne_vacancies_saltillo.csv"
    rows = load_vacancies_csv(path)
    assert count_demand(rows, "Saltillo", "AWS") == 8
    assert count_demand(rows, "Ramos Arizpe", "AWS") == 0
