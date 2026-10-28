# data

Databases, replication, distributed data, queues, async pipelines, and data/ETL platforms.

## Detection signals

- Migration directories (alembic, flyway, prisma, goose, atlas)
- DB clients/drivers in dependencies (postgres, mysql, mongo, redis clients)
- Queue clients (kafka, rabbitmq, sqs, celery, sidekiq, bull)
- CDC/streaming tooling (debezium, flink)
- Data-pipeline tooling (airflow/ dags/ dir, dbt projects, spark jobs, glue, dataflow)

## Stack quick-map

- Any SQL-backed service → database
- Queues/workers present → messaging-async
- Multiple datastores or replication/sharding configured → distributed-systems
- ETL/ELT jobs, dbt models or a warehouse load → data-pipelines
- Warehouse or lake holds personal data → compliance-privacy
