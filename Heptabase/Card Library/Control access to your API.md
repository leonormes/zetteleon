### Control access to your API

When you build your API, you need to decide the best way to give users access. In general you should make all users of your API authenticate their identities. This is essential if your API deals with personal or sensitive data.

Avoid endpoints that allow anonymous users, as these can:

- increase the [attack surface available to hackers](https://www.security.gov.uk/guidance/secure-by-design/principles/#7-minimise-the-attack-surface)

- make it harder to monitor users that are consuming excessive resources

If you require anonymous endpoints, their responses should be limited to open data. For example the [GOV.UK Content API](https://content-api.publishing.service.gov.uk/) does not require authentication, but only returns metadata and the HTML content of pages published on [GOV.UK](http://GOV.UK). Anonymous endpoints should also be rate limited to prevent excessive or malicious use.

Use the industry standard [OAuth 2.0 Authorization Framework](https://datatracker.ietf.org/doc/html/rfc6749) to manage access to your API. This will make it easier for users to consume your API while giving you better control over the level of access they have.

Never use basic authentication because usernames and passwords are sent encoded, but unencrypted, in the HTTP header. This makes it easy for an attacker to steal them.

You should also avoid using API keys. An API key is a unique identifier that is issued to API users. It needs to be sent with every request – either in the URL, as a request header or as a cookie – and it can easily be intercepted by an attacker and reused. If you do use API keys you should time limit their use and regularly change the keys to keep them secure.

Neither basic nor API key authentication is secure unless used in conjunction with HTTPS.

OAuth 2.0 typically uses digitally signed security tokens in [JWT](https://datatracker.ietf.org/doc/html/rfc7519) (JSON Web Token) format that are passed in the Authenticate header of a request, making them harder to tamper with.

OAuth 2.0 defines ways to authenticate different types of API clients:

- use [client credentials](https://datatracker.ietf.org/doc/html/rfc6749#section-1.3.4) when another service or application is consuming your API, outside of the context of a user

- use [authorization code](https://datatracker.ietf.org/doc/html/rfc6749#section-1.3.1), with the [PKCE](https://datatracker.ietf.org/doc/html/rfc7636) extension, when a user accesses your API – for example, through a web application

As well as authenticating your users, you should define resource-level access controls for your API, and check the authorisation for every request.

When using OAuth 2.0 this means:

- a user must first request the scope of access they need to your API – for example, an order-read or order-write scope

- on each call to your API you should check that the user has the required scope before granting them access

[Defining scopes](https://datatracker.ietf.org/doc/html/rfc6749#section-3.3) in this way allows for fine-grained access control to the endpoints of your API, and means you can include the [authorisation information in your OAS specification](https://spec.openapis.org/oas/latest.html#oauth-flow-object). This makes it easier for consumers to use your API securely.

Authentication and authorisation are features that can be defined and controlled through an API management system. Find out more about how to [manage operations with an API gateway](https://www.gov.uk/guidance/defining-an-api-management-strategy#managing-operations-with-an-api-gateway).

### Secure your API

Follow the [GOV.UK](http://GOV.UK) Service Manual guidance on [using HTTPS](https://www.gov.uk/service-manual/technology/using-https) when serving your API over the web, to make it as secure as possible.

You must use TLS 1.2 or above to secure your API. The National Cyber Security Centre has guidance on [using TLS to securely deliver web services](https://www.ncsc.gov.uk/guidance/using-tls-to-protect-data).

[Validate all inputs](https://www.ncsc.gov.uk/collection/cyber-security-design-principles/making-compromise-difficult) to your API. Endpoints that de-serialise data should enforce schema validation and reject unknown attributes. All parameters (URL and query string) should be validated and type checked before being processed. Otherwise attackers could exploit lax input validation to craft requests that result in unexpected effects.

Configure your API using appropriate [Cross-Origin Resource Sharing (CORS) headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS). This will minimise the risk of cross-origin attacks.

Turn off unnecessary HTTP verbs (GET, PUT, POST, etc), and only allow the verbs your API actually supports on each resource. For example, if users can never be deleted, do not accept DELETE on the users resource.

Remove any endpoints you do not need – for example, test endpoints or stubs for future development – and only expose the endpoints users will actually use.

You can also enforce your content type. For example, if your API only accepts JSON then enforce this through content type headers and reject other types of request.

For a complete list of common security issues to fix in your API, refer to the [OWASP API Security Project](https://owasp.org/www-project-api-security/).