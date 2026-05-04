# DDD

## Core Domain

Hutch-bunny's core domain is Cohort Discovery - the process of analyzing patient populations in clinical databases to identify groups matching specific criteria while maintaining data privacy and standardization.

## Bounded Contexts

1. Query Processing Context

   - Handles the interpretation and execution of queries

   - Manages query validation and transformation

   - Interfaces with the OMOP database

2. Clinical Data Context

   - Manages the OMOP CDM data model

   - Handles standardized medical concepts

   - Deals with patient records and clinical events

3. Results Management Context

   - Handles query results processing

   - Manages data obfuscation and privacy

   - Formats and returns results

4. Integration Context

   - Manages communication with external systems

   - Handles task queuing and processing

   - Deals with authentication and authorization

## Ubiquitous Language

### Query Concepts

- Availability Query: A query that determines the number of patients matching specific criteria

- Distribution Query: A query that analyzes how values or characteristics are distributed across a patient population

- Query Solver: Component responsible for executing queries and producing results

- Rule: A specific criterion in a query (e.g., age range, diagnosis)

- Rule Group: A collection of rules combined with logical operators (AND/OR)

### Clinical Concepts

- Concept: A standardized medical term in the OMOP vocabulary (e.g., conditions, drugs, measurements)

- Domain: A category of medical data (e.g., Condition, Drug, Measurement)

- Person: A patient record with demographic information

- Observation: A clinical finding or measurement

- Condition Occurrence: An instance of a medical condition

- Drug Exposure: A record of medication administration

- Procedure Occurrence: A medical procedure record

### Result Concepts

- RquestResult: The standardized format for query results

- File: A container for result data with metadata

- Obfuscation: Process of protecting patient privacy in results

- Distribution Type: Category of distribution analysis (Demographics or Generic)

### Integration Concepts

- Task API: Interface for receiving and responding to query requests

- Collection: A grouping of data sources or results

- Biobank: A source of clinical data

- Relay: System for distributing queries and collecting results

### Technical Terms

- OMOP CDM: Observational Medical Outcomes Partnership Common Data Model. A standardized data model for healthcare data used to facilitate data sharing and analysis.

- Concept ID: Unique identifier for standardized medical concepts

- Source Value: Original value before standardization

- Source Concept: Original concept before mapping to standard

## Value Objects

- Query DTOs: Data transfer objects for queries

- Result DTOs: Standardized result formats

- Concept Mappings: Relationships between concepts and domains

## Entities

- Person: Core entity representing a patient

- Concept: Standardized medical terminology

- Clinical Events: Various medical occurrences (conditions, drugs, procedures)

## Services

- Query Solvers: Services that process different types of queries

- Database Manager: Handles database connections and operations

- Task API Client: Manages communication with external systems

## Glossary

- OMOP CDM: Observational Medical Outcomes Partnership Common Data Model.

- Cohort Discovery: The process of identifying groups of patients within a database who share specific characteristics. This is a core function of Hutch-bunny.

- Availability Query: A query that checks whether data matching certain criteria exists in the database.

- Distribution Query: A query that analyzes the distribution of medical concepts or demographic factors within a patient population.

- Query Solver: A component responsible for processing and executing a specific type of query (e.g., `AvailabilityQuerySolver`, `CodeDistributionQuerySolver`).

- Concept: A standardized medical entity in the OMOP CDM (e.g., a diagnosis, medication, or demographic attribute).

- Concept ID: A unique identifier for a specific concept within the OMOP CDM.

- Relay: A system that acts as a message broker, distributing queries to Hutch-bunny and collecting the results.

- Task API: The interface used by Hutch-bunny to communicate with the wider Hutch ecosystem, including the Relay system.

- Obfuscation: The process of applying data protection measures to query results to protect patient privacy (e.g., low number suppression, rounding).

- Low Number Suppression: A data protection technique that suppresses results below a certain threshold to prevent the identification of small groups or individuals.

- Rounding: A data protection technique that rounds results to a specific interval to further enhance privacy.

## Domain-Driven Design Analysis

Core Domain:

- Cohort Discovery: Hutch-bunny's core value proposition lies in its ability to perform cohort discovery within large medical datasets. This involves efficiently processing and analyzing queries related to the distribution of medical concepts and demographic data across patient populations.

Bounded Contexts:

- Query Processing: Encapsulates the logic for receiving, parsing, validating, and executing queries. Includes Query Solver classes, the Query Solver Factory, and the logic for constructing SQL queries.

- Data Access: Handles the interaction with the OMOP CDM database. Includes the database connection management, SQLAlchemy models, and data retrieval operations.

- Data Protection: Focuses on applying obfuscation techniques to query results to ensure patient privacy. Includes filters for low number suppression, rounding, and any other privacy-enhancing methods.

- Relay Integration: Manages the communication with the Relay system, sending queries and receiving results.