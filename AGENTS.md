# AGENTS.md

- Mantener el alcance V0.1: Saltillo, 10 negocios y una consulta de radio.
- No agregar scoring, IA, autenticación, PostGIS, Redis, GKE o nuevas fuentes sin change request.
- No comprometer secretos. Usar `.env.example` como contrato de configuración.
- Ejecutar `pytest` para API y `npm run build` para frontend antes de entregar cambios.
