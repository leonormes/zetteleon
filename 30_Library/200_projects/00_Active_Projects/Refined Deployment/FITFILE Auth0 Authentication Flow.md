---
aliases: []
confidence: 
created: 2025-09-23T08:41:59Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:11Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: FITFILE Auth0 Authentication Flow
type:
uid: 
updated: 
version:
---

## FITFILE Auth0 Authentication Flow - Technical Wiki

### Overview

This document explains how Auth0 authentication works for FITFILE application's, using the CUH Production deployment (`cuh-prod-1.fitfile.net`) as an example. The authentication flow follows the OAuth 2.0 Authorization Code flow with PKCE (Proof Key for Code Exchange) for enhanced security.

### Architecture Components

#### 1. Auth0 Tenant

- **Domain**: `fitfile-prod.eu.auth0.com`
- **Purpose**: Central identity provider for all FITFILE production deployments
- **Location**: Auth0 cloud service (EU region)
- **Configuration**: Managed via Terraform in `/central-services/auth0/prod/`

#### 2. FITFILE Application (CUH Example)

- **Public URL**: `https://cuh-prod-1.fitfile.net`
- **Private URL**: `https://cuh-prod-1.privatelink.fitfile.net`
- **Purpose**: Healthcare data analytics platform
- **Authentication**: Requires Auth0 login for all users

#### 3. Auth0 Resource Server

- **Identifier**: `https://cuh-prod-1.privatelink.fitfile.net`
- **Purpose**: Defines the API audience for JWT tokens
- **Token Lifetime**: 300 seconds (5 minutes)
- **Signing Algorithm**: RS256

#### 4. Auth0 Application (Client)

- **Type**: Single Page Application (SPA)
- **Grant Types**: Authorization Code with PKCE
- **Purpose**: Represents the FITFILE frontend application in Auth0

### Authentication Flow

#### Step 1: User Accesses Application

```sh
User → https://cuh-prod-1.fitfile.net
```

- User navigates to the FITFILE application
- Application detects unauthenticated user
- Frontend JavaScript initiates Auth0 authentication

#### Step 2: Redirect to Auth0

```sh
Browser → https://fitfile-prod.eu.auth0.com/authorize?
  client_id=<client_id>&
  response_type=code&
  redirect_uri=https://cuh-prod-1.fitfile.net/callback&
  audience=https://cuh-prod-1.privatelink.fitfile.net&
  scope=openid profile email&
  code_challenge=<pkce_challenge>&
  code_challenge_method=S256
```

**Parameters Explained:**

- `client_id`: Identifies the FITFILE application to Auth0
- `response_type=code`: Requests authorization code (OAuth 2.0)
- `redirect_uri`: Where Auth0 sends user after authentication
- `audience`: Specifies which API the token is for
- `scope`: Requested user information (OpenID Connect)
- `code_challenge`: PKCE security parameter

#### Step 3: User Authentication

```sh
User → Auth0 Login Page → Identity Provider
```

- Auth0 presents login form or redirects to identity provider
- User enters credentials (username/password, SSO, etc.)
- **MFA Enabled**: Multi-factor authentication required
- Auth0 validates credentials against configured identity sources

#### Step 4: Authorization Code Return

```sh
Auth0 → https://cuh-prod-1.fitfile.net/callback?code=<auth_code>&state=<state>
```

- Auth0 redirects back to application with authorization code
- Code is temporary and single-use
- State parameter prevents CSRF attacks

#### Step 5: Token Exchange

```sh
FITFILE App → Auth0 Token Endpoint
POST https://fitfile-prod.eu.auth0.com/oauth/token
{
  "grant_type": "authorization_code",
  "client_id": "<client_id>",
  "code": "<auth_code>",
  "redirect_uri": "https://cuh-prod-1.fitfile.net/callback",
  "code_verifier": "<pkce_verifier>"
}
```

#### Step 6: JWT Tokens Returned

```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIs...",
  "id_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIs...",
  "token_type": "Bearer",
  "expires_in": 300
}
```

**Token Types:**

- **Access Token**: Used for API calls to FITFILE backend
- **ID Token**: Contains user profile information
- **Refresh Token**: Used to obtain new access tokens (if configured)

#### Step 7: API Authentication

```sh
FITFILE Frontend → FITFILE Backend API
Authorization: Bearer <access_token>
```

- All API calls include the JWT access token
- Backend validates token signature using Auth0 public keys
- Token contains audience claim matching the resource server

### Key Configuration Components

#### 1. Redirect URLs

```javascript
// Allowed callback URLs after authentication
const redirectUrls = [
  "https://cuh-prod-1.fitfile.net/callback",
  "https://cuh-prod-1.fitfile.net/silent-callback" // Silent renewal
  // Additional URLs for other deployments...
]
```

#### 2. Logout URLs

```javascript
// Allowed URLs after logout
const logoutUrls = [
  "https://cuh-prod-1.fitfile.net/",
  "https://*.fitfile.net/fitfile",
  "https://*.net.stgeorges.nhs.uk/fitfile", // NHS trust domains
  "https://*.kingsch.nhs.uk/fitfile"
]
```

#### 3. Web Origins

```javascript
// Allowed origins for CORS
const webOrigins = [
  "https://cuh-prod-1.fitfile.net",
  "https://*.fitfile.net",
  "https://*.net.stgeorges.nhs.uk",
  "https://*.kingsch.nhs.uk"
]
```

#### 4. JWT Token Structure

```json
{
  "header": {
    "typ": "JWT",
    "alg": "RS256",
    "kid": "<key_id>"
  },
  "payload": {
    "iss": "https://fitfile-prod.eu.auth0.com/",
    "sub": "auth0|<user_id>",
    "aud": "https://cuh-prod-1.privatelink.fitfile.net",
    "iat": 1695456789,
    "exp": 1695457089,
    "azp": "<client_id>",
    "scope": "openid profile email"
  }
}
```

### Security Features

#### 1. Multi-Factor Authentication (MFA)

- **Status**: Enabled for all users
- **Methods**: SMS, Email, Authenticator apps
- **Enforcement**: Required for all authentication attempts

#### 2. PKCE (Proof Key for Code Exchange)

- **Purpose**: Prevents authorization code interception attacks
- **Implementation**: Code challenge/verifier pair
- **Required**: For all Single Page Applications

#### 3. Token Security

- **Signing**: RS256 asymmetric encryption
- **Lifetime**: 5 minutes (short-lived for security)
- **Validation**: Backend verifies signature using Auth0 public keys
- **Audience**: Tokens are scoped to specific applications

#### 4. CORS Protection

- **Web Origins**: Strictly controlled allowed origins
- **Redirect URLs**: Whitelist of allowed callback URLs
- **State Parameter**: CSRF protection during OAuth flow

### Integration with FITFILE Components

#### 1. SpiceDB Authorization

```yaml
spicedb_host: "ac.fitfile.net:443"
spicedb_psk: "997bXKi@6mIW"
```

- **Purpose**: Fine-grained authorization after authentication
- **Integration**: Auth0 user ID mapped to SpiceDB subjects
- **Permissions**: Role-based access control for healthcare data

#### 2. PowerBI Integration

```javascript
// Additional application for PowerBI embedding
const powerBiUrls = ["https://oauth.powerbi.com/views/oauthredirect.html"]
```

#### 3. Service Accounts

- **Purpose**: Machine-to-machine authentication
- **Grant Type**: Client Credentials
- **Usage**: Backend services, data pipelines, monitoring

### Deployment-Specific Configuration

#### CUH Production (`cuh-prod-1`)

```hcl
cuh-prod-1 = {
  tenant_name                               = "CUH Prod 1"
  api_name                                  = "CUH Prod 1"
  api_audience                              = "https://cuh-prod-1.privatelink.fitfile.net"
  enabled_apis                              = []
  api_token_lifetime                        = 300 # 5 Minutes
  api_token_lifetime_web                    = 300
  whitelist_api_audience_for_login_redirect = true
}
```

**Key Points:**

- **Private Audience**: Uses private link domain for internal API calls
- **Short Token Lifetime**: Enhanced security with 5-minute tokens
- **Whitelisted Audience**: Allows audience in login redirects

### Troubleshooting Common Issues

#### 1. Token Validation Failures

- **Cause**: Audience mismatch between frontend and backend
- **Solution**: Ensure `api_audience` matches backend validation
- **Check**: JWT payload `aud` claim

#### 2. CORS Errors

- **Cause**: Domain not in `additional_web_origins`
- **Solution**: Add domain to allowed origins list
- **Note**: Wildcards supported for subdomains

#### 3. Redirect URI Mismatch

- **Cause**: Callback URL not in allowed redirect URLs
- **Solution**: Add exact URL to `additional_login_redirect_urls`
- **Important**: URLs must match exactly (including trailing slashes)

#### 4. Token Expiry

- **Cause**: 5-minute token lifetime
- **Solution**: Implement token refresh mechanism
- **Best Practice**: Use silent authentication for seamless renewal

### Monitoring and Logging

#### Auth0 Logs

- **Location**: Auth0 Dashboard → Logs
- **Events**: Login attempts, token exchanges, errors
- **Retention**: 30 days (varies by plan)

#### Application Logs

- **Frontend**: Browser console, application monitoring
- **Backend**: API authentication logs, token validation
- **Infrastructure**: Load balancer access logs

### Security Best Practices

1. **Token Storage**: Store tokens securely (memory, secure cookies)
2. **HTTPS Only**: All Auth0 communication over HTTPS
3. **Regular Rotation**: Rotate client secrets regularly
4. **Monitoring**: Monitor for suspicious authentication patterns
5. **Least Privilege**: Grant minimum required scopes
6. **Token Validation**: Always validate tokens on backend
7. **Logout**: Implement proper logout clearing all tokens

### Related Documentation

- [Auth0 Documentation](https://auth0.com/docs)
- [OAuth 2.0 RFC](https://tools.ietf.org/html/rfc6749)
- [OpenID Connect Specification](https://openid.net/connect/)
- [PKCE RFC](https://tools.ietf.org/html/rfc7636)
- [JWT RFC](https://tools.ietf.org/html/rfc7519)

---

**Last Updated**: September 2025
**Maintained By**: FITFILE Platform Team
**Configuration Location**: `/central-services/auth0/prod/`

## **Key Sections:**

### **🏗️ Architecture Components**

- Auth0 Tenant configuration
- FITFILE Application setup
- Resource Server and Client definitions

### **🔄 Complete Authentication Flow**

- Step-by-step user login process
- OAuth 2.0 Authorization Code flow with PKCE
- Token exchange and JWT structure

### **🔧 Technical Configuration**

- Redirect URLs, logout URLs, and web origins
- JWT token structure and validation
- Security parameters and settings

### **🔒 Security Features**

- Multi-Factor Authentication (MFA)
- PKCE implementation
- Token security and CORS protection

### **🔗 FITFILE Integration**

- SpiceDB authorization integration
- PowerBI embedding support
- Service account configuration

### **🚨 Troubleshooting Guide**

- Common authentication issues
- CORS and redirect URI problems
- Token validation failures

### **📊 Monitoring & Best Practices**

- Logging and monitoring approaches
- Security recommendations
- Token management best practices
