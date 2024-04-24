-- Ejercicio 1
-- Extraer agentes cuyo nombre empieza por M y termina en O
--INSERT INTO agents  VALUES(11,'Martin Moreno');
SELECT *
FROM   agents a 
WHERE  a.name LIKE 'M%o'
;

-- Ejercicio 2
-- Consulta que obtenga una lista en orden alfabetico, de todas las distintas
-- ocupaciones en la tabla customer que contenga la palabra engineer
SELECT DISTINCT(c.occupation)
FROM   customers c 
WHERE  c.occupation LIKE '%Engineer%'
ORDER BY c.occupation 
;

-- Ejercicio 3
-- Escribir una consulta que devuelva el ID del cliente, su nombre y una columna
-- nueva "Mayor30" que contenga "Si" si el cliente es mayor de 30 y "No" en caso contrario
SELECT c.customerid ,
       c.name ,
       c.Age,
       CASE
       	WHEN c.Age > 30 THEN
       	   "Si"
       	WHEN c.Age <= 30 THEN
       	   "No"
       END
       Mayor30
FROM customers c 
;


-- Ejercicio 4
-- Escribir una consulta que devuelva todas las llamadas realizadas a clientes de la profesion 
-- ingenieria y muestre si son mayores o menores de 30, asi como si terminaron comprando el 
-- producto de esa llamada

SELECT c.callid ,
       c2.customerid ,
       c2.name ,
       CASE
       	WHEN c2.Age > 30 THEN
       	   "Si"
       	WHEN c2.Age <= 30 THEN
       	   "No"
       END
       Mayor30,
       CASE
       	WHEN c.productsold > 0 THEN
       	   "Si"
       	WHEN c.productsold = 0 THEN
       	   "No"
       END
       Compro
FROM calls c 
INNER JOIN customers c2 
ON c.customerid  = c2.customerid 
WHERE c.pickedup  = 1
AND c2.occupation LIKE '%Engineer%'
;


-- Ejercicio 5
-- Una consutla que regrese la cantidad de ventas totales y llamadas totales realizadas a los clientes 
-- de la ocupacion ingenieria
-- Otra que calcule las mismas metricas para toda la base de clientes

SELECT COUNT(c.callid) llamadas,
       SUM(c.productsold) ventas
FROM calls c 
INNER JOIN customers c2 
ON c.customerid = c2.customerid 
WHERE c2.occupation LIKE '%Engineer%'
;

SELECT COUNT(c.callid) llamadas,
       COUNT(CASE 
       	WHEN c.productsold > 0 THEN
       	   TRUE
       END) 
       ventas      
FROM calls c 
INNER JOIN customers c2 
ON c.customerid = c2.customerid 
WHERE c2.occupation LIKE '%Engineer%'
;

SELECT COUNT(c.callid) llamadas,
       SUM(c.productsold) ventas
FROM calls c 
INNER JOIN customers c2 
ON c.customerid = c2.customerid 
;

SELECT COUNT(c.callid) llamadas,
       COUNT(CASE 
       	WHEN c.productsold > 0 THEN
       	   TRUE
       END) 
       ventas      
FROM calls c 
INNER JOIN customers c2 
ON c.customerid = c2.customerid 
;


-- Ejercicio 6
-- Escribir una consulta que devuelve el nombre del agente, cantidad de llamadas, las llamadas mas largas, mas cortas,
-- duracion promedio de las llamadas y cantidad total de productos vendidos
-- Nombre de las columnas: AgentName, NCalls, Shortest, Longest, AvgDuration y TotalSales
-- Ordenas la tabla por AgentName en orden alfabetido

SELECT a.name AgentName,
       COUNT(c.callid) NCalls,
       MIN(c.duration) Shortest,
       MAX(c.duration) Longest,
       AVG(c.duration) AvgDuration,
       SUM(c.productsold) TotalSales
FROM calls c 
INNER JOIN agents a 
ON a.agentid = c.agentid 
GROUP BY a.agentid 
ORDER BY AgentName
;


-- Ejercicio 7
-- Una consulta que extraiga 2 metricas:
-- Por cada agente, la cantidad de segundos promedio que le toma vender un producto cuando tienen exito
-- Para cada agente, la cantidad de segundos promedio permanecen en el telefono antes de darse por vencidos cuando no tienen exito

SELECT t.name,
       CASE 
       	WHEN t.PromExito IS NOT NULL THEN t.PromExito
       	WHEN t.PromExito IS NULL THEN 0
       END PromExito,
       CASE 
       	WHEN t.PromSinExito IS NOT NULL THEN t.PromExito
       	WHEN t.PromSinExito IS NULL THEN 0
       END PromSinExito
FROM
(
   SELECT DISTINCT(a.agentid),
          a.name ,
          (SELECT AVG(c.duration)
           FROM calls c
           WHERE c.agentid = a.agentid
           AND c.productsold > 0) PromExito,
          (SELECT AVG(c.duration)
           FROM calls c
           WHERE c.agentid = a.agentid
           AND c.productsold = 0) PromSinExito
   FROM agents a 
) t
ORDER BY t.name
;

