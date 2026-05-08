---
created: 2026-05-04T08:01:26+00:00
modified: 2026-05-08T12:53:45+00:00
title: This makes OpenTelemetry a cross-cutting concern - a piece of software which is mixed into many o
---

This makes OpenTelemetry a [cross-cutting concern](https://en.wikipedia.org/wiki/Cross-cutting_concern) - a piece of software which is mixed into many other pieces of software in order to provide value. Cross-cutting concerns, by their very nature, violate a core design principle–separation of concerns. As a result, OpenTelemetry client design requires extra care and attention to avoid creating issues for the codebases which depend upon these cross-cutting APIs.
