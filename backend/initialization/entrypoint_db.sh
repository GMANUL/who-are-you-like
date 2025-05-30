#!/bin/bash
set -e

DB_FILE="./data/sqlite_imdb.db"

if [ ! -f "$DB_FILE" ]; then
    echo "Инициализация БД..."
    python ./initialization/init_db.py
fi

exec "$@"