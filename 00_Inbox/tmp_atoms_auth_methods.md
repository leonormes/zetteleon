---
type: tmp_atoms
status: tmp
source_title: "Every API Authentication Method Explained"
source_url: "https://youtube.com/watch?v=_lTECv25N2U"
captured_utc: "2026-04-13T09:18:17+01:00"
signal_to_noise: "95% signal / 5% noise"
---

- Discarded channel branding ("Cloud X Berry").
- Discarded conversational transitions ("The video explains...", "Detailed what they are...").
- Discarded anecdotal advice on "don't choose the wrong one" unless specific to a mechanism.

### Atom 1: Basic Authentication
- Kind: mechanism
- Statement: Basic Authentication transmits credentials as a Base64-encoded string within the HTTP authorisation header of every request.
- Scope & Conditions: Requires HTTPS to prevent credential interception.
- Evidence: "The client sends a username and password with every HTTP request via the authorisation header. The credentials are only Base64 encoded..." ([00:29](http://www.youtube.com/watch?v=_lTECv25N2U&t=29)).
- Implications:
    - High risk of credential exposure if transport security fails.
    - Simplest implementation for legacy systems.
- Validation: 
    - [x] Single-Idea
    - [x] Boundary
    - [x] Conjunction
    - [x] Reusability
- Confidence: high
- Tags: [security, authentication, basic-auth, http]

### Atom 2: Digest Authentication
- Kind: mechanism
- Statement: Digest Authentication uses a challenge-response mechanism to verify credentials via a hashed response.
- Scope & Conditions: Prevents raw password transmission but is considered complex for modern token-based systems.
- Evidence: "Uses a challenge-response mechanism. The server sends a challenge, and the client generates a hashed response using the password..." ([01:07](http://www.youtube.com/watch?v=_lTECv25N2U&t=67)).
- Implications:
    - Mitigates replay attacks compared to Basic Auth.
    - Rarely used in modern API design.
- Validation: 
    - [x] Single-Idea
    - [x] Boundary
    - [x] Conjunction
    - [x] Reusability
- Confidence: high
- Tags: [security, authentication, digest-auth, hashing]

### Atom 3: Session Authentication
- Kind: mechanism
- Statement: Session Authentication identifies clients using a server-generated session ID stored in a browser cookie.
- Scope & Conditions: Standard for server-rendered web applications.
- Evidence: "The server creates a session... and sends a session ID back to the browser (usually as a cookie). The browser automatically sends this cookie on subsequent requests." ([01:42](http://www.youtube.com/watch?v=_lTECv25N2U&t=102)).
- Implications:
    - Introduces scaling challenges due to server-side state requirements.
    - Provides a seamless experience for traditional web apps.
- Validation: 
    - [x] Single-Idea
    - [x] Boundary
    - [x] Conjunction
    - [x] Reusability
- Confidence: high
- Tags: [authentication, sessions, cookies, stateful]

### Atom 4: API Keys
- Kind: mechanism
- Statement: API Keys act as unique identifiers that authenticate specific applications rather than individual users.
- Scope & Conditions: Typically used for public APIs or service-to-service communication.
- Evidence: "A unique identifier is assigned to an application... API keys typically identify the application rather than the individual user." ([02:21](http://www.youtube.com/watch?v=_lTECv25N2U&t=141)).
- Implications:
    - Easy to implement for rate limiting and usage tracking.
    - Low security for user-specific data access.
- Validation: 
    - [x] Single-Idea
    - [x] Boundary
    - [x] Conjunction
    - [x] Reusability
- Confidence: high
- Tags: [authentication, api-keys, application-identity]

### Atom 5: Bearer Tokens
- Kind: mechanism
- Statement: Bearer Tokens grant access to any entity possessing the token without requiring server-side session storage.
- Scope & Conditions: Widely used in modern stateless APIs.
- Evidence: "The term 'bearer' simply means whoever holds the token is allowed access... server does not need to store session state." ([02:51](http://www.youtube.com/watch?v=_lTECv25N2U&t=171)).
- Implications:
    - Requires rigorous protection (e.g., short expiry, HTTPS).
    - Enables stateless architecture.
- Validation: 
    - [x] Single-Idea
    - [x] Boundary
    - [x] Conjunction
    - [x] Reusability
- Confidence: high
- Tags: [security, authentication, bearer-tokens, stateless]

### Atom 6: JSON Web Tokens (JWT)
- Kind: definition
- Statement: JSON Web Tokens are a digitally signed format for transmitting structured JSON payloads used in stateless verification.
- Scope & Conditions: Used as a token format, not an authentication protocol.
- Evidence: "A JWT contains a structured JSON payload with user information and is digitally signed by the server... verify requests without having to query a database." ([03:25](http://www.youtube.com/watch?v=_lTECv25N2U&t=205)).
- Implications:
    - Reduces database load through self-contained validation.
    - Difficult to revoke before expiry without additional infrastructure.
- Validation: 
    - [x] Single-Idea
    - [x] Boundary
    - [x] Conjunction
    - [x] Reusability
- Confidence: high
- Tags: [authentication, jwt, tokens, digital-signatures]

### Atom 7: Access Tokens
- Kind: definition
- Statement: Access tokens are short-lived credentials used to perform requests against protected API resources.
- Scope & Conditions: Limited lifespan reduces the window of risk if the token is compromised.
- Evidence: "Access tokens are short-lived tokens used to access protected APIs, limiting the window of risk if compromised." ([04:01](http://www.youtube.com/watch?v=_lTECv25N2U&t=241)).
- Implications:
    - Enhances security posture through frequent rotation.
    - Requires a mechanism for renewal (e.g., Refresh Tokens).
- Validation: 
    - [x] Single-Idea
    - [x] Boundary
    - [x] Conjunction
    - [x] Reusability
- Confidence: high
- Tags: [security, tokens, access-control]

### Atom 8: Refresh Tokens
- Kind: mechanism
- Statement: Refresh tokens are long-lived credentials used to obtain new access tokens without requiring user re-authentication.
- Scope & Conditions: Must be stored more securely than access tokens.
- Evidence: "Refresh tokens are longer-lived and are used to request new access tokens without forcing the user to repeatedly enter their credentials." ([04:01](http://www.youtube.com/watch?v=_lTECv25N2U&t=241)).
- Implications:
    - Improves user experience by maintaining sessions.
    - Increases risk if the storage medium is compromised.
- Validation: 
    - [x] Single-Idea
    - [x] Boundary
    - [x] Conjunction
    - [x] Reusability
- Confidence: high
- Tags: [authentication, tokens, user-experience]

### Atom 9: OAuth 2.0
- Kind: definition
- Statement: OAuth 2.0 is an authorisation framework that allows applications to access resources on behalf of a user without password exposure.
- Scope & Conditions: Focuses on authorisation rather than identity verification.
- Evidence: "Allows applications to access resources on behalf of a user without seeing the user's password... focuses solely on authorisation, not identity verification." ([04:28](http://www.youtube.com/watch?v=_lTECv25N2U&t=268)).
- Implications:
    - Industry standard for third-party integrations.
    - Requires an additional layer (like OIDC) for identity.
- Validation: 
    - [x] Single-Idea
    - [x] Boundary
    - [x] Conjunction
    - [x] Reusability
- Confidence: high
- Tags: [authorisation, oauth2, security, framework]

### Atom 10: OpenID Connect (OIDC)
- Kind: definition
- Statement: OpenID Connect is an identity layer built on top of OAuth 2.0 that provides verified user information via an ID token.
- Scope & Conditions: Enables modern "Sign in with" identity providers.
- Evidence: "An identity layer built on top of OAuth 2.0. It introduces an 'ID token' containing verified information about the user..." ([05:05](http://www.youtube.com/watch?v=_lTECv25N2U&t=305)).
- Implications:
    - Standardises identity across different platforms.
    - Leverages OAuth 2.0 flows for secure transport.
- Validation: 
    - [x] Single-Idea
    - [x] Boundary
    - [x] Conjunction
    - [x] Reusability
- Confidence: high
- Tags: [identity, oidc, authentication, oauth2]

### Atom 11: Single Sign-On (SSO)
- Kind: definition
- Statement: Single Sign-On is a user experience pattern that provides access to multiple applications through a single authentication event.
- Scope & Conditions: Often implemented using protocols like OIDC or SAML.
- Evidence: "A user experience rather than a specific protocol. It allows a user to sign in just once to gain access to multiple applications..." ([05:37](http://www.youtube.com/watch?v=_lTECv25N2U&t=337)).
- Implications:
    - Reduces password fatigue for users.
    - Simplifies identity management for organisations.
- Validation: 
    - [x] Single-Idea
    - [x] Boundary
    - [x] Conjunction
    - [x] Reusability
- Confidence: high
- Tags: [ux, sso, identity-management, productivity]
