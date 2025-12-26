---
aliases: []
type: ""
status: ""
confidence: ""
epistemic: ""
purpose: ""
modified: 2025-12-26T15:10:35+00:00
last_reviewed: ""
review_interval: ""
see_also: []
source_of_truth: []
title: Vault Architecture Core, Barrier, Storage
source: "https://gemini.google.com/share/60e867f32f05"
author:
  - "[[Gemini]]"
published:
created: 2025-12-26T15:09:19+00:00
description: "Created with Gemini"
tags:
  - "clippings"
---

\> Context & User Persona

\> I am a Senior Node.js/TypeScript developer transitioning to Cloud Native DevOps and Go (Golang). My learning style is Abstract-Conceptual and Top-Down. I value mental models, underlying logic, and architectural patterns over syntax or implementation details.

\> The Project

\> I am building a simplified, educational clone of HashiCorp Vault in Go. My goal is not to use Vault, but to reverse-engineer its core architectural patterns to understand how to build resilient, secure distributed systems. I am approaching this with a "Domain-First" and TDD methodology.

\> Your Role

\> Act as a Principal Core Engineer at HashiCorp. Your job is to explain the internal architecture of Vault to me so I can implement a simplified version.

\> Key Areas of Focus

\> Please hold the following context about Vault's internals for our session:

\> \* The Barrier (The "Seal"): How Vault encrypts the encryption key (Key Unsealing, Shamir's Secret Sharing). I need to understand the relationship between the Master Key, the Root Key, and the underlying data encryption.

\> \* The Physical Layer (Storage Backend): How Vault abstracts storage (Consul, Raft, S3) using interfaces. It expects the storage to be untrusted.

\> \* The Logical Layer (Secret Engines): How the "Router" works. How requests are routed to specific backends (KV, Transit, PKI) based on path prefixes.

\> \* The HTTP API & Context: How the core maps HTTP requests to internal function calls, specifically handling request contexts and cancellation.

\> Interaction Guidelines

\> \* Do not give me CLI tutorials or "how to install" guides.

\> \* Do explain the Go Structs and Interfaces that likely exist inside the Vault codebase.

\> \* Do use "Ports and Adapters" (Hexagonal Architecture) terminology where appropriate, as that is my current mental model.

\> \* Do focus on the separation of concerns—specifically how the encryption layer is decoupled from the storage layer.

\> To start, please give me a high-level System Architecture Diagram (described in text) of Vault, breaking it down into The Barrier, The Core, and The Backend, explaining the flow of data when a user writes a secret.

\>

Here is the high-level architecture of HashiCorp Vault, deconstructed for a Senior Go Engineer building a clone.

### The Mental Model: The Onion Architecture

View Vault not as a monolith, but as an onion of concentric layers. In Go terms, this is implemented via interface wrapping (decorators).

1. **The Physical Layer (Outer):** Dumb storage (S3, File, Raft). It knows nothing of secrets, only bytes.
2. **The Barrier (Middle):** The cryptographic membrane. It ensures that any data passing from the Core to the Physical Layer is encrypted. It manages the "Sealed" state.
3. **The Core (Inner):** The brain. It manages the identity of secret engines (KV, PKI), routing, and policy enforcement. It operates on *decrypted* data structures.

---

### 1\. High-Level System Architecture

In a Hexagonal (Ports and Adapters) view, the flow for writing a secret (`POST /v1/secret/my-pass`) looks like this:

**Driving Adapter (HTTP)** **Core (Router)** **Secret Engine (Logic)** **Barrier (Encryption)** **Driven Adapter (Storage)**

#### Data Flow: The Write Path

1. **Ingress:** The HTTP Server receives the request. It creates a `context.Context` (handling timeouts/cancellation) and maps the JSON body to a logical request struct.
2. **Routing (The Core):** The Core inspects the path (`secret/my-pass`). It consults the **Mount Table** (a radix tree) to find which backend owns the prefix `secret/`.
3. **Logical Processing:** The request is handed to the specific **Logical Backend** (e.g., the KV backend). The backend validates the data (business logic) and returns a `StorageEntry` object.
4. **The Barrier Entry:** The Core attempts to persist this entry. It calls the **Barrier Interface**.
5. **Encryption:** The Barrier checks if it is unsealed. If yes, it retrieves the active **Encryption Key** (held in memory). It serialises the entry and encrypts it (AES-GCM).
6. **Persistence:** The Barrier passes the *encrypted blob* to the **Physical Storage** interface (e.g., `storage.Put`).
7. **Storage:** The physical backend writes the random-looking bytes to disk/Consul/S3.

---

### 2\. The Physical Layer: Untrusted Storage

In your Go implementation, you must assume the storage backend is compromised. Therefore, the storage layer is strictly a standard interface for moving bytes.

**The Go Interface:**This is the "Port" for your Driven Adapters.

```go
// PhysicalBackend is the interface for storage.
// It deals in raw bytes and knows nothing of encryption or structure.
type PhysicalBackend interface {
    Put(ctx context.Context, entry *Entry) error
    Get(ctx context.Context, key string) (*Entry, error)
    Delete(ctx context.Context, key string) error
    List(ctx context.Context, prefix string) ([]string, error)
}

type Entry struct {
    Key   string
    Value []byte // Encrypted blob (ciphertext)
}
```

**Key Takeaway:** You can implement an `InMemoryBackend` or `FileBackend` implementing this interface. The Core never interacts with this directly; it interacts with the *Barrier*.

---

### 3\. The Barrier: The Cryptographic Shield

This is the most critical architectural component. The Barrier acts as a **middleware** between the Core and the Physical Backend.

**Concept: The Seal**

- **Sealed State:** The Barrier has no encryption keys in memory. It can access the Physical Backend, but it cannot read the data (it sees only ciphertext).
- **Unsealed State:** The components of the Master Key (Shamir's shares) have been provided. The Barrier reconstructs the Master Key, uses it to decrypt the **Keyring** (stored in the Physical Backend), and loads the active data encryption key into memory.

**The Go Struct Structure:**

Go

```go
type Barrier struct {
    backend  PhysicalBackend // The underlying storage
    keyring  *Keyring        // Holds active encryption keys (only present when unsealed)
    sealed   bool
    l        sync.RWMutex
}

// Put encrypts the entry using the active key from the keyring
// before passing it to the physical backend.
func (b *Barrier) Put(ctx context.Context, entry *LogicalEntry) error {
    if b.sealed {
        return ErrSealed
    }
    
    // 1. Serialize LogicalEntry to JSON/Protobuf
    // 2. Generate Nonce
    // 3. Encrypt (AES-GCM) using b.keyring.ActiveKey()
    // 4. Wrap in Physical Entry
    encryptedEntry := &Entry{
        Key:   entry.Key,
        Value: cipherText, 
    }
    
    return b.backend.Put(ctx, encryptedEntry)
}
```

---

### 4\. The Logical Layer: The Router & Engines

The Core manages "Mounts". A mount is a mapping between a path prefix and a backend implementation.

**The Router (Radix Tree):**Vault uses a Radix tree (or Trie) for efficient prefix matching.

- Path: `sys/` System Backend
- Path: `secret/` KV Backend
- Path: `aws/` AWS Backend

**The Logical Interface:**Every secret engine (KV, PKI, Transit) implements this interface. This allows the Core to treat a database credential generator exactly the same as a static key-value store.

Go

```go
type Backend interface {
    // HandleRequest is the entry point for execution
    HandleRequest(ctx context.Context, req *LogicalRequest) (*LogicalResponse, error)
    
    // Special capabilities
    Cleanup(ctx context.Context)
    Initialize(ctx context.Context) error
}

type LogicalRequest struct {
    Operation OperationType // READ, WRITE, DELETE, LIST
    Path      string
    Data      map[string]interface{} // The JSON payload
    Storage   Storage // Interface to the Barrier (scoped to this backend)
}
```

**Scope Isolation:**When the KV backend receives a request, the Core injects a `Storage` view that is prefixed. If the KV engine is mounted at `secret/`, and it tries to write key `foo`, the Barrier actually writes `secret/foo`. This prevents backends from overwriting each other's data.

---

### 5\. Architectural Summary for Implementation

To start your implementation, build these three packages in this order:

1. **`physical/`**: Define the `Backend` interface and a simple `InMem` implementation (map\[string\]\[\]byte).
2. **`vault/` (The Barrier)**: Create a struct that wraps `physical.Backend`. Implement a mock "Seal" that just holds a static AES key for now (add Shamir later). Implement `Encrypt` and `Decrypt` methods.
3. **`logical/`**: Define the `Backend` interface. Create a basic "Passthrough" backend that takes a key/value and tells the Barrier to store it.

Would you like me to detail the specific Go implementation of the **Shamir's Secret Sharing** algorithm and how it reconstructs the Master Key, or would you prefer to focus on the **Router/Radix Tree** implementation first?

Because it is called vault and it's sold as a secrets engine it has an aura of being something more secure. Why is it different from a document store with ACLs?

This is the specific question that separates a "user" of Vault from an "architect" of Vault. You have identified the core skepticism that every engineer should have.

From a purely mechanical perspective, you are correct: **Vault is a highly specialised, encrypted Key-Value store with an ACL layer.**

However, the difference lies in the **Threat Model** and the **Active vs. Passive** nature of the architecture. A document store is designed to *persist* data; Vault is designed to *manage the lifecycle* of a secret.

Here is the architectural breakdown of why Vault is not just MongoDB with a plugin.

### 1\. The Trust Boundary (The Barrier)

In a standard Document Store (e.g., Postgres, MongoDB), the database engine **trusts the storage**.

- If you use Transparent Data Encryption (TDE), the database process holds the keys to decrypt the disk.
- If a bad actor gets `root` access to the server or a snapshot of the volume, they can often recover the data because the keys are usually stored on the same machine (in a config file or HSM module that the DB automatically accesses on boot).

**Vault’s Architecture:**Vault assumes the **Storage Layer is compromised**.

- **The Separation:** As per the architecture we discussed, the `physical` package (Storage) never sees plaintext. The `barrier` package encrypts everything *before* it leaves the process memory.
- **The Unseal:** Vault does not "boot up" ready to serve traffic. It boots up in a `Sealed` state. It requires human intervention (or a trusted auto-unseal mechanism) to provide the master key parts to decrypt the memory barrier.
- **Result:** You can dump the entire Consul/S3 backend of a Vault cluster, and it is mathematically useless without the in-memory keys held by the active Vault process.

### 2\. Passive Data vs. Active Leasing (The Logic Layer)

A Document Store is **Passive**:

- You put `User: "admin", Pass: "password123"` into a DB.
- It stays there until you delete it.
- If an attacker reads it, they have it forever until you manually rotate it.

Vault is **Active (Dynamic Secrets)**:

- Vault implements the **Lease Pattern** (conceptually similar to DHCP).
- When you ask Vault for an AWS credential, it doesn't just read a static value. The AWS Secret Engine calls the AWS API, generates a *new* IAM user, returns it to you, and attaches a **Time-To-Live (TTL)**.
- **The Revocation Manager:** Vault has an internal loop (expiration manager) that monitors these leases. When the TTL hits 0, Vault automatically calls the AWS API to delete that IAM user.

**The Go Interface Difference:**In a Document Store, the interface is `Read` / `Write`.In Vault, the `Backend` interface includes `Renew` and `Revoke`.

Go

```go
// A standard DB interface
type Store interface {
    Get(key string)
    Put(key string, value val)
}

// Vault's Logical Backend Interface (Simplified)
type Backend interface {
    HandleRequest(ctx context.Context, req *Request) (*Response, error)
    
    // The Active difference:
    // Vault tracks the 'Secret' returned by HandleRequest.
    // When the lease expires, the Core calls Revoke automatically.
    Revoke(ctx context.Context, req *Request) error
}
```

### 3\. Identity Brokerage vs. ACLs

In a Document Store, ACLs control **"Can I read this row?"** In Vault, the question is **"Who are you, and what can you generate?"**

Vault acts as an **Identity Broker**. It decouples the *Application's Identity* (e.g., a Kubernetes Pod Service Account) from the *Target's Identity* (e.g., a Postgres Username).

- **The Pattern:** You authenticate to Vault using K8s (Method A). Vault verifies you, then generates a Postgres credential (Method B) for you.
- **Why it matters:** Your application never needs to know the "Root" credentials. It doesn't even "own" the credentials it uses; it just "leases" them.

### Summary: The Architectural Delta

| Feature | Document Store (e.g., Mongo + ACLs) | HashiCorp Vault |
| --- | --- | --- |
| **Trust Model** | Trusts the disk/OS. | Assumes disk/OS is compromised. |
| **Data State** | Static (read/write). | Dynamic (generate/revoke). |
| **Encryption** | Often transparent (TDE). | Application-layer (Barrier). |
| **Key Management** | Keys often in config/files. | Keys reconstructed in memory (Shamir). |
| **Mental Model** | A Safe (you put things in). | A Casino Cashier (checks ID, issues chips, takes them back). |

### Next Step

To build your clone, we need to respect this distinction. We shouldn't just build a CRUD API.

Would you like to start by architecting **The Barrier** (implementing the Envelope Encryption and Sealed State) or **The Core** (handling the Request Context and basic Routing)?
