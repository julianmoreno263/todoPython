
use pruebaPedidos;

ALTER TABLE clientes 
ADD email VARCHAR(50);

UPDATE clientes
SET email = 'laura@gmail.com'
WHERE cliente_id = 5;

/*recordar orden de ejecucion de sql:

Un ejemplo rápido para ver el "viaje" de SQL
Imagina que ejecutas esto:

SQL
SELECT pais, COUNT(*) AS total
FROM clientes
WHERE edad > 18
GROUP BY pais
HAVING COUNT(*) > 5
ORDER BY total DESC;

El cerebro de SQL hace este recorrido:

Va a la tabla clientes (FROM).

Se queda solo con los mayores de 18 (WHERE).

Los junta por su pais (GROUP BY).

Revisa cuáles países tienen más de 5 clientes (HAVING).

Genera la columna pais y calcula el alias total (SELECT).

Finalmente, usa ese alias total para ordenar de mayor a menor (ORDER BY).*/

/*

Aquí tienes la tabla real, donde puedes ver que el orden cambia por completo:

El flujo real de SQL (¡Ahora sí!)
Orden en que tú lo ESCRIBES                    Orden en que SQL lo EJECUTA
1. SELECT                                       1. FROM / JOIN (Busca la tabla)
2. FROM                                         2. WHERE (Filtra filas individuales)
3. WHERE                                        3. GROUP BY (Agrupa los datos)
4. GROUP BY                                     4. HAVING (Filtra los grupos)
5. HAVING                                       5. SELECT (Elige columnas y crea alias)
6. ORDER BY                                     6. ORDER BY (Ordena el resultado)
7. LIMIT                                        7. LIMIT / TOP (Corta las filas)

¿Por qué es así? (Pensándolo con lógica humana)Si lo piensas, el motor de SQL es muy pragmático:No puede filtrar registros (WHERE) si primero no sabe de qué tabla sacarlos (FROM).No puede decirte qué columnas mostrar (SELECT) si primero no ha agrupado (GROUP BY) o filtrado la información.No puede ordenar el resultado final (ORDER BY) si todavía no sabe qué columnas quedaron en el SELECT.*/



/*Like: le da a la consulta un criterio de busqueda que es variable*/