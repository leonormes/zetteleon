---
aliases: [Etcd Encryption, Kubernetes Secret Security]
created: 2025-02-07T12:57:56Z
last_reviewed: 2026-02-13
modified: 2026-02-13T13:38:39+00:00
status: stable
tags: [etcd, kubernetes, secrets, security, sot]
title: SoT - Kubernetes Secrets Management
type: SoT
---

## SoT - Kubernetes Secrets Management

### 1. Minimum Viable Understanding (MVU)

Kubernetes `Secret` objects are intended to store sensitive data, such as passwords, tokens, or keys. By default, these are stored as unencrypted base64-encoded strings in `etcd`. To achieve a production-grade security posture, these must be protected via Encryption at Rest and Access Control at the storage layer.

### 2. Securing the Kubernetes Etcd Database

The etcd database is the source of truth for all cluster state. Securing it is crucial for protecting the integrity and confidentiality of the entire cluster.

#### 2.1 Restricting Network Access

- Firewall Isolation: The most effective way to secure etcd is to isolate it behind a firewall that permits access only from the Kubernetes API servers.
- Controlling Sensitive Ports: etcd uses specific ports for client communication (2379-2380). Network traffic to these ports should be strictly controlled.

#### 2.2 Authentication and Authorisation

- Strong Credentials for API Servers: API servers should authenticate to etcd using robust credentials, such as TLS client certificates for mutual authentication.
- etcd ACLs (Access Control Lists): etcd supports ACLs to define fine-grained access control policies for different keys and users.

### 3. Encryption at Rest

- Encrypting etcd Data: Kubernetes supports encrypting data stored in etcd, including Secret resources. This safeguards sensitive information even if attackers gain access to etcd backups.
- Secure Backup Encryption: When backing up etcd data, use strong encryption mechanisms to protect the data from unauthorised access. Consider using FIPS 140-2 validated modules.

### 4. Operational Best Practices

- Separate etcd Instances: Consider using dedicated etcd instances for different components or services to limit the impact of a compromise.
- Key Rotation: Regularly rotate encryption keys used for etcd encryption and authentication.
- Audit Logging: Enable and regularly review etcd audit logs to track access and identify suspicious activities.
- External Secret Management: For FitFile deployments, native K8s secrets are often treated as "materialized state" while the "Source of Truth" resides in HashiCorp Vault. See [[SoT - FITFILE Secret Management Architecture]].
