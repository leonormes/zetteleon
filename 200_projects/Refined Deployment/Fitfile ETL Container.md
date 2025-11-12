---
aliases: []
confidence: 
created: 2025-11-04T15:12:08Z
epistemic: 
last_reviewed: 
modified: 2025-11-12T14:24:27Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Fitfile ETL Container
type: 
uid: 
updated: 
---

## Fitfile ETL Container

*version tag: v0.4.1*

This document describes the technical details of the Extract-Transform-Load (ETL) docker container developed by The Hyve, that takes care of OMOP data harmonisation within the EoE NHS project. (TODO: correct project title). This document does not describe the functional designs of the project - the reader is assumed to be familiar with this though other sources.

The ETL container is deployed within the Fitfile platform and is not developed or intended as a standalone product.

![ETL container in context](generated/images/overall-context.png)

*The ETL container in its context. The first 3 items in this diagram will be explained.*

This document describes the ETL container as it is intended to function at the end of the development project. At the time of writing (June 2025), two components are not yet in their intended final form:

1. The ETL scripts (Python scripts implementing the actual data transformations) are currently embedded inside the container. The goal is that these NHS site specific scripts reside in a Github repository provided by HIE, and the container is only passed an identification of the NHS site, a Github location, and optionally credentials;
2. The source data is not yet a copy/extract database of the live data of an NHS site. Instead, synthetic data is used, embedded inside the container.

As a consequence, the ETL container is currently not generic for the project, but requires a specific version to be built and deployed for each NHS site. The final version of the ETL container will be generic, meaning that only one version of the container can be used for all Fitfile deployments.

### Configuration Quick Reference

The following table lists the configurable items that can exist for the ETL container. Usually these are passed in as an environment variable.

| Item | Status | Environment Variable | Description | Required |
|------   |--- |----- |------------- |--- |
| NHS Site | implemented | `NHS_SITE` | Site name for which the ETL container instance is running | Yes |
| Source database | planned | `SITE_SOURCE_DB` | Server and credentials for the site's source data | Yes |
| Target OMOP database | implemented | `OMOP_TARGET_DB` | Server and credentials for the site's target (OMOP) database| Yes |
| Github repository | planned | `ETL_REPOSITORY` | Repository location for ETL scripts, used together with `NHS_SITE` to determine the location of the scripts | Yes |
| Github tag | planned | `ETL_SCRIPTS_TAG` | Tag that identifies the version of the ETL scripts to be used | Yes |
| Github private key | planned | `ETL_REPO_KEY` | Private key to be used to access the Github repository | Yes |
| Data Quality reports/logs location (inside container) | implemented | `QCR_REPORTS_PATH` | Location where data quality reports and logs are written within the container. Defaults to `/tmp/reports` if not provided | No
| Data Quality reports/logs location | planned | TBD | Location/credentials of S3 bucket where data quality reports and logs will be written to. | No
| Data Quality reports/logs local HTTP access point | implemented | -- | The ETL container runs a small webserver that gives HTTP access to the directory where DQ reports and logs are written (see `QCR_REPORTS_PATH`). The ETL container runs this webserver at port 9000

## Source Data

*Please Note: the description below is not implemented yet. Instead, synthetic data representing the structure and typical content of the database is embedded within the container.*

The source data for the OMOP harmonization process implemented by the ETL container is a PostgreSQL database that contains a copy or extract of the EHR data of the NHS site. The ETL scripts have been developed based on meta information describing the structure and contents of the source data. Changes to the structure of the source data imply that the ETL scripts should be adapted to these changes.

## ETL Container

![Components of the ETL pipeline container](generated/images/etl-pipeline.png)

The (docker) ETL container contains these components:

1. Apache Airflow as the workflow engine that schedules and coordinates the steps to be executed when the ETL pipeline is invoked. In principle the invocation of the ETL pipeline is intended to be triggered at regular intervals by the scheduler of Airflow, but it is also possible to invoke the ETL pipeline, or parts of it, through the web interface that Airflow provides;
2. Delphyne. This is a Python library developed by The Hyve that implements a large number of standard functions required by an ETL implementation;
3. Data Quality tools. This is a set of standard data quality tools from the OHDSI community and the IMI EHDEN project: Data Quality Dashboard (DQD), Achilles, CdmOnboarding package.
4. Athena vocabularies data files. The ETL pipeline requires these vocabularies. When the environment for the ETL pipeline is initialized, these vocabularies are loaded into a separate schema in the target database (data sink); An update of the Athena vocabularies is published every 6 months.
5. ETL scripts. For each NHS site, ETL scripts are developed in Python. These scripts take care of the transformation of the site specific data into OMOP harmonized data.  
*Currently, the scripts for each NHS site are part of the container. Eventually, these scripts will reside in a Github repository, and will be pulled from there into the container.*

This document does not list the versions used of the components. These can be derived from the [Dockerfile](https://github.com/thehyve/fitfile_etl_container/blob/main/Dockerfile) in the Github repository of this project.

The Dockerfile should also be used as a reference for how the container is constructed. A few notes on some choices:

## Target Database: Harmonized Data and Related

![Target database: schema overview](generated/images/harmonized-data.png)

The target database contains the schema's, for the harmonized data and source data/minimally transformed data, and a number of schema's needed to support the harmonization process.

### Harmonized Data (OMOP CDM)

This schema contains the results of the ETL harmonization process. The schema is structured according to OMOP CDM version 5.4 .

### Source Data

Copy of the source data, with restricted access.

#### Source Data (filtered)

This schema contains the source data for the ETL pipeline, excluding the restricted codes.

### Restricted Codes

TODO

### Cdm-results-schema (TODO: Better title)

TODO

### Vocabularies

This schema contains the Athena vocabularies, loaded from the vocabulary files provided by the ETL container.

## Context

To be able to function within the Fitfile system, the ETL container needs access to a number of components that should be provided in its context:

1. a data source, typically a copy/extract of the patient database of an NHS site. In the current implementation this is expected to be in the form of a PostgreSQL database (currently the data source is synthetic data residing inside the container);
2. a data sink, where the harmonised data will reside, together with associated data supporting the functionality of the Fitfile platform. This is a PostgreSQL database as well;
3. a Github repository that contains the ETL scripts for each NHS site.
4. a location where data quality (DQ) reports and logs files can be written to. This is planned to be an AWS S3 bucket provided by HIE.

### Interfaces

For the above components, a number of interfaces are defined for the ETL container. These interfaces are usually defined as a location (or server) and set of credentials. These credentials should be made available to the ETL container in a secure way. These interfaces are described in the [configuration quick reference](#configuration-quick-reference) at the top of this document.

There is an additional interface that can optionally be used by an NHS site to access the DQ reports and logs directly. This is implemented as a small web server that gives access to the directory where these files are stored through the HTTP protocol. For this interface to be accessible, the port of the interface needs to be exposed by Fitfile. The current configuration for the port is 9000.
