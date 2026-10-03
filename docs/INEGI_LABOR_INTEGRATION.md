# Integración laboral INEGI: DENUE + ENOE

## Alcance

- **DENUE**: establecimientos, ubicación, actividad económica y estrato de personal ocupado.
- **ENOE**: encuesta de hogares; carrera, ocupación, condición laboral y factores de expansión.
- **Demanda específica**: vacantes y habilidades (por ejemplo AWS), que deben incorporarse desde una fuente de vacantes autorizada o un extracto controlado.

La API DENUE usa un token en la ruta. El cliente nunca contiene el token ni lo escribe en logs. ENOE no se trata como una API de vacantes: se carga mediante extractos CSV/tabulados o microdatos oficiales procesados conforme a su diseño muestral.

## Operaciones DENUE implementadas

| Operación | Uso | Ruta oficial |
|---|---|---|
| `Buscar` | condición alrededor de coordenadas | `/Buscar/{condición}/{latitud,longitud}/{metros}/{token}` |
| `BuscarEntidad` | condición, entidad y rango de registros | `/BuscarEntidad/{condición}/{entidad}/{inicio}/{fin}/{token}` |
| `Nombre` | nombre o razón social por entidad | `/Nombre/{nombre}/{entidad}/{inicio}/{fin}/{token}` |
| `Ficha` | detalle de un establecimiento | `/Ficha/{id}/{token}` |
| `Cuantificar` | conteo por actividad, área y estrato | `/Cuantificar/{actividad}/{área}/{estrato}/{token}` |
| `BuscarAreaAct` | listado por entidad, municipio, localidad, AGEB, manzana, actividad y estrato | `/BuscarAreaAct/{áreas}/{actividad}/{inicio}/{fin}/{estrato}/{token}` |

El radio máximo aplicado por el cliente es 5,000 metros, conforme a la documentación del servicio. Los códigos de actividad y área se mantienen como parámetros explícitos para no confundir una clave SCIAN con una ocupación laboral.

El método `iter_entity` usa ventanas `inicio/fin` y termina al recibir una página corta. `max_pages` limita el consumo accidental del servicio.
`search_area_activity` expone los códigos municipales, de localidad, AGEB y manzana sin ocultarlos en una cadena libre; para Saltillo se puede usar entidad `05` y municipio `030`.

## Variables ENOE que se conservarán

| Grupo | Variables de trabajo |
|---|---|
| Sociodemográficas | edad, sexo, nivel de instrucción, carrera, asistencia y egreso |
| Actividad | PEA/PNEA, ocupado, desocupado, disponibilidad y búsqueda de empleo |
| Ocupación | ocupación principal, actividad económica, posición en el trabajo |
| Calidad | trimestre, dominio geográfico, factor de expansión, error estándar y CV |

El esquema interno del fixture reduce estas variables a `geography`, `field_of_study`, `occupation`, `employment_status`, `skill` y `expansion_factor`; los microdatos productivos deben conservar sus diccionarios y metadatos originales.

Antes de procesar un extracto, el lector verifica columnas mínimas, geografía, condición laboral y que el factor de expansión sea numérico. Las columnas originales de la edición ENOE deben mapearse a este contrato en una etapa previa y conservarse junto con el diccionario de datos.

## Configuración

Definir `INEGI_DENUE_TOKEN` en el entorno local. No subir el archivo real. El smoke test no consulta la red salvo que se indique `--real`.

```powershell
$env:PYTHONPATH="apps/api"
$env:INEGI_DENUE_TOKEN="<token-local>"
python scripts/inegi_smoke_test.py --real --condition tecnologia --entity 05
```

## Pruebas

```powershell
python -m pytest -q
python scripts/inegi_smoke_test.py
python scripts/labor_market_example.py

# También acepta archivos normalizados propios
python scripts/labor_market_example.py --enoe ruta/enoe.csv --denue ruta/denue.csv --vacancies ruta/vacantes.csv --geography Saltillo --skill AWS
```

Las pruebas unitarias usan `httpx.MockTransport`; no necesitan internet ni token. Prueban URL, parsing, token ausente, respuesta inválida y HTTP 429. El smoke test real es opt-in para evitar consumo accidental del servicio.

## Ejemplo laboral

`data/sample/enoe_extract_saltillo.csv` y `data/sample/denue_saltillo_tech.csv` son fixtures sintéticos y anonimizados. El script enlaza tres establecimientos tecnológicos con una oferta disponible de AWS y una demanda deliberadamente sintética. No debe publicarse como estadística oficial.

Para producción hay que conservar trimestre, diccionario, ponderador y metadatos ENOE; agregar usando el factor de expansión; validar dominio de estudio, error estándar y coeficiente de variación; e incorporar vacantes con fecha, localidad, habilidad, salario y fuente.

La ENOE tiene cobertura nacional, por entidad y ciudad autorrepresentada; no debe forzarse una estimación municipal de Saltillo si el dominio muestral no la respalda.

## Vacantes y demanda

El adaptador `vacancies.py` consume un CSV normalizado con identificador, geografía, puesto, habilidad, fuente y fecha. El fixture sigue la estructura mínima necesaria para procesar un extracto del Portal del Empleo/SNE. El conjunto público de [Servicios de vinculación laboral en datos.gob.mx](https://www.datos.gob.mx/dataset/servicios_vinculacion_laboral) es una fuente de referencia gubernamental; antes de cargar una edición real se debe verificar su URL de descarga, licencia, periodo y diccionario de datos.

El Portal del Empleo también publica el [periódico digital de ofertas del SNE](https://www.empleo.gob.mx/static/periodico-digital.html). Si la fuente se entrega como PDF o CSV, debe convertirse a este contrato sin conservar datos personales de candidatos.

## Fuentes oficiales

- [API DENUE](https://www.inegi.org.mx/servicios/api_denue.html)
- [ENOE](https://www.inegi.org.mx/programas/enoe/)
- [Metadatos ENOE 2025](https://www.inegi.org.mx/rnm/index.php/catalog/1121)
- [Anuarios ANUIES](https://anuario.anuies.mx/)
