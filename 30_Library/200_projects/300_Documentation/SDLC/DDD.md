---
aliases: []
confidence: 
created: 2025-01-02T14:50:11Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:43Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: DDD
type:
uid: 
updated: 
version:
---

## DDD

Domain-Driven Design (DDD) can be used to define business requirements and create categories within a system by focusing on the business domain, its language, and its inherent structure. DDD helps to create a shared understanding between technical teams and business experts, which results in software that better reflects the needs of the business.

Here’s how DDD can be applied to define requirements and create system categories:

- **Ubiquitous Language**: DDD emphasizes the creation of a **ubiquitous language**, which is a shared vocabulary used by both technical and business teams to describe the business domain. This language should be used in all discussions, documentation, and code, ensuring that everyone has the same understanding of the concepts and terms. The ubiquitous language is derived from conversations with domain experts and captures the concepts and terms of the specific business domain. Gherkin scenarios can be a great source of a ubiquitous language, as each scenario is a record of a conversation between business experts and technical experts. This language acts as the foundation for the design of the software, and helps communication between software developers and domain experts.
- **Domain Experts**: DDD brings **domain experts** and software developers together to develop software that reflects the mental model of the business experts. This ensures that the software is as close as possible to what business experts would create if they were the coders.
- **Strategic Design**: DDD includes strategic design, which helps to understand the business domain and its subdomains. This involves identifying the **core**, **supporting**, and **generic** subdomains of the business. A subdomain resembles a set of interrelated use cases.
    - The **core domain** is where the most value should be added in the system.
    - **Supporting subdomains** model aspects of the business that are essential but not core.
    - **Generic subdomains** capture aspects required for the overall solution that are not specific to the business.
    - By focusing on the core complexity, DDD helps to ensure that the most important areas of the business are given the attention they deserve.
- **Bounded Contexts**: DDD uses **bounded contexts** to define the scope of a specific domain model. A bounded context is a conceptual boundary where a domain model and its ubiquitous language are applicable. This helps to prevent the mixing of responsibilities between different parts of the system. Each context should have its own unified model. Bounded contexts are aligned with the division of business functions and technical teams. They also provide a clear boundary for the ubiquitous language. Bounded contexts also help in modelling by specifying the purpose of the boundary, dividing the responsibility of languages. A single bounded context does not necessarily fall within a single subdomain, but it may.
- **Context Maps**: **Context Maps** show the relationships between different bounded contexts. They help to visualise the different languages and models at play in an organisation and inform strategic decisions. Context maps can also show how different contexts integrate with each other.
- **Modelling**: DDD is about modelling the domain, as opposed to modelling data. DDD recognises that a unified model for a large system is not feasible or cost-effective. It forces thinking about individual models for different contexts, rather than trying to create a single universal model. Models should capture the domain experts' mental models. The model needs to be unified to be internally consistent.
- **Identifying Business Rules:** DDD helps to capture business rules in the design. Business rules can be documented using a type system that represents what is valid or invalid, so that the compiler can check it.
- **User Stories:** User stories can be linked to specific use cases within the domain. Application Service methods can be modified to deal with a single use case flow or user story. The user interface should express the underlying abstractions of the domain through the use of the ubiquitous language.
- **Event Storming:** Techniques such as **Event Storming** can be used to capture the flow of business events and help to build a shared vision for the product. This is a collaborative exercise that helps to build up a shared vision for the product.
- **Tactical Design**: Once the strategic design is complete, **tactical design** patterns are used to create the executable software deliverables. These patterns help to implement the domain model in code, and ensure that the code "speaks" the ubiquitous language.

By using these DDD principles, you can define clear business requirements, create a well-organized system with logical boundaries, and build software that truly meets the needs of the business. The use of a ubiquitous language ensures that all stakeholders have a shared understanding, and the focus on the domain model ensures that the software is aligned with business goals.
