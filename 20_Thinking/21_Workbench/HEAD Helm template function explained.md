---
captured: 2026-06-12T08:52:17+01:00 2026-06-12T08:52:17+01:00
created: 2026-06-12 07:52:20+00:00
modified: 2026-06-12 08:23:44+00:00
source: https://claude.ai/chat/07eb6366-0ccb-42c1-83be-9267fa2ed08d
status: processing
tags:
- input
title: HEAD Helm template function explained
type: head
permalink: llmeon/20-thinking/21-workbench/head-helm-template-function-explained
---

## Raw Output / Content

You

Explain helm template function to me.

---

Claude

There are actually two distinct things people call "helm template," so let me orient you first, then go deep on the one your phrasing ("function") most likely means.

- The `template` _action_—used _inside_ chart files, e.g. `{{ template "name". }}`. This is the "function" reading.
- The `helm template` _command_—a CLI subcommand that renders a chart locally.

I'll cover the action in depth (with its more important sibling, `include`), then the command briefly. Tell me if you meant the other emphasis.

---

### 1\. The Template Action (inside charts)

#### What it is

It's a built-in Go template action that runs a _named template_ and writes its output into the rendered manifest at that exact spot.

```yaml
{{ template "NAME" PIPELINE }}
```

- `"NAME"`—the named template to execute.
- `PIPELINE`—the scope/context handed to that template (almost always `.`).

#### Where Named Templates come From: Define

You declare reusable snippets with `define`, conventionally in `_helpers.tpl` (files prefixed with `_` are _never_ rendered as standalone manifests—they only hold helpers):

```yaml
{{- define "mychart.labels" -}}
app.kubernetes.io/name: {{ .Chart.Name }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end -}}
```

Then invoke it:

```yaml
metadata:
  labels:
    {{- template "mychart.labels" . }}
```

#### The why behind Two Non-obvious Behaviours

Names are global. A named template defined _anywhere_ in the chart—including subcharts—lives in one shared namespace. That's why the convention is to prefix names with the chart name (`mychart.labels`): it prevents a subchart silently clobbering your definition.

Scope is everything. The `.` you pass becomes `.` _inside_ the template. If you write `{{ template "mychart.labels" }}` with no context, then `.Chart.Name` inside it resolves against `nil` and rendering fails. This is the single most common beginner trap—the helper "mysteriously" can't see `.Release` or `.Values` because you forgot to pass scope.

---

### 2\. The Critical Principle: Template Vs Include

This is the part that actually matters in real charts.

- `template` is an action, not a function. It writes _directly to output_ and returns nothing. Therefore it cannot go through a pipe.

```yaml
# ❌ Parse error — there's no value to pipe
{{ template "mychart.labels" . | indent 4 }}
```

- `include` is a function Helm added that does the same job but returns the output as a string, so it _can_ be piped:

```yaml
# ✅ Works
{{- include "mychart.labels" . | nindent 4 }}
```

#### The Mental Model

- `template "x" $ctx` → _"paste this here, now, raw."_
- `include "x" $ctx` → _"hand me the result as a value I can shape."_

#### Why This Dominates Real Charts

YAML is whitespace-sensitive, so a helper's output almost always needs indenting to slot in correctly. Only `include` can feed `indent` / `nindent`. That's why the Helm docs recommend `include` over `template`, and why you'll see `{{- include "…". | nindent 4 }}` everywhere in production charts. `template` survives mainly in older charts and trivial cases where no indentation is needed.

(`nindent N` = prepend a newline, then indent every line by N spaces. The `{{-` / `-}}` "chomps" trim surrounding whitespace, which is why they cluster around these helper calls.)

---

### 3\. The Helm Template Command (the other meaning)

Renders a chart's templates locally and prints the resulting Kubernetes YAML to stdout:

```bash
helm template my-release ./mychart
```

- Client-side only—it does _not_ install anything and, by default, does _not_ query your cluster (so the `lookup` function returns empty and capabilities fall back to defaults).
- Its main uses: debugging what a chart will actually produce, and GitOps/CI pipelines where you render manifests as an artefact. This is directly relevant to ArgoCD—Argo effectively does this rendering for Helm-sourced apps before applying.

---

### Your next Action (micro-step)

Don't "study helm templating." Just get a sandbox you can _see_ working—`helm create` ships a `_helpers.tpl` full of real `define` / `include` examples:

Step 1—run this one command:

```bash
cd /tmp && helm create scratch
```

Step 2—once that exists, render it and watch `include` resolve the labels block:

```bash
helm template scratch ./scratch | grep -A3 'app.kubernetes.io'
```

Then open `scratch/templates/_helpers.tpl` and you'll recognise every concept above in the wild. Want me to walk through what that generated `_helpers.tpl` is doing, line by line?

---

You

How does the cli command version actually work

---

Claude

Good question—the real mechanics are more interesting (and more useful) than the docs let on. Here's what's actually happening when you type `helm template./chart`.

### The One Secret that Explains Everything

`helm template` is not its own engine. Under the hood it instantiates the _same install action_ that `helm install` uses, but flips two switches:

- `ClientOnly = true` → never talk to the cluster
- `DryRun = true` → render, but stop before writing anything

…then it prints the rendered manifests to stdout instead of persisting them.

The principle: rendering is just a _prefix_ of installing. Install and template share ~90% of the same code path; `template` simply short-circuits right before the point where Helm would POST objects to the API server. Once you internalise that, every quirk below stops being a quirk.

### The Pipeline, in order

1\. Load the chart
Helm parses the chart into an in-memory object—`Chart.yaml`, `values.yaml`, everything under `templates/`, plus subcharts in `charts/`. Files prefixed with `_` are flagged as partials (helpers), not output candidates.

2\. Coalesce the values
This is where `.Values` is built, by merging sources in ascending precedence:

- the chart's own `values.yaml` (lowest)
- subchart values, scoped under their chart name
- any `-f / --values` files you pass
- `--set` / `--set-string` / `--set-json` (highest)

Parent values flow _down_ into subcharts; subcharts can't reach _up_. That asymmetry is deliberate—it keeps a subchart from depending on its parent's internals.

3\. Build the render context (the `.` object)
Helm assembles the top-level scope: `.Values`, `.Chart`, `.Release`, `.Capabilities`, `.Files`, `.Template`. The critical bit is that, with no cluster connection, several of these are synthesised from defaults:

- `.Release.Name` defaults to `release-name` (or your arg), `.Revision` = 1, `.IsInstall` = true.
- `.Capabilities.KubeVersion` is a default version baked into your Helm binary, _not_ your cluster's—unless you pass `--kube-version`. Same for `.Capabilities.APIVersions` (override with `-a/--api-versions`).

4\. Render through the engine
Each template file is compiled with Go's `text/template`, all sharing one namespace (hence global `define` names—see last turn). The function set is Sprig plus a small Helm-specific layer: `include`, `tpl`, `required`, `lookup`, and the `toYaml` / `fromYaml` family.

5\. Post-process

- Templates that render to nothing (whitespace only) are dropped—that's how `{{ if }}` guards make whole files disappear.
- Output is concatenated with `---` separators and `# Source: chart/templates/x.yaml` comment headers.
- Hook-annotated resources are _rendered_ into the output, but never executed—there's no apply step. `--no-hooks` removes them; `-s/--show-only file.yaml` narrows output to one template.

6\. Print to stdout—done. Nothing touched your cluster, no state was stored.

### The Principle that Will Bite You (and It's Relevant to ArgoCD)

Because step 3 runs offline, `lookup` always returns empty during `helm template`. Any chart logic shaped like _"if this Secret already exists, reuse it"_ silently evaluates as _"it doesn't exist."_ Combined with the _guessed_ `.Capabilities.KubeVersion`, this means `helm template` can produce different YAML than a live `helm install`.

This matters directly for you: ArgoCD renders Helm sources essentially this way (client-side template, then apply). So a chart that relies on `lookup` or real cluster capabilities will behave differently under Argo than under an interactive `helm install`—a classic GitOps footgun. `--kube-version` / `--api-versions` exist precisely to close part of that gap in CI.

### Your next Action (micro-step)

See the offline-context effect with your own eyes in one command—compare the default capabilities against a forced one:

Step 1—run this:

```bash
cd /tmp && helm create scratch && helm template scratch ./scratch --kube-version 1.99.0 | grep -i 'kube\|version' | head
```

You won't see much yet because the default chart doesn't _use_ capabilities—which is exactly the point of step 2.

Step 2—add one line to prove the context is live. Open `scratch/templates/serviceaccount.yaml` and drop this at the top, then re-render:

```yaml
# Rendered against K8s {{ .Capabilities.KubeVersion.Version }}
```

Watch your injected `1.99.0` appear in the output—that's the synthesised context from step 3, made visible.

Want me to show how ArgoCD's repo-server invokes this same path, so you can predict exactly when Argo and local Helm will diverge?