-- Eksempelfil for å se Høst-temaene på SQL.
CREATE TABLE IF NOT EXISTS elev (
    id          INTEGER PRIMARY KEY,
    navn        VARCHAR(100) NOT NULL,
    klasse      CHAR(3) DEFAULT '3ST',
    fodt        DATE,
    aktiv       BOOLEAN DEFAULT TRUE
);

INSERT INTO elev (navn, klasse, fodt) VALUES ('Ada', '3ST', '2008-12-10');

/* Gjennomsnitt per klasse på siste prøve */
SELECT e.klasse,
       COUNT(*) AS antall,
       ROUND(AVG(p.poeng), 1) AS snitt
FROM elev AS e
JOIN prove AS p ON p.elev_id = e.id
WHERE p.dato >= DATE '2026-08-15'
  AND e.aktiv = TRUE
  AND p.poeng IS NOT NULL
GROUP BY e.klasse
HAVING COUNT(*) > 5
ORDER BY snitt DESC
LIMIT 10;
