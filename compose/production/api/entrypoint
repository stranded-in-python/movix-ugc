#!/bin/bash

kafka_ready() {
python << END
import sys
import os

import msgpack
from pydantic import BaseSettings
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

class Settings(BaseSettings):
    project_name: str = "movix-events"

    view_event: str = "views"

    kafka_host: str = "broker"
    kafka_port: int = 9092

    base_dir = os.path.dirname(os.path.dirname(__file__))


settings = Settings()

try:
    kafka = KafkaProducer(
            bootstrap_servers=[f"{settings.kafka_host}:{settings.kafka_port}"],
            value_serializer=msgpack.dumps,
        )
except NoBrokersAvailable:
    sys.exit(-1)
sys.exit(0)

END
}

until kafka_ready; do
  >&2 echo 'Waiting for Kafka to become available...'
  sleep 5
done
>&2 echo 'Kafka is available'

exec "$@"
