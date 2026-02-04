---
captured: "2026-02-04T07:02:42+00:00 2026-02-04T07:02:42+00:00"
created: 2026-02-04T07:02:45+00:00
modified: 2026-02-04T07:27:50+00:00
source: "https://gemini.google.com/share/7a9d3591cbb8"
status: "processing"
tags: ["input"]
title: Data Structures vs. Data Modeling
type: "head"
---

## Raw Output / Content

I'm a developer and always looking for ways to improve my understanding and mental models. I recently took an interest in Linus torvalds quote about good programmers worry about data. The concept seemed appealing so I found out more about the idea and the high level concept. Moving complexity to the data structures. But when I started to read about it all I found was detail about linked lists and hashtables. I think I am conflating 2 things. I am thinking about objects we use in typescript as structuring or organising data that I am dealing with in software. Essentially doing the data normalisation DBA people do in dB. What is the distinction and what was Linus referring to

It is very common to feel a disconnect here. You are spotting a subtle but critical distinction between Data Structures (the containers) and Data Modelling (the shape and relationships).

When Linus Torvalds said, _"Bad programmers worry about the code. Good programmers worry about data structures and their relationships,"_ he was effectively bridging the two concepts you are currently separating.

Here is the breakdown of the distinction and how to reconcile it with your TypeScript and "DBA-style" thinking.

### The Distinction: Container vs. Schema

You are currently seeing these as two separate worlds:

1. The "Computer Science" View (Low-Level):
	- Focus: Efficiency, memory layout, algorithmic complexity (vs).
	- Examples: Linked lists, hash tables, binary trees, arrays.
	- Goal: How do I insert, retrieve, or sort this data quickly?
2. The "Domain" View (High-Level / Your View):
	- Focus: Normalisation, business logic, entity relationships, validity.
	- Examples: TypeScript Interfaces, SQL Schemas, JSON objects.
	- Goal: Does this data accurately represent the real world?

### What Linus Actually Meant

Linus works in C (Linux Kernel, Git). In C, the "container" and the "schema" are often tightly coupled. However, his philosophy applies perfectly to high-level languages like TypeScript.

He was not just telling people to use Hash Maps instead of Arrays. He was saying that if you design the shape of your data correctly, the code required to manipulate it disappears.

If your code is full of `if` statements, special cases, and error checking, it is usually because the data structure (the shape of your object) allows for invalid states, forcing the code to handle the complexity.

### The Bridge: "Making Illegal States Unrepresentable"

This is where your "DBA thinking" meets Linus's "Data Structure" thinking. In TypeScript, "worrying about data" means using the type system to structure data so that logic becomes unnecessary.

#### Example: The "Bad" Programmer (Worrying about Code)

Here, the data structure is generic and loose. The complexity lives in the functions (the code).

#### Example: The "Good" Programmer (Worrying about Data)

Here, we structure the data using a Discriminated Union. We have moved the complexity out of the `render` function and into the _definition_ of the data.

### Summary of the Concept

1. Complexity Conservation: Complexity has to live somewhere. You can either spread it out across thousands of lines of procedural code (logic), or you can bake it into the data definitions (structure).
2. Table-Driven Methods: This is a classic example of Linus's philosophy. Instead of writing a massive `switch` statement or `if/else` chain (logic), you put the decisions into an array or object (data) and look them up.
3. Git Example: Linus designed Git. Git is essentially a Directed Acyclic Graph (DAG) of objects. The code for Git is complex, but it is entirely subservient to the data model. Once the data model (commits pointing to trees pointing to blobs) was decided, the code just naturally followed.

### Your "DBA" Intuition is Correct

You mentioned doing "data normalisation." This is exactly what Linus advocates, just applied to memory rather than disk storage.

- DBA: "Don't store the user's address in the Order table; reference the User ID." (Data consistency).
- Linus: "Don't store the 'is\_valid' flag alongside the data; store valid data in a separate list or structure that implies validity."

Both approaches ensure that the state of the system is captured by the structure of the data, not by the flow of the code.

### How to Apply This

When you are about to write a complex function with many conditionals:

- Stop.
- Look at the arguments (the data) coming in.
- Ask: "Can I change the shape of this object so that these conditions are impossible?"
- Ask: "Can I use a lookup table (object/map) instead of a switch statement?"

Would you like to see a specific example of refactoring a "code-heavy" TypeScript function into a "data-heavy" one?

What about helm templating if else hell for handling Boolean flags in a deployment

This is a fantastic application of the concept. Helm templates are notoriously prone to "logic creep," where the template (the code) becomes a tangled mess of Go template logic `{{ if.Values.foo }}`, obscuring the actual Kubernetes manifest (the data) you are trying to produce.

Applying Linus's "worry about data" philosophy to Helm completely changes how you structure your `values.yaml`.

Here is how you move from "If/Else Hell" (worrying about code) to "Data-Driven Templates" (worrying about data).

### The Anti-Pattern: Boolean Flags (Logic-Heavy)

The common mistake is treating `values.yaml` as a switchboard of on/off toggles, forcing the template to hold the intelligence of _what to do_ when a switch is flipped.

The "Bad" Data Structure (`values.yaml`):

The "Bad" Code (Template):

Why this fails the Linus test:

1. High Complexity: Every new feature requires modifying the template (the code).
2. Hardcoded Logic: The template "knows" exactly what the New Relic image is. You cannot easily change the sidecar image without editing the template logic or adding _yet another_ specific parameter.

---

### The Solution: Iteration over Definitions (Data-Heavy)

To fix this, we move the complexity into the data structure. Instead of flags that _trigger_ sidecars, we simply define a list of sidecars.

The "Good" Data Structure (`values.yaml`):

The "Good" Code (Template):

Why this works:

- Zero Logic: The template contains no `if` statements regarding specific features.
- Extensible: You can add 50 different sidecars in `values.yaml` without changing a single line of the template.
- Unrepresentable States: You cannot have a flag `enableNewRelic: true` but forget to define the image configuration, because the configuration _is_ the enablement.

### Scenario 2: Environment Variables (The "Prod" Flag Trap)

A classic mistake is using an `isProduction` flag to determine environment variables.

The Logic Approach (Bad):

The Data Approach (Good):You treat the environment configuration as pure data. The template should not know what "Production" is. It should only know how to render a list of variables.

values-production.yaml:

values-dev.yaml:

Template:

### The Mental Shift

To apply the "Good Programmer" mindset to Helm:

1. Stop writing "Recipes": Do not write templates that look like: "If user wants X, then add Y line of text."
2. Start writing "Printers": Write templates that look like: "Here is a list of generic containers/volumes/env-vars provided by the user; print them all."
3. Genericise the Concepts: Instead of `enablePrometheus`, think `extraAnnotations`. Instead of `addDebugVolume`, think `extraVolumes`.

You are essentially normalising the data structure of your deployment so the "code" (the template) can remain static and simple.

Would you like me to show you how this applies to "Library Charts" (a common Helm pattern) which essentially acts as the shared schema definition for this data?

Yes

Here is how Helm Library Charts function as the ultimate "Data Normalisation" tool in the Kubernetes world.

If you think of your microservices as rows in a database, a Library Chart is the Table Definition (Schema). It forces all your services to adhere to a shared structure, meaning the individual service charts become almost pure data.

### The Analogy: TypeScript Classes

Since you know TypeScript, think of it this way:

- Standard Helm Pattern: Copy-pasting the same `class` definition into 50 different files, changing values slightly in each.
- Library Chart Pattern: Defining the `class` once in a shared package. Your 50 services just instantiate that class with their specific arguments.

---

### The Architecture: Separating Logic from Data

In this model, we separate the roles explicitly:

1. The "Code" (Library Chart): Maintained by the Platform Team. Contains all the complex logic, loops, and `if/else` structures.
2. The "Data" (App Chart): Maintained by the Developer. Contains almost no templates, just a `values.yaml` file (the data).

#### 1\. The "Code" (The Library)

_File: `charts/my-common-lib/templates/_deployment.yaml`_

This is where the complexity lives. It is a reusable function (template) that expects data in a specific shape.

#### 2\. The "Data" (The App)

_File: `charts/payment-service/values.yaml`_

Notice there is zero logic here. It is just the "mental model" of the application.

_File: `charts/payment-service/templates/deploy.yaml`_

The application's template file becomes a simple one-line invocation. It effectively says "Render the Common Deployment using my data."

### Why This Satisfies the "Linus Test"

1. Complexity is hidden: The application developer (User) does not need to worry about correct YAML indentation, Kubernetes API versions, or the syntax for iterating over environment variables. They just provide the data.
2. Single Source of Truth: If you (the "DBA" / Platform Engineer) want to change how deployments work (e.g., add a default security context to _all_ containers), you update the Library Chart (the schema). You do not touch the data (the apps).
3. Data Normalisation: You have forced all 50 microservices to use the exact same data structure for `env` vars, `images`, and `replicas`. You have "normalised" the deployment model across your organisation.

### The "DBA" Twist: JSON Schema Validation

To fully complete your mental model of "DBA data normalisation," Helm has a feature called `values.schema.json`.

Just as a database rejects an `INSERT` if the data types are wrong, you can add a JSON Schema to your chart to reject a `helm install` if the `values.yaml` structure is invalid.

Example `values.schema.json`:

If a developer tries to deploy with a tag "latest" instead of "v1.0.0", Helm (the engine) rejects it before it even hits the template logic.

This is the pinnacle of "Worrying about Data." You aren't writing code to check if the tag starts with 'v'; you are defining a data constraint that makes an invalid tag unrepresentable.

Would you like to look at how this philosophy applies to application state in Redux/React (if you do frontend work), or perhaps stick to the backend/infrastructure side?

I have 50 seperate clusters with 50 values.yaml. I want to keep them all aligned with the main features. A new common feature would go on the base chart. But then I would need to update all 50 values with similar overrides that seems heavy handed. What are alternatives

This is the classic "N+1 Update Problem." You have normalised your logic (templates) using the Library Chart, but your data (values.yaml) is still de-normalised. You are repeating the same "common" data 50 times.

To solve this using the "Good Programmer" mental model, we need to introduce Hierarchical Data. You need a way to define "Global Data" that applies to everyone, and "Specific Data" that applies to the cluster.

Here are the three standard ways to solve this, ranked from "Native Helm" to "Industry Standard Wrapper."

### 1\. The "Smart Defaults" Approach (Native Helm)

Best for: When the "new feature" behaves the same for 90% of clusters.

The most strictly "Linus" approach is to ask: _Why do I need to add overrides if they are similar?_

If you are adding a feature to the Base Chart, you should set the default values inside the Base Chart's `values.yaml`.

- Scenario: You add a "Log Shipper" sidecar to the Base Chart.
- Bad way: Leave Base Chart `values.yaml` empty. Update 50 cluster `values.yaml` files to add `logShipper: enabled: true`.
- Good way: Update Base Chart `values.yaml` to `logShipper: enabled: true`.
- Result: All 50 clusters inherit this immediately upon their next upgrade. You only touch the `values.yaml` of the 2 clusters that _should not_ have it (exception-based config).

The Data Model:

### 2\. The "Helmfile" Approach (Layering)

Best for: When you need a shared config file that lives _outside_ the chart (e.g., usually a repo of config).

Helm alone allows only one `values.yaml` by default (unless you pass multiple `-f` flags manually). Helmfile is a standard wrapper tool that automates passing multiple values files. It allows you to "compose" your data.

You create a file structure like this:

Your `helmfile.yaml` looks like this:

When you run the deploy, Helmfile merges them. If you add a new feature, you just update `common.yaml` once. All 50 clusters pick it up.

### 3\. The "Kustomize" Approach (Patching)

Best for: If you are using GitOps (ArgoCD or Flux).

If you use ArgoCD, you can avoid Helm wrappers and use Kustomize to "patch" your Helm charts. This separates the "Base" definition from the "Overlays" completely.

Structure:

In this model, your "Base" is the single source of truth for the common configuration. The clusters just "subscribe" to the base.

### Summary: Which One Fits You?

My Recommendation:Start with Option 1. If you control the Base Chart, put the "heavy" configuration in the Base Chart's `values.yaml` as a default. Make your 50 cluster files "sparse"—containing _only_ the diffs (like hostnames and replica counts).

Does your current Base Chart have a `values.yaml`, or is it mostly empty?

Google Account

Leon Ormes

leonormes@gmail.com
