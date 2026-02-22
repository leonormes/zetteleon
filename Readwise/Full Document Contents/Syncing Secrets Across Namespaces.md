# Syncing Secrets Across Namespaces

![rw-book-cover](https://cert-manager.io/images/og1.png)

## Metadata
- Author: [[cert-manager]]
- Full Title: Syncing Secrets Across Namespaces
- Category: #articles
- Summary: Multiple components in different namespaces can share the same Secret from one Certificate using extensions like reflector or kubed. Wildcard certificates can serve as default SSL certificates across namespaces but need DNS01 validation. Reflector and kubed help sync and keep Secrets updated automatically across specified namespaces.
- URL: https://cert-manager.io/v1.8-docs/faq/sync-secrets/

## Full Document
It may be required for multiple components across namespaces to consume the same `Secret` that has been created by a single `Certificate`. The recommended way to do this is to use extensions such as:

* [reflector](https://github.com/emberstack/kubernetes-reflector) with support for auto secret reflection

#### Serving a wildcard to ingress resources in different namespaces (default SSL certificate)

Most ingress controllers, including [ingress-nginx](https://kubernetes.github.io/ingress-nginx/user-guide/tls/#default-ssl-certificate), [Traefik](https://docs.traefik.io/https/tls/#default-certificate), and [Kong](https://docs.konghq.com/2.0.x/configuration/#ssl_cert) support specifying a *single* certificate to be used for ingress resources which request TLS but do not specify `tls.[].secretName`. This is often referred to as a "default SSL certificate". As long as this is correctly configured, ingress resources in any namespace will be able to use a single wildcard certificate. Wildcard certificates are not supported with HTTP01 validation and require DNS01.

Sample ingress snippet:

```
  - host: service.example.com  
  #[...]  
    #secretName omitted to use default wildcard certificate
```

#### 

In order for the target Secret to be synced, you can use the `secretTemplate` field for annotating the generated secret with the extension specific annotation (See [CertificateSecretTemplate](https://cert-manager.io/v1.8-docs/reference/api-docs/#cert-manager.io/v1.CertificateSecretTemplate)).

##### 

The example below shows syncing a certificate's secret from the `cert-manager` namespace to multiple namespaces (i.e. `dev`, `staging`, `prod`). Reflector will ensure that any namespace (existing or new) matching the allowed condition (with regex support) will get a copy of the certificate's secret and will keep it up to date. You can also sync other secrets (different name) using `reflector` (consult the extension's [README](https://github.com/emberstack/kubernetes-reflector/blob/main/README.md))

```
apiVersion: cert-manager.io/v1  
name: source  
namespace: cert-manager  
secretName: source-tls  
name: source-ca  
group: cert-manager.io  
annotations:  
reflector.v1.k8s.emberstack.com/reflection-allowed: "true"  
reflector.v1.k8s.emberstack.com/reflection-allowed-namespaces: "dev,staging,prod"  # Control destination namespaces  
reflector.v1.k8s.emberstack.com/reflection-auto-enabled: "true" # Auto create reflection for matching namespaces  
reflector.v1.k8s.emberstack.com/reflection-allowed-namespaces: "dev,staging,prod" # Control auto-reflection namespaces
```

##### 

The example below shows syncing a certificate belonging to the `sandbox` Certificate from the `cert-manager` namespace, into the `sandbox` namespace.

```
name: sandbox  
cert-manager-tls: sandbox # Define namespace label for kubed  
apiVersion: cert-manager.io/v1  
name: sandbox  
namespace: cert-manager  
secretName: sandbox-tls  
name: sandbox-ca  
group: cert-manager.io  
annotations:  
kubed.appscode.com/sync: "cert-manager-tls=sandbox" # Sync certificate to matching namespaces
```
