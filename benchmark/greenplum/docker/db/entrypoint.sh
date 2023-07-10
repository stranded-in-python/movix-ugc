#!/bin/bash

set -e

/etc/init.d/ssh start
sleep 1
su - gpadmin bash -c 'gpstart -a'

trap "kill %1; su - gpadmin bash -c 'gpstop -a -M fast' && END=1" INT TERM

tail -f "$(ls /data/master/gpsne-1/pg_log/gpdb-* | tail -n1)" &

# Wait for Greenplum to start
until su - gpadmin bash -c 'psql -d postgres -c "SELECT 1;"' &>/dev/null; do
  sleep 1
done

# Create the 'test' database
su - gpadmin bash -c 'psql -d postgres -c "CREATE DATABASE test;"'

# Trap
while [ "$END" == '' ]; do
  sleep 1
done
