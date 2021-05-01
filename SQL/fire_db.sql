--------Creating Tables--------
--Create Titles
CREATE TABLE firemap (
  index VARCHAR(50) PRIMARY KEY,
  lng FLOAT,
  lat FLOAT,
  discovery_date TIMESTAMP,
  fire_cause VARCHAR(50),
  fire_cause_general VARCHAR(50),
  fire_cause_specific VARCHAR(50),
  incident_name VARCHAR(50)
);
DROP TABLE firemap;

SELECT * FROM firemap;