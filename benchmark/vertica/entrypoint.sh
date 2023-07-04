#!/bin/bash

vertica_ready() {
python << END
import sys
import vertica_python
import vertica_python.errors

connection_info = {
    "host": "vertica",
    "port": "5433",
    "user": "dbadmin",
    "database": "docker",
}

try:
    vertica_python.connect(**connection_info)
except vertica_python.errors.ConnectionError:
    sys.exit(-1)
sys.exit(0)

END
}

until vertica_ready; do
  >&2 echo 'Waiting for Vertica to become available...'
  sleep 5
done
>&2 echo 'Vertica is available'

exec "$@"
