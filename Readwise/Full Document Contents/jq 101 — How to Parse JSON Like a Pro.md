---
created: 2026-03-14T09:50:12+00:00
modified: 2026-03-14T11:09:30+00:00
tags: [articles]
title: jq 101 — How to Parse JSON Like a Pro
---

## Jq 101—How to Parse JSON Like a Pro

![rw-book-cover](https://miro.medium.com/v2/resize:fit:1024/1*7V6pHPpO7r4ivO5DgpCJ4g.png)

### Metadata

- Author: [[Rafael Umbelino]]
- Full Title: jq 101—How to Parse JSON Like a Pro
- Category: articles
- Summary: jq is a powerful tool to easily filter and transform JSON data from cloud platforms like AWS and Azure. It helps avoid slow manual checks and complex scripts by processing JSON right in the command line. Learning jq makes working with cloud data faster and more efficient for DevOps engineers.
- URL: <https://medium.com/@odinumbelino/jq-101-how-to-parse-json-like-a-pro-a883ca08b3f9>

### Full Document

![](https://miro.medium.com/v2/resize:fit:700/1*7V6pHPpO7r4ivO5DgpCJ4g.png)A dark-themed digital illustration of a large blue funnel labeled "jq" in the center. At the top, a chaotic stream of colorful JSON fragments: braces, brackets, keys, and sample fields like IDs and regions—flows downward into the funnel. At the bottom, a small, clean stream of neatly formatted data cards emerges, showing simplified fields such as a name and an ID, visually representing raw JSON being filtered and structured into concise output.

#### JSON in DevOps and Cloud Engineering

JSON (JavaScript Object Notation) is the de facto data format for APIs, cloud services, and infrastructure tooling. If you work with cloud platforms, you are already working with JSON—whether you realize it or not.

Two concrete examples:

Amazon Web Services (AWS)—The AWS CLI returns JSON for nearly every command (aws ec2 describe-instances, aws iam list-roles). Infrastructure state, policies, and event logs are JSON documents.

Microsoft Azure (Azure)—Azure CLI (az vm list, az resource show) outputs JSON by default. ARM templates and many REST APIs are JSON-based.

If you cannot efficiently filter, transform, and extract data from JSON, you will:

- Pipe everything to grep (fragile)
- Manually inspect large outputs (slow)
- Write unnecessary scripts in Python (overkill)

jq solves this.

It is a lightweight, composable JSON processor designed for CLI workflows. Think of it as sed/awk for structured data.

We will be utilizing the Car API (<https://carapi.app/api>) since it's readily available and will give us actual data we can play with.

##### Installation

macOS

```
brew install jq  

```

Ubuntu / Debian

```
sudo apt update  
sudo apt install jq -y  

```

RHEL / CentOS / Fedora

```
sudo dnf install jq -y  

```

Windows

```
choco install jq  

```

Or download the binary from the official repository and add it to your PATH.

Verify:

```
jq --version  

```

##### Basic Usage

Pretty-print JSON

```
curl -s https://carapi.app/api/makes | jq  

```

`jq` automatically formats JSON in a readable structure.

Select a Field

```
curl -s https://carapi.app/api/makes | jq '.data'  

```

- `.` → root object
- `.data` → access key

Equivalent mental model:

```
{ "data": [...] }  

```

Array Indexing

```
curl -s https://carapi.app/api/makes | jq '.data[0]'  

```

Extract Specific Fields

```
curl -s https://carapi.app/api/makes | jq '.data[] | {id, name}'  

```

Key principles:

- `.data[]` → iterate over array
- `{}` → construct new JSON object
- `|` → pipe operator (compose transformations)

This is the core pattern used when parsing AWS/Azure CLI output.

##### Real Examples (Using Car API)

We'll use:

```
curl -s "https://carapi.app/api/makes?year=2020"  

```

1. Extract Only Make Names

```
curl -s "https://carapi.app/api/makes?year=2020" \  
| jq -r '.data[].name'  

```

- `-r` → raw output (no quotes)
- `.data[]` → iterate
- `.name` → select property

Equivalent AWS use case:

```
aws ec2 describe-instances | jq -r '.Reservations[].Instances[].InstanceId'  

```

Same structural principle: navigate nested arrays → extract field.

#### Get Rafael Umbelino's Stories in Your Inbox

Join Medium for free to get updates from this writer.

Subscribe

Subscribe

2. Filter Results (Select Specific Make)

```
curl -s "https://carapi.app/api/makes?year=2020" \  
| jq '.data[] | select(.name == "Ford")'  

```

`select()` is one of the most important jq functions.

Azure equivalent:

```
az vm list | jq '.[] | select(.location == "eastus")'  

```

Filtering JSON in-place without external scripting.

1. Count Results

```
curl -s "https://carapi.app/api/makes?year=2020" \  
| jq '.data | length'  

```

Count array elements.

Cloud equivalent:

```
aws iam list-users | jq '.Users | length'  

```

Operationally useful for audits and reporting.

4. Transform Output Into Custom Structure

```
curl -s "https://carapi.app/api/makes?year=2020" \  
| jq '.data[] | {name: .name, id: .id}'  

```

You reshape JSON to match your desired schema.

Critical when:

- Feeding data into Terraform
- Generating reports
- Transforming API output into monitoring inputs

5. Sort Results

```
curl -s "https://carapi.app/api/makes?year=2020" \  
| jq '.data | sort_by(.name) | .[].name'  

```

Sorting is essential when deterministic output matters (e.g., CI pipelines).

##### Jq Patterns You Must Master

These are the most used patterns in cloud engineering:

- `.key`
- `.array[]`
- `select()`
- `length`
- `map()`
- `sort_by()`
- `{ new:.old }`
- `|` (composition)

If you understand these, you can parse 90% of AWS/Azure CLI output.

##### Recap

- JSON is foundational in modern cloud systems.
- AWS CLI and Azure CLI output JSON by default.
- `jq` is the fastest way to parse and manipulate that output.
- Mastering array traversal and `select()` is critical.
- Transforming JSON inline avoids writing unnecessary scripts.

Most engineers only _use_ JSON.

Strong engineers manipulate it confidently from the CLI.

Practice `jq` daily:

- Pipe every AWS/Azure CLI command through it.
- Rewrite manual inspections as filters.
- Replace `grep` with structured parsing.

Fluency comes from repetition.

`jq` is not optional in modern DevOps.

If you found this useful, follow me on LinkedIn—I write practical, no-BS crash courses for DevOps engineers who want real leverage.
