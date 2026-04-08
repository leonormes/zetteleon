---
captured: "2026-04-06T18:12:18+01:00 2026-04-06T18:12:18+01:00"
created: 2026-04-06T18:00:04+00:00
modified: 2026-04-08T18:01:19+00:00
source: "https://gemini.google.com/app/dee27ce63d4d52f3"
status: "processing"
tags: ["input"]
title: HEAD You said I am using Auth0 for login in an app. I a...
type: "head"
---

## Raw Output / Content

You

I am using Auth0 for login in an app. I am not sure what all the components are for. Audience for instance. Explain all the bits and what they do

---

Gemini

Navigating Auth0 and the underlying OAuth 2.0 and OpenID Connect protocols can be genuinely baffling at first. There are many moving parts, and the terminology is highly specific.

To make sense of it, it helps to break Auth0 down into the physical "actors" in your system and the "currency" they use to communicate.

Here is a breakdown of all the primary bits and what they actually do:

### The Core Infrastructure

- Tenant: This is your isolated slice of Auth0. It holds all your configurations, users, and apps. You can think of it as your company's specific domain within the Auth0 ecosystem (e.g., `your-company.eu.auth0.com`).
- Applications (Clients): This is the actual software your users interact with. It could be a Single Page Application (React, Angular), a mobile app, or a traditional web app.
  - Client ID: A public alphanumeric string that uniquely identifies your application to Auth0. It is safe to expose this in your frontend code.
    - Client Secret: A private string used to authenticate the application itself to Auth0. Never put this in a frontend application or mobile app; it belongs strictly on a secure backend server.

### APIs and The "Audience"

- APIs (Resource Servers): This is your backend code (e.g., a Node.js or Python server) that holds your sensitive data or performs actions. It relies on Auth0 to tell it if an incoming request is legitimate.
- Audience: This is exactly what you were wondering about. The Audience is the unique identifier of the API that your Application wants to talk to.
  - When your frontend application asks Auth0 to log a user in, it includes the `audience` parameter to say: _"Hey Auth0, please log this user in and give me a token that is specifically valid for the 'Orders API'."_ \* This is a security measure. If an attacker intercepts a token meant for your 'Orders API' (the Audience), they cannot use it to access your 'Billing API' because the token is exclusively scoped to the requested audience.

### Where Users Live

- Connections: These are the sources that actually verify a user's identity.
  - Database Connections: Auth0 stores the email and password hashes directly.
    - Social Connections: Users log in via Google, Apple, or GitHub. Auth0 acts as a middleman.
    - Enterprise Connections: Hooking into a corporate directory like Azure Active Directory or Okta via SAML.

### The "Currency" (Tokens)

When a user successfully authenticates, Auth0 hands back different types of tokens. These are the lifeblood of the system.

- ID Token: Think of this as a digital passport or ID card. It contains information _about_ the user (name, email, profile picture). Your frontend application reads this token to display the user's interface and know who just logged in. It is not meant to be sent to your API.
- Access Token: Think of this as a hotel key card. It does not care _who_ you are; it only cares what doors you are allowed to open. Your frontend application attaches this token to HTTP requests (usually in the `Authorization` header) when asking your backend API for data. Your API validates this token before responding.
- Refresh Token: Access tokens are designed to expire quickly for security reasons (e.g., after 5 minutes). A Refresh Token is a special, long-lived token used by your application to silently request new Access Tokens in the background without forcing the user to type their password in again.

### Customisation

- Actions (formerly Rules and Hooks): These are serverless Node.js functions you can write within Auth0 that run automatically at specific triggers, such as immediately after a user logs in. You can use Actions to add custom roles to a token, block specific IP addresses, or send a webhook to your own database.

---

Would you like me to walk through the exact step-by-step flow of how a user logs in and retrieves these tokens for your specific type of application?
