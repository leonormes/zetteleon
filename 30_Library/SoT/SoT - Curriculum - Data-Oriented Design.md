---
aliases: ["DOD Curriculum", "DOP Learning Path", "Data-First Challenges"]
confidence: "5/5"
created: 2025-12-31T00:00:00Z
epistemic: "curriculum"
last_reviewed: "2025-12-31"
modified: 2025-12-31T23:08:33+00:00
purpose: "A progressive series of exercises to transition from 'Code-First' to 'Data-First' thinking, specifically designed to instill the Linus Torvalds/Data-Oriented mindset."
review_interval: "3 months"
see_also: ["[[SoT - Data-Oriented Programming (DOP)]]", "[[SoT - Data-Centric Software Engineering]]", "[[SoT - Slot Map (Generational Arena)]]"]
source_of_truth: []
status: "active"
tags: ["curriculum", "dop", "practice", "exercises"]
title: SoT - Curriculum - Data-Oriented Design
type: "SoT"
uid: 
updated: 
---

## 1. The Philosophy: "Code is Derivative"

> "Bad programmers worry about the code. Good programmers worry about data structures and their relationships."—**Linus Torvalds**

This curriculum is designed to break the habit of "writing code to manage state" and replace it with "designing state that manages itself."

---

## Level 1: The State Enforcer (Invariants)

**The Principle:** Make invalid states impossible to represent.
**The Goal:** Eliminate `if (isValid)` checks from your codebase.

### Challenge: The "Smart" Traffic Light

Design the data model for a traffic light system that handles the transition between Green, Amber, and Red.

#### The Code-First Trap (The "Flag" Soup)

```typescript
class TrafficLight {
    isGreen: boolean;
    isAmber: boolean;
    isRed: boolean;
}
```

* **The Bug:** It is technically possible for `isGreen` and `isRed` to be true simultaneously.
* **The Cost:** You must write "Guard Clauses" everywhere.

#### The Data-First Solution (The Union)

```typescript
type TrafficLight = { state: 'Green' } | { state: 'Amber' } | { state: 'Red' };
```

### 🛑 Your Task: User Registration Refactor

* **Current State:** `isEmailVerified`, `hasPassword`, `isSuspended`.
* **Goal:** Create a state machine where a user cannot be "Suspended" if they haven't "Verified Email" yet.
* **Hint:** A `SuspendedUser` type should be distinct from a `PendingUser` type.

---

## Level 2: The Flat Hierarchy (Recursion Killer)

**The Principle:** Pointers are expensive; Indices are cheap. Avoid recursion in data structures.
**The Goal:** Query complex trees without recursion.

### Challenge: The Reddit Comment Section

Design a model for thousands of comments, where comments can be replies to other comments (infinite nesting).

#### The Code-First Trap (The Recursive Node)

```typescript
class Comment {
    id: number;
    text: string;
    replies: Comment[]; // Recursion here
}
```

* **The Bug:** To display the thread, you need a recursive render function. To find a specific comment, you have to traverse the tree.

#### The Data-First Solution (Adjacency List)

Flatten the tree into a list. Use `parentId` integers.

### 🛑 Your Task: Design a File System

* **Constraint:** Do not use a `Folder` class that contains a list of `Files`.
* **Goal:** How do you delete a folder and all its sub-contents efficiently without writing a recursive "delete children" function?
* **Hint:** Look up "Path Enumeration" or "Closure Tables".

---

## Level 3: The Sparse Entity (Composition)

**The Principle:** Don't pay for what you don't use.
**The Goal:** Handle heterogeneous data without massive inheritance trees.

### Challenge: The E-Commerce Product Catalog

You sell Books (Author, ISBN), T-Shirts (Size, Material), and Gift Cards (Value, Expiry).

#### The Code-First Trap (Inheritance Hell)

```typescript
class Product { id, price }
class PhysicalProduct extends Product { weight }
class Book extends PhysicalProduct { isbn }
```

* **The Bug:** What happens when you sell a "Digital Book"? It has an ISBN but no weight.

#### The Data-First Solution (Composition/Tags)

Treat properties as data rows (tables), not class members.

```typescript
const prices = new Map<ProductId, number>();
const weights = new Map<ProductId, number>(); // Only physical items are here
```

### 🛑 Your Task: RPG Character System

* **Characters:** Warrior (Health, Strength), Mage (Health, Mana), Ghost (Mana, but no Health/Physical body).
* **Goal:** Create a data structure where "Taking Damage" works for Warriors and Mages but is impossible to call on a Ghost, without using `if (obj.hasHealth)`.

---

## Level 4: The Time Traveller (Event Sourcing)

**The Principle:** Current state is just a cache of history.
**The Goal:** Debugging impossible scenarios.

### Challenge: The Bank Account

Manage a balance where money comes in and goes out.

#### The Code-First Trap (The Mutable Snapshot)

```typescript
class Account {
    balance: number = 0;
    deposit(amount) { this.balance += amount; }
}
```

* **The Bug:** The balance is 50. Why? You lost the data.

#### The Data-First Solution (The Log)

The "Data Structure" is an append-only array of events.

```typescript
type Transaction = { type: 'deposit' | 'withdrawal', amount: number };
const ledger: Transaction[] = [];
```

### 🛑 Your Task: Design a Chess Game

* **Constraint:** You cannot store the "Board" (an 8x8 array of pieces) as the primary source of truth.
* **Goal:** Store the game as a list of moves (`e2 -> e4`). How do you determine if a move is valid? (You must replay the history).

---

## Final Boss: The "Do It Yourself" Relational Model

**Project:** Build a Task Management System (Jira/Trello).

1. **Users** (Level 1: Strict States - Active/Invited).
2. **Tasks** (Level 2: Flat Hierarchy - Tasks can have sub-tasks).
3. **Custom Fields** (Level 3: Sparse Data - Some tasks have "Due Dates," some have "Story Points").
4. **Audit Trail** (Level 4: History - Who moved the ticket?).

**Constraint:** You may use TypeScript, but you are **banned from using Classes**. You must use `Interfaces`, `Arrays`, `Maps`, and `Functions` only.

**Why this works:** By stripping away the Class/Object "shell," you are forced to look at the naked data. You will naturally start organising it into efficient tables and indices.
