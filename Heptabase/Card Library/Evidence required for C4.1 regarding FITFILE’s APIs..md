---
created: 2026-05-04T08:01:26+00:00
modified: 2026-05-26T11:43:55+00:00
title: Evidence required for C4.1 regarding FITFILE’s APIs.
---

## Evidence Required for C4.1 regarding FITFILE's APIs

Section C4 of the Digital Technology Assessment Criteria (DTAC) focuses on Interoperability. This is a crucial part of the assessed sections (Section C) that determine the overall success of the assessment. The purpose of C4 is "Establishing how well your product exchanges data with other systems".

C4.1 specifically asks: "Does your product expose any Application Programme Interfaces (API) or integration channels for other consumers?". If the answer is "Yes", you must provide detail and evidence in response to C4.1.1.

The specific details and evidence requested in C4.1.1 are:

1. The APIs (e.g., what they connect to): This requires a description of the APIs your product exposes. What functionality do they offer? What systems, data sources, or services do they interact with or provide access to?. The GDS guidance on API technical standards, referenced by DTAC, suggests developing a specification, such as an OpenAPI Specification, as the first output of your design process. This specification describes the format and responses of your API and is a key piece of evidence detailing the API itself.
2. Set out the healthcare standards of data interoperability e.g., Health Level Seven International (HL7) / Fast Healthcare Interoperability Resources (FHIR): You need to state which specific healthcare interoperability standards are used by your APIs for exchanging data. Evidence would involve demonstrating how your API design, data structures, and messaging comply with these stated standards.
3. Confirm that they follow Government Digital Services Open API Best Practice: The provided `API technical and data standards - ``[GOV.UK](GOV.UK)``.pdf` document outlines these best practices. Evidence here involves demonstrating adherence to the principles and standards within that guidance. This includes aspects like:

   - Designing your API first, based on user needs (developers are users of APIs).
   - Checking for existing APIs before building new ones.
   - Following the Technology Code of Practice and other government data standards, including GDPR and data protection by design.
   - Using the REST API style where appropriate and following its principles.
   - Developing and maintaining an OpenAPI specification.
   - Being secure by design from the outset. API security involves data level security (access control), application level security (authentication/authorisation), and auditing. You should avoid common OWASP API security risks.
   - Using UTF-8 for text encoding.
   - Using JSON for response formats where possible, perhaps JSON:API.
   - Using consistent names for resources.
   - Using standard HTTP responses and documenting error codes.
   - Controlling access and requiring authentication, preferably using the industry standard OAuth 2.0 Authorization Framework. Avoid basic authentication and be cautious with API keys unless used with HTTPS. Define and check resource-level access controls/scopes.
   - Using TLS 1.2 or above for secure communication.
   - Validating all inputs.
   - Configuring appropriate CORS headers.
   - Removing unnecessary endpoints and limiting supported HTTP verbs.
   - Considering performance and scalability, including caching and rate limiting.
   - Logging and monitoring API use, especially for personal data, to comply with GDPR and detect misuse.
   - Having a versioning strategy, such as URI versioning.
   - Using an API management system or gateway can help provide many of these services reliably.

4. Confirm they are documented and freely available: This requires providing proof that comprehensive documentation for your APIs exists and is accessible. Evidence would be links to or copies of your API documentation. The GDS guidance stresses the importance of documentation, including reference documentation, and suggests generating it automatically from your specification where possible. "Freely available" implies the documentation is publicly accessible without payment or restrictive conditions.
5. Third parties have reasonable access to connect: You need to describe the process or mechanisms by which external developers or systems can integrate with your APIs. Evidence could include a description of your developer portal (if you have one, as suggested by GDS guidance), the steps for registration, obtaining necessary credentials (like OAuth 2.0 tokens), accessing the documentation, and potentially accessing a sandbox or test environment.

In summary, the required evidence for C4.1 is primarily comprehensive documentation and clear explanations that demonstrate your APIs exist, function, use relevant healthcare standards, adhere to GDS best practices for design, security, and operation, are well-documented and accessible, and can be reasonably integrated by third parties. The specific types of documents might include API specifications (like OpenAPI documents), architecture descriptions, security policies related to APIs, and links to public documentation and developer resources.

Given that FITFILE states in B2 that they offer a "distributed technology platform and associated services through software "Nodes"" and that their product enables access to and querying of data, linking data, and executing computations, exposing APIs or integration channels seems highly probable. However, the provided excerpt does not contain FITFILE's actual response to C4.1.1.

A logical next step would be to examine FITFILE's specific response to C4.1.1 within the DTAC document (if available) and compare the details and evidence they have provided against the requirements outlined in C4 and the referenced GDS API technical standards. This will allow for an assessment of their stated interoperability capabilities and compliance.
