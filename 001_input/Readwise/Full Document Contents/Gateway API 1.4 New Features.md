---
aliases: []
confidence: 
created: 2025-12-08T07:34:19Z
epistemic: 
last_reviewed: 
modified: 2025-12-08T11:11:57Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [articles]
title: Gateway API 1.4 New Features
type: 
uid: 
updated: 
---

## Gateway API 1.4: New Features

![rw-book-cover](https://kubernetes.io/icons/icon-128x128.png)

### Metadata
- Author: [[Kubernetes – Production-Grade Container Orchestration]]
- Full Title: Gateway API 1.4: New Features
- Category: #articles
- Summary: Gateway API v1.4.0 adds new features like BackendTLSPolicy for secure connections, supportedFeatures for better status reporting, and experimental external authentication for HTTPRoutes. It also introduces the Mesh resource for service mesh settings and default Gateways to simplify route configuration. These updates improve security, usability, and flexibility for Kubernetes Gateway users.
- URL: <https://kubernetes.io/blog/2025/11/06/gateway-api-v1-4/>

### Full Document

![Gateway API logo](https://kubernetes.io/blog/2025/11/06/gateway-api-v1-4/gateway-api-logo.svg)Gateway API logo

Ready to rock your Kubernetes networking? The Kubernetes SIG Network community presented the General Availability (GA) release of Gateway API (v1.4.0)! Released on October 6, 2025, version 1.4.0 reinforces the path for modern, expressive, and extensible service networking in Kubernetes.

Gateway API v1.4.0 brings three new features to the *Standard channel* (Gateway API's GA release channel):

- **BackendTLSPolicy for TLS between gateways and backends**
- **`supportedFeatures` in GatewayClass status**
- **Named rules for Routes**

and introduces three new experimental features:

- **Mesh resource for service mesh configuration**
- **Default gateways** to ease configuration burden\*\*
- **`externalAuth` filter for HTTPRoute**

#### Graduations to Standard Channel

##### Backend TLS Policy

GEP-1897: [BackendTLSPolicy](https://github.com/kubernetes-sigs/gateway-api/issues/1897)

[BackendTLSPolicy](https://gateway-api.sigs.k8s.io/api-types/backendtlspolicy) is a new Gateway API type for specifying the TLS configuration of the connection from the Gateway to backend pod(s). . Prior to the introduction of BackendTLSPolicy, there was no API specification that allowed encrypted traffic on the hop from Gateway to backend.

The `BackendTLSPolicy` `validation` configuration requires a hostname. This `hostname` serves two purposes. It is used as the SNI header when connecting to the backend and for authentication, the certificate presented by the backend must match this hostname, *unless* `subjectAltNames` is explicitly specified.

If `subjectAltNames` (SANs) are specified, the `hostname` is only used for SNI, and authentication is performed against the SANs instead. If you still need to authenticate against the hostname value in this case, you MUST add it to the `subjectAltNames` list.

BackendTLSPolicy `validation` configuration also requires either `caCertificateRefs` or `wellKnownCACertificates`. `caCertificateRefs` refer to one or more (up to 8) PEM-encoded TLS certificate bundles. If there are no specific certificates to use, then depending on your implementation, you may use `wellKnownCACertificates`, set to "System" to tell the Gateway to use an implementation-specific set of trusted CA Certificates.

In this example, the BackendTLSPolicy is configured to use certificates defined in the auth-cert ConfigMap to connect with a TLS-encrypted upstream connection where pods backing the auth service are expected to serve a valid certificate for `auth.example.com`. It uses `subjectAltNames` with a Hostname type, but you may also use a URI type.

```sh
apiVersion: gateway.networking.k8s.io/v1kind: BackendTLSPolicymetadata:name: tls-upstream-authspec:targetRefs:- kind: Servicename: authgroup: ""sectionName: "https"validation:caCertificateRefs:- group: "" # core API groupkind: ConfigMapname: auth-certsubjectAltNames:- type: "Hostname"hostname: "auth.example.com"
```

In this example, the BackendTLSPolicy is configured to use system certificates to connect with a TLS-encrypted backend connection where Pods backing the dev Service are expected to serve a valid certificate for `dev.example.com`.

```sh
apiVersion: gateway.networking.k8s.io/v1kind: BackendTLSPolicymetadata:name: tls-upstream-devspec:targetRefs:- kind: Servicename: devgroup: ""sectionName: "btls"validation:wellKnownCACertificates: "System"hostname: dev.example.com
```

More information on the configuration of TLS in Gateway API can be found in [Gateway API - TLS Configuration](https://gateway-api.sigs.k8s.io/guides/tls/).

##### Status Information about the Features that an Implementation Supports

GEP-2162: [Supported features in GatewayClass Status](https://github.com/kubernetes-sigs/gateway-api/blob/main/geps/gep-2162/index.md)

GatewayClass status has a new field, `supportedFeatures`. This addition allows implementations to declare the set of features they support. This provides a clear way for users and tools to understand the capabilities of a given GatewayClass.

This feature's name for conformance tests (and GatewayClass status reporting) is **SupportedFeatures**. Implementations must populate the `supportedFeatures` field in the `.status` of the GatewayClass **before** the GatewayClass is accepted, or in the same operation.

Here’s an example of a `supportedFeatures` published under GatewayClass' `.status`:

```sh
apiVersion: gateway.networking.k8s.io/v1kind: GatewayClass...status:conditions:- lastTransitionTime: "2022-11-16T10:33:06Z"message: Handled by Foo controllerobservedGeneration: 1reason: Acceptedstatus: "True"type: AcceptedsupportedFeatures:- HTTPRoute- HTTPRouteHostRewrite- HTTPRoutePortRedirect- HTTPRouteQueryParamMatching
```

Graduation of SupportedFeatures to Standard, helped improve the conformance testing process for Gateway API. The conformance test suite will now automatically run tests based on the features populated in the GatewayClass' status. This creates a strong, verifiable link between an implementation's declared capabilities and the test results, making it easier for implementers to run the correct conformance tests and for users to trust the conformance reports.

This means when the SupportedFeatures field is populated in the GatewayClass status there will be no need for additional conformance tests flags like `–suported-features`, or `–exempt` or `–all-features`. It's important to note that Mesh features are an exception to this and can be tested for conformance by using *Conformance Profiles*, or by manually providing any combination of features related flags until the dedicated resource graduates from the experimental channel.

##### Named Rules for Routes

GEP-995: [Adding a new name field to all xRouteRule types (HTTPRouteRule, GRPCRouteRule, etc.)](https://gateway-api.sigs.k8s.io/geps/gep-995)

This enhancement enables route rules to be explicitly identified and referenced across the Gateway API ecosystem. Some of the key use cases include:

- **Status:** Allowing status conditions to reference specific rules directly by name.
- **Observability:** Making it easier to identify individual rules in logs, traces, and metrics.
- **Policies:** Enabling policies ([GEP-713](https://gateway-api.sigs.k8s.io/geps/gep-773)) to target specific route rules via the `sectionName` field in their `targetRef[s]`.
- **Tooling:** Simplifying filtering and referencing of route rules in tools such as `gwctl`, `kubectl`, and general-purpose utilities like `jq` and `yq`.
- **Internal configuration mapping:** Facilitating the generation of internal configurations that reference route rules by name within gateway and mesh implementations.

This follows the same well-established pattern already adopted for Gateway listeners, Service ports, Pods (and containers), and many other Kubernetes resources.

While the new name field is **optional** (so existing resources remain valid), its use is **strongly encouraged**. Implementations are not expected to assign a default value, but they may enforce constraints such as immutability.

Finally, keep in mind that the [name format](https://gateway-api.sigs.k8s.io/geps/gep-995/?h=995#format) is validated, and other fields (such as [`sectionName`](https://gateway-api.sigs.k8s.io/reference/spec/?h=sectionname#sectionname)) may impose additional, indirect constraints.

##### Enabling External Auth for HTTPRoute

Giving Gateway API the ability to enforce authentication and maybe authorization as well at the Gateway or HTTPRoute level has been a highly requested feature for a long time. (See the [GEP-1494 issue](https://github.com/kubernetes-sigs/gateway-api/issues/1494) for some background.)

This Gateway API release adds an Experimental filter in HTTPRoute that tells the Gateway API implementation to call out to an external service to authenticate (and, optionally, authorize) requests.

This filter is based on the [Envoy ext\_authz API](https://www.envoyproxy.io/docs/envoy/latest/configuration/http/http_filters/ext_authz_filter#config-http-filters-ext-authz), and allows talking to an Auth service that uses either gRPC or HTTP for its protocol.

Both methods allow the configuration of what headers to forward to the Auth service, with the HTTP protocol allowing some extra information like a prefix path.

A HTTP example might look like this (noting that this example requires the Experimental channel to be installed and an implementation that supports External Auth to actually understand the config):

```sh
apiVersion: gateway.networking.k8s.io/v1kind: HTTPRoutemetadata:name: require-authnamespace: defaultspec:parentRefs:- name: your-gateway-hererules:- matches:- path:type: Prefixvalue: /adminfilters:- type: ExternalAuthexternalAuth:protocol: HTTPbackendRef:name: auth-servicehttp:# These headers are always sent for the HTTP protocol,# but are included here for illustrative purposesallowedHeaders:- Host- Method- Path- Content-Length- AuthorizationbackendRefs:- name: admin-backendport: 8080
```

This allows the backend Auth service to use the supplied headers to make a determination about the authentication for the request.

When a request is allowed, the external Auth service will respond with a 200 HTTP response code, and optionally extra headers to be included in the request that is forwarded to the backend. When the request is denied, the Auth service will respond with a 403 HTTP response.

Since the Authorization header is used in many authentication methods, this method can be used to do Basic, Oauth, JWT, and other common authentication and authorization methods.

##### Mesh Resource

Lead(s): [Flynn](https://github.com/kflynn)

GEP-3949: [Mesh-wide configuration and supported features](https://github.com/kubernetes-sigs/gateway-api/issues/3949)

Gateway API v1.4.0 introduces a new experimental Mesh resource, which provides a way to configure mesh-wide settings and discover the features supported by a given mesh implementation. This resource is analogous to the Gateway resource and will initially be mainly used for conformance testing, with plans to extend its use to off-cluster Gateways in the future.

The Mesh resource is cluster-scoped and, as an experimental feature, is named `XMesh` and resides in the `gateway.networking.x-k8s.io` API group. A key field is controllerName, which specifies the mesh implementation responsible for the resource. The resource's `status` stanza indicates whether the mesh implementation has accepted it and lists the features the mesh supports.

One of the goals of this GEP is to avoid making it more difficult for users to adopt a mesh. To simplify adoption, mesh implementations are expected to create a default Mesh resource upon startup if one with a matching `controllerName` doesn't already exist. This avoids the need for manual creation of the resource to begin using a mesh.

The new XMesh API kind, within the gateway.networking.x-k8s.io/v1alpha1 API group, provides a central point for mesh configuration and feature discovery (source).

A minimal XMesh object specifies the `controllerName`:

```sh
apiVersion: gateway.networking.x-k8s.io/v1alpha1kind: XMeshmetadata:name: one-mesh-to-mesh-them-allspec:controllerName: one-mesh.example.com/one-mesh
```

The mesh implementation populates the status field to confirm it has accepted the resource and to list its supported features ( source):

```sh
status:conditions:- type: Acceptedstatus: "True"reason: AcceptedsupportedFeatures:- name: MeshHTTPRoute- name: OffClusterGateway
```

Lead(s): [Flynn](https://github.com/kflynn)

GEP-3793: [Allowing Gateways to program some routes by default](https://github.com/kubernetes-sigs/gateway-api/issues/3793).

For application developers, one common piece of feedback has been the need to explicitly name a parent Gateway for every single north-south Route. While this explicitness prevents ambiguity, it adds friction, especially for developers who just want to expose their application to the outside world without worrying about the underlying infrastructure's naming scheme. To address this, we have introduce the concept of **Default Gateways**.

As an application developer, you often don't care about the specific Gateway your traffic flows through, you just want it to work. With this enhancement, you can now create a Route and simply ask it to use a default Gateway.

This is done by setting the new `useDefaultGateways` field in your Route's `spec`.

Here’s a simple `HTTPRoute` that uses a default Gateway:

```sh
apiVersion: gateway.networking.k8s.io/v1kind: HTTPRoutemetadata:name: my-routespec:useDefaultGateways: Allrules:- backendRefs:- name: my-serviceport: 80
```

That's it! No more need to hunt down the correct Gateway name for your environment. Your Route is now a "defaulted Route."

###### For Cluster Operators: You're Still in Control

This feature doesn't take control away from cluster operators ("Chihiro"). In fact, they have explicit control over which Gateways can act as a default. A Gateway will only accept these *defaulted Routes* if it is configured to do so.

You can also use a ValidatingAdmissionPolicy to either require or even forbid for Routes to rely on a default Gateway.

As a cluster operator, you can designate a Gateway as a default by setting the (new) `.spec.defaultScope` field:

```sh
apiVersion: gateway.networking.k8s.io/v1kind: Gatewaymetadata:name: my-default-gatewaynamespace: defaultspec:defaultScope: All# ... other gateway configuration
```

Operators can choose to have no default Gateways, or even multiple.

###### How it Works and Key Details

- To maintain a clean, GitOps-friendly workflow, a default Gateway does *not* modify the `spec.parentRefs` of your Route. Instead, the binding is reflected in the Route's `status` field. You can always inspect the `status.parents` stanza of your Route to see exactly which Gateway or Gateways have accepted it. This preserves your original intent and avoids conflicts with CD tools.
- The design explicitly supports having multiple Gateways designated as defaults within a cluster. When this happens, a defaulted Route will bind to *all* of them. This enables cluster operators to perform zero-downtime migrations and testing of new default Gateways.
- You can create a single Route that handles both north-south traffic (traffic entering or leaving the cluster, via a default Gateway) and east-west/mesh traffic (traffic between services within the cluster), by explicitly referencing a Service in `parentRefs`.

Default Gateways represent a significant step forward in making the Gateway API simpler and more intuitive for everyday use cases, bridging the gap between the flexibility needed by operators and the simplicity desired by developers.

##### Configuring Client Certificate Validation

GEP-91: [Address connection coalescing security issue](https://github.com/kubernetes-sigs/gateway-api/pull/3942)

This release brings updates for configuring client certificate validation, addressing a critical security vulnerability related to connection reuse. HTTP connection coalescing is a web performance optimization that allows a client to reuse an existing TLS connection for requests to different domains. While this reduces the overhead of establishing new connections, it introduces a security risk in the context of API gateways. The ability to reuse a single TLS connection across multiple Listeners brings the need to introduce shared client certificate configuration in order to avoid unauthorized access.

###### Why SNI-based mTLS is not the Answer

One might think that using Server Name Indication (SNI) to differentiate between Listeners would solve this problem. However, TLS SNI is not a reliable mechanism for enforcing security policies in a connection coalescing scenario. A client could use a single TLS connection for multiple peer connections, as long as they are all covered by the same certificate. This means that a client could establish a connection by indicating one peer identity (using SNI), and then reuse that connection to access a different virtual host that is listening on the same IP address and port. That reuse, which is controlled by client side heuristics, could bypass mutual TLS policies that were specific to the second listener configuration.

Here's an example to help explain it:

```sh
apiVersion: gateway.networking.k8s.io/v1kind: Gatewaymetadata:name: wildcard-tls-gatewayspec:gatewayClassName: examplelisteners:- name: foo-httpsprotocol: HTTPSport: 443hostname: foo.example.comtls:certificateRefs:- group: "" # core API groupkind: Secretname: foo-example-com-cert  # SAN: foo.example.com- name: wildcard-httpsprotocol: HTTPSport: 443hostname: "*.example.com"tls:certificateRefs:- group: "" # core API groupkind: Secretname: wildcard-example-com-cert # SAN: *.example.com
```

I have configured a Gateway with two listeners, both having overlapping hostnames. My intention is for the `foo-http` listener to be accessible only by clients presenting the `foo-example-com-cert` certificate. In contrast, the `wildcard-https` listener should allow access to a broader audience using any certificate valid for the `*.example.com` domain.

Consider a scenario where a client initially connects to `foo.example.com`. The server requests and successfully validates the `foo-example-com-cert` certificate, establishing the connection. Subsequently, the same client wishes to access other sites within this domain, such as `bar.example.com`, which is handled by the `wildcard-https` listener. Due to connection reuse, clients can access `wildcard-https` backends without an additional TLS handshake on the existing connection. This process functions as expected.

However, a critical security vulnerability arises when the order of access is reversed. If a client first connects to `bar.example.com` and presents a valid `bar.example.com` certificate, the connection is successfully established. If this client then attempts to access `foo.example.com`, the existing connection's client certificate will not be re-validated. This allows the client to bypass the specific certificate requirement for the `foo` backend, leading to a serious security breach.

###### The Solution: Per-port TLS Configuration

The updated Gateway API gains a `tls` field in the `.spec` of a Gateway, that allows you to define a default client certificate validation configuration for all Listeners, and then if needed override it on a per-port basis. This provides a flexible and powerful way to manage your TLS policies.

Here’s a look at the updated API definitions (shown as Go source code):

```sh
// GatewaySpec defines the desired state of Gateway.
type GatewaySpec struct {
    ...
    // GatewayTLSConfig specifies frontend tls configuration for gateway.
    TLS *GatewayTLSConfig `json:"tls,omitempty"`
}
// GatewayTLSConfig specifies frontend tls configuration for gateway.
type GatewayTLSConfig struct {
    // Default specifies the default client certificate validation configuration
    Default TLSConfig `json:"default"`
    // PerPort specifies tls configuration assigned per port.
    PerPort []TLSPortConfig `json:"perPort,omitempty"`
}
// TLSPortConfig describes a TLS configuration for a specific port.
type TLSPortConfig struct {
    // The Port indicates the Port Number to which the TLS configuration will be applied.
    Port PortNumber `json:"port"`
    // TLS store the configuration that will be applied to all Listeners handling
    // HTTPS traffic and matching given port.
    TLS TLSConfig `json:"tls"`
}

```

#### Breaking Changes

##### Standard GRPCRoute - `.spec` Field Required (technicality)

The promotion of GRPCRoute to Standard introduces a minor but technically breaking change regarding the presence of the top-level `.spec` field. As part of achieving Standard status, the Gateway API has tightened the OpenAPI schema validation within the GRPCRoute CustomResourceDefinition (CRD) to explicitly ensure the spec field is required for all GRPCRoute resources. This change enforces stricter conformance to Kubernetes object standards and enhances the resource's stability and predictability. While it is highly unlikely that users were attempting to define a GRPCRoute without any specification, any existing automation or manifests that might have relied on a relaxed interpretation allowing a completely absent `spec` field will now fail validation and **must** be updated to include the `.spec` field, even if empty.

##### Experimental CORS Support in HTTPRoute - Breaking Change for `allowCredentials` Field

The Gateway API subproject has introduced a breaking change to the Experimental CORS support in HTTPRoute, concerning the `allowCredentials` field within the CORS policy. This field's definition has been strictly aligned with the upstream CORS specification, which dictates that the corresponding `Access-Control-Allow-Credentials` header must represent a Boolean value. Previously, the implementation might have been overly permissive, potentially accepting non-standard or string representations such as `true` due to relaxed schema validation. Users who were configuring CORS rules must now review their manifests and ensure the value for `allowCredentials` strictly conforms to the new, more restrictive schema. Any existing HTTPRoute definitions that do not adhere to this stricter validation will now be rejected by the API server, requiring a configuration update to maintain functionality.

#### Improving the Development and Usage Experience

As part of this release, we have improved some of the developer experience workflow:

- Added [Kube API Linter](https://github.com/kubernetes-sigs/kube-api-linter) to the CI/CD pipelines, reducing the burden of API reviewers and also reducing the amount of common mistakes.
- Improving the execution time of CRD tests with the usage of [`envtest`](https://pkg.go.dev/sigs.k8s.io/controller-runtime/pkg/envtest).

Additionally, as part of the effort to improve Gateway API usage experience, some efforts were made to remove some ambiguities and some old tech-debts from our documentation website:

- The API reference is now explicit when a field is `experimental`.
- The GEP (GatewayAPI Enhancement Proposal) navigation bar is automatically generated, reflecting the real status of the enhancements.

#### Try it out

Unlike other Kubernetes APIs, you don't need to upgrade to the latest version of Kubernetes to get the latest version of Gateway API. As long as you're running Kubernetes 1.26 or later, you'll be able to get up and running with this version of Gateway API.

To try out the API, follow the [Getting Started Guide](https://gateway-api.sigs.k8s.io/guides/).

As of this writing, seven implementations are already conformant with Gateway API v1.4.0. In alphabetical order:

Wondering when a feature will be added? There are lots of opportunities to get involved and help define the future of Kubernetes routing APIs for both ingress and service mesh.

- Check out the [user guides](https://gateway-api.sigs.k8s.io/guides) to see what use-cases can be addressed.
- Or [join us in the community](https://gateway-api.sigs.k8s.io/contributing/) and help us build the future of Gateway API together!
