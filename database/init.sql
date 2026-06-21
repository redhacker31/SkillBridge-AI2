-- =============================================================================
-- SkillBridge AI — PostgreSQL Initialization
-- =============================================================================
-- This script runs on first database creation via Docker entrypoint.
-- =============================================================================

-- Enable useful extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Set timezone
SET timezone = 'UTC';

-- Log successful initialization
DO $$
BEGIN
    RAISE NOTICE 'SkillBridge AI database initialized successfully';
END
$$;
