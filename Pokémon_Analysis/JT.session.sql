-- Add Generation ColoumnDO $$
-- DO $$
-- BEGIN
--     IF NOT EXISTS (
--         SELECT 1
--         FROM information_schema.columns
--         WHERE table_name = 'pokemon' AND column_name = 'generation'
--     ) THEN
--         ALTER TABLE pokemon
--         ADD COLUMN generation INT;
--     END IF;
-- END $$;

-- Create Generation Coloumn
UPDATE pokemon
SET generation =
    CASE 
        WHEN id > 0 AND id <= 151 THEN 1
        WHEN id > 151 AND id <= 251 THEN 2
        WHEN id > 251 AND id <= 386 THEN 3
        WHEN id > 386 AND id <= 493 THEN 4
        WHEN id > 493 AND id <= 649 THEN 5
        ELSE NULL
    END;


DROP TABLE IF EXISTS TypeEffective;

CREATE TABLE TypeEffective
(
    pokemon_id INT,
    Normal VARCHAR(10),
    Fire VARCHAR(10),
    Water VARCHAR(10),
    Electric VARCHAR(10),
    Grass VARCHAR(10),
    Ice VARCHAR(10),
    Fighting VARCHAR(10),
    Poison VARCHAR(10),
    Ground VARCHAR(10),
    Flying VARCHAR(10),
    Psychic VARCHAR(10),
    Bug VARCHAR(10),
    Rock VARCHAR(10),
    Ghost VARCHAR(10),
    Dark VARCHAR(10),
    Steel VARCHAR(10)
);

-- Insert pokemon IDs into the new table
INSERT INTO TypeEffective (pokemon_id)
SELECT id
FROM pokemon;

SELECT * FROM TypeEffective