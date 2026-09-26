#!/bin/bash
# Creates the two least-privilege database users (docs/05-data-model.md section 7).
# Runs once, when the MySQL container initialises an empty data directory. The same script is used by
# docker-compose.yml (development) and by the Testcontainers setup (tests).
#
#   cc_migrator  owns the schema: DDL, run by Flyway. It may grant table rights to cc_app.
#   cc_app       used by the running application. Its table-level rights are granted by the Flyway
#                callback db/migration/afterMigrate.sql, which gives audit_event INSERT and SELECT only.
#
# Neither user is root. Passwords come from the environment, never from this file.
# No "set -u": the MySQL entrypoint may source (not execute) this file, and -u would leak into it.
set -eo pipefail

: "${MYSQL_DATABASE:?MYSQL_DATABASE is required}"
: "${CC_DB_MIGRATOR_PASSWORD:?CC_DB_MIGRATOR_PASSWORD is required}"
: "${CC_DB_APP_PASSWORD:?CC_DB_APP_PASSWORD is required}"

mysql --protocol=socket -uroot -p"${MYSQL_ROOT_PASSWORD}" <<SQL
CREATE USER IF NOT EXISTS 'cc_migrator'@'%' IDENTIFIED BY '${CC_DB_MIGRATOR_PASSWORD}';
CREATE USER IF NOT EXISTS 'cc_app'@'%' IDENTIFIED BY '${CC_DB_APP_PASSWORD}';
GRANT ALL PRIVILEGES ON \`${MYSQL_DATABASE}\`.* TO 'cc_migrator'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;
SQL
