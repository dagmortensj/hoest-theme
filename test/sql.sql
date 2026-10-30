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
