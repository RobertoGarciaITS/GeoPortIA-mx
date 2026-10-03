"""Genera el dashboard filtrable a partir de los mismos datos del comparativo."""
from __future__ import annotations

import json
import sys
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from generate_city_labor_visuals import INDICATOR_ROWS, OUT, make_geojson  # noqa: E402


TEMPLATE = r'''<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>GeoPortIA — tablero laboral filtrable</title>
<script src="https://cdn.jsdelivr.net/npm/d3@7.9.0/dist/d3.min.js"></script>
<style>
:root{color-scheme:light;--ink:#17212b;--muted:#607080;--line:#d9e1e8;--surface:#f7f9fb;--high:#c94c4c;--mid:#d28a3b;--low:#4a9471}
body{font-family:system-ui,-apple-system,"Segoe UI",sans-serif;color:var(--ink);margin:0;padding:24px;max-width:1180px;margin-inline:auto}h1{margin:0 0 4px;font-size:26px}h2{font-size:18px;margin:24px 0 8px}.note{color:var(--muted);font-size:13px;margin-bottom:16px}.controls{display:flex;gap:14px;flex-wrap:wrap;margin:16px 0}.control{display:flex;align-items:center;gap:7px;color:var(--muted);font-size:13px}.control select{font:inherit;color:var(--ink);background:var(--surface);border:1px solid var(--line);padding:7px 9px}.layout{display:grid;grid-template-columns:minmax(320px,1.15fr) minmax(300px,.85fr);gap:22px}svg{width:100%;height:auto;display:block}.map{background:var(--surface);border:1px solid var(--line)}.boundary{stroke:#52606d;stroke-width:1.1;vector-effect:non-scaling-stroke}.boundary:hover{stroke:#111;stroke-width:2}.label{font-size:12px;fill:var(--ink);paint-order:stroke;stroke:#fff;stroke-width:3px;stroke-linejoin:round}.legend{display:flex;gap:16px;flex-wrap:wrap;color:var(--muted);font-size:12px;margin-top:8px}.swatch{display:inline-block;width:11px;height:11px;margin-right:4px;vertical-align:-1px}.table-wrap{overflow-x:auto}.table{border-collapse:collapse;width:100%;font-size:14px}.table th,.table td{padding:9px 8px;border-bottom:1px solid var(--line);text-align:right}.table th:first-child,.table td:first-child{text-align:left}.chart-title{font-size:14px;font-weight:600;margin:18px 0 4px}.bar-label,.bar-value{font-size:12px;fill:var(--ink)}.axis{font-size:11px;fill:var(--muted)}.gridline{stroke:var(--line);stroke-width:1}.high{fill:var(--high)}.mid{fill:var(--mid)}.low{fill:var(--low)}@media(max-width:760px){body{padding:16px}.layout{grid-template-columns:1fr}h1{font-size:22px}}
</style></head><body>
<h1>Comparación territorial de talento AWS</h1>
<div class="note">Escenario sintético de validación del modelo GeoPortIA · no representa estadísticas oficiales.</div>
<div class="controls" aria-label="Filtros del tablero">
  <label class="control" for="country-filter">País<select id="country-filter"></select></label>
  <label class="control" for="city-filter">Ciudad<select id="city-filter"></select></label>
  <label class="control" for="skill-filter">Habilidad<select id="skill-filter"></select></label>
  <label class="control" for="metric-filter">Métrica<select id="metric-filter"><option value="scarcity_index">Índice de escasez</option><option value="deficit">Déficit absoluto</option><option value="demand">Demanda</option><option value="available_talent">Oferta disponible</option></select></label>
</div>
<div class="layout"><section><h2>Mapa municipal</h2><svg id="map" class="map" viewBox="0 0 760 430" role="img" aria-label="Municipios filtrados por índice de escasez"></svg><div class="legend"><span><i class="swatch high"></i>Escasez alta</span><span><i class="swatch mid"></i>Escasez moderada</span><span><i class="swatch low"></i>Equilibrio o superávit</span></div></section>
<section><h2>Indicadores</h2><div class="table-wrap"><table class="table"><thead><tr><th>Estado</th><th>Ciudad</th><th>Oferta</th><th>Demanda</th><th>Déficit</th><th>Índice</th></tr></thead><tbody id="table-body"></tbody></table></div><div class="chart-title">Oferta disponible frente a demanda</div><svg id="bars" viewBox="0 0 520 250" role="img" aria-label="Oferta y demanda filtradas"></svg><div class="chart-title" id="metric-title">Índice de escasez</div><svg id="metric-chart" viewBox="0 0 520 210" role="img" aria-label="Métrica seleccionada filtrada"></svg></section></div>
<script>
const DATA=__DATA__; const rows=DATA.rows; const palette={"Escasez alta":"#c94c4c","Escasez moderada":"#d28a3b","Equilibrio o superávit":"#4a9471"};
const countryFilter=document.getElementById('country-filter'), cityFilter=document.getElementById('city-filter'), skillFilter=document.getElementById('skill-filter'), metricFilter=document.getElementById('metric-filter');
const countries=['México','Canadá','Estados Unidos'], cities=[...new Set(rows.map(d=>d.city))], skills=[...new Set(rows.map(d=>d.skill))]; countryFilter.innerHTML=countries.map(d=>`<option value="${d}">${d}</option>`).join(''); cityFilter.innerHTML='<option value="all">Todas las ciudades</option>'+cities.map(d=>`<option value="${d}">${d}</option>`).join(''); skillFilter.innerHTML=skills.map(d=>`<option value="${d}">${d}</option>`).join('');
const features=DATA.geojson.features, rowByCity=Object.fromEntries(rows.map(d=>[d.city,d])), coords=[]; function collect(v){if(typeof v[0]==='number'){coords.push(v);return}v.forEach(collect)} features.forEach(f=>collect(f.geometry.coordinates));
const projection=d3.geoMercator().fitExtent([[25,25],[735,405]],DATA.geojson), path=d3.geoPath(projection), map=d3.select('#map'); map.selectAll('path').data(features).join('path').attr('class','boundary').attr('d',path).attr('fill',d=>palette[rowByCity[d.properties.city].expected_result]).append('title').text(d=>`${d.properties.city}: índice ${rowByCity[d.properties.city].scarcity_index.toFixed(2)}`); map.selectAll('text').data(features).join('text').attr('class','label').attr('x',d=>path.centroid(d)[0]).attr('y',d=>path.centroid(d)[1]).attr('text-anchor','middle').text(d=>d.properties.city);
function selected(){return rows.filter(d=>d.country===countryFilter.value&&(cityFilter.value==='all'||d.city===cityFilter.value)&&d.skill===skillFilter.value)}
function renderTable(view){document.getElementById('table-body').innerHTML=view.length?view.map(d=>`<tr><td>${d.state}</td><td>${d.city}</td><td>${d.available_talent}</td><td>${d.demand}</td><td>${d.deficit}</td><td>${d.scarcity_index.toFixed(2)}</td></tr>`).join(''):'<tr><td colspan="6">Sin datos para los filtros seleccionados</td></tr>'}
function renderBars(view){const svg=d3.select('#bars'),w=520,h=250,l=120,r=18,t=22,b=28,max=Math.max(1,d3.max(view,d=>Math.max(d.available_talent,d.demand))||1),x=d3.scaleLinear([0,max],[l,w-r]),y=d3.scaleBand(view.map(d=>d.city),[t,h-b]).padding(.26);svg.selectAll('*').remove();svg.selectAll('.gridline').data([0,max/2,max]).join('line').attr('class','gridline').attr('x1',x).attr('x2',x).attr('y1',t-4).attr('y2',h-b);svg.selectAll('.bar-label').data(view).join('text').attr('class','bar-label').attr('x',l-8).attr('y',d=>y(d.city)+y.bandwidth()/2+4).attr('text-anchor','end').text(d=>d.city);[['available_talent','Oferta','#4a9471'],['demand','Demanda','#c94c4c']].forEach(([key,label,color],i)=>svg.selectAll(`.bar-${key}`).data(view).join('rect').attr('x',l).attr('y',d=>y(d.city)+i*y.bandwidth()/2).attr('width',d=>x(d[key])-l).attr('height',y.bandwidth()/2-2).attr('fill',color).append('title').text(d=>`${d.city} — ${label}: ${d[key]}`));svg.selectAll('.axis').data([0,max/2,max]).join('text').attr('class','axis').attr('x',d=>x(d)).attr('y',h-6).attr('text-anchor','middle').text(d=>d)}
function renderMetric(view){const metric=metricFilter.value,labels={scarcity_index:'Índice de escasez',deficit:'Déficit absoluto',demand:'Demanda',available_talent:'Oferta disponible'};document.getElementById('metric-title').textContent=labels[metric];const svg=d3.select('#metric-chart'),w=520,h=210,l=120,r=30,t=18,b=28,values=view.map(d=>d[metric]),max=Math.max(1,d3.max(values)||1),min=Math.min(0,d3.min(values)||0),x=d3.scaleLinear([min,max],[l,w-r]),y=d3.scaleBand(view.map(d=>d.city),[t,h-b]).padding(.3);svg.selectAll('*').remove();svg.selectAll('.gridline').data([0,max/2,max]).join('line').attr('class','gridline').attr('x1',d=>x(d)).attr('x2',d=>x(d)).attr('y1',t-3).attr('y2',h-b);svg.selectAll('.bar-label').data(view).join('text').attr('class','bar-label').attr('x',l-8).attr('y',d=>y(d.city)+y.bandwidth()/2+4).attr('text-anchor','end').text(d=>d.city);svg.selectAll('.metric-bar').data(view).join('rect').attr('x',d=>x(Math.min(0,d[metric]))).attr('y',d=>y(d.city)).attr('width',d=>Math.abs(x(d[metric])-x(0))).attr('height',y.bandwidth()).attr('fill',d=>palette[d.expected_result]).append('title').text(d=>`${d.city} — ${labels[metric]}: ${d[metric].toFixed(2)}`);svg.selectAll('.bar-value').data(view).join('text').attr('class','bar-value').attr('x',d=>x(d[metric])+6).attr('y',d=>y(d.city)+y.bandwidth()/2+4).text(d=>d[metric].toFixed(2));svg.selectAll('.axis').data([0,max/2,max]).join('text').attr('class','axis').attr('x',d=>x(d)).attr('y',h-6).attr('text-anchor','middle').text(d=>d)}
function render(){const view=selected();renderTable(view);map.selectAll('path').attr('opacity',d=>cityFilter.value==='all'||d.properties.city===cityFilter.value?1:.18);map.selectAll('text').attr('opacity',d=>cityFilter.value==='all'||d.properties.city===cityFilter.value?1:.25);renderBars(view);renderMetric(view)}
countryFilter.addEventListener('change',render);cityFilter.addEventListener('change',render);skillFilter.addEventListener('change',render);metricFilter.addEventListener('change',render);countryFilter.value='México';skillFilter.value=skills[0];render();
</script></body></html>'''


def main() -> None:
    geojson = make_geojson()
    rows = INDICATOR_ROWS
    payload = json.dumps({"geojson": geojson, "rows": rows}, ensure_ascii=False).replace("</", "<\\/")
    (OUT / "city_labor_dashboard.html").write_text(TEMPLATE.replace("__DATA__", payload), encoding="utf-8")
    (OUT / "state_city_labor_indicators.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    with (OUT / "state_city_labor_indicators.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"PASS: dashboard filtrable creado en {OUT / 'city_labor_dashboard.html'}")


if __name__ == "__main__":
    main()
