---
aliases: []
confidence: 
created: 2025-09-07T08:09:36Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:41Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [source/book]
title: Learning Domain-Driven Design
type:
uid: 
updated: 
version:
---

## Learning Domain-Driven Design

![rw-book-cover](https://m.media-amazon.com/images/I/81WJbw5XJbL._SY160.jpg)

### Metadata

- Author: [[Vlad Khononov]]
- Full Title: Learning Domain-Driven Design
- Category:
- Document Tags: [[ddd]]

### Highlights

- you will learn domain-driven design tools for analyzing a company’s business domain and its structure: its core, supporting, and generic subdomains. This material is the groundwork for designing software. In the remaining chapters, you will learn the different ways these concepts affect software design. ([Location 347](https://readwise.io/to_kindle?action=open&asin=B09J2CMJZY&location=347))
- Complexity A core subdomain that is simple to implement can only provide a short-lived competitive advantage. Therefore, core subdomains are naturally complex. ([Location 393](https://readwise.io/to_kindle?action=open&asin=B09J2CMJZY&location=393))
- There should be high entry barriers for a company’s core business; it should be hard for competitors to copy or imitate the company’s solution. ([Location 401](https://readwise.io/to_kindle?action=open&asin=B09J2CMJZY&location=401))
- Supporting subdomains The problems with obvious solutions. These are the activities the company likely has to implement in-house, but that do not provide any competitive advantage. ([Location 784](https://readwise.io/to_kindle?action=open&asin=B09J2CMJZY&location=784))
- It’s developers’ (mis)understanding, not domain experts’ knowledge, that gets released in production. Alberto Brandolini ([Location 805](https://readwise.io/to_kindle?action=open&asin=B09J2CMJZY&location=805))
- You learned how to identify a company’s business domains, or areas of activity, and analyze its strategy to compete in them; that is, its business subdomains’ boundaries and types. ([Location 808](https://readwise.io/to_kindle?action=open&asin=B09J2CMJZY&location=808))
  - Note: how do we compete in the market? who are or competitors? what would make us stand out? what can we do from here to make that happen
- Model Boundaries As we discussed in the previous chapter, a model is not a copy of the real world but a construct that helps us make sense of a complex system. The problem it is supposed to solve is an inherent part of a model—its purpose. ([Location 1181](https://readwise.io/to_kindle?action=open&asin=B09J2CMJZY&location=1181))
- Bounded contexts define the applicability of a ubiquitous language and of the model it represents. ([Location 1189](https://readwise.io/to_kindle?action=open&asin=B09J2CMJZY&location=1189))
- The language is focused on describing only the model that is encompassed by the bounded context. ([Location 1197](https://readwise.io/to_kindle?action=open&asin=B09J2CMJZY&location=1197))
- Defining the scope of a ubiquitous language—its bounded context—is a strategic design decision. ([Location 1209](https://readwise.io/to_kindle?action=open&asin=B09J2CMJZY&location=1209))
- One thing to beware of is splitting a coherent functionality into multiple bounded contexts. Such division will hinder the ability to evolve each context independently. ([Location 1222](https://readwise.io/to_kindle?action=open&asin=B09J2CMJZY&location=1222))
- As historian Yuval Noah Harari puts it, “Scientists generally agree that no theory is 100 percent correct. Thus, the real test of knowledge is not the truth, but utility.” ([Location 1359](https://readwise.io/to_kindle?action=open&asin=B09J2CMJZY&location=1359))
- As a result, there will always be touchpoints between bounded contexts. These are called contracts. ([Location 1453](https://readwise.io/to_kindle?action=open&asin=B09J2CMJZY&location=1453))
- The need for contracts results from differences in bounded contexts’ models and languages. ([Location 1454](https://readwise.io/to_kindle?action=open&asin=B09J2CMJZY&location=1454))
- Unlike in the cooperation case, both teams (upstream and downstream) can succeed independently. Consequently, in most cases we have an imbalance of power: either the upstream or the downstream team can dictate the integration contract. This section will discuss three patterns addressing such power differences: the conformist, anticorruption layer, and open-host service patterns. ([Location 1562](https://readwise.io/to_kindle?action=open&asin=B09J2CMJZY&location=1562))
- The supplier’s public interface is not intended to conform to its ubiquitous language. Instead, it is intended to expose a protocol convenient for the consumers, expressed in an integration-oriented language. As such, the public protocol is called the published language. In a sense, the open-host service pattern is a reversal of the anticorruption layer pattern: instead of the consumer, the supplier implements the translation of its internal model. ([Location 1613](https://readwise.io/to_kindle?action=open&asin=B09J2CMJZY&location=1613))
- A system’s public interface can be seen as a collection of business transactions that consumers can execute, ([Location 1769](https://readwise.io/to_kindle?action=open&asin=B09J2CMJZY&location=1769))
- Active Record An object that wraps a row in a database table or view, encapsulates the database access, and adds domain logic on that data. Martin Fowler2 ([Location 2035](https://readwise.io/to_kindle?action=open&asin=B09J2CMJZY&location=2035))
- Active record When the business logic is simple but operates on complicated data structures, you can implement those data structures as active records. An active record object is a data structure that provides simple CRUD data access methods. ([Location 2136](https://readwise.io/to_kindle?action=open&asin=B09J2CMJZY&location=2136))
- In his book, Evans presents a set of patterns aimed at tightly relating the code to the underlying model of the business domain: aggregate, value objects, repositories, and others. These patterns closely follow where Fowler left off in his book and resemble an effective set of tools for implementing the domain model pattern. ([Location 2206](https://readwise.io/to_kindle?action=open&asin=B09J2CMJZY&location=2206))
- The pattern is “domain model,” and the aggregates and value objects are its building blocks. ([Location 2210](https://readwise.io/to_kindle?action=open&asin=B09J2CMJZY&location=2210))
- Domain Model The domain model pattern is intended to cope with cases of complex business logic. Here, instead of CRUD interfaces, we deal with complicated state transitions, business rules, and invariants: rules that have to be protected at all times. ([Location 2212](https://readwise.io/to_kindle?action=open&asin=B09J2CMJZY&location=2212))
- A domain model is an object model of the domain that incorporates both behavior and data.1 DDD’s tactical patterns—aggregates, value objects, domain events, and domain services—are the building blocks of such an object model.2 ([Location 2232](https://readwise.io/to_kindle?action=open&asin=B09J2CMJZY&location=2232))
- Building Blocks Let’s look at the central domain model building blocks, or tactical patterns, offered by DDD: value objects, aggregates, and domain services. ([Location 2254](https://readwise.io/to_kindle?action=open&asin=B09J2CMJZY&location=2254))
- Value object A value object is an object that can be identified by the composition of its values. For example, consider a color object: ([Location 2256](https://readwise.io/to_kindle?action=open&asin=B09J2CMJZY&location=2256))
- When to use value objects The simple answer is, whenever you can. Not only do value objects make the code more expressive and encapsulate business logic that tends to spread apart, but the pattern makes the code safer. Since value objects are immutable, the value objects’ behavior is free of side effects and is thread safe. ([Location 2604](https://readwise.io/to_kindle?action=open&asin=B09J2CMJZY&location=2604))
- Entities An entity is the opposite of a value object. It requires an explicit identification field to distinguish between the different instances of the entity. ([Location 2617](https://readwise.io/to_kindle?action=open&asin=B09J2CMJZY&location=2617))
- Contrary to value objects, entities are not immutable and are expected to change. ([Location 2674](https://readwise.io/to_kindle?action=open&asin=B09J2CMJZY&location=2674))
- Aggregates An aggregate is an entity: it requires an explicit identification field and its state is expected to change during an instance’s lifecycle. However, it is much more than just an entity. The goal of the pattern is to protect the consistency of its data. Since an aggregate’s data is mutable, there are implications and challenges that the pattern has to address to keep its state consistent at all times. ([Location 2682](https://readwise.io/to_kindle?action=open&asin=B09J2CMJZY&location=2682))
- It is also important to point out that domain services have nothing to do with microservices, service-oriented architecture, or almost any other use of the word service in software engineering. It is just a stateless object used to host business logic. ([Location 3137](https://readwise.io/to_kindle?action=open&asin=B09J2CMJZY&location=3137))
