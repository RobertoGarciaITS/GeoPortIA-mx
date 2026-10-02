CREATE SCHEMA IF NOT EXISTS `${PROJECT_ID}.${DATASET}`;

CREATE TABLE IF NOT EXISTS `${PROJECT_ID}.${DATASET}.municipalities` (
  municipality_id STRING NOT NULL, cvegeo STRING NOT NULL, municipality_name STRING NOT NULL,
  state_name STRING NOT NULL, geometry GEOGRAPHY NOT NULL, source STRING NOT NULL
);

CREATE TABLE IF NOT EXISTS `${PROJECT_ID}.${DATASET}.businesses` (
  business_id STRING NOT NULL, source_record_id STRING NOT NULL, name STRING NOT NULL,
  scian STRING NOT NULL, economic_activity STRING NOT NULL, employee_range STRING NOT NULL,
  latitude FLOAT64 NOT NULL, longitude FLOAT64 NOT NULL, geography GEOGRAPHY NOT NULL,
  municipality_id STRING NOT NULL, source STRING NOT NULL
);
