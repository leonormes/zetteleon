## Understanding TPP's Strategic Reporting and IM1 for Bulk Data Extraction

TPP's "Strategic Reporting" solution is designed to provide daily incremental data extracts from SystmOne, their primary care Electronic Patient Record (EPR) system. It's crucial to note that this data is **not intended for, nor should it be used for, direct patient care**. Instead, it serves purposes like yours: providing population-level research data and enabling cohort discovery queries \[R4\]. The data is provided in CSV file format, with one CSV file per table, and can contain either a full history or delta (changed data since the last extract) information.

The "IM1" (Interface Mechanism 1) is a set of API standards developed by NHS Digital to enable third-party applications to integrate with GP clinical systems like EMIS Web, Cegedim Vision, and TPP SystmOne. For your specific goal of bulk data extraction for research, the relevant IM1 interface mechanism is the **Bulk API**. This API empowers your application to gain daily, weekly, or monthly extracts of bulk data feeds of patient or clinical system user data, once GP practice consent has been obtained. This is distinct from the IM1 Patient API (for patient-facing services like appointment booking) or the IM1 Transaction API (for real-time access and updates for medical professionals).

- [x] Where is the document explaining the TPP use case  #tdsync %%\[tid:: [6c6RqQc3VRQpXhjv](todoist://task?id=6c6RqQc3VRQpXhjv)\]%%  \[completion:: 2025-06-12\]

## Strategic Reporting Data Content and Configuration

The Strategic Reporting extract can be configured to include specific tables and fields relevant to your needs. Any new additions (either tables or fields) to the Strategic Reporting extract are not automatically added to your configuration, requiring manual updates if you wish to use them. The extract also supports filtering patient content based on criteria such as patient's sex, age, Read codes in their record, and medication in their record.

A critical option for population-level research is the "Include the shared record" setting. When this option is selected, the extract will include patient data recorded at units outside of your designated recipient organisation group, provided:

1. The patient has consented to share out from the recording unit.

2. The patient has consented to share in to a unit within your organisation group.

Without this option, the extract would only contain patient data explicitly recorded at a unit within your recipient organisation group. This highlights the importance of careful consideration of Information Governance implications when setting this configuration.

You can also choose to "Limit Full Download to last" a certain number of months, which can result in faster full download speeds for specific historical periods, rather than receiving all of an organisation's historical data. Additionally, the "Manage Full Downloads" option allows you to customise when specific tables or new units will receive their full downloads, should they be necessary.

## Integration and Onboarding Process via IM1

The process to integrate with TPP via IM1 for Strategic Reporting (Bulk API) follows a structured path, ensuring compliance with NHS standards. Fitfile has already initiated this by submitting your Supplier Conformance Assessment List (SCAL).

Here's a breakdown of the typical process and Fitfile's current standing:

1. **Prerequisites and SCAL Submission:** Before development, organisations must complete the IM1 Clinical and Information Governance prerequisites form. Your SCAL is then reviewed to evaluate compatibility with provider APIs and ensure compliance with NHS standards. Fitfile submitted its SCAL on November 29, 2024. TPP's clinical team reviewed and approved your product on December 18, 2024. 

---

> **From**: Integration
> **Sent**: 18 December 2024 11:19
> **To**: Petros Kotsidis ; Susannah Thomas ; TEAM, Im1 (NHS ENGLAND - X26)
> **Subject**: RE: FITFILE - SCAL Submission
> Good morning,
> Our clinical team have reviewed and approved the FitFile product. The next step is for the IM1 team to review internally and issue the Recommendation to Connect. Once we’ve received this we can then provide a Go-Live date.
> Please note that we are currently in a change freeze so can only issue FitFile into Live from 07/01/25.
> Kind regards,
> Lauren Nightingale

1. **Model Interface License:** Once compatibility is confirmed, an Approved Developer (such as Fitfile) executes a Model Interface License with each provider (TPP in this case), granting access to the provider’s API test environment.

2. **Testing Phases:**

   - **Unsupported Test Phase:** Developers use a Pairing and Integration Pack (PIP) to build and refine their solution.

   - **Supported Test Phase (Assurance/Witness Testing):** Providers and developers collaborate to conduct assurance tests, ensuring functionality, security, and compliance. NHS Digital provides a Recommendation to Connect Notice (RTCN) after the SCAL is agreed and witness testing is undergone.

      - **Fitfile's Status:** The NHS England IM1 team scheduled a final review of your SCAL for January 8, 2025, with a witness test for the week of January 20, 2025. However, on January 8, 2025, NHS England requested a mitigation report for any medium & high findings from your pen test. This report was provided on April 10, 2025.

      - Additionally, NHS England requested a copy of your data sharing agreement with GPs on January 22, 2025. You responded that you do not have current data sharing agreements with TPP GPs, but have received data from 32 GPs via the approved EMIS data sharing route via IM1.

      - Furthermore, on March 5, 2025, and reiterated on April 2, 2025, NHS England requested completed test scripts showing actual results from your witness tests/outcomes. Fitfile indicated on April 23, 2025, that you did not yet have a TPP development environment set up and were therefore unable to perform witness testing or provide TPP-specific test scripts. NHS England then clarified on April 25, 2025, that test access for TPP was provided to Fitfile on March 13, 2024, including details for a test environment (Unit Name: HSCIC Test environment 61, Unit ID: 92HSCIC, Username: pkotsidis0324) and test patient details. They also asked for reasons why Fitfile cannot use "transaction" instead of "BULK".

3. **Go-Live:** Once all requirements are met and NHS England issues a "Recommended to Connect" status, your product can be rolled out to live environments. Fitfile was informed that go-live could only occur from January 7, 2025, due to a change freeze.

## Technical Aspects of Strategic Reporting Download

The transfer mechanism for Strategic Reporting is integrated into the SystmOne client. Downloads are limited to the "owning organisation" (the one that owns the Strategic Reporting group). To receive the daily extract, you need to configure a "Scheduled Job" within SystmOne, typically linked to a "Gateway PC" which should be left running and logged into SystmOne in a locked-out state overnight. This ensures the automated download occurs. You will need to contact TPP to be granted access to the "Scheduled Jobs" screen.

The download process automatically organizes the files: previous downloads are moved into an "Archived" subfolder, and a "manifest file" (SRManifest.csv) is downloaded last. This manifest file indicates whether each included data file is a full history or a delta, and the date range covered. It's recommended to parse the manifest before loading data into an external data warehouse.

## Security Considerations for Strategic Reporting

TPP emphasizes the security of data transfer for Strategic Reporting. In-flight data (during download) is encrypted using industry-standard algorithms over a direct socket connection between the SystmOne client and server via the N3 network. Penetration testing is conducted by a third party to establish the security of this communication. For data at rest, the local folder where the files are written is configured by a SystmOne user with appropriate access rights (granted by a Caldicott Guardian), and local restrictions are expected to prevent unauthorized access to this directory.

## Addressing the "Transaction vs. Bulk" Query

NHS England has specifically asked for clarification on why Fitfile cannot use "transaction" instead of "BULK" for data access. This is a critical distinction:

- **IM1 Transaction API:** This API supports **real-time transactions** between consumer systems and GP's core IT systems. It allows medical professionals to access, retrieve, and *update* patient data, manage appointments, and *create new consultation records*. The purpose is to streamline administrative processes and ensure up-to-date information for direct patient care.

- **IM1 Bulk API:** This API is explicitly designed for obtaining **daily, weekly, or monthly extracts of bulk data feeds** of patient or clinical system user data.

Given Fitfile's goal is to enable researchers to make **cohort discovery queries and have population-level research data** \[R4\], the **Bulk API** is the appropriate choice. The Transaction API, while offering real-time access, is focused on individual patient interactions and clinical updates, which is fundamentally different from the need for large, population-level datasets for research and analytics. Attempting to use the Transaction API for bulk data extraction would be inefficient, potentially violate usage policies, and might not provide the comprehensive historical or population-wide data necessary for your stated purpose.

## Recommendations for Fitfile's Next Steps

1. **Resolve Test Environment Access and Test Scripts:** Immediately clarify with NHS England's IM1 team the discrepancy regarding the TPP development environment access. TPP states access was provided on March 13, 2024, and provides login details. You need to confirm if you have successfully accessed this environment. Once access is verified, you must proceed with witness testing in this environment and provide the requested test scripts with actual results. This is a critical blocker to your go-live.

2. **Address Data Sharing Agreement:** Proactively follow up with Joanne Maw regarding the data sharing agreement. Explain your current setup with EMIS data sharing via IM1 and seek specific guidance on what is required for TPP GPs. Understanding their requirements for a TPP-specific data sharing agreement is crucial.

3. **Reinforce Bulk API Rationale:** Clearly articulate to NHS England's IM1 team that your objective is **cohort discovery and population-level research**, which necessitates **bulk data extraction**, making the IM1 Bulk API the appropriate and most efficient mechanism for your use case, rather than the Transaction API designed for real-time clinical workflows \[R4, 297, 659\].

4. **Strategic Reporting Configuration Review:** Once connected, ensure careful configuration of the Strategic Reporting organisation group, including all necessary units whose data you wish to extract. Critically, ensure the "Include the shared record" option is enabled to capture comprehensive population data for your research purposes.

5. **Dedicated Gateway PC:** Plan for and implement a dedicated Gateway PC that can remain logged into SystmOne overnight to ensure uninterrupted daily data downloads.

Your immediate next step should be to directly address the discrepancy regarding the TPP development environment access with NHS England. Obtain and verify access to the provided test environment, and then prioritize completing the required witness testing and submitting the actual test scripts.

**Next Step:** I recommend you schedule a call with Joanne Maw or the relevant NHS England IM1 team contact to clarify the status of your TPP test environment access and confirm the specific requirements for the test scripts and data sharing agreement, emphasizing your need for the Bulk API for population-level [research.As](http://research.As) your dedicated consultant, I am here to help you quickly and effectively analyze the provided sources to make strategic recommendations for Fitfile. My expertise spans technical, regulatory, and financial considerations to ensure well-reasoned and supported advice. The knowledge base you've provided includes a security vulnerability remediation report for [pentest.fitfile.net](http://pentest.fitfile.net), a detailed decision from the Competition and Markets Authority (CMA) regarding the anticipated acquisition of EMIS Group PLC by UnitedHealth Group Incorporated, documentation on connecting to TPP's SystmOne via its open API, Fitfile's email correspondence regarding their SCAL submission and integration journey, NHS England Developer Community discussions on IM1 APIs, and several documents from 6B Digital and TPP detailing various IM1 APIs and Strategic Reporting functionalities.

You, Fitfile, are looking to integrate with TPP's SystmOne to bulk extract data for researchers to perform cohort discovery queries and population-level research \[R4\]. This requires understanding how TPP's "Strategic Reporting" functionality is made available via IM1.

## Understanding TPP's Strategic Reporting and IM1 for Bulk Data Extraction

TPP's "Strategic Reporting" solution is designed to provide daily incremental data extracts from SystmOne, their primary care Electronic Patient Record (EPR) system. It's crucial to note that this data is **not intended for, nor should it be used for, direct patient care**. Instead, it serves purposes like yours: providing population-level research data and enabling cohort discovery queries \[R4\]. The data is provided in CSV file format, with one CSV file per table, and can contain either a full history or delta (changed data since the last extract) information.

The "IM1" (Interface Mechanism 1) is a set of API standards developed by NHS Digital to enable third-party applications to integrate with GP clinical systems like EMIS Web, Cegedim Vision, and TPP SystmOne. For your specific goal of bulk data extraction for research, the relevant IM1 interface mechanism is the **Bulk API**. This API empowers your application to gain daily, weekly, or monthly extracts of bulk data feeds of patient or clinical system user data, once GP practice consent has been obtained. This is distinct from the IM1 Patient API (for patient-facing services like appointment booking) or the IM1 Transaction API (for real-time access and updates for medical professionals).

## Strategic Reporting Data Content and Configuration

The Strategic Reporting extract can be configured to include specific tables and fields relevant to your needs. Any new additions (either tables or fields) to the Strategic Reporting extract are not automatically added to your configuration, requiring manual updates if you wish to use them. The extract also supports filtering patient content based on criteria such as patient's sex, age, Read codes in their record, and medication in their record.

A critical option for population-level research is the "Include the shared record" setting. When this option is selected, the extract will include patient data recorded at units outside of your designated recipient organisation group, provided:

1. The patient has consented to share out from the recording unit.

2. The patient has consented to share in to a unit within your organisation group.

Without this option, the extract would only contain patient data explicitly recorded at a unit within your recipient organisation group. This highlights the importance of careful consideration of Information Governance implications when setting this configuration.

You can also choose to "Limit Full Download to last" a certain number of months, which can result in faster full download speeds for specific historical periods, rather than receiving all of an organisation's historical data. Additionally, the "Manage Full Downloads" option allows you to customise when specific tables or new units will receive their full downloads, should they be necessary.

## Integration and Onboarding Process via IM1

The process to integrate with TPP via IM1 for Strategic Reporting (Bulk API) follows a structured path, ensuring compliance with NHS standards. Fitfile has already initiated this by submitting your Supplier Conformance Assessment List (SCAL).

Here's a breakdown of the typical process and Fitfile's current standing:

1. **Prerequisites and SCAL Submission:** Before development, organisations must complete the IM1 Clinical and Information Governance prerequisites form. Your SCAL is then reviewed to evaluate compatibility with provider APIs and ensure compliance with NHS standards. Fitfile submitted its SCAL on November 29, 2024. TPP's clinical team reviewed and approved your product on December 18, 2024.

2. **Model Interface License:** Once compatibility is confirmed, an Approved Developer (such as Fitfile) executes a Model Interface License with each provider (TPP in this case), granting access to the provider’s API test environment.

3. **Testing Phases:**

   - **Unsupported Test Phase:** Developers use a Pairing and Integration Pack (PIP) to build and refine their solution.

   - **Supported Test Phase (Assurance/Witness Testing):** Providers and developers collaborate to conduct assurance tests, ensuring functionality, security, and compliance. NHS Digital provides a Recommendation to Connect Notice (RTCN) after the SCAL is agreed and witness testing is undergone.

      - **Fitfile's Status:** The NHS England IM1 team scheduled a final review of your SCAL for January 8, 2025, with a witness test for the week of January 20, 2025. However, on January 8, 2025, NHS England requested a mitigation report for any medium & high findings from your pen test. This report was provided on April 10, 2025.

      - Additionally, NHS England requested a copy of your data sharing agreement with GPs on January 22, 2025. You responded that you do not have current data sharing agreements with TPP GPs, but have received data from 32 GPs via the approved EMIS data sharing route via IM1.

      - Furthermore, on March 5, 2025, and reiterated on April 2, 2025, NHS England requested completed test scripts showing actual results from your witness tests/outcomes. Fitfile indicated on April 23, 2025, that you did not yet have a TPP development environment set up and therefore unable to perform witness testing or provide TPP-specific test scripts. NHS England then clarified on April 25, 2025, that test access for TPP was provided to Fitfile on March 13, 2024, including details for a test environment (Unit Name: HSCIC Test environment 61, Unit ID: 92HSCIC, Username: pkotsidis0324) and test patient details. They also asked for reasons why Fitfile cannot use "transaction" instead of "BULK".

4. **Go-Live:** Once all requirements are met and NHS England issues a "Recommended to Connect" status, your product can be rolled out to live environments. Fitfile was informed that go-live could only occur from January 7, 2025, due to a change freeze.

## Technical Aspects of Strategic Reporting Download

The transfer mechanism for Strategic Reporting is integrated into the SystmOne client. Downloads are limited to the "owning organisation" (the one that owns the Strategic Reporting group). To receive the daily extract, you need to configure a "Scheduled Job" within SystmOne, typically linked to a "Gateway PC" which should be left running and logged into SystmOne in a locked-out state overnight. This ensures the automated download occurs. You will need to contact TPP to be granted access to the "Scheduled Jobs" screen.

The download process automatically organizes the files: previous downloads are moved into an "Archived" subfolder, and a "manifest file" (SRManifest.csv) is downloaded last. This manifest file indicates whether each included data file is a full history or a delta, and the date range covered. It's recommended to parse the manifest before loading data into an external data warehouse.

## Security Considerations for Strategic Reporting

TPP emphasizes the security of data transfer for Strategic Reporting. In-flight data (during download) is encrypted using industry-standard algorithms over a direct socket connection between the SystmOne client and server via the N3 network. Penetration testing is conducted by a third party to establish the security of this communication. For data at rest, the local folder where the files are written is configured by a SystmOne user with appropriate access rights (granted by a Caldicott Guardian), and local restrictions are expected to prevent unauthorized access to this directory.

## Addressing the "Transaction vs. Bulk" Query

NHS England has specifically asked for clarification on why Fitfile cannot use "transaction" instead of "BULK" for data access. This is a critical distinction:

- **IM1 Transaction API:** This API supports **real-time transactions** between consumer systems and GP's core IT systems. It allows medical professionals to access, retrieve, and *update* patient data, manage appointments, and *create new consultation records*. The purpose is to streamline administrative processes and ensure up-to-date information for direct patient care.

- **IM1 Bulk API:** This API is explicitly designed for obtaining **daily, weekly, or monthly extracts of bulk data feeds** of patient or clinical system user data.

Given Fitfile's goal is to enable researchers to make **cohort discovery queries and population-level research data** \[R4\], the **Bulk API** is the appropriate choice. The Transaction API, while offering real-time access, is focused on individual patient interactions and clinical updates, which is fundamentally different from the need for large, population-level datasets for research and analytics. Attempting to use the Transaction API for bulk data extraction would be inefficient, potentially violate usage policies, and might not provide the comprehensive historical or population-wide data necessary for your stated purpose.

## Recommendations for Fitfile's Next Steps

1. **Resolve Test Environment Access and Test Scripts:** Immediately clarify with NHS England's IM1 team the discrepancy regarding the TPP development environment access. TPP states access was provided on March 13, 2024, and provides login details. You need to confirm if you have successfully accessed this environment. Once access is verified, you must proceed with witness testing in this environment and provide the requested test scripts with actual results. This is a critical blocker to your go-live.

2. **Address Data Sharing Agreement:** Proactively follow up with Joanne Maw regarding the data sharing agreement. Explain your current setup with EMIS data sharing via IM1 and seek specific guidance on what is required for TPP GPs. Understanding their requirements for a TPP-specific data sharing agreement is crucial.

3. **Reinforce Bulk API Rationale:** Clearly articulate to NHS England's IM1 team that your objective is **cohort discovery and population-level research**, which necessitates **bulk data extraction**, making the IM1 Bulk API the appropriate and most efficient mechanism for your use case, rather than the Transaction API designed for real-time clinical workflows \[R4, 297, 659\].

4. **Strategic Reporting Configuration Review:** Once connected, ensure careful configuration of the Strategic Reporting organisation group, including all necessary units whose data you wish to extract. Critically, ensure the "Include the shared record" option is enabled to capture comprehensive population data for your research purposes.

5. **Dedicated Gateway PC:** Plan for and implement a dedicated Gateway PC that can remain logged into SystmOne overnight to ensure uninterrupted daily data downloads.

Your immediate next step should be to directly address the discrepancy regarding the TPP development environment access with NHS England. Obtain and verify access to the provided test environment, and then prioritize completing the required witness testing and submitting the actual test scripts.

**Next Step:** I recommend you schedule a call with Joanne Maw or the relevant NHS England IM1 team contact to clarify the status of your TPP test environment access and confirm the specific requirements for the test scripts and data sharing agreement, emphasizing your need for the Bulk API for population-level research.