#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

/usr/local/bin/python /app/main.py
