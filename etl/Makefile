ch-init:
	docker cp ./clickhouse/init.sh clickhouse:/home/
	docker cp ./clickhouse/table.sql clickhouse:/home/
	docker exec -it clickhouse chmod +x /home/init.sh
	docker exec --user clickhouse -it clickhouse /bin/bash -c "/home/init.sh"
	docker exec --user clickhouse -it clickhouse clickhouse-client --queries-file /home/table.sql

start:
	docker-compose --env-file ./.env.example up -d --no-deps --build
