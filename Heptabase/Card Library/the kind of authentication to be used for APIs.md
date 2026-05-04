# the kind of authentication to be used for APIs

Okay, I understand. I am here to be your thought partner, drawing on the provided sources to help you quickly analyze information and develop well-supported strategic recommendations for senior leadership. My knowledge base is built from the documents you have given me, including excerpts from the DTAC criteria document (`20250427_DTAC_``[FITFILE.md](FITFILE.md)`) and the [GOV.UK](GOV.UK) guidance on API technical and data standards (`API technical and data standards - ``[GOV.UK](GOV.UK)``.pdf`). I can navigate these materials to provide summaries, specific facts, clarify complex topics, and suggest areas for further analysis, always citing the sources that support my responses.

Addressing your query about the kind of authentication to be used for APIs, the sources do specify recommended and preferred types of authentication.

The Government Digital Service (GDS) guidance on API technical and data standards, which is referenced by the DTAC criteria in relation to APIs, explicitly addresses controlling access to your API and the methods of authentication.

The guidance states that in general, you should make all users of your API authenticate their identities. This is essential if your API deals with personal or sensitive data.

The recommended industry standard to manage access to your API is the **OAuth 2.0 Authorization Framework**. Using OAuth 2.0 makes it easier for users to consume your API while giving you better control over the level of access they have. OAuth 2.0 typically uses digitally signed security tokens, often in JWT (JSON Web Token) format, which are harder to tamper with. The guidance outlines specific OAuth 2.0 flows for different client types:

- Use **client credentials** when another service or application is consuming your API outside the context of a user.

- Use **authorization code** with the PKCE extension when a user accesses your API, for example, through a web application.

The guidance advises against using certain authentication methods:

- **Basic authentication** should never be used because usernames and passwords are sent encoded but unencrypted in the HTTP header, making them easy for an attacker to steal.

- You should also avoid using **API keys**. An API key is a unique identifier sent with every request and can easily be intercepted and reused by an attacker. If you do use API keys, you should time limit their use and regularly change the keys to keep them secure.

Crucially, the guidance notes that neither basic authentication nor API key authentication is secure *unless* used in conjunction with HTTPS. It is a requirement to secure your API using HTTPS, specifically TLS 1.2 or above, when serving it over the web.

Beyond authentication (verifying identity), the sources also emphasize the importance of **authorization** (controlling access to resources). When using OAuth 2.0, you should define resource-level access controls and check the authorization for every request. This involves defining scopes, which allow for fine-grained access control to API endpoints. Authentication and authorization features can be defined and controlled through an API management system.

In summary, the sources specify that OAuth 2.0 is the recommended standard for API authentication, while advising against basic authentication and API keys unless used with HTTPS and other security measures. The use of HTTPS/TLS 1.2+ is required regardless of the authentication method chosen.

Given that FITFILE's product involves accessing, querying, linking, and computing data, and is intended for use by health researchers and planners, understanding how they implement these specified authentication and authorization standards is critical for a DTAC assessment, particularly under the Interoperability (C4) and Technical Security (C3) sections.

A potential next step could be to examine FITFILE's specific response to C4.1.1 (if available in the full document) to see what authentication and authorization mechanisms they state they use and how they provide evidence of compliance with these GDS standards.