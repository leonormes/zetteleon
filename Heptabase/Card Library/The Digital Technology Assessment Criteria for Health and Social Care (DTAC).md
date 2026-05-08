---
created: 2026-05-04T08:01:26+00:00
modified: 2026-05-08T12:53:44+00:00
title: The Digital Technology Assessment Criteria for Health and Social Care (DTAC)
---

## The Digital Technology Assessment Criteria for Health and Social Care (DTAC)

[C4 - Interoperability criteria  .md](C4%20-%20Interoperability%20criteria%20%20.md)

The requirements for API documentation are found in Section C4 - Interoperability criteria. This section is assessed to establish how well your product exchanges data with other systems.

[If your product exposes any Application Programme Interfaces (APIs) or integration channels for o.md](If%20your%20product%20exposes%20any%20Application%20Programme%20Interfaces%20(APIs)%20or%20integration%20channels%20for%20o.md)

The specific requirements and details related to your API documentation and how your APIs function are:

- You need to provide detail and evidence about your APIs.
- Set out what the APIs connect to.
- Set out the healthcare standards of data interoperability used, such as Health Level Seven International (HL7) / Fast Healthcare Interoperability Resources (FHIR).
- Confirm that they follow Government Digital Services Open API Best Practice. The document notes that Government Digital Services provide guidance on Open API best practice. According to the document, APIs should generally follow these practices and be documented and freely available, with third parties having reasonable access to integrate technologies.
- Confirm they are documented and freely available.
- Confirm that third parties have reasonable access to connect.

From this, you should be aware that the documentation needs to explicitly address these points:

Adherence to GDS Open API Best Practices

Clear description of connectivity and interoperability standards

Confirmation that the documentation is publicly available and free

and assurance that third parties can reasonably access the APIs for integration.

This documentation is crucial for demonstrating compliance in the Interoperability section.

The structure of the DTAC, details about the company and product value proposition (non-assessed sections A and B), the core technical assessment criteria (Section C), and key principles for success (Section D).

### C4 - Interoperability Criteria within the Larger Context of C. Technical Questions

The Digital Technology Assessment Criteria (DTAC) is structured into five core components. Sections A and B provide context and are not assessed. The core assessment criteria are defined in Section C, while Section D details usability and accessibility principles, which are scored but do not contribute to the overall assessment criteria as set out in Section C.

Section C is titled "Technical questions" and is explicitly described as the "Assessed sections". The core criteria in Section C will determine the overall success of the assessment of your product or service. This indicates that performance and compliance within Section C are critical for a product to pass the DTAC assessment. Section C is broken down into four key areas: C1 - Clinical safety, C2 - Data protection, C3 - Technical security, and C4 - Interoperability criteria. Each of these subsections is assessed, and collectively, they form the basis for evaluating the product's technical suitability and safety for use in health and social care settings.

C4 - Interoperability criteria is one of these four crucial assessed sections. Its specific purpose is "Establishing how well your product exchanges data with other systems". The document emphasises the importance of interoperability within the health and social care system to provide a seamless care journey. This means ensuring that relevant technologies can work together, exchanging information smoothly across different hardware and software systems, including the data contained within them. An example provided is the need for data from a patient's blood glucose monitor to be downloadable onto an appropriate clinical system without being restricted to one type. Technologies that need to interface with clinical record systems must also be interoperable.

The DTAC highlights several benefits associated with good interoperability. It is stated that good interoperability "reduces expenditure, complexity and delivery times on local system integration projects by standardising technology and interface specifications and simplifying integration". Furthermore, it allows integration solutions to be "replicated and scaled up" and "opens the market for innovation by defining the standards to develop upfront".

While Section C criteria are universally assessed, Section C4 specifically "should be tailored to the specific use case of the product and the needs of the buyer". However, it must still "reflect the standards used within the NHS and social care and direction of travel". Responses and details provided in this section should relate specifically to the product being assessed, not the organisation in general.

The C4 section includes specific questions designed to evaluate the product's interoperability capabilities:

- C4.1: Asks if the product exposes any Application Programme Interfaces (APIs) or integration channels for other consumers. If the answer is yes, the developer must provide details and evidence, including what the APIs connect to, the healthcare data interoperability standards used (e.g., HL7 / FHIR), confirmation that they follow Government Digital Services Open API Best Practice, confirmation that they are documented and freely available, and how third parties have reasonable access to connect. If no, a reason must be provided. Guidance on APIs and standards is available from the NHS website developer portal and Government Digital Services.
- C4.2: Asks if the product uses the NHS number to identify patient record data. If yes, it asks if it uses NHS Login to establish a user's verified NHS number. If NHS Login is not used, the rationale, how the NHS number is established, and associated security measures must be set out. If the product does not identify patient record data, this option can be selected.
- C4.3: Evaluates the product's capability for read/write operations with electronic health records (EHRs) using industry standards for secure interoperability (e.g., OAuth 2.0, TLS 1.2). If yes, the standard must be detailed. If no, the reasons, mitigations, methodology, and security measures must be stated. An option exists if the product does not read/write into EHRs.
- C4.4: Asks if the product is a wearable or device or integrates with them. If yes, evidence must be provided demonstrating compliance with ISO/IEEE 11073 Personal Health Data (PHD) Standards. If no, the developer should continue to Section D.

In summary, C4 is a vital part of the mandatory technical assessment (Section C) within DTAC. It assesses a product's ability to exchange data effectively and securely with other systems, which is fundamental for a seamless care journey in the NHS and social care. Compliance with interoperability standards and demonstrating the capacity to integrate with existing healthcare infrastructure is a key requirement for successful DTAC assessment.

Given the importance of C4 within the assessed Section C criteria, a logical next step would be to specifically examine FITFILE's provided responses to the questions within C4 (C4.1 to C4.4) to understand how their product measures up against these interoperability requirements and standards.
