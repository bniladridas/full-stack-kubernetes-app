#!/bin/bash
set -e

# Ensure the postgres user exists
psql -v ON_ERROR_STOP=1 --username postgres <<-EOSQL
    -- Create the postgres user if it doesn't exist
    DO \$\$
    BEGIN
        IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'postgres') THEN
            CREATE USER postgres WITH SUPERUSER PASSWORD 'postgrespassword';
        END IF;
    END
    \$\$;

    -- Create the myappuser with a password
    DO \$\$
    BEGIN
        IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'myappuser') THEN
            CREATE USER myappuser WITH PASSWORD 'myapppassword' CREATEDB;
        END IF;
    END
    \$\$;

    -- Create the database
    DO \$\$
    BEGIN
        IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'myappdb') THEN
            CREATE DATABASE myappdb;
        END IF;
    END
    \$\$;

    -- Grant all privileges to myappuser
    GRANT ALL PRIVILEGES ON DATABASE myappdb TO myappuser;
EOSQL

# Connect to the database and grant schema privileges
psql -v ON_ERROR_STOP=1 --username postgres --dbname myappdb <<-EOSQL
    -- Grant all privileges on public schema to myappuser
    GRANT ALL PRIVILEGES ON SCHEMA public TO myappuser;
    GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO myappuser;
    GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO myappuser;
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON TABLES TO myappuser;
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON SEQUENCES TO myappuser;
EOSQL

# Connect to the database and create the user table
psql -v ON_ERROR_STOP=1 --username postgres --dbname myappdb <<-EOSQL
    -- Ensure the table doesn't exist before creating
    DROP TABLE IF EXISTS "user";

    -- Create user table
    CREATE TABLE "user" (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        hashed_password VARCHAR(255) NOT NULL,
        is_active BOOLEAN DEFAULT TRUE,
        is_superuser BOOLEAN DEFAULT FALSE
    );

    -- Insert a default admin user
    -- Bcrypt hash of 'adminpassword'
    INSERT INTO "user" (username, email, hashed_password, is_active, is_superuser) 
    VALUES (
        'admin', 
        'admin@example.com', 
        '\$2b\$12\$EixZaYVK1fsbw1ZfbX3OXePaWxn0jolaWJM2BTEFzpcewf9kxvHDw', 
        TRUE, 
        TRUE
    ) ON CONFLICT DO NOTHING;
EOSQL

# Print out the users to verify
psql -v ON_ERROR_STOP=1 --username postgres --dbname myappdb <<-EOSQL
    SELECT username, email FROM "user";
EOSQL
