"""Genera mapa, tabla y gráficos comparativos del indicador laboral."""
from __future__ import annotations

import csv
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts" / "labor_comparison"
OGR2OGR = Path(r"C:\Program Files\QGIS 4.2.3\bin\ogr2ogr.exe")
INDICATOR_SOURCE = ROOT / "data" / "sample" / "labor_indicators_v1.json"

CITY_DEFS = [
    ("Saltillo", "05030", ROOT / "794551163061_s/estados_extraidos/05_coahuiladezaragoza/conjunto_de_datos/05mun.shp", "030"),
    ("Monterrey", "19039", ROOT / "794551163061_s/estados_extraidos/19_nuevoleon/conjunto_de_datos/19mun.shp", "039"),
    ("Guadalajara", "14039", ROOT / "794551163061_s/estados_extraidos/14_jalisco/conjunto_de_datos/14mun.shp", "039"),
]


def load_indicator_rows() -> list[dict]:
    payload = json.loads(INDICATOR_SOURCE.read_text(encoding="utf-8"))
    if payload.get("schema_version") != "1.0" or not isinstance(payload.get("rows"), list):
        raise ValueError("Contrato de indicadores laborales no válido")
    required = {"country", "state", "city", "skill", "available_talent", "demand", "deficit", "scarcity_index", "expected_result", "synthetic"}
    for row in payload["rows"]:
        if not required <= row.keys():
            raise ValueError("Fila de indicadores sin campos requeridos")
    return payload["rows"]


INDICATOR_ROWS = load_indicator_rows()
INDICATORS = {row["city"]: {key: row[key] for key in ("available_talent", "demand", "deficit", "scarcity_index", "expected_result")} for row in INDICATOR_ROWS}


def make_geojson() -> dict:
    OUT.mkdir(parents=True, exist_ok=True)
    geojson_path = OUT / "city_boundaries.geojson"
    if geojson_path.exists():
        geojson_path.unlink()
    for index, (_, cvegeo, source, cve_mun) in enumerate(CITY_DEFS):
        command = [str(OGR2OGR), "-f", "GeoJSON"]
        if index:
            command += ["-update", "-append"]
        command += [str(geojson_path), str(source), "-where", f"CVE_MUN = '{cve_mun}'", "-t_srs", "EPSG:4326", "-nln", "cities"]
        subprocess.run(command, check=True, capture_output=True, text=True)
    payload = json.loads(geojson_path.read_text(encoding="utf-8"))
    by_cvegeo = {cvegeo: city for city, cvegeo, _, _ in CITY_DEFS}
    for feature in payload["features"]:
        cvegeo = feature["properties"].get("CVEGEO")
        city = by_cvegeo[cvegeo]
        feature["properties"].update({"city": city, **INDICATORS[city]})
    geojson_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    return payload


def write_outputs(geojson: dict) -> None:
    rows = []
    for city, values in INDICATORS.items():
        rows.append({"city": city, "skill": "AWS", **values, "synthetic": True})
    (OUT / "city_labor_indicators.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    with (OUT / "city_labor_indicators.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    data_json = json.dumps({"geojson": geojson, "rows": rows}, ensure_ascii=False).replace("</", "<\\/")
    html = HTML_TEMPLATE.replace("__DATA__", data_json)
    (OUT / "city_labor_dashboard.html").write_text(html, encoding="utf-8")


HTML_TEMPLATE = r'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>GeoPortIA — comparación laboral AWS</title>
<script src="https://cdn.jsdelivr.net/npm/d3@7.9.0/dist/d3.min.js"></script>
<style>
:root{color-scheme:light;--ink:#17212b;--muted:#607080;--line:#d9e1e8;--surface:#f7f9fb;--high:#c94c4c;--mid:#d28a3b;--low:#4a9471}
body{font-family:system-ui,-apple-system,"Segoe UI",sans-serif;color:var(--ink);margin:0;padding:24px;max-width:1180px;margin-inline:auto}h1{margin:0 0 4px;font-size:26px}h2{font-size:18px;margin:26px 0 8px}.note{color:var(--muted);font-size:13px;margin-bottom:18px}.layout{display:grid;grid-template-columns:minmax(320px,1.15fr) minmax(300px,.85fr);gap:22px}svg{width:100%;height:auto;display:block}.map{background:var(--surface);border:1px solid var(--line)}.boundary{stroke:#52606d;stroke-width:1.1;vector-effect:non-scaling-stroke}.boundary:hover{stroke:#111;stroke-width:2}.label{font-size:12px;fill:var(--ink);paint-order:stroke;stroke:#fff;stroke-width:3px;stroke-linejoin:round}.legend{display:flex;gap:16px;flex-wrap:wrap;color:var(--muted);font-size:12px;margin-top:8px}.swatch{display:inline-block;width:11px;height:11px;margin-right:4px;vertical-align:-1px}.table-wrap{overflow-x:auto}.table{border-collapse:collapse;width:100%;font-size:14px}.table th,.table td{padding:9px 8px;border-bottom:1px solid var(--line);text-align:right}.table th:first-child,.table td:first-child{text-align:left}.chart-title{font-size:14px;font-weight:600;margin:18px 0 4px}.bar-label{font-size:12px;fill:var(--ink)}.bar-value{font-size:12px;fill:var(--ink);font-variant-numeric:tabular-nums}.axis{font-size:11px;fill:var(--muted)}.gridline{stroke:var(--line);stroke-width:1}.high{fill:var(--high)}.mid{fill:var(--mid)}.low{fill:var(--low)}@media(max-width:760px){body{padding:16px}.layout{grid-template-columns:1fr}h1{font-size:22px}}
</style>
</head>
<body>
<h1>Comparación territorial de talento AWS</h1>
<div class="note">Escenario sintético de validación del modelo GeoPortIA · no representa estadísticas oficiales.</div>
<div class="layout"><section><h2>Mapa municipal</h2><svg id="map" class="map" viewBox="0 0 760 430" role="img" aria-label="Municipios de Saltillo, Monterrey y Guadalajara coloreados por índice de escasez"></svg><div class="legend"><span><i class="swatch high"></i>Escasez alta</span><span><i class="swatch mid"></i>Escasez moderada</span><span><i class="swatch low"></i>Equilibrio o superávit</span></div></section><section><h2>Indicadores</h2><div class="table-wrap"><table class="table"><thead><tr><th>Ciudad</th><th>Oferta</th><th>Demanda</th><th>Déficit</th><th>Índice</th></tr></thead><tbody id="table-body"></tbody></table></div><div class="chart-title">Oferta disponible frente a demanda</div><svg id="bars" viewBox="0 0 520 250" role="img" aria-label="Gráfico de oferta disponible y demanda por ciudad"></svg><div class="chart-title">Índice de escasez</div><svg id="index-chart" viewBox="0 0 520 210" role="img" aria-label="Gráfico del índice de escasez por ciudad"></svg></section></div>
<script>
const DATA=__DATA__;
const rows=DATA.rows;
const palette={"Escasez alta":"#c94c4c","Escasez moderada":"#d28a3b","Equilibrio o superávit":"#4a9471"};
const rowByCity=Object.fromEntries(rows.map(row=>[row.city,row]));
document.getElementById('table-body').innerHTML=rows.map(row=>`<tr><td>${row.city}</td><td>${row.available_talent}</td><td>${row.demand}</td><td>${row.deficit}</td><td>${row.scarcity_index.toFixed(2)}</td></tr>`).join('');
const features=DATA.geojson.features; const coords=[];
function collect(value){if(typeof value[0]==='number'){coords.push(value);return;} value.forEach(collect)} features.forEach(f=>collect(f.geometry.coordinates));
const lonExtent=d3.extent(coords,d=>d[0]), latExtent=d3.extent(coords,d=>d[1]); const projection=d3.geoMercator().fitExtent([[25,25],[735,405]],DATA.geojson); const path=d3.geoPath(projection);
const map=d3.select('#map'); map.selectAll('path').data(features).join('path').attr('class','boundary').attr('d',path).attr('fill',d=>palette[rowByCity[d.properties.city].expected_result]).append('title').text(d=>`${d.properties.city}: índice ${rowByCity[d.properties.city].scarcity_index.toFixed(2)}`);
map.selectAll('text').data(features).join('text').attr('class','label').attr('x',d=>path.centroid(d)[0]).attr('y',d=>path.centroid(d)[1]).attr('text-anchor','middle').text(d=>d.properties.city);
function bars(){const svg=d3.select('#bars'), width=520,height=250,left=120,right=18,top=22,bottom=28; const max=d3.max(rows,d=>Math.max(d.available_talent,d.demand)); const x=d3.scaleLinear([0,max],[left,width-right]); const y=d3.scaleBand(rows.map(d=>d.city),[top,height-bottom]).padding(.26); svg.selectAll('.gridline').data([0,max/2,max]).join('line').attr('class','gridline').attr('x1',x).attr('x2',x).attr('y1',top-4).attr('y2',height-bottom+2); svg.selectAll('.bar-label').data(rows).join('text').attr('class','bar-label').attr('x',left-8).attr('y',d=>y(d.city)+y.bandwidth()/2+4).attr('text-anchor','end').text(d=>d.city); const series=[['available_talent','Oferta','#4a9471'],['demand','Demanda','#c94c4c']]; series.forEach(([key,label,color],i)=>svg.selectAll(`.bar-${key}`).data(rows).join('rect').attr('class',`bar-${key}`).attr('x',left).attr('y',d=>y(d.city)+i*y.bandwidth()/2).attr('width',d=>x(d[key])-left).attr('height',y.bandwidth()/2-2).attr('fill',color).append('title').text(d=>`${d.city} — ${label}: ${d[key]}`)); svg.selectAll('.axis').data([0,max/2,max]).join('text').attr('class','axis').attr('x',d=>x(d)).attr('y',height-6).attr('text-anchor','middle').text(d=>d);}
function indexChart(){const svg=d3.select('#index-chart'),width=520,height=210,left=120,right=30,top=18,bottom=28; const max=Math.max(3,d3.max(rows,d=>d.scarcity_index)); const x=d3.scaleLinear([0,max],[left,width-right]); const y=d3.scaleBand(rows.map(d=>d.city),[top,height-bottom]).padding(.3); svg.selectAll('.gridline').data([0,1,2,3]).join('line').attr('class','gridline').attr('x1',d=>x(d)).attr('x2',d=>x(d)).attr('y1',top-3).attr('y2',height-bottom); svg.selectAll('.bar-label').data(rows).join('text').attr('class','bar-label').attr('x',left-8).attr('y',d=>y(d.city)+y.bandwidth()/2+4).attr('text-anchor','end').text(d=>d.city); svg.selectAll('.index-bar').data(rows).join('rect').attr('class','index-bar').attr('x',left).attr('y',d=>y(d.city)).attr('width',d=>x(d.scarcity_index)-left).attr('height',y.bandwidth()).attr('fill',d=>palette[d.expected_result]).append('title').text(d=>`${d.city} — índice: ${d.scarcity_index.toFixed(2)}`); svg.selectAll('.bar-value').data(rows).join('text').attr('class','bar-value').attr('x',d=>x(d.scarcity_index)+6).attr('y',d=>y(d.city)+y.bandwidth()/2+4).text(d=>d.scarcity_index.toFixed(2)); svg.selectAll('.axis').data([0,1,2,3]).join('text').attr('class','axis').attr('x',d=>x(d)).attr('y',height-6).attr('text-anchor','middle').text(d=>d);}
bars(); indexChart();
</script>
</body>
</html>'''


def main() -> None:
    write_outputs(make_geojson())
    print(f"PASS: visualizaciones creadas en {OUT}")


if __name__ == "__main__":
    main()
