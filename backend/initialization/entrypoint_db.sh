#!/bin/bash
set -e

DB_FILE="/app/data/sqlite_tiny.db"

if [ ! -f "$DB_FILE" ]; then
    echo "Инициализация БД..."
    python ./init_db.py
fi

exec "$@"