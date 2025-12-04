---
aliases: []
confidence: 
created: 2025-10-24T09:50:32Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:23Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: NGSI-LD Report
type:
uid: 
updated: 
version:
---

## NGSI-LD Report

### NGSI-LD: A Framework for Context Information

NGSI-LD is a standard for modeling, representing, and sharing context information. The "LD" stands for "Linked Data," which is central to its design. It provides a common way to describe "Entities" (the things in your world) and their "Properties" and "Relationships" with other entities.

At its core, NGSI-LD is based on a **property graph** model. This means that it represents information as a set of entities, the properties they possess, and the relationships between them.

### Core Concepts

1. **Entity**: An Entity is the central concept in NGSI-LD. It represents a physical or conceptual object. For example, in your Obsidian vault, an entity could be a note, a person, a project, or a concept. Each Entity has a unique `id` (a URI) and a `type`.
2. **Property**: A Property is a characteristic of an Entity. It has a `value`. For example, a `Note` entity could have a `wordCount` property with a value of `500`.
3. **Relationship**: A Relationship describes a link between an Entity and another Entity. It has an `object` that is the `id` of the target entity. For example, a `Note` entity could have a `cites` relationship pointing to another `Note` entity.

### How NGSI-LD Uses JSON-LD

NGSI-LD uses **JSON-LD** to represent this information. This is what makes it "Linked Data." The key is the `@context` field in the JSON-LD document. The `@context` maps the short, human-readable terms in your JSON (like `"speed"`) to globally unique URIs.

For example, the `ngsi-ld-core-context.jsonld` file you have in your `coreContext` folder defines these mappings:

```json
{
  "@context": {
    "Property": "ngsi-ld:Property",
    "Relationship": "ngsi-ld:Relationship",
    "value": "ngsi-ld:hasValue",
    "object": "ngsi-ld:hasObject",
    "observedAt": {
      "@id": "ngsi-ld:observedAt",
      "@type": "DateTime"
    }
  }
}
```

This allows a machine to understand that when it sees `"speed": { "type": "Property", "value": 80 }`, the `"speed"` is not just a string, but a concept with a specific meaning defined by a URI, and that `80` is its value.

### Codifying Metadata in NGSI-LD

NGSI-LD is particularly powerful for codifying metadata because it allows **Properties of Properties** and **Properties of Relationships**. This lets you attach rich metadata to any piece of information.

Let's look at the `Entity-example.json` you have:

```json
{
  "id": "urn:ngsi-ld:Vehicle:V123",
  "type": "Vehicle",
  "speed": {
    "type": "Property",
    "value": 23,
    "accuracy": {
      "type": "Property",
      "value": 0.7
    },
    "providedBy": {
      "type": "Relationship",
      "object": "urn:ngsi-ld:Person:Bob"
    }
  },
  ...
}
```

In this example:

- The `Vehicle` entity has a `speed` property.
- The `speed` property itself has other properties:
  - `accuracy`: This is a **property of the property** `speed`. It tells us that the speed measurement has an accuracy of 0.7.
  - `providedBy`: This is a **relationship of the property** `speed`. It tells us that this speed measurement was provided by the entity `urn:ngsi-ld:Person:Bob`.

This hierarchical structure is how NGSI-LD codifies metadata. You can add any number of properties or relationships to another property or relationship, allowing for very detailed and structured metadata.

Here's another example from `Vehicle_C2.2.json`:

```json
"isParked": {
  "type": "Relationship",
  "object": "urn:ngsi-ld:OffStreetParking:Downtown1",
  "observedAt": "2017-07-29T12:00:04Z",
  "providedBy": {
    "type": "Relationship",
    "object": "urn:ngsi-ld:Person:Bob"
  }
}
```

Here, the `isParked` relationship has metadata:

- `observedAt`: A timestamp indicating when this relationship was observed.
- `providedBy`: A relationship indicating who provided this information.

### Application for Your Obsidian PKM System

For your `llmpkm` system in Obsidian, you can use NGSI-LD's JSON-LD format to structure your notes and their metadata in a way that is both human-readable and machine-understandable.

Here's how you could apply it:

- **Each note as an Entity**: Each of your markdown files could be an NGSI-LD Entity. The `id` could be a URI based on the file path. The `type` could be "Note", "Person", "Project", etc.
- **Frontmatter as Properties**: The YAML frontmatter of your notes could be represented as NGSI-LD Properties.
- **Links as Relationships**: The links between your notes (`[[wikilinks]]`) can be represented as NGSI-LD Relationships.
- **Metadata on everything**: You can add metadata to any property or link. For example, a link could have a `linkType` property (e.g., "supports", "refutes") or a `createdAt` timestamp.

By adopting this model, you can create a rich, interconnected knowledge graph within your Obsidian vault that can be queried and processed by your `llmpkm` system. The use of JSON-LD and a shared `@context` will ensure that the meaning of your metadata is consistent and unambiguous.
