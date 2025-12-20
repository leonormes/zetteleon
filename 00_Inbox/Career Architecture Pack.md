---
aliases: []
confidence: 
created: 2025-12-19T02:50:28Z
epistemic: 
last_reviewed: 
modified: 2025-12-20T09:54:03Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Career Architecture Pack
type: 
uid: 
updated: 
---

## Career Architecture Pack: Leon Ormes
**Generated:** 19 December 2025
**Version:** 1.0 (Final Architecture)

---

### Table of Contents
1. [Master CV](#1-master-cv)
2. [Strategic Cover Letter](#2-strategic-cover-letter)
3. [LinkedIn Profile Optimisation](#3-linkedin-profile-optimisation)
4. [Interview Architecture (Deep Dives)](#4-interview-architecture-deep-dives)
5. [Salary Negotiation Script](#5-salary-negotiation-script)

---

### 1. Master CV

**Leon Ormes**
**Location:** Leigh-on-Sea, United Kingdom
**Contact:** 07896350700 | leonormes@gmail.com
**Links:** [LinkedIn](https://www.linkedin.com/in/leonormes)

#### **Professional Profile**
**Senior DevOps & Platform Engineer** transitioning from a strong software engineering background. Specialises in architecting secure, compliant, and scalable cloud-native infrastructures within high-regulatory environments (Healthcare/FinTech).

- **Core Competency:** Bridging the gap between application logic and infrastructure. Expert in transforming manual, high-error deployment processes into automated, "single-command" GitOps workflows.
- **Architectural Focus:** Zero Trust security principles, Privacy-Preserving Data Analytics (federated learning/MPC), and Infrastructure as Code (IaC) modularisation.
- **Operational Philosophy:** Implementation of DORA metrics to drive efficiency, TDD/BDD/DDD for reliability, and reduction of cognitive load for developer teams through platform standardisation.

#### **Technical Architecture Stack**

| Domain | Technologies & Frameworks |
| :--- | :--- |
| **Cloud & Infrastructure** | AWS (EKS, EC2, VPC), Azure (AKS, VNets, NSGs), Terraform (IaC), Terraform Cloud |
| **Orchestration & GitOps** | Kubernetes (K8s), Helm, ArgoCD, Docker, GitHub Actions, GitLab CI/CD |
| **Security & Identity** | HashiCorp Vault, Auth0, ISO 27001/HIPAA compliance, Trivy, SonarQube, Zero-Trust |
| **Observability** | Grafana, Prometheus, ELK Stack, Azure Monitor, DORA Metrics implementation |
| **Backend & Languages** | Node.js, TypeScript, JavaScript, Go (Golang), Python, SQL (Postgres), GraphQL |

#### **Professional Experience**

**FITFILE | Senior Engineer / Platform Engineer**
*Remote / London, UK | October 2022 – Present*
*FITFILE provides privacy-enhancing technologies for healthcare data analytics.*

**High-Level Achievement:** Architected a comprehensive Terraform-based platform for automating customer onboarding, reducing deployment time by **86%** (70 mins to 10 mins) and error rates from **22% to 3%**.

- **Infrastructure Architecture:** Spearheaded the "central-services repository" strategy, establishing a single source of truth for all deployment configurations. Developed reusable Terraform modules for multi-service orchestration, achieving >99.9% module execution success.
- **Security & Compliance:** Enforced NHS Trust compliance and ISO 27001 standards via automated policy-as-code. Implemented Zero-Trust networking (Azure VNets, NSGs, forced tunnelling) and managed secrets via HashiCorp Vault.
- **Tooling & Automation:** Developed `chart-manager` (Go-based tool) to automate Helm chart lifecycles, scanning, and OCI registry imports, cutting standard operation times to <1 minute.
- **GitOps Implementation:** Deployed ArgoCD for declarative application management across Azure (AKS) and AWS (EKS), ensuring <5 minutes sync drift and enabling rapid rollback capabilities.

**nate | Software Engineer (Backend/DevOps)**
*London, UK | September 2021 – August 2022*
*FinTech startup focusing on universal shopping automation.*

**High-Level Achievement:** Led the transition toward DevOps culture by introducing DORA metrics and Kubernetes-native CI/CD, directly linking engineering output to business value delivery.

- **System Design:** Developed the risk assessment component of the purchase flow using Dependency Injection and Domain-Driven Design (DDD) to ensure scalability and testability.
- **Observability:** Overhauled production logging and metrics infrastructure to surface performance bottlenecks. Implemented DORA metrics monitoring to visualise deployment frequency and lead time for changes.
- **CI/CD Architecture:** Architected and deployed a K8s-native CI/CD pipeline using ArgoCD, shifting the team towards a continuous delivery model.

**Tessian | Node.js Developer**
*London, UK | February 2018 – September 2021*
*Cybersecurity company using machine learning to prevent email security breaches.*

**High-Level Achievement:** Key contributor to the email gateway server infrastructure, managing the migration from JavaScript to TypeScript to reduce technical debt and improve maintainability.

- **Core Engineering:** Maintained high-throughput Node.js email servers handling SMTP protocols, encryption, and data security at scale.
- **Culture & Quality:** Championed "Test First" methodologies and cross-team knowledge sharing. Awarded "Culture Champion" for fostering engineering excellence and breaking down silos.

**FifthMorrison | Web Developer**
*United Kingdom | June 2017 – February 2018*.

- **Full Stack Development:** Built complex web applications using Postgres, GraphQL, Express, and Angular. Responsible for end-to-end delivery of software solutions under the Lead Developer.

---

#### **Previous Experience**

**Teacher (Maths, ICT, Music)** | King John School | *September 2007 – January 2017*
- Developed high-level communication and leadership skills managing large groups.
- *Relevance:* Transferable skills in mentorship, public speaking, and simplifying complex concepts for diverse audiences.

#### **Education & Certifications**

- **General Assembly:** Web Development Immersive (2017)
- **freeCodeCamp:** Full-Stack Web Development Certification, Computer Science (2016 – 2017)

---

### 2. Strategic Cover Letter

**Leon Ormes**
Leigh-on-Sea, United Kingdom
07896350700 | leonormes@gmail.com
[LinkedIn Profile URL]

**[Date]**

**[Hiring Manager Name - or - The Engineering Team]**
**[Company Name]**

**RE: Application for [Role Title]**

Dear **[Hiring Manager Name]**,

Throughout my career in software engineering, I identified a recurring structural inefficiency: development teams are frequently bottlenecked not by their ability to write code, but by the friction involved in shipping it securely and reliably. I transitioned from Full Stack development to Platform Engineering to solve this specific architectural problem. I am writing to apply for the **[Role Title]** position at **[Company Name]**, where I can leverage my background in application logic to build robust, developer-centric infrastructure.

My approach to DevOps is grounded in the "Platform as a Product" mental model. I do not simply manage servers; I architect self-service frameworks that reduce cognitive load for developers while enforcing strict compliance and security standards by default.

At **FITFILE**, I applied this philosophy to dismantle a high-friction customer onboarding process. By architecting a comprehensive Terraform-based platform and treating infrastructure as code, I reduced onboarding time by **86%** (from 70 minutes to 10 minutes) and slashed error rates from **22% to 3%**. This was not merely an operational improvement but a fundamental shift in how the business delivers value to NHS Trusts under strict ISO 27001 constraints.

Previously at **nate**, I implemented DORA metrics and Kubernetes-native GitOps (ArgoCD) to provide objective visibility into engineering performance. My background as a software engineer—specifically using TDD and Domain-Driven Design—allows me to empathise with application developers and build tooling that fits naturally into their workflow, rather than imposing external constraints.

I am seeking a role where I can continue to design high-leverage platforms that abstract away infrastructure complexity, allowing engineering teams to focus purely on business logic.

I would welcome the opportunity to discuss how my architectural approach to Platform Engineering can drive efficiency at **[Company Name]**.

Yours sincerely,

**Leon Ormes**

---

### 3. LinkedIn Profile Optimisation

**Headline:**
Senior Platform Engineer | DevOps Architect | Kubernetes, Terraform & Zero Trust | Ex-Tessian, nate

**About Section:**

**Senior DevOps & Platform Engineer | Architecting Efficiency & Compliance**

I operate at the intersection of Software Engineering and Infrastructure, applying strict architectural principles (TDD, DDD, Zero Trust) to platform operations. My core philosophy is **"Platform as a Product"**—building self-service frameworks that abstract complexity, reduce cognitive load for developers, and enforce compliance by design.

**Core Focus:** Transforming manual, high-friction deployment processes into automated, auditable, and scalable GitOps workflows.

**Quantifiable Impact:**
- **Operational Efficiency (FITFILE):** Architected a Terraform-based onboarding platform, achieving an **86% reduction in deployment time** (70 mins to 10 mins) and cutting error rates from **22% to 3%**.
- **Engineering Visibility (nate):** Implemented DORA metrics monitoring and Kubernetes-native CI/CD (ArgoCD), directly linking engineering output to business value and increasing deployment velocity.
- **Technical Debt Reduction (Tessian):** Led the migration of core server infrastructure from JavaScript to TypeScript, enhancing code maintainability and type safety across the stack.

**Technical Architecture:**
- **Infrastructure:** AWS (EKS), Azure (AKS, VNets), Terraform (IaC).
- **Orchestration:** Kubernetes, Helm, ArgoCD, Docker.
- **Security:** HashiCorp Vault, ISO 27001/HIPAA Compliance, Zero-Trust Networking.
- **Languages:** Node.js, TypeScript, Go (Golang).

---

### 4. Interview Architecture (Deep Dives)

#### Topic A: The FITFILE Onboarding Architecture
**Question:** *"How did you reduce onboarding time by 86%?"*
- **Situation:** High-friction manual process (70 mins), mutable state, 22% error rate.
- **Action:** Implemented "Central Services" repo (Single Source of Truth), reusable Terraform modules, and a custom Go tool (`chart-manager`) for Helm lifecycles.
- **Key Concept:** **Immutability**. Replacing "repairing servers" with "re-provisioning validated state."
- **Result:** 10-minute deployment time, 3% error rate, ISO 27001 compliance enforced via code.

#### Topic B: Observability (nate)
**Question:** *"How do you measure engineering success?"*
- **Situation:** Invisible work and subjective "feelings" about speed vs. stability.
- **Action:** Implemented **DORA Metrics** (Deployment Frequency, Lead Time). Architected K8s-native CI/CD (ArgoCD) to decouple CI from CD.
- **Key Concept:** **Feedback Loops**. Making the invisible visible to drive safe velocity.
- **Result:** Shifted culture to data-driven delivery; enabled rapid, safe iteration.

#### Topic C: Security in Regulated Ops
**Question:** *"How do you handle security without slowing down devs?"*
- **Situation:** Healthcare data (NHS) requires Zero Trust, but manual security gates kill velocity.
- **Action:** **Policy as Code**. Terraform for network micro-segmentation (Azure NSGs, Forced Tunnelling). Kubernetes Network Policies (Calico) for pod-level isolation.
- **Key Concept:** **Guardrails, not Gates**. Security is baked into the platform; developers can't deploy insecurely even if they try.

---

### 5. Salary Negotiation Script

**Target Range:** £100,000 – £115,000
**Mental Model:** You are selling **leverage** (1.1x multiplier on all other devs) and **insurance** (risk mitigation).

#### Phase 1: The Anchor (When Asked for expectations)

> "Given the strategic nature of this role—specifically the requirement to architect [Key Tech] platforms rather than just maintain them—I am targeting a base salary in the region of **£110,000 to £115,000**.
>
> "This figure reflects the commercial impact I deliver. For context, in my recent role at FITFILE, my platform architecture reduced customer onboarding time by **86%**. I am looking for a role where I can replicate that level of operational efficiency."

#### Phase 2: Handling Pushback ("That's above budget")

> "I appreciate that is at the top end of the standard 'Senior DevOps' bracket. However, I am operating as a **Platform Engineer** with a focus on **Engineering Velocity** and **Compliance**.
>
> "Standard DevOps maintains the pipeline. My approach—using DORA metrics and automating infrastructure-as-code—actively multiplies the output of your entire development team. The premium for this role isn't for 'doing the work'; it is for the **risk mitigation** and the **multiplier effect**. Is the budget hard-capped, or is there flexibility for the right commercial impact?"

#### Phase 3: The Closing (The Compromise)

> "Looking at the package objectively, £95,000 is a strong starting point, but it undervalues the **Teacher-Engineer hybrid** skill set I bring. My background in teaching means I don't just build the platform; I train your teams to use it, drastically reducing the 'time-to-competence' for new hires.
>
> "If we can adjust the base to **£105,000**, I would be ready to sign immediately and start outlining the architectural roadmap before Day 1."
