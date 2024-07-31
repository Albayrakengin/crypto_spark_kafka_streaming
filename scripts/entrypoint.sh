#!/bin/bash
set -e

# Ensure that all necessary environment variables are set
: "${AIRFLOW_USERNAME:?Need to set AIRFLOW_USERNAME}"
: "${AIRFLOW_FIRSTNAME:?Need to set AIRFLOW_FIRSTNAME}"
: "${AIRFLOW_LASTNAME:?Need to set AIRFLOW_LASTNAME}"
: "${AIRFLOW_ROLE:?Need to set AIRFLOW_ROLE}"
: "${AIRFLOW_EMAIL:?Need to set AIRFLOW_EMAIL}"
: "${AIRFLOW_PASSWORD:?Need to set AIRFLOW_PASSWORD}"

if [ -e "/opt/airflow/requirements.txt" ]; then
  $(command -v pip) install --user -r /opt/airflow/requirements.txt
fi

# Initialize the database and create the Airflow user if the database does not exist
if [ ! -f "/opt/airflow/airflow.db" ]; then
  $(command -v airflow) db init
  $(command -v airflow) users create \
    --username "${AIRFLOW_USERNAME}" \
    --firstname "${AIRFLOW_FIRSTNAME}" \
    --lastname "${AIRFLOW_LASTNAME}" \
    --role "${AIRFLOW_ROLE}" \
    --email "${AIRFLOW_EMAIL}" \
    --password "${AIRFLOW_PASSWORD}"
fi

$(command -v airflow) db upgrade

exec $(command -v airflow) webserver
