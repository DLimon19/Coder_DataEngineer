SHOW TABLES
FROM
SCHEMA "data-engineer-database"."luis_981908_coderhouse";

-- Se eliminan la vista y la tabla si existen previamente
DROP VIEW IF EXISTS luis_981908_coderhouse.covid_data_analist;
DROP TABLE IF EXISTS luis_981908_coderhouse.stage_covid_data;

-- Se crea la tabla stage_covid_data
CREATE TABLE stage_covid_data(
    fips	             VARCHAR(200)
,   admin2	             VARCHAR(200)
,   province_state	     VARCHAR(200)
,   country_region       VARCHAR(200)
,   last_update          DATE
,   lat                  VARCHAR(50)
,   long_                VARCHAR(50)
,   confirmed            VARCHAR(50)
,   deaths               VARCHAR(50)
,   recovered            VARCHAR(50)
,   active               VARCHAR(50)
,   combined_key         VARCHAR(50)
,   incident_rate        VARCHAR(50)
,   case_fatality_ratio  VARCHAR(50)
);


SELECT  
*
FROM stage_covid_data;

-- Se crea la vista con masking en el campo deaths
CREATE OR REPLACE VIEW covid_data_analist AS
(
	SELECT sc.province_state, 
	       sc.country_region, 
	       sc.last_update, 
	       sc.lat, sc.long_ AS long, 
	       sc.confirmed, 
	       regexp_replace(sc.deaths::text, '[[:digit:]]'::text, '*'::text) AS deaths, 
	       sc.recovered, 
	       sc.active, 
	       sc.incident_rate, 
	       sc.case_fatality_ratio
   FROM stage_covid_data sc
);


SELECT
*
FROM covid_data_analist;