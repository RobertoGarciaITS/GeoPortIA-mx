import { StrictMode, useEffect, useRef, useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

type Business = { business_id:string; name:string; economic_activity:string; employee_range:string; latitude:number; longitude:number; source:string };
type Municipality = { municipality_name:string; state_name:string; geometry:{coordinates:number[][][]} };
const API = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";
declare global { interface Window { google?: any } }

function App() {
  const [businesses, setBusinesses] = useState<Business[]>([]);
  const [municipality, setMunicipality] = useState<Municipality | null>(null);
  const [selected, setSelected] = useState<Business | null>(null);
  const [nearby, setNearby] = useState<Business[]>([]);
  const [radius, setRadius] = useState(2000);
  const [error, setError] = useState("");
  const [mapReady, setMapReady] = useState(false);
  const mapRef = useRef<HTMLDivElement>(null);
  useEffect(() => { Promise.all([fetch(`${API}/api/businesses`).then(r=>r.json()), fetch(`${API}/api/municipality`).then(r=>r.json())]).then(([b,m])=>{setBusinesses(b);setMunicipality(m)}).catch(()=>setError("No se pudo conectar con la API.")); }, []);
  useEffect(() => { const timer = window.setInterval(() => { if (window.google) { setMapReady(true); window.clearInterval(timer); } }, 250); return () => window.clearInterval(timer); }, []);
  useEffect(() => {
    const key = import.meta.env.VITE_GOOGLE_MAPS_API_KEY;
    if (!key || !mapRef.current || !businesses.length || !window.google || !mapReady) return;
    const map = new window.google.maps.Map(mapRef.current, { center: {lat:25.438,lng:-100.973}, zoom:12, mapTypeControl:false, streetViewControl:false });
    businesses.forEach((b) => new window.google.maps.Marker({map, position:{lat:b.latitude,lng:b.longitude}, title:b.name}));
    new window.google.maps.Circle({map, center:{lat:25.438,lng:-100.973}, radius, strokeColor:"#f1b86b", fillColor:"#f1b86b", fillOpacity:.12});
  }, [businesses, radius, mapReady]);
  async function runQuery() { const r = await fetch(`${API}/api/nearby?lat=25.438&lng=-100.973&radius_m=${radius}`); const data = await r.json(); setNearby(data.businesses || []); }
  return <main><header><div><span className="eyebrow">GEOOPPORTUNITY MX · V0.1</span><h1>GeoOpportunity {municipality?.municipality_name || "Saltillo"}</h1><p>Explora negocios y valida una consulta espacial de proximidad.</p></div><div className="badge">{businesses.length} negocios</div></header>
    {error && <div className="error">{error} Ejecuta la API en el puerto 8000.</div>}
    <section className="layout"><div className="map"><div className="map-title">Mapa de referencia · {municipality?.state_name || "Coahuila de Zaragoza"}</div><div ref={mapRef} className="google-map"/><div className="territory">{businesses.map((b,i)=><button key={b.business_id} className={`marker ${nearby.some(n=>n.business_id===b.business_id)?"inside":""}`} style={{left:`${15+(i%5)*16}%`,top:`${25+Math.floor(i/5)*32}%`}} onClick={()=>setSelected(b)} title={b.name}>{i+1}</button>)}<div className="radius"/></div><div className="legend"><span className="dot"/> negocios <span className="dot selected-dot"/> dentro del radio</div></div>
      <aside><div className="panel"><h2>Análisis espacial</h2><label>Radio: <strong>{radius.toLocaleString()} m</strong></label><input type="range" min="500" max="5000" step="500" value={radius} onChange={e=>setRadius(Number(e.target.value))}/><button className="primary" onClick={runQuery}>Buscar negocios cercanos</button><div className="metric"><strong>{nearby.length}</strong><span>dentro del radio</span></div></div><div className="panel"><h2>{selected?.name || "Selecciona un negocio"}</h2>{selected ? <><p>{selected.economic_activity}</p><p>Empleados: {selected.employee_range}</p><p className="muted">{selected.latitude.toFixed(4)}, {selected.longitude.toFixed(4)}</p></> : <p className="muted">Haz clic en un marcador para ver sus atributos.</p>}</div></aside></section></main>
}
createRoot(document.getElementById("root")!).render(<StrictMode><App /></StrictMode>);
