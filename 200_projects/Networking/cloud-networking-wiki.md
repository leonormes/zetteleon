---
aliases: []
confidence: 
created: 2025-10-29T07:09:57Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:45Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [topic/technology/networking/cloud-networking]
title: cloud-networking-wiki
type:
uid: 
updated: 
version:
---

## Cloud Network Devices Wiki

A comprehensive guide to understanding network devices from a data-centric perspective, with AWS and Azure product mappings.

---

### 1. Load Balancer

#### Generic Description

A load balancer distributes incoming network traffic across multiple backend servers to ensure high availability, reliability, and optimal resource utilization. It acts as a reverse proxy, sitting between clients and servers.

#### Cloud Products
- **AWS**:
  - Application Load Balancer (ALB) - Layer 7 (HTTP/HTTPS)
  - Network Load Balancer (NLB) - Layer 4 (TCP/UDP)
  - Gateway Load Balancer (GWLB) - Layer 3 (IP packets)
  - Classic Load Balancer (CLB) - Legacy, both Layer 4 & 7
- **Azure**:
  - Azure Load Balancer - Layer 4 (TCP/UDP)
  - Azure Application Gateway - Layer 7 (HTTP/HTTPS)
  - Azure Front Door - Global Layer 7 load balancer
  - Azure Traffic Manager - DNS-based load balancer

#### Data-Centric Example

**Incoming Packet:**

```sh
Source IP: 203.0.113.45 (Client)
Destination IP: 198.51.100.10 (Load Balancer VIP)
Source Port: 54321
Destination Port: 443 (HTTPS)
Protocol: TCP
Payload: HTTP Request - GET /api/users HTTP/1.1
Headers: Host: api.example.com, User-Agent: Mozilla/5.0...
```

**Load Balancer Processing:**
1. Terminates TCP connection
2. Parses HTTP headers (for ALB)
3. Applies routing rules based on path (/api/users)
4. Selects healthy backend server (10.0.1.25) using round-robin algorithm
5. Establishes new connection to backend

**Forwarded Packet:**

```sh
Source IP: 10.0.0.50 (Load Balancer Internal IP)
Destination IP: 10.0.1.25 (Backend Server)
Source Port: 48392 (Ephemeral)
Destination Port: 8080
Protocol: TCP
Payload: GET /api/users HTTP/1.1
Headers: Host: api.example.com, X-Forwarded-For: 203.0.113.45...
```

#### Functional Requirements

**What It DOES:**
- Distributes traffic across multiple targets using algorithms (round-robin, least connections, IP hash)
- Performs health checks on backend targets
- Terminates SSL/TLS connections (SSL offloading)
- Maintains session persistence (sticky sessions)
- Routes based on content (path, host, headers) for Layer 7
- Provides high availability through redundancy
- Scales automatically based on traffic

**How It Works:**
- Listens on configured ports and protocols
- Maintains a pool of registered backend targets
- Monitors target health via periodic health checks
- Uses load balancing algorithms to select targets
- Translates source/destination addresses (NAT)
- Can buffer requests/responses

**What It Does NOT Do:**
- Does not inspect deep packet content for security threats
- Does not authenticate users or validate credentials
- Does not modify application logic or business rules
- Does not provide encryption beyond SSL/TLS termination
- Does not cache content (unless combined with CDN features)
- Does not filter traffic based on security rules (not a firewall)
- Does not provide DDoS protection (requires separate service)

---

### 2. Firewall

#### Generic Description

A firewall is a network security device that monitors and controls incoming and outgoing network traffic based on predetermined security rules. It establishes a barrier between trusted internal networks and untrusted external networks.

#### Cloud Products
- **AWS**:
  - AWS Network Firewall - Managed Layer 3-7 firewall
  - Security Groups - Stateful virtual firewall at instance level
  - Network ACLs (NACLs) - Stateless firewall at subnet level
- **Azure**:
  - Azure Firewall - Managed Layer 3-7 firewall
  - Network Security Groups (NSGs) - Firewall rules at subnet/NIC level
  - Azure Firewall Premium - Advanced threat protection

#### Data-Centric Example

**Incoming Packet:**

```sh
Source IP: 185.220.101.50 (External Internet)
Destination IP: 198.51.100.20 (Public Server IP)
Source Port: 44567
Destination Port: 22 (SSH)
Protocol: TCP
TCP Flags: SYN (Connection initiation)
Payload: SSH handshake
```

**Firewall Processing:**
1. Receives packet at ingress interface
2. Checks against security rules (top to bottom)
3. Rule 1: Allow TCP 443 from any → No match
4. Rule 2: Allow TCP 80 from any → No match
5. Rule 3: Allow TCP 22 from 10.0.0.0/8 → No match (source is external)
6. Rule 4: Deny TCP 22 from any → **MATCH**
7. Logs the denied connection attempt
8. Drops packet silently (or sends TCP RST)

**Action Taken:**

```sh
Action: DENY
Reason: Rule #4 - SSH access not allowed from Internet
Packet: DROPPED
Log Entry: [2025-10-29 14:32:15] DENY TCP 185.220.101.50:44567 → 198.51.100.20:22
State Table: No entry created (connection blocked)
```

**Allowed Packet Example:**

```sh
Source IP: 203.0.113.100 (External Internet)
Destination IP: 198.51.100.20
Destination Port: 443 (HTTPS)
Protocol: TCP
Action: ALLOW (Rule #1)
State Table Entry Created:
  - Connection: 203.0.113.100:55432 → 198.51.100.20:443
  - State: ESTABLISHED
  - Return traffic automatically allowed (stateful)
```

#### Functional Requirements

**What It DOES:**
- Filters packets based on IP addresses, ports, and protocols
- Maintains stateful connection tracking
- Blocks or allows traffic based on security rules
- Logs traffic for audit and analysis
- Protects against network-layer attacks
- Performs Network Address Translation (NAT)
- Supports both ingress and egress filtering
- Creates DMZ zones for public-facing servers

**How It Works:**
- Inspects packet headers (source/dest IP, ports, protocol)
- Evaluates rules in priority order (usually top to bottom)
- Uses connection state tables for stateful inspection
- Default deny policy (implicit deny at the end)
- Can operate at Layer 3 (network) and Layer 4 (transport)
- Advanced firewalls inspect up to Layer 7 (application)

**What It Does NOT Do:**
- Does not decrypt SSL/TLS traffic by default
- Does not inspect encrypted payload content
- Does not provide application-layer authentication
- Does not balance load across servers
- Does not cache or optimize content
- Does not protect against application-layer attacks (without Layer 7 features)
- Does not prevent attacks from already-established connections
- Does not provide malware scanning (needs additional features)

---

### 3. API Gateway

#### Generic Description

An API Gateway is a server that acts as an entry point for all client requests to backend services. It handles request routing, composition, protocol translation, authentication, rate limiting, and provides a single endpoint for multiple microservices.

#### Cloud Products
- **AWS**:
  - Amazon API Gateway - Fully managed API service
  - AWS AppSync - GraphQL API service
  - Amazon API Gateway (REST, HTTP, WebSocket APIs)
- **Azure**:
  - Azure API Management (APIM) - Full API lifecycle management
  - Azure Application Gateway (with API features)
  - Azure Front Door (with API routing)

#### Data-Centric Example

**Incoming Request:**

```sh
Source IP: 203.0.113.75 (Mobile App Client)
Destination IP: 198.51.100.30 (API Gateway)
Method: POST
URI: /api/v1/orders
Protocol: HTTPS
Headers:
  Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
  Content-Type: application/json
  X-API-Key: ak_live_abc123xyz
  X-Client-ID: mobile-app-v2.1.0
Body:
{
  "customer_id": "cust_12345",
  "items": [{"product_id": "prod_789", "quantity": 2}],
  "total": 49.99
}
```

**API Gateway Processing:**

1. **Authentication Check:**
   - Validates API Key: ak_live_abc123xyz ✓
   - Verifies JWT token signature ✓
   - Checks token expiration ✓
   - Extracts user claims: user_id=12345, role=customer ✓

2. **Rate Limiting:**
   - Client: mobile-app-v2.1.0
   - Requests in last minute: 45/100 ✓
   - Remaining quota: 55 requests

3. **Request Transformation:**
   - Adds correlation ID: req_abc123
   - Enriches headers with user context
   - Validates request schema against OpenAPI spec ✓

4. **Routing Decision:**
   - Path: /api/v1/orders → Routes to Orders Service
   - Target: <http://orders-service.internal:8080/orders>

**Forwarded to Backend:**

```sh
Source IP: 10.0.2.50 (API Gateway Internal)
Destination IP: 10.0.3.25 (Orders Microservice)
Method: POST
URI: /orders
Headers:
  X-Correlation-ID: req_abc123
  X-User-ID: 12345
  X-User-Role: customer
  X-Original-IP: 203.0.113.75
  Content-Type: application/json
Body:
{
  "customer_id": "cust_12345",
  "items": [{"product_id": "prod_789", "quantity": 2}],
  "total": 49.99
}
```

**Backend Response:**

```sh
Status: 201 Created
Headers:
  Content-Type: application/json
  X-Service: orders-service
Body:
{
  "order_id": "ord_98765",
  "status": "pending",
  "created_at": "2025-10-29T14:32:15Z"
}
```

**API Gateway Response Transformation:**

```sh
Status: 201 Created
Headers:
  Content-Type: application/json
  X-Correlation-ID: req_abc123
  X-RateLimit-Remaining: 54
  X-RateLimit-Reset: 1698594795
Body:
{
  "order_id": "ord_98765",
  "status": "pending",
  "created_at": "2025-10-29T14:32:15Z",
  "_links": {
    "self": "/api/v1/orders/ord_98765",
    "payment": "/api/v1/orders/ord_98765/payment"
  }
}
```

#### Functional Requirements

**What It DOES:**
- Routes requests to appropriate backend services
- Authenticates and authorizes API requests
- Enforces rate limiting and throttling per client/API key
- Transforms requests and responses (protocol translation)
- Validates request/response schemas
- Aggregates responses from multiple services
- Provides API versioning support
- Logs and monitors API usage
- Caches responses to reduce backend load
- Handles CORS (Cross-Origin Resource Sharing)
- Generates API documentation (OpenAPI/Swagger)
- Manages API keys and tokens

**How It Works:**
- Receives client requests at a single endpoint
- Performs security checks (authentication, authorization)
- Applies policies (rate limits, quotas, transformations)
- Routes to backend services based on path, method, headers
- Can invoke multiple backends and aggregate results
- Applies response transformations before returning
- Maintains analytics and usage metrics

**What It Does NOT Do:**
- Does not host the actual business logic (only routes to it)
- Does not replace service-to-service authentication
- Does not provide data persistence or storage
- Does not execute long-running background jobs
- Does not provide load balancing at the TCP layer
- Does not inspect or filter network-layer packets
- Does not provide DDoS protection (needs WAF integration)
- Does not replace security groups or firewalls
- Does not guarantee message delivery (not a message queue)

---

### 4. NAT Gateway

#### Generic Description

A NAT (Network Address Translation) Gateway enables instances in a private subnet to connect to the internet or other AWS services while preventing the internet from initiating connections to those instances. It translates private IP addresses to public IP addresses for outbound traffic.

#### Cloud Products
- **AWS**:
  - NAT Gateway - Managed NAT service
  - NAT Instance - EC2-based NAT (legacy approach)
- **Azure**:
  - NAT Gateway - Managed outbound connectivity
  - Azure Firewall (can provide NAT functionality)
  - Public IP on Load Balancer (for outbound)

#### Data-Centric Example

**Outbound Request from Private Instance:**

```sh
Source IP: 10.0.1.15 (Private EC2 Instance)
Destination IP: 172.217.14.206 (google.com)
Source Port: 49152
Destination Port: 443 (HTTPS)
Protocol: TCP
Payload: TLS Client Hello - SNI: www.google.com
```

**NAT Gateway Processing:**

1. **Receives packet from private instance**
2. **Checks NAT translation table** (no existing entry)
3. **Creates new NAT mapping:**

   ```sh
   Internal: 10.0.1.15:49152
   External: 198.51.100.50:51234
   Protocol: TCP
   Destination: 172.217.14.206:443
   Timeout: 350 seconds (TCP established)
   ```

4. **Translates source address**
5. **Forwards to Internet Gateway**

**Packet Leaving NAT Gateway:**

```sh
Source IP: 198.51.100.50 (NAT Gateway Public IP)
Source Port: 51234 (Mapped port)
Destination IP: 172.217.14.206 (google.com)
Destination Port: 443
Protocol: TCP
Payload: TLS Client Hello - SNI: www.google.com
```

**Return Traffic from Internet:**

```sh
Source IP: 172.217.14.206 (google.com)
Destination IP: 198.51.100.50 (NAT Gateway Public IP)
Source Port: 443
Destination Port: 51234 (Mapped port)
Protocol: TCP
Payload: TLS Server Hello
```

**NAT Gateway Reverse Translation:**

1. **Looks up mapping table:**

   ```sh
   External: 198.51.100.50:51234 → Internal: 10.0.1.15:49152
   ```

2. **Translates destination address**
3. **Forwards to private subnet**

**Packet Delivered to Private Instance:**

```sh
Source IP: 172.217.14.206 (google.com)
Source Port: 443
Destination IP: 10.0.1.15 (Private Instance)
Destination Port: 49152
Protocol: TCP
Payload: TLS Server Hello
```

#### Functional Requirements

**What It DOES:**
- Translates private IPs to public IPs for outbound traffic
- Maintains NAT translation state table
- Allows private instances to access internet
- Provides multiple outbound public IPs for high bandwidth
- Supports TCP, UDP, and ICMP protocols
- Automatically scales to handle traffic volume
- Maintains connection state for return traffic
- Provides high availability within an AZ

**How It Works:**
- Uses Port Address Translation (PAT) / NAT Overload
- Maps internal IP:Port to external IP:Port
- Routes outbound traffic through Internet Gateway
- Tracks connection state for bidirectional communication
- Releases mappings after connection timeout
- Uses ephemeral port range (typically 1024-65535)

**What It Does NOT Do:**
- Does not allow inbound connections from internet
- Does not provide load balancing
- Does not filter traffic based on security rules
- Does not inspect packet contents
- Does not support VPN termination
- Does not work across multiple Availability Zones (single AZ)
- Does not provide DNS resolution
- Does not cache or optimize traffic
- Does not support protocol translation (e.g., IPv4 to IPv6)

---

### 5. VPN Gateway

#### Generic Description

A VPN (Virtual Private Network) Gateway creates an encrypted tunnel between on-premises networks and cloud networks, or between different cloud regions, enabling secure communication over the public internet.

#### Cloud Products
- **AWS**:
  - AWS Virtual Private Gateway (VGW) - For Site-to-Site VPN
  - AWS Client VPN - For remote user access
  - AWS Transit Gateway - Hub for multiple VPNs
- **Azure**:
  - Azure VPN Gateway - Site-to-Site and Point-to-Site VPN
  - Azure Virtual WAN - Global transit network
  - Azure VPN Gateway (Basic, VpnGw1-5 SKUs)

#### Data-Centric Example

**Original Packet from On-Premises:**

```sh
Source IP: 192.168.10.50 (On-Prem Server)
Destination IP: 10.0.1.25 (AWS Private Instance)
Source Port: 55443
Destination Port: 3306 (MySQL)
Protocol: TCP
Payload: MySQL Query - SELECT * FROM customers
```

**VPN Gateway Encapsulation (IPsec/ESP):**

1. **Encryption Phase:**
   - Encrypts original packet using AES-256
   - Adds ESP header with SPI (Security Parameter Index)

2. **Encapsulation:**

```sh
Outer IP Header:
  Source IP: 203.0.113.10 (On-Prem VPN Device Public IP)
  Destination IP: 198.51.100.100 (AWS VPN Gateway Public IP)
  Protocol: ESP (50)

ESP Header:
  SPI: 0x12345678 (Security Association ID)
  Sequence Number: 98765

Encrypted Payload:
  [Original packet encrypted with AES-256-GCM]
  Original: 192.168.10.50:55443 → 10.0.1.25:3306
  TCP + MySQL Query (encrypted)

ESP Trailer:
  Padding: [if needed]
  Pad Length: 0
  Next Header: 4 (IP in IP)

ESP Authentication Data:
  HMAC-SHA256 digest
```

**Transit over Internet:**
- Packet travels through public internet
- Encrypted payload prevents inspection
- Only outer headers visible to internet routers

**VPN Gateway Decapsulation:**

1. **Receives ESP packet**
2. **Validates ESP authentication**
3. **Looks up Security Association (SPI: 0x12345678)**
4. **Decrypts payload using shared keys**
5. **Extracts original packet**
6. **Routes to private subnet**

**Decrypted Packet Delivered:**

```sh
Source IP: 192.168.10.50 (On-Prem Server)
Destination IP: 10.0.1.25 (AWS Private Instance)
Source Port: 55443
Destination Port: 3306
Protocol: TCP
Payload: MySQL Query - SELECT * FROM customers
```

**Return Path (AWS to On-Prem):**

```sh
1. Response: 10.0.1.25:3306 → 192.168.10.50:55443
2. VPN Gateway encrypts and encapsulates
3. Sends via ESP: 198.51.100.100 → 203.0.113.10
4. On-Prem VPN device decrypts
5. Delivers to 192.168.10.50
```

#### Functional Requirements

**What It DOES:**
- Creates encrypted IPsec tunnels between networks
- Authenticates both tunnel endpoints
- Encrypts all traffic traversing the tunnel
- Supports multiple encryption algorithms (AES-128, AES-256)
- Maintains tunnel state and handles rekeying
- Provides route propagation to subnets
- Supports Border Gateway Protocol (BGP) for dynamic routing
- Handles both site-to-site and point-to-site connections
- Provides redundancy with multiple tunnels
- Monitors tunnel health and status

**How It Works:**
- Uses IKE (Internet Key Exchange) for tunnel establishment
- Phase 1: Establishes secure channel (ISAKMP SA)
- Phase 2: Negotiates IPsec parameters (IPsec SA)
- Encapsulates packets in ESP (Encapsulating Security Payload)
- Encrypts payload and adds authentication
- Routes packets through tunnel based on destination
- Maintains Security Association Database (SAD)

**What It Does NOT Do:**
- Does not provide load balancing across tunnels by default
- Does not inspect or filter decrypted traffic (needs firewall)
- Does not guarantee bandwidth or QoS
- Does not translate between IPv4 and IPv6
- Does not cache or optimize application data
- Does not provide application-layer authentication
- Does not protect against attacks on decrypted traffic
- Does not provide multi-region connectivity directly (needs transit gateway)
- Does not support all protocols (some require special handling)

---

### 6. Web Application Firewall (WAF)

#### Generic Description

A Web Application Firewall inspects HTTP/HTTPS traffic to detect and block common web attacks such as SQL injection, cross-site scripting (XSS), and other OWASP Top 10 vulnerabilities. It operates at Layer 7 (application layer).

#### Cloud Products
- **AWS**:
  - AWS WAF - Managed web application firewall
  - AWS Shield Advanced (includes WAF features)
  - AWS Managed Rules for WAF
- **Azure**:
  - Azure Web Application Firewall (on Application Gateway)
  - Azure Front Door WAF
  - Azure Firewall (with premium features)

#### Data-Centric Example

**Malicious HTTP Request (SQL Injection Attempt):**

```sh
Method: POST
URI: /api/login
Source IP: 198.51.100.85
Headers:
  Host: webapp.example.com
  Content-Type: application/x-www-form-urlencoded
  User-Agent: Mozilla/5.0...
  Cookie: session=abc123xyz

Body:
username=admin' OR '1'='1&password=' OR '1'='1
```

**WAF Processing:**

1. **Request Inspection:**

   ```sh
   Request ID: req_waf_98765
   Size: 245 bytes
   Method: POST
   Path: /api/login
   ```

2. **Rule Evaluation:**

   **Rule 1 - SQL Injection Pattern Match:**

   ```sh
   Pattern: (?i)(union|select|insert|update|delete|drop).*from
   Match: No
   
   Pattern: (?i)(\w+)\s*'\s*or\s*'1'\s*=\s*'1
   Match: YES ✓
   Location: Body parameter 'username'
   Matched Text: "admin' OR '1'='1"
   Severity: HIGH
   Action: BLOCK
   ```

   **Rule 2 - Multiple SQL Keywords:**

   ```sh
   Pattern: Multiple SQL keywords in single request
   Match: YES ✓
   Keywords found: OR (2 occurrences)
   Severity: MEDIUM
   ```

3. **Action Taken:**

   ```sh
   Decision: BLOCK
   Response Code: 403 Forbidden
   Log Entry Created:
     Timestamp: 2025-10-29T14:35:20Z
     Rule ID: SQLi-001
     Source IP: 198.51.100.85
     URI: /api/login
     Matched Pattern: SQL Injection
     Action: BLOCKED
   ```

**WAF Response to Client:**

```sh
HTTP/1.1 403 Forbidden
Content-Type: application/json
X-WAF-Request-ID: req_waf_98765

{
  "error": "Request blocked by security policy",
  "request_id": "req_waf_98765"
}
```

**Legitimate Request Example:**

```sh
Method: POST
URI: /api/login
Body:
username=john.doe@example.com&password=SecureP@ss123!

WAF Processing:
- SQL Injection Check: PASS ✓
- XSS Pattern Check: PASS ✓
- Size Limit Check: PASS ✓
- Rate Limiting: 5/100 requests ✓
- Geo-blocking: US (Allowed) ✓

Action: ALLOW
Forwarded to Application Server
```

**XSS Attack Example:**

```sh
Method: GET
URI: /search?q=<script>alert('XSS')</script>
Headers:
  Host: webapp.example.com

WAF Processing:
- XSS Pattern Match: DETECTED
  Pattern: <script[^>]*>.*</script>
  Location: Query parameter 'q'
  Action: BLOCK
  
Response: 403 Forbidden
```

#### Functional Requirements

**What It DOES:**
- Inspects HTTP/HTTPS requests and responses
- Detects and blocks OWASP Top 10 attacks
- Protects against SQL injection attacks
- Prevents cross-site scripting (XSS)
- Blocks cross-site request forgery (CSRF)
- Filters based on IP addresses, geo-location, headers
- Rate limits requests per IP or session
- Validates request size and content
- Protects against HTTP protocol violations
- Detects bot traffic and scraping attempts
- Uses signatures and behavioral analysis
- Logs all blocked and allowed requests
- Supports custom rules and managed rule sets

**How It Works:**
- Sits in front of web applications (reverse proxy mode)
- Inspects full HTTP request (method, URI, headers, body)
- Evaluates against ordered rule sets
- Uses pattern matching (regex) for attack signatures
- Employs anomaly scoring for suspicious patterns
- Can operate in detection mode (log only) or block mode
- Integrates with CDN and load balancers
- Updates rules dynamically for new threats

**What It Does NOT Do:**
- Does not protect against DDoS volumetric attacks (needs DDoS protection)
- Does not inspect encrypted traffic without SSL termination
- Does not prevent zero-day application vulnerabilities
- Does not replace secure coding practices
- Does not provide authentication or authorization
- Does not protect network-layer attacks (needs network firewall)
- Does not scan for malware in uploaded files (needs separate scanner)
- Does not prevent insider threats or privileged access abuse
- Does not guarantee 100% protection (false positives/negatives)
- Does not protect APIs without proper configuration
- Does not inspect WebSocket traffic after upgrade

---

### 7. Content Delivery Network (CDN)

#### Generic Description

A CDN is a geographically distributed network of servers that cache and deliver content to users from the nearest edge location, reducing latency and improving performance.

#### Cloud Products
- **AWS**:
  - Amazon CloudFront - Global CDN service
  - CloudFront Functions - Lightweight edge compute
  - Lambda@Edge - Full Lambda at edge locations
- **Azure**:
  - Azure Content Delivery Network (CDN)
  - Azure Front Door - CDN with WAF and load balancing
  - Azure CDN from Microsoft/Verizon/Akamai

#### Data-Centric Example

**First Request (Cache Miss):**

**Client Request:**

```sh
Method: GET
URI: /images/logo.png
Source IP: 203.0.113.99 (User in Tokyo)
Destination: cdn.example.com
Headers:
  Host: cdn.example.com
  User-Agent: Mozilla/5.0...
  Accept: image/png
  Accept-Encoding: gzip, br
```

**CDN Edge Location (Tokyo):**

```sh
1. DNS Resolution:
   cdn.example.com → 13.35.24.15 (Tokyo Edge)

2. Request Received at Edge

3. Cache Lookup:
   Key: /images/logo.png
   Result: MISS (not in cache)
   
4. Forward to Origin:
   Origin: origin.example.com (us-east-1)
   Headers Added:
     X-Forwarded-For: 203.0.113.99
     X-Edge-Location: Tokyo
```

**Request to Origin Server:**

```sh
Method: GET
URI: /images/logo.png
Source IP: 54.239.130.15 (CloudFront IP)
Destination: 192.0.2.50 (Origin Server)
Headers:
  Host: origin.example.com
  X-Forwarded-For: 203.0.113.99
  X-Edge-Location: Tokyo
  Via: 1.1 CloudFront
```

**Origin Response:**

```sh
Status: 200 OK
Headers:
  Content-Type: image/png
  Content-Length: 45623
  Cache-Control: public, max-age=86400
  ETag: "abc123xyz"
  Last-Modified: Mon, 28 Oct 2025 10:00:00 GMT

Body: [PNG image binary data - 45,623 bytes]
```

**CDN Edge Caching:**

```sh
1. Receives response from origin
2. Stores in edge cache:
   Cache Key: /images/logo.png
   Object: [PNG data]
   TTL: 86400 seconds (24 hours)
   Size: 45,623 bytes
   Headers: [all cacheable headers]
   
3. Serves to client
4. Cache Status: MISS (first request)
```

**Response to Client:**

```sh
Status: 200 OK
Headers:
  Content-Type: image/png
  Content-Length: 45623
  Cache-Control: public, max-age=86400
  X-Cache: Miss from cloudfront
  X-Edge-Location: Tokyo
  Age: 0

Body: [PNG image binary data]
```

**Second Request (Cache Hit):**

**Another Client Request (10 minutes later):**

```sh
Method: GET
URI: /images/logo.png
Source IP: 203.0.114.25 (Another user in Tokyo)
Destination: cdn.example.com
```

**CDN Edge Location Processing:**

```sh
1. Request received at Tokyo Edge

2. Cache Lookup:
   Key: /images/logo.png
   Result: HIT ✓
   Age: 600 seconds (10 minutes)
   TTL Remaining: 85800 seconds
   
3. Validation:
   If-Modified-Since: Not present in request
   ETag Match: N/A
   Cache still valid: YES

4. Serve from cache (no origin request)
```

**Response to Client:**

```sh
Status: 200 OK
Headers:
  Content-Type: image/png
  Content-Length: 45623
  Cache-Control: public, max-age=86400
  X-Cache: Hit from cloudfront
  X-Edge-Location: Tokyo
  Age: 600 (10 minutes old)
  
Body: [PNG from edge cache - no origin fetch]

Response Time: 5ms (vs 250ms from origin)
```

**Conditional Request (Cache Revalidation):**

```sh
Client Request (25 hours later):
GET /images/logo.png
If-None-Match: "abc123xyz"
If-Modified-Since: Mon, 28 Oct 2025 10:00:00 GMT

CDN Processing:
1. Cache entry expired (TTL exceeded)
2. Forwards conditional request to origin
3. Origin checks If-None-Match
4. File unchanged: Returns 304 Not Modified
5. CDN refreshes TTL
6. Returns cached object to client with new TTL

Response: 304 Not Modified
X-Cache: Revalidated from cloudfront
```

#### Functional Requirements

**What It DOES:**
- Caches static content (images, CSS, JS, videos)
- Serves content from geographically distributed edge locations
- Reduces latency by serving from nearest location
- Offloads traffic from origin servers
- Supports cache invalidation and purging
- Compresses content (gzip, Brotli)
- Terminates SSL/TLS at the edge
- Respects Cache-Control headers
- Performs conditional GET requests (If-Modified-Since)
- Handles HTTP/2 and HTTP/3 protocols
- Provides analytics on cache hit rates
- Supports multiple origins and origin failover
- Executes edge compute functions

**How It Works:**
- User requests content via CDN domain
- DNS resolves to nearest edge location
- Edge checks local cache for requested object
- On cache miss, fetches from origin server
- Stores object in edge cache per TTL
- Serves subsequent requests from cache
- Revalidates expired content with origin
- Uses Anycast routing for optimal path

**What It Does NOT Do:**
- Does not cache dynamic/personalized content by default
- Does not execute full backend application logic
- Does not provide database storage
- Does not authenticate users (without edge functions)
- Does not perform complex business logic
- Does not inspect or filter malicious traffic (needs WAF)
- Does not guarantee real-time content updates
- Does not replace origin server infrastructure
- Does not provide session state management
- Does not handle POST/PUT requests the same as GET
- Does not work well for live streaming without specific config

---

### 8. DNS (Domain Name System)

#### Generic Description

DNS translates human-readable domain names into IP addresses, enabling users to access resources using memorable names instead of numeric IP addresses. It operates as a hierarchical distributed database.

#### Cloud Products
- **AWS**:
  - Amazon Route 53 - Scalable DNS and domain registration
  - Route 53 Resolver - Hybrid DNS resolution
  - Route 53 Application Recovery Controller
- **Azure**:
  - Azure DNS - DNS hosting service
  - Azure Private DNS - DNS for virtual networks
  - Azure Traffic Manager - DNS-based load balancing

#### Data-Centric Example

**DNS Query Process:**

**Client DNS Query:**

```sh
Query Type: A (IPv4 address lookup)
Domain: www.example.com
Protocol: UDP
Source IP: 192.168.1.100 (Client)
Source Port: 54321
Destination IP: 8.8.8.8 (Google DNS - Recursive Resolver)
Destination Port: 53

DNS Packet:
Transaction ID: 0x1a2b
Flags: Standard query
Questions: 1
  - Name: www.example.com
  - Type: A (1)
  - Class: IN (Internet)
Answer RRs: 0
Authority RRs: 0
Additional RRs: 0
```

**Recursive Resolver Processing:**

**Step 1 - Check Cache:**

```sh
Lookup: www.example.com in cache
Result: MISS (not cached or expired)
Next Action: Perform iterative queries
```

**Step 2 - Query Root Name Server:**

```sh
Query to: 198.41.0.4 (a.root-servers.net)
Question: www.example.com A record

Response:
Transaction ID: 0x1a2b
Flags: Response, No error
Answers: 0
Authority Records: 13
  - com. NS a.gtld-servers.net (192.5.6.30)
  - com. NS b.gtld-servers.net
  ... [referral to .com TLD servers]
Glue Records: A records for TLD servers

Action: Referred to .com TLD servers
```

**Step 3 - Query TLD Server:**

```sh
Query to: 192.5.6.30 (a.gtld-servers.net)
Question: www.example.com A record

Response:
Transaction ID: 0x1a2b
Flags: Response, No error
Answers: 0
Authority Records: 2
  - example.com. NS ns1.example.com (198.51.100.1)
  - example.com. NS ns2.example.com (198.51.100.2)
Glue Records:
  - ns1.example.com A 198.51.100.1
  - ns2.example.com A 198.51.100.2

Action: Referred to authoritative servers for example.com
```

**Step 4 - Query Authoritative Server:**

```sh
Query to: 198.51.100.1 (ns1.example.com)
Question: www.example.com A record

Response:
Transaction ID: 0x1a2b
Flags: Authoritative Answer, No error
Questions: 1
Answers: 1
  - www.example.com. 300 IN A 203.0.113.50

Authority Records: 2
  - example.com. NS ns1.example.com
  - example.com. NS ns2.example.com

Additional Records: 2
  - ns1.example.com A 198.51.100.1
  - ns2.example.com A 198.51.100.2
```

**Step 5 - Resolver Caches and Returns:**

```sh
Cache Entry Created:
  - Name: www.example.com
  - Type: A
  - Value: 203.0.113.50
  - TTL: 300 seconds (5 minutes)
  - Timestamp: 2025-10-29T14:40:00Z
```

**Final Response to Client:**

```sh
Protocol: UDP
Source IP: 8.8.8.8 (Google DNS)
Source Port: 53
Destination IP: 192.168.1.100
Destination Port: 54321

DNS Packet:
Transaction ID: 0x1a2b
Flags: Response, Recursion Available, No error
Questions: 1
Answers: 1
  - www.example.com. 300 IN A 203.0.113.50
Authority RRs: 0
Additional RRs: 0

Total Resolution Time: 45ms
```

**Advanced Routing Example (Latency-Based):**

**Route 53 Latency-Based Routing:**

```sh
Client Location: Tokyo, Japan
Query: api.example.com

Route 53 Processing:
1. Receives query from Tokyo
2. Evaluates latency-based routing policy
3. Checks configured regions:
   - us-east-1: Latency ~180ms
   - eu-west-1: Latency ~250ms
   - ap-northeast-1: Latency ~5ms ✓ (Closest)
4. Returns IP for Asia-Pacific region

Response:
api.example.com. 60 IN A 13.112.168.25 (Tokyo region)

Second Client Location: London, UK
Same Query: api.example.com

Route 53 Processing:
1. Receives query from London
2. Checks latency from London:
   - us-east-1: Latency ~80ms
   - eu-west-1: Latency ~10ms ✓ (Closest)
   - ap-northeast-1: Latency ~220ms
3. Returns IP for Europe region

Response:
api.example.com. 60 IN A 18.202.216.50 (London region)
```

**Health Check Example:**

```sh
Route 53 Health Check Configuration:
Endpoint: 203.0.113.50:443
Protocol: HTTPS
Path: /health
Interval: 30 seconds
Failure Threshold: 3

Health Check Result:
Status: HEALTHY
Last Check: 2025-10-29T14:40:15Z
Response Time: 45ms
Status Code: 200

If Health Check Fails:
1. Mark endpoint as unhealthy
2. Stop returning this IP in DNS responses
3. Failover to backup endpoint: 203.0.113.51
```

#### Functional Requirements

**What It DOES:**
- Resolves domain names to IP addresses
- Supports multiple record types (A, AAAA, CNAME, MX, TXT, etc.)
- Provides hierarchical domain name resolution
- Caches responses to reduce query load
- Implements TTL (Time To Live) for cache expiration
- Supports recursive and iterative queries
- Provides routing policies (latency, geolocation, weighted)
- Performs health checks on endpoints
- Enables traffic management and failover
- Supports DNSSEC for security
- Manages domain registration

**How It Works:**
- Client queries local DNS resolver
- Resolver queries root, TLD, and authoritative servers
- Authoritative server returns answer
- Resolver caches result and returns to client
- Uses UDP port 53 (TCP for large responses)
- Follows delegation chain from root to domain

**What It Does NOT Do:**
- Does not encrypt queries by default (needs DNS over HTTPS/TLS)
- Does not provide content delivery or caching beyond IP resolution
- Does not inspect or filter traffic
- Does not authenticate users
- Does not guarantee data privacy (queries are visible)
- Does not provide load balancing at connection level
- Does not execute application logic
- Does not store application data
- Does not provide real-time updates (TTL dependent)
- Does not protect against DDoS directly

---

### 9. Internet Gateway

#### Generic Description

An Internet Gateway is a horizontally scaled, redundant VPC component that allows communication between instances in a VPC and the internet. It provides a target for internet-routable traffic and performs NAT for instances with public IP addresses.

#### Cloud Products
- **AWS**:
  - Internet Gateway (IGW) - VPC component
  - Egress-Only Internet Gateway - IPv6 outbound only
- **Azure**:
  - Virtual Network - Implicit internet connectivity
  - Public IP addresses - Attached to resources
  - Azure NAT Gateway (for outbound)

#### Data-Centric Example

**Outbound Traffic (Instance to Internet):**

**Instance with Public IP:**

```sh
EC2 Instance:
Private IP: 10.0.1.20
Public IP: 198.51.100.75 (Elastic IP associated)
```

**Packet from Instance:**

```sh
Source IP: 10.0.1.20 (Private IP)
Destination IP: 172.217.14.206 (google.com)
Source Port: 49152
Destination Port: 443
Protocol: TCP
Payload: HTTPS request
```

**Internet Gateway Processing (Outbound):**

1. **Route Table Lookup:**

   ```sh
   Destination: 172.217.14.206
   Matches Route: 0.0.0.0/0 → Internet Gateway
   ```

2. **NAT Translation:**

   ```sh
   Before IGW:
   Source: 10.0.1.20:49152 → Dest: 172.217.14.206:443
   
   IGW Translation:
   - Looks up instance's public IP mapping
   - Instance 10.0.1.20 → Public IP 198.51.100.75
   - Translates source address
   
   After IGW:
   Source: 198.51.100.75:49152 → Dest: 172.217.14.206:443
   ```

3. **Forwards to Internet:**

   ```sh
   Packet exits AWS network with public source IP
   ```

**Packet on Internet:**

```sh
Source IP: 198.51.100.75 (Public Elastic IP)
Destination IP: 172.217.14.206
Source Port: 49152
Destination Port: 443
Protocol: TCP
Payload: HTTPS request
```

**Inbound Traffic (Internet to Instance):**

**Packet from Internet:**

```sh
Source IP: 172.217.14.206 (google.com)
Destination IP: 198.51.100.75 (Public Elastic IP)
Source Port: 443
Destination Port: 49152
Protocol: TCP
Payload: HTTPS response
```

**Internet Gateway Processing (Inbound):**

1. **Receives packet at public IP**
2. **Reverse NAT Lookup:**

   ```sh
   Public IP: 198.51.100.75
   Maps to: Instance i-1234567890 at 10.0.1.20
   ```

3. **Address Translation:**

   ```sh
   Before Translation:
   Source: 172.217.14.206:443 → Dest: 198.51.100.75:49152
   
   After Translation:
   Source: 172.217.14.206:443 → Dest: 10.0.1.20:49152
   ```

4. **Security Group Check:**

   ```sh
   Instance Security Group: sg-abc123
   Rule: Allow inbound TCP 49152 from established connections ✓
   Action: ALLOW (stateful - part of established connection)
   ```

5. **Delivers to subnet**

**Packet Delivered to Instance:**

```sh
Source IP: 172.217.14.206
Destination IP: 10.0.1.20 (Private IP)
Source Port: 443
Destination Port: 49152
Protocol: TCP
Payload: HTTPS response
```

**New Inbound Connection Attempt:**

```sh
External Source: 203.0.113.100
Destination: 198.51.100.75:22 (SSH)

Internet Gateway:
1. Translates to private IP: 10.0.1.20
2. Forwards to VPC

Security Group Check:
Rule: Allow TCP 22 from 203.0.113.0/24 ✓
Action: ALLOW

Route Table:
Destination: 10.0.1.20
Subnet: 10.0.1.0/24
Action: Deliver to instance
```

#### Functional Requirements

**What It DOES:**
- Provides internet connectivity for VPC resources
- Performs 1:1 NAT for instances with public IPs
- Routes traffic between VPC and internet
- Maintains mapping between private and public IPs
- Scales automatically (horizontally scaled)
- Provides high availability (redundant)
- Supports both IPv4 and IPv6
- Works with Elastic IPs and auto-assigned public IPs
- Integrates with route tables

**How It Works:**
- Attached to VPC (one per VPC)
- Listed as target in route table for 0.0.0.0/0
- Performs bidirectional NAT for public IPs
- Stateless operation (relies on route tables)
- No bandwidth constraints or availability risks
- Managed service (no configuration needed)

**What It Does NOT Do:**
- Does not provide NAT for instances without public IPs (use NAT Gateway)
- Does not filter or inspect traffic (needs security groups/NACLs)
- Does not perform port address translation (PAT)
- Does not provide VPN functionality
- Does not cache or optimize traffic
- Does not provide DNS resolution
- Does not balance load
- Does not authenticate connections
- Does not limit bandwidth per instance
- Does not work with private subnets (needs NAT Gateway)

---

### 10. Transit Gateway

#### Generic Description

A Transit Gateway acts as a network transit hub that connects VPCs, on-premises networks, and other transit gateways. It simplifies network architecture by eliminating complex peering relationships.

#### Cloud Products
- **AWS**:
  - AWS Transit Gateway - Regional network hub
  - Transit Gateway Network Manager - Global network management
- **Azure**:
  - Azure Virtual WAN - Global transit network
  - Azure Virtual Network Gateway (VPN/ExpressRoute)
  - Azure Route Server

#### Data-Centric Example

**Hub-and-Spoke Topology:**

```sh
Network Setup:
- Transit Gateway: tgw-123456
- VPC A: 10.1.0.0/16 (Production)
- VPC B: 10.2.0.0/16 (Development)
- VPC C: 10.3.0.0/16 (Shared Services)
- On-Premises: 192.168.0.0/16 (via VPN)
```

**Traffic from VPC A to VPC B:**

**Original Packet:**

```sh
Source IP: 10.1.5.20 (Instance in VPC A)
Destination IP: 10.2.8.15 (Instance in VPC B)
Source Port: 55123
Destination Port: 443
Protocol: TCP
Payload: API request
```

**VPC A Route Table:**

```sh
Destination: 10.2.0.0/16
Target: Transit Gateway (tgw-123456)
Attachment: tgw-attach-vpcA
```

**Transit Gateway Processing:**

1. **Receives from VPC A attachment**

   ```sh
   Ingress Attachment: tgw-attach-vpcA
   Source: 10.1.5.20
   Destination: 10.2.8.15
   ```

2. **Route Table Lookup:**

   ```sh
   Transit Gateway Route Table: tgw-rtb-main
   
   Routes:
   - 10.1.0.0/16 → tgw-attach-vpcA
   - 10.2.0.0/16 → tgw-attach-vpcB ✓
   - 10.3.0.0/16 → tgw-attach-vpcC
   - 192.168.0.0/16 → tgw-attach-vpn
   
   Match: 10.2.0.0/16 routes to tgw-attach-vpcB
   ```

3. **Forwards to VPC B attachment**

   ```sh
   Egress Attachment: tgw-attach-vpcB
   No address translation (maintains source/dest IPs)
   ```

**Packet Arrives at VPC B:**

```sh
Source IP: 10.1.5.20 (VPC A instance)
Destination IP: 10.2.8.15 (VPC B instance)
Source Port: 55123
Destination Port: 443
Protocol: TCP
Payload: API request

VPC B Route Table:
Destination: 10.2.8.15
Local delivery to subnet
```

**Advanced Routing - Segmentation:**

**Isolated Route Table Configuration:**

```sh
Production Route Table (tgw-rtb-prod):
Attachments: VPC A (Production)
Routes:
- 10.3.0.0/16 → tgw-attach-vpcC (Shared Services) ✓
- 192.168.0.0/16 → tgw-attach-vpn (On-Prem) ✓
- 10.2.0.0/16 → Blackhole (Block Dev access)

Development Route Table (tgw-rtb-dev):
Attachments: VPC B (Development)
Routes:
- 10.3.0.0/16 → tgw-attach-vpcC (Shared Services) ✓
- 10.1.0.0/16 → Blackhole (Block Prod access)
- 192.168.0.0/16 → Blackhole (Block On-Prem)
```

**Blocked Traffic Example:**

```sh
Source: 10.2.5.30 (Dev VPC)
Destination: 10.1.5.20 (Prod VPC)

Transit Gateway Processing:
1. Receives from tgw-attach-vpcB
2. Looks up in tgw-rtb-dev
3. Route: 10.1.0.0/16 → Blackhole
4. Action: DROP packet
5. No response sent (blackhole)

Result: Traffic blocked, enforcing network segmentation
```

**On-Premises to VPC Traffic:**

**Packet from On-Prem Network:**

```sh
Source IP: 192.168.50.100 (On-Prem Server)
Destination IP: 10.3.10.25 (Shared Services VPC)
Protocol: TCP
Port: 389 (LDAP)
```

**VPN Connection to Transit Gateway:**

```sh
Arrives via: VPN Attachment (tgw-attach-vpn)
BGP Learned Route: 192.168.0.0/16

Transit Gateway Processing:
1. Receives from VPN attachment
2. Route lookup in appropriate table
3. Route: 10.3.0.0/16 → tgw-attach-vpcC
4. Forwards to VPC C attachment
```

**Delivered to Shared Services VPC:**

```sh
Source IP: 192.168.50.100 (maintained)
Destination IP: 10.3.10.25
Route Table: Local delivery
Security Group: Allow TCP 389 from 192.168.0.0/16
Result: Delivered to LDAP server
```

**Return Traffic:**

```sh
Source: 10.3.10.25
Destination: 192.168.50.100

Path:
1. VPC C route: 192.168.0.0/16 → tgw-123456
2. TGW routes to tgw-attach-vpn
3. Encrypted via IPsec tunnel
4. Delivered to on-premises
```

#### Functional Requirements

**What It DOES:**
- Connects multiple VPCs within and across regions
- Connects VPCs to on-premises networks via VPN/Direct Connect
- Routes traffic between attached networks
- Supports multiple route tables for network segmentation
- Enables transitive routing between networks
- Integrates with VPN and Direct Connect
- Supports BGP for dynamic routing
- Provides centralized routing management
- Scales to thousands of VPCs
- Supports multicast (in some configurations)
- Enables inter-region peering
- Provides network monitoring and flow logs

**How It Works:**
- Networks attach via attachments (VPC, VPN, Direct Connect)
- Each attachment associates with a route table
- Route tables contain CIDR routes to other attachments
- Inspects destination IP and routes to appropriate attachment
- Does not modify packet headers (except for encapsulation)
- Uses BGP to learn and advertise routes
- Supports route propagation from attachments

**What It Does NOT Do:**
- Does not perform NAT (maintains source/destination IPs)
- Does not inspect or filter traffic (needs firewall)
- Does not provide encryption (except via VPN attachments)
- Does not load balance across multiple paths
- Does not cache or optimize application traffic
- Does not resolve DNS queries
- Does not authenticate connections
- Does not guarantee bandwidth per attachment
- Does not support overlapping CIDR blocks
- Does not provide application-layer routing
- Does not replace security groups or NACLs

---

### 11. DDoS Protection Service

#### Generic Description

A DDoS (Distributed Denial of Service) Protection service detects and mitigates volumetric, protocol, and application-layer attacks by absorbing and filtering malicious traffic before it reaches protected resources.

#### Cloud Products
- **AWS**:
  - AWS Shield Standard - Automatic DDoS protection
  - AWS Shield Advanced - Enhanced DDoS protection with 24/7 response
  - AWS WAF (for Layer 7 DDoS)
- **Azure**:
  - Azure DDoS Protection Basic - Automatic protection
  - Azure DDoS Protection Standard - Enhanced protection
  - DDoS Rapid Response Team

#### Data-Centric Example

**Normal Traffic Baseline:**

```sh
Normal Traffic Pattern:
- Average: 10,000 requests/second
- Peak: 15,000 requests/second
- Geographic Distribution: 60% US, 30% EU, 10% Asia
- User Agents: Diverse (Chrome, Safari, Firefox, Mobile)
- Connection Rate: 500 new connections/second
```

**DDoS Attack - SYN Flood:**

**Attack Traffic:**

```sh
Malicious SYN Packets:
Count: 500,000 packets/second
Source IPs: 50,000+ unique IPs (botnet)
Destination: 198.51.100.50:443

Sample Packet:
Source IP: 185.220.101.75 (Botnet node)
Destination IP: 198.51.100.50
Source Port: 32451 (Random)
Destination Port: 443
TCP Flags: SYN
Sequence Number: Random
Window Size: 8192
Payload: None

Characteristics:
- Random source IPs (spoofed)
- Incomplete TCP handshake (no ACK)
- High packet rate from single sources
- No legitimate payload
```

**DDoS Protection Detection:**

1. **Traffic Analysis:**

   ```sh
   Metric: SYN packets/second
   Baseline: 500/sec
   Current: 500,000/sec
   Deviation: 1000x increase ⚠️
   
   Metric: Half-open connections
   Baseline: 200
   Current: 450,000
   Deviation: 2250x increase ⚠️
   
   Metric: Connection completion rate
   Baseline: 98%
   Current: 2%
   Deviation: Critical ⚠️
   ```

2. **Attack Classification:**

   ```sh
   Attack Type: SYN Flood (Layer 4)
   Severity: HIGH
   Confidence: 99%
   Attack Vector: TCP Protocol Violation
   ```

3. **Mitigation Activated:**

   ```sh
   Timestamp: 2025-10-29T14:45:00Z
   Mitigation: Automatic (within 60 seconds)
   Method: SYN Proxy + Rate Limiting
   ```

**Mitigation in Action:**

**SYN Proxy Implementation:**

```sh
Legitimate Client Packet:
Source: 203.0.113.45
Dest: 198.51.100.50:443
Flags: SYN
Seq: 1000

Shield Processing:
1. Intercepts SYN packet
2. Sends SYN-ACK to client (challenge)
3. Client responds with ACK (proves legitimacy)
4. Shield establishes connection to backend
5. Bridges connections together

Malicious Packet:
Source: 185.220.101.75 (Spoofed)
Dest: 198.51.100.50:443
Flags: SYN
Seq: Random

Shield Processing:
1. Intercepts SYN packet
2. Sends SYN-ACK to source IP
3. No ACK received (spoofed IP can't respond)
4. Connection dropped
5. Source IP not forwarded to backend
```

**Rate Limiting Rules:**

```sh
Applied Rules:
1. Limit connections per source IP: 10/second
2. Limit total SYN rate: 50,000/second
3. Prioritize established connections
4. Challenge suspicious sources with CAPTCHA (Layer 7)

Results:
- Malicious traffic: Dropped before reaching origin
- Legitimate users: Slight delay for challenge
- Backend servers: Protected from overwhelming connections
```

**HTTP Flood Attack (Layer 7):**

**Attack Pattern:**

```sh
Request Rate: 100,000 requests/second
Source IPs: 10,000+ unique IPs
Characteristics:
- Valid HTTP requests
- Random User-Agents (mimics legitimate browsers)
- Distributed across many IPs (hard to block)
- Targets expensive API endpoints

Sample Attack Request:
GET /api/search?q=expensive-query&limit=10000 HTTP/1.1
Host: api.example.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)...
Accept: application/json

Behavior:
- Each request is valid HTTP
- Requests cause expensive database queries
- High CPU/memory consumption on backend
- Cannot be filtered by simple rate limiting
```

**WAF + Shield Advanced Mitigation:**

```sh
Detection:
1. Behavioral Analysis:
   - Request rate per IP: 100/second (abnormal)
   - Geographic distribution: 95% from 3 data centers
   - User-Agent variety: Low (only 50 unique)
   - Request pattern: Identical query parameters
   - Session behavior: No normal browsing patterns

2. Anomaly Scoring:
   Score: 85/100 (Attack likely)
   Confidence: 95%

Mitigation:
1. Rate limit per IP: 10 req/sec
2. CAPTCHA challenge for suspicious IPs
3. Block known bot signatures
4. Cache expensive queries (reduce backend load)
5. Throttle search endpoint globally

Rules Applied:
- Source IP 185.220.101.75: CHALLENGE (CAPTCHA)
- User-Agent "Mozilla/5.0 (Linux; Bot)": BLOCK
- Query "expensive-query": RATE_LIMIT (1/sec/IP)
- Geographic anomaly (data center IPs): CHALLENGE
```

**Legitimate Traffic Handling:**

```sh
Legitimate User Request:
Source: 203.0.113.50
Rate: 2 requests/second
Pattern: Normal browsing
Session: Valid cookie

Processing:
1. Traffic profiling: LEGITIMATE ✓
2. No challenges applied
3. Forwarded to backend immediately
4. No impact on user experience

Attack Traffic:
Source: 185.220.101.75
Rate: 100 requests/second
Pattern: Repetitive queries
Session: None

Processing:
1. Traffic profiling: SUSPICIOUS ⚠️
2. CAPTCHA challenge presented
3. Bot fails challenge
4. Traffic blocked
5. Backend protected
```

#### Functional Requirements

**What It DOES:**
- Detects volumetric, protocol, and application-layer attacks
- Automatically mitigates attacks in real-time
- Uses machine learning for anomaly detection
- Implements SYN proxy for SYN flood protection
- Applies rate limiting per source IP or globally
- Filters malicious traffic before reaching origin
- Provides always-on monitoring
- Offers 24/7 DDoS response team (advanced tiers)
- Protects against reflection/amplification attacks
- Handles UDP floods, ICMP floods
- Provides post-attack forensics and reports
- Integrates with WAF for Layer 7 protection

**How It Works:**
- Monitors traffic patterns and establishes baselines
- Detects anomalies through statistical analysis
- Classifies attack types automatically
- Redirects traffic through scrubbing centers
- Filters malicious packets while allowing legitimate traffic
- Uses rate limiting, geo-blocking, and challenges
- Scales capacity automatically during attacks
- Returns clean traffic to origin infrastructure

**What It Does NOT Do:**
- Does not prevent application vulnerabilities
- Does not protect against zero-day exploits
- Does not provide data encryption
- Does not authenticate users
- Does not replace firewalls or WAF (complements them)
- Does not guarantee 100% uptime during massive attacks
- Does not protect against insider threats
- Does not prevent account takeovers
- Does not scan for malware in traffic
- Does not provide infrastructure patching
- Does not prevent all false positives (some legitimate traffic may be challenged)

---

### Summary Comparison Table

| Device | Layer | Primary Function | AWS Product | Azure Product |
|--------|-------|------------------|-------------|---------------|
| Load Balancer | 4/7 | Distribute traffic | ALB, NLB | Azure Load Balancer, App Gateway |
| Firewall | 3/4 | Filter traffic | Network Firewall, Security Groups | Azure Firewall, NSGs |
| API Gateway | 7 | API management | API Gateway | API Management |
| NAT Gateway | 3/4 | Outbound NAT | NAT Gateway | NAT Gateway |
| VPN Gateway | 3/4 | Encrypted tunnels | Virtual Private Gateway | VPN Gateway |
| WAF | 7 | Web attack protection | AWS WAF | Web Application Firewall |
| CDN | 7 | Content caching | CloudFront | Azure CDN |
| DNS | 7 | Name resolution | Route 53 | Azure DNS |
| Internet Gateway | 3 | VPC internet access | Internet Gateway | Implicit in VNet |
| Transit Gateway | 3 | Network hub | Transit Gateway | Virtual WAN |
| DDoS Protection | 3-7 | Attack mitigation | Shield | DDoS Protection |

---

### Key Differences: Data Path Vs Control Path

#### Data Path Devices (Forward Traffic)
- Load Balancer
- NAT Gateway
- Internet Gateway
- Transit Gateway
- CDN

#### Control/Inspection Devices (Inspect and Filter)
- Firewall
- WAF
- DDoS Protection
- API Gateway (partial)

#### Resolution Devices (Do Not Forward Packets)
- DNS

---

### Common Misconceptions

1. **Load Balancer ≠ Firewall**
   - Load balancers distribute traffic but don't filter based on security rules
   - Need separate firewall for security filtering

2. **NAT Gateway ≠ Internet Gateway**
   - NAT: For private instances (outbound only, no public IP on instance)
   - IGW: For public instances (bidirectional, requires public IP)

3. **API Gateway ≠ Application Load Balancer**
   - API Gateway: API-specific features (auth, rate limiting, transformation)
   - ALB: Generic Layer 7 load balancing (no API-specific features)

4. **WAF ≠ Firewall**
   - WAF: Layer 7, application attacks (SQL injection, XSS)
   - Firewall: Layer 3/4, network filtering (IP, port, protocol)

5. **CDN ≠ Load Balancer**
   - CDN: Caches content at edge locations (reduces origin load)
   - Load Balancer: Distributes live requests across backends (no caching)

---

This wiki provides a comprehensive understanding of cloud network devices from a data-centric perspective, showing exactly how packets are processed, what each device can and cannot do, and which cloud products map to each device type.

I am learning about cloud networking. I know there are multiple network devices. Also Aws and Azure have different products for each. Write me a markdown wiki listing the devices like firewall API gateway loadbalancer and so on. For each describe the genetic device, list the products for both Aws and Azure.

This is where my requirements get specific. I want to understand these devices from a data centric perspective. Give an example with a fictional packet. Also list functional requirements for each device so I fully understand what each device is supposed to do, and how and what it is not.

Here is a structured markdown wiki for key cloud networking devices—Firewall, API Gateway, and Load Balancer—with a data-centric perspective. For each device, you'll find: (1) a general description, (2) leading products from AWS and Azure, (3) a walkthrough with a fictional network packet, and (4) functional requirements to clarify what the device is and isn't supposed to do.

***

## Cloud Network Devices: Data-Centric Overview

***

### Firewall

#### Purpose & Device Description

A firewall is a security device or service that inspects and filters network packets based on a defined set of rules, allowing or blocking traffic to protect applications, services, and data from unauthorized access or attacks. Firewalls can work at different OSI layers, implementing packet filtering, stateful inspection, and deep packet inspection[1][2].

#### Key Offerings

| Provider | Product(s)       |
|----------|------------------|
| **AWS**  | AWS Network Firewall, AWS WAF, Security Groups, NACLs |
| **Azure**| Azure Firewall, Azure Web Application Firewall (WAF), NSGs |

#### Fictional Packet Example
- **Input:** A TCP SYN packet from 192.0.2.25:58001 targeting 10.10.21.15:443 attempts to enter the VPC.
    - AWS: AWS Network Firewall checks rules for inbound traffic on port 443; packet allowed if permitted, dropped if not.
    - Azure: Azure Firewall inspects the packet, applies TLS inspection if configured, forwards or blocks based on rule match.

#### Functional Requirements
- Allow/deny traffic based on protocol, port, source/destination IP, and packet content (for deep inspection)
- Log allowed and denied attempts for auditing and compliance
- Enforce stateful inspection (track connection state)
- Provide defense against known threats (e.g., malware, port scans, DDoS at the network/app layer if combined with WAF)
- **Not:** Responsible for application logic, serving user requests, or granular request routing to microservices[2].

***

### API Gateway

#### Purpose & Device Description

An API Gateway acts as a single point of entry for all client requests to backend APIs and microservices. It manages, authenticates, transforms, and routes API calls, implements security policies, and may aggregate or reformat data before sending it to consumers[3].

#### Key Offerings

| Provider | Product(s)       |
|----------|------------------|
| **AWS**  | Amazon API Gateway, AWS AppSync |
| **Azure**| Azure API Management (APIM)     |

#### Fictional Packet Example
- **Input:** HTTP POST /api/v1/orders with JSON payload and JWT token from client 198.51.100.25 at 08:01 UTC.
    - **Gateway actions:**
        - Validates JWT.
        - Logs the request metadata.
        - Applies rate limiting (blocks if over quota).
        - Translates path if necessary (e.g., /orders -> /orders-service/v2/process).
        - Forwards permitted request to correct backend microservice (orders-service pod).
        - Returns API response to client.

#### Functional Requirements
- Authenticate/authorize client requests[3].
- Route requests to appropriate microservice(s) based on URI, method, or header rules.
- Enforce rate limiting, quotas, and throttling.
- Transform requests/responses (e.g., API versioning, protocol conversion).
- Aggregate calls to multiple services into single response if needed.
- Provide request/response logging for observability.
- **Not:** Responsible for distributing traffic for raw TCP load or serving as a full Layer 4/7 load balancer for non-API protocols.

***

### Load Balancer

#### Purpose & Device Description

A load balancer distributes incoming network or application traffic among multiple servers to improve reliability, performance, and scalability. Load balancers operate at Layer 4 (transport—TCP/UDP) or Layer 7 (application—HTTP/S), rerouting packets intelligently to healthy targets[3][2].

#### Key Offerings

| Provider | Product(s)           |
|----------|----------------------|
| **AWS**  | Elastic Load Balancing: Application (ALB), Network (NLB), Gateway Load Balancer (GWLB) |
| **Azure**| Azure Load Balancer (L4), Application Gateway (L7), Traffic Manager (DNS), Azure Front Door |

#### Fictional Packet Example
- **Input:** HTTPS GET request for `/home` arrives at ALB from 203.0.113.36:49383
    - ALB health checks backend pool, routes request to least loaded and healthy target, maintains session stickiness if required.
    - Azure Application Gateway inspects URL path, applies WAF rules if configured, then forwards to one of the backend web servers.

#### Functional Requirements
- Distribute requests/packets based on load, protocol, health, or session stickiness[3][2].
- Scale backend services horizontally by adding/removing instances.
- Provide health checks and automatic failover.
- Support SSL termination or passthrough.
- Offer L4 (TCP/UDP) and/or L7 (HTTP/S) balancing as needed.
- **Not:** Responsible for application-specific logic, user authentication, or in-depth packet content filtering (unless integrated with WAF).

***

## Quick Comparison Table

| Device        | Core Function                           | AWS Offerings                   | Azure Offerings              | Example Packet Action             |
|---------------|----------------------------------------|----------------------------------|------------------------------|-----------------------------------|
| Firewall      | Inspects & filters traffic for threats  | Network Firewall, WAF, Security Groups | Azure Firewall, WAF, NSG      | Allows/denies inbound TCP SYN     |
| API Gateway   | Manages and routes API traffic          | API Gateway, AppSync             | APIM                        | Authenticates, rate limits POST   |
| Load Balancer | Distributes traffic to backend targets  | ALB, NLB, GWLB                   | Load Balancer, App Gateway   | Routes HTTPS GET to healthy VM    |

***

## References & Further Reading

- Roles and comparisons: API Gateway vs Load Balancer[3]
- Example cloud architectures: Azure High-Availability reference[2]

***

This wiki gives you both the theoretical and practical context to reason about each device from a network data-path perspective—what it does, with which products, and exactly how it handles a typical packet across AWS and Azure.

Citations:

[1] Network Devices: Common Types and Their Functions <https://www.lepide.com/blog/the-most-common-types-of-network-devices/>

[2] Multi-region load balancing - Azure Architecture Center <https://learn.microsoft.com/en-us/azure/architecture/high-availability/reference-architecture-traffic-manager-application-gateway>

[3] Decoding the Roles: API Gateway vs Load Balancer <https://www.moesif.com/blog/technical/api-development/API-Gateway-VS-Load-Balancer/>

[4] Common Types of Network Devices and Their Functions <https://netwrix.com/en/resources/blog/network-devices-explained/>

[5] Google Cloud networking products <https://cloud.google.com/products/networking>

[6] 10 Most Common Network Devices & How to Monitor Them <https://obkio.com/blog/common-network-devices/>

[7] Network Devices <https://www.geeksforgeeks.org/computer-networks/network-devices-hub-repeater-bridge-switch-router-gateways/>

[8] BIG-IP integration with Azure Gateway Load Balancer <https://community.f5.com/kb/technicalarticles/big-ip-integration-with-azure-gateway-load-balancer/291102>

[9] 10 common network devices: What they are + what they do <https://www.meter.com/resources/network-devices>

[10] Gateway Load Balancer (GWLB) <https://aws.amazon.com/elasticloadbalancing/gateway-load-balancer/>

[11] Cisco Networking Products and Solutions <https://www.cisco.com/site/uk/en/products/networking/index.html>

[12] Difference between AWS Network Firewall & Gateway ... <https://www.reddit.com/r/aws/comments/qd0ftx/difference_between_aws_network_firewall_gateway/>

[13] Azure Firewall and Application Gateway for Virtual Networks <https://learn.microsoft.com/en-us/azure/architecture/example-scenario/gateway/firewall-application-gateway>

[14] Top 10: Data Centre Networking Technologies <https://datacentremagazine.com/top10/top-10-data-centre-networking-technologies>

[15] Deployment models for AWS Network Firewall <https://aws.amazon.com/blogs/networking-and-content-delivery/deployment-models-for-aws-network-firewall/>

[16] Gateway load balancer - Azure <https://learn.microsoft.com/en-us/azure/load-balancer/gateway-overview>

[17] Azure networking services overview <https://learn.microsoft.com/en-us/azure/networking/fundamentals/networking-overview>

[18] Best practices for deploying Gateway Load Balancer <https://aws.amazon.com/blogs/networking-and-content-delivery/best-practices-for-deploying-gateway-load-balancer/>

[19] VM-Series Virtual Firewalls Integrate with Azure Gateway ... <https://www.paloaltonetworks.com/blog/network-security/vm-series-azure-gateway-load-balancer/>

[20] What are the names of few commonly used networking ... <https://www.leaftechit.com/what-are-the-names-of-few-commonly-used-networking-devices/>
