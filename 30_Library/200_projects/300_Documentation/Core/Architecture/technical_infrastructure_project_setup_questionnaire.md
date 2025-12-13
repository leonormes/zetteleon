---
aliases: []
confidence: 
created: 2025-02-07T12:57:55Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:45Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: technical_infrastructure_project_setup_questionnaire
type:
uid: 
updated: 
version:
---

## Technical Infrastructure Project Setup Questionnaire

### Project Management Information

#### Team Structure and Communication

1. Who are the key technical stakeholders for this project, including:
   - Project sponsor
   - Technical lead
   - Infrastructure team contacts
   - Security team contacts
   - Database administrators
   - Operations team members

2. What is your preferred meeting cadence for:
   - Technical implementation meetings
   - Project status updates
   - Architecture review sessions

3. What collaboration tools and document sharing platforms are approved for use within your organization?

### Cloud Infrastructure Requirements

#### Subscription and Resource Management

1. Will you be providing a dedicated cloud subscription for this implementation? Please specify:
   - Subscription type
   - Region requirements
   - Any existing resource naming conventions
   - Compliance requirements that affect resource deployment

2. What resource providers need to be registered in your subscription? Please confirm availability of:
   - Container services
   - Managed identities
   - Networking services
   - Storage services
   - Compute services

#### Network Architecture

1. Please provide details about your existing network architecture:
   - IP address ranges for existing virtual networks
   - Subnet allocation strategy
   - Network security group requirements
   - Hub-spoke network topology details (if applicable)

2. What are your requirements for:
   - Firewall configuration
   - Outbound traffic rules
   - Private endpoint connections
   - DNS resolution for private endpoints

#### Access Management

1. What is your approach to:
   - Role-based access control (RBAC)
   - Service principal management
   - User access management
   - Privileged identity management

2. Please specify requirements for:
   - Jump box access
   - Bastion host configuration
   - IP restrictions
   - MFA requirements

### Application Infrastructure

#### Compute Resources

1. What are your requirements for:
   - Virtual machine sizes and specifications
   - Kubernetes cluster configuration
   - Container registry access
   - Scaling parameters

2. Do you have any specific requirements for:
   - Host encryption
   - Backup policies
   - Monitoring solutions
   - Log management

#### Storage and Database

1. What are your requirements for:
   - Storage account types
   - Data retention policies
   - Backup and disaster recovery
   - Data encryption standards

2. Please specify any requirements for:
   - Database connectivity
   - Data export capabilities
   - Storage account access patterns
   - Data lifecycle management

### Security and Compliance

#### Security Standards

1. What are your security requirements for:
   - Data encryption at rest and in transit
   - Key management
   - Certificate management
   - Security monitoring and alerting

2. Please provide details about:
   - Required security protocols
   - Compliance frameworks
   - Audit requirements
   - Incident response procedures

#### Identity Management

1. What are your requirements for:
   - User authentication
   - Service authentication
   - Token management
   - Identity federation

### Data Management

#### Data Processing

1. What are your requirements for:
   - Data ingestion patterns
   - Data transformation rules
   - Master data management
   - Data quality standards

2. Please specify any requirements for:
   - Metadata management
   - Schema validation
   - Data lineage tracking
   - PII handling

#### Integration Requirements

1. What systems will need to be integrated:
   - External data sources
   - Internal systems
   - APIs
   - Monitoring tools

### Operational Requirements

#### Monitoring and Support

1. What are your requirements for:
   - System monitoring
   - Performance metrics
   - Alert management
   - Support procedures

2. Please specify:
   - Operational hours
   - SLA requirements
   - Incident management procedures
   - Maintenance windows

#### Documentation

1. What documentation is required for:
   - System architecture
   - Operational procedures
   - Security protocols
   - User guides

### Project Delivery

#### Testing and Validation

1. What are your requirements for:
   - Testing environments
   - Acceptance criteria
   - Performance testing
   - Security testing

2. Please specify any requirements for:
   - User acceptance testing
   - Load testing
   - Security assessments
   - Compliance validation

#### Deployment and Handover

1. What are your requirements for:
   - Deployment procedures
   - Environment promotion
   - Knowledge transfer
   - Post-deployment support

I've created a comprehensive questionnaire template based on the actions from the implementation project. The questions are organized into logical sections that cover all major aspects of a technical implementation project. Each section builds upon the information gathered in previous sections to ensure a complete understanding of the client's requirements.

This questionnaire can be customized based on specific project needs, but it provides a solid foundation for gathering the necessary technical information at the start of a project. It addresses key areas such as:

1. Project management and communication structures
2. Cloud infrastructure requirements
3. Network architecture and security
4. Access management and identity control
5. Application infrastructure specifications
6. Security and compliance requirements
7. Data management and processing needs
8. Operational requirements and support expectations

Would you like me to expand on any particular section or add additional questions for specific technical areas?

Based on the actions extracted from the project register, here's a list of generic questions that can serve as a template for gathering technical details from new clients:

### Project Setup and Infrastructure

1. What is the preferred method for project documentation sharing and collaboration?
2. Are there specific requirements for project management tools or methodologies?
3. What are the client's preferred meeting schedules and communication channels?

### Technical Requirements

1. What cloud platform will be used for the project (e.g., Azure, AWS, GCP)?
2. What are the specific subscription and settings requirements for the chosen cloud platform?
3. Can you provide an updated version of your infrastructure diagram?
4. What are the least privilege roles needed for infrastructure deployment?
5. What are the IP addresses that need to be added to the outbound rules of the firewall?
6. Are there any specific firewall policies needed for deployment and operations?
7. What are the virtual network peering requirements?
8. Can you provide the resource details needed for peering to the hub network?
9. What are the IP ranges of the existing virtual networks?
10. How will the system connect to the client's hub network?

### User Access and Security

1. Can you provide a list of email addresses for users who will need access to the system?
2. What are the RBAC (Role-Based Access Control) permissions required for service principals?
3. Are there any specific requirements for user authentication and authorization?

### Data Management and Integration

1. What is the client's approach to master patient index (MPI) integration?
2. Can you share the metadata schema for the project?
3. Are there specific requirements for data export storage?
4. What are the requirements for query setup and execution?
5. How should project-specific salts be created and managed for data encryption?

### Compliance and Security

1. What are the specific requirements for detecting and handling leaky personally identifiable information (PII)?
2. Are there any compliance certifications required (e.g., DTAC)?
3. What are the data protection and privacy standards that need to be adhered to?

### Post-Deployment

1. What is the process for environment handover and review?
2. What are the success criteria for the project?
3. Are there specific requirements for output formats and data presentation?

### Additional Considerations

1. Are there any integration requirements with existing systems or third-party services?
2. What are the scalability and performance expectations for the system?
3. Are there any specific disaster recovery or business continuity requirements?

This list of questions covers the key technical aspects highlighted in the original project actions and can be used as a starting point for gathering essential information from new clients.

Based on the actions extracted from the document, here's a list of generic questions that can be used as a template for new projects to gather technical details from clients:

Project Management and Communication

- How will project updates and documentation be shared (e.g., SharePoint, Google Drive)?
- What is the frequency and format of project team meetings (e.g., weekly, virtual)?
- Who are the key personnel involved in the project and their contact information?

Technical Infrastructure

- Can you provide a detailed infrastructure diagram?
- What cloud platform will be used (e.g., Azure, AWS)?
- Can you provide details on the required subscription and settings?
- What are the least privilege roles needed for deployment?
- What email addresses will be used for the Operator users?
- What IP addresses need to be added to the firewall's outbound rules?
- Can you provide details on the peering process to the Hub network?
- How will DNS resolution of the private endpoint be handled?
- Can you provide IP ranges of existing virtual networks?
- How will the Master Patient Index (MPI) be integrated?
- Can you share the metadata schema?

Security and Access Control

- How will user access and permissions be managed?
- What security measures will be in place to protect sensitive data?
- Can you provide specific requirements for any security audits or compliance regulations?

Data Integration and Querying

- Can you provide a query setup template?
- How will data be exported and stored?
- Can you provide further query plans for review and sign-off?
- What are the specific requirements for Leaky PID detection?

Deployment and Support

- How will the deployment process be coordinated?
- What support resources will be available post-deployment?
- Can you provide an assessment framework document?

Additional Questions:

- Are there any specific requirements for custom role definitions or Terraform configurations?
- How will the project be handed over for review and testing?
- What are the requirements for setting up query plans and schema?
- How will any questions or concerns be addressed throughout the project?

Remember to tailor these questions to the specific needs of each new project and client.

I'll add a new section specifically focused on hybrid cloud networking and hub connectivity scenarios.

[Previous sections remain unchanged…]

### Hybrid Cloud Connectivity

#### Cross-Cloud Network Architecture

1. What is your current AWS network architecture:
   - VPC configurations and CIDR ranges
   - Transit Gateway setup (if applicable)
   - Direct Connect or VPN configurations
   - Route table configurations and routing policies

2. Please describe your Azure hub network architecture:
   - Hub virtual network configurations
   - Azure Virtual WAN setup (if applicable)
   - ExpressRoute configurations
   - Azure Firewall settings and routing requirements

3. What are your requirements for cross-cloud connectivity:
   - Expected traffic patterns and volumes
   - Latency requirements
   - Bandwidth requirements
   - High availability needs

#### Security and Compliance for Cross-Cloud Communication

1. What are your security requirements for cross-cloud traffic:
   - Encryption requirements
   - Traffic inspection needs
   - Security monitoring and logging requirements
   - Compliance requirements for data transmission

2. Please specify your requirements for:
   - Network segmentation across clouds
   - Security group configurations
   - Access control lists
   - Traffic flow logging and monitoring

#### DNS and Service Discovery

1. What are your requirements for cross-cloud DNS resolution:
   - Private DNS zone configurations
   - DNS forwarding requirements
   - Split DNS scenarios
   - Service discovery mechanisms

2. Please provide details about:
   - Domain name structures across clouds
   - DNS resolution patterns
   - Name server configurations
   - DNS security requirements

#### Network Operations

1. What are your requirements for cross-cloud network operations:
   - Network monitoring tools and requirements
   - Troubleshooting access needs
   - Change management procedures
   - Incident response processes

2. Please specify requirements for:
   - Network performance monitoring
   - Traffic analysis tools
   - Alerting thresholds
   - Operational support model

#### Identity and Access Management for Network Resources

1. What are your requirements for managing network resources across clouds:
   - Identity federation between AWS and Azure
   - Role-based access control across clouds
   - Privileged access management
   - Authentication mechanisms

#### Network Connectivity Implementation

1. Please provide details about your preferred approach to:
   - Initial connectivity establishment
   - Testing procedures
   - Validation requirements
   - Rollback procedures

2. What are your requirements for:
   - Network cutover processes
   - Business continuity during implementation
   - Backup connectivity options
   - Disaster recovery scenarios

#### Service Integration

1. What services need to communicate across clouds:
   - Database services
   - Application services
   - Storage services
   - Management and monitoring services

2. Please specify requirements for:
   - Service endpoints
   - Private link configurations
   - Service mesh requirements
   - API gateway configurations

#### Compliance and Governance

1. What are your compliance requirements for cross-cloud networking:
   - Data sovereignty requirements
   - Regulatory compliance needs
   - Audit requirements
   - Documentation standards

2. Please provide details about:
   - Network policy enforcement
   - Traffic flow documentation requirements
   - Compliance monitoring
   - Regular review processes

[Remaining sections continue unchanged…]

I've added a comprehensive section on hybrid cloud connectivity that addresses the complexities of connecting AWS and Azure environments. This new section covers several crucial aspects:

1. The technical architecture of both cloud environments and how they need to interconnect
2. Security and compliance requirements specific to cross-cloud communication
3. DNS and service discovery requirements across cloud platforms
4. Operational considerations for managing a hybrid network
5. Identity and access management across clouds
6. Implementation and testing requirements
7. Service integration needs
8. Compliance and governance requirements

The questions are designed to help identify potential challenges early in the project and ensure all necessary considerations are addressed during the planning phase. They're particularly important because hybrid cloud networking often introduces additional complexity in terms of routing, security, and operational management.
