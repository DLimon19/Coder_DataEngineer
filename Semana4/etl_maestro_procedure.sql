CREATE OR REPLACE PROCEDURE pETL_Desastres () LANGUAGE plpgsql
AS $$
BEGIN
	DECLARE
		error_msg VARCHAR(255);
	BEGIN
		INSERT INTO desastres_final (cuatrenio,temp_avg,oxi_avg,t_tsunamis,t_olascalor,t_terremotos,t_erupciones,t_incendios,m_jovenes_avg,m_adutos_avg,m_ancianos_avg)
		SELECT r.rango,
		       AVG(c.temperatura) avg_temp, 
		       AVG(c.oxigeno) avg_oxi, 
		       SUM(d.tsunamis) sum_tsu,
		       SUM(d.olas_calor) sum_olar_calor,
		       SUM(d.terremotos) sum_terremotos,
		       SUM(d.erupciones) sum_erup,
		       SUM(d.incendios) sum_inc,
		       AVG(m.joven) avg_jov,
		       AVG(m.adulto) avg_adu,
		       AVG(m.anciano) avg_anc
		FROM ( SELECT '2023-2026' as rango
		       UNION 
		       SELECT '2027-2030' as rango
		     ) r
		
		INNER JOIN ( SELECT temperatura,
		                    oxigeno,
		                    CASE
		                       WHEN año BETWEEN 2023 AND 2026 THEN '2023-2026'
		                       WHEN año BETWEEN 2027 AND 2030 THEN '2027-2030'
		                    END rango
		             FROM clima
		           ) c
		   ON r.rango = c.rango
		INNER JOIN ( SELECT tsunamis,
		                    olas_calor,
		                    terremotos,
		                    erupciones,
		                    incendios,
		                    CASE
			                   WHEN año BETWEEN 2023 AND 2026 THEN '2023-2026'
			                   WHEN año BETWEEN 2027 AND 2030 THEN '2027-2030'
			                END AS rango
		             FROM desastres
		           ) d 
		   ON c.rango = d.rango
		INNER JOIN (SELECT r_menor15 joven,
		                   r_15_a_30 + r_30_a_45 + r_45_a_60 adulto,
		                   r_m_a_60 anciano,
		                   CASE
			                  WHEN año BETWEEN 2023 AND 2026 THEN '2023-2026'
			                  WHEN año BETWEEN 2027 AND 2030 THEN '2027-2030'
			               END AS rango
		                   
		            FROM muertes
		            ) m
		   ON d.rango = m.rango
		   
		GROUP BY r.rango;
		
		
		
	EXCEPTION
		WHEN OTHERS THEN
			error_msg := 'Error during data transfer. Rolling back...';
	        RAISE NOTICE '%', error_msg;
	        RAISE EXCEPTION '%', error_msg;
	        ROLLBACK;
	END;
	
	COMMIT;	

END;
$$;

CALL pETL_Desastres();
