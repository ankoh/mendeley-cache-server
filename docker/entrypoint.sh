#!/usr/bin/env bash

# First check the environment variables
if [ -z "$MC_DATABASE_HOSTNAME" ]; then
    echo "You need to provide MC_DATABASE_HOSTNAME as environment variable"
    exit 1
fi
if [ -z "$MC_DATABASE_PORT" ]; then
    echo "You need to provide MC_DATABASE_PORT as environment variable"
    exit 1
fi
if [ -z "$MC_DATABASE_DB" ]; then
    echo "You need to provide MC_DATABASE_DB as environment variable"
    exit 1
fi
if [ -z "$MC_DATABASE_USER" ]; then
    echo "You need to provide MC_DATABASE_USER as environment variable"
    exit 1
fi
if [ -z "$MC_DATABASE_SECRET" ]; then
    echo "You need to provide MC_DATABASE_SECRET as environment variable"
    exit 1
fi

# Then wait for mysql
while ! mysqladmin ping --host="$MC_DATABASE_HOSTNAME" --port="$MC_DATABASE_PORT" --silent; do
    sleep 1
done

# Assert mcdb database
printf "Creating database if not existing\n"
mysql --host="$MC_DATABASE_HOSTNAME" --port="$MC_DATABASE_PORT" \
      --user="$MC_DATABASE_USER" --password="$MC_DATABASE_SECRET" \
      --execute="CREATE DATABASE IF NOT EXISTS $MC_DATABASE_DB;"

# Prepare application
python -m mendeleycache.runner prepare

# Then fire the rest of the commands
exec "$@"