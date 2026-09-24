CREATE TABLE IF NOT EXISTS contador (id integer PRIMARY KEY, total integer NOT NULL);
INSERT INTO contador (id, total) VALUES (1, 0) ON CONFLICT (id) DO NOTHING;
