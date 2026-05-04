# Relay system

Based on the code and configuration files, I can provide a detailed explanation of the Relay system and its architecture:

## Relay System Architecture

1. **Components**

```yaml
# dev.compose.yml
services:
  relay:
    image: ghcr.io/health-informatics-uon/hutch/relay:dev-latest
    depends_on:
      - rabbitmq
      - db
    ports:
      - 8080:8080  # Main API port
      - 8081:8081  # Management port
```

1. **Message Queue Integration**

```yaml
  rabbitmq:
    image: rabbitmq:3-management
    ports:
      - 5672:5672    # AMQP port
      - 15672:15672  # Management UI
    environment:
      RABBITMQ_DEFAULT_USER: user
      RABBITMQ_DEFAULT_PASS: password
```

1. **Communication Pattern**

```python
# src/hutch_bunny/daemon.py
def main():
    # 1. Poll for new jobs
    polling_endpoint = f"task/nextjob/{settings.COLLECTION_ID}"
    while True:
        response = client.get(endpoint=polling_endpoint)
        if response.status_code == 200:
            # 2. Process job
            result = execute_query(query_dict, results_modifiers_list, logger, db_manager)
            
            # 3. Return results
            return_endpoint = f"task/result/{result.uuid}/{result.collection_id}"
            for _ in range(4):  # Retry logic
                response = client.post(endpoint=return_endpoint, data=result.to_dict())
```

## Scaling Architecture

1. **Distributed Query Processing**

- Each Hutch-bunny instance connects to its own OMOP database

- Relay coordinates queries across multiple instances

- Results are aggregated through the Task API

1. **Configuration Options**

```yaml
environment:
  # Relay Connection
  TASK_API_BASE_URL: http://relay:8080/
  TASK_API_USERNAME: username
  TASK_API_PASSWORD: password
  
  # Query Processing
  COLLECTION_ID: collection_id
  TASK_API_TYPE: a  # Supports different API versions
  POLLING_INTERVAL: 5
```

1. **Security and Authentication**

```python
# src/hutch_bunny/core/task_api_client.py
class TaskApiClient:
    def request(self, method: SupportedMethod, url: str, data: Optional[dict] = None):
        basicAuth = HTTPBasicAuth(self.username, self.password)
        response = requests.request(
            method=method.value, 
            url=url, 
            json=data, 
            auth=basicAuth
        )
```

1. **Result Handling**

```python
# Result formatting and obfuscation
def execute_query(query_dict, results_modifiers, logger, db_manager):
    result = solve_query()
    result.count = apply_filters_v2(result.count, results_modifiers)
    return result
```

## Key Features for Scaling

1. **Asynchronous Processing**

- Poll-based job retrieval

- Non-blocking query execution

- Retry logic for result submission

1. **Load Distribution**

- Multiple Hutch-bunny instances can run in parallel

- Each instance handles its own database connection

- Relay manages job distribution

1. **Fault Tolerance**

```python
# Retry logic for failed submissions
for _ in range(4):
    response = client.post(endpoint=return_endpoint, data=result.to_dict())
    if 200 <= response.status_code < 300:
        break
    time.sleep(5)
```

1. **Configuration Management**

```yaml
# Environment-specific settings
DOTNET_Environment: Development
ConnectionStrings__Default: Server=db;Port=5432;Database=hutch-relay
RelayTaskQueue__ConnectionString: amqp://user:password@rabbitmq:5672
```

1. **Monitoring and Management**

- RabbitMQ management interface (port 15672)

- Relay management API (port 8081)

- Logging and error tracking

This architecture enables:

- Horizontal scaling across multiple databases

- Fault-tolerant query processing

- Secure communication between components

- Flexible deployment options

- Centralized result aggregation

Based on the documentation, I'll explain the end-to-end process of how Relay and Hutch-bunny interact, and the flexibility for researchers:

### End-to-End Process Flow

1. **Network Setup**

- Relay is deployed centrally to create a federated network of subnodes

- Each subnode runs Hutch-bunny locally with access to their OMOP CDM database

- Relay acts as a task distribution and result aggregation hub

1. **Query Flow**

```mermaid
sequenceDiagram
    participant U as Upstream Task API
    participant R as Relay
    participant B as Hutch-bunny Nodes
    participant D as Local OMOP DBs

    U->>R: Send Query
    R->>R: Distribute to Subnodes
    loop For each Subnode
        R->>B: Send Query Task
        B->>D: Execute Query
        D->>B: Return Results
        B->>R: Send Results
        R->>R: Apply Obfuscation
    end
    R->>R: Aggregate Results
    R->>U: Return Combined Results
```

1. **Communication Pattern**

- Hutch-bunny makes only outgoing requests, enabling operation behind firewalls

- Relay polls upstream for tasks and distributes them to subnodes

- Results flow back through the same channels

### Query Types and Flexibility

1. **Query Types**

- **Availability Queries**: Count patients matching specific criteria

- **Distribution Queries**:

   - Demographics distribution (gender, race, ethnicity)

   - Code distribution (conditions, drugs, measurements, etc.)

   - Support for numeric ranges and categorical values

1. **Query Construction**

- Queries can combine multiple rules with AND/OR logic

- Support for:

   - Numeric range queries (e.g., measurement values between min and max)

   - Boolean inclusion/exclusion queries (has/doesn't have condition)

   - Complex nested logic between rules and rule groups

1. **Data Protection**

- Built-in obfuscation methods:

   - Low number suppression (configurable threshold)

   - Result rounding (configurable target)

- Sensitive data remains within local environments

### Researcher Flexibility

1. **Query Building**

- Researchers can create queries targeting:

   - Patient demographics

   - Clinical conditions

   - Medications

   - Lab measurements

   - Procedures

   - Observations

1. **Query Composition**

```json
{
  "cohort": {
    "groups":
      {
        "rules":
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
  }
}
```

1. **Integration Options**

- Can connect directly to:

   - HDR Cohort Discovery tool

   - Other Relay instances

   - Custom task API implementations

- Supports different query types through `TASK_API_TYPE`:

   - Type 'a': Availability queries

   - Type 'b': Distribution and PHEWAS

   - Type 'c': Analytics (GWAS, Quantitative Trait, Burden Test)

1. **Result Formats**

- Standardized result format including:

   - Counts

   - Statistical measures (for distributions)

   - Metadata

   - Status information

The system provides significant flexibility while maintaining:

- Data privacy through local execution

- Standardized query interfaces

- Result obfuscation

- Scalable federation capabilities

This makes it suitable for researchers to conduct multi-site cohort discovery while respecting data governance requirements.