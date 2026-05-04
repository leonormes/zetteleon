## Phase 3: Container Orchestration with Kubernetes

1. Kubernetes Networking:

   - Pod-to-Pod Communication: Learn how pods communicate with each other, including on the same and different nodes. Understand the role of `kube-proxy` and services.

      - *Practical Learning*: Examine the networking configuration of a pod in a Kubernetes cluster. Trace packet flows between pods.

   - Network Policies: Configure network policies to control traffic flow within the cluster.

      - *Practical Learning*: Implement Kubernetes network policies to restrict traffic between namespaces and pods.

   - Calico Policies: Explore Calico, an open-source project that simplifies, scales, and secures container and Kubernetes networks.

      - *Practical Learning*: Set up a cluster with Calico and follow the Calico policy lab.

2. Kubernetes Security:

   - Pod Security Policies: Understand how PSPs can control the capabilities and security settings of pods.

   - Observability: Learn how to monitor and secure a Kubernetes cluster. Understand how to collect logs and set up alerts.

      - *Practical Learning*: Explore the observability features of your Kubernetes implementation, using metrics, logs, and traces.