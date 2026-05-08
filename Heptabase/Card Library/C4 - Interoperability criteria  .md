---
created: 2026-05-04T08:01:26+00:00
modified: 2026-05-08T12:53:37+00:00
title: "C4 - Interoperability criteria  "
---

## C4 - Interoperability Criteria

### Establishing how well Your Product Exchanges Data with other Systems

To provide a seamless care journey, it is important that relevant technologies in the health and social care system are interoperable, in terms of hardware, software and the data contained within. For example, it is important that data from a patient's ambulatory blood glucose monitor can be downloaded onto an appropriate clinical system without being restricted to one type. Those technologies that need to interface within clinical record systems must also be interoperable. Application Programme Interfaces (APIs) should follow the Government Digital Services Open API Best Practices, be documented and freely available and third parties should have reasonable access in order to integrate technologies.

Good interoperability reduces expenditure, complexity and delivery times on local system integration projects by standardising technology and interface specifications and simplifying integration. It allows it to be replicated and scaled up and opens the market for innovation by defining the standards to develop upfront.

This section should be tailored to the specific use case of the product and the needs of the buyer however it should reflect the standards used within the NHS and social care and direction of travel.

Please provide details relating to the specific technology and not generally to your organisation.

| Code | Question | Options | Supporting information | Scoring criteria |

|---|---|---|---|---|

| C4.1 | Does your product expose any Application Programme Interfaces (API) or integration channels for other consumers? | Yes \~\~ | No\~\~ | The NHS website developer portal provides guidance on [APIs and the NHS](https://developer.api.nhs.uk/). Government Digital Services provide guidance on [Open API best practice](https://www.gov.uk/government/collections/api-design-guidance). |

| C4.1.1 | If yes, please provide detail and evidence: The API's (e.g., what they connect to) set out the healthcare standards of data interoperability e.g., Health Level Seven International (HL7) / Fast Healthcare Interoperability Resources (FHIR) Confirm that they follow Government Digital Services Open API Best Practice Confirm they are documented and freely available Third parties have reasonable access to connect If no, please set out why your product does not have APIs. | |  | |

| C4.2 | Do you use NHS number to identify patient record data? | \~\~Yes | No | \~\~ No because product does not identify patient record data |

| C4.2.1 | If yes, please confirm whether it uses NHS Login to establish a user's verified NHS number. If no, please set out the rationale, how your product established NHS number and the associated security measures in place. | Free text | |  |

| C4.3 | Does your product have the capability for read/write operations with electronic health records (EHRs) using industry standards for secure interoperability (e.g. OAuth 2.0, TLS 1.2) | Yes \~\~ | No | No because the product does not read/ write into EHRs\~\~ |

| C4.3.1 | If yes, please detail the standard | Free text | |  |

| C4.3.2 | If no, please state the reasons and mitigations, methodology and security measures. | Free text | |  |

| C4.4 | Is your product a wearable or device, or does it integrate with them? | \~\~Yes | \~\~ No | If no, continue to section D. |

| C4.4.1 | If yes, provide evidence of how it complies with ISO/IEEE 11073 Personal Health Data (PHD) Standards. | Provided | No evidence available | [Access the ISO Standard.](https://www.iso.org/standard/46493.html) This is a paid-for document. |
