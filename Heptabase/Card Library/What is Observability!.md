## What is Observability?

Observability lets you understand a system from the outside by letting you ask questions about that system without knowing its inner workings. Furthermore, it allows you to easily troubleshoot and handle novel problems, that is, “unknown unknowns”. It also helps you answer the question “Why is this happening?”

To ask those questions about your system, your application must be properly instrumented. That is, the application code must emit [Signals.md](Signals.md) such as [traces](https://app.heptabase.com/c16a6d60-49a6-4aec-9d1a-6161cbbe31a8/card/fdaa97ea-0490-4a11-9749-5ce178b144b9), [metrics](https://app.heptabase.com/c16a6d60-49a6-4aec-9d1a-6161cbbe31a8/card/4755c857-be20-43a5-9a9d-0a3f21191987), and [logs](https://app.heptabase.com/c16a6d60-49a6-4aec-9d1a-6161cbbe31a8/card/b95fd21c-e603-4145-b01c-1394318f44e9). An application is properly instrumented when developers don’t need to add more instrumentation to troubleshoot an issue, because they have all of the information they need.

[OpenTelemetry.md](OpenTelemetry.md) is the mechanism by which application code is instrumented to help make a system observable.