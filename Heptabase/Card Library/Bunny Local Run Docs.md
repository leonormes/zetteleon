# Bunny Local Run Docs

## Prerequisites

- Docker and Docker Compose

- Python 3.9 or higher

- Poetry package manager

- PostgreSQL 16

## 1\. Directory Structure Setup

```bash
mkdir hutch-dev
cd hutch-dev

# Clone repositories
git clone https://github.com/Health-Informatics-UoN/hutch-bunny.git
git clone https://github.com/Health-Informatics-UoN/hutch.git
```

## 2\. Set Up PostgreSQL Database

First, let's create a PostgreSQL container for our OMOP CDM database:

```bash
docker run -d \
  --name hutch-db \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_DB=hutch-omop \
  -p 5432:5432 \
  postgres:16
```

## 3\. Configure Environment

Create a `.env` file in the `hutch-bunny` directory:

```bash
# Task API Configuration
TASK_API_BASE_URL=http://localhost:8080
TASK_API_USERNAME=username
TASK_API_PASSWORD=password
COLLECTION_ID=dev_collection

# Database Settings
DATASOURCE_DB_USERNAME=postgres
DATASOURCE_DB_PASSWORD=postgres
DATASOURCE_DB_HOST=localhost
DATASOURCE_DB_PORT=5432
DATASOURCE_DB_DATABASE=hutch-omop
DATASOURCE_DB_DRIVERNAME=postgresql
DATASOURCE_DB_SCHEMA=public

# Optional Settings
LOW_NUMBER_SUPPRESSION_THRESHOLD=0
ROUNDING_TARGET=0
POLLING_INTERVAL=5
```

## 4\. Set Up Relay

Navigate to the `hutch` directory and create a `relay.compose.yml`:

```yaml
version: "3.8"
services:
  relay:
    image: ghcr.io/health-informatics-uon/hutch/relay:dev-latest
    ports:
      - "8080:8080"
    environment:
      - ConnectionStrings__Default=Server=localhost;Port=5432;Database=hutch-relay;User Id=postgres;Password=postgres
      - Database__ApplyMigrationsOnStartup=true
      - RelayTaskQueue__ConnectionString=amqp://user:password@rabbitmq:5672
      - UpstreamTaskApi__BaseUrl=https://my-task-api.com
      - UpstreamTaskApi__CollectionId=dev_collection
      - UpstreamTaskApi__Username=username
      - UpstreamTaskApi__Password=password
    depends_on:
      - rabbitmq

  rabbitmq:
    image: rabbitmq:3-management
    ports:
      - "5672:5672"
      - "15672:15672"
    environment:
      - RABBITMQ_DEFAULT_USER=user
      - RABBITMQ_DEFAULT_PASS=password
```

Start Relay:

```bash
docker compose -f relay.compose.yml up -d
```

## 5\. Set Up Hutch-bunny

Navigate to the `hutch-bunny` directory:

```bash
cd ../hutch-bunny

# Install dependencies
poetry install

# Create database tables
poetry run python create_tables.py

# Insert test data
poetry run python insert_test_data.py
```

The test data script will create:

- Required OMOP concept tables

- Gender concepts (Male/Female)

- Race concepts (White)

- Ethnicity concepts (Not Hispanic)

- 6,272 male test persons

- 1,000 female test persons

## 6\. Start Hutch-bunny Daemon

```bash
# Start the bunny daemon
poetry run bunny-daemon
```

You should see output like:

```sh
INFO - Setting up database connection...
INFO - Looking for job...
```

## 7\. Verify Setup

### Test the Database Connection

```bash
poetry run python -c "
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()
engine = create_engine(f'postgresql://{os.getenv(\"DATASOURCE_DB_USERNAME\")}:{os.getenv(\"DATASOURCE_DB_PASSWORD\")}@{os.getenv(\"DATASOURCE_DB_HOST\")}:{os.getenv(\"DATASOURCE_DB_PORT\")}/{os.getenv(\"DATASOURCE_DB_DATABASE\")}')
with engine.connect() as conn:
result = conn.execute('SELECT COUNT(*) FROM person').scalar()
print(f'Number of persons in database: {result}')
"
```

### Run the Test Suite

```bash
poetry run pytest tests/
```

## 8\. Test a Query

Create a file named `test_query.json`:

```json
{
  "task_id": "test-job",
  "project": "test_project",
  "owner": "test_user",
  "cohort": {
    "groups": [
      {
        "rules": [
          {
            "varname": "OMOP",
            "varcat": "Person",
            "type": "TEXT",
            "oper": "=",
            "value": "8507"
          }
        ],
        "rules_oper": "AND"
      }
    ],
    "groups_oper": "OR"
  },
  "collection": "dev_collection",
  "protocol_version": "v2",
  "char_salt": "test",
  "uuid": "test-uuid"
}
```

Run the query using the CLI:

```bash
poetry run bunny-cli --body test_query.json
```

This will create an `output.json` file with the query results.

## Troubleshooting

1. **Database Connection Issues**

   - Verify PostgreSQL is running: `docker ps`

   - Check connection settings in `.env`

   - Ensure ports are not in use

2. **Relay Connection Issues**

   - Check Relay logs: `docker logs hutch-relay`

   - Verify RabbitMQ is running

   - Confirm Task API credentials

3. **Test Data Issues**

- If tests fail, try recreating the database:

```bash
poetry run python insert_test_data.py
```

1. **Common Ports Used**

   - PostgreSQL: 5432

   - Relay: 8080

   - RabbitMQ: 5672 (AMQP), 15672 (Management UI)

## Next Steps

- Access RabbitMQ management interface at `http://localhost:15672` (user/password from compose file)

- Monitor Relay logs for incoming queries

- Explore different query types using the test data

- Modify test data script to add more OMOP concepts and patient records

This setup provides a complete local development environment for testing Hutch-bunny with Relay and dummy OMOP CDM data.