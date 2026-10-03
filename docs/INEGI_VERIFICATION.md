# Evidencia de verificación de integración INEGI

Fecha de ejecución: 2026-10-03

## Comandos

```text
python -m pytest -q
25 passed

python scripts/inegi_smoke_test.py
SKIP: modo seguro; use --real para consultar DENUE.
CONFIG: token=ausente

python scripts/inegi_smoke_test.py --real --condition tecnologia --entity 05
BLOCKED: falta INEGI_DENUE_TOKEN; no se hizo una llamada real.
EXIT_CODE=2

Consulta real controlada con token ficticio:
HTTP 200 — `No autorizado. Utilice una clave válida.`
Resultado: el cliente lo traduce a `DenueError` sin persistir la respuesta.

Smoke del cliente con token ficticio:
`FAIL: DENUE rechazó el token: No autorizado`
`CLIENT_SMOKE_EXIT_CODE=1`

python scripts/labor_market_example.py
technology_establishments_fixture: 3
supply_available_estimate: 3.0
demand_fixture: 8.0
deficit_fixture: 5.0
scarcity_index: 2.6666666666666665
status: escasez
```

## Interpretación

- Las pruebas unitarias no dependen de internet y usan respuestas controladas.
- El smoke test local confirma que la ausencia del token se diagnostica sin llamar al servicio.
- El modo `--real` confirma el mismo bloqueo seguro y devuelve código 2 cuando falta el token.
- El smoke test real queda preparado, pero requiere definir `INEGI_DENUE_TOKEN` localmente.
- El ejemplo cruza un fixture de establecimientos DENUE con un extracto ENOE sintético.
- La demanda del ejemplo proviene de un fixture con el contrato de vacantes SNE; no representa vacantes oficiales descargadas.

## Criterios cubiertos

- Configuración por entorno: sí.
- Cliente DENUE y normalización: sí.
- Errores HTTP, JSON inválido, token y rate limit: sí.
- Paginación por ventanas `inicio/fin`: sí.
- Lector ENOE con factor de expansión: sí.
- Cruce de oferta, establecimientos y déficit: sí en fixture.
- Consulta real DENUE: pendiente de token local.
- Demanda real de vacantes: pendiente de fuente autorizada.
