from pathlib import Path

from app.inegi.enoe import EnoeRecord, load_enoe_csv, validate_enoe_columns, weighted_summary


def test_weighted_summary_separates_available_talent_from_employed():
    rows = [
        EnoeRecord("Saltillo", "Computación", "DevOps", "busca_cambio", 2, "AWS"),
        EnoeRecord("Saltillo", "Computación", "Programador", "ocupado", 3, "AWS"),
        EnoeRecord("Saltillo", "Derecho", "Abogado", "desempleado", 1, ""),
    ]
    result = weighted_summary(rows, "Saltillo", "AWS")
    assert result == {"available_talent": 2, "employed": 3, "records_used": 2.0}


def test_load_enoe_fixture_preserves_expansion_factor():
    path = Path(__file__).resolve().parents[3] / "data" / "sample" / "enoe_extract_saltillo.csv"
    rows = load_enoe_csv(path)
    assert len(rows) == 3
    assert rows[0].skill == "AWS"
    assert rows[0].expansion_factor == 2


def test_enoe_schema_reports_missing_columns():
    try:
        validate_enoe_columns(["geography"])
    except ValueError as exc:
        assert "employment_status" in str(exc)
    else:
        raise AssertionError("Se esperaba rechazo del esquema ENOE")
