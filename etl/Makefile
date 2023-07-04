ch-create-table:
	docker cp ./clickhouse/table.sql clickhouse:/home/
	docker exec --user clickhouse -it clickhouse clickhouse-client --queries-file /home/table.sql