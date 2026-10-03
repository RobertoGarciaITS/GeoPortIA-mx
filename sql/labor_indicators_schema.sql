-- Esquema lógico para BigQuery o PostgreSQL/PostGIS.
-- La geometría se mantiene separada para permitir varias escalas territoriales.
CREATE TABLE IF NOT EXISTS labor_indicators (
  snapshot_date DATE NOT NULL,
  country_code STRING NOT NULL,
  country_name STRING NOT NULL,
  state_code STRING NOT NULL,
  state_name STRING NOT NULL,
  city_code STRING NOT NULL,
  city_name STRING NOT NULL,
  skill_code STRING NOT NULL,
  skill_name STRING NOT NULL,
  available_talent FLOAT64 NOT NULL,
  demand FLOAT64 NOT NULL,
  deficit FLOAT64 NOT NULL,
  scarcity_index FLOAT64,
  demand_source STRING NOT NULL,
  supply_source STRING NOT NULL,
  is_synthetic BOOL NOT NULL,
  source_version STRING NOT NULL,
  loaded_at TIMESTAMP NOT NULL
);

-- Índices/particiones recomendados en PostgreSQL:
-- (snapshot_date, country_code, state_code, city_code, skill_code)
