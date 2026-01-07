---
aliases: []
tags: []
title: Ontop
type: ""
status: ""
confidence: ""
epistemic: ""
purpose: ""
created: 2026-01-06T16:11:52+00:00
modified: 2026-01-06T16:13:04+00:00
last_reviewed: ""
review_interval: ""
see_also: []
source_of_truth: []
---

The sources describe Ontop not merely as a standalone query engine, but as the central component of a broader **ecosystem of tools** designed to lower the barrier to entry for Ontology-Based Data Access (OBDA). These tools facilitate the creation, deployment, and utilization of Virtual Knowledge Graphs (VKGs) across various high-value academic and industrial use cases.

The Tool Ecosystem

To operationalize the core concepts of mapping and query rewriting, Ontop functions through several distinct interfaces and integrates with complementary software to handle the lifecycle of a VKG.

* **Development and Management Interfaces:**
    * **Protégé Plugin:** For system developers and ontology engineers, Ontop integrates into the popular ontology editor Protégé. This plugin provides a graphical interface for key OBDA tasks, such as editing mappings, executing SPARQL queries, checking ontology consistency, and managing database connections.
    * **SPARQL Endpoint:** For deployment, Ontop can run as a standard SPARQL endpoint (using the Sesame/RDF4J API). This allows it to serve as a web application that receives queries over HTTP, capable of result caching and streaming answers,. Recent versions have introduced a Docker image to simplify this deployment in containerised environments,.
    * **Command Line Interface (CLI):** A tool for scripting and automating tasks such as bootstrapping or materialising triples,.
* **Bootstrapping and Mapping Generation:**
    Creating mappings is identified as the most complex step in setting up a VKG. To mitigate this, the ecosystem includes **Mapping Bootstrappers**. These tools automatically generate a basic vocabulary and mapping assertions from the database schema. While simple "Direct Mappings" are often insufficient for capturing complex domain semantics, advanced tools like **BootOX** and **MIRROR** can generate complex mappings by analysing schema patterns and data, and integrating with ontology matching tools like **LogMap**,.

* **Federation Tools:**
    Ontop supports data integration from multiple sources through federation.
    * **SQL Federation:** It connects to federated database engines like **Teiid** or **Exareme**, which present multiple independent databases (relational, XML, CSV) as a single virtual schema to Ontop,.
    * **SPARQL Federation:** It can operate within a seamless federation (managed by systems like **FedX**) or process `SERVICE` keywords to delegate parts of a query to remote endpoints,.
* **Visual Query Interfaces:**
    To help end-users who may not be proficient in SPARQL, Ontop serves as the query translation backend for visual tools. A prominent example is the **Optique Platform**, which includes a visual query builder (**OptiqueVQS**) that allows users to formulate queries graphically using the ontology terms,.

**Applications and Use Cases**

The sources highlight that Ontop has been adopted in diverse scenarios where the primary challenge is accessing complex, heterogeneous, or massive datasets without moving the data.

**1. Industrial Use Cases: Statoil and Siemens**
These major use cases were developed within the EU Optique project, demonstrating Ontop's ability to handle "Big Data" in corporate environments.
* **Statoil (Equinor):** Geologists needed access to the **Exploration and Production Data Store (EPDS)**, a massive legacy database containing over 1,500 tables of historical exploration data. The complex schema made direct SQL access nearly impossible for domain experts. Ontop allowed geologists to access this data using familiar geological terms defined in an ontology, bypassing the need for pre-defined, rigid SQL queries,.
* **Siemens:** This use case involved monitoring power generation devices (turbines). The data consists of timestamped sensor readings stored in a relational database, growing by 30 GB per day. Service engineers spent up to 80% of their time just gathering data. Ontop facilitated the diagnosis and analysis of this streaming and historical data by mediating between the engineers' diagnostic vocabulary and the raw sensor data tables.

**2. Open Data and Public Sector**
Ontop is also utilised to publish and integrate public sector data, ensuring transparency and accessibility.
* **South Tyrolean Tourism (Open Data Hub):** In a joint project with NOI Techpark, Ontop was used to expose tourism data (hotels, events) stored in PostgreSQL as a Knowledge Graph. This replaced a rigid JSON-based Web API with a flexible SPARQL endpoint. They further developed **Web Components** that embed these SPARQL results directly into standard HTML pages for easy visualization.
* **UNiCS and Toscana Open Research:** The UNiCS platform integrates data from government bodies and higher education sectors. A specific deployment, the **Toscana Open Research (TOR)** portal, uses Ontop to help policy-makers analyse the regional research system. It enables users to perform analytics and integrate proprietary data with public records.

**3. Academic Research**
* **EPNet:** This project uses Ontop to give scholars access to historical data regarding food production and commercial trade during the Roman Empire, integrating various data sources.
* **Benchmarking (NPD):** The **NPD Benchmark** was created based on real data from the Norwegian Petroleum Directorate to rigorously test OBDA systems. It utilizes the complex real-world challenges found in the oil and gas industry to measure performance, where Ontop has demonstrated robust scalability compared to other systems,.

***

**Analogy**

You can think of the entire Ontop ecosystem like a modern **Architectural Firm**.

* **Ontop (The Engine)** is the **Lead Architect**. It understands both the artistic vision of the client (the Ontology/SPARQL) and the rigid laws of physics and engineering required to build it (the SQL/Database).
* **The Tools** are the **Drafting Software and Cranes**.
    * *Protégé* is the CAD software where the architect draws the blueprints (mappings).
    * *Bootstrappers* are the surveying drones that automatically map out the terrain (database schema) so the architect doesn't have to measure every inch by hand.
    * *Visual Query Interfaces (Optique)* are the 3D walkthroughs shown to the client, so they can say "I want a window here" (query data) without needing to understand load-bearing walls (SQL joins).
* **The Use Cases** are the **Buildings**.
    * *Statoil* is a massive, sprawling **Industrial Plant** with thousands of pipes (tables); the workers need a map that makes sense to *them*, not a blueprint of the plumbing.
    * *Open Data Hub* is a public **Visitor Centre**, designed to be easily accessible and transparent to any tourist (web user) who walks in.
