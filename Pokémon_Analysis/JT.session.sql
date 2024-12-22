-- Add Generation ColoumnDO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_name = 'pokemon' AND column_name = 'generation'
    ) THEN
        ALTER TABLE pokemon
        ADD COLUMN generation INT;
    END IF;


SELECT * FROM pokemon


