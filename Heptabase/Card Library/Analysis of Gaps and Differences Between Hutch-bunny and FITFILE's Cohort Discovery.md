# **Analysis of Gaps and Differences Between Hutch-bunny and FITFILE's Cohort Discovery**

**Analysis of Gaps and Differences Between Hutch-bunny and FITFILE's Cohort Discovery**

It appears that FITFILE is intended to be a more comprehensive solution, encompassing data transformation, de-identification, and federated cohort discovery, whereas Hutch-bunny is specifically a query resolver for cohort discovery against OMOP databases. FITFILE is designed to integrate with the wider SDE, whereas Hutch-bunny is intended to be a component within that environment.

Here's a breakdown of the key differences and gaps:

**1\. Scope and Functionality**

- **Hutch-bunny:**

   - **Core Function:** Acts as a query resolver for cohort discovery, processing queries against OMOP-CDM databases.

   - **Query Types:** Handles availability and distribution queries, including demographic and code-based distributions.

   - **Data Handling:** Focuses on querying data that is already in OMOP format.

   - **Integration:** Designed to integrate with the Hutch Relay system for federated networks and other compatible Task APIs.

   - **Obfuscation:** Includes result obfuscation, low number suppression, and result rounding to protect patient privacy.

   - **Deployment:** Can run as a daemon service, through a CLI, or within a Docker container.

- **FITFILE:**

   - **Core Function:** Provides a full solution for data transformation, de-identification, and federated cohort discovery.

   - **Data Handling:** Includes ETL pipelines (likely using The Hyve's software) to transform source data into OMOP format.

   - **Federated Discovery:** Supports federated cohort discovery across multiple NHS data providers via distributed nodes connected to the SDE network.

   - **Data Linkage:** Designed to link data across multiple NHS data providers.

   - **De-identification:** Performs de-identification and pseudonymisation on harmonized and original records.

   - **Integration:** Works within the SDE environment and integrates with the National Cohort Discovery Portal.

   - **Data Catalogue:** Includes capabilities for data cataloguing, profiling, and quality assurance.

**2\. Data Transformation and Harmonization**

- **Hutch-bunny:** Assumes that data is already in OMOP-CDM format. It does not handle data transformation or harmonization.

- **FITFILE:** Includes an ETL pipeline (provided by The Hyve) to convert data from various source systems into OMOP format. This is a key difference, as it manages the entire data transformation process.

**3\. De-identification and Data Minimization**

- **Hutch-bunny:** Provides basic result obfuscation (low number suppression and rounding) for query results.

- **FITFILE:** Manages de-identification and pseudonymisation on both the harmonised data and the original records. It also appears to have a focus on providing a minimal set of data based on the query itself.

**4\. Federated Cohort Discovery**

- **Hutch-bunny:** Can function as part of a federated network through Hutch Relay.

- **FITFILE:** Designed for federated cohort discovery across multiple NHS data providers, with a master node coordinating the process.

**5\. User Interface and Workflow**

- **Hutch-bunny:** Primarily operates as a service or through a command-line interface.

- **FITFILE:** Integrates into the SDE and National Portal, providing user interfaces for cohort discovery. SDE Managers will create queries for specific projects with manual input from the researcher (outside of the FITFILE platform).

**6\. Data Catalogue and Profiling**

- **Hutch-bunny:** Does not include data cataloguing or data profiling features.

- **FITFILE:** Includes data profiling (using WhiteRabbit) to understand source data structure and a data catalogue to support researchers and data providers.

**7\. Governance and Compliance**

- **Hutch-bunny:** Focuses on technical security through obfuscation and is designed to be deployed behind a firewall.

- **FITFILE:** Aims to implement data governance rules and guidelines at the right time and maintain governance levels. This includes de-identification, audit trails, and compliance with information governance rules.

**8\. Integration with Existing Infrastructure**

- **Hutch-bunny:** Designed to be a component within a broader system, such as the HDR UK Cohort Discovery tool.

- **FITFILE:** Is designed to be a complete solution within the SDE, incorporating all necessary components for cohort discovery.

**9\. Purpose**

- **Hutch-bunny:** A general-purpose tool that acts as a component of a larger system.

- **FITFILE:** Designed to solve a specific problem with NHS data by linking the national cohort discovery platform with local provider data.

**Design Document for Cohort Discovery Approach**

Based on the analysis, here is a design document to help decide how to approach cohort discovery, focusing on capabilities, how solutions work, and potential modifications to FITFILE:

**1\. Goal**

- To implement a secure, efficient, and compliant cohort discovery solution within the SDE, leveraging the strengths of both FITFILE and Hutch-bunny (if necessary).

**2\. Capabilities**

- **Data Transformation and Harmonization:**

   - Convert data from various NHS data provider systems into the OMOP CDM using The Hyve's ETL pipeline.

   - Ensure data quality and consistency through data profiling and mapping.

- **De-identification and Data Minimization:**

   - Apply de-identification and pseudonymisation techniques to both harmonized and original data.

   - Implement data minimisation rules to ensure only the necessary data is exposed.

   - Comply with national and local information governance rules.

- **Federated Cohort Discovery:**

   - Enable federated cohort discovery across multiple NHS data providers.

   - Support queries from the National Cohort Discovery Portal.

- **Query Processing:**

   - Process availability and distribution queries (including demographic and code-based queries).

   - Provide efficient and secure query execution.

- **Data Catalogue and Profiling:**

   - Provide a data catalogue for researchers and data providers to understand available data attributes.

   - Use data profiling to analyze source data structure and content.

- **User Interface and Workflow:**

   - Integrate with the National Portal and SDE for user interaction.

   - Enable SDE Managers to create queries with input from researchers.

- **Security and Compliance:**

   - Ensure data security and patient privacy through data obfuscation and de-identification.

   - Maintain audit trails for all queries and data access activities.

   - Comply with all relevant regulations and standards (e.g., ISO27001, GDPR).

**3\. How Solutions Work**

- **FITFILE:**

   - FITFILE nodes are deployed at each NHS data provider and in the SDE.

   - The Hyve's software, deployed within the FITFILE node, performs ETL, transforming source data to OMOP format.

   - Data is de-identified, and the FITFILE system supports federated cohort discovery via its distributed nodes.

   - The SDE Manager uses the FITFILE platform to construct the required queries via a bespoke user interface.

   - The FITFILE Master Node coordinates queries and returns aggregate results.

   - FITFILE interacts with the National Portal via APIs.

- **Hutch-bunny:**

   - Hutch-bunny is deployed within each data provider's environment.

   - It receives queries from the National Cohort Discovery Tool (NCDT) via the Relay API.

   - It then processes the queries against the local OMOP CDM database, providing aggregate counts back to the National Portal.

   - It supports demographic and code-based distribution queries.

**4\. Potential Modifications to FITFILE**

- **Integration with Hutch-bunny:** Although it seems that FITFILE already provides the required capability, in the event that there's a need to, the FITFILE platform could be extended to incorporate Hutch-bunny's query processing capabilities.

   - This would involve creating an interface within FITFILE to interact with Hutch-bunny's Task API.

   - FITFILE would act as a mediator, passing queries to Hutch-bunny and handling the results.

- **Data Catalog Enhancement:** If the data catalogue in FITFILE does not cover all the required metadata, consider adding modules or functionality in FITFILE to enhance the data catalogue capabilities, such as more detailed attribute descriptions, data lineage, and quality metrics.

- **De-identification Customization:** Provide more customization options for the de-identification process, such as a user interface for defining rules and configuring parameters for de-identification and pseudonymisation.

- **Enhanced Monitoring and Alerting:** Integrate Grafana or similar tools for more advanced monitoring of the FITFILE platform and for logging and reporting on errors, providing an alert in the event of a node being unavailable.

- **Query Optimisation:** Review the SQL query generation process within the FITFILE pipeline and implement strategies to optimise SQL queries for speed and efficiency.

**5\. Gap Analysis**

- **Hutch-bunny:** Gaps include data transformation, de-identification, federated cohort discovery, and data cataloguing.

- **FITFILE:** No significant gaps identified based on the current documents for cohort discovery. Potential gaps in customising de-identification, reporting and query optimisation might need to be considered if that becomes necessary.

**6\. Recommendation**

- **Prioritize FITFILE:** Based on the comprehensive capabilities of FITFILE, it is the preferred solution as it provides an end-to-end data transformation, de-identification, and cohort discovery system.

- **Optional Hutch-bunny Integration:** If it is deemed that the FITFILE query engine does not meet performance needs, consider integrating Hutch-bunny's query solving capabilities into FITFILE. This can be done via a Task API integration.

- **Address identified gaps:** Implement the potential modifications outlined above to address any gaps or improve functionality based on specific needs.

**Next Steps:**

1. **Review this design document** with the technical team and stakeholders to ensure alignment.

2. **Engage FITFILE team** to understand implementation details, including data flow, security, and reporting and discuss a possible integration plan.

3. **Prioritise any additional features** or customisation requirements based on your specific needs.

4. **Plan for testing and validation** of the system once implemented.

This design document and the analysis of the gaps will provide a strong basis for your strategic decision-making. By carefully considering the capabilities of both FITFILE and Hutch-bunny, you can ensure that the chosen cohort discovery approach is effective, secure, and meets the needs of the project.