#!/bin/sh
# Database initialization script for SQLite container
# This ensures the database directory exists and has proper permissions

set -e

DB_DIR="/data"
DB_FILE="${DB_DIR}/medhealth.db"

echo "Initializing database directory..."
mkdir -p "${DB_DIR}"
chmod 777 "${DB_DIR}"

# Wait for backend to initialize the database schema
# The backend will create the tables on first connection
echo "Database directory ready. Backend will initialize schema on first connection."
echo "Database will be stored at: ${DB_FILE}"

# Keep container running
tail -f /dev/null
