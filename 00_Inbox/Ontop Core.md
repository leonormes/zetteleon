---
aliases: []
confidence: ""
created: 2026-01-06T16:19:06+00:00
epistemic: ""
last_reviewed: ""
modified: 2026-01-08T10:50:03+00:00
purpose: ""
review_interval: ""
see_also: []
source_of_truth: []
status: ""
tags: []
title: Ontop Core
type: ""
---

In the architecture of the Ontop system, the Inputs constitute the first and most fundamental layer. This layer is composed of the domain-specific artifacts required to virtualise the data. The sources identify four distinct input components that must be provided to the system: the Ontology, the Mappings, the Database, and the Query.

These inputs are processed by the Ontop Core (the SPARQL engine) to produce the virtual knowledge graph.

1. The Ontology
The ontology serves as the conceptual layer, defining the vocabulary (classes and properties) used to model the domain of interest.
 Standards: Ontop relies on OWL 2 QL and RDFS as its primary ontology languages. OWL 2 QL is a profile of the Web Ontology Language specifically designed for efficient query rewriting, based on the DL-Lite family of description logics.
 Role: The ontology hides the structure of the underlying data sources and enriches the data with background knowledge, such as subclass and subproperty hierarchies.
 Reasoning: The system compiles the ontology into the mappings (creating T-mappings) to support reasoning without materialisation. Recently, Ontop has extended its input capabilities to support a fragment of SWRL (Semantic Web Rule Language) for more complex rule-based logic.

The Mappings

Mappings are the critical link between the ontology and the data. They provide a declarative specification that relates the terms in the ontology to SQL views over the data.

Structure: A mapping assertion consists of two parts:

Source: An SQL query that retrieves specific data from the database.

Target: A template that constructs RDF triples using the values returned by the source query.

Languages: Ontop supports two input formats for mappings:

- R2RML: The W3C standard language for mapping relational databases to RDF.
- Ontop Native Syntax: A simpler, concise syntax that is easier for humans to read and write. The system includes tools to convert between this native format and R2RML.
 Data Integration: Mappings handle the logic required to integrate data. For example, they can generate URIs from database keys to ensure that entities from different tables (or databases) are treated as the same object, or use `owl:sameAs` to state equality explicitly.
3. The Database (Data Sources)
The data sources act as the storage layer where the actual data resides. Ontop does not store data itself but connects to these external sources.
 Relational Databases: The system supports standard relational database engines via the JDBC interface. This includes major commercial systems (Oracle, DB2, MS SQL Server) and open-source engines (PostgreSQL, MySQL, H2).
 Federation: As an input, the database layer can be a federated database. By connecting to federation engines like Teiid or Exareme, Ontop can treat multiple heterogeneous sources (including XML, CSV, and Web Services) as a single virtual relational schema.
 Schema Constraints: The system utilises the database's integrity constraints (such as primary and foreign keys) as input for its Semantic Query Optimization (SQO) module, which is essential for generating efficient SQL.
4. The Query
The final input is the user's information request, expressed in SPARQL.
 Standards Compliance: Ontop accepts SPARQL 1.0 and almost all features of SPARQL 1.1. This includes complex features like aggregates (`SUM`, `COUNT`), solution modifiers (`LIMIT`, `ORDER BY`), and negation (`MINUS`, `FILTER NOT EXISTS`).
 Entailment: The queries are processed under the OWL 2 QL entailment regime, meaning the answers reflect not just the explicit data in the database, but also facts inferred from the ontology axioms.
Analogy
You can view the Inputs of the Ontop architecture like the essential components of a High-End Restaurant.

The Database is the Pantry. It is full of raw ingredients (Data) stored on shelves (Tables). The layout makes sense to the stock manager (DBA), but a customer wouldn't know where to find anything or how to eat it raw.

The Ontology is the Menu. It lists items like "Spaghetti Carbonara" (Concepts) that the customer understands and desires. It describes the food conceptually without explaining the physics of cooking it.

The Mappings are the Recipes. They bridge the gap. A recipe tells the kitchen: "To make the 'Carbonara' listed on the Menu (Target), go to the Pantry, take eggs from shelf A and pasta from shelf B (Source), and combine them this specific way."

The Query is the Customer's Order. The customer looks at the Menu and says, "I want the Carbonara, but without pepper" (SPARQL). The kitchen (Ontop) then uses the Recipe (Mapping) to fetch the right ingredients from the Pantry (Database) to serve the request.
