-- Add photo_url column to ec_sfinti for AI-generated saint images
-- Run: psql "postgresql://ruguser:PASSWORD@localhost:5432/rugaciunisanatate" -f scripts/add-saint-photo-url.sql

BEGIN;

ALTER TABLE ec_sfinti ADD COLUMN IF NOT EXISTS photo_url TEXT;

-- Verify
SELECT slug, photo_url FROM ec_sfinti ORDER BY slug;

COMMIT;
