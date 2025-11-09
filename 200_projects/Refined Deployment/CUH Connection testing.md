---
aliases: []
confidence: 
created: 2025-09-08T11:30:09Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:10Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: CUH Connection testing
type:
uid: 
updated: 
version:
---

TT prep

1. We can perform test 1.3.2 without a hostname (on ip address only) and monitor for failed TLS handshake in the ingress-nginx logs. This will take ~30 mins.

- ingress-nginx new chart values to increase verbosity is this:
  - controller:
  - extraArgs:
    - v: "5"

30 mins total

---

2.3.1 - certificate lifecycle

- FITFILE Cloudflare DNS configured with public IP of CUH. 5 minutes
- **CUH vault secrets updated with cloud flare API key - 15 minutes**
- **CUH terraform to deploy additional Vault app role secrets to cert-manager namespace - 30 mins**
- Import cert-manager into our fitfile private ACR - 5 mins
- Verify the imported helm chart is valid and all images are correct (i.e. from the private ACR) - 15 mins
- Modify the fitfile ffnode chart to use this cert-manager chart - 5 mins
- Deploy this to our own kubernetes clusters and ensure it works - 1hour
- Modify the fitconnect and ffcloud helm charts to accept more general ingress configuration. Needs to support this: 1 hour

apiVersion: networking.k8s.io/v1

kind: Ingress

metadata:

name: foo-tls

namespace: default

spec:

ingressClassName: nginx

tls:

- hosts:
  - foo.bar.com
    This secret must exist beforehand
    The cert must also contain the subj-name foo.bar.com
    <https://github.com/kubernetes/ingress-nginx/blob/main/docs/examples/PREREQUISITES.md#tls-certificates>
    secretName: foobar
- hosts:
  - bar.baz.com
    This secret must exist beforehand
    The cert must also contain the subj-name bar.baz.com
    <https://github.com/kubernetes/ingress-nginx/blob/main/docs/examples/PREREQUISITES.md#tls-certificates>
    secretName: barbaz
    rules:
- host: foo.bar.com
  http:
  paths:
  - path: /
    pathType: Prefix
    backend:
    service:
    name: http-svc
    port:
    number: 80
- host: bar.baz.com
  http:
  paths:
  - path: /
    pathType: Prefix
    backend:
    service:
    name: nginx
    port:
    number: 80

- Configure the cert-manager deployment for CUH
  - Configuring all the certificates which would be needed for cert-manager - 1 certificates needed (app.cuh-prod-1.fitfile.net) and ensure existing default nginx certificate still is used for (cuh-poc-1.privatelink.fitfile.net) - 30 mins
  - **Configure vault secret for cloud flare api key for cert-manager - 5 mins**
  - Configure the fitconnect and ffcloud ingress objects - 30 mins
  - Deploy these changes - 30 mins
- Run the test cases for cloudflare integration

5 hours of work time - round up to a day as we are always pulled into bullshit

Test time for cloud flare integration is around 2 hours

7 hours total

---

3.3.0 Curl Relay from CUH

1. Import busy box into our ACR - 10 mins
2. Connect to CUH jump-box - 5 mins
3. Deploy debug pod into CUH - 30 mins
4. Run curl test - 5 mins

~ 1 hour

3.3.1 Test Bunny connection to SQL database and 3.3.2

- Dependent on database credentials
- Upgrade relay version in SDE - import images, modify helm and release to EoE ~ 1 hour
- Upgrade bunny version - import images and modify helm ~ 30 mins
- **Configure vault secrets with new bunny credentials ~ 15 mins**
- CUH terraform update to deploy app role secrets for bunny Vault access ~ 30 mins
- Configure the bunny CUH deployment helm ~ 30 mins
- Release bunny to CUH ~ 30 mins

Tests - 1 hour is successful

~ 5 hours

Total 6 hours

Of course, here is a summary of the points made in the email chain, formatted as a markdown note.

---

## 📧 Email Chain Summary: Fit File Node Connection to OMOP Database

This note summarises the key actions, decisions, and status updates regarding the establishment of a connection between the FITFILE CUH Node and the OMOP Database, as well as the subsequent connection to the SDE Node.

**Change Request Number:** `CHG0048896` 1

**Key Organisations Involved:**

- **FITFILE:** The software provider.
- **Telefónica Tech (TT):** The delivery partner managing technical implementation.
- **Cambridge University Hospitals NHS Foundation Trust (CUH):** The client/host of the database.
- **Health Innovation East (HIE):** Supporting CUH and FITFILE with the SDE (Secure Data Environment)222.

---

### 📝 Discovery & Planning

- **Project Documentation:**
  - Mark Dines-Allen (HIE) enquired about a Project Initiation Document (PID) to support the change request3.
  - Laurence Coleby-Frater (Telefónica Tech) confirmed he will issue the PID as soon as possible 4and will document the full project plan5.
- **Scope Finalisation:**
  - Sean and Donald (Telefónica Tech) are responsible for finalising the project scope, including all necessary URLs, IPs, and ports6.
  - Sean will also update the impact assessment to reflect the planned changes7.
- **Meeting Coordination:**
  - Multiple emails were exchanged to schedule a planning call for the week commencing 1st September to agree on next steps8888888888888888.

---

### 💻 Technical Implementation & Configuration

- **Authentication Method:**
  - The project team troubleshooted connection issues between the FITFILE CUH Node and the OMOP database9.
  - **Windows authentication** was chosen as the preferred method over SQL Server authentication10.
  - Changes were required in the FITFILE client to support this method11.
- **Database Permissions:**
  - Jakub (CUH) updated database permissions to grant the FITFILE service account the necessary access rights12.
  - It was confirmed the account has the appropriate

        **"OMOP reader" role**13.

- **Infrastructure Changes (Telefónica Tech):**
  - **Firewall:** Ahmed is leading the firewall rule changes, which will be implemented after CAB approval on Thursday or Friday14.
  - **Proxy:** Sean and Laurence will update the proxy allow list, also pending CAB approval15.
  - **DNS:** Sean and Donald will handle the DNS record creation16.
  - A separate change request (

        `CHG0048910`) was raised to allow specific URLs17.

---

### ✅ Testing & Validation

- **Initial Connection:** The team successfully established a connection and confirmed they could access synthetic OMOP data for testing and training purposes18.
- **Live Testing Plan:**
  - Live testing was proposed to begin on 8th September19.
  - Testing is being conducted under an open change for the week commencing the 8th to allow for adjustments20.
- **Status Update (as of 8th Sep):**
  - Oliver Rushton (FITFILE) confirmed that the first set of test cases were

        **completed successfully**21.

  - Completed tests include:
    - `1.3.2`: Inbound HTTPS routing from SDE Node to CUH Node (without TLS)22.
    - `2.3.0`: Outbound access to the Cloudflare API23.
    - `3.3.0`: Outbound access to the Relay24.
  - **Next Steps:** Leon and Ollie (FITFILE) will now work on the remaining tests, which is estimated to take a couple of days25.

---

### 🔑 Clarification on SDE Access

- Leon Ormes (FITFILE) clarified the access model to avoid confusion26.
- SDE Data Managers from HIE do

  **not** directly log in to the CUH FITFILE application27. They use their own separate FITFILE application28.

- The connection being built is a **machine-to-machine link only**. The SDE system queries CUH as a data source and receives treated data back29292929.
- Because access is not direct, SDE Data Managers do not need to complete 3PVA (Third-Party Vendor Access) forms30.
  Certainly, here is the content from the provided file converted into an Obsidian markdown note.

---

EOE CUH Networking Test Plan 1

1. Connectivity Test Plan: FITFILE Hub (EoE SDE) to CUH FITFILE Node (via On-Premise Network) 2

1.1 Introduction & Objective 3

This document outlines the test plan to validate network connectivity from the FITFILE application in the East of England AWS environment (the FITFILE Hub), to the CUH FITFILE Node deployed in Azure via the CUH on-premise network4. The primary objective is to perform an end-to-end connectivity test to confirm that the newly configured network path is fully functional for machine-to-machine communication between the FITFILE nodes5.

1.2 Prerequisites & Scheduling 6

To proceed with testing, the following information is required from the TT team7:

- **Endpoint Details:** The specific IP address and port8.
  - Once provided, FITFILE can implement the certificate management solution and DNS configuration needed to establish a TLS connection from the SDE Hub to the CUH Node9.
- **Test Window:** An agreed-upon time slot to conduct the test, ensuring personnel from both teams are available for monitoring and collaboration10.

  1.3 Test Procedure & Responsibilities 11

The test will be conducted as a coordinated effort between both teams12.

1.3.1 Assert DNS lookup resolves public IP 13

**FITFILE Team Responsibilities** 14

1. FITFILE to run

   `dig` from within the SDE FITFILE Node to ensure the public IP of the CUH Node endpoint can be resolved15.

**TT Team Responsibilities** 16

- Ahead of time, provide the public IP address which the CUH FITFILE Node API endpoint is exposed on17.

**Success Criteria** 18

- The

          `dig` command resolves the expected public IP address19.

  1.3.2 Assert HTTPS routing from SDE Node to CUH Node via on premise network 20

**FITFILE Team Responsibilities** 21

1. Connect to the secure SDE EKS environment22.
2. Deploy a troubleshooting container into the SDE cluster with networking utilities23.
3. Attempt to

   `Curl` the health endpoint of the CUH FITFILE Node24.

4. Monitor our internal application logs for the outcome of the request and provide real-time feedback25.

**TT Team Responsibilities** 26

1. During the agreed test window, actively monitor the relevant on-premise network infrastructure (e.g., firewalls, web gateways) for incoming connection attempts from our SDE source IPs27.
2. Be prepared to capture and share relevant infrastructure logs to assist with diagnostics if required28.

**Success Criteria** 29

The test will be considered successful if30:

- Our application logs show a successful connection to the CUH endpoint31.
- `curl` receives the expected response from the service (e.g., a successful TLS handshake, an HTTP 200 OK status code)32.

**Failure Criteria & Initial Response** 33

- The test will be considered failed if the

  `curl` command cannot establish a connection (e.g., connection timeout, connection refused, DNS resolution failure)34.

- In the event of a failure35:
  1. The FITFILE team will immediately notify the TT team with the specific error message, timestamp, and the verbose logs of the

     `curl` command36.

  2. The TT team will provide corresponding logs from the on-premise infrastructure for the same time period37.
  3. Both teams will collaboratively analyse the combined logs to diagnose the root cause, following the detailed procedures in the appendix38.

---

2. Connectivity Test Plan: FITFILE CUH Node TLS certificate lifecycle management 39

2.1 Introduction & Objective 40

FITFILE will manage the lifecycle of TLS certificates for the FITFILE CUH application41. The ACME CA server will verify FITFILE owns the domain via a DNS01 challenge to the FITFILE Cloudflare tenant DNS42. Therefore, a new outbound firewall route to the Cloudflare APIs has been requested, and the lifecycle management of the CUH FITFILE application TLS certificates needs to be tested43.

2.2 Prerequisites & Scheduling 44

To proceed with testing, we need the following information from the TT team45:

- Confirmation that the CUH on-premise firewall and proxy configuration has been configured to allow outbound TLS traffic to the Cloudflare API46.
- An agreed-upon time slot to conduct the test, ensuring personnel from both teams are available47.

FITFILE must complete the following prior to the test48:

- Deploy and configure cert-manager into the CUH Node49.

  2.3 Test Procedure & Responsibilities 50

The test will be conducted as a coordinated effort between both teams51.

2.3.0 Curl Cloudflare API from CUH 52

**FITFILE Team Responsibilities:** 53

1. **Initiate Connection:** 54
   - `curl` the Cloudflare API from a debug pod inside the CUH cluster55.

2. **Monitor Logs & status** 56

**CUH/TT Team Responsibilities:** 57

1. **Monitor Network Infrastructure:** During the agreed test window, actively monitor the relevant on-premise network infrastructure for outbound connection attempts from our Azure source IPs to the Relay FQDN58.
2. **Provide Logs on Request:** Be prepared to capture and share relevant infrastructure logs to assist with collaborative diagnostics if required59.

**Success & Failure Criteria** 60

- **Success Criteria:** The `curl` command returns 20061.
- **Failure Criteria & Initial Response:** The test is considered failed if the `curl` response is not 200, or application logs show errors like `Connection timeout`, `Connection refused`, `DNS resolution failure`, or TLS/SSL handshake errors62. In case of failure, the FITFILE team will immediately notify the CUH/TT team with the error message and timestamp63. Both teams will then use the troubleshooting steps in the appendix64.

  2.3.1 Assert initial TLS certificate creation 65

**FITFILE Team Responsibilities** 66

1. FITFILE to configure a certificate request for the CUH FITFILE Node API service67.
2. FITFILE to monitor certificate creation via calls to the Kubernetes API from the CUH Jumpbox68.
3. FITFILE to verify certificate authenticity via a

   `curl` call to the CUH Node API health endpoint from the Jumpbox69.

   - `/etc/hosts` on the Jumpbox will be modified to add the hostname within the TLS certificate70.

**TT Team Responsibilities** 71

- During the agreed test window, actively monitor the on-premise network infrastructure for outbound connection attempts from the CUH FITFILE Kubernetes outbound IP address to Cloudflare APIs72.
- Be prepared to capture and share relevant infrastructure logs to assist with diagnostics if required73.

**Success Criteria** 74

The test will be considered successful if75:

- The cert-manager logs show a successful certificate instantiation lifecycle76.
- Our application logs show a successful connection to the API health endpoint77.
- `curl` receives the expected response from the service (e.g., successful TLS handshake, HTTP 200 OK)78.

**Failure Criteria & Initial Response** 79

- The test will be considered failed if the cert-manager service errors during the DNS01 challenge with the Cloudflare APIs80.
- The test will also fail if the

  `curl` command cannot establish a connection to the health endpoint81.

- In the event of a failure82:

          1. The FITFILE team will immediately notify the TT team with the specific error message and timestamp83.
          2. The TT team will provide corresponding logs from the on-premise infrastructure84.
          3. Both teams will collaboratively analyse the logs to diagnose the root cause85.

  2.3.2 Assert TLS certificate rotation 86

**FITFILE Team Responsibilities** 87

1. FITFILE to forcefully delete the previously deployed TLS certificate within the CUH FITFILE Node to trigger a new certificate request88.
2. FITFILE to monitor certificate rotation via calls to the Kubernetes API from the CUH Jumpbox89.
3. FITFILE to verify certificate authenticity via a

   `curl` call to the CUH Node API health endpoint from the Jumpbox90.

   - `/etc/hosts` on the Jumpbox will be modified to add the hostname within the TLS certificate91.

**TT Team Responsibilities** 92

- During the agreed test window, actively monitor the network for outbound connection attempts from the CUH FITFILE Kubernetes outbound IP address to Cloudflare APIs93.
- Be prepared to capture and share infrastructure logs if required94.

**Success Criteria** 95

The test will be successful if96:

- The cert-manager logs show a successful certificate rotation lifecycle97.
- Application logs show a successful connection to the API health endpoint98.
- `curl` receives the expected response (e.g., successful TLS handshake, HTTP 200 OK)99.

**Failure Criteria & Initial Response** 100

- The test is failed if cert-manager errors during the DNS01 challenge with Cloudflare APIs101.
- The test is also failed if

  `curl` cannot connect to the health endpoint102.

- In the event of a failure103:
  1. FITFILE team will notify the TT team with the error message and timestamp104.
  2. TT team will provide corresponding logs from the on-premise infrastructure105.
  3. Both teams will analyse the logs to find the root cause106.

---

3. Connectivity Test Plan: FITFILE CUH Cohort Discovery 107

3.1 Introduction 108

The National Cohort Discovery initiative allows researchers to query cohort counts across multiple SDEs109. FITFILE deploys an application called "Bunny" to the CUH node to fetch and execute these queries against the OMOP database110.

3.1.1 Architecture & Communication Flow 111

- FITFILE uses a 3rd party solution called Hutch, which consists of two services: Bunny and Relay112.
- **Bunny:** A client that connects to an OMOP SQL database to run queries113. It is deployed at the source in the CUH FITFILE Kubernetes cluster114.
- **Relay:** A proxy to the HDRUK BC RQuest system's task API115. It is deployed in the EoE SDE Node116.
- The connection from Bunny to Relay travels via the CUH on-premise network and web proxy, requiring new firewall routing for outbound traffic117.
- **Flow:** `SQL OMOP Database <-- Bunny (CUH) ---> Relay (EoE SDE) ---> HDRUK (BC RQuest)`118.
- The connection is initiated outbound from the Azure CUH environment119. Traffic from the Azure VNet is routed through on-premise firewalls and proxies managed by TT120.
- No extra networking is needed for Bunny's connection to the SQL database121.

  3.2 Prerequisites 122

- The CUH public egress IP address(es) must be identified123.
- FITFILE must configure the AWS Security Group to only allow inbound traffic from the CUH public egress IP(s)124.
- SQL credentials for the Bunny client must be created and securely provided to FITFILE125. Bunny supports basic SQL username/password authentication126.
- FITFILE will deploy the Bunny instance into the CUH cluster once prerequisites are met127.
- TT must have configured firewall rules and the web proxy to allow outbound HTTPS traffic to the Relay server128.
- A test window must be agreed upon to ensure teams are available to monitor logs129.

  3.3 Test Procedure & Responsibilities 130

This is a coordinated effort131.

3.3.0 Curl Relay from CUH 132

**FITFILE Team Responsibilities:** 133

1. **Initiate Connection:** `curl` the relay server from a debug pod inside the CUH cluster134.
2. **Monitor Logs & status** 135

**CUH/TT Team Responsibilities:** 136

1. **Monitor Network Infrastructure:** Actively monitor on-premise network infrastructure for outbound connection attempts137.
2. **Provide Logs on Request:** Be ready to share infrastructure logs for diagnostics138.

**Success & Failure Criteria** 139

- **Success Criteria:** The `curl` command returns 200140.
- **Failure Criteria & Initial Response:** The test fails if the `curl` response is not 200 or if there are connection errors141. In case of failure, FITFILE will notify the CUH/TT team immediately 142, and both teams will use the troubleshooting steps in the appendix143.

  3.3.1 Test Bunny connection to SQL database 144

**FITFILE Team Responsibilities:** 145

1. **Initiate Connection:** Ensure the Bunny pod starts successfully in the AKS cluster146.
2. **Monitor Logs & Status:** Monitor the Bunny pod's logs in real-time to observe database connection attempts147.

**CUH/TT Team Responsibilities:** 148

1. **Monitor Network Infrastructure:** Actively monitor on-premise network infrastructure for outbound connection attempts149.
2. **Provide Logs on Request:** Be ready to share infrastructure logs for diagnostics150.

**Success & Failure Criteria** 151

- **Success Criteria:** The Hutch Bunny application logs show a successful connection to the database152.
- **Failure Criteria & Initial Response:** The test fails if Bunny logs show connection errors or invalid credentials153. In case of failure, FITFILE will notify the CUH/TT team 154, and both teams will use the troubleshooting steps in the appendix155.

  3.3.2 Test Bunny connection to Relay 156

**FITFILE Team Responsibilities:** 157

1. **Initiate Connection:** Ensure the Bunny pod starts successfully; it will automatically poll the Relay endpoint158.
2. **Monitor Logs & Status:** Monitor Bunny pod logs for connection attempts to the Relay159.

**Success & Failure Criteria** 160

- **Success Criteria:** 161
  - Bunny application logs show a successful connection (HTTP 200 OK) when polling the Relay's task API162.
  - Relay application logs in AWS show an incoming request from Bunny's source IP163.
  - Bunny successfully retrieves a "no tasks available" message or a test task164.
- **Failure Criteria & Initial Response:** The test fails if Bunny logs show connection errors165. In case of failure, FITFILE will notify the CUH/TT team 166, and both teams will use the troubleshooting steps in the appendix167.

---

Appendix A: Troubleshooting TLS/Certificate Issues 168

These steps will be followed for TLS/SSL handshake failures169.

**FITFILE Team Diagnostics** 170

1. **Deploy Debug Pod:** A temporary troubleshooting pod will be launched in the AKS cluster171.

   Bash

   ```sh
   kubectl run it -rm --image nicolaka/netshoot cert-debug -- /bin/bash [cite: 555]
   ```

2. **Inspect Server Certificate:** Use `openssl` to inspect the certificate presented by the CUH endpoint172.

   Bash

   ```sh
   # Replace <fqdn> and <port> with actual endpoint details [cite: 557]
   openssl s_client -connect <fqdn>:<port> -servername <fqdn> [cite: 558]
   ```

3. **Analyse Certificate:** Check for common issues173:
   - **Trust:** Is the certificate signed by an internal CUH CA? 174
   - **Hostname Mismatch:** Does the CN or SAN match the FQDN? 175
   - **Expiration:** Is the certificate expired? 176
   - **Incomplete Chain:** Is the server sending the full certificate chain? 177

**Information Required from TT Team** 178

If an internal CA is used, the public keys for the full CA chain will be required to add to the application's trust store179.

---

Appendix B: Troubleshooting Routing & Firewall Issues 180

This approach is used for errors like network timeout, "No route to host," or "Connection refused"181.

**FITFILE Team Diagnostics** 182

1. **Deploy Debug Pod:** A debug pod will be used for diagnostics183.
2. **Verify DNS Resolution:** Confirm the on-premise FQDN resolves correctly184.

   Bash

   ```sh
   # Replace <fqdn> with the actual on-premise hostname [cite: 572]
   nslookup <fqdn> [cite: 573]
   ```

3. **Trace Network Path:** Use `traceroute` to map the packet's journey185.

   Bash

   ```sh
   # Replace <on-prem-ip> with the actual IP address [cite: 575]
   traceroute <on-prem-ip> [cite: 576]
   ```

4. **Verify Azure Routing:** Use Azure tools ("Effective Routes" and "IP Flow Verify") to confirm a valid route exists and is not blocked by NSG rules186.

**Information & Logs Required from TT Team (On-Premise)** 187

The TT team will be requested to correlate test attempts with logs from your infrastructure188.

1. **Firewall Log Analysis:** Check on-premise firewall logs for traffic from Azure source IPs to determine189:
   - Did the traffic arrive at the firewall? 190
   - Was the traffic allowed (ACCEPT) or blocked (DENY / DROP)? 191
   - If blocked, which policy was responsible? 192

2. **BGP Route Verification:** Confirm that on-premise edge routers are correctly receiving the BGP route for our Azure VNet address space (`10.224.0.0/12`)193. Return traffic will fail if this route is missing194.
3. **Web Gateway / Proxy Logs:** If applicable, inspect logs for any blocked connection attempts from our source IPs195.
