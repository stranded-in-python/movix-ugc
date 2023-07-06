FROM clickhouse/clickhouse-server:latest

COPY ./compose/clickhouse/production/init.sh /home/init.sh
RUN chmod +x /home/init.sh

COPY ./compose/clickhouse/production/table.sql /home/table.sql
RUN chmod +x /home/table.sql

COPY ./compose/clickhouse/production/entrypoint.sh /docker-entrypoint-initdb.d/entrypoint.sh
RUN sed -i 's/\r$//g' /docker-entrypoint-initdb.d/entrypoint.sh
RUN chmod +x /docker-entrypoint-initdb.d/entrypoint.sh

