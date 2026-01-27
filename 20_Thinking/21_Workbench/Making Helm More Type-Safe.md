---
captured: 2026-01-24T22:20:09+00:00 2026-01-24T22:20:09+00:00
created: 2026-01-24T22:20:13+00:00
modified: 2026-01-27T08:17:27+00:00
source: https://gemini.google.com/share/ed5c2a1cbb9a
status: processing
tags:
  - input
title: Helm YAML Advanced Features & Tricks
type: head
---

## Phase 1: Ingestion (The Stream)

> [!abstract] Context
> Created with Gemini

### Raw Output / Content

Helm is essentially a text-templating engine, it is notoriously prone to "stringly-typed" errors.

I am interested in making it more type and data oriented.

Is this possible with the yaml and golang templating combo? Maybe also consider the k8s API and static analyses tools?

Yes, it is entirely possible. While Helm will always be a text-templating engine at its core, you can wrap it in a "safety sandwich" of schemas, static analysis, and strict template logic to make it behave much more like a typed application.

To move away from "stringly-typed" errors, you need to validate the Input (Values), the Logic (Templates), and the Output (Manifests).

Here is the architectural stack to make Helm type-safe and data-oriented.

---

### 1. Input Safety: Native JSON Schema

This is the single most effective "type safety" feature in Helm 3, yet often ignored. You can enforce types, required fields, and constraints on your `values.yaml` natively.

Create a file named `values.schema.json` alongside your `Chart.yaml`. Helm will automatically use this to validate `helm install` or `helm upgrade` commands and fail immediately if the data doesn't match.

Example `values.schema.json`:

JSON

```json
{
"$schema": "http://json-schema.org/draft-07/schema#",
"properties": {
"replicaCount": {
  "type": "integer",
  "minimum": 1
},
"image": {
  "type": "object",
  "required": ["repository", "tag"],
  "properties": {
    "repository": { "type": "string" },
    "tag": { "type": "string", "pattern": "^v[0-9]+.[0-9]+" }
  }
},
"environment": {
  "type": "string",
  "enum": ["production", "staging", "dev"]
}
},
"required": ["image", "replicaCount"]
}
```

- Why this works: It stops "stringly" errors (like passing a string "true" instead of a boolean) before the template engine even starts.

### 2. Logic Safety: Strict Template Functions

Stop assuming values exist. Use Go template functions that force failures when data is missing or malformed.

- `required`: Fails the render if a value is nil or empty.
YAML

```yaml
# If .Values.legacySystem.apiUrl is missing, the build fails with this message.
apiUrl: {{ required "A legacySystem.apiUrl is required!" .Values.legacySystem.apiUrl }}
```

- `fail`: Allows you to implement custom logic checks and halt the build.
YAML

```yaml
{{- if and .Values.ingress.enabled (not .Values.ingress.host) -}}
 {{- fail "If ingress is enabled, you MUST provide a host" -}}
{{- end -}}
```

- `coalesce`: Useful for data-oriented defaults (handling null vs empty string correctly).

### 3. Output Safety: Static Analysis (The "Compiler")

Since Helm templates generate YAML, you need to validate that the generated YAML matches the Kubernetes API schema.

The Tool: `kubeconform`

This is the modern replacement for `kubeval`. It validates your rendered manifests against the actual Kubernetes OpenAPI specifications (schemas).

- Workflow:
Bash

```sh
helm template my-chart | kubeconform -strict -kubernetes-version 1.29 -summary
```

- What it catches:
- Misspelled keys (e.g., `servicePort` vs `port`).
- Invalid types (e.g., passing a number where a string is expected by K8s).
- Missing required K8s spec fields.

The Tool: `pluto` Helm won't tell you if you are using a Kubernetes API version that is deprecated (e.g., `extensions/v1beta1`). `pluto` checks your rendered templates against deprecated API versions.

### 4. Verification: Unit Testing as Code

Treat your chart like software. `helm-unittest` allows you to write test suites in YAML that assert the output without needing a cluster.

Example Test (`tests/deployment_test.yaml`):

YAML

```yaml
suite: test deployment
templates:
- deployment.yaml
tests:
- it: should match snapshot and have correct replicas
set:
  replicaCount: 3
asserts:
  - isKind: Deployment
  - equal:
      path: spec.replicas
      value: 3
  - matchSnapshot: {}
```

- This prevents "regressions" where a template change accidentally breaks a specific data path.

### 5. Integration: The Ultimate Check

The final step in a "data-oriented" pipeline is validating against the cluster itself without deploying.

- Server-side Dry Run:
Bash

```sh
helm install my-release ./my-chart --dry-run=server
```

Unlike a standard dry-run (which is client-side), this sends the manifests to the Kubernetes API server. The server verifies if it could apply them (checking webhooks, quotas, and specific cluster constraints) but stops short of persisting changes.

### Summary: The "Typed" Helm Pipeline

If you implement this pipeline, you effectively turn Helm into a typed build system:

| Step | Tool / Feature | Role |
| --- | --- | --- |
| Input | `values.schema.json` | Enforces strong types on user input. |
| Logic | `required` / `fail` | Enforces mandatory data presence. |
| Lint | `helm lint` | Checks basic Helm structure. |
| Test | `helm-unittest` | Verifies logic branches (If X then Y). |
| Build | `kubeconform` | Validates output against K8s API Schema. |
| Verify | `pluto` | Checks for deprecated K8s APIs. |

Would you like me to generate a strict `values.schema.json` template based on a specific set of parameters you typically use?

A slight complication in my gitops is that I use ArgoCD to handle the helm. Does this change anything

It changes the location of where you catch errors, but not the tools you use. In fact, it makes the "strict" approach even more vital.

In a manual Helm workflow, if you run `helm install` and it fails, you see the error immediately on your terminal. In GitOps (ArgoCD), if you push bad configuration, ArgoCD will attempt to sync, fail, and stick in a `SyncFailed` or `Degraded` state. You lose that immediate feedback loop.

To maintain a "type-safe" environment with ArgoCD, you must "Shift Left"—moving all those checks into your CI pipeline (e.g., GitHub Actions, GitLab CI) before the code ever reaches the branch that ArgoCD watches.

Here is how the architecture adapts for ArgoCD:

### 1. The CI Pipeline Becomes the "Compiler"

You cannot rely on ArgoCD to tell you if your types are wrong; you must block the Pull Request if the data is invalid.

Your CI process for any change to the Helm Chart (or the values files ArgoCD uses) should look like this:

1. Lint: Run `helm lint --strict`.
2. Unit Test: Run `helm-unittest` (verifies logic).
3. Render & Validate (The Critical Step):You must simulate what ArgoCD will do.
Bash

```sh
# Render the templates using the EXACT values file ArgoCD will use
helm template my-release ./charts/my-chart 
 -f ./envs/production/values.yaml 
 --include-crds 
> full-manifest.yaml
# Validate the output against K8s schemas
kubeconform -strict -summary full-manifest.yaml
```

4. Schema Check: If you added `values.schema.json` (as discussed previously), the `helm template` command above will automatically fail if your values in `./envs/production/values.yaml` violate the schema.

### 2. Validating the "Glue" (The ArgoCD Application)

In GitOps, your arguments (values) are often stored in the ArgoCD `Application` manifest itself. You need to treat this manifest as typed data too.

If you inline values like this:

YAML

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
spec:
source:
helm:
  values: |
    replicaCount: "three"  # <--- Stringly error! Should be int.
```

ArgoCD will accept this YAML because it is a valid ArgoCD object, even though it contains invalid Helm data.

The Fix:Avoid inlining complex values in the `Application` manifest. Instead, reference a strictly typed value file in your Git repository:

YAML

```yaml
spec:
source:
helm:
  valueFiles:
    - values.yaml # This file can be validated by your CI pipeline
```

### 3. Handling Secrets (The "Untyped" Danger)

A common pain point in GitOps is that secrets are often injected at runtime (e.g., via External Secrets or Vault), meaning your templates might be expecting a string but receive a nil/empty value during the CI check because the secret doesn't exist yet.

The Data-Oriented Fix:Use the `coalesce` function or "mock" values in your CI pipeline to ensure type safety without exposing real secrets.

- In Template:
YAML

```yaml
# Safe handling if the value is missing during dry-run
key: {{ required "ApiKey is needed" .Values.secrets.apiKey }}
```

- In CI (Mocking):Create a `ci-values.yaml` that mimics the structure of your secret values so `kubeconform` passes, without committing real credentials.

### 4. ArgoCD-Specific Validation

ArgoCD effectively runs `helm template` under the hood. If you use the `values.schema.json` method I mentioned earlier:

1. Strictness: ArgoCD will fail the Sync operation if the values violate the schema.
2. UI Feedback: The ArgoCD UI will display the schema validation error in the sync status (e.g., `Error: values.yaml: execution error at (root): replicaCount must be an integer`).

This is excellent because it prevents "bad data" from even attempting to apply to the cluster.

### Summary of Changes

| Feature | Standard Helm | Helm + ArgoCD |
| --- | --- | --- |
| Validation Trigger | You run `helm install` manually. | CI Pipeline runs validation on PR. |
| Feedback Loop | Instant (Terminal). | Delayed (ArgoCD UI)–unless you catch it in CI. |
| Value Storage | `values.yaml` or CLI flags. | Committed `values.yaml` files (Avoid inline values). |
| Schema Enforcement | Prevents installation. | Prevents Sync (Keeps cluster safe). |

Recommendation:Since you are using ArgoCD, `values.schema.json` is actually more valuable. It acts as a contract between your repository and the ArgoCD controller, ensuring ArgoCD never attempts to apply invalid configurations.

Would you like me to outline a GitHub Actions (or GitLab CI) step that specifically runs this "ArgoCD dry-run" check?

Yes. We use gitlab

Here is a robust, data-oriented GitLab CI pipeline configuration designed specifically to catch errors before they reach ArgoCD.

This pipeline acts as your "compiler". If this passes, you can be 99% confident that ArgoCD will successfully sync the application.

### The GitLab CI Configuration

You can include this in your `.gitlab-ci.yml`. It relies on a Docker image that contains `helm` and `kubeconform` (I have used a common community image, but you can build your own).

YAML

```yaml
stages:
- lint
- validate

variables:
# Point this to your chart directory
CHART_DIR: "./charts/my-app"
# Point this to the values file ArgoCD uses for production
PROD_VALUES: "./envs/production/values.yaml"
KUBERNETES_VERSION: "1.29.0"

# ---------------------------------------------------------
# STAGE 1: INPUT SAFETY (Schema & Syntax)
# ---------------------------------------------------------
helm_lint:
stage: lint
image: alpine/helm:3.14.0
script:
- echo "Checking Helm syntax and Schema compliance..."
# --strict fails on warnings
# This automatically checks values.schema.json if it exists!
- helm lint $CHART_DIR --strict --values $PROD_VALUES

# ---------------------------------------------------------
# STAGE 2: OUTPUT SAFETY (The "ArgoCD Simulator")
# ---------------------------------------------------------
kubeconform_check:
stage: validate
image:
name: ghcr.io/yannh/kubeconform:latest-alpine
entrypoint: [""]
before_script:
# We need Helm to render the template first
- apk add --no-cache helm
script:
- echo "Simulating ArgoCD render..."

# 1. Render the templates exactly as ArgoCD would
# We output to a single file 'manifests.yaml' to treat it as a data artifact
- helm template release-name $CHART_DIR -f $PROD_VALUES > manifests.yaml

- echo "Validating against Kubernetes $KUBERNETES_VERSION Schema..."

# 2. Run the Static Analysis
# -strict: Fail on any schema violation
# -ignore-missing-schemas: Useful if you use custom CRDs (optional)
# -schema-location: Pulls the official K8s schemas
- kubeconform 
    -kubernetes-version $KUBERNETES_VERSION 
    -strict 
    -summary 
    manifests.yaml
artifacts:
paths:
  - manifests.yaml
expire_in: 1 day
```

### Why This Works for Your Specific Constraints

#### 1. It Catches "Stringly" Errors Immediately

If you defined `replicaCount: { type: integer }` in your schema, but someone commits `"2"` (a string) in `values.yaml`:

- Result: The `helm lint` job fails immediately.
- ArgoCD Impact: ArgoCD never sees the bad commit.

#### 2. It Validates the Result, not just the Logic

Standard linting checks if the YAML syntax is valid. `kubeconform` checks if the Kubernetes Object is valid.

- Example: You accidentally misspell `targetPort` as `tagretPort`.
- Helm Lint: Passes (it is valid YAML).
- Kubeconform:Fails (it is not a valid Kubernetes Service spec).

#### 3. It Creates a Data Artifact

Notice I added an `artifacts` section to save `manifests.yaml`.

- This allows you to download the "compiled" manifest from GitLab UI to see exactly what would have been applied to the cluster. This is incredibly useful for debugging "why did ArgoCD change this?" without needing access to the cluster.

### A Note on Custom Resource Definitions (CRDs)

If your chart uses CRDs (like Prometheus `ServiceMonitor` or CertManager `Certificate`), `kubeconform` will fail because it doesn't know what those are.

You have two options:

1. Ignore them (Easier): Add `-ignore-missing-schemas` to the `kubeconform` command.
2. Validate them (Strict): You must pass the CRD schemas to kubeconform. This is harder to set up but provides 100% type safety.

Would you like a script that can auto-generate the initial `values.schema.json` from your current `values.yaml` file, so you don't have to write it by hand?

Yes

Here is the most efficient way to bootstrap your schema.

Since you want to move away from "stringly-typed" errors, do not write the schema from scratch. It is tedious and error-prone. Use a generator to create the baseline, then tighten the constraints manually.

I have provided two options: the "Standard Tool" way and a "Python Script" way (if you don't want to install Helm plugins).

### Option 1: The Helm Plugin (Recommended)

There is a community plugin called `helm-schema-gen` designed exactly for this.

1. Install the plugin:
Bash

```sh
helm plugin install https://github.com/karuppiah7890/helm-schema-gen.git
```

2. Generate the schema:Run this inside your chart directory:
Bash

```sh
helm schema-gen values.yaml > values.schema.json
```

### Option 2: The Python Script (No Plugin Required)

If you prefer not to install plugins or need to run this in a CI environment where you only have Python, use this script. It reads your `values.yaml` and outputs a Draft-07 JSON Schema.

Prerequisite:`pip install pyyaml`

Python

```py
import yaml
import json
import sys

def get_type(value):
if isinstance(value, bool): return "boolean"
if isinstance(value, int): return "integer"
if isinstance(value, float): return "number"
if isinstance(value, str): return "string"
if isinstance(value, list): return "array"
if isinstance(value, dict): return "object"
return "string" # Default fallback

def generate_schema(data):
schema = {"type": get_type(data)}

if schema["type"] == "object":
    schema["properties"] = {}
    # By default, we don't make fields required in the generated schema
    # because we don't know your business logic yet.
    for key, value in data.items():
        schema["properties"][key] = generate_schema(value)
        
elif schema["type"] == "array":
    if len(data) > 0:
        # Assumes all items in the list are the same type
        schema["items"] = generate_schema(data[0])
    else:
        schema["items"] = {}
        
return schema

try:
with open("values.yaml", "r") as f:
    values = yaml.safe_load(f)
    
full_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Generated Schema",
    generate_schema(values)
}

print(json.dumps(full_schema, indent=2))

except Exception as e:
print(f"Error: {e}", file=sys.stderr)
```

---

### Critical Next Step: Tighten the Screws

The script/plugin only sees what is currently there, not what is allowed. It generates a "loose" schema. To get the type-safety you want, you must edit the generated `values.schema.json` to add constraints.

3 Things to Change Immediately in the generated file:

1. Add `required` fields:The generator makes everything optional. You need to explicitly list which fields must exist.
JSON

```json
"image": {
 "type": "object",
 "required": ["repository", "tag"],  // <--- ADD THIS
 "properties": { ... }
}
```

2. Restrict `enums`:If you have an environment field, the generator sees a string. You should restrict it to allowed values.
- Change:`"type": "string"`
- To:`"enum": ["prod", "dev", "staging"]`
1. Constrain Numbers:
- Change:`"replicaCount": { "type": "integer" }`
- To:`"replicaCount": { "type": "integer", "minimum": 1 }`

Would you like to see how to add a "custom error message" to the schema so that when ArgoCD fails, it gives a human-readable explanation instead of a generic validation error?

## Phase 1: Ingestion (The Stream)

Tell me some of the advanced features of yamland what things can be done programmatically. I'm using helm and managing kuberenetes manifest and was interested in any quality of life tips and tricks

When managing Kubernetes manifests with Helm, you are often bridging the gap between static data and dynamic logic. YAML itself has "hidden" features that help reduce repetition, while Helm's templating engine (Go templates) provides the "programmatic" power.

Here are the advanced features and quality-of-life tricks to streamline your manifests.

---

## 1. YAML Advanced Features (The "DRY" Syntax)

These features are part of the YAML spec and work even without Helm, but they are incredibly useful in `values.yaml` files.

### Anchors (&) and Aliases ()

If you have multiple containers or jobs with the same environment variables or resources, don't copy-paste them.

- Anchor (`&`): Defines a block.
- Alias (``): References that block.
- Merge Key (`<<`): Injects the referenced block into the current map.

### Multi-line String "Chomping"

Kubernetes `ConfigMaps` or `Secrets` often store scripts. How you handle the trailing newline matters:

- `|` (Literal): Preserves newlines.
- `|—` (Strip): Removes all trailing newlines (cleaner for one-liners).
- `|+` (Keep): Preserves every single trailing newline.
- `>` (Folded): Replaces newlines with spaces (great for long labels or descriptions).

---

## 2. Programmatic Tricks in Helm

Helm uses the Go `text/template` engine. This is where you can do "coding" inside your YAML.

### Named Templates (Partials)

If you find yourself writing the same complex label block or selector in 5 different files, use `_helpers.tpl`.

YAML

```markdown
{{/ Define the block in _helpers.tpl /}}
{{- define "mychart.labels" -}}
app.kubernetes.io/name: {{ .Chart.Name }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end -}}

{{/ Use it in deployment.yaml /}}
metadata:
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
```

### Control Structures

You can use `if/else` and `range` (loops) to build manifests programmatically.

- Looping through maps:
	YAML

	```markdown
	env:
	{{- range $key, $val := .Values.extraEnv }}
	- name: {{ $key }}
	  value: {{ $val | quote }}
	{{- end }}
	```

- The `with` scope: Changes the `.` (dot) context to a specific sub-key to save typing.
	YAML

	```markdown
	{{- with .Values.image }}
	image: "{{ .repository }}:{{ .tag }}"
	imagePullPolicy: {{ .pullPolicy }}
	{{- end }}
	```

---

## 3. Quality of Life (QoL) Tips

### The Indentation Savior: Nindent Vs Indent

- Problem: When you include a template, the whitespace is usually wrong.
- Solution: Always use `nindent`. The "n" adds a newline before the content, allowing you to pipe it cleanly.
	- `{{- include "template". | nindent 8 }}`

### Mandatory Values with Required

Don't let a deployment fail silently because someone forgot a variable. Force it to fail during `helm install`.

YAML

```markdown
image:
  repository: {{ required "A valid image.repository is required!" .Values.image.repository }}
```

### Type Conversion and Defaulting

Helm allows you to provide defaults or change types on the fly:

- `{{ default "production".Values.env }}`: Uses "production" if `.Values.env` is empty.
- `{{.Values.replicas | int }}`: Ensures a value is treated as an integer.
- `{{.Values.config | toJson }}`: Converts a YAML map from your values file directly into a JSON string (great for ConfigMaps).

### Dry-Run & Debugging

Before applying, always use these to see what your "programmatic" YAML actually looks like:

- `helm install --debug --dry-run`: Renders templates and prints them without deploying.
- `helm lint`: Checks for syntax and best-practice errors.

Would you like me to create a specific `_helpers.tpl` example for a common task, such as dynamic environment variable generation?

Google Account

Leon Ormes

leonormes@gmail.com

---

## Phase 2: The Gate (4D Filter)

- [ ] Do: < 2 mins?
- [ ] Delegate: Who?
- [ ] Defer: Move to Hangar or SoT?
- [ ] Delete: Is this noise?

---

## Phase 5: The Scribe (#SAVESTATE)

- The Conflict:
- The Current State:
- The Next Test:
