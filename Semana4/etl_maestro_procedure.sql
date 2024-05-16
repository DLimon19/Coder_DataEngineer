CREATE OR REPLACE PROCEDURE pETL_Desastres () LANGUAGE plpgsql
AS $$
BEGIN
	DECLARE
		error_msg VARCHAR(255);
	BEGIN
		INSERT INTO desastres_final (cuatrenio,temp_avg,oxi_avg,t_tsunamis,t_olascalor,t_terremotos,t_erupciones,t_incendios,m_jovenes_avg,m_adutos_avg,m_ancianos_avg)
		SELECT r.rango,
		       c.temperatura avg_temp, 
		       c.oxigeno avg_oxi, 
		       d.tsunamis sum_tsu,
		       d.olas_calor sum_olar_calor,
		       d.terremotos sum_terremotos,
		       d.erupciones sum_erup,
		       d.incendios sum_inc,
		       m.joven avg_jov,
			   m.adulto avg_adu,
			   m.anciano avg_anc
		FROM ( SELECT '2023-2026' as rango
		       UNION 
		       SELECT '2027-2030' as rango
		     ) r
		
		INNER JOIN ( SELECT AVG(temperatura) temperatura,
		                    AVG(oxigeno) oxigeno,
		                    CASE
		                       WHEN año BETWEEN 2023 AND 2026 THEN '2023-2026'
		                       WHEN año BETWEEN 2027 AND 2030 THEN '2027-2030'
		                    END rango
		             FROM clima
		             GROUP BY rango
		           ) c
		   ON r.rango = c.rango
		INNER JOIN ( SELECT SUM(tsunamis) tsunamis,
		                    SUM(olas_calor) olas_calor,
		                    SUM(terremotos) terremotos,
		                    SUM(erupciones) erupciones,
		                    SUM(incendios) incendios,
		                    CASE
			                   WHEN año BETWEEN 2023 AND 2026 THEN '2023-2026'
			                   WHEN año BETWEEN 2027 AND 2030 THEN '2027-2030'
			                END AS rango
		             FROM desastres
		             GROUP BY rango
		           ) d 
		   ON c.rango = d.rango
		INNER JOIN (SELECT AVG(r_menor15) joven,
		                   AVG(r_15_a_30 + r_30_a_45 + r_45_a_60) adulto,
		                   AVG(r_m_a_60) anciano,
		                   CASE
			                  WHEN año BETWEEN 2023 AND 2026 THEN '2023-2026'
			                  WHEN año BETWEEN 2027 AND 2030 THEN '2027-2030'
			               END AS rango
		                   
		            FROM muertes
		            GROUP BY rango
		            ) m
		   ON d.rango = m.rango
		;
		
		
		
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
