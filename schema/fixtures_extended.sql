BEGIN;

ALTER TABLE fixtures
ADD COLUMN status VARCHAR(4),
ADD COLUMN home_goals INTEGER,
ADD COLUMN away_goals INTEGER,
ADD COLUMN halftime_home INTEGER,
ADD COLUMN halftime_away INTEGER,
ADD COLUMN fulltime_home INTEGER,
ADD COLUMN fulltime_away INTEGER,
ADD COLUMN extratime_home INTEGER,
ADD COLUMN extratime_away INTEGER,
ADD COLUMN penalty_home INTEGER,
ADD COLUMN penalty_away INTEGER;

COMMIT;
