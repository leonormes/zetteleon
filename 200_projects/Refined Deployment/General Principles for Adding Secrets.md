---
aliases: []
confidence: 
created: 2025-10-24T08:26:44Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:11Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: General Principles for Adding Secrets
type:
uid: 
updated: 
version:
---

Hello! I can help you document the process of adding secrets to a cluster in FITFILE. Based on the context and your work yesterday, here are detailed instructions.

The primary method for managing secrets in FITFILE clusters is through HashiCorp Vault, with integration into Kubernetes handled by the Vault Secrets Operator (VSO) and Helm charts. Secrets are typically stored in Vault and then exposed to pods as Kubernetes secrets or environment variables.

## General Principles for Adding Secrets

Before diving into specific steps, remember these core principles:

- **Never store plaintext secrets in dotfiles or shell configs.** (Relevant long-term memory from `~/.local/share/chezmoi` accessed 2025-10-11 11:27:11 Saturday October 11 2025)
- **Use 1Password CLI (or Vault CLI) to fetch secrets at runtime only.** (Relevant long-term memory from `~/.local/share/chezmoi` accessed 2025-10-11 11:27:11 Saturday October 11 2025)
- **Inject secrets for single-use environments (child processes, not global shell).** (Relevant long-term memory from `~/.local/share/chezmoi` accessed 2025-10-11 11:27:11 Saturday October 11 2025)
- **Secrets are configured through values files, hardcoded values (less common), or external secret references.** (Relevant long-term memory from `values.yaml` accessed 2025-10-23 09:25:16 Thursday October 23 2025)
- **Key patterns include referencing shared secrets, base64 encoding, conditional creation, and URI construction.** (Relevant long-term memory from `values.yaml` accessed 2025-10-23 09:25:16 Thursday October 23 2025)

## Adding Secrets Using HashiCorp Vault and Helm

The most common method involves defining secrets in HashiCorp Vault and then referencing them within your Helm chart's `values.yaml` file.

**1. Add Secrets to HashiCorp Vault**

- **Access Vault:** You'll need to authenticate to HCP Vault. Based on your previous interactions (e.g., around 2025-10-23 09:44:23 Thursday October 23 2025), this typically involves setting the following environment variables:
  - `export VAULT_ADDR="https://fitfile-vault.vault.hashicorp.cloud"` (or your specific Vault instance address)
  - `export VAULT_TOKEN="<your-vault-token>"` (obtained from the HCP portal)
  - `export VAULT_NAMESPACE="admin/deployments/<deployment-key>"` (e.g., `admin/deployments/ff-c` or `admin/deployments/prod-1`)
- **Locate or Create the Secret Path:** Secrets are typically stored under a path structured like: `admin/deployments/<deployment-key>/secrets/<secret-group>`.
  - For example, for `thehyve` secrets in the `ff-c` deployment, the path is `admin/deployments/ff-c/secrets/thehyve`.
  - For `thehyve-mkuh` in `prod-1`, it's `admin/deployments/prod-1/secrets/thehyve-mkuh`.
- **Add/Update Secrets:** You can use either the Vault CLI or the Vault UI.

  **Using Vault CLI:**
  - To add or update secrets, use the `vault kv patch` command. This is generally preferred as it updates existing secrets without overwriting other keys.

    ```bash
    export VAULT_NAMESPACE="admin/deployments/ff-c" # Or the appropriate namespace
    vault kv patch -mount=secrets thehyve \
      your_secret_key="your-secret-value" \
      another_key="another-value"
    ```

    Replace `admin/deployments/ff-c`, `secrets`, `thehyve`, `your_secret_key`, `your-secret-value`, etc., with your specific values.

  **Using Vault UI:**
  1. Navigate to the Vault UI.
  2. Select the correct namespace (e.g., `admin/deployments/ff-c`).
  3. Go to "Secrets Engines," select the `secrets` mount.
  4. Navigate to the specific secret path (e.g., `thehyve`).
  5. Click on the secret, then click "Create new version +" to add or update key-value pairs.

**2. Reference Secrets in Helm Chart Values (`values.yaml`)**

Once secrets are in Vault, you need to reference them in your Helm chart's `values.yaml` file. This is typically done within the `extraEnvVars` section for direct environment variable injection, and also within a `VaultStaticSecret` definition for more complex transformations or when using VSO.

- **Location:** Helm chart values file (e.g., `ffnodes/fitfile/ff-c/values.yaml` or `central-services/thehyve_values.yaml`).
- **Referencing in `extraEnvVars`:**

```yaml
extraEnvVars:
# Example for an existing secret
- name: QCR_BUCKET
valueFrom:
secretKeyRef:
  name: thehyve # Name of the Kubernetes secret to be created by VSO
  key: qcr_bucket # Key within the Kubernetes secret that maps to the Vault secret
# Example for a new secret
- name: YOUR_NEW_SECRET_VAR
valueFrom:
secretKeyRef:
  name: thehyve # Name of the Kubernetes secret to be created by VSO
  key: your_new_secret_key # Key within the Kubernetes secret that maps to the Vault secret
```

- **Defining `VaultStaticSecret`:** This resource tells VSO how to fetch secrets from Vault and populate the Kubernetes secret. It's usually found within the `extraDeploy` section of your `values.yaml`.

  ```yaml
  extraDeploy:
    - apiVersion: secrets.hashicorp.com/v1beta1
      kind: VaultStaticSecret
      metadata:
        name: thehyve # This name becomes the Kubernetes secret name
        namespace: "{{ .Release.Namespace }}" # Or specify a fixed namespace
      spec:
        # Vault configuration
        namespace: admin/deployments/ff-c # The Vault namespace
        mount: secrets # The Vault secrets engine mount path
        path: thehyve # The path within the secrets engine
        type: kv-v2 # Vault secrets engine type
        hmacSecretData: true # Enable drift detection
        # Destination Kubernetes secret configuration
        destination:
          create: true
          name: thehyve # Name of the Kubernetes secret to create/update
        # Transformation rules
        transformation:
          # excludes: # Uncomment and define if needed
          #   - '.*' # Example: exclude all keys by default
          templates:
            # Map Vault secret key to Kubernetes secret key name
            qcr_bucket: # Key in the Kubernetes secret
              text: '{{ get .Secrets "qcr_bucket" }}' # Vault secret key name
            qcr_access_key_id:
              text: '{{ get .Secrets "qcr_access_key_id" }}'
            qcr_secret_access_key:
              text: '{{ get .Secrets "qcr_secret_access_key" }}'
            qcr_iam_role:
              text: '{{ get .Secrets "qcr_iam_role" }}'
            # Template for a new secret
            your_new_secret_key: # Key in the Kubernetes secret
              text: '{{ get .Secrets "your_new_secret_key" }}' # Vault secret key name
        # Rollout restart configuration
        rolloutRestartTargets:
          - kind: Deployment
            name: '{{ include "thehyve.fullname" . }}' # The deployment to restart
        refreshAfter: 10m # How often to check for secret updates
        vaultAuthRef: default # Reference to the Vault authentication method (e.g., Kubernetes auth)
  ```

**Key Configuration Points:**

- **`metadata.name`** in `VaultStaticSecret` (e.g., `thehyve`) will be the name of the Kubernetes secret.
- **`spec.destination.name`** should typically match `metadata.name`.
- **`spec.namespace`** (under `spec`) refers to the Vault namespace.
- **`spec.path`** refers to the path within the Vault secrets engine.
- **`spec.transformation.templates`** map Vault secret keys to keys in the resulting Kubernetes secret. The `text:` field uses Go template syntax to fetch secrets.
- **`spec.rolloutRestartTargets`** ensures that pods are restarted when secrets are updated to pick up the new environment variables.

**3. Deploy Changes**

- **Commit and Push:** After modifying the Helm chart values, commit your changes and push them to your Git repository.

  ```bash
  git add .
  git commit -m "feat: Add secrets for <your_secret_name>" # Follow conventional commit format
  git push
  ```

- **ArgoCD Sync:** ArgoCD will detect the changes in your Git repository and apply them to the cluster. This will typically trigger a rollout restart of the affected deployment(s) as defined in `rolloutRestartTargets`.

**4. Verify Secrets**

- **Check Kubernetes Secret:** Verify that the Kubernetes secret has been created or updated.

  ```bash
  kubectl get secret <secret-name> -n <namespace> -o yaml
  ```

  For example: `kubectl get secret thehyve -n thehyve-mkuh -o yaml`

- **Check Pod Environment Variables:** Exec into a pod and check if the environment variables are set.

  ```bash
  kubectl exec -n <namespace> deployment/<deployment-name> -- env | grep YOUR_SECRET_VAR
  ```

  For example: `kubectl exec -n thehyve-mkuh deployment/thehyve-mkuh -- env | grep QCR_`

- **Check VSO Logs:** If secrets are not appearing, check the logs of the Vault Secrets Operator pods for errors.

  ```bash
  kubectl get pods -n vault-secrets-operator-system
  kubectl logs -n vault-secrets-operator-system -c vault-secrets-operator <vso-pod-name>
  ```

By following these steps, you can securely add and manage secrets for your FITFILE cluster deployments. Let me know if you have any specific parts you'd like to elaborate on!
