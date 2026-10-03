from app.inegi.denue import DenueRecord
from app.inegi.enoe import EnoeRecord
from app.inegi.labor import build_snapshot


def test_snapshot_keeps_demand_source_and_calculates_gap():
    enoe = [
        EnoeRecord("Saltillo", "Computación", "DevOps", "busca_cambio", 2, "AWS"),
        EnoeRecord("Saltillo", "Computación", "Programador", "ocupado", 3, "AWS"),
    ]
    denue = [
        DenueRecord("1", "Nube", "TI", "11 a 30", 25, -100, "Saltillo", {}),
        DenueRecord("2", "Fuera", "TI", "11 a 30", 25, -100, "Ramos Arizpe", {}),
    ]
    result = build_snapshot(
        geography="Saltillo",
        skill="AWS",
        enoe_records=enoe,
        denue_records=denue,
        demand=8,
        demand_source="fixture_vacancies",
    )
    assert result.technology_establishments == 1
    assert result.available_talent == 2
    assert result.employed_talent == 3
    assert result.deficit == 6
    assert result.scarcity_index == 4
    assert result.demand_source == "fixture_vacancies"
