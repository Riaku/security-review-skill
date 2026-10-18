# data

Databases, replication, distributed data, queues and async pipelines.

Detection signals:
- Migration directories (alembic, flyway, prisma, goose, atlas)
- DB clients/drivers in dependencies (postgres, mysql, mongo, redis clients)
- Queue clients (kafka, rabbitmq, sqs, celery, sidekiq, bull)
- CDC/streaming tooling (debezium, flink)

Categories:
- `database`
- `distributed-systems`
- `messaging-async`

## Stack quick-map

- Any SQL-backed service → database
- Queues/workers present → messaging-async
- Multiple datastores or replication/sharding configured → distributed-systems
