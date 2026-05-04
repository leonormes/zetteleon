## Hutch-Bunny System Documentation

### Overview

Hutch-bunny is an HDR UK (Health Data Research UK) Cohort Discovery Task Resolver designed to fetch and resolve Availability and Distribution Queries against OMOP-CDM (Observational Medical Outcomes Partnership Common Data Model) databases. The system serves as a crucial component in a larger health informatics infrastructure, focusing on cohort discovery and analysis in medical databases.

#### Main Purpose

The system processes and analyzes distributed queries in healthcare data, specifically focusing on:

- Calculating the distribution of medical concepts (conditions, drugs, procedures) across populations

- Providing insights into population health trends

- Supporting researchers and clinicians in making data-driven decisions

- Ensuring privacy and security of sensitive medical data

#### Key Features

The system provides several core capabilities:

1. Query Resolution

   - Processing demographic distribution queries

   - Handling availability queries

   - Working with OMOP-CDM databases

2. Data Processing

   - Supporting result obfuscation for privacy protection

   - Handling query execution and result formatting

   - Returning results in JSON format

3. Database Support

   - Supporting multiple database backends (PostgreSQL, MySQL, SQL Server)

   - Providing configurable database connections

   - Implementing schema-aware operations

### System Architecture

#### Component Overview

The system consists of several key components that work together to process queries and return results:

1. Entry Points

```python
# src/hutch_bunny/cli.py
def main():
    db_manager = setting_database(logger=logger)
    with open(args.body) as body:
        query_dict = json.load(body)
    result = execute_query(query_dict, results_modifier, logger, db_manager)
    save_to_output(result, args.output)

# src/hutch_bunny/daemon.py
def main():
    db_manager = setting_database(logger=logger)
    while True:
        response = client.get(endpoint=polling_endpoint)
        query_dict = response.json()
        result = execute_query(query_dict, results_modifiers_list, logger, db_manager)
```

- CLI Interface (`bunny`): Processes manual query submissions through `src/hutch_bunny/cli.py`

- Daemon Mode (`bunny-daemon`): Handles continuous operation and polling for new queries

1. Query Processing Components

   - Query Solver Factory: Determines query type and selects appropriate solver

   - Availability Query Solver: Processes availability queries

   - Distribution Query Solver: Handles distribution queries

   - OMOP CDM Database: Stores healthcare data in standardized format

```python
# src/hutch_bunny/core/query_solvers.py
def _get_distribution_solver(db_manager: SyncDBManager, query: DistributionQuery):
    if query.code == DistributionQueryType.GENERIC:
        return CodeDistributionQuerySolver(db_manager, query)
    if query.code == DistributionQueryType.DEMOGRAPHICS:
        return DemographicsDistributionQuerySolver(db_manager, query)
```

1. External Integration

   - Relay: Acts as message broker between Hutch-bunny and Task API

   - Task API: Provides interface to wider Hutch ecosystem

#### Technical Stack

Configuration example:

```yaml
# dev.compose.yml
services:
  bunny:
    build:
      context: .
      dockerfile: Dockerfile
    environment:
      DATASOURCE_DB_USERNAME: postgres
      DATASOURCE_DB_PASSWORD: postgres
      DATASOURCE_DB_DATABASE: hutch-omop
      DATASOURCE_DB_SCHEMA: public
      DATASOURCE_DB_PORT: 5432
      DATASOURCE_DB_HOST: db
```

The system is built using:

- Python 3.13+

- Key Dependencies:

   - numpy, pandas for data processing

   - SQLAlchemy for database operations

   - psycopg for PostgreSQL

   - trino for distributed SQL queries

### Query Processing

#### Query Types

The system handles two main types of queries:

1. Availability Queries

   - Determine if data matching specific criteria exists

   - Return counts of matching records

   - Support complex logical combinations of rules

```python
# src/hutch_bunny/core/rquest_dto/query.py
class AvailabilityQuery(BaseDto):
    def __init__(
        self,
        cohort: Cohort,
        uuid: str,
        owner: str,
        collection: str,
        protocol_version: str,
        char_salt: str,
    ):
        self.cohort = cohort
        self.uuid = uuid
        self.owner = owner
        self.collection = collection
        self.protocol_version = protocol_version
        self.char_salt = char_salt
```

1. Distribution Queries

   - Calculate distribution of medical concepts

   - Provide detailed statistical analysis

   - Support demographic analysis

```python
# src/hutch_bunny/core/rquest_dto/query.py
class DistributionQuery(BaseDto):
    def __init__(
        self,
        owner: str,
        code: DistributionQueryType,
        analysis: str,
        uuid: str,
        collection: str,
    ):
        self.owner = owner
        self.code = code
        self.analysis = analysis
        self.uuid = uuid
        self.collection = collection
```

#### Query Lifecycle

1. Query Reception and Processing

```python
# src/hutch_bunny/core/execute_query.py
def execute_query(query_dict, results_modifiers, logger, db_manager):
    if "analysis" in query_dict:
        query = DistributionQuery.from_dict(query_dict)
        result = query_solvers.solve_distribution(db_manager, query)
    else:
        query = AvailabilityQuery.from_dict(query_dict)
        result = query_solvers.solve_availability(db_manager, query)
        result.count = apply_filters_v2(result.count, results_modifiers)
    return result
```

1. Query Reception

   - Queries received via CLI or daemon

   - Daemon continuously polls Relay system

   - Queries parsed into appropriate DTO objects

2. Query Processing

   - Query type determined by presence of "analysis" key

   - Appropriate solver selected and instantiated

   - SQL queries generated using SQLAlchemy

   - Results retrieved and processed

3. Result Handling

   - Results packaged into RquestResult object

   - Obfuscation applied if necessary

   - Results transmitted back to Relay system

#### Data Protection

The system implements several data protection measures:

1. Low Number Suppression

   - Suppresses counts below configurable threshold

   - Prevents identification of small groups

   - Returns zero for suppressed values

2. Rounding

   - Rounds values to nearest base number

   - Configurable rounding interval

   - Applied after suppression if necessary

```python
# src/hutch_bunny/core/obfuscation.py
def low_number_suppression(value: Union[int, float], threshold: int = 10):
    """Suppress values that fall below a given threshold."""
    return value if value > threshold else 0

def rounding(value: Union[int, float], nearest: int = 10):
    """Round the value to the nearest base number."""
    return nearest * round(value / nearest)

def apply_filters_v2(value: Union[int, float], filters: list):
    actions = {
        "Low Number Suppression": low_number_suppression,
        "Rounding": rounding
    }
    result = value
    for f in filters:
        if action := actions.get(f.pop("id", None)):
            result = action(result, **f)
            if result == 0:
                break
    return result
```

### Database Integration

#### OMOP CDM Schema

```python
# src/hutch_bunny/core/entities.py
class Person(Base):
    __tablename__ = "person"
    person_id = Column(Integer, primary_key=True)
    gender_concept_id = Column(Integer, ForeignKey("concept.concept_id"))
    year_of_birth = Column(Integer, nullable=False)
    race_concept_id = Column(Integer, ForeignKey("concept.concept_id"))
    ethnicity_concept_id = Column(Integer, ForeignKey("concept.concept_id"))

class Concept(Base):
    __tablename__ = "concept"
    concept_id = Column(Integer, primary_key=True)
    concept_name = Column(String(255), nullable=False)
    domain_id = Column(String(20), nullable=False)
```

The system uses SQLAlchemy ORM models mapping to OMOP CDM tables:

- Person: Demographics and basic patient information

- Concept: Medical concepts and terminology

- ConditionOccurrence: Patient conditions and diagnoses

- DrugExposure: Medication information

- Measurement: Clinical measurements

- Observation: Clinical observations

- ProcedureOccurrence: Medical procedures

#### Query Generation

```python
# src/hutch_bunny/core/query_solvers.py
class CodeDistributionQuerySolver:
    allowed_domains_map = {
        "Condition": ConditionOccurrence,
        "Drug": DrugExposure,
        "Gender": Person,
    }
    
    def solve_query(self):
        stmnt = select(
            func.count(table.person_id), 
            concept_col
        ).group_by(concept_col)
        
        df = pd.read_sql_query(
            sql=stmnt,
            con=self.db_manager.engine.connect()
        )
```

SQL queries are generated dynamically using:

1. Domain Mapping: Connects medical domains to database tables

2. SQLAlchemy ORM: Provides type-safe query building

3. Optimization Features: Includes distinct selections and efficient joins

### Development and Deployment

#### Testing

The test suite covers:

- Database connectivity

- Query processing

- Result obfuscation

- Error handling

- Edge cases

```python
# tests/test_return.py
def test_solve_availability_returns_result(availability_result):
    assert isinstance(availability_result, RquestResult)

def test_solve_availability_is_ok(availability_result):
    assert availability_result.status == "ok"

def test_solve_availability_count_matches(availability_result, availability_example):
    assert availability_result.count == availability_example.count
```

#### Deployment Options

The system supports:

- Docker deployment (includes Dockerfile)

- Container image distribution

- MIT Licensed operation

- Flexible configuration through environment variables

#### Security Considerations

Security measures include:

- Result obfuscation for privacy

- SQLAlchemy's SQL injection protection

- Secure communication with Relay

- Support for institutional firewalls

### Integration Points

#### Relay Communication

Results are returned to Relay using:

- HTTP POST requests

- JSON-formatted response bodies

- Retry logic for failed transmissions

- Standard endpoint structure

```python
# src/hutch_bunny/daemon.py
def main():
    # … setup code …
    
    return_endpoint = f"task/result/{result.uuid}/{result.collection_id}"
    
    # Send results with retry logic
    for _ in range(4):
        response = client.post(
            endpoint=return_endpoint, 
            data=result.to_dict()
        )
        if 200 <= response.status_code < 300:
            break
        time.sleep(5)
```

#### Task API Integration

The system integrates with:

- HDR Cohort Discovery tool

- Hutch Relay for federated networks

- Other compatible Task APIs