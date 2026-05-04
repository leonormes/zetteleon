# Signals

Learn about the categories of telemetry supported by OpenTelemetry

The purpose of OpenTelemetry is to collect, process, and export signals. Signals are system outputs that describe the underlying activity of the operating system and applications running on a platform. A signal can be something you want to measure at a specific point in time, like temperature or memory usage, or an event that goes through the components of your distributed system that you’d like to trace. You can group different signals together to observe the inner workings of the same piece of technology under different angles.

OpenTelemetry currently supports [traces](https://app.heptabase.com/c16a6d60-49a6-4aec-9d1a-6161cbbe31a8/card/fdaa97ea-0490-4a11-9749-5ce178b144b9), metrics, logs and baggage. *Events* are a specific type of log, and *profiles* are being work on by the Profiling Working Group.

---

[Traces.md](Traces.md)

[Metrics.md](Metrics.md)

[Logs.md](Logs.md)

[Baggage.md](Baggage.md)

Source: <https://opentelemetry.io/docs/concepts/signals/>