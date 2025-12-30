---
aliases: ["Parse Don't Validate", "Type-Driven Validation", "Alexis King Principle"]
confidence: "5/5"
created: 2025-12-30T11:05:24+00:00
epistemic: "principle"
last_reviewed: "2025-12-30"
modified: 2025-12-30T14:11:32+00:00
purpose: "To define the architectural principle of shifting validation to the system boundaries by transforming data into Types, rather than just checking it."
review_interval: "12 months"
see_also: ["[[SoT - Type-Driven Development (The Torvalds Loop)]]", "[[SoT - Algebraic Data Types (ADTs)]]", "[[SoT - The Infrastructure Witness Pattern]]"]
source_of_truth: []
status: "stable"
tags: ["architecture", "type_theory", "security", "principle"]
title: "SoT - Parse, Don't Validate"
type: "SoT"
uid: 
updated: 
---

## 1. The Core Principle

> [!definition] Parse, Don't Validate
> A design philosophy (coined by Alexis King) stating that we should **Parse** incoming data (transforming it into a structural Type that preserves the check) rather than just **Validating** it (checking a property and discarding the proof).

- **Validation:** checks `is_email(string) -> bool`. The output is still just a `string`. You have to check it again later.
- **Parsing:** checks `parse_email(string) -> Result<Email, Error>`. The output is an `Email` type. You never have to check it again.

---

## 2. The Problem: "Shotgun Parsing"

When we rely on validation, we often fall into the trap of **Shotgun Parsing**: checking data integrity ad-hoc, everywhere in the codebase.

- **Redundancy:** Every function checks `if valid(x)`.
- **Fragility:** If one function forgets to check, the system breaks.
- **Boolean Blindness:** The boolean result (`true`) doesn't carry *why* it's valid or *what* invariants are guaranteed.

---

## 3. The Solution: The Type System as Proof

By parsing, we use the Type System to capture the "Proof of Validity."

### Example: The Non-Empty List

**Validation Approach (Bad):**

```rust
fn head(list: List<T>) -> Option<T> {
    if list.is_empty() { None } else { Some(list[0]) }
}
// You have to handle the empty case everywhere.
```

**Parsing Approach (Good):**

```rust
struct NonEmptyList<T>(T, Vec<T>); // Proof: Head is always present.

fn head(list: NonEmptyList<T>) -> T {
    list.0 // No check needed. Guaranteed by the type.
}
```

---

## 4. Application to Architecture

### 4.1 The Boundary Layer

All external input (User, Network, Disk) is "Untrusted."

- **Layer 1 (The Parser):** The *only* place where runtime checks happen. It attempts to construct a valid Type (e.g., `UserId`, `Email`, `Config`).
- **Layer 2 (The Core):** Accepts *only* the valid Types. It contains **zero** validation logic because the types themselves prove the data is valid.

### 4.2 Making Illegal States Unrepresentable

If a state is impossible (e.g., "Logged in but no User ID"), the Type System should make it impossible to construct.

- **Bad:** `struct User { logged_in: bool, id: Option<String> }`
- **Good:** `enum UserState { Guest, LoggedIn(UserId) }`

---

## 5. Naming Heuristics for Parsed Types

Naming is the vocabulary of the domain. In this paradigm, we name **Invariants** and **Roles**, not just "containers."

### I. Name the Invariant (The Guarantee)
Name the type after the proof it carries.
- **Bad:** `StringWrapper`, `ValidatedData`.
- **Good:** `EmailAddress`, `NonEmptyString`, `SortedList`.
- *Logic:* When you see `SortedList`, you know the property "is sorted" is already proven.

### II. Name the Role (The Context)
Name the type based on its stage in the pipeline or its function.
- **Bad:** `CertData`, `KeyInfo`.
- **Good:** `CertificateSigningRequest`, `VerifiedCertificate`, `SessionKey`.

### III. The "State as Type" Pattern
For complex transitions, reflect the lifecycle stage in the name.
- **Example:** `DraftOrder` $\to$ `PaidOrder` $\to$ `ShippedOrder`.

---

## 6. Summary

**"Validation"** is a question ("Is this true?").
**"Parsing"** is a transformation ("Turn this raw data into a Fact").

Always choose the transformation.
