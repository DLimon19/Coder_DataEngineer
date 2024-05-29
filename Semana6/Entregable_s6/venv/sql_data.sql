SHOW TABLES
FROM
SCHEMA "data-engineer-database"."luis_981908_coderhouse";

DROP TABLE IF EXISTS luis_981908_coderhouse.stage_covid_data;

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
