# The_specific_OMOP_CDM_tables

The specific OMOP CDM tables targeted by Hutch-bunny's availability and distribution queries are determined by the `allowed_domains_map` variable found in the `core/query_solvers.py` file.

Looking at the code, the following OMOP CDM tables are included in this mapping:

- **`Person`:** Used for demographic information like gender, race, and ethnicity.

- **`ConditionOccurrence`:** Stores data about patient conditions.

- **`DrugExposure`:** Contains information about drug exposures for patients.

- **`Measurement`:** Records patient measurements like blood pressure or lab results.

- **`Observation`:** Captures clinical observations about a patient.

- **`ProcedureOccurrence`:** Logs procedures performed on patients.

Both availability and distribution queries use this mapping to determine the appropriate tables to query based on the domain specified in the query.

Based on the codebase analysis, I can provide a comprehensive overview of the OMOP CDM tables targeted by Hutch-bunny's availability and distribution queries:

Core Tables Used:

1. **Person** (`person`)

   - Used for demographic information

   - Contains gender, race, ethnicity data

   - Primary source for demographic distribution queries

2. **Condition** (`condition_occurrence`)

   - Stores patient conditions/diagnoses

   - Used for condition-based queries

   - Tracks condition start/end dates

3. **Drug** (`drug_exposure`)

   - Records medication exposures

   - Includes drug start/end dates

   - Used for medication-related queries

4. **Measurement** (`measurement`)

   - Contains clinical measurements

   - Supports numeric value queries

   - Used for lab results and other quantitative data

5. **Observation** (`observation`)

   - Stores clinical observations

   - Supports both numeric and categorical values

   - Used for various clinical findings

6. **Procedure** (`procedure_occurrence`)

   - Records medical procedures

   - Used for procedure-based queries

7. **Concept** (`concept`)

   - Core reference table

   - Maps all standardized concepts

   - Used across all other tables for concept lookups

The tables are used differently depending on the query type:

**Availability Queries**:

- Use all tables based on the domain of the query

- Support boolean (has/doesn't have) and numeric range queries

- Can combine data from multiple tables using AND/OR logic

**Distribution Queries**:
Two types:

1. Code Distribution:

   - Uses all tables based on the `allowed_domains_map`

   - Counts occurrences of concepts across all domains

2. Demographics Distribution:

   - Primarily uses the `Person` table

   - Currently focused on gender distribution

   - Can be extended for race and ethnicity distributions

The system uses SQLAlchemy for database interactions and supports complex queries across these tables while maintaining OMOP CDM's standardized structure.

The `CodeDistributionQuerySolver` and `DemographicsDistributionQuerySolver` target specific data points based on the OMOP CDM structure and predefined categories within the `allowed_domains_map` variable located in

**CodeDistributionQuerySolver:**

- It targets **concept IDs** within the following predefined medical domains:

   - Condition

   - Ethnicity

   - Drug

   - Gender

   - Race

   - Measurement

   - Observation

   - Procedure

- For each concept ID within these domains, it calculates the frequency (count) of occurrences.

**DemographicsDistributionQuerySolver:**

- Currently, it primarily focuses on the **Gender** domain.

- It calculates the count of patients for each gender category.

**Custom Queries:**

Currently, the code doesn't support user-defined custom queries for these solvers. They rely on the predefined domain-to-table mapping in `allowed_domains_map`. However, the system does include a `CustomQuerySolver` class, suggesting the possibility for future development to allow more flexible, user-defined queries.