---
aliases: ["ECS", "Entity Component System"]
confidence: "5/5"
created: 2025-12-31T00:00:00Z
epistemic: "architecture"
last_reviewed: "2025-12-31"
modified: 2026-01-03T10:18:55+00:00
purpose: "To define the ECS architecture as the standard framework for Data-Oriented Programming."
review_interval: "1 year"
see_also: ["[[SoT - Data-Oriented Programming (DOP)]]", "[[SoT - Rust Language]]"]
source_of_truth: []
status: "stable"
tags: ["ecs", "SoftwareEngineering/Architecture", "game_development", "rust"]
title: SoT - Entity Component System (ECS)
type: "SoT"
uid: 
updated: 
---

## 1. Definitive Statement

> [!definition] The Core Philosophy
> **Entity Component System (ECS)** is an architectural pattern that favors **Composition over Inheritance**. It decouples **Data** (Components) from **Identity** (Entities) and **Logic** (Systems).
>
> It functions as an **In-Memory Relational Database** where logic queries for data combinations rather than calling methods on objects.

## 2. The Trinity: E-C-S

| Concept | OOP Equivalent | ECS Reality |
|:--- |:--- |:--- |
| **Entity** | The Object | **The Primary Key (ID).** It is a generic integer (e.g., `Entity(402)`). It holds no data and no logic. It simply tags components together. |
| **Component** | Fields / Properties | **The Data (Table).** A flat struct containing only raw data (no methods). Examples: `Position`, `Velocity`, `Health`. |
| **System** | Methods | **The Logic (Query).** Global functions that query the database for entities possessing a specific combination of components. |

## 3. The Logic Flow

In OOP, logic is inside the object: `player.update()`.

In ECS, logic is a "System" that runs on a query.

**The Query:**
`SELECT Position, Velocity FROM World WHERE HasComponent(Position) AND HasComponent(Velocity)`

```rust
// Rust / Bevy Example
fn movement_system(mut query: Query<(&mut Position, &Velocity)>) {
    // Iterates contiguous memory arrays (SoA)
    for (mut pos, vel) in query.iter_mut() {
        pos.x += vel.x;
        pos.y += vel.y;
    }
}
```

## 4. Archetypes and Performance

Modern ECS engines (like Bevy, Flecs) use **Archetypes** to guarantee memory contiguity.

* **Archetype:** A unique combination of components (e.g., `[Pos, Vel]` vs `[Pos, Vel, Name]`).
* **Storage:** Entities of the same Archetype are stored in specific "Tables" (tightly packed arrays).
* **Transition:** Adding a component moves the entity from "Table A" to "Table B" (memcpy).

## 5. Benefits over OOP

1. **Horizontal Composition:** You can attach a `Health` component to a `Player`, `Tree`, or `Wall`. The `DamageSystem` handles them all uniformly without complex inheritance hierarchies.
2. **Cache Locality:** Systems iterate linearly through arrays.
3. **Parallelism:** Because data access is explicit (System A reads `Pos`, System B writes `Pos`), the scheduler can automatically run non-conflicting systems in parallel.

## 6. Trade-offs

* **Rigidity:** Easy to add global behavior (new System). Hard to handle specific interactions between two specific entities (e.g., "If *this* Key unlocks *that* Door").
* **Discovery:** Harder to know "what can a Player do?" because logic is scattered across independent Systems.
