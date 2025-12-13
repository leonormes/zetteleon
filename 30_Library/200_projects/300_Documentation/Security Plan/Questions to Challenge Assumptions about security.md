---
aliases: []
confidence: 
created: 2025-03-18T11:14:26Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:43Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [security]
title: Questions to Challenge Assumptions about security
type: question
uid: 
updated: 
version: 
---

## Questions to Challenge Assumptions

- **Beyond Authentication:**
    - “What would happen if an attacker managed to bypass or steal valid authentication tokens? What additional controls do we have in place?”
    - “If a service or component is compromised, how does that impact our system’s overall security?”
- **Trust Boundaries and Internal Threats:**
    - “What assumptions are we making about the trustworthiness of internal services or third-party components? How are we verifying their security?”
    - “How do we enforce the principle of least privilege within our system? Are we assuming that authenticated users automatically deserve full access?”
- **Data Protection and Encryption:**
    - “How is data protected in transit and at rest? Do we rely solely on authentication, or do we also use robust encryption and key management?”
    - “What assumptions have we made about the security of our encryption implementations?”
- **Network and Distributed System Risks:**
    - “Distributed systems introduce challenges like network latency, packet loss, and unreliable connections. How do these factors affect our security posture?”
    - “How resilient is our design to issues like misconfigurations or unexpected failures in one part of the system?”
- **Incident Detection and Response:**
    - “What monitoring and logging mechanisms are in place to detect potential breaches or anomalous behavior?”
    - “How do we plan to respond if a security incident is detected, especially if it involves internal components?”
- **Threat Modelling and Risk Assessment:**
    - “Have we performed a threat modelling exercise to identify potential attack vectors beyond authentication, such as injection attacks or misconfigurations?”
    - “What are our assumptions about the cost and likelihood of different attack scenarios?”

## Approaches to Facilitate Open Discussion

- **Misuse Case Scenarios:** Ask developers to describe “what if” situations. For example, “Describe a scenario where an insider misuses their access even though they’re authenticated. How would our system prevent or mitigate this?”
- **Peer Review Sessions:** Organize sessions where teams discuss their security assumptions and critique each other’s designs. This encourages a culture of “security as a team responsibility” rather than an afterthought.
- **Link to Known Fallacies:** Introduce the "Fallacies of Distributed Computing" to illustrate that assumptions such as “the network is secure” or “authentication makes everything safe” are common pitfalls.
- **Real-world Examples:** Present case studies or recent breaches where authentication was only one piece of a larger security failure. Ask, “What could have been done differently if we had considered these additional factors?”

By incorporating these questions into design reviews or threat modelling sessions, you encourage developers to articulate and then challenge their own assumptions about data security in distributed systems. This broader perspective can help validate claims and drive the adoption of more robust, layered security strategies.
