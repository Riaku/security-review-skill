# data

Databases, replication, distributed data, queues, async pipelines, and data/ETL platforms.

Index: [SKILL.md](../SKILL.md)

Detection signals:
- Migration directories (alembic, flyway, prisma, goose, atlas)
- DB clients/drivers in dependencies (postgres, mysql, mongo, redis clients)
- Queue clients (kafka, rabbitmq, sqs, celery, sidekiq, bull)
- CDC/streaming tooling (debezium, flink)
- Data-pipeline tooling (airflow/ dags/ dir, dbt projects, spark jobs, glue, dataflow)

Categories:
- [database](../categories/database.md)
- [distributed-systems](../categories/distributed-systems.md)
- [messaging-async](../categories/messaging-async.md)
- [data-pipelines](../categories/data-pipelines.md)

## Stack quick-map

- Any SQL-backed service → [database](../categories/database.md)
- Queues/workers present → [messaging-async](../categories/messaging-async.md)
- Multiple datastores or replication/sharding configured → [distributed-systems](../categories/distributed-systems.md)
