#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python /opt/services/flaskapp/src/manage.py create_db
python /opt/services/flaskapp/src/manage.py seed_db

exec "$@"