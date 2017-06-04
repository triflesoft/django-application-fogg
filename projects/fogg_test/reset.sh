#!/bin/bash

su -c 'psql -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '\''fogg_test'\'';"' postgres
su -c 'psql -c "DROP DATABASE fogg_test;"' postgres
su -c 'psql -c "CREATE DATABASE fogg_test WITH ENCODING='\''UTF8'\'' OWNER=fogg_test;"' postgres
su -c 'psql -c "CREATE EXTENSION HSTORE;" -d fogg_test' postgres

./manage.py migrate --run-syncdb
./manage.py load_fogg_countries
./manage.py load_fogg_ge_divisions
./manage.py createsuperuser --username admin --noinput --email "admin@localhost"
./manage.py changepassword admin

echo "==== TABLES ===="
su -c 'psql -P pager=off -c "SELECT table_name FROM information_schema.tables WHERE table_schema = '\''public'\'' ORDER BY table_name;"' postgres
echo "================"

exit
