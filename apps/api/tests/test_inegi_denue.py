import httpx
import pytest

from app.inegi.config import InegiSettings
from app.inegi.denue import DenueClient, DenueError


ROW = {"Id": "123", "Nombre": "Empresa Demo", "Clase_actividad": "Servicios de TI", "Estrato": "11 a 30 personas", "Latitud": "25.43", "Longitud": "-100.97", "Ubicacion": "Saltillo"}


def client_for(handler):
    transport = httpx.MockTransport(handler)
    return DenueClient(InegiSettings(denue_token="test-token"), httpx.Client(transport=transport))


def test_search_entity_builds_official_path_without_exposing_token_in_logic():
    seen = {}

    def handler(request):
        seen["url"] = str(request.url)
        return httpx.Response(200, json=[ROW])

    records = client_for(handler).search_entity("tecnologia", "05", 1, 10)
    assert records[0].establishment_id == "123"
    assert "/BuscarEntidad/tecnologia/05/1/10/test-token" in seen["url"]


def test_missing_token_is_safe_and_explicit():
    with pytest.raises(DenueError, match="INEGI_DENUE_TOKEN"):
        DenueClient(InegiSettings()).search_entity("tecnologia", "05")


def test_rate_limit_is_translated():
    client = client_for(lambda request: httpx.Response(429))
    with pytest.raises(DenueError, match="límite"):
        client.search_entity("tecnologia", "05")


def test_denue_real_style_unauthorized_text_is_translated():
    client = client_for(lambda request: httpx.Response(200, text="No autorizado. Utilice una clave válida."))
    with pytest.raises(DenueError, match="rechazó el token"):
        client.search_entity("tecnologia", "05")


def test_invalid_payload_is_rejected():
    client = client_for(lambda request: httpx.Response(200, json={"error": "bad"}))
    with pytest.raises(DenueError, match="formato"):
        client.search_entity("tecnologia", "05")


def test_quantify_normalizes_activity_geography_and_total():
    client = client_for(lambda request: httpx.Response(200, json=[{"AE": "541", "AG": "05030", "Total": "12"}]))
    assert client.quantify(["541"], ["05030"]) == [{"activity_code": "541", "geography_code": "05030", "total": "12"}]


def test_search_radius_enforces_official_maximum():
    with pytest.raises(ValueError):
        client_for(lambda request: httpx.Response(200, json=[])).search_radius("tecnologia", 25, -100, 5001)


def test_iter_entity_reads_pages_until_short_page():
    def handler(request):
        page_start = request.url.path.split("/")[-3]
        if page_start == "1":
            return httpx.Response(200, json=[ROW, {**ROW, "Id": "124"}])
        return httpx.Response(200, json=[{**ROW, "Id": "125"}])

    records = list(client_for(handler).iter_entity("tecnologia", "05", page_size=2))
    assert [record.establishment_id for record in records] == ["123", "124", "125"]


def test_search_area_activity_builds_municipality_and_stratum_path():
    seen = {}

    def handler(request):
        seen["path"] = request.url.path
        return httpx.Response(200, json=[ROW])

    result = client_for(handler).search_area_activity(entity="05", municipality="030", condition="computacion", stratum="3")
    assert result[0].name == "Empresa Demo"
    assert "/BuscarAreaAct/05/030/0/0/0/0/0/0/0/computacion/1/10/3/test-token" in seen["path"]
