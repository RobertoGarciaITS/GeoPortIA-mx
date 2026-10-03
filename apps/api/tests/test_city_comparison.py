import importlib.util
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[3] / "scripts" / "compare_city_labor_examples.py"
SPEC = importlib.util.spec_from_file_location("compare_city_labor_examples", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def test_city_scenarios_produce_expected_order_of_scarcity():
    snapshots = []
    for city, values in MODULE.SCENARIOS.items():
        enoe, denue = MODULE._records(city, values)
        snapshots.append(MODULE.build_snapshot(
            geography=city,
            skill="AWS",
            enoe_records=enoe,
            denue_records=denue,
            demand=values["demand"],
            demand_source="scenario_fixture",
        ))
    by_city = {row.geography: row for row in snapshots}
    assert by_city["Saltillo"].scarcity_index == 8 / 3
    assert by_city["Monterrey"].scarcity_index == 1.8
    assert by_city["Guadalajara"].scarcity_index == 0.8
    assert by_city["Monterrey"].deficit > by_city["Saltillo"].deficit > by_city["Guadalajara"].deficit
    assert by_city["Saltillo"].scarcity_index > by_city["Monterrey"].scarcity_index > by_city["Guadalajara"].scarcity_index
