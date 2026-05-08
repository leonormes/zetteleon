---
created: 2026-05-04T08:01:26+00:00
modified: 2026-05-08T12:53:38+00:00
title: Components !  Grafana Alloy documentation
---

## Components | Grafana Alloy Documentation

_Components_ are the building blocks of Alloy. Each component handles a single task, such as retrieving secrets or collecting Prometheus metrics.

Components are composed of the following:

[Arguments! Settings that configure a component..md](Arguments!%20Settings%20that%20configure%20a%20component..md)

[Exports! Named values that a component exposes to other components..md](Exports!%20Named%20values%20that%20a%20component%20exposes%20to%20other%20components..md)

Each component has a name that describes what that component is responsible for. For example, the `local.file` component is responsible for retrieving the contents of files on disk.

You specify components in the configuration file by first providing the component's name with a user-specified label, and then by giving arguments to configure the component.

```
discovery.kubernetes "pods" {
  role = "pod"
}

discovery.kubernetes "nodes" {
  role = "node"
}
```

You reference components by combining the component name with its label. For example, you can reference a `local.file` component labeled `foo` as `local.file.foo`.

The combination of a component's name and its label must be unique within the configuration file. Combining component names with a label means you can define multiple instances of a component as long as each instance has a different label value.

### Pipelines

Most arguments for a component in a configuration file are constant values, such as setting a `log_level` attribute to the quoted string `"debug"`.

You use _expressions_ to dynamically compute the value of an argument at runtime. You can use expressions to retrieve the value of an environment variable (`log_level = env("LOG_LEVEL")`) or to reference an exported field of another component (`log_level = local.file.log_level.content`).

You create a dependent relationship when a component's argument references an exported field of another component. A component's arguments now depend on another component's exports. The input of the component is re-evaluated whenever the exports of the components it references are updated.

The flow of data through the set of references between components forms a _pipeline_.

An example pipeline may look like this:

1. A `local.file` component watches a file that contains an API key.
2. A `prometheus.remote_write` component is configured to receive metrics and forward them to an external database using the API key from the `local.file` for authentication.
3. A `discovery.kubernetes` component discovers and exports Kubernetes Pods where metrics can be collected.
4. A `prometheus.scrape` component references the exports of the previous component, and sends collected metrics to the `prometheus.remote_write` component.

The following configuration file represents the pipeline.

```
// Get our API key from disk.
//
// This component has an exported field called "content", holding the content
// of the file.
//
// local.file will watch the file and update its exports any time the
// file changes.
local.file "api_key" {
  filename  = "/var/data/secrets/api-key"

  // Mark this file as sensitive to prevent its value from being shown in the
  // UI.
  is_secret = true
}

// Create a prometheus.remote_write component, which other components can send
// metrics to.
//
// This component exports a "receiver" value, which can be used by other
// components to send metrics.
prometheus.remote_write "prod" {
  endpoint {
    url = "https://prod:9090/api/v1/write"

    basic_auth {
      username = "admin"

      // Use the password file to authenticate with the production database.
      password = local.file.api_key.content
    }
  }
}

// Find Kubernetes pods where we can collect metrics.
//
// This component exports a "targets" value, which contains the list of
// discovered pods.
discovery.kubernetes "pods" {
  role = "pod"
}

// Collect metrics from Kubernetes pods and send them to prod.
prometheus.scrape "default" {
  targets    = discovery.kubernetes.pods.targets
  forward_to = [prometheus.remote_write.prod.receiver]
}
```

Source: <https://grafana.com/docs/alloy/latest/get-started/components/>
