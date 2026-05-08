---
created: 2026-05-04T08:01:26+00:00
modified: 2026-05-08T12:53:44+00:00
title: Semantic Conventions
---

## Semantic Conventions

The Semantic Conventions define the keys and values which describe commonly observed concepts, protocols, and operations used by applications.

Semantic Conventions are now located in their own repository: <https://github.com/open-telemetry/semantic-conventions>

Both the collector and the client libraries SHOULD autogenerate semantic convention keys and enum values into constants (or language idiomatic equivalent). Generated values shouldn't be distributed in stable packages until semantic conventions are stable. The [YAML](https://github.com/open-telemetry/semantic-conventions/tree/main/model) files MUST be used as the source of truth for generation. Each language implementation SHOULD provide language-specific support to the [code generator](https://github.com/open-telemetry/build-tools/tree/main/semantic-conventions#code-generator).

Additionally, attributes required by the specification will be listed [here](https://opentelemetry.io/docs/specs/otel/semantic-conventions/)
