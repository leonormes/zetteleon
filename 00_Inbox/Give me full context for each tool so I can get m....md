Here is the full technical context for each tool, extracted and structured for use by an LLM to plan infrastructure code and deployment workflows.

### **Global Context & Variables**

* **Repository:** "Central Services" 1

* **Deployment Key:** A unique, short identifier for the customer (e.g., WM-Prod). This key is used as the directory name and variable key throughout the infrastructure code. **Crucial:** Do not use the full customer name. 2

* **Actors:** DevOps contributors responsible for Central Services. 3

### ---

**1\. HashiCorp Vault**

Role: Secret management and storage.  
State: Managed via Terraform (structure) and manual entry (secret values).

#### **Context A: Infrastructure Provisioning (Terraform)**

* **Location:** hcp/vault directory within the Central Services repository. 4

* **File to Modify:** locals.tf. 55

* **Action:** Add a new block to the deployments variable map using the deployment-key. 6666

* **HCL Structure:**  
  Terraform  
  "\<replace\_with\_deployment\_key\>" \= {  
    secrets \= tomap({  
      "application"    \= {},  
      "spicedb"        \= {},  
      "cloudflare"     \= {}, \# Include only if using Cloudflare  
      "monitoring"     \= {}, \# For Grafana credentials  
      "argo-workflows" \= {}, \# For Argo Workflows SSO  
    })  
  }

  7

* **Execution:** Commit changes to trigger Terraform Cloud plan/apply. 8

#### **Context B: Secret Population (Manual/Console)**

* **Access Method:** HCP Portal \-\> Vault Dedicated \-\> Generate Admin Token (Public). 9

* **Namespace:** deployments/\<deployment-key\>. 10

* **Constraint:** Vault JSON input **does not accept comments**. All comments in the schemas below must be stripped before saving. 11

**Secret Schemas (JSON):**

* **application Secret:**  
  * **Source:** Mixed (Manual generation, Terraform outputs, UDE CLI, OpenSSL).  
  * **Fields:**  
    * cli\_auth\_client\_id, cli\_auth\_client\_secret: Leave blank. 12121212

    * mesh\_client\_cert, mesh\_client\_key, mesh\_hash\_secret, mesh\_mailbox\_password: Leave blank if opt-out. 13

    * mongodb\_password: Min length 10, alphanumeric. 14

    * mongodb\_username: "root". 15

    * mongodb\_replica\_set\_key: Length 64, alphanumeric. 16

    * postgresql\_password: Min length 10, alphanumeric. 17

    * postgresql\_username: "postgres". 18

    * s3\_access\_key\_id: "ffadmin". 19

    * s3\_secret\_access\_key: Min length 10, alphanumeric. 20

    * ude\_key: Derived from UDE CLI (see Tool 2). 21

    * spicedb\_pre\_shared\_key: Shared key. If centralised, retrieve from admin/fitfile/production/spicedb\_secrets. 22

    * fitfile\_tenant\_pkcs8.key: Derived from OpenSSL (see Tool 3). 23

    * fitfile\_tenant\_public.crt: Derived from OpenSSL (see Tool 3). 24

    * auth0\_client\_id: From Auth0 Terraform output. 25

    * auth0\_client\_secret: From Auth0 Terraform output. 26

    * auth0\_audience: From Auth0 Terraform output. 27

    * auth0\_frontend\_client\_id: From Auth0 Terraform output. 28

    * auth0\_frontend\_client\_secret: From Auth0 Terraform output. 29

* **spicedb Secret:**  
  * **Fields:**  
    * postgresql\_password: Min length 10, alphanumeric. 30

    * postgresql\_username: "postgres". 31

    * spicedb\_preshared\_key: Must match the key in application secrets. 32

* **cloudflare Secret:**  
  * **Prerequisite:** Only if using Cloudflare DNS. 33

  * **Source:** Cloudflare Portal \-\> API Tokens \-\> Edit DNS permissions for specific zone. 34

  * **Fields:** {"api\_token": "..."} 35

* **monitoring Secret:**  
  * **Source:** Grafana Terraform outputs (see Tool 5).  
  * **Fields:** prometheus\_host, prometheus\_username, prometheus\_password, loki\_host, loki\_username, loki\_password, tempo\_host (append :443), tempo\_username, tempo\_password. 36

### ---

**2\. UDE CLI**

**Role:** Generating cryptographic keys for the ude\_key field in Vault.

* **Repository:** "UDE CLI". 37

* **Prerequisites:** Rust Nightly (rustup install nightly). 38

* **Command:** cargo run key-gen 39

* **Output:** The final line of the console output is the unique key string required for Vault. 40

### ---

**3\. OpenSSL**

**Role:** Generating Tenant PKCS8 signing keys for fitfile\_tenant secrets in Vault.

* **Context:** Run locally in a temporary directory named \<deployment-key\>. 41

* **Commands:**  
  1. openssl genrsa \-out keypair.pem 4096 42

  2. openssl pkcs8 \-topk8 \-inform PEM \-outform PEM \-nocrypt \-in keypair.pem \-out pkcs8.key 43

  3. openssl rsa \-in keypair.pem \-pubout \-out publickey.crt 44

* **Mapping to Vault:**  
  * pkcs8.key content \-\> fitfile\_tenant\_pkcs8.key 45

  * publickey.crt content \-\> fitfile\_tenant\_public.crt 46

### ---

**4\. Auth0 (Identity)**

Role: Identity management for the application.  
State: Managed via Terraform.

* **Location:** auth0/prod or auth0/non-prod directory within Central Services. 47

* **File to Modify:** auth0/locals.tf. 48

* **Configuration Block (fitfile\_tenant\_applications):**  
  * tenant\_name: Internal display name (e.g., "WM Dev 1"). 49

  * api\_audience: The HTTPS address of the ingress controller DNS record. 50505050

  * enabled\_apis: List of partner audiences (can be empty \[\]). 51

  * whitelist\_api\_audience\_for\_login\_redirect: true for web apps. 52

* **File to Modify:** main.tf (Optional).  
  * additional\_logout\_redirect\_urls: e.g., https://\<host\>/fitfile. 53

  * additional\_web\_origins: e.g., https://\<host\> (Wildcards supported). 54

* **Outputs Required:** Run terraform output \-json to retrieve: 55

  * Deployment client\_id & client\_secret.  
  * webapp\_application\_client\_credential client\_id & client\_secret.  
  * api\_audience.

### ---

**5\. Grafana (Observability)**

Role: Monitoring stack (Prometheus, Loki, Tempo).  
State: Managed via Terraform.

* **Location:** grafana directory within Central Services. 56

* **File to Modify:** locals.tf. 57

* **Configuration:** Add key to deployments map.  
  * stack: Set to local.prod\_stack or local.non\_prod\_stack. 58

* **Outputs Required:** Run terraform output \-json to retrieve hostnames and credentials for Prometheus, Loki, and Tempo. These are inputs for the Vault monitoring secret. 59

### ---

**6\. ArgoCD & Argo Workflows**

Role: Continuous Deployment and Workflow Orchestration.  
State: Configuration via Vault Secrets.

#### **ArgoCD Secrets (argo-cd)**

* **Location:** Vault Secret argo-cd (implied context from schema list).  
* **Fields:**  
  * admin\_password: Generated via htpasswd \-nbBC 10 \<password\> | tr \-d ':\\n' | sed 's/\\$2y/\\$2a/'. 60

  * gitlab\_deploy\_token\_username / password: From GitLab "Deploy tokens" (read\_repository role). 61

  * sso\_azure\_client\_secret: From Microsoft Entra ID. 62

  * server\_secret\_key: Generated via openssl rand \-base64 32. 63

#### **Argo Workflows Secrets (argo-workflows)**

* **Location:** Vault Secret argo-workflows.  
* **Fields:**  
  * argo\_sso\_client\_id / argo\_sso\_client\_secret: Optional (if ingress attached). 64

  * postgresql\_password / postgresql\_username: Currently mirrors the **application** database credentials. 65656565

### ---

**Dependency Map for Planner**

1. **Vault Init:** Must be done first to create the "buckets" for secrets.  
2. **Tool Execution:**  
   * Run **UDE CLI** to get ude\_key.  
   * Run **OpenSSL** to get tenant keys.  
3. **Terraform Layers:**  
   * Run **Auth0 Terraform**. \-\> *Output feeds into Vault application secret.*  
   * Run **Grafana Terraform**. \-\> *Output feeds into Vault monitoring secret.*  
4. **Vault Finalisation:**  
   * Populate application secret (needs Auth0 outputs \+ UDE key \+ OpenSSL keys).  
   * Populate monitoring secret (needs Grafana outputs).  
   * Populate argo-cd and spicedb (independent generation).

Would you like me to generate the specific terraform output command scripts to automate the extraction of these values into a JSON format?