# Hutch-Bunny Query Generation Docs

## Query Generation in Hutch-Bunny

### Overview

The query generation process in Hutch-bunny is a sophisticated system that transforms high-level query descriptions into efficient SQL queries. Rather than accepting raw SQL from users, which could introduce security risks and inconsistencies, the system uses a structured approach to generate optimized queries that work with the OMOP Common Data Model (CDM).

### Core Components

#### Domain Mapping System

The system uses several mapping dictionaries that serve as the foundation for query generation. These mappings ensure that queries are constructed correctly for the OMOP CDM schema:

```python
concept_table_map = {
    "Condition": ConditionOccurrence,
    "Drug": DrugExposure,
    "Gender": Person,
    "Race": Person,
    "Ethnicity": Person,
    "Measurement": Measurement,
    "Observation": Observation,
    "Procedure": ProcedureOccurrence
}
```

This mapping connects high-level medical domains to their corresponding database tables. For instance, when a query mentions "Drug", the system knows to look in the DrugExposure table.

Similarly, the concept ID mapping connects domains to their specific identifier columns:

```python
domain_concept_id_map = {
    "Condition": ConditionOccurrence.condition_concept_id,
    "Drug": DrugExposure.drug_concept_id,
    "Gender": Person.gender_concept_id,
    "Race": Person.race_concept_id,
    "Ethnicity": Person.ethnicity_concept_id
}
```

#### Query Building Process

The query generation process happens in several stages, each building upon the previous one:

##### 1\. Concept Resolution

Before building the main query, the system needs to resolve any concept IDs mentioned in the query. This happens through a concept lookup query:

```python
def _find_concepts(self):
    """
    Resolves concept IDs to their domains by querying the Concept table.
    Returns a dictionary mapping concept IDs to their domains.
    """
    concept_query = (
        select(Concept.concept_id, Concept.domain_id)
        .where(Concept.concept_id.in_(self.concept_ids))
        .distinct()
    )
    
    # Execute query and create mapping
    with self.db_manager.engine.connect() as connection:
        concepts = connection.execute(concept_query).fetchall()
        return {c.concept_id: c.domain_id for c in concepts}
```

This step ensures that we know which table each concept belongs to before constructing the main query.

##### 2\. Rule Query Construction

Individual rules within a query are transformed into SQL conditions. The system handles different types of rules:

```python
def _build_rule_query(self, rule, concept_domain):
    """
    Constructs a query for a single rule based on its type and operator.
    """
    concept_table = self.concept_table_map[concept_domain]
    concept_col = self.domain_concept_id_map[concept_domain]
    
    if rule.type_ == "numeric":
        # Handle numeric range queries
        return (
            select(concept_table.person_id)
            .where(
                and_(
                    concept_col == int(rule.value),
                    self._get_numeric_column(rule).between(
                        rule.min_value, 
                        rule.max_value
                    )
                )
            )
            .distinct()
        )
    else:
        # Handle equality-based queries
        operator_map = {"=": "__eq__", "!=": "__ne__"}
        operator_func = getattr(concept_col, operator_map[rule.operator])
        return (
            select(concept_table.person_id)
            .where(operator_func(int(rule.value)))
            .distinct()
        )
```

##### 3\. Group Query Assembly

Rules are combined into groups based on logical operators:

```python
def _build_group_query(self, group, concepts):
    """
    Combines multiple rule queries into a group based on AND/OR logic.
    """
    rule_queries =
    for rule in group.rules:
        domain = concepts[int(rule.value)]
        rule_query = self._build_rule_query(rule, domain)
        rule_queries.append(rule_query)
    
    if group.rules_operator == "AND":
        # Intersect all rule results
        return self._intersect_queries(rule_queries)
    else:
        # Union all rule results
        return self._union_queries(rule_queries)
```

##### 4\. Distribution Query Generation

For distribution queries, the system generates aggregation queries that calculate frequencies and statistics:

```python
def _build_distribution_query(self, domain):
    """
    Generates a query to calculate the distribution of values in a domain.
    """
    table = self.allowed_domains_map[domain]
    concept_col = self.domain_concept_id_map[domain]
    
    return (
        select([
            func.count(table.person_id).label('count'),
            concept_col.label('concept_id'),
            Concept.concept_name,
            Concept.domain_id
        ])
        .join(
            Concept,
            concept_col == Concept.concept_id
        )
        .group_by(
            concept_col,
            Concept.concept_name,
            Concept.domain_id
        )
    )
```

#### Query Optimization Features

The system incorporates several optimization techniques:

1. **Distinct Selection**: Uses `distinct()` to eliminate duplicate patient IDs early in the query process.

2. **Efficient Joins**: Leverages SQLAlchemy's join optimization for concept lookups:

```python
def _optimize_joins(self, query, domain):
    """
    Applies join optimizations based on the domain and query structure.
    """
    if domain in self.requires_concept_join:
        query = query.join(
            Concept,
            self.domain_concept_id_map[domain] == Concept.concept_id,
            isouter=False  # Use inner join for better performance
        )
    return query
```

1. **Result Caching**: Implements caching for frequently used concept lookups:

```python
@lru_cache(maxsize=1000)
def _get_concept_info(self, concept_id):
    """
    Caches concept information to avoid repeated database lookups.
    """
    query = select(Concept).where(Concept.concept_id == concept_id)
    return self.db_manager.engine.execute(query).first()
```

#### Error Handling and Validation

The query generation system includes robust error handling:

```python
def _validate_query(self, query):
    """
    Validates query structure and parameters before processing.
    """
    if not query.cohort.groups:
        raise ValueError("Query must contain at least one group")
    
    for group in query.cohort.groups:
        if not group.rules:
            raise ValueError("Each group must contain at least one rule")
        
        for rule in group.rules:
            if not self._is_valid_rule(rule):
                raise ValueError(f"Invalid rule configuration: {rule}")
```

### Example Query Flow

Let's follow a complete example of how a query flows through the system:

1. Initial Query Description:

```python
query = {
    "cohort": {
        "groups":
            "rules":
                "varname": "gender",
                "value": "8507",  # Concept ID for 'Female'
                "operator": "="
            }],
            "rules_operator": "AND"
        }],
        "groups_operator": "AND"
    }
}
```

1. Generated SQL (simplified):

```sql
WITH female_patients AS (
    SELECT DISTINCT person_id
    FROM person
    WHERE gender_concept_id = 8507
)
SELECT COUNT(DISTINCT person_id)
FROM female_patients;
```

This query would be automatically optimized by SQLAlchemy and executed efficiently against the database.

### Performance Considerations

The query generation system incorporates several performance optimizations:

1. Early Filtering: Applies filters at the database level rather than in application code

2. Efficient Join Ordering: Uses SQLAlchemy's query optimizer to determine the most efficient join order

3. Index Usage: Generates queries that can utilize database indexes effectively

4. Connection Pooling: Uses SQLAlchemy's connection pool to manage database connections efficiently

### Integration with Data Protection

The query generation system works in concert with the data protection features:

```python
def _apply_protection(self, query):
    """
    Modifies queries to respect data protection rules.
    """
    if self.requires_protection:
        # Add HAVING clause for low number suppression
        query = query.having(func.count(distinct(Person.person_id)) > 
                           self.suppression_threshold)
    return query
```

This ensures that privacy protections are applied at the database level, making them more efficient and harder to circumvent.