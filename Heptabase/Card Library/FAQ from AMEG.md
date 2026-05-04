# FAQ from AMEG

---

# 1\. FAQ Page

| **FAQ ID** | **The Question** | 
|---|---|
| **FAQ-201** | You specified that the FitFile technical team will need access to the Azure subscriptions for installing and managing the FitFile Node. What are the explicit Azure roles that your team requires (for both Initial setup and ongoing operations)? | 
| **Category:** | Infrastructure, Security | 
| **Standard Answer:** | We typically require the 'Contributor' role assigned to our DevOps engineers for the deployment. This can be scoped to the entire Azure subscription if we are providing it, or to a specific resource group if the deployment is within your subscription. The Contributor role is necessary because when deploying an Azure Kubernetes Service (AKS), Azure automatically creates a second, managed resource group for the Kubernetes nodes, which requires these permissions. | 
| **Key Links:** |  | 
| *Related Features:* | \[\[3.1.1 Azure Deployment Configuration\]\] | 
| *Underlying Requirements:* | \[\[REQ-101 Define Azure Role-Based Access Control (RBAC) for Deployment\]\] | 



| **FAQ ID** | **The Question** | 
|---|---|
| **FAQ-202** | Will the FitFile technical team have access to any of the data stored that is processed in the FitFile Node when managing the DSCRO environment – In particular clear patient data? | 
| **Category:** | Data Handling, Security | 
| **Standard Answer:** | No, the FitFile technical team will not have access to any clear patient data. The platform is designed for the data provider to connect data sources themselves via the user interface. Access to the underlying Kubernetes cluster is configured via Role-Based Access Control (RBAC) to prevent access to data stored within the deployment (e.g., from uploaded datasets or query results). While our technical team may need access to the application for configuration, their user roles will be strictly configured to restrict access to any identifiable information. | 
| **Key Links:** |  | 
| *Related Features:* | \[\[3.2.1 Granular In-App Role-Based Access Control (RBAC)\], \[3.3.1 User-Interface Driven Data Source Connection\]\] | 
| *Underlying Requirements:* | \[\[REQ-102 Prevent Technical Team Access to Clear Patient Data\]\] | 



| **FAQ ID** | **The Question** | 
|---|---|
| **FAQ-203** | Can you please supply the Firewall URL List for outbound whitelisting? | 
| **Category:** | Networking, Security | 
| **Standard Answer:** | Yes, the list of required firewall rules for outbound whitelisting can be provided. Please refer to the specific networking requirements document shared with you (e.g., `firewall_rules.csv`). | 
| **Key Links:** |  | 
| *Related Features:* | \[\[3.1.1 Azure Deployment Configuration\]\] | 
| *Underlying Requirements:* | \[\[REQ-103 Provide Outbound Firewall Whitelisting Rules\]\] | 



| **FAQ ID** | **The Question** | 
|---|---|
| **FAQ-204** | For the “Firewall Rules & Network Requirements” section, there is a VPC/VNet CIDR range – 10.0.0.0/16 referenced. It mentions in your technical document that this can be modified. If we use our own address range can the CIDR IP address spaced be changed from /16 to reduce the number of usable IP addresses? | 
| **Category:** | Networking, Infrastructure | 
| **Standard Answer:** | Yes, this IP range can be modified. We now utilise Calico for networking within Kubernetes, which significantly reduces the address range required for the node. A smaller range, such as /24, should be sufficient for the deployment. | 
| **Key Links:** |  | 
| *Related Features:* | \[\[3.1.1 Azure Deployment Configuration\]\] | 
| *Underlying Requirements:* | \[\[REQ-104 Support for Flexible VNet CIDR Ranges\]\] | 



| **FAQ ID** | **The Question** | 
|---|---|
| **FAQ-205** | Who will manage access controls to the FitFile web system via Auth0 in your central services? | 
| **Category:** | Security, User Management | 
| **Standard Answer:** | User *authentication* (i.e., verifying a user's identity) is managed via our central Auth0 service, with access typically controlled by our Product Owner or delegated administrators in the technical team. However, all *authorisation* (i.e., a user's roles and permissions determining what they can do and see) is managed entirely within the FitFile application itself and cannot be modified externally. | 
| **Key Links:** |  | 
| *Related Features:* | \[\[3.2.1 Granular In-App Role-Based Access Control (RBAC)\], \[3.2.2 Centralised User Authentication via Auth0\]\] | 
| *Underlying Requirements:* | \[\[REQ-105 Separate Authentication and Authorisation Mechanisms\]\] | 



| **FAQ ID** | **The Question** | 
|---|---|
| **FAQ-206** | I have not seen your product demo yet but I am assuming it is possible to surface patient data via the web system? | 
| **Category:** | Data Handling, User Management | 
| **Standard Answer:** | Yes, the system can surface patient data, but visibility is strictly controlled by roles and permissions. You can configure user roles to prevent them from seeing any "identifiable" data, effectively blocking access to it based on their assigned permissions. | 
| **Key Links:** |  | 
| *Related Features:* | \[\[3.2.1 Granular In-App Role-Based Access Control (RBAC)\]\] | 
| *Underlying Requirements:* | \[\[REQ-106 Role-Based Control over Data Visibility\]\] | 

---

# 2\. Requirements Page

### **Summary of Requirements**

| **Requirement ID** | **Title** | **Type** | **Source** | 
|---|---|---|---|
| REQ-101 | Define Azure Role-Based Access Control (RBAC) for Deployment | Security | Client Request | 
| REQ-102 | Prevent Technical Team Access to Clear Patient Data | Security | Client Request | 
| REQ-103 | Provide Outbound Firewall Whitelisting Rules | Non-Functional | Client Request | 
| REQ-104 | Support for Flexible VNet CIDR Ranges | Non-Functional | Client Request | 
| REQ-105 | Separate Authentication and Authorisation Mechanisms | Security | Client Request | 
| REQ-106 | Role-Based Control over Data Visibility | Functional | Client Request | 

---

### **Detailed Requirements**

Requirement ID & Title:

REQ-101: Define Azure Role-Based Access Control (RBAC) for Deployment

- **Source:** Client Request

- **Type:** Security

- **Description:** The system must have clearly defined Azure role requirements for initial installation and ongoing management. The client needs to know the principle of least privilege required for FitFile DevOps engineers to perform their duties on the client's Azure subscription or a dedicated resource group.

- **Key Links:**

   - *Satisfied by Feature(s):* \[\[3.1.1 Azure Deployment Configuration\]\]

---

Requirement ID & Title:

REQ-102: Prevent Technical Team Access to Clear Patient Data

- **Source:** Client Request

- **Type:** Security

- **Description:** The application architecture must ensure that FitFile technical staff cannot access clear, identifiable patient data when performing management or support tasks. This includes data stored in databases, in-transit, or viewable through application interfaces. Access controls must be enforced at the infrastructure and application layers.

- **Key Links:**

   - *Satisfied by Feature(s):* \[\[3.2.1 Granular In-App Role-Based Access Control (RBAC)\], \[3.3.1 User-Interface Driven Data Source Connection\]\]

---

Requirement ID & Title:

REQ-103: Provide Outbound Firewall Whitelisting Rules

- **Source:** Client Request

- **Type:** Non-Functional

- **Description:** The product must have a documented list of all required outbound network destinations (URLs, IP addresses, ports) to allow for precise firewall whitelisting in a secure corporate environment.

- **Key Links:**

   - *Satisfied by Feature(s):* \[\[3.1.1 Azure Deployment Configuration\]\]

---

Requirement ID & Title:

REQ-104: Support for Flexible VNet CIDR Ranges

- **Source:** Client Request

- **Type:** Non-Functional

- **Description:** The system's networking configuration must be flexible enough to accommodate different customer VNet IP address schemes. It should not impose an unnecessarily large CIDR block, and must support smaller ranges like /24.

- **Key Links:**

   - *Satisfied by Feature(s):* \[\[3.1.1 Azure Deployment Configuration\]\]

---

Requirement ID & Title:

REQ-105: Separate Authentication and Authorisation Mechanisms

- **Source:** Client Request

- **Type:** Security

- **Description:** The system must decouple user authentication (verifying who a user is) from user authorisation (what a user can do). Authentication can be handled by a central identity provider (IdP), but authorisation logic must reside and be managed exclusively within the application.

- **Key Links:**

   - *Satisfied by Feature(s):* \[\[3.2.1 Granular In-App Role-Based Access Control (RBAC)\], \[3.2.2 Centralised User Authentication via Auth0\]\]

---

Requirement ID & Title:

REQ-106: Role-Based Control over Data Visibility

- **Source:** Client Request

- **Type:** Functional

- **Description:** The application must provide administrators with the tools to configure roles and permissions that can restrict user access to specific types of data, such as identifiable patient information. Users assigned to such roles must be blocked from viewing the restricted data.

- **Key Links:**

   - *Satisfied by Feature(s):* \[\[3.2.1 Granular In-App Role-Based Access Control (RBAC)\]\]

---

# 3\. Feature Pages

| **Property** | **Value** | 
|---|---|
| **ID** | 3\.1.1 | 
| **Feature Name** | Azure Deployment Configuration | 
| **Status** | Implemented | 
| **Owner** | DevOps Team | 
| **Last Reviewed** | 2025-06-19 | 

Brief Description:

Provides a configurable and documented deployment process for the FitFile Node within a client's Azure environment.

Purpose & User Value:

This feature allows for secure and flexible installation of the FitFile Node into diverse client Azure environments. It provides clients with the confidence that the deployment adheres to their specific networking and security policies, such as custom IP address ranges and strict firewall rules.

**Functional Details:**

- The deployment scripts and templates (e.g., ARM/Bicep) allow for the VNet CIDR range to be specified as a parameter.

- The deployment process leverages Calico CNI for Kubernetes networking to minimise IP address consumption.

- A pre-defined list of required outbound endpoints is maintained and provided to clients for firewall configuration.

- Deployment documentation specifies the need for 'Contributor' access on the target resource group.

**Privacy & Security Considerations:**

- Deployment requires 'Contributor' rights, the scope of which should be limited to the smallest possible area (ideally a dedicated resource group).

- All networking requirements are documented to ensure clients can maintain a secure, least-privilege firewall policy.

**Links to Collateral:**

- *Addresses Requirements:* \[\[REQ-101 Define Azure Role-Based Access Control (RBAC) for Deployment\]\], \[\[REQ-103 Provide Outbound Firewall Whitelisting Rules\]\], \[\[REQ-104 Support for Flexible VNet CIDR Ranges\]\]

- *Relevant FAQs:* \[\[FAQ-201 Azure Role Requirements\]\], \[\[FAQ-203 Firewall URL List\]\], \[\[FAQ-204 VNet CIDR Range Modification\]\]

- *Jira Tasks:* DEVOPS-431, DEVOPS-512

---

| **Property** | **Value** | 
|---|---|
| **ID** | 3\.2.1 | 
| **Feature Name** | Granular In-App Role-Based Access Control (RBAC) | 
| **Status** | Implemented | 
| **Owner** | Product Team | 
| **Last Reviewed** | 2025-06-19 | 

Brief Description:

A comprehensive in-application system for managing user permissions and controlling access to data and functionality.

Purpose & User Value:

This feature is critical for security and data governance. It empowers administrators to enforce the principle of least privilege, ensuring users can only access the data and tools necessary for their role. This directly addresses client concerns about protecting sensitive patient data from unauthorised internal or external access.

**Functional Details:**

- Administrators can create and define custom roles within the application's settings panel.

- Permissions can be assigned to roles, covering actions (e.g., 'Run Query', 'Manage Users') and data visibility (e.g., 'View Identifiable Data').

- Users are assigned one or more roles, which collectively determine their permissions.

- The system denies access by default; permissions must be explicitly granted.

- This authorisation logic is managed entirely within the application and is separate from the authentication system.

**Privacy & Security Considerations:**

- This is the primary mechanism for preventing data breaches and unauthorised access to patient information.

- Configuration of roles must be carefully managed. By default, even FitFile technical support staff should be given roles that prevent sight of identifiable data.

**Links to Collateral:**

- *Addresses Requirements:* \[\[REQ-102 Prevent Technical Team Access to Clear Patient Data\]\], \[\[REQ-105 Separate Authentication and Authorisation Mechanisms\]\], \[\[REQ-106 Role-Based Control over Data Visibility\]\]

- *Relevant FAQs:* \[\[FAQ-202 Access to Clear Patient Data\]\], \[\[FAQ-205 Access Control Management\]\], \[\[FAQ-206 Surfacing Patient Data\]\]

- *Jira Tasks:* FEAT-88, SEC-45

---

| **Property** | **Value** | 
|---|---|
| **ID** | 3\.2.2 | 
| **Feature Name** | Centralised User Authentication via Auth0 | 
| **Status** | Implemented | 
| **Owner** | Product Team | 
| **Last Reviewed** | 2025-06-19 | 

Brief Description:

Integrates with Auth0 to handle user identity verification and login processes.

Purpose & User Value:

Leverages a trusted, industry-standard Identity Provider (IdP) for robust and secure user authentication. This separates the concern of who a user is from what they can do, simplifying user management and enhancing security.

**Functional Details:**

- The FitFile web application redirects users to an Auth0 login page for authentication.

- Auth0 verifies the user's credentials (e.g., username/password, SSO).

- Upon successful authentication, Auth0 returns a token to the FitFile application, confirming the user's identity.

- The FitFile application then manages the user's session and applies its internal authorisation rules.

- Management of user identities in Auth0 is a distinct administrative function from managing their permissions inside the app.

**Privacy & Security Considerations:**

- Auth0 provides features like Multi-Factor Authentication (MFA) and breached password detection, enhancing account security.

- No application-level permissions are stored or managed in Auth0, preventing external escalation of privilege.

**Links to Collateral:**

- *Addresses Requirements:* \[\[REQ-105 Separate Authentication and Authorisation Mechanisms\]\]

- *Relevant FAQs:* \[\[FAQ-205 Access Control Management\]\]

- *Jira Tasks:* FEAT-89, SEC-46

---

| **Property** | **Value** | 
|---|---|
| **ID** | 3\.3.1 | 
| **Feature Name** | User-Interface Driven Data Source Connection | 
| **Status** | Implemented | 
| **Owner** | Product Team | 
| **Last Reviewed** | 2025-06-19 | 

Brief Description:

Allows authorised client users to connect their data sources to the FitFile Node directly through the web interface.

Purpose & User Value:

Empowers the data owner to manage their own data connections without needing to involve FitFile technical staff. This enhances security and privacy by ensuring that only the client handles their data source credentials and connection process.

**Functional Details:**

- An "Data Sources" section in the application UI allows users with appropriate permissions to add new data sources.

- The user is presented with a form to input connection details (e.g., server address, database name, credentials).

- The application securely stores these credentials (e.g., using Azure Key Vault) and uses them to establish a connection.

- The process is self-service and does not require intervention from FitFile engineers.

**Privacy & Security Considerations:**

- This feature is key to preventing FitFile staff from ever needing access to client data sources or credentials.

- Permissions to access this feature must be strictly controlled via the in-app RBAC system.

**Links to Collateral:**

- *Addresses Requirements:* \[\[REQ-102 Prevent Technical Team Access to Clear Patient Data\]\]

- *Relevant FAQs:* \[\[FAQ-202 Access to Clear Patient Data\]\]

- *Jira Tasks:* FEAT-104

You are absolutely right. My apologies, the previous markdown for the tables on the Feature Page was not standard and could cause rendering issues.

I have corrected the formatting for those tables to be more robust and have reviewed the other sections for clarity as well. Here is the corrected and complete documentation.

---

### **FAQ Page**

#### **FAQ-201: Data Handling and Anonymisation Pre-processing**

*Does FITFILE hold the data in Azure before it is anonymised? Is the data in a readable (identifiable) format while in the FITFILE Azure subscription?*

**Category:** Security, Data Handling

Standard Answer:

When FITFILE queries a data source, the raw output is temporarily loaded into a secure, internal, s3-like bucket for subsequent privacy processing. This storage is isolated within the data pipeline and is not accessible via any user interface. By default, data is retained for only one hour, and this duration can be configured to be even shorter if required.

**Key Links:**

- **Related Features:** \[\[3.1.1 Secure Data Staging\]\]

- **Underlying Requirements:** \[\[REQ-101 Temporary Data Staging\]\], \[\[REQ-102 Secure Internal Storage\]\], \[\[REQ-103 Configurable Data Retention\]\]

---

#### **FAQ-202: Performance Impact on Source Database**

*Does the data connection have any performance impact on the on-prem SQL server? Does FITFILE upload data in a batch or is it constantly probing the on-prem SQL DB?*

**Category:** Integration, Performance

Standard Answer:

FITFILE queries your SQL server on an on-demand basis when a user executes a "Query Plan". This means it does not constantly probe the database. Performance impact is possible depending on the complexity of the queries being run, but this can be managed by configuring a query timeout to prevent long-running operations. Query execution by operators is expected to be infrequent.

Separately, the system performs two automated tasks:

1. An hourly query of the `information_schema` to synchronise table and column metadata.

2. A nightly query run by the `hutch-bunny` client to support national cohort discovery, which extracts concept domains and may run ad-hoc count queries.

**Key Links:**

- **Related Features:** \[\[3.2.1 On-Demand Query Execution\]\], \[\[3.2.2 Automated Schema Discovery\]\], \[\[3.2.3 Scheduled System Queries\]\]

- **Underlying Requirements:** \[\[REQ-104 Query Performance Mitigation\]\], \[\[REQ-105 Schema Synchronisation\]\], \[\[REQ-106 On-Demand Querying\]\], \[\[REQ-107 Automated Reporting Queries\]\]

---

### **Requirements Page**

#### **Summary of Requirements**

| **Requirement ID** | **Title** | **Type** | **Source** | 
|---|---|---|---|
| REQ-101 | Temporary Data Staging | Functional | Client Request | 
| REQ-102 | Secure Internal Storage | Security | Security Constraint | 
| REQ-103 | Configurable Data Retention | Non-Functional | Client Request | 
| REQ-104 | Query Performance Mitigation | Non-Functional | Client Request | 
| REQ-105 | Schema Synchronisation | Functional | Technical Specification | 
| REQ-106 | On-Demand Querying | Functional | Client Request | 
| REQ-107 | Automated Reporting Queries | Functional | Technical Specification | 

---

#### **Requirement Details**

Requirement ID & Title:

REQ-101 Temporary Data Staging

- **Source:** Client Request

- **Type:** Functional

- **Description:** The system must be able to temporarily hold the output of a query from a source database in an intermediate storage area before it undergoes privacy-enhancing treatments.

- **Key Links:**

   - *Satisfied by Feature(s):* \[\[3.1.1 Secure Data Staging\]\]

Requirement ID & Title:

REQ-102 Secure Internal Storage

- **Source:** Security Constraint

- **Type:** Security

- **Description:** The temporary storage area for queried data must be internal to the system's data pipelines and must not be exposed or accessible through any external interface or application, ensuring raw data is isolated.

- **Key Links:**

   - *Satisfied by Feature(s):* \[\[3.1.1 Secure Data Staging\]\]

Requirement ID & Title:

REQ-103 Configurable Data Retention

- **Source:** Client Request

- **Type:** Non-Functional

- **Description:** The retention period for data held in the temporary staging area must be configurable by the administrator. The system should provide a secure, short default (e.g., 1 hour).

- **Key Links:**

   - *Satisfied by Feature(s):* \[\[3.1.1 Secure Data Staging\]\]

Requirement ID & Title:

REQ-104 Query Performance Mitigation

- **Source:** Client Request

- **Type:** Non-Functional

- **Description:** The system must provide a mechanism to limit the performance impact of queries on a client's source database. This includes the ability to configure a timeout for long-running queries initiated by users or automated processes.

- **Key Links:**

   - *Satisfied by Feature(s):* \[\[3.2.1 On-Demand Query Execution\]\], \[\[3.2.3 Scheduled System Queries\]\]

Requirement ID & Title:

REQ-105 Schema Synchronisation

- **Source:** Technical Specification

- **Type:** Functional

- **Description:** The system must periodically query the source database's `information_schema` to detect and synchronise changes to table structures, column names, and data types.

- **Key Links:**

   - *Satisfied by Feature(s):* \[\[3.2.2 Automated Schema Discovery\]\]

Requirement ID & Title:

REQ-106 On-Demand Querying

- **Source:** Client Request

- **Type:** Functional

- **Description:** Data should be pulled from the source SQL database only when a query plan is actively executed by a user or a scheduled task, rather than through constant, passive probing.

- **Key Links:**

   - *Satisfied by Feature(s):* \[\[3.2.1 On-Demand Query Execution\]\]

Requirement ID & Title:

REQ-107 Automated Reporting Queries

- **Source:** Technical Specification

- **Type:** Functional

- **Description:** The system must support scheduled, automated queries against the source data for specific use cases, such as the nightly distribution queries required for the national cohort discovery portal.

- **Key Links:**

   - *Satisfied by Feature(s):* \[\[3.2.3 Scheduled System Queries\]\]

---

### **Feature Page**

| **Property** | **Value** | 
|---|---|
| **ID** | 3\.1.1 | 
| **Feature** | Secure Data Staging | 
| **Status** | Implemented | 
| **Owner** | Data Engineering Team | 
| **Last Reviewed** | 19 June 2025 | 

**Brief Description:** Provides a secure, temporary, and isolated s3-like bucket to stage data post-query for privacy processing.

Purpose & User Value:

This feature ensures that raw, identifiable data extracted from a client's source database is handled securely before anonymisation. It provides peace of mind by isolating the data within the processing pipeline, preventing unauthorised access, and automatically deleting it after a short, configurable period.

**Functional Details:**

- When a query plan is executed against an SQL data source, the results are streamed into an internal s3-like bucket within the FITFILE Azure environment.

- This bucket is only accessible by the internal data pipeline services responsible for applying privacy enhancements.

- Data within this bucket is governed by a retention policy, which defaults to 1 hour. Administrators can adjust this retention period to a shorter duration if needed.

**Privacy & Security Considerations:**

- **Isolation:** The staging bucket is not publicly exposed and cannot be accessed directly by users or external systems. Access is restricted to specific internal service principals.

- **Data Minimisation:** The short, configurable retention period ensures that raw data exists for the minimum time necessary to complete the privacy processing pipeline.

- **Data in Transit:** Data transfer from the source database to the staging bucket and from the bucket to the processing pipeline is encrypted.

**Links to Collateral:**

- **Addresses Requirements:** \[\[REQ-101 Temporary Data Staging\]\], \[\[REQ-102 Secure Internal Storage\]\], \[\[REQ-103 Configurable Data Retention\]\]

- **Relevant FAQs:** \[\[FAQ-201 Data Handling and Anonymisation Pre-processing\]\]

- **Jira Tasks:** DE-451, SEC-210

---

| **Property** | **Value** | 
|---|---|
| **ID** | 3\.2.1 | 
| **Feature** | On-Demand Query Execution | 
| **Status** | Implemented | 
| **Owner** | Application Team | 
| **Last Reviewed** | 19 June 2025 | 

**Brief Description:** Enables users to execute query plans against the source database on-demand with performance controls.

Purpose & User Value:

This feature gives users direct control over when the source database is queried, ensuring that performance impact only occurs during active analysis. The inclusion of a timeout setting protects the source database from being overloaded by excessively complex or long-running queries.

**Functional Details:**

- Users can trigger the execution of pre-defined Query Plans from the FITFILE interface.

- Execution is an on-demand process, not a continuous stream.

- An administrator can configure a global or per-connection timeout value (e.g., 300 seconds). If a query exceeds this duration, the process is terminated, and an error is returned to the user.

**Privacy & Security Considerations:**

- N/A for this feature directly, but it initiates the process handled by \[\[3.1.1 Secure Data Staging\]\].

**Links to Collateral:**

- **Addresses Requirements:** \[\[REQ-106 On-Demand Querying\]\], \[\[REQ-104 Query Performance Mitigation\]\]

- **Relevant FAQs:** \[\[FAQ-202 Performance Impact on Source Database\]\]

- **Jira Tasks:** APP-982, UI-415

---

| **Property** | **Value** | 
|---|---|
| **ID** | 3\.2.2 | 
| **Feature** | Automated Schema Discovery | 
| **Status** | Implemented | 
| **Owner** | Data Engineering Team | 
| **Last Reviewed** | 19 June 2025 | 

**Brief Description:** Automatically synchronises FITFILE's metadata with the source database's schema on an hourly basis.

Purpose & User Value:

Ensures that the metadata (table names, column names, data types) visible within FITFILE remains an accurate reflection of the source database. This prevents errors and empowers users to build queries with confidence, without needing manual intervention after a database schema change.

**Functional Details:**

- A scheduled background job runs every hour.

- The job connects to the source SQL database and queries the `information_schema` tables.

- It compares the result with the currently stored metadata in FITFILE and updates it to reflect any additions, deletions, or modifications.

**Privacy & Security Considerations:**

- This feature only queries metadata about the database structure (`information_schema`), not the content of the data tables themselves. Therefore, no identifiable or sensitive client data is accessed during this process.

**Links to Collateral:**

- **Addresses Requirements:** \[\[REQ-105 Schema Synchronisation\]\]

- **Relevant FAQs:** \[\[FAQ-202 Performance Impact on Source Database\]\]

- **Jira Tasks:** DE-501

---

| **Property** | **Value** | 
|---|---|
| **ID** | 3\.2.3 | 
| **Feature** | Scheduled System Queries | 
| **Status** | Implemented | 
| **Owner** | Application Team | 
| **Last Reviewed** | 19 June 2025 | 

**Brief Description:** Supports automated, scheduled queries for system-level use cases like the National Cohort Discovery.

Purpose & User Value:

This feature enables FITFILE to support federated data networks and national portals by providing necessary data summaries on a regular schedule. It automates the extraction of cohort distribution and count data, reducing the administrative burden and ensuring timely updates for national-level analysis.

**Functional Details:**

- The `hutch-bunny` client application is a component that facilitates federated queries.

- It is configured to run a distribution query on a nightly schedule to extract concept domains from an OMOP schema.

- It can also be triggered to run `COUNT(*)` queries on-demand as requested by the federated network.

- These automated queries are subject to the same timeout configurations as user-driven queries to manage performance.

**Privacy & Security Considerations:**

- The queries executed by this feature are typically aggregate (`COUNT`) or metadata-based (distribution of concepts), designed to avoid extracting row-level, identifiable data. All query results are handled by the secure data pipeline.

**Links to Collateral:**

- **Addresses Requirements:** \[\[REQ-107 Automated Reporting Queries\]\], \[\[REQ-104 Query Performance Mitigation\]\]

- **Relevant FAQs:** \[\[FAQ-202 Performance Impact on Source Database\]\]

- **Jira Tasks:** APP-1050, FED-55