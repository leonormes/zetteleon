# Technical details of the data linkage algorithm

![rw-book-cover](https://digital.nhs.uk/webfiles/1750159430455/images/nhs-england-logo-social.jpg)

## Metadata
- Author: [[NHS England Digital]]
- Full Title: Technical details of the data linkage algorithm
- Category: #articles
- Summary: The data linkage algorithm matches records by checking mandatory fields like family name, year of birth, and gender, and if no match is found, it uses additional methods to find potential matches. If a record is still unmatched, a new identifier (MPS_ID) may be created. The algorithm also tracks which matching method was used and provides scores based on the match quality.
- URL: https://digital.nhs.uk/services/personal-demographics-service/master-person-service/the-person_id-handbook/technical-details-of-the-data-linkage-algorithm

## Full Document
1. 
2. 
3. 
4. 
5. 

####  Overview of Master Person Service (MPS)

The process to link a given record to an existing person identifier happens across DPS and Spine as described in Figure 1.

![Creation of Person_ID via MPS process flow (high-level)](https://digital.nhs.uk/binaries/content/gallery/website/services/personal-demographics-service/master-person-service-mps/february/figure-1.svg)
**Figure 1. Creation of Person\_ID via MPS process flow (high-level)**

Figure 1 illustrates the entire workflow of how the Person\_ID is assigned to a data set. This section provides a high-level explanation of the diagram, while more details are given in the following sections.

The workflow starts on DPS core with the request of the Person\_ID that corresponds to a record in the data set, this is also referred to as the ‘request query record’. The request query can also be triggered outside of DPS as part of Master Person Service as a Service (MPSaaS) which is out of the scope of this document.

The pipeline in DPS core first maps the data to the request file fields. Where the NHS number and DOB are provided, DPS cross-checks them against the local cached version of PDS and confirms the identity. This is the most straightforward step.

The records that could not be matched at this stage (either because one of these fields is empty or the information does not match with the reference, that is, PDS) are collected into a request file and sent via the Message Exchange for Social Care and Health (MESH) to MPS in Spine.

PDS is updated daily on DPS core, which makes the PDS cached version slightly different from the live version of PDS in Spine.

The request file goes through quality checks in MPS, and the demographic fields available for the record are used for the following tracing steps against the live version of PDS in Spine.

There are three tracing steps, cross-check, alphanumeric and algorithmic, the latter is the most computationally expensive. The tracing against PDS stops whenever a successful match is found, or if the record does not meet the eligibility criteria to proceed to the following step, or at the end of the last step. The HES databases skip the alphanumeric trace because the fields needed for this step are not available. For completeness, this is still discussed in the present document.

On top of NHS number and DOB, the cross-check trace in Spine uses name and outbound postcode if available. If no perfect match is found, the algorithm proceeds to the alphanumeric trace, where the mandatory fields (family name, year of birth and gender) are used to identify a match on PDS. If a match is not found (or the trace is not run for lack of demographics), MPS proceeds to the algorithmic trace step, where the single query record is compared to all records in PDS. The comparisons involve the same demographic information mentioned above plus gender and full postcode, and are scored based on similarity. If the similarity is deemed acceptable, the matched record is returned. Otherwise, the algorithm proceeds to look for similarities to previously unmatched records, stored in the MPS record bucket, a separate data set.

The MPS record bucket in the Spine’s data stfore is used to link records for the same person that cannot be traced in PDS. If a match is found, an MPS\_ID is returned, otherwise, the algorithm considers whether to create a new MPS\_ID. MPS\_ID is also known as UPRI 1 in certain documentations.

A new MPS\_ID can be created only when the minimum required fields are provided. If this is not the case, an empty MPS\_ID field is returned, and DPS core generates a one-time-use ID (also known as UPRI 2).

The MPS users will submit a file (request file) with the records that need to be matched. The file must follow the technical specification (see the [Request file section in the Appendix)](https://digital.nhs.uk/services/personal-demographics-service/master-person-service/the-person_id-handbook/appendix#request-file) which describes the 25 fields used in the matching process.

Once all the records have been processed in Spine, MPS will return a file (response file, see the [Response file in the Appendix](https://digital.nhs.uk/services/personal-demographics-service/master-person-service/the-person_id-handbook/appendix#response-file)) with the details of the transaction, like the number of data records included in the file, and the fields of interest such as the NHS number, the MPS\_ID, and others that provide information on the matching process.

####  Input data and validation

HES data sets obtain the Person\_ID field when processed via DPS core pipelines, similarly to any other data set in DPS which requires MPS tracing.

Among other things, it is the responsibility of the DPS pipeline author to:

* map the submitted fields into the MPS request schema – the request file is composed of the fields described in [Table 9 (n the Appendix](https://digital.nhs.uk/services/personal-demographics-service/master-person-service/the-person_id-handbook/appendix#request-file)). Not all the fields are required for MPS to find a match
* make sure that records are deduplicated based on the available demographic fields – this is done to reduce the computational burden

This may require varying levels of preparation work depending on whether all the relevant information is available within the same table, or whether it needs to be retrieved from multiple locations/tables.

The creation of the request file happens immediately after the data set has been processed via cross-check trace in DPS. Only the records that could not be matched in DPS are sent to MPS in Spine for further processing.

Before proceeding to the other tracing steps, the fields in the request file are validated with basic checks looking at whether mandatory data are present, data type, format and strings length are consistent. If the request file fails the validation, the entire process is unsuccessful, and the data is not processed further.

Once the data has been validated, empty fields are removed. The family, given and any other name are all changed to upper case. Invalid characters1 are removed from all fields except local patient identifier, internal identifier, telephone number, mobile number and e-mail address. The expected format of the postcode field is with a space in the middle. Such space is then replaced with underscore to match the postcodes in PDS. If this is not the case, the postcode field might not match correctly.

   Footnote 1  1 This is the list of invalid characters: '!', '$', '%', '&', '(', ')', '[', ']', '{', '}', '=', ':', ';', 'Number', '~', '@', '|', '<', '>', '.', '?', '/', '\_', '\\', '\xc2\xa3'

 
####  Cross-check trace (DPS and Spine steps)

Cross-check trace is the first and simplest tracing step, which can be used when an NHS number is present. The vast majority (above 99%) of HES records are matched using cross-check trace (data referring to the most recent HES tables at the time of writing, that is, 2021/2022).

As illustrated in Figure 1, cross-check trace is repeated twice, once in DPS against the cached version of PDS, and another time in Spine against the live version of PDS.

The cross-check trace in DPS looks for an exact match of the provided NHS number and DOB (Figure 2).

![Cross-check trace process flow in DPS core](https://digital.nhs.uk/binaries/content/gallery/website/services/personal-demographics-service/master-person-service-mps/february/figure-2.svg)
**Figure 2. Cross-check trace process flow in DPS core**

![Cross-check trace process flow in Spine](https://digital.nhs.uk/binaries/content/gallery/website/services/personal-demographics-service/master-person-service-mps/february/figure-3.svg)
**Figure 3. Cross-check trace process flow in Spine**

The diagram in Figure 3 describes the cross-check trace algorithm carried out in Spine. Besides NHS number and DOB, it also includes a partial DOB check and checks on the name and outcode values, that is, the left part of the postcode before the single space in the middle of the postcode.

Perfect matches for NHS number and DOB immediately return a PDS match. If instead the DOB only matches partially, then it checks name or outcode values.

##### Partial DOB match

A partial DOB match is where at least 2 of day (DD), month (MM), and year (YYYY) match, allowing for:

* DD/MM being swapped to MM/DD, for example, 12/06 becomes 06/12
* D1D2 being swapped to D2D1, for example, 12 becomes 21
* Y1Y2Y3Y4 being swapped to Y1Y2Y4Y3, for example, 1945 becomes 1954

##### Name match

A name match is where:

* given name is present and matches on the first character, and
* family name is present and matches on the first three characters

If given name or family name are not present, then the algorithm tries an outcode match instead. In HES, names are never provided, so this check automatically fails.

##### Outcode match

The outcode match is where the first part of a postcode (for example LS17) of the query matches the first part of the current or any of the historic postcodes on the PDS record.

##### Scoring

If a PDS record is returned at this stage (both in the DPS and in the Spine cross-check trace steps), it is considered certain and it gets a score of 100 in the MatchedConfidencePercentage field in the response file.

##### Superseded NHS numbers

An NHS number can be superseded in PDS, which means that it is no longer valid, and it has been replaced by another one. If a query record contains a superseded NHS number, cross-check trace in DPS does not recognize this as a match and the record is processed via cross-check trace in Spine. Spine cross-check trace is capable of recognizing such matches, but returns the corresponding valid NHS number as a matched record rather than the submitted superseded one.

####  Alphanumeric trace

Alphanumeric trace is the stage after cross-check trace and before algorithmic trace. Records only reach alphanumeric trace when no match is found in the previous trace step, and if the query record contains the following mandatory fields:

* family name
* year of birth
* gender

In addition, alphanumeric uses the following features as non-mandatory fields:

* DOB (full)
* given name
* postcode
* GP provider
* date of death
* Royal Mail’s Postcode Address File2 (PAF) address

The logic of alphanumeric trace is described in Figure 4.

First, the record is checked to see if it contains all the mandatory fields. Failing this, it goes to the next trace step. For query records with all the mandatory fields, alphanumeric trace will filter candidate records in PDS using the following fields if they exist in the request query record:

* current family name (exact Soundex match)
* current gender (exact match)
* current and historical DOB (exact match)
	+ if the query record has a partial DOB then an exact match on the partial DOB is required
* historical or current PAF address (exact match)
* historical or current GP Provider (exact match)
* historical or current postcode (exact match)
* historical or current given name (exact Soundex match)
* date of death (exact match)

Soundex calculation is described in the [Soundex Matching section of the Appendix](https://digital.nhs.uk/services/personal-demographics-service/master-person-service/the-person_id-handbook/appendix#soundex-matching) If only one candidate record from PDS is found at the end of the filtering steps, then this is returned as matched record. If no candidate is left or more than one candidate is found, then the request query record goes to the next trace step.

Records with a partial Date of Deaths

If a query record contains a partial date of death (for example, just the year of death) then alphanumeric trace will skip the checking of the minimum mandatory fields.

![Alphanumeric trace process flow in Spine](https://digital.nhs.uk/binaries/content/gallery/website/services/personal-demographics-service/master-person-service-mps/february/figure-4.svg)
**Figure 4. Alphanumeric trace process flow in Spine**

#####  Examples of alphanumeric trace

The following examples show common outputs from alphanumeric trace step. First, consider PDS only consisting of the following records:

| Mandatory field | Non mandatory field |
| --- | --- |

| id  | Family name | Date of birth | Gender | Given name | Postcode | GP provider  | Date of death  | Royal mail address  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Bernard | 1992-01-01 | 1 | Sammy  | SW1A 2AB | 000001 |  |  |
| 2 | Cherry | 1976-08-15 | 2 | Penelope | E14 5EA | 000002 |  |  |
| 3 | Fox | 2002-12-17 | 1 | Hadley  | SE1 8UG (start to 2005-01-02); LS1 4AP (2005-01-02 to present) | 000003 |  |  |

* + **id** 1
	+ **Family name**Bernard
	+ **Date of birth**1992-01-01
	+ **Gender**1
	+ **Given name**Sammy
	+ **Postcode**SW1A 2AB
	+ **GP provider** 000001
	+ **Date of death**
	+ **Royal mail address**
* + **id** 2
	+ **Family name**Cherry
	+ **Date of birth**1976-08-15
	+ **Gender**2
	+ **Given name**Penelope
	+ **Postcode**E14 5EA
	+ **GP provider** 000002
	+ **Date of death**
	+ **Royal mail address**
* + **id** 3
	+ **Family name**Fox
	+ **Gender**1
	+ **Given name**Hadley
	+ **Postcode**SE1 8UG  
	 (start to 2005-01-02);  
	 LS1 4AP  
	 (2005-01-02 to present)
	+ **GP provider** 000003
	+ **Date of death**
	+ **Royal mail address**

**Fictitious data**

**Example 1: Consider the following query record where the mandatory field gender is missing**

| Family name | Date of Birth | Gender | Given name | Postcode | GP provider | Date of death | Royal mail address |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Bernard | 1992-01-01 |  | Sammy | SW1A 2AB |  |  |  |

* + **Family name**Bernard
	+ **Date of Birth**1992-01-01
	+ **Gender**
	+ **Given name**Sammy
	+ **Postcode**SW1A 2AB
	+ **GP provider**
	+ **Date of death**
	+ **Royal mail address**

**Fictitious data**

The query record will move to the next trace step due to missing gender in the mandatory field.

**Example 2: Consider the following query record where non-mandatory fields are missing**

| Family name | Date of birth | Gender | Given name | Postcode | GP provider | Date of death | Royal Mail address |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Cherry | 1976-08-15 | 2 | Penelope | E14 5EA |  |  |  |

* + **Family name**Cherry
	+ **Date of birth**1976-08-15
	+ **Gender**2
	+ **Given name**Penelope
	+ **Postcode**E14 5EA
	+ **GP provider**
	+ **Date of death**
	+ **Royal Mail address**

**Fictitious data**

The query record will match with record id 2 in PDS even though the GP Provider is null in the query field.

**Example 3: Consider the following query record where one of the non-mandatory fields is different from the PDS record**

| Family name | Date of birth | Gender | Given name | Postcode | GP provider | Date of death | Royal mail address  |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Fox | 2002-12-17 | M | Hadley | LS1 4AP | 000009 |  |  |

* + **Family name**Fox
	+ **Date of birth**2002-12-17
	+ **Gender**M
	+ **Given name**Hadley
	+ **Postcode**LS1 4AP
	+ **GP provider**000009
	+ **Date of death**
	+ **Royal mail address**

**Fictitious data**

The query file will move to the next step as there is a mismatch in the GP Provider.

**Example 4: Consider the following query record where one of the non-mandatory fields matches on historical values**

| Family name | Date of birth | Gender | Given name | Postcode | GP provider | Date of death | Royal mail address  |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Fox | 2002-12-17 | M | Hadley | SE1 8UG |  |  |  |

* + **Family name**Fox
	+ **Date of birth**2002-12-17
	+ **Gender**M
	+ **Given name**Hadley
	+ **Postcode**SE1 8UG
	+ **GP provider**
	+ **Date of death**
	+ **Royal mail address**

The query file will match with id 3 in PDS, the postcode matches on a historical value in PDS.

####  Algorithmic trace

Algorithmic trace is the final stage in MPS to match records with PDS, and it is run if no match was found with cross-check trace or alphanumeric trace. The minimum eligibility criteria for running this step are having valid values in the DOB, gender and postcode fields. An overview of the workflow of the algorithmic trace is described in Figure 5.

Algorithmic trace can be summarised as follows: for each query record, a set of PDS candidate records are identified by blocking on some demographic fields; 50 or fewer records are blocked (filtered) and scored. The highest scoring candidate record is chosen as the matching record, and it is returned. However, if no candidates are found, or the highest scoring candidate cannot be resolved (for example there are multiple close matches) then no PDS record is returned.

![Algorithmic trace for all records including HES](https://digital.nhs.uk/binaries/content/gallery/website/services/personal-demographics-service/master-person-service-mps/february/figure-5.svg)
**Figure 5: Algorithmic trace for all records including HES**

#####  Blocking

The main principle of the algorithmic trace is block matching or blocking, where PDS records are considered candidates for the query record if they match to a block of demographic characteristics.

Before the blocking stage takes place, family name and given names are pre-processed by removing spaces and hyphens and then mapping via a dictionary into a normalised name3. The algorithmic traces consider the following blocks:

* Soundex of family name, Soundex of given name, DOB
* Soundex of family name, gender, DOB, postcode
* Soundex of given name, gender, DOB, postcode
* DOB, postcode, gender

[Soundex calculation](https://digital.nhs.uk/services/personal-demographics-service/master-person-service/the-person_id-handbook/appendix#soundex-matching) is described in the Appendix. The PDS records need an exact match on the elements of the block to be considered as a candidate. However, the exact match is accepted on either the current or the historical values of the features except for gender which must match exactly on current value including unknown and indeterminate values.

A maximum of 50 candidates are retained from the blocking step, and these are chosen starting from the PDS records that matched on the highest number of blocks (that is, PDS records that matched on all 4 blocks are included first in the list of candidates). For HES records where names are unavailable, algorithmic trace can only use the last blocking rule based on DOB, postcode and gender.

   Footnote 3  3. The dictionary maps input names like “Jenny” to the full form “Jennifer”. The full content of the dictionary is available in the [supplementary material](https://digital.nhs.uk/binaries/content/assets/website-assets/services/mps/name_mapping.csv).

 
Scoring and ranking algorithmic trace on HES

In HES we do not have features with partial scores. This is because the only block available in algorithmic trace is block 4 (DOB, postcode, gender), and PDS records need perfect matches on all features to be considered candidates. Hence, all PDS candidate records in algorithmic trace will have a perfect match and therefore an algorithmic score of 100.

This also makes the ranking inconsequential because all the selected candidates have equal perfect scores. Hence, where multiple candidates are found, they are all rejected with error code 97 (that is, multiple matches found). When only one candidate is identified by blocking, algorithmic trace can successfully return a match.

The following sections on scoring and ranking are provided for guidance on the operation of MPS for other datasets.

#####  Scoring

Each PDS candidate is scored based on the similarity of features from the query record. The score is calculated from the average of similarity scores of DOB, postcode, gender and the name instance(not available for HES). The name instance is a combination of given name, other given name and family name at a specific point in time. The scoring uses the original entries in PDS and not the normalised version from the blocking stage. If any of the features are missing or null, they are not included in the average calculation.

For Date of Birth (DOB), the YYYYMMDD dates are scored based on the rules in Table 1.

**Table 1. Algorithmic trace scoring system for DOB**

| Condition | Score |
| --- | --- |
| Match on YYYYMMDD | 100 |
| Match on MM and DD only | 66 |
| Match on YYYY and MM only | 66 |
| Match on YYYY and DD only | 66 |
| Match on YYYY and MMDD transposed matches | 66 |
| Match on YYYY only | 33 |
| All other states | 0 |

* + **Condition**Match on YYYYMMDD
	+ **Score**100
* + **Condition**Match on MM and DD only
	+ **Score**66
* + **Condition**Match on YYYY and MM only
	+ **Score**66
* + **Condition**Match on YYYY and DD only
	+ **Score**66
* + **Condition**Match on YYYY and MMDD transposed matches
	+ **Score**66
* + **Condition**Match on YYYY only
	+ **Score**33
* + **Condition**All other states
	+ **Score**0

For gender, the scores are based on the rules in Table 2.

**Table 2. Algorithmic trace scoring system for gender**

|  | **Query gender** |  |  |  |
| --- | --- | --- | --- | --- |
| **PDS gender** | **Not known** | **Male** | **Female** | **Not specified**  |
| Not known | 100 | 50 | 50 | 50 |
| Male | 50 | 100 | 0 | 50 |
| Female | 50 | 0 | 100 | 50 |
| Not specified | 50 | 50 | 50 | 100 |

* + **PDS gender**
	+ **Query gender****Not known**
	+ **Male**
	+ **Female**
	+ **Not specified**
* + Not known
	+ **Query gender**100
	+ 50
	+ 50
	+ 50
* + Male
	+ **Query gender**50
	+ 100
	+ 0
	+ 50
* + Female
	+ **Query gender**50
	+ 0
	+ 100
	+ 50
* + Not specified
	+ **Query gender**50
	+ 50
	+ 50
	+ 100

For postcode, the scoring is summarised in Figure 6.

The scoring considers the current and historical home address postcodes separately. It starts with the current postcode, and there are three possible outcomes: an exact, partial or no match. To achieve an exact match, all postcode characters between PDS and query must match. This produces a score of 100.

A partial score can be obtained if the query record contains a partial postcode, and these n characters match perfectly the first n characters of the postcodes in the PDS candidate records. In this case, the score would be the length of the postcode in the query record divided by the length of the postcode in the candidate record. For example, the postcode in the query record is LS1 and the postcode on the PDS record is LS1 4AP, the length of the postcode in the query record is 3. Because it matches the first 3 characters of the PDS record postcode, then the postcode score is 3/7\*100 = 43 (approximation to no decimal points).

If none of the current postcodes (usually there is only one current home address postcode) have scored above zero, the algorithm considers historical postcodes on the PDS candidate records. All historical postcodes are scored with either exact or partial scores, and the highest score is taken as a match.

![Compute postcode score in algorithmic trace process flow](https://digital.nhs.uk/binaries/content/gallery/website/services/personal-demographics-service/master-person-service-mps/february/figure-6.svg)
**Figure 6. Compute postcode score in algorithmic trace process flow**

For the name instance, the scoring is summarised in Figure 7.

The name instance is a set of given name, other given name and family name values at the same point in time. Notably, other given name is only included in the matching if the field is non-null on the query record. For each current and historical name instance, any non-ASCII characters are converted to a “@” character. The Jaro-Winkler score is then computed. The highest total score over all name instances is returned.

![Compute name score in algorithmic trace process flow](https://digital.nhs.uk/binaries/content/gallery/website/services/personal-demographics-service/master-person-service-mps/february/figure-7.svg)
**Figure 7. Compute name score in algorithmic trace process flow**

Family name and given name confidence score in response record

The MPS response file contains distinct confidence percentage scores for given name and family name. However, the user should be aware that these might differ from the scores calculated for the name instance as explained above. The ranking step in algorithmic trace uses the name instance score, and not the confidence percentage scores for given name and family name provided in the response file and consequently in the HES fields.

Moreover, if the query record has non-null other given name then the highest Jaro-Winkler score between given name and other given name will be taken as the given name confidence percentage score in the response record.

The users might encounter occasional inconsistencies in the algorithmic trace scores that can be linked back to this explanation.

#####  Ranking

For each combination of PDS candidate and query records, a score (between 0 and 100) is calculated as the average of the similarity scores across all non-null features. For HES, two of the five fields (given name and family name) are always null, and the remaining three (DOB, postcode and gender) are required to be non-null for algorithmic trace to be carried out. So, for HES the score will be an average over similarity scores for three fields.

Candidates from all blocks are ranked and algorithmic trace returns the matched PDS record with the highest score. If two or more of the highest-ranking PDS candidates have similar scores (within 5 points), then algorithmic trace does not return a match. For example, if the highest-ranking PDS candidate achieved a score of 95 and the second highest of 91, they are both rejected because they are too close to disambiguate, and the record will be returned with an error code of 97 (see the [error and success codes section](https://digital.nhs.uk//services/personal-demographics-service/master-person-service/the-person_id-handbook/appendix#error-and-success-codes)).

#####  Examples for algorithmic trace

The following examples show common scenarios in the blocking and scoring stage of the algorithmic trace step.

**Example 1: Preprocessing of names in blocking**

Consider the following query record at the start of the blocking step.

| Given name | Other given name | Family name | Date of birth | Gender | Postcode |
| --- | --- | --- | --- | --- | --- |
| Jon |  | Jones-Smith | 1992-01-01 | 1 | SW1A 2AA |

* + **Given name**Jon
	+ **Other given name**
	+ **Family name**Jones-Smith
	+ **Date of birth**1992-01-01
	+ **Gender**1
	+ **Postcode**SW1A 2AA

**Fictitious data**

In the preprocessing the following happens:

* Jon becomes Johnny because of the name normalisation
* The hyphen is removed from Jones-Smith which become Jonessmith

Thus, the fields used for the blocking are

| Given name | Other given name | Family name | Date of birth | Gender | Postcode |
| --- | --- | --- | --- | --- | --- |
| Johnny |  | Jonessmith | 1992-01-01 | 1 | SW1A 2AA |

* + **Given name**Johnny
	+ **Other given name**
	+ **Family name**Jonessmith
	+ **Date of birth**1992-01-01
	+ **Gender**1
	+ **Postcode**SW1A 2AA

**Fictitious data**

**Example 2: Scoring of names with hyphens**

Consider the comparison of the following query record with one candidate from the blocking stage:

|  | Given name | Other given name | Family name | Date of birth | Gender | Postcode |
| --- | --- | --- | --- | --- | --- | --- |
| Query record | Jon |  | Smith-Jones | 1992-01-01 | 1 | SW1A 2AA |
| Candidate | James |  | Smith | 1992-01-01 | 1 | SW1A 2AA |

* + Query record
	+ **Given name**Jon
	+ **Other given name**
	+ **Family name**Smith-Jones
	+ **Date of birth**1992-01-01
	+ **Gender**1
	+ **Postcode**SW1A 2AA
* + Candidate
	+ **Given name**James
	+ **Other given name**
	+ **Family name**Smith
	+ **Date of birth**1992-01-01
	+ **Gender**1
	+ **Postcode**SW1A 2AA

**Fictitious data**

The scoring is calculated as the following:

* for given name, the Jaro-Winkler distance is computed between “Jon” and “James” which gives 51
* for family name, hyphens is an ASCII character and are not replaced with @. Thus, Jaro Winkler is computed between “Smith-Jones” and “Smith” which gives 89
* there is an exact match on all other fields thus scoring 100

|  | Given name | Other given name | Family name | Date of birth | Gender | Postcode |
| --- | --- | --- | --- | --- | --- | --- |
| Candidate 1 | 51 |  | 89 | 100 | 100 | 100 |

* + Candidate 1
	+ **Given name**51
	+ **Other given name**
	+ **Family name**89
	+ **Date of birth**100
	+ **Gender**100
	+ **Postcode**100

The final aggregated score is the mean average of all 5 fields, that is 88 in this case.

**Example 3: Scoring of candidates with non-ASCII signs**

Consider the following query records providing 2 candidates from the blocking stage:

|  | Given name | Other given name | Family name | Date of birth | Gender | Postcode |
| --- | --- | --- | --- | --- | --- | --- |
| Query record | Zöe |  | Ó Briain | 1992-01-01 | 2 | SW1A 2AA |
| Candidate 1 | Zöe |  | O Briain | 1992-01-01 | 2 | SW1A 2AA |
| Candidate 2  | Zoe |  | Briain | 1992-01-01 | 2 | SW1A 2AA |

* + Query record
	+ **Given name**Zöe
	+ **Other given name**
	+ **Family name**Ó Briain
	+ **Date of birth**1992-01-01
	+ **Gender**2
	+ **Postcode**SW1A 2AA
* + Candidate 1
	+ **Given name**Zöe
	+ **Other given name**
	+ **Family name**O Briain
	+ **Date of birth**1992-01-01
	+ **Gender**2
	+ **Postcode**SW1A 2AA
* + Candidate 2
	+ **Given name**Zoe
	+ **Other given name**
	+ **Family name**Briain
	+ **Date of birth**1992-01-01
	+ **Gender**2
	+ **Postcode**SW1A 2AA

**Fictitious data**

For given name, the scores are calculated as follows:

* for Candidate 1, the name “Zöe” is transformed to “Z@e”. Thus, the Jaro-Winkler score is computed between “Z@e” from query record and “Z@e” from Candidate 1, which gives 100
* for Candidate 2, the Jaro-Winkler score is computed between “Z@e” from the query record and “Zoe” from Candidate 2, which gives 80

For family name, the scores are calculated as follows

* for Candidate 1, the name “Ó Briain” is transformed to “@ Briain”. Thus, the Jaro-Winkler score is computed by comparing “@ Briain” with “O Briain”, which gives 92
* for Candidate 2, the Jaro-Winkler score compares “@ Briain” with “Briain”, which gives 80

All other fields have a perfect match thus scoring 100

|  | Given name | Other given name | Family name | Date of birth | Gender | Postcode |
| --- | --- | --- | --- | --- | --- | --- |
| Candidate 1 | 100 |  | 92 | 100 | 100 | 100 |
| Candidate 2  | 80 |  | 92 | 100 | 100 | 100 |

* + Candidate 1
	+ **Given name**100
	+ **Other given name**
	+ **Family name**92
	+ **Date of birth**100
	+ **Gender**100
	+ **Postcode**100
* + Candidate 2
	+ **Given name**80
	+ **Other given name**
	+ **Family name**92
	+ **Date of birth**100
	+ **Gender**100
	+ **Postcode**100

The final aggerated score is the mean average of all 5 fields, that is 98 for Candidate 1 and 94 for Candidate 2.

No match is returned in this case, as there is a less than 5-point gap between the highest and the second highest score.

**Example 4: Scoring of candidates with a non-null other given name field**

Consider the comparison of the following query record with 3 candidates from the blocking stage:

|  | Given name | Other given name | Family name | Date of birth | Gender | Postcode |
| --- | --- | --- | --- | --- | --- | --- |
| Query Record | John | Adams | Smith  | 1992-01-01 | 1 | SW1A 2AA |
| Candidate 1 | Jon |  | Smith  | 1992-01-01 | 1 | SW1A 2AA |
| Candidate 2  | Jon | Adams | Smith  | 1992-01-01 | 1 | SW1A 2AA |
| Candidate 3 | John | Dan | Smith  | 1992-01-01 | 1 | SW1A 2AA |

* + Query Record
	+ **Given name**John
	+ **Other given name**Adams
	+ **Family name**Smith
	+ **Date of birth**1992-01-01
	+ **Gender**1
	+ **Postcode**SW1A 2AA
* + Candidate 1
	+ **Given name**Jon
	+ **Other given name**
	+ **Family name**Smith
	+ **Date of birth**1992-01-01
	+ **Gender**1
	+ **Postcode**SW1A 2AA
* + Candidate 2
	+ **Given name**Jon
	+ **Other given name**Adams
	+ **Family name**Smith
	+ **Date of birth**1992-01-01
	+ **Gender**1
	+ **Postcode**SW1A 2AA
* + Candidate 3
	+ **Given name**John
	+ **Other given name**Dan
	+ **Family name**Smith
	+ **Date of birth**1992-01-01
	+ **Gender**1
	+ **Postcode**SW1A 2AA

**Fictitious data**

For given name, the scores are calculated as follows:

* for candidate 1 and 2, the Jaro-Winkler score is computed comparing “John” and “Jon”, which gives 93
* for candidate 3, the Jaro-Winkler score is computed using “John” and “John”, which gives 100

For other given name

* for candidate 1, the field is null thus the Jaro-Winkler score is 0
* for candidate 2, the Jaro-Winkler score is computed using “Adams” and “Adams”, which gives 100
* candidate 3, the Jaro-Winkler score is computed using “Adams” and “Dan”, which gives 51

For the other fields, there in an exact match for all candidates thus scoring 10

|  | Given name | Other given name | Family name | Date of birth | Gender | Postcode |
| --- | --- | --- | --- | --- | --- | --- |
| Candidate 1  | 93 | 0 | 100 | 100 | 100 | 100 |
| Candidate 2 | 93 | 100 | 100 | 100 | 100 | 100 |
| Candidate 3 | 100 | 51 | 100 | 100 | 100 | 100 |

* + Candidate 1
	+ **Given name**93
	+ **Other given name**0
	+ **Family name**100
	+ **Date of birth**100
	+ **Gender**100
	+ **Postcode**100
* + Candidate 2
	+ **Given name**93
	+ **Other given name**100
	+ **Family name**100
	+ **Date of birth**100
	+ **Gender**100
	+ **Postcode**100
* + Candidate 3
	+ **Given name**100
	+ **Other given name**51
	+ **Family name**100
	+ **Date of birth**100
	+ **Gender**100
	+ **Postcode**100

The final aggregate score is the mean average for all 6 fields, that is, 82 for candidate 1, 99 for candidate 2 and 91 for candidate 3.

In this case candidate 2 is returned as match.

####  MPS\_ID matching

![MPS_ID matching process flow](https://digital.nhs.uk/binaries/content/gallery/website/services/personal-demographics-service/master-person-service-mps/february/figure-8.svg)
**Figure 8. MPS\_ID matching process flow**

The last step in MPS consists of running MPS\_ID matching against the MPS record bucket as illustrated in Figure 8. If the query record matches an existing record in the MPS record bucket, then the MPS\_ID is returned. Otherwise, if the minimum required fields are provided, then a new MPS record is generated and stored in the MPS record bucket.

An empty MPS\_ID field is returned if the query record does not have the minimum required fields.

##### Initial checks

MPS\_ID matching is run only if the previous tracing steps returned an invalid NHS number (that is, if the NHS number is 0000000000).

##### MPS query with local patient ID

This step is run if the query record includes a local patient ID. All the MPS records with local patient ID corresponding to the query record are selected if any of the following sets of fields match:

* family name, DOB, postcode and either given name or gender
* given name, DOB and postcode
* given name, family name, gender and postcode
* given name, family name, and DOB
* DOB only (if given name or family name are missing) – this is the only set that is relevant for HES

##### MPS query without local patient ID

If the query does not include a local patient ID, or if the previous step returned no MPS\_IDs, then this step returns all records in the MPS record bucket which match one of the following:

* if the query record of the request file contains a given name and family name, then given name and family name must both match the record in the MPS record bucket (along with DOB and postcode)
* if the query record does not contain a given name or family name, then gender must match the record in the MPS record bucket (along with DOB and postcode)

Multiple MPS\_ID Matches

MPS matching can return multiple MPS\_ID matches for the same record. This can occur because this is a rigid search and the records are not scored like in the algorithmic trace step, so all the matched records are considered equally good. We can find multiple matches if a record in the MPS bucket is duplicated in multiple records with different MPS\_IDs. There is no current process to remove duplicates (unlike PDS, which is curated by the National Back Office), and hence multiple matches are returned in the response file.

When the HES pipeline in DPS processes the response file, multiple matches are lost because only the first identifier is picked. The first identifier will not consistently be the same one, so these records might be randomly allocated to one of the duplicates over time.

#####  Minimum required fields

If neither of the above queries returns any MPS\_IDs, then the following step creates a new MPS record. The minimum required fields for creating a new MPS record are valid DOB and either local patient identifier or valid postcode.

#####  MPS record bucket maintenance

Records in the MPS record bucket are not updated based on new queries. For example, if a query record is matched to an MPS\_ID but the postcode is different, this new postcode is not added to the MPS record information.

Differently than PDS, MPS record bucket is not periodically checked for duplicates or inconsistent and impossible records.

An MPS\_ID can be used to link records across datasets.

#####  Which records can populate MPS record bucket?

In the process above we described that, if a match is not found but the query record has sufficient information for the creation of a new MPS\_ID record, then this is added to the MPS record bucket.

However, there is a control mechanism in place to prevent the addition of unsuitable records, such as the ones that have a retention period linked to a research study. This is the case for many cohorts that external organisations submit via DARS (Data Access Request Service) with the purpose of linking these patients’ data to other assets controlled by NHS England. These records will be assigned a one-time-use ID instead of a MPS\_ID.

In summary, the cohort data transmitted through DARS does not ultimately populate the MPS record bucket.

####  One-time-use ID

The records that could not be matched neither with PDS, nor with MPS record bucket, and that did not have sufficient information to generate a new MPS\_ID, are left unmatched by MPS. Such unmatched records have a one-time use ID generated in DPS, so that all the different unmatched records are kept distinct. This identifier is also known as UPRI 2 (unmatched person record identifier 2)

The one-time use IDs cannot be used to link records across datasets, or even within a datase

####  Scoring and other outputs

The results from MPS are provided in the response file. The response file is only used in DPS for internal purposes (for example, creating the final Person\_ID field, as explained in the [Person\_ID creation and data set enrichment section.](https://digital.nhs.uk//services/personal-demographics-service/master-person-service/the-person_id-handbook/technical-details-of-the-data-linkage-algorithm#person_id-creation-and-data-set-enrichment)

The fields of this file are detailed in the [Response file section of the Appendix](https://digital.nhs.uk/services/personal-demographics-service/master-person-service/the-person_id-handbook/appendix#response-file), but in summary, they are the same fields as the request file with the addition of specific MPS output fields as follows:

* SENSITIVE FLAG
* ERROR/SUCCESS\_CODE
* MATCHED \_NHS\_NO
* MPS\_ID
* MatchedAlgorithmIndicator
* MatchedConfidencePercentage
* FamilyNameScorePercentage
* GivenNameScorePercentage
* DateOfBirthScorePercentage
* GenderScorePercentage
* PostcodeScorePercentage

Some fields from the response file are carried across in the final data asset created in DPS, depending on the specific data set. In HES, the last 7 fields are carried across as a structure in a field called MPS Confidence.

##### Sensitive flag

Where a patient record is flagged as sensitive, all demographic data is returned in the query response; however, pipeline authors should ensure records are appropriately handled before data is shared with end users, in particular by redacting ‘location information’ such as addresses which allow individuals to be located.

##### Error/success code

This code indicates the status of the match at record level. The most common codes will be 00 for success or 98 for not found. See Table 11 for a list of all possible codes.

##### MATCHED\_NHS\_NO and MPS\_ID

These are the fields populated with the matched NHS numbers if a record was successfully matched in PDS, or with the MPS\_ID if a record from MPS record bucket was matched instead.

##### MatchedAlgorithmIndicator field

This field indicates which tracing step was run last before exiting MPS. The complete list of values is listed in Table 3.

Note that this field does not indicate whether the record was matched or not. For example, in HES MatchedAlgorithmIndicator can assume values 1 or 4 even without a match. This can happen if the record does not satisfy the eligibility criteria to proceed to the next tracing step. The eligibility criteria for cross-check trace are that NHS number and DOB are present and valid. For algorithmic trace there should be sufficient valid fields to populate at least one block

**Table 3. Explanation of the MatchedAlgorithmIndicator field values**

| Matched Algorithm Indicator value | Explanation |
| --- | --- |
| 0 | None of the tracing steps were run. This can happen when the record does not have sufficient information to run any tracing step, for example when DOB is invalid or not available. But there are other edge-case scenarios like unexpected data store errors (for example, the PDS record has duplicates). |
| 1 | The last tracing step run was cross-check trace (either DPS or Spine version). |
| 3 | The last tracing step run was alphanumeric trace (never run in HES). |
| 4 | The last tracing step run was algorithmic trace. |

* + **Matched Algorithm Indicator value**0
	+ **Explanation**None of the tracing steps were run. This can happen when the record does not have sufficient information to run any tracing step, for example when DOB is invalid or not available. But there are other edge-case scenarios like unexpected data store errors (for example, the PDS record has duplicates).
* + **Matched Algorithm Indicator value**1
	+ **Explanation**The last tracing step run was cross-check trace (either DPS or Spine version).
* + **Matched Algorithm Indicator value**3
	+ **Explanation**The last tracing step run was alphanumeric trace (never run in HES).
* + **Matched Algorithm Indicator value**4
	+ **Explanation**The last tracing step run was algorithmic trace.

The remaining fields (MatchedConfidencePercentage, FamilyNameScorePercentage, GivenNameScorePercentage, DateOfBirthScorePercentage, GenderScorePercentage, PostcodeScorePercentage) are the scores from the different tracing steps.

##### Scoring in cross-check trace and alphanumeric trace

If a PDS record was matched by cross-check trace, the scoring is binary, that is, MatchedConfidencePercentage is either 100 if there was a successful match or 0 otherwise, and MatchedAlgorithmIndicator would be 1. This is valid for both DPS and Spine cross-check trace steps. However, the records matched in DPS have null values for the individual percentage scores (for example, DateOfBirthScorePercentage, etc), while those matched in Spine have zero values.

Alphanumeric trace is not used for matching HES records, due to the absence of family name fields. Its output would also be binary, 100 or 0, depending on whether there was a successful match or not. MatchedAlgorithmIndicator would be 2, and all other fields would have zero values.

##### Scoring in algorithmic trace

In algorithmic trace, the score is a value between 0 and 100, which is the unweighted average of the scores across the name instance (a combination of given name, other given name and family name as explained in the [Algorithmic trace](https://digital.nhs.uk//services/personal-demographics-service/master-person-service/the-person_id-handbook/technical-details-of-the-data-linkage-algorithm#algorithmic-trace) section), postcode, DOB, and gender, if present. For HES data, family name and given name are not present so this score will be the average of the scores from the remaining three fields (postcode, DOB, and gender).

FamilyNameScorePercentage and GivenNameScorePercentage have values of zero in the MPS outputs but will not contribute to the calculation of the average.

The details of how the scores are calculated can be found in the [Algorithmic trace](https://digital.nhs.uk//services/personal-demographics-service/master-person-service/the-person_id-handbook/technical-details-of-the-data-linkage-algorithm#algorithmic-trace) section.

##### Scoring thresholds

There is no minimum score threshold for a match. However, the blocking rules make sure that there are no candidates with a score below 50. Some users might want to apply further filtering to select only matches with higher confidence score. This can be done in post-processing by using the field MatchedConfidencePercentage.

##### Examples

Table 4 shows examples of scoring outputs for different matching conditions.

If the match was found with algorithmic trace, as in the example in Table 4 column 4, the scores would be as follows; family name and given name were not present (as per all HES examples), but DOB, gender, and postcode can all match between 0 and 100.

In the MPS\_ID matching example (Table 4, column 5), the MatchedAlgorithmIndicator can still have values 1 or 4 for HES (other data sets might also have values of 3) depending on which tracing step was last run.

The example in Table 4 column 6 considers when multiple NHS numbers are matched for the same record. This can only happen with algorithmic trace and therefore the MatchedAlgorithmIndicator can only indicate a value of 4 while the remaining scores will be set to 0.

Finally, the example in Table 4 column 7 shows what happens when no match was found (neither in PDS nor in MPS record bucket). The MatchedAlgorithmIndicator in this case can indicate any possible value (for HES the only possibilities are 0, 1, 4).

**Table 4.Examples of the values that the MPS output fields can assume depending on the tracing step that the record was matched on**

| Example matched step | DPS cross-check trace | Spine cross-check trace | Alphanumeric trace | Algorithmic trace | MPS\_ID matching | Multiple NHS number match | No match  |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MATCHED\_ NHS\_NO | NHS num | NHS num | NHS num | NHS num | 0000000000 | 9999999999 | 0000000000 |
| MPS\_ID | Empty | Empty | Empty | Empty | Present | Empty | Empty |
|  | 1 | 1 | 3 | 4 | 1,3,4 | 4 | 0,1,3,4 |
|  | 100 | 100 | 100 | 50\*-100 | 0 | 0 | 0 |
| FamilyNameScore | null | 0 | 0 | 0-100 | 0 | 0 | 0 |
| Score | null | 0 | 0 | 0-100 | 0 | 0 | 0 |
| Score | null | 0 | 0 | 0-100 | 0 | 0 | 0 |
| Score | null | 0 | 0 | 0-100 | 0 | 0 | 0 |
| Score | null | 0 | 0 | 0-100 | 0 | 0 | 0 |

* + **Example matched step** MATCHED\_
	
	 NHS\_NO
	+ **DPS cross-check trace**NHS num
	+ **Spine cross-check trace**NHS num
	+ **Alphanumeric trace**NHS num
	+ **Algorithmic trace**NHS num
	+ **MPS\_ID matching**0000000000
	+ **Multiple NHS number match**9999999999
	+ **No match** 0000000000
* + **Example matched step**MPS\_ID
	+ **DPS cross-check trace**Empty
	+ **Spine cross-check trace**Empty
	+ **Alphanumeric trace**Empty
	+ **Algorithmic trace**Empty
	+ **MPS\_ID matching**Present
	+ **Multiple NHS number match**Empty
	+ **No match** Empty
* + **Example matched step**
	+ **DPS cross-check trace**1
	+ **Spine cross-check trace**1
	+ **Alphanumeric trace**3
	+ **Algorithmic trace**4
	+ **MPS\_ID matching**1,3,4
	+ **Multiple NHS number match**4
	+ **No match** 0,1,3,4
* + **Example matched step**
	+ **DPS cross-check trace**100
	+ **Spine cross-check trace**100
	+ **Alphanumeric trace**100
	+ **Algorithmic trace**50\*-100
	+ **MPS\_ID matching**0
	+ **Multiple NHS number match**0
	+ **No match** 0
* + **Example matched step**
	+ **DPS cross-check trace**null
	+ **Spine cross-check trace**0
	+ **Alphanumeric trace**0
	+ **Algorithmic trace**0-100
	+ **MPS\_ID matching**0
	+ **Multiple NHS number match**0
	+ **No match** 0
* + **Example matched step**
	+ **DPS cross-check trace**null
	+ **Spine cross-check trace**0
	+ **Alphanumeric trace**0
	+ **Algorithmic trace**0-100
	+ **MPS\_ID matching**0
	+ **Multiple NHS number match**0
	+ **No match** 0
* + **Example matched step**
	+ **DPS cross-check trace**null
	+ **Spine cross-check trace**0
	+ **Alphanumeric trace**0
	+ **Algorithmic trace**0-100
	+ **MPS\_ID matching**0
	+ **Multiple NHS number match**0
	+ **No match** 0
* + **Example matched step**
	+ **DPS cross-check trace**null
	+ **Spine cross-check trace**0
	+ **Alphanumeric trace**0
	+ **Algorithmic trace**0-100
	+ **MPS\_ID matching**0
	+ **Multiple NHS number match**0
	+ **No match** 0
* + **Example matched step**
	+ **DPS cross-check trace**null
	+ **Spine cross-check trace**0
	+ **Alphanumeric trace**0
	+ **Algorithmic trace**0-100
	+ **MPS\_ID matching**0
	+ **Multiple NHS number match**0
	+ **No match** 0

\*The lower bound of the MatchedConfidencePercentage range is not fixed at 50. However, the blocking rules used in the algorithmic trace always guarantee a minimum level of match that practically never produces overall scores below 50.

####  Person\_ID creation and data set enrichment

The MPS response file contains the fields detailed in the [Response file section of the Appendix](https://digital.nhs.uk/services/personal-demographics-service/master-person-service/the-person_id-handbook/appendix#response-file), including scoring outputs as explained in the [scoring and other outputs section](https://digital.nhs.uk//services/personal-demographics-service/master-person-service/the-person_id-handbook/technical-details-of-the-data-linkage-algorithm#scoring-and-other-outputs). The response file still does not contain the Person\_ID field, but only the matched NHS number and MPS\_ID. As part of the DPS pipeline, Person\_ID is created from these other fields.

The derivation logic for the Person\_ID is as follows:

* if the record in the response file contains a valid MATCHED\_NHS\_NO, this is used as Person\_ID (see example in Table 5, row 1)
* else, if the record in the response file contains an MPS\_ID (UPRI 1), this is used as Person\_ID (see example in Table 5, row 2 - in this case, MATCHED\_NHS\_NO has a default value of 0000000000)
* if the MPS\_ID field contains multiple MPS\_IDs, only the first one is retained (see example in Table 5, row 3)
* else, a one-time-use ID (UPRI 2) is generated, and this is used as Person\_ID (see examples in Table 5, rows 4 and 5)

Notably, MPS\_ID and one-time-use ID have a leading letter that helps the users understand the origin of the Person\_ID (that is, “A/B” if it originates from MPS\_ID, “U” if it originates from the one-time-use ID). These, however, are lost with the tokenization process..

**Table 5. Examples of how the fields MATCHED\_NHS\_NO and MPS\_ID from the response file are combined to produce a Person\_ID**

| Row number | Person\_ID | Matched\_NHS\_No | MPS\_ID (UPRI 1) | One-time-use ID (UPRI 2) |
| --- | --- | --- | --- | --- |
| 1 | 0123456789 | 0123456789 | - | - |
| 2 | A987654321 | 0000000000 | A987654321 | - |
| 3 | A123454321 | 0000000000 | A123454321~~~ A987656789 | - |
| 4 | U123123123 | 9999999999 | - | U123123123 |
| 5 | U312321321 | 0000000000 | - | U312321321 |

* + **Row number**1
	+ **Person\_ID**0123456789
	+ **Matched\_NHS\_No**0123456789
	+ **MPS\_ID (UPRI 1)**-
	+ **One-time-use ID (UPRI 2)**-
* + **Row number**2
	+ **Person\_ID**A987654321
	+ **Matched\_NHS\_No**0000000000
	+ **MPS\_ID (UPRI 1)**A987654321
	+ **One-time-use ID (UPRI 2)**-
* + **Row number**3
	+ **Person\_ID**A123454321
	+ **Matched\_NHS\_No**0000000000
	+ **MPS\_ID (UPRI 1)**A123454321~~~ A987656789
	+ **One-time-use ID (UPRI 2)**-
* + **Row number**4
	+ **Person\_ID**U123123123
	+ **Matched\_NHS\_No**9999999999
	+ **MPS\_ID (UPRI 1)**-
	+ **One-time-use ID (UPRI 2)**U123123123
* + **Row number**5
	+ **Person\_ID**U312321321
	+ **Matched\_NHS\_No**0000000000
	+ **MPS\_ID (UPRI 1)**-
	+ **One-time-use ID (UPRI 2)** U312321321

**Fictitious data** 

The response file has 34 fields which include personal identifiable information retrieved from PDS. However, not all of them are used to enrich the data set. In HES, only Person\_ID and the 7 MPS indicators are returned in the data set for the users to see. These are:

* MatchedAlgorithmIndicator
* MatchedConfidencePercentage
* FamilyNameScorePercentage
* GivenNameScorePercentage
* DateOfBirthScorePercentage
* GenderScorePercentage
* PostcodeScorePercentage

However, other data sets might have different requirements and return additional personal identifiable information for the patient to enrich the input data set. It is the responsibility of the pipeline author in DPS to add the fields returned by MPS to the original input data.

Superseded NHS numbers

An NHS number can be superseded in PDS, which means that it is no longer valid, and it has been replaced by another one. If a query record contains a superseded NHS number, all three tracing steps run in Spine (cross-check trace, alphanumeric trace and algorithmic trace) are capable of recognizing this, and they return the corresponding valid NHS number. This can be confusing for users as they might see a Person\_ID that is different from the submitted NHS number being matched at cross-check trace. When this happens, it is most likely a case of superseded NHS number, as illustrated in case study 11 in the [Empirical examples](https://digital.nhs.uk//services/personal-demographics-service/master-person-service/the-person_id-handbook/case-studies#empirical-examples) section.

####  Tokenization

In the previous chapters it was established how the Person\_ID is a unique identifier for each individual patient, generated via the MPS. For HES, this identifier replaces the legacy HES\_ID field.

Most users will not have visibility of the clear values for personal identifiable information such as Person\_ID, but will only have access to the tokenized version of such information, depending under which Data Sharing Agreement (DSA) the data set is provided.

Tokenization (also referred to as “de-id”) is the service that allows for data items to be anonymised. Currently, this happens for NHS number, Person\_ID and local patient identifier.

A separate store/table contains the random relationships between the original entry identifier and the token. Tokenized values can also be re-identified using the table in the inverse order.

The token maintains the same format of the original entry so that the same operations can be applied to both fields. In HES, for example, a tokenised version of Person\_ID can be found in the field Token\_Person\_ID, they are both alphanumeric strings, but Person\_ID contains 10 digits only, while Token\_Person\_ID contains 32 digits (see example in Table 6).

Notably, the tokenized version of Person\_ID will no longer preserve the A/B/U initial digit which identifies whether the Person\_ID was a UPRI 1 or 2.

Across the same data set, a unique Token\_Person\_ID is used to identify records with the same underlying Person\_ID. The same will be true across different data sets, provided that they belong to the same domain. Different domains might be used in different DSAs, and consequently the same Person\_ID might be identified with different Token\_Person\_ID across different domains.

**Table 6. Examples of NHS number and Person\_ID and the tokenized version**

| NHS number | Person\_ID | Token\_Person\_ID |
| --- | --- | --- |
| 0123456789 | 0123456789 | 987A543219876G432198RR5432198765 |
| - | A123456789 | 647A5142198RRT432198RHH432112332 |
| - | U123456789 | 1017JJ146HH8R12322198RHYY771KK32 |

* + **NHS number**0123456789
	+ **Person\_ID**0123456789
	+ **Token\_Person\_ID**987A543219876G432198RR5432198765
* + **NHS number**-
	+ **Person\_ID**A123456789
	+ **Token\_Person\_ID**647A5142198RRT432198RHH432112332
* + **NHS number**-
	+ **Person\_ID**U123456789
	+ **Token\_Person\_ID**1017JJ146HH8R12322198RHYY771KK32

**Fictitious data**

Last edited: 27 February 2024 4:12 pm

#### Chapters

Some content could not be imported from the original document. [View content ↗](https://consentcdn.cookiebot.com/sdk/bc-v4.min.html)
