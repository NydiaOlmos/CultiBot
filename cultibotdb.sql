CREATE TABLE plantas (
id_planta BIGINT NOT NULL GENERATED ALWAYS AS IDENTITY,
nombre VARCHAR(50) NOT NULL,
tipo VARCHAR(50) NOT NULL,
tipo_suelo VARCHAR(15) NOT NULL,

PRIMARY KEY(id_planta)
);

CREATE TABLE metricas (
id_metrica BIGINT NOT NULL GENERATED ALWAYS AS IDENTITY,
id_planta BIGINT NOT NULL,
humedad_suelo FLOAT NULL,
temperatura_ambiente FLOAT NULL,
luminosidad FLOAT NULL,
nitrogeno FLOAT NULL,
potasio FLOAT NULL, 
fosforo FLOAT NULL,
fecha TIMESTAMP NOT NULL,

PRIMARY KEY(id_metrica),
CONSTRAINT fk_metrica_planta_id FOREIGN KEY(id_planta) REFERENCES plantas(id_planta)
);

INSERT INTO plantas (nombre, tipo, tipo_suelo) VALUES
('Tomata', 'Tomate Roma', 'Otro'),
('Helena', 'Helecho Espada', 'Tierra negra'),
('Amatista', 'Lavanda Inglesa', 'Arenoso');

INSERT INTO metricas (id_planta, humedad_suelo, temperatura_ambiente, luminosidad, nitrogeno, potasio, fosforo, fecha) VALUES

-- --------------------------------------------------------
-- PLANTA 1: Tomate Manzano (id_planta = 1)
-- --------------------------------------------------------
-- Día 1
(1, 65.5, 18.2, 0.0, 2.1, 1.8, 1.2, '2026-05-20 00:00:00'),
(1, 63.2, 21.5, 4500.0, 2.1, 1.8, 1.2, '2026-05-20 06:00:00'),
(1, 58.0, 28.4, 45000.0, 2.0, 1.7, 1.2, '2026-05-20 12:00:00'),
(1, 60.1, 24.1, 12000.0, 2.0, 1.7, 1.1, '2026-05-20 18:00:00'),
-- Día 2
(1, 57.3, 17.9, 0.0, 2.0, 1.7, 1.1, '2026-05-21 00:00:00'),
(1, 70.0, 20.8, 4100.0, 2.2, 1.9, 1.3, '2026-05-21 06:00:00'), -- Simula un riego temprano
(1, 64.2, 27.6, 43500.0, 2.2, 1.8, 1.3, '2026-05-21 12:00:00'),
(1, 61.8, 23.5, 11500.0, 2.1, 1.8, 1.2, '2026-05-21 18:00:00'),

-- --------------------------------------------------------
-- PLANTA 2: Helecho Espada (id_planta = 2)
-- --------------------------------------------------------
-- Día 1
(2, 80.2, 16.5, 0.0, 1.5, 1.2, 0.8, '2026-05-20 00:00:00'),
(2, 79.0, 18.0, 800.0, 1.5, 1.2, 0.8, '2026-05-20 06:00:00'), -- Prefiere la sombra
(2, 75.4, 22.3, 2500.0, 1.4, 1.1, 0.7, '2026-05-20 12:00:00'),
(2, 74.1, 19.8, 600.0, 1.4, 1.1, 0.7, '2026-05-20 18:00:00'),
-- Día 2
(2, 72.8, 16.1, 0.0, 1.4, 1.1, 0.7, '2026-05-21 00:00:00'),
(2, 82.0, 17.5, 750.0, 1.6, 1.3, 0.9, '2026-05-21 06:00:00'), -- Simula riego
(2, 78.5, 21.9, 2400.0, 1.5, 1.2, 0.8, '2026-05-21 12:00:00'),
(2, 76.3, 19.2, 550.0, 1.5, 1.2, 0.8, '2026-05-21 18:00:00'),

-- --------------------------------------------------------
-- PLANTA 3: Lavanda Inglesa (id_planta = 3)
-- --------------------------------------------------------
-- Día 1
(3, 40.1, 19.0, 0.0, 0.8, 1.5, 0.5, '2026-05-20 00:00:00'), -- Prefiere suelos secos
(3, 39.5, 22.4, 5000.0, 0.8, 1.5, 0.5, '2026-05-20 06:00:00'),
(3, 35.2, 31.2, 52000.0, 0.7, 1.4, 0.4, '2026-05-20 12:00:00'), -- Alta exposición solar
(3, 34.0, 26.7, 15000.0, 0.7, 1.4, 0.4, '2026-05-20 18:00:00'),
-- Día 2
(3, 33.5, 18.5, 0.0, 0.7, 1.4, 0.4, '2026-05-21 00:00:00'),
(3, 45.0, 21.8, 4800.0, 0.9, 1.6, 0.6, '2026-05-21 06:00:00'), -- Riego ligero semanal
(3, 41.3, 30.5, 50500.0, 0.8, 1.5, 0.5, '2026-05-21 12:00:00'),
(3, 38.7, 25.9, 14200.0, 0.8, 1.5, 0.5, '2026-05-21 18:00:00');

UPDATE plantas SET tipo_suelo = 'otro' WHERE tipo_suelo = 'Otro';
UPDATE plantas SET tipo_suelo = 'tierra negra' WHERE tipo_suelo = 'Tierra negra';
UPDATE plantas SET tipo_suelo = 'arenoso' WHERE tipo_suelo = 'Arenoso';
