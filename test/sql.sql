-- SQL: tabeller, spørringer, sammenslåinger og funksjoner
CREATE TABLE IF NOT EXISTS legeme (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    navn      VARCHAR(64) NOT NULL UNIQUE,
    masse     DOUBLE PRECISION DEFAULT 1.0 CHECK (masse > 0),
    opprettet TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    aktiv     BOOLEAN DEFAULT TRUE
);

CREATE INDEX idx_navn ON legeme (navn);

INSERT INTO legeme (navn, masse) VALUES ('Jorda', 5.972e24), ('Mars', 6.417e23);

/* Blokkommentar
   over flere linjer */
SELECT l.navn,
       COUNT(m.id) AS antall_maaner,
       ROUND(AVG(m.masse), 2) AS snitt,
       CASE WHEN l.masse > 1e24 THEN 'tung' ELSE 'lett' END AS klasse
FROM legeme AS l
LEFT JOIN maane m ON m.planet_id = l.id
WHERE l.navn LIKE 'J%' AND l.aktiv IS NOT NULL
  AND l.id IN (SELECT planet_id FROM maane WHERE masse BETWEEN 1 AND 1e30)
GROUP BY l.navn
HAVING COUNT(*) >= 1
ORDER BY snitt DESC NULLS LAST
LIMIT 10 OFFSET 0;

WITH tunge AS (SELECT * FROM legeme WHERE masse > 1e24)
UPDATE legeme SET aktiv = FALSE WHERE id NOT IN (SELECT id FROM tunge);

DELETE FROM legeme WHERE opprettet < NOW() - INTERVAL '1 year';
BEGIN TRANSACTION;
COMMIT;

-- Vanskelige tilfeller: underspørringer, vindusfunksjoner, uttrykk, strenger og typer
SELECT navn,
       masse * 1e-24 AS masse_i_jordmasser,
       (masse - LAG(masse) OVER (ORDER BY masse)) / NULLIF(masse, 0) AS endring,
       ROW_NUMBER() OVER (PARTITION BY aktiv ORDER BY opprettet DESC) AS nr,
       COALESCE(NULLIF(navn, ''), 'ukjent') || ' (' || CAST(id AS TEXT) || ')' AS etikett,
       'a + b == c' AS tekst, 'apostrof ''x''' AS sitat, "kolonne med mellomrom" AS k,
       EXTRACT(YEAR FROM opprettet) - 2000 >= 26 AND masse <> 0 OR NOT aktiv AS test,
       CASE WHEN masse IS NULL THEN -1 WHEN masse != 0 AND id % 2 = 0 THEN masse ELSE 0 END AS verdi
FROM legeme l
INNER JOIN (SELECT planet_id, SUM(masse) AS total FROM maane GROUP BY planet_id) m ON m.planet_id = l.id
WHERE navn NOT LIKE '%\_%' ESCAPE '\' AND navn ILIKE 'j%' AND opprettet >= DATE '2026-01-01' AND id <= 1e3
  AND EXISTS (SELECT 1 FROM maane WHERE maane.planet_id = l.id AND maane.masse > ALL (SELECT 0))
ORDER BY 2 DESC, nr ASC;
ALTER TABLE legeme ADD COLUMN radius NUMERIC(10, 2) NOT NULL DEFAULT 0 CHECK (radius >= 0);
CREATE OR REPLACE FUNCTION kraft(m1 DOUBLE PRECISION, m2 DOUBLE PRECISION, r DOUBLE PRECISION) RETURNS DOUBLE PRECISION AS $$
  SELECT 6.674e-11 * m1 * m2 / (r * r);
$$ LANGUAGE SQL IMMUTABLE;
CREATE VIEW tunge AS SELECT * FROM legeme WHERE masse > 1e24 UNION ALL SELECT * FROM legeme WHERE id IN (1, 2);
DROP TABLE IF EXISTS gammel CASCADE; TRUNCATE TABLE logg; GRANT SELECT ON legeme TO leser;
