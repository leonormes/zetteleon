# hutch-bunny_implementation

Based on the sources, the knowledge base includes detailed specifications for a project related to health data harmonization and cohort discovery, focusing on the East of England (EoE) NHS region. There are also technical documents describing the Hutch-bunny project, a cohort discovery task resolver, as well as information on the FITFILE and The Hyve partnership and their proposed solutions.

Now, let's get to your question:

**How does the hutch-bunny implementation meet the EOE requirements?**

The Hutch-bunny project is designed to address core requirements of the EoE project, particularly around data harmonization and cohort discovery within a secure environment. It is an HDR UK (Health Data Research UK) Cohort Discovery Task Resolver. Here's how it aligns with the requirements, based on the documents:

1. **Data Harmonization:**

   - The EoE project requires data from NHS providers to be mapped to the OMOP (Observational Medical Outcomes Partnership) common data model. Hutch-bunny is built to work specifically with OMOP-CDM databases.

   - Hutch-bunny is designed to handle data from various NHS data providers that will be mapped to the OMOP common data model. This involves standardizing data from Electronic Patient Records (EPRs) and other sources to facilitate research. The system can be configured to just enable Cohort Discovery capabilities.

   - The system uses the allowed_domains_map to map medical concept domains to corresponding database tables. This ensures that the system can correctly find the relevant data for queries.

   - Hutch-bunny supports multiple database backends, such as PostgreSQL, MySQL, and SQL Server, which is crucial for connecting to the diverse systems used by NHS providers.

2. **Cohort Discovery:**

   - The EoE project emphasizes the need for tools that support cohort discovery, allowing researchers to explore patient cohorts. Hutch-bunny is explicitly designed as a cohort discovery task resolver, capable of handling availability and distribution queries.

   - The system can fetch queries from various sources including the HDR Cohort Discovery tool and Hutch Relay.

   - The system is capable of handling demographic distribution queries, availability queries, and analytics. These features align with the project's goals of supporting researchers in identifying and accessing patient cohorts for their work.

   - Hutch-bunny can perform federated cohort discovery across multiple NHS data providers. The solution works in a distributed fashion.

   - Hutch-bunny provides mechanisms for suppressing small numbers to protect patient privacy, a key aspect of the EOE requirements. This is an important functionality of the system, as per the information governance guidelines.

3. **Security and Governance:**

   - The EoE project requires the application of the "Five Safes" principles, and Hutch-bunny is designed to operate within the data governance constraints of Trusted Research Environments (TREs) or Secure Data Environments (SDEs).

   - Hutch-bunny includes data obfuscation features like result rounding and low number suppression to protect patient privacy.

   - The system has been built with a modular approach to manage distributed queries, and works within the data governance constraints of TREs or SDEs.

   - The system only makes outgoing requests, which enhances security.

   - Hutch-bunny is designed to manage data in a federated way, meaning that data remains within secure local environments until necessary for the query.

4. **Technical Implementation:**

   - The system supports multiple database drivers, which is needed for integration across various data providers.

   - Hutch-bunny uses SQLAlchemy for database operations, ensuring robust data interaction and query execution.

   - Hutch-bunny provides flexible deployment options, including a daemon service, CLI, and Docker container support, aligning with the EoE project's need for a deployable solution.

5. **Federated analytics:**

   - Hutch supports federated analytics and can be configured to just enable cohort discovery capabilities

**How does it differ from fitfile-hyve?**

While Hutch-bunny is a specific tool for cohort discovery, the FITFILE-Hyve partnership represents a broader solution encompassing data harmonization, de-identification, and linkage in addition to cohort discovery. Here are the key differences based on the sources:

1. **Scope:**

   - **Hutch-bunny:** This is primarily a query resolver designed for cohort discovery and analysis. It handles specific types of queries (availability and distribution) against OMOP databases. It’s a standalone component within the larger Hutch ecosystem.

   - **FITFILE-Hyve:** This is a collaborative solution that aims to provide end-to-end data management, from data extraction and harmonization to de-identification and cohort discovery. It integrates FITFILE's node infrastructure with The Hyve's OMOP software.

2. **Data Handling:**

   - **Hutch-bunny:** It operates on OMOP-CDM databases and focuses on analyzing data in that format. It is not responsible for the initial conversion of data into OMOP.

   - **FITFILE-Hyve:** This partnership includes an ETL (Extract, Transform, Load) pipeline to convert raw data into OMOP format using Hyve’s technology. This involves data profiling, syntactic and semantic mappings, and ensuring data quality. They use open-source tooling developed and maintained by the OHDSI community.

3. **De-identification and Linkage:**

   - **Hutch-bunny:** It includes data obfuscation techniques like low number suppression, but it doesn't handle the initial de-identification or linkage of datasets.

   - **FITFILE-Hyve:** They have specific approaches for de-identification, using both reversible pseudonymization and irreversible anonymization. They also perform linkage of datasets, using either deterministic or probabilistic methods.

4. **Federated Operations:**

   - **Hutch-bunny:** It is designed to work in a federated manner, enabling queries across multiple data sources. It can be part of a federated network, utilizing Hutch Relay.

   - **FITFILE-Hyve:** Their solution uses distributed nodes connected to a central SDE Master node, which coordinates queries. They can receive OMOP and non-OMOP queries and enable cohort exploration.

5. **Integration:**

   - **Hutch-bunny:** Integrates with a relay system and a Task API for communication with the wider Hutch ecosystem. It focuses on the query execution phase, acting as a task resolver.

   - **FITFILE-Hyve:** They will install FITFILE nodes with The Hyve’s OMOP software, meaning the data will be harmonized locally using Hyve’s technology within the FITFILE nodes.

6. **Data Cataloguing:**

   - **Hutch-bunny:** It primarily operates on the data that is already in the OMOP format and relies on a set of pre-defined mappings of domains and database tables. It doesn't explicitly handle data cataloguing or data source profiling.

   - **FITFILE-Hyve:** The Hyve will provide data source profiling using WhiteRabbit, providing information about data structure and contents. They will also generate reports on the OMOP schema, data quality, and transformation processes. FITFILE, in combination with the Hyve's systems, aims to make these Data Catalogues accessible to researchers and data managers.

**In Summary:**

- Hutch-bunny is a focused tool that excels at *executing queries* against OMOP-CDM databases, handling both availability and distribution queries while respecting security and privacy.

- FITFILE-Hyve is a more *comprehensive solution* that takes raw NHS data, converts it to OMOP, de-identifies and links records, and enables cohort discovery. It integrates all the steps from data extraction to results and includes data cataloguing.

In the context of the EoE project, both hutch-bunny and FITFILE-Hyve would have roles to play, where FITFILE-Hyve provides the infrastructure and data handling pipeline and hutch-bunny processes the queries. While hutch-bunny addresses the core requirements for federated cohort discovery, FITFILE-Hyve provides the overall solution for the EoE project.

As a next step, would you like me to provide a summary of the main components of the Hutch-bunny architecture or maybe test your understanding of the differences between Hutch-bunny and FITFILE-Hyve?
Okay, I understand that you'd like a more detailed and thorough explanation of how Hutch-bunny meets the EOE requirements and how it differs from the FITFILE-Hyve solution. I will elaborate on my previous response and provide further reasoning and explanations, referencing the sources as I go.

Let's begin by revisiting the core purpose of the East of England (EoE) project. It seeks to create a robust and secure data-sharing infrastructure across multiple NHS providers to enable researchers to access and analyse patient data effectively while adhering to strict privacy and governance standards. This necessitates a system that not only harmonizes diverse data sources into a common model but also facilitates cohort discovery in a federated manner, and manages de-identification and data access securely.

**Hutch-bunny's Alignment with EOE Requirements**

Hutch-bunny is designed to be a key component within this infrastructure, specifically addressing the *query resolution* aspect. It's a task resolver within the Hutch ecosystem, which means it focuses on fetching, interpreting, and executing queries against OMOP-CDM databases, rather than the full lifecycle of data management. Let’s delve deeper into how it meets the specific needs of the EoE project:

1. **Data Harmonisation and the OMOP CDM:**

   - The EoE project stipulates that data from disparate NHS systems, such as Electronic Patient Records (EPRs), must be transformed into the OMOP Common Data Model (CDM). This standardisation is essential for enabling federated queries across different data sources. Hutch-bunny is explicitly built to work with OMOP-CDM databases. It uses the structure and terminologies of the OMOP CDM as a basis for how it translates user queries into database queries.

   - Hutch-bunny relies on the `allowed_domains_map` to map medical domains (e.g., conditions, procedures) to their corresponding tables within the OMOP schema. This mapping is critical for the system to correctly interpret the meaning of a user query and fetch data from the correct tables. The modular design of Hutch-bunny allows it to easily adapt to the OMOP CDM schema, or even be extended to use other common data models. For example, new solver classes can be created to handle new types of queries or domains.

   - The use of SQLAlchemy for database operations ensures that Hutch-bunny is compatible with a variety of database backends. This is important in the EoE context because different NHS trusts may use different database systems (PostgreSQL, SQL Server, etc.).

2. **Cohort Discovery Capabilities:**

   - The primary goal of the EoE project is to empower researchers to discover cohorts of patients that match their specific research criteria. Hutch-bunny directly supports this requirement by providing functionality to perform both *availability* and *distribution* queries.

   - Availability queries allow researchers to determine if data matching their criteria exist, and return a simple count of records that match. For example, a researcher might use an availability query to see how many patients have a specific diagnosis.

   - Distribution queries enable a more in-depth analysis. These queries allow researchers to see how certain factors are distributed within the patient population. For example, a researcher might use a distribution query to explore the number of patients in different age ranges, or with specific conditions.

   - Hutch-bunny supports a range of query types, such as demographics analysis and PheWAS queries. This functionality helps researchers explore data in different ways and gain insights into the data.

   - Hutch-bunny can receive queries from various task APIs and via a relay system, making it very flexible. This supports the project requirement of a federated query system.

3. **Security and Governance Implementation:**

   - The EoE project mandates strict adherence to data protection principles. This includes requirements for de-identification, access control, and the suppression of small numbers to prevent patient re-identification. Hutch-bunny is designed to be used within Secure Data Environments (SDEs) or Trusted Research Environments (TREs), supporting a secure, federated approach.

   - Hutch-bunny implements data obfuscation features such as result rounding and low number suppression to safeguard patient privacy. Low number suppression ensures that results based on a small number of patients are not exposed. This is critical for maintaining the confidentiality of patient data and is a core requirement for the system.

   - By only making outbound requests and being deployed behind institutional firewalls, Hutch-bunny enhances security. This means that the system initiates communication with the outside world, rather than allowing inbound requests, which reduces attack surfaces.

   - The system enforces data protection, for example, results from distribution queries are marked as `sensitive=True`. This ensures that any system receiving those results knows that they may contain protected data.

4. **Technical and Federated Architecture:**

   - Hutch-bunny uses a modular architecture for handling queries, which makes it extensible and easy to maintain. Each query type has a designated solver class that handles query construction and execution (e.g., `CodeDistributionQuerySolver`, `DemographicsDistributionQuerySolver`).

   - The system's federated nature is achieved by its connection to the Relay system, which acts as a message broker. This allows Hutch-bunny to function in a distributed environment, where each instance is deployed at a different site but can still participate in federated analyses. Multiple instances of Hutch-bunny can operate in parallel, and the Relay system coordinates queries across these instances, helping with load distribution.

   - Hutch-bunny supports both synchronous and asynchronous query execution. This means it can execute queries and return results in real-time or process them in the background.

   - Hutch-bunny has support for various deployment options, such as a daemon service, CLI, and Docker containers. This flexibility is critical for different use cases and environments.

5. **Query Generation:**

   - Instead of accepting raw SQL queries directly, which would create potential security vulnerabilities, Hutch-bunny constructs its own SQL queries based on the structured input it receives. This design maintains data integrity and security by ensuring consistent and valid SQL queries.

   - The system uses mappings from medical domains to database tables to construct SQL queries dynamically. This approach centralises these definitions, which makes the code easier to maintain and extend.

**Differentiating Hutch-bunny from the FITFILE-Hyve Solution**

Now, let’s clarify the differences between Hutch-bunny and the FITFILE-Hyve solution. These differences revolve around their scope, functions, and integration in the context of the EoE project.

1. **Scope and Focus:**

   - **Hutch-bunny:** This is a focused, standalone tool that acts as a *query resolver*. It is designed to execute queries against OMOP-CDM databases and return the results. It is part of a larger ecosystem that manages data harmonisation and security, but does not implement those processes itself. It's like the engine in a car, responsible for generating the power but not for building the car itself. It is a component in a larger ecosystem.

   - **FITFILE-Hyve:** This is a comprehensive solution that provides an end-to-end data pipeline. It includes data extraction, transformation to OMOP, de-identification, and cohort discovery. It’s like a complete car manufacturer, taking raw materials and creating a finished, functional car.

2. **Data Handling and ETL:**

   - **Hutch-bunny:** It operates on data that is *already* in OMOP-CDM format. The system does not perform the initial transformation of raw data.

   - **FITFILE-Hyve:** The FITFILE-Hyve solution provides the full data processing pipeline. It starts with raw data from NHS systems and uses The Hyve's ETL pipeline to transform it into the OMOP format. This includes data profiling, syntactic and semantic mappings, and quality assessment of data. This also involves tools like WhiteRabbit for data source profiling, which helps to identify the structure and contents of the original database.

3. **De-identification and Linkage:**

   - **Hutch-bunny:** While it includes obfuscation techniques like low number suppression, it does not perform the de-identification or linkage of patient data itself.

   - **FITFILE-Hyve:** They have a detailed de-identification process, which is either deterministic (anonymous or pseudo) or probabilistic (pseudo). They use FITFILE-patented methods for deterministic linkage or Bloom Filters for probabilistic linkage. This ensures that the data is de-identified according to information governance rules and guidelines, and can be reliably linked across multiple NHS providers.

4. **Federated Operations:**

   - **Hutch-bunny:** It operates in a federated way by connecting to the Relay system, which facilitates communication between multiple instances deployed in different locations. This enables a distributed architecture, which enhances performance and resilience.

   - **FITFILE-Hyve:** Their solution works by deploying distributed nodes across NHS data providers, with a central SDE Master node that coordinates queries. Each node operates independently, meaning that even if one node is unavailable, the rest of the system will continue to work, ensuring the solution's stability.

5. **Integration and Deployment:**

   - **Hutch-bunny:** Designed to be deployed as a Docker container, meaning it is easily portable and can be deployed across various environments. It integrates with external systems through a Task API and Relay.

   - **FITFILE-Hyve:** They install a FITFILE node with The Hyve’s OMOP software at each NHS provider. The data is harmonized locally within these FITFILE nodes using Hyve's technology. This approach ensures data remains within secure environments and is only exposed when necessary for the query.

6. **Data Cataloguing and Metadata:**

   - **Hutch-bunny:** It relies on predefined mappings and does not include explicit functionality for data cataloguing or metadata management.

   - **FITFILE-Hyve:** Their solution aims to expose data attributes and types via a Data Catalogue and Dictionary. This includes creating reports on the OMOP data schema, the pre-OMOP schema, data quality reports, and transformation processes. This enables the National Portal to display available data to researchers to support their query creation.

7. **Scaling:**

   - **Hutch-bunny:** It does not have any explicit mechanisms for scaling itself. It is assumed that any needed scaling for query processing will be handled by the external Relay system or Task APIs.

   - **FITFILE-Hyve:** Their system is based on a cloud-agnostic platform that scales horizontally and vertically. This system architecture includes features like Kubernetes-based orchestration for containerized applications and Terraform for infrastructure management.

**Summarising the Differences**

To recap, Hutch-bunny is a component focused on *query execution* against data already converted into the OMOP format, while FITFILE-Hyve provides the *end-to-end data management solution* from raw data to cohort discovery and including de-identification, data linkage and cataloguing..

Hutch-bunny is analogous to an engine – it takes structured instructions (queries), performs the work (executes SQL against the database), and produces results (aggregated counts or distributions). FITFILE-Hyve is analogous to the entire car manufacturer - it takes raw materials (data from different sources), converts it into a usable format (OMOP CDM), adds all the necessary components (de-identification, linkage), and creates a functioning whole (cohort discovery).

Within the EoE project, Hutch-bunny would be used to query the OMOP data produced by the FITFILE-Hyve pipeline. This pipeline is responsible for extracting, transforming, and loading data from various NHS data providers into a harmonized, de-identified, and linked form, while Hutch-bunny executes researcher queries against this prepared data.

I hope that this detailed explanation has clarified the roles of Hutch-bunny and the FITFILE-Hyve partnership in the context of the EoE project.

As a next step, would you like me to provide a more detailed explanation of the Hutch-bunny query lifecycle or perhaps provide an imaginary scenario and ask you how you would respond using your understanding of the system?
Okay, I'd be happy to provide a detailed explanation of the Hutch-bunny query lifecycle, drawing from the provided sources. I can be your expert guide through this information, and I'll make sure to present the material clearly and concisely. I'll also offer suggestions for further exploration at the end.

Before we dive into the specifics, let me briefly summarise how I can help and the nature of the knowledge base you've provided: I am designed to help you navigate and understand the provided documents which cover the Hutch-bunny project and related systems, including the EoE-SDE (East of England Sub-National Secure Data Environment) project. The documents include specifications, meeting notes, code documentation, and design documents, and delve into the technical aspects of data handling, cohort discovery, and system architecture. I can help you with summaries, specific facts, technical details, and procedures. I can also quiz you to check your comprehension of the materials.

Now, let's get into the Hutch-bunny query lifecycle:

**1\. Query Origination and Entry Points**

- Queries can originate from a few different places. They might be submitted manually via the command line interface (CLI) or come from a continuous polling mechanism running as a daemon process.

- The daemon process continuously polls the Relay system for new queries using the Task API Client. The Task API acts as an interface to the wider Hutch ecosystem. The Relay system is a message broker that distributes queries to Hutch-bunny and collects results.

- The CLI (`bunny`) is used for manual query submissions. It takes a query as JSON input, processes it, and can save the results to an output file.

**2\. Query Reception and Initial Processing**

- The daemon sends GET requests through the Task API client until the Task API endpoint sends a job.

- When a query is received (either via the CLI or the daemon), the system first parses the query from its JSON format into a query object. These are Data Transfer Objects (DTOs) that represent the query. The appropriate query class (`AvailabilityQuery` or `DistributionQuery`) is used to parse the query dictionary and create a query object, which validates the received parameters.

**3\. Query Type Determination**

- The system determines the query type based on the presence of an `"analysis"` key within the query.

   - If the `"analysis"` key is absent, it is treated as an **availability query**. An availability query determines whether data matching specific criteria exists and returns a count of matching records.

   - If the `"analysis"` key is present, it is treated as a **distribution query**. A distribution query calculates the distribution of medical concepts and provides detailed statistical analysis, supporting demographic analysis.

**4\. Query Solving**

- The system uses a Query Solver Factory to select the appropriate solver.

- For an *availability query*, the `solve_availability` method creates an `AvailabilityQuerySolver` object and calls its `solve_query` method. This solver constructs and executes SQL queries to count the number of records that match the specified criteria in the OMOP CDM database.

- For a *distribution query*, the `solve_distribution` method determines the correct solver based on the `code` field of the `DistributionQuery`. It then calls the `solve_query` method of the chosen solver.

   - The `CodeDistributionQuerySolver` handles distribution queries that calculate the distribution of data elements across the dataset, such as the distribution of ICD codes across multiple domains.

   - The `DemographicsDistributionQuerySolver` is designed for demographic information such as age and gender distribution. It focuses on calculating and formatting data with alternatives.

- The solvers use SQLAlchemy to generate SQL queries dynamically based on the OMOP CDM schema. They leverage mapping dictionaries like `allowed_domains_map` to identify the correct tables and columns to query in the database.

**5\. Data Retrieval and Processing**

- The selected solver executes the SQL query against the OMOP CDM database using the database manager.

- Data structures such as dictionaries (`allowed_domains_map`, `domain_concept_id_map`, `concept_table_map`) guide the construction of these SQL queries.

- Results are often stored and manipulated using Pandas DataFrames.

- The system uses SQLAlchemy's ORM (Object-Relational Mapping) models, which map directly to the OMOP CDM tables, making queries more structured and maintainable. The specific OMOP tables targeted include `Person`, `ConditionOccurrence`, `DrugExposure`, `Measurement`, `Observation`, and `ProcedureOccurrence`.

**6\. Result Handling and Obfuscation**

- After a query is solved, the results are packaged into an `RquestResult` object. This object contains information like the query ID, status, count (for availability queries), or file information (for distribution queries).

- For availability queries, results may be obfuscated using the `apply_filters_v2` function. This involves applying rules like low number suppression and rounding to protect sensitive data.

   - Low number suppression means that any results below a defined threshold will be suppressed.

   - Rounding means that results are rounded to a specified interval.

- Distribution query results are marked as sensitive.

**7\. Result Transmission**

- The `RquestResult` object is serialized into JSON format.

- The system then sends an HTTP POST request to the Relay system, with the JSON representation of the `RquestResult` as the body of the request.

- The Task API client sends the `RquestResult` back to the Relay system.

**In summary**, the Hutch-bunny query lifecycle involves receiving queries either via a CLI or a daemon, determining the type of query, selecting the appropriate solver, generating and executing SQL against an OMOP CDM database, applying data protection measures, packaging results and finally transmitting the results back to the requesting system via a relay API. The whole process is designed to be efficient and secure.

What would you like to explore next? Would you like me to quiz you on this information to confirm your comprehension or would you like to explore another aspect of the system, perhaps focusing on the specific SQL generation process, or the role of the Relay?
Okay, I'm ready to provide a more detailed explanation of the Hutch-bunny query lifecycle, building upon my previous response and drawing from the wealth of information in our shared knowledge base. I'll aim for thoroughness, clarity, and a bit of extra insight to ensure you have a complete understanding. I'll also maintain my helpful, supportive tone throughout our interaction.

Let's dive deep into the fascinating world of Hutch-bunny's query processing pipeline:

**1\. Query Origination and Entry Points: The Beginning of the Journey**

As I mentioned earlier, queries don't just magically appear; they have origins, and in Hutch-bunny, these are primarily two:

- **Command-Line Interface (CLI) - The Manual Route:** The `bunny` CLI is your go-to tool for direct, hands-on interaction with Hutch-bunny. Think of it like a command prompt for data analysis. It resides in `src/hutch_bunny/cli.py`. Here's a more detailed look:

   - **JSON Input:** The CLI expects queries to be formatted as JSON. This is crucial because JSON's structured nature allows Hutch-bunny to easily understand and process the request.

   - **Local Execution:** The CLI is perfect for testing and development because it lets you execute a single query and see results instantly.

   - **Output Files:** The CLI saves results to an output file, giving you a tangible record of the analysis. This is particularly handy for debugging and sharing results.

   - **Direct Access:** It allows direct interaction with the database and returns results locally, which means it doesn't require a relay system.

   - **No Relay Polling:** This execution path doesn't involve the Relay, making it ideal for local testing or situations where continuous background operations aren't needed.

- **Daemon Process - The Continuous Watchman:** The `bunny-daemon` is the workhorse for ongoing, automated query processing. It is designed to run as a background service. Key points include:

   - **Relay Connection:** The daemon connects to the Relay system (a message broker) using a Task API client. This connection is crucial for fetching queries and sending results. The Relay system distributes queries and gathers results from multiple Hutch-bunny instances.

   - **Continuous Polling:** It continuously polls the Relay system for new jobs, ensuring that no query goes unnoticed. The `POLLING_INTERVAL` variable sets the frequency of checks, usually every 5 seconds.

   - **Automated Operation:** Once a job is received, the daemon automatically processes the query, making it perfect for production environments where continuous analysis is needed.

   - **No User Interface:** Unlike the CLI, the daemon runs in the background and doesn't display results in a terminal. Instead, results are returned to the Relay system.

   - **Production-Ready:** The daemon is designed to be deployed in a containerised environment and integrated into a larger system using environment variables for configuration.

**2\. Query Reception and Initial Processing: Making Sense of the Request**

Once a query has been received, it's not just passed along as a string of text. Hutch-bunny needs to understand the query’s structure. This is where parsing and DTOs come into play:

- **Task API Client Interaction:** The Task API client sends a GET request to the Relay system to check for new queries. It uses environment variables like `TASK_API_BASE_URL`, `TASK_API_USERNAME`, and `TASK_API_PASSWORD` to connect to the Relay. The response from the Task API is a JSON payload that includes a query.

- **JSON Parsing:** Whether the query comes from the CLI or the daemon, the first step is parsing the JSON into a Python dictionary. The JSON object includes information like query type, parameters, and other relevant details.

- **Data Transfer Objects (DTOs):** The parsed dictionary is then converted into a specific DTO, which is a Python class that represents the query. There are two main DTOs for queries `AvailabilityQuery` and `DistributionQuery`. These DTOs are designed to encapsulate the query parameters and provide methods for accessing and validating them.

   - **Structure and Validation:** These DTOs are crucial for data integrity, as they define the expected format of a query. Before further processing, these classes perform validation to ensure the required parameters are present and valid.

**3\. Query Type Determination: Knowing What to Do**

Hutch-bunny needs to know whether it should be simply counting records or calculating distributions. This decision point hinges on the presence (or absence) of the `analysis` key:

- **The `"analysis"` Key:** The presence or absence of this key determines the query type.

   - **Availability Queries (No `"analysis"` Key):** An availability query is like asking "How many?". It's designed to determine whether data matching specific criteria exists within the database. They return a simple count representing how many individuals meet the given conditions.

   - **Distribution Queries (With `"analysis"` Key):** A distribution query is for more nuanced questions. It doesn't just count, it analyses the spread of data. It is designed to calculate the distribution of medical concepts across a population and provides detailed statistical analyses.

**4\. Query Solving: The Heart of the Process**

Here's where the magic happens: SQL queries are crafted and executed, guided by specialized solvers:

- **Query Solver Factory:** Before a query can be solved, the system needs to identify what type of solver is needed. This is the job of the Query Solver Factory. It examines the query type and selects the appropriate class to handle the query. This promotes a modular design and allows adding new query types easily.

- **Availability Query Solver: The Count Master:** The `AvailabilityQuerySolver` is responsible for the 'How many?' type of queries. Here's its workflow:

   - **SQL Construction:** It generates SQL queries based on the parameters in the availability query. This process uses SQLAlchemy to build structured queries, taking advantage of the OMOP CDM's schema.

   - **Database Interaction:** The query is then executed against the OMOP CDM database.

   - **Count Retrieval:** It retrieves the count of matching records, packaging it up for further use.

- **Distribution Query Solvers: The Distribution Experts:** For distribution queries, there are two key players:

   - **`CodeDistributionQuerySolver` - The Generalist:** This solver is used for most distribution analysis requirements. Here’s its breakdown:

      - **Domain-Specific Logic:** It handles the distribution of concept IDs across a range of medical domains like conditions, drugs, measurements, etc..

      - **SQL Generation:** Based on the query and the `allowed_domains_map`, it crafts SQL queries that use `COUNT` and `GROUP BY` operations to gather frequency counts. The queries use the OMOP CDM tables and their standard fields.

      - **Descriptive Statistics (Partial):** While the current implementation does not compute full descriptive statistics (min, max, quartiles etc) it retrieves the data in a structured way, implying an intended extension to include those statistics in future.

      - **Output Formatting:** The results are formatted as a tab-separated string (tsv). It is designed for easy storage and later analysis. Each row shows a unique concept ID and its count.

   - **`DemographicsDistributionQuerySolver` - The Specialist:** This solver is optimized for queries about demographic data.

      - **Focused Analysis:** It focuses on demographic characteristics like gender and provides detailed distribution information.

      - **Alternative Representations:** The solver provides alternative ways of expressing the result, tailored to demographic analysis.

      - **SQL Generation:** Similar to the `CodeDistributionQuerySolver`, it constructs SQL queries to count patients based on the demographic information.

**5\. Data Retrieval and Processing: Getting the Information**

With the query types known and solvers at the ready, here's how Hutch-bunny brings the data to life:

- **Database Manager:** The solvers interact with the database using the `db_manager`. The `db_manager` handles connections and query execution, ensuring they're managed safely and efficiently.

- **SQLAlchemy's Power:** SQL queries are built using SQLAlchemy, which ensures the queries are constructed correctly for multiple database backends.

   - **ORM Models:** SQLAlchemy's Object-Relational Mapping (ORM) is used to link tables to objects, which simplifies and standardizes database interaction.

   - **Dynamic Query Building:** The SQLAlchemy ORM enables dynamic query generation by using mapping dictionaries (e.g. `allowed_domains_map`), ensuring the correct tables and columns are used based on the request.

- **Mapping Dictionaries:** `allowed_domains_map` is the key to knowing where data lives.

   - **Domain-to-Table Mapping:** It links medical concept domains (e.g., 'Condition', 'Drug') to the corresponding tables in the OMOP CDM.

   - **Dynamic SQL:** This map allows the code to automatically choose the correct table for a given domain when constructing a SQL query.

   - **Consistency and Extensibility:** It ensures consistency across the codebase and makes adding new domains easier.

- **Data Manipulation with Pandas:** Results are often retrieved into Pandas DataFrames. This is a popular choice for data analysis as it allows easy filtering, grouping and manipulation of data before being passed to the next step.

- **Target OMOP CDM Tables:** The OMOP CDM tables that Hutch-bunny targets include:

   - `Person`: For demographic information (gender, ethnicity, etc.).

   - `ConditionOccurrence`: For data about patient conditions.

   - `DrugExposure`: For details of drug exposures.

   - `Measurement`: For lab results and other quantitative measurements.

   - `Observation`: For clinical observations.

   - `ProcedureOccurrence`: For data about procedures.

   - `Concept`: A reference table for all medical concepts.

**6\. Result Handling and Obfuscation: Ensuring Data Privacy**

Data privacy is essential, and Hutch-bunny takes several steps to protect sensitive information:

- **The `RquestResult` Object:** This object is the container for all query results, acting as a structured way to send information back to the system. It contains key information like:

   - `uuid`: The unique ID of the query.

   - `status`: Indicates if the query ran successfully or encountered an error (`ok` or `error`).

   - `count`: The result for an availability query.

   - `collection_id`: The data collection ID.

   - `files`: List of files (for distribution queries).

   - Metadata about the data.

- **Obfuscation with `apply_filters_v2`:** For availability queries, the `apply_filters_v2` function (in `src/hutch_bunny/core/obfuscation.py`) applies result modifiers that have been defined in the configuration. These filters are designed to safeguard patient privacy.

   - **Low Number Suppression:** If a result is below a certain threshold (specified by the `LOW_NUMBER_SUPPRESSION_THRESHOLD` environment variable), it is suppressed, preventing identification of small groups. The threshold is set in the `settings.py`.

   - **Rounding:** If rounding is needed (specified by the `ROUNDING_TARGET` environment variable), results are rounded to the nearest `n` to increase anonymity.

- **Marking of Sensitive Data:** Results from distribution queries are marked as sensitive.

**7\. Result Transmission: Sending the Analysis Back Home**

Finally, the results need to be returned to the calling system. Here’s how Hutch-bunny handles this last leg:

- **JSON Serialization:** The `RquestResult` object is serialized into a JSON string. This ensures the data is portable and can be sent over HTTP.

- **HTTP POST Request:** The Task API client sends an HTTP POST request to the Relay endpoint.

   - **Data in the Body:** The JSON representation of the `RquestResult` is included as the body of the request. This ensures the data is transmitted reliably and securely.

- **Relay Receives Data:** The Relay receives the data and can proceed with further processing. This is how results are returned to the wider Hutch ecosystem.

- **Retry Logic:** The daemon uses retry logic to ensure the results are sent to the Relay even if the request fails initially.

**In Summary**

The Hutch-bunny query lifecycle is a highly sophisticated, multi-stage process. It begins with a query entry point, either a manual CLI or a constantly polling daemon process. The query is parsed into structured DTO objects, the type of query is determined, and the appropriate query solvers are used to craft SQL queries based on the OMOP CDM. After retrieval, the results are processed, possibly obfuscated, and then encapsulated in an `RquestResult` DTO which is transmitted back to the Relay System using an HTTP POST request. This carefully crafted pipeline is designed for efficient and secure data analysis.
Hutch-bunny handles query obfuscation through a series of steps designed to protect patient privacy, primarily by modifying the query results before they are returned. This involves applying filters, specifically low number suppression and rounding, to the aggregated counts produced by the queries. The system does not allow users to input raw SQL, but instead uses a structured approach to generate queries and then obfuscate the results.

**1\. Obfuscation Mechanisms**

- **Low Number Suppression:** This is a data protection mechanism designed to prevent the disclosure of potentially identifiable information when dealing with small counts in query results. If a count is below a certain threshold, it is replaced with 0. For example, if the `LOW_NUMBER_SUPPRESSION_THRESHOLD` is set to 5, any count of 4 or less will be returned as 0. This is implemented in the `low_number_suppression` function within `core/obfuscation.py`.

- **Rounding:** This technique rounds the query result to the nearest multiple of a defined `ROUNDING_TARGET`. For instance, if the `ROUNDING_TARGET` is set to 10, a count of 7 becomes 10, and a count of 12 also becomes 10. This is implemented in the `rounding` function within `core/obfuscation.py`.

- **Combined Application:** If both low number suppression and rounding are configured, the low number suppression is applied first, followed by rounding. So, a count of 3 would first be suppressed to 0, and a count of 7 might be rounded to 10.

**2\. Implementation Details**

- **`apply_filters_v2` Function:** The core logic for applying these obfuscation techniques resides in the `apply_filters_v2` function, which is located in the `core/obfuscation.py` file. This function takes the raw query result as input, and applies the configured suppression and rounding rules.

- **Configuration via Environment Variables:** The thresholds for low number suppression and rounding are set via environment variables. The `LOW_NUMBER_SUPPRESSION_THRESHOLD` and `ROUNDING_TARGET` variables are read from the environment and used to configure the `get_results_modifiers` function in the obfuscation module.

- **Result Modification:** The `apply_filters_v2` function is used in `execute_query.py`, where it modifies the results prior to sending them back to the Relay system.

- **Modular Design:** The obfuscation logic is implemented as a modular component, meaning new data protection methods can be added without requiring changes to the core query execution logic.

- **Data Sensitivity:** Results of distribution queries are marked as sensitive, indicating that they may contain potentially identifiable information, and have the obfuscation filters applied.

**3\. Purpose of Obfuscation**

- **Privacy Protection:** The primary goal of these techniques is to prevent the re-identification of individuals by limiting the granularity of the results.

- **Data Governance:** By obfuscating the results, Hutch-bunny can simplify data governance issues associated with sharing sensitive medical data.

- **Secure Query Execution:** Hutch-bunny is designed to be deployed behind institutional firewalls, and the obfuscation measures help ensure that even in the event of a security breach, the privacy of individual patients is maintained.

**4\. How it fits into the Query Lifecycle**

- **Query Execution:** Hutch-bunny receives a structured query, not raw SQL, which it then translates into an appropriate database query, which might be an availability query or a distribution query.

- **Result Retrieval:** After executing the query, the system obtains the results, which are initially in the form of numerical counts.

- **Obfuscation Application:** The `apply_filters_v2` function from `core.obfuscation` is used by the `execute_query` to modify the raw results by applying configured low number suppression and rounding, thereby obfuscating them.

- **Result Packaging:** The obfuscated results are packaged into a `RquestResult` object, which includes metadata, and then serialized into JSON format.

- **Result Transmission:** The JSON payload containing the obfuscated results is then sent back to the Relay system via an HTTP POST request.

**5\. Example**

Let's say a researcher queries the database to find out how many patients have a specific condition. The query result shows 3 patients at one site. If the `LOW_NUMBER_SUPPRESSION_THRESHOLD` is set to 5, the result returned by Hutch-bunny would be 0 instead of 3. If the `ROUNDING_TARGET` was set to 10, a result of 7 would be rounded to 10, and a result of 12 would also be rounded to 10.

In summary, Hutch-bunny uses low number suppression and rounding, configured via environment variables, to obfuscate query results. This ensures patient privacy, allows Hutch-bunny to be deployed safely behind firewalls, and simplifies data governance, all while providing valuable aggregated data to researchers.

A next step would be to review the test suite to verify that the result modifiers are correctly applied under different conditions, and that the configured parameters work as expected, especially in edge cases.

Hutch-bunny's test suite includes tests that specifically address the application of result modifiers, including low number suppression and rounding, although there are some limitations in the scope of the testing. These tests are primarily found in the `test_return.py` file and `test_demographics_distribution_query.py`. The existing test suite provides a solid foundation but could be expanded to improve coverage of all conditions, parameters, and edge cases.

Here’s a detailed breakdown of the test suite’s coverage of result modifiers:

**1\. Existing Tests for Result Modifiers**

- **`test_solve_availability_count_matches`**: This test, found in `test_return.py`, confirms that Hutch-bunny can correctly interpret and process Availability Queries, returning the correct count of individuals matching specific criteria. It uses a test database and asserts that the returned count matches an expected value after the application of the result modifiers. It appears that a threshold of 10 is being used in the test, to verify the number is suppressed to 0 when the result is lower than 10.

- **`test_demographics_distribution_query.py`**: This set of tests checks that Hutch-bunny can handle Distribution Queries for demographic data, such as age and gender. These tests primarily focus on verifying the format and content of the generated distribution results, but also confirm the results match expected values after any relevant result modifiers have been applied. This test suite verifies the correct application of the result modifiers, including number suppression and rounding, confirming the system works correctly.

**2\. Key Aspects of Current Testing**

- **Focus on Core Functionality:** The existing tests verify that Hutch-bunny can connect to the database, handle different types of queries (Availability and Distribution), and apply basic result modifiers like low number suppression and rounding.

- **Test Data:** The tests utilize a predefined test database, allowing for repeatable and predictable results. The test database likely includes a range of data points to help test various scenarios.

- **Assertion of Expected Results:** Each test asserts that the output from Hutch-bunny matches predefined expected results, thereby confirming that the result modifiers work as intended.

- **Environment Variables**: The test suite implicitly uses environment variables to configure the low number suppression and rounding behavior. This allows the tests to confirm that the configured parameters work as expected, although this could be more explicitly tested.

**3\. Limitations and Areas for Improvement**

While the existing tests are valuable, there are areas where the test suite could be expanded to improve confidence in the system.

- **Limited Database Backends**: Currently, the tests are primarily focused on a PostgreSQL database. Hutch-bunny is expected to also support Trino and possibly other database backends. Testing needs to be extended to cover all supported database backends to verify consistent behaviour across different environments.

- **Error Handling:** The current tests do not extensively test how Hutch-bunny handles errors that could occur with the result modifiers. For example, the test suite should verify how the code responds to invalid filter configurations, or how an error in the rounding algorithm would be handled.

- **Edge Cases:** The existing tests appear to cover basic cases but may not extensively cover edge cases that could arise in production systems. Specific edge cases related to result modifiers should include:

   - Queries that return no results.

   - Queries that return results equal to the suppression threshold.

   - Queries that return results with values at the rounding boundary.

   - Queries where very large numbers are returned and should be rounded.

   - Queries where the `LOW_NUMBER_SUPPRESSION_THRESHOLD` or `ROUNDING_TARGET` is set to 0 or a negative value.

- **Performance Testing:** The test suite currently lacks tests that evaluate the performance of Hutch-bunny when applying result modifiers. There aren’t any performance tests to verify the impact of obfuscation filters on query execution time, especially when dealing with large datasets or complex queries.

- **Explicit Testing of Environment Variables:** Although the tests are configured by environment variables, this testing could be made more explicit by running the same test with different values for the environment variables for suppression and rounding. This would make the tests more robust and ensure the proper behaviour is observed for all parameter configurations.

- **Filter Interactions:** The tests do not explicitly test the interaction between low number suppression and rounding. Additional tests are needed to ensure that when both filters are enabled, they are applied in the correct sequence, with suppression taking precedence.

**4\. Recommendations for Enhanced Testing**

To improve the verification of result modifiers, the following steps are recommended:

- **Add Tests for Different Database Backends**: Introduce testing that covers each of the supported database backends (such as Trino), and ensure consistent results across them.

- **Develop Tests Specifically for Error Handling**: Create tests to confirm how Hutch-bunny responds to errors related to result modifier configuration. These tests would verify proper logging and ensure that the system fails gracefully in error scenarios.

- **Expand Edge Case Testing**: Introduce tests that specifically check the behaviour of result modifiers under edge cases. For example:

   - Tests that verify queries return correct results when there are no matches.

   - Tests to check if boundary values are correctly suppressed or rounded according to configuration.

   - Tests to verify the behaviour when the LOW_NUMBER_SUPPRESSION_THRESHOLD or ROUNDING_TARGET is zero, negative, or invalid.

- **Implement Performance Tests**: Add tests that measure the execution time and resource usage of queries with result modifiers enabled. This will help identify performance bottlenecks and verify that the system can handle large datasets efficiently.

- **Create a dedicated suite for environment variable testing** Tests should be developed to explicitly test different configurations of the `LOW_NUMBER_SUPPRESSION_THRESHOLD` and `ROUNDING_TARGET` environment variables, which can involve a combination of unit tests and integration tests. This will confirm that different configurations behave correctly.

- **Filter Combination Testing:** Add tests that explicitly verify that the filters (suppression and rounding) are applied in the correct order, with suppression taking precedence, so as to ensure the filters do not conflict in their operation.

- **Automated Test Data Generation**: Implement a mechanism to automate the generation of test data that includes edge cases and varying levels of data volume, to reduce reliance on a static test database.

- **Integration Testing**: Develop integration tests that verify the interaction of the result modifiers with other components of Hutch-bunny, such as the database connection, query execution, and result packaging.

**5\. Example Implementation of New Tests**

To illustrate, here is an example of new tests that could be added:

- **Edge Case Test for Suppression:** A new test could be added to `test_return.py` that asserts that when a query result is equal to the low number suppression threshold, it is properly suppressed. For example, if the threshold is set to 5, a result of 5 should be suppressed to 0.

- **Edge Case Test for Rounding:** Another test could be added to `test_return.py` to check how rounding is applied when values are on the rounding boundary. For example, if the rounding target is 10, and a query returns 15, this should be rounded to 20.

- **Performance Tests**: A test script can be created that runs multiple queries in a loop with varying levels of data and with the filters enabled to measure the time taken for each iteration, and the resources used.

- **Explicit Environment Variable Configuration:** A test can be created to verify that the `get_results_modifiers` function in the `obfuscation` module correctly parses the environment variables and returns the expected modifiers.

By implementing these recommendations, the test suite can be made more comprehensive, resulting in a more robust and reliable system. This would ensure that Hutch-bunny’s result modifiers work correctly across various conditions, parameter configurations, and edge cases.

A next step would be to review the test implementation in the provided code, and identify opportunities to implement these additional tests, and suggest specific code changes.