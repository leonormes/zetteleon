### Contrib Packages

The OpenTelemetry project maintains integrations with popular OSS projects which have been identified as important for observing modern web services. Example API integrations include instrumentation for web frameworks, database clients, and message queues. Example SDK integrations include plugins for exporting telemetry to popular analysis tools and telemetry storage systems.

Some plugins, such as OTLP Exporters and TraceContext Propagators, are required by the OpenTelemetry specification. These required plugins are included as part of the SDK.

Plugins and instrumentation packages which are optional and separate from the SDK are referred to as **Contrib** packages. **API Contrib** refers to packages which depend solely upon the API; **SDK Contrib** refers to packages which also depend upon the SDK.

The term Contrib specifically refers to the collection of plugins and instrumentation maintained by the OpenTelemetry project; it does not refer to third-party plugins hosted elsewhere.