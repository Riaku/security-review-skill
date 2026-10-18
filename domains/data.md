# data

Databases, replication, distributed data, queues, async pipelines, and data/ETL platforms.

## Detection signals

- Migration directories (alembic, flyway, prisma, goose, atlas)
- DB clients/drivers in dependencies (postgres, mysql, mongo, redis clients)
- Queue clients (kafka, rabbitmq, sqs, celery, sidekiq, bull)
- CDC/streaming tooling (debezium, flink)
- Data-pipeline tooling (airflow/ dags/ dir, dbt projects, spark jobs, glue, dataflow)

## Stack quick-map

- Any SQL-backed service → [database](../categories/database.md)
- Queues/workers present → [messaging-async](../categories/messaging-async.md)
- Multiple datastores or replication/sharding configured → [distributed-systems](../categories/distributed-systems.md)

## Categories

- [api-design](../categories/api-design.md)
- [cloud-network](../categories/cloud-network.md)
- [compliance-privacy](../categories/compliance-privacy.md)
- [correctness-pitfalls](../categories/correctness-pitfalls.md)
- [data-pipelines](../categories/data-pipelines.md)
- [database](../categories/database.md)
- [deployment-release](../categories/deployment-release.md)
- [distributed-systems](../categories/distributed-systems.md)
- [hardening-benchmarks](../categories/hardening-benchmarks.md)
- [messaging-async](../categories/messaging-async.md)
- [multi-tenancy](../categories/multi-tenancy.md)
- [observability](../categories/observability.md)
- [payments-fraud](../categories/payments-fraud.md)
- [resilience](../categories/resilience.md)
- [scaling-capacity](../categories/scaling-capacity.md)
- [secrets-crypto](../categories/secrets-crypto.md)
- [sre-incidents](../categories/sre-incidents.md)
- [web-api-security](../categories/web-api-security.md)

Index: [SKILL.md](../SKILL.md)
