---
title: "Redesigning complex OMOP querying capabilities - FITFILE"
source: "https://fitfile.atlassian.net/wiki/spaces/FITFILE/pages/2529361943/Redesigning+complex+OMOP+querying+capabilities"
captured: "2026-04-16T11:41:53+01:00 2026-04-16T11:41:53+01:00"
status: "processing"
tags:
  - "input"
type: "head"
---
## Raw Output / Content
## Redesigning complex OMOP querying capabilities

## I. Introduction

==There is a need to expand and redesign how data consumers interact with relational data sources in the FITFILE application (e.g. OMOP), specifically how they query those data sources and extract information (e.g. as specified in a Data Access Request or DAR).==

The redesigned experience should support the following minimal end-to-end steps:

### Project Extract Use Case

1. **Understanding data availability**  
	Identify what data is available to the user and verify whether the data requested in the DAR can be queried across different data providers.
2. **Selecting Data Providers and Data Sources**  
	Select data sources from one or more data providers.
3. **Navigating the OMOP Data Model**  
	Select data fields from specific relational data sources (e.g. particular OMOP ==tables==) that comply with data minimisation without breaking the integrity of the data.
4. **Applying filtering criteria**  
	Apply filtering criteria (e.g. defined in the DAR), both at:
	- ==the cohort level, and==
		- ==the table/data field level.==
5. **Applying privacy treatment measures**  
	Apply appropriate privacy treatments so the resulting data is de-identified or anonymised to the required degree.
6. **Linking data across Providers**  
	Receive linked, record-level results consolidated across all selected data providers.
7. **Exporting results**  
	Export the results in the preferred format to a designated location.

### Cohort Discovery Use Case

For the cohort discovery use case, steps 1–4 remain the same. However, privacy treatment is not required, as the output is limited to aggregated statistical counts rather than record-level data.

---

## II. East of England (SDE) Use Case

### 1\. Understanding data availability

The SDE Data Manager is familiar with the OMOP Common Data Model (CDM) schema (v5.4):  
[OMOP CDM v5.4](https://ohdsi.github.io/CommonDataModel/cdm54.html)

However, they need to ==understand:==

- ==which OMOP fields are available from each data provider, at the individual field level==
- ==what values or distributions exist within those fields==
- What is the relationship between interlinked OMOP fields, and which fields are mandatory to query together in order to preserve context within the CDM

This information is required to determine whether requesting a specific ==field== from a given OMOP table will satisfy the requirements defined in the DAR. For example, if the DAR specifies certain condition, the Data Manager needs to confirm whether the `condition_concept_id` field contains those values.

---

### 2\. Selecting Data Providers and Data Sources

The primary goal of the SDE is to query and link patient-level information across multiple data providers in order to define and analyse cohorts for research purposes.

This can be achieved by the user who selects the relevant data sources (e.g. synthetic or live, harmonised data), and selects the appropriate data providers that are connected to the SDE network of Nodes - all within an operation launched from the SDE Node.

---

### 3\. Navigating the OMOP Data Model

The OMOP Common Data Model typically consists of 39 core tables, organised into ==domains== such as:

- **Core patient data**: PERSON
- **Clinical events**: CONDITION\_OCCURRENCE, DRUG\_EXPOSURE, PROCEDURE\_OCCURRENCE, MEASUREMENT, OBSERVATION
- **Healthcare encounters**: ==VISIT\_OCCURRENCE, VISIT\_DETAIL==
- **Healthcare system context**: LOCATION, CARE\_SITE, PROVIDER
- **Vocabulary**: ==CONCEPT==, VOCABULARY, RELATIONSHIP, and r ==elated tables==
- **Summary:** DRUG\_ERA and CONDITION\_ERA (“ERA” tables are derived summary tables - they aggregate individual clinical events into longer, clinically meaningful periods and are auto-generated)

While the exact number of tables may vary slightly by CDM version, the key characteristic is the relational structure that links tables through shared identifiers to provide a unified longitudinal view of patient data.

The DAR explains what information is expected in the output, and it is the SDE Manager’s role to configure the operation query in such a way that it will return the expected results. The below are some domain specific complexities they may struggle with:

- which OMOP tables contain the required information,
- which tables and fields are mandatory (key domains),
- how to select the correct combination of tables and fields without breaking OMOP structural dependencies, and
- how to define the cohort and table filters based to receive expected data fields.

This requires a deep understanding of how DAR-defined requirements map to OMOP domains and how information is distributed across tables.  

Using an existing DAR as an example, the researcher needs the following data fields:  
  
All patients with a coded diagnosis of CMD (e.g diabetes, hypercholesterolemia, cerebrovascular disease, cardiovascular disease, heart failure and hypertension, see SNOMED code see tables at bottom of file).

Aged >18 years old and:

- Demographics (Age, sex, ethnic group, race, education (level/years))
- Comorbidities \[all recorded secondary diagnoses\]
- Vital signs (weight, height, blood pressure, heart rate, oxygen saturation)
- Routinely collected blood test results (liver, renal and thyroid functions, glucose, HbA1c, haematology tests, troponin and N-terminal pro B-type natriuretic peptide, thyroid function.)
- Current and previous medications
- Date of symptom onset and first symptom
- Specific primary diagnosis and date
- Name of treatment centre
- Past hospital admissions \[date & primary diagnostic code & length of stay\]
- Smoking history
- Date of death if applicable  
	  
	==Snippet of how the SQL has to be defined:==  
	**==\-- cohort filters==**  
	==person\_id IN==
	==(SELECT person\_id==
	==FROM cdm.condition\_occurrence==
	==WHERE condition\_concept\_id IN (13348267, 1746282)==
	==)==  
	==AND (SELECT person\_id FROM cdm.person WHERE year\_of\_birth > 2007)==  
	**==\-- Additional filters (tables)==**
	==AND measurement\_concept\_id IN (7427834, 3484784);==

### How data fields map to the OMOP tables

<table><tbody><tr><th rowspan="1" colspan="1"><div><p>Requirement</p><figure></figure></div></th><th rowspan="1" colspan="1"><div><p>Source table(s)</p><figure></figure></div></th></tr></tbody></table>

<table><tbody><tr><th rowspan="1" colspan="1"><div><p>Requirement</p><figure></figure></div></th><th rowspan="1" colspan="1"><div><p>Source table(s)</p><figure></figure></div></th></tr><tr><td rowspan="1" colspan="1"><p>Age > 18</p></td><td rowspan="1" colspan="1"><p><code>person</code></p></td></tr><tr><td rowspan="1" colspan="1"><p>Demographics</p></td><td rowspan="1" colspan="1"><p><code>person</code>, <code>observation</code> (education data is not stored in OMOP table)</p></td></tr><tr><td rowspan="1" colspan="1"><p>Comorbidities</p></td><td rowspan="1" colspan="1"><p><code>condition_occurrence</code></p></td></tr><tr><td rowspan="1" colspan="1"><p>Vital signs</p></td><td rowspan="1" colspan="1"><p><code>measurement</code></p></td></tr><tr><td rowspan="1" colspan="1"><p>Laboratory blood results</p></td><td rowspan="1" colspan="1"><p><code>measurement</code></p></td></tr><tr><td rowspan="1" colspan="1"><p>Medications</p></td><td rowspan="1" colspan="1"><p><code>drug_exposure</code></p></td></tr><tr><td rowspan="1" colspan="1"><p>Symptom onset</p></td><td rowspan="1" colspan="1"><p><code>observation</code> or <code>condition_occurrence</code> (depending on site)</p></td></tr><tr><td rowspan="1" colspan="1"><p>Primary diagnosis + date</p></td><td rowspan="1" colspan="1"><p><code>condition_occurrence</code> (+ <code>visit_occurrence</code> if needed)</p></td></tr><tr><td rowspan="1" colspan="1"><p>Treatment centre</p></td><td rowspan="1" colspan="1"><p><code>care_site</code> joined via visit if required</p></td></tr><tr><td rowspan="1" colspan="1"><p>Admissions + lenght of stay</p></td><td rowspan="1" colspan="1"><p><code>visit_occurrence</code></p></td></tr><tr><td rowspan="1" colspan="1"><p>Smoking</p></td><td rowspan="1" colspan="1"><p><code>observation</code></p></td></tr><tr><td rowspan="1" colspan="1"><p>Death</p></td><td rowspan="1" colspan="1"><p><code>death</code></p></td></tr></tbody></table>

---

### 4\. Applying filtering criteria

The East of England team has provided example DARs Pharma Opportunity 21 Nov 25 (2).pptx [20251010\_building\_SDE\_datasets\_using\_fitfile.docx](https://eahsn.sharepoint.com/:w:/r/sites/EoESub-NationSDEWP2-12_DataHarmonisation2/Shared%20Documents/Data%20Harmonisation/02_Data/20251010_building_SDE_datasets_using_fitfile.docx?d=wc3a22eac4819470dbdccf4310ef12ef8&csf=1&web=1&e=1cwXnr "https://eahsn.sharepoint.com/:w:/r/sites/EoESub-NationSDEWP2-12_DataHarmonisation2/Shared%20Documents/Data%20Harmonisation/02_Data/20251010_building_SDE_datasets_using_fitfile.docx?d=wc3a22eac4819470dbdccf4310ef12ef8&csf=1&web=1&e=1cwXnr") that specify the exact data required for research use.

Each DAR includes filtering criteria that must be applied at two levels:

- **Cohort-level filtering**, e.g.  
	`year_of_birth < 2007`
- **Table-level filtering**, e.g.  
	`condition_concept_id IN (201254, 201820, 201826, 319835, 320128, 4028244, 4028265, 4028367, 4029305)`

Currently, to translate human-readable clinical conditions from the DAR into OMOP concept IDs, users must rely on external tools such as Athena:  
[https://athena.ohdsi.org/search-terms/start](https://athena.ohdsi.org/search-terms/start)

A user guide has been created to explain how to identify and generate OMOP vocabulary concepts for use in queries: 20251023\_EoE\_SDE\_FITFILE\_OMOP Data Querying - User Guide v1.0.pdf

For complex queries that involve large numbers of concept IDs ==and tables==, this ==process== is:

- time-consuming, and
- error-prone, due to manual copying and transfer of many IDs.

This creates a significant usability and reliability ==challenge.==

---

### 5\. Applying privacy treatment measures

***The SDE Manager must ensure that no identifiable data is released to the researcher from SDE Node.***  
  
***The SDE Manager must ensure that direct identifiers are removed prior to any data leaving the data provider’s perimeter and take all reasonable precautions to ensure that the remaining data is transformed to a degree that minimises the risk of re-identification.***

The SDE Manager must assess re-identification risk and decide whether the output is safe to share with the researcher. This may involve:

- running and inspecting profile of the data at source (before it leaves the data provider perimeter)
- ==inspecting outputs==,
- adjusting transformations, or
- removing ==fields== entirely if the risk is too high.

#### Privacy Treatment Options in FITFILE

FITFILE currently supports two approaches:

**a) Automated privacy treatment (k-anonymity)**

- Selected fields are evaluated collectively (in combination)
- Protocol transforms the data fields based on schema classification and uniqueness (equivalence classes)
- Transformations are applied automatically to reduce risk while preserving utility.

This approach works well for outputs with up to approximately 7 columns. However, for complex SDE queries with ~100 columns, this method is not viable, as it would likely nullify most of the data and severely reduce utility.

**b) Custom ==field-level== transformations**  
Users can apply transformations to ==individual fields or grouped fields (grouped according to context and relationships between fields)== based on data type to reduce re-identification risk.

Within the ==OMOP harmonised== context, the ==applicable transformations== are:

- ==date shifting (on individual or grouped fields)==
- bucketisation
- low-count suppression
- replacement
- outlier removal
- column removal
- rounding

None of the proposed transformations may compromise the integrity of the OMOP structure, meaning that if a field can only be transformed as part of a group of fields, this constraint must be suggested to the user.  
  
==These transformations can be chained. However, changes to data types (e.g. casting to integer) must be carefully managed, as they affect both execution and expected output schemas.==

---

### 6\. Linking data across Providers

The objective is to produce a single operational output for each research project/use case that consolidates data from ==multiple data providers.==

Data linkage is performed using a direct overlapping identifier present across all providers. The linkage process must:

- identify overlapping patient records and consolidate them, and
- enrich the cohort with non-overlapping patients from each provider.

---

### 7\. Exporting results

Data export requirements include:

1. **Export location**  
	After reviewing and approving the output, the SDE Manager exports the data to a designated ==S3 bucket so it can be later moved to Project Research Environment (PRE) by the SDE team==.
2. **==Export formats==**  
	Two output formats are required:
	- **OMOP-compliant output**:  
		All OMOP tables generated individually based on filtering and linkage, including empty tables where applicable, and empty column values - either nulls or concept\_id '0' to represent missing or removed values. This format is intended for downstream analysis using tools such as “R” software.

*Example of the output tables:*

### PERSON table

<table><tbody><tr><th rowspan="1" colspan="1"><div><p>person_id</p><figure></figure></div></th><th rowspan="1" colspan="1"><div><p>gender_concept_id</p><figure></figure></div></th><th rowspan="1" colspan="1"><div><p>year_of_birth</p><figure></figure></div></th><th rowspan="1" colspan="1"><div><p>month_of_birth</p><figure></figure></div></th><th rowspan="1" colspan="1"><div><p>day_of_birth</p><figure></figure></div></th><th rowspan="1" colspan="1"><div><p>race_concept_id</p><figure></figure></div></th><th rowspan="1" colspan="1"><div><p>ethnicity_concept_id</p><figure></figure></div></th></tr></tbody></table>

<table><tbody><tr><th rowspan="1" colspan="1"><div><p>person_id</p><figure></figure></div></th><th rowspan="1" colspan="1"><div><p>gender_concept_id</p><figure></figure></div></th><th rowspan="1" colspan="1"><div><p>year_of_birth</p><figure></figure></div></th><th rowspan="1" colspan="1"><div><p>month_of_birth</p><figure></figure></div></th><th rowspan="1" colspan="1"><div><p>day_of_birth</p><figure></figure></div></th><th rowspan="1" colspan="1"><div><p>race_concept_id</p><figure></figure></div></th><th rowspan="1" colspan="1"><div><p>ethnicity_concept_id</p><figure></figure></div></th></tr><tr><td rowspan="1" colspan="1"><p>1001</p></td><td rowspan="1" colspan="1"><p>8507</p></td><td rowspan="1" colspan="1"><p>1975</p></td><td rowspan="1" colspan="1"><p>5</p></td><td rowspan="1" colspan="1"><p>12</p></td><td rowspan="1" colspan="1"><p>8527</p></td><td rowspan="1" colspan="1"><p>38003563</p></td></tr><tr><td rowspan="1" colspan="1"><p>1002</p></td><td rowspan="1" colspan="1"><p>8532</p></td><td rowspan="1" colspan="1"><p>1982</p></td><td rowspan="1" colspan="1"><p>NULL</p></td><td rowspan="1" colspan="1"><p>NULL</p></td><td rowspan="1" colspan="1"><p>0</p></td><td rowspan="1" colspan="1"><p>38003563</p></td></tr><tr><td rowspan="1" colspan="1"><p>1003</p></td><td rowspan="1" colspan="1"><p>8507</p></td><td rowspan="1" colspan="1"><p>1968</p></td><td rowspan="1" colspan="1"><p>11</p></td><td rowspan="1" colspan="1"><p>4</p></td><td rowspan="1" colspan="1"><p>8516</p></td><td rowspan="1" colspan="1"><p>NULL</p></td></tr></tbody></table>

### CONDITION\_OCCURRENCE table

<table><tbody><tr><th rowspan="1" colspan="1"><div><p>person_id</p><figure></figure></div></th><th rowspan="1" colspan="1"><div><p>condition_concept_id</p><figure></figure></div></th><th rowspan="1" colspan="1"><div><p>condition_start_date</p><figure></figure></div></th><th rowspan="1" colspan="1"><div><p>condition_end_date</p><figure></figure></div></th><th rowspan="1" colspan="1"><div><p>condition_type_concept_id</p><figure></figure></div></th></tr></tbody></table>

<table><tbody><tr><th rowspan="1" colspan="1"><div><p>person_id</p><figure></figure></div></th><th rowspan="1" colspan="1"><div><p>condition_concept_id</p><figure></figure></div></th><th rowspan="1" colspan="1"><div><p>condition_start_date</p><figure></figure></div></th><th rowspan="1" colspan="1"><div><p>condition_end_date</p><figure></figure></div></th><th rowspan="1" colspan="1"><div><p>condition_type_concept_id</p><figure></figure></div></th></tr><tr><td rowspan="1" colspan="1"><p>1001</p></td><td rowspan="1" colspan="1"><p>201826</p></td><td rowspan="1" colspan="1"><p>2010-03-12</p></td><td rowspan="1" colspan="1"><p>2010-03-12</p></td><td rowspan="1" colspan="1"><p>44786627</p></td></tr><tr><td rowspan="1" colspan="1"><p>1001</p></td><td rowspan="1" colspan="1"><p>316866</p></td><td rowspan="1" colspan="1"><p>2012-07-01</p></td><td rowspan="1" colspan="1"><p>NULL</p></td><td rowspan="1" colspan="1"><p>44786627</p></td></tr><tr><td rowspan="1" colspan="1"><p>1002</p></td><td rowspan="1" colspan="1"><p>0</p></td><td rowspan="1" colspan="1"><p>NULL</p></td><td rowspan="1" colspan="1"><p>NULL</p></td><td rowspan="1" colspan="1"><p>NULL</p></td></tr><tr><td rowspan="1" colspan="1"><p>1003</p></td><td rowspan="1" colspan="1"><p>434056</p></td><td rowspan="1" colspan="1"><p>2015-01-20</p></td><td rowspan="1" colspan="1"><p>2015-01-20</p></td><td rowspan="1" colspan="1"><p>44786627</p></td></tr></tbody></table>

- **Single nested file output**:  
	A consolidated, patient-level file where each record includes fields from multiple OMOP tables

*Example of the single output:*

### PERSON table + CONDITION\_OCCURRENCE table + MEASUREMENT table + OBSERVATION table + DEATH table

<table><tbody><tr><th rowspan="1" colspan="1"><div><p>person_id</p><figure></figure></div></th><th rowspan="1" colspan="1"><div><p>condition_concept_id</p><figure></figure></div></th><th rowspan="1" colspan="1"><div><p>condition_start_date</p><figure></figure></div></th><th rowspan="1" colspan="1"><div><p>measurement_concept_id</p><figure></figure></div></th><th rowspan="1" colspan="1"><div><p>measurement_date</p><figure></figure></div></th><th rowspan="1" colspan="1"><div><p>measurement_value</p><figure></figure></div></th><th rowspan="1" colspan="1"><div><p>smoking_status_concept_id</p><figure></figure></div></th><th rowspan="1" colspan="1"><div><p>death_date</p><figure></figure></div></th></tr></tbody></table>

<table><tbody><tr><th rowspan="1" colspan="1"><div><p>person_id</p><figure></figure></div></th><th rowspan="1" colspan="1"><div><p>condition_concept_id</p><figure></figure></div></th><th rowspan="1" colspan="1"><div><p>condition_start_date</p><figure></figure></div></th><th rowspan="1" colspan="1"><div><p>measurement_concept_id</p><figure></figure></div></th><th rowspan="1" colspan="1"><div><p>measurement_date</p><figure></figure></div></th><th rowspan="1" colspan="1"><div><p>measurement_value</p><figure></figure></div></th><th rowspan="1" colspan="1"><div><p>smoking_status_concept_id</p><figure></figure></div></th><th rowspan="1" colspan="1"><div><p>death_date</p><figure></figure></div></th></tr><tr><td rowspan="1" colspan="1"><p>1001</p></td><td rowspan="1" colspan="1"><p>201826</p></td><td rowspan="1" colspan="1"><p>2010-03-12</p></td><td rowspan="1" colspan="1"><p>3025315</p></td><td rowspan="1" colspan="1"><p>2022-01-15</p></td><td rowspan="1" colspan="1"><p>82</p></td><td rowspan="1" colspan="1"><p>8516</p></td><td rowspan="1" colspan="1"><p>NULL</p></td></tr><tr><td rowspan="1" colspan="1"><p>1001</p></td><td rowspan="1" colspan="1"><p>316866</p></td><td rowspan="1" colspan="1"><p>2012-07-01</p></td><td rowspan="1" colspan="1"><p>3012888</p></td><td rowspan="1" colspan="1"><p>2022-01-15</p></td><td rowspan="1" colspan="1"><p>120</p></td><td rowspan="1" colspan="1"><p>8516</p></td><td rowspan="1" colspan="1"><p>NULL</p></td></tr><tr><td rowspan="1" colspan="1"><p>1001</p></td><td rowspan="1" colspan="1"><p>434056</p></td><td rowspan="1" colspan="1"><p>2015-01-20</p></td><td rowspan="1" colspan="1"><p>3025315</p></td><td rowspan="1" colspan="1"><p>2023-03-10</p></td><td rowspan="1" colspan="1"><p>78</p></td><td rowspan="1" colspan="1"><p>8516</p></td><td rowspan="1" colspan="1"><p>NULL</p></td></tr></tbody></table>

For the single file option, it should be considered to include headers and labels (for foreign keys in vocabulary entries) so researchers can interpret the data without translating OMOP vocabulary manually (e.g. `condition_concept_id = 24673` → *Liver Failure*).

---

## III. Usability Considerations

==Key usability requirements include:==

- The full workflow (steps 1–7) should be configurable within a single operation workflow to minimise the steps the user needs to configure.
- Users must be able to edit operation configuration:
	- during setup, and
		- after execution, based on output inspection.
- The system should minimise the level of OMOP and ==SQL expertise== required by:
	- guiding OMOP table and data field selection,
		- introducing automated protocols for easier ==configuration== e.g. ==custom transformation== recommended approach for each OMOP tables
		- ==simplifying filtering logic for cohort and OMOP tables,==
- Users must be warned if their output includes ==direct identifiers== (e.g. NHS number), as such fields should not leave the data provider perimeter.
- The system should guide users on mandatory OMOP tables and fields to prevent breaking domain hierarchies.
- ==Users should understand the availability of data fields across providers and the distribution of field values to verify that the fields contain the information specified in the DAR before initiating a query, supporting cost-effectiveness and data exploration.==
- The system must support complex queries involving multiple cohort filters and large concept ID lists (ideally generated within the FITFILE system or have an easy way to ingest large lists generated externally).
- Operations, configurations, and ==outputs== must be easy to locate, trace, and distinguish, as users may run multiple queries daily.
- Users should be warned when query configurations are likely to result in excessively large data volumes or failed operations.
- Query operation error messages should be improved so the user can try to troubleshoot by changing the query configuration themselves (reduce the depandancy on FITFILE team).
- The long term (c 10 month) goal for this process is to become a self-service for SDE Manager (reduce the dependancy on FITFILE team).
- Generation of the concept\_id table should be streamlined, or at least considered how we can assist the user in more automated fashion (need an approach that wouldn't require the user to have to define every single join).
- Users must be able to choose between:
	- automated privacy treatment, or
		- fully custom privacy configuration.
- ==Users need a mechanism to generalise data hierarchically so grouping values into broader concepts, so that each group contains a sufficient number of entities to protect privacy and support meaningful analysis.==
- Users need guidance on when transformations must be applied to grouped fields to avoid compromising OMOP structure integrity, prevent illogical results, or inadvertently reveal sensitive information.
- If the user selects duplicated fields, they should be informed about it so they can change the query configuration
- The existing system functionalities and features have to be working correctly for this improved process, the following should be considered:  
	\- Data Catalogue  
	\- Format of the outputs (single and multiple files) and how would they integrate into Data Catalogue and Data Operations ~ consider Data Collections (as we have an output with multiple datasets similar to Data Sources concept)  
	\- The data output could be used as an input for another operation  
	\- Permission structure that is based on data sources, data sets and projects  
	\- Data Disclosure  
	\- Small Number Suppression on tenant level  
	  
	DRAFT:
- ==the users would benefit from being able to explore the data before running the final queries. This could be allowing them to output 10 top records or something similar==

---

## IV. Proposed Solution

Step 1: Preparation to configure the operation query (Data Catalogue + Data Profile)

**User Story 1 – Understanding Data Availability**

==As an== SDE Data Manager,  
I want to view which OMOP tables, fields, and values are available from each data provider,  
so that I can determine whether the data requested in a DAR can be satisfied before configuring a query.

**Value**

- Reduces failed or invalid queries
- Enables informed decision-making early in the workflow

**Key Behaviours**

- View OMOP schema and field availability per provider
- Inspect value distributions (e.g. concept presence)
- Get the count and the description against data field in OMOP (glossary)
- Validate DAR feasibility
![Screenshot 2025-12-19 at 16.57.46.png](https://media-cdn.atlassian.com/file/9f25c198-104c-4b13-b63f-a807569f31d6/image/cdn?allowAnimated=true&client=79d9a90a-d0b1-4ba1-9c4d-7fda8295d8c2&collection=contentId-2529361943&height=125&max-age=2592000&mode=full-fit&source=mediaCard&token=eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiI3OWQ5YTkwYS1kMGIxLTRiYTEtOWM0ZC03ZmRhODI5NWQ4YzIiLCJhY2Nlc3MiOnsidXJuOmZpbGVzdG9yZTpjb2xsZWN0aW9uOmNvbnRlbnRJZC0yNTI5MzYxOTQzIjpbInJlYWQiXX0sImV4cCI6MTc3NjMzODk4MiwibmJmIjoxNzc2MzM2MTAyLCJhYUlkIjoiNjMzYWUyYjlmZWRjNjE2OWFlZDhmNjAxIiwiaHR0cHM6Ly9pZC5hdGxhc3NpYW4uY29tL2FwcEFjY3JlZGl0ZWQiOmZhbHNlLCJhdXRoVHlwZSI6InNlc3Npb24ifQ.Lg0aooGkyNiekAAwMRDvlQg4wCtwSjAVAZ-GF0kG_l8&width=415#media-blob-url=true&id=9f25c198-104c-4b13-b63f-a807569f31d6&clientId=79d9a90a-d0b1-4ba1-9c4d-7fda8295d8c2&contextId=contentId-2529361943&collection=contentId-2529361943)

Step 2: Select the relevant information from DAR (specify the OMOP tables and fields)  
  
**User Story 2 – Navigating the OMOP Data Model** → **Table and Field Selection**

As an SDE Data Manager,  
I want to select the OMOP tables and fields required for my research output without breaking OMOP domain relationships,  
so that the resulting dataset remains structurally valid and usable for downstream analysis.

**Value**

- Preserves OMOP compliance
- Prevents structurally invalid outputs

**Key Behaviours**

- Guided selection of tables and ==mandatory fields==
- Warnings when dependencies are missing
- Reduced need for expert OMOP knowledge
![Screenshot 2025-12-19 at 16.58.42.png](https://media-cdn.atlassian.com/file/23ff1a8d-d02e-46a3-921a-d25489d91e5d/image/cdn?allowAnimated=true&client=79d9a90a-d0b1-4ba1-9c4d-7fda8295d8c2&collection=contentId-2529361943&height=125&max-age=2592000&mode=full-fit&source=mediaCard&token=eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiI3OWQ5YTkwYS1kMGIxLTRiYTEtOWM0ZC03ZmRhODI5NWQ4YzIiLCJhY2Nlc3MiOnsidXJuOmZpbGVzdG9yZTpjb2xsZWN0aW9uOmNvbnRlbnRJZC0yNTI5MzYxOTQzIjpbInJlYWQiXX0sImV4cCI6MTc3NjMzODk4MiwibmJmIjoxNzc2MzM2MTAyLCJhYUlkIjoiNjMzYWUyYjlmZWRjNjE2OWFlZDhmNjAxIiwiaHR0cHM6Ly9pZC5hdGxhc3NpYW4uY29tL2FwcEFjY3JlZGl0ZWQiOmZhbHNlLCJhdXRoVHlwZSI6InNlc3Npb24ifQ.Lg0aooGkyNiekAAwMRDvlQg4wCtwSjAVAZ-GF0kG_l8&width=736#media-blob-url=true&id=23ff1a8d-d02e-46a3-921a-d25489d91e5d&clientId=79d9a90a-d0b1-4ba1-9c4d-7fda8295d8c2&contextId=contentId-2529361943&collection=contentId-2529361943)

Step 3: Apply filtering criteria to cohort and selected OMOP tables

**User Story 3 – Applying DAR filtering criteria**  
  
As an SDE Data Manager,  
I want to apply cohort-level and table-level filters defined in a DAR,  
so that I can precisely identify the population and clinical events required for the research.

**Value**

- Ensures DAR compliance
- Supports complex research criteria

**Key Behaviours**

- Apply demographic (cohort) filters
- Apply domain-based filters using OMOP vocabularies
- Support large ==concept== lists without ==manual error==

Step 4: Apply privacy-treatment transformations

**User Story 4 – Applying de-identification measures (privacy treatment)**

As an SDE Data Manager,  
I want to assess re-identification risk and apply appropriate privacy transformations to the output,  
so that no identifiable data is disclosed to the researcher and governance requirements are met.

**Value**

- Protects patient privacy
- Ensures regulatory compliance

**Key Behaviours**

- Warning regarding the direct identifiers in the output
- Option to apply automated k-anonymity for less complex outputs (==<=== than 7 columns)
- Option to apply automated custom transformation protocol (that considers OMOP hierarchy and transforms grouped data fields)
- Ability to manually configure custom ==field-level transformations with guidance to prevent nonsensical or invalid configurations==

Step 5: Select the data sources that needs to be linked (data from multiple data providers)

**User Story 5 – Linking Data Across Providers**

As an SDE Data Manager,  
I want my cohort to include patient records from multiple data providers  
so that I receive a unified dataset representing a single cohort across institutions.

**Value**

- Enables multi-institutional research
- Avoids duplication of patient records

**Key Behaviours**

- Identify overlapping patients via direct identifiers
- Consolidate records for the same patient
- Enrich the cohort with unique patients from each provider

Step 6: Run the operation and check its status & Step 7: Investigate the results and operation configuration

**User Story 6 & 7 – Operation Management**

As an SDE Data Manager,  
I want to ==configure==, run, inspect, edit, ==rerun,== and trace my operations from a single interface,  
so that I can efficiently manage multiple complex queries on a daily basis.  
  
As an SDE Data Manager,  
I want to know if my query operation will result in ==high-volume== output  
so I can spot filtering and configurability issues and edit my query if necessary

**Value**

- Full configurability of the operations
- Ensures auditability and traceability

**Key Behaviours**

- Single-operation configuration for all steps
- Post-run editing and ==inspection==
- Clear visibility of configurations and ==outputs (including versioning)==
- Warnings for high-risk or high-volume queries

Step 7: Investigate the results and operation configuration

Step 8: Export the operation output  

**User Story 8 – Exporting Results**

As an SDE Data Manager,  
I want to export the operation results in a researcher-ready format to a secure location,  
so that researchers can immediately use the data for analysis.

**Value**

- Fulfilling the DAR submitted by researcher
- Enable the research and recruitment use cases

**Key Behaviours**

- Export to a designated PRE S3 bucket
- Choose between OMOP-compliant or ==nested== output formats
- Include human-readable labels for clinical concepts
- Ensure final approval before export

V) Implementation details for each Step

VI) Phases of development

MVP

Phase II

Phase III

Related content
