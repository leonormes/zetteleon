---
aliases: []
author:
confidence: 
created: 2024-10-31T10:38:39Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:49Z
purpose: 
review_interval: 
see_also: []
source: "https://digital.nhs.uk/services/gp-it-futures-systems/im1-pairing-integration"
source_of_truth: []
status: 
tags: []
title: im1_integration_process_guide
type:
uid: 
updated: 
version:
---

## IM1 Integration Process Guide

The Future of IM1

There are no current plans to decommission IM1. The long-term future is being considered and, in the future, there may be alternative options which replace IM1. There are no confirmed plans or timescales for this currently. 

We will provide further updates if this changes. For more information please contact:

Interface mechanisms enable separate systems to:

- read patient information
- extract information in bulk
- enter data into the other system

You can find

There are 3 existing suppliers, who providing the Foundation Solution set to meet the Foundation Capabilities on the Digital Care Services Framework, they each offer interfaces for consuming systems to integrate with, Cegedim (Vision), EMIS (EMIS Web) and TPP (SystmOne).

There are also several new suppliers who will provide the foundation set capabilities once they have completed the onboarding process for the Digital Care Services Framework.  

Each supplier of foundation capabilities must provide an 'interface mechanism' for use by third party systems to support integration between the core providing systems and specialist applications, such as clinical decision,  support, patient facing services, document management or appointments.

Interface mechanisms enable separate systems to: 

- read patient information
- extract information in bulk
- enter data into the other system

The interface mechanisms for the provider suppliers offer under the digital care services framework must comply with the [IM1 - Interface Mechanism - GP IT Futures Capabilities & Standards - Confluence (atlassian.net)](https://gpitbjss.atlassian.net/wiki/spaces/GPITF/pages/1391133895/IM1+-+Interface+Mechanism).

Any consuming supplier can apply to 'pair' their service with any provider supplier system.  

---

### Process

Complete the IM1 Clinical and Information Governance prerequisites form

Supplier Conformance Assessment List (SCAL) will be issued if prerequisites are confirmed and in place as part of the application process. Your application will be assessed for compatibility against the provider suppliers' APIs and you will need to include some information about the product you are wanting to develop. We may also ask you to submit evidence to show you meet the SCAL requirements. 

When we have confirmed your product is compatible, you will be asked to execute a Model Interface Licence with each of the provider suppliers, this will cover your use of the provider suppliers' APIs. Once the Model Interface Licence has been executed by both consumer and provider suppliers, you will be given access to a test environment so you can develop your solution using the provider supplier guidance/documentation. 

#### IM1 Process Flow

##### Initiation

- identify product
- prerequisites are confirmed and in place
- complete stage one SCAL with requested product information
- NHS England IM1 team confirms if product is viable via API
- complete model interface licence
- access to provider supplier mock API

##### Unsupported Test Phase

- develop using Pairing and Integration Pack (PIP)
- work to fully complete SCAL in preparation for assurance

##### Supported Test Phase

- once development is complete, request access to Supported Test Environment (STE), by submitting your fully completed SCAL
- work directly with provider supplier to agree assurance approach

##### Assurance

- SCAL reviewed and agreed by NHS England
- test evidence agreed or witness test undertaken
- assurance accepted by NHS England and Recommended to Connect issued
- Plan to Connect issued by provider supplier
- live product rolled out to provider supplier estate
- Model Interface Licence uplifted to include assured SCAL

##### Live

- changes to product functionality or use case, are requested via the RFC, (Request for Change), process, to the IM1 Team
- provider and consumer suppliers attend the IM1 supplier forum

---

### IM1 Live Suppliers

We have listed all the suppliers who have already completed IM1 assurance in the table below.  

| Consumer supplier | Product or system name | Provider supplier working with |
| --- | --- | --- |
| 121 Sync | Vpad1 | TPP |
| 121 Sync | Vpad 1.8.12 | EMIS |
| Abtrace | CDSS v1.0 | TPP, EMIS |
| Access Technology Group Limited | Access Elemental (Social Prescribing Platform) | TPP |
| Accenda Ltd | Integrated Care Gateway | EMIS, TPP |
| AccuRx Ltd | accuRx 1.0 | EMIS, TPP, Cegedim |
| Advanced Software Ltd | Odyssey | EMIS, TPP |
| Advanced Software Ltd | Docman 10 | Cegedim |
| Apollo | SQL Suite | EMIS, TPP, Cegedim |
| Appconnect Ltd | Appconnect Smartphone App version 1.4.5 | EMIS |
| Appt-Health | Appt Patient Engagement | EMIS, TPP |
| Aprobrium Limited | Lexacom | EMIS |
| Ardens Workplace Ltd | Ardens Manager | EMIS, TPP |
| AT Tech | Dr IQ | EMIS, TPP |
| AT Tech | EZ Analytics | EMIS, TPP |
| Avicenna Ltd | Manage My Meds | EMIS, TPP |
| Babble | Babblevoice | TPP |
| BDM Medical Limited | Doctaly Assist | EMIS |
| Better Ltd | Shared Care Planning Application (SCPA) | TPP, EMIS |
| BlackPear | Black Pear Core | TPP, EMIS |
| Blinx Solutions Ltd | PACO (Patient and Care Optimiser) | EMIS |
| Boots UK | boot.uk/nhs | EMIS, TPP, Cegedim |
| Ctalk Limited | Fire | EMIS |
| C the Signs Ltd | C the Signs Ltd | EMIS, TPP, Cegedim |
| C7 Health | Easy refer v1.0 practice | EMIS |
| Camascope | RPM | EMIS |
| Capri Healthcare | v-Consult | EMIS, TPP |
| CareIQ | CareIQ | EMIS |
| CareIS Apollo | Valida DS | TPP |
| Cerner | HealtheIntent | EMIS, TPP |
| Charac Ltd | Charac app | EMIS, TPP |
| Check Communications | Check Cloud PRS Integration | EMIS |
| Cinapsis | Cinapsis | EMIS |
| Consultant Connect Ltd | Consultant Connect (v1) | EMIS |
| Continuum Health Ltd | Anima | EMIS, TPP |
| Convenet | Convenet Platform | EMIS, TPP, Cegedim |
| Crescendo Systems Limited | DigiScribe-XL Digital Dictation Workflow (v5) | EMIS |
| CSharp | Patally | EMIS, TPP, Cegedim |
| Ctalk Limited | Fire | EMIS |
| Digital Medical Supply (LIVI) | LIVI UK | EMIS |
| Doctorlink Limited | Doctorlink v1 | EMIS, TPP, Cegedim |
| DXS International plc | DXS Point-of-Care | EMIS |
| DXS International plc | Expert Care | EMIS, TPP |
| eConsult Health Ltd | eConsult Toolbar | TPP, EMIS |
| Egton Medical Information System Ltd | Patient Access | TPP |
| EK Interactive Innovations Ltd | Self-screening health kiosk | EMIS |
| Edenbridge | APEX | EMIS |
| Engage Health Systems | Engage Touch | EMIS, TPP |
| Engage Health Systems | Engage Consult | EMIS |
| Evergreen | ELG APP | EMIS, TPP, Cegedim |
| Evergreen | Evergreen Connect | EMIS, TPP |
| FITFILE Group Limited | FITFILE | EMIS |
| Gamma Telecom Ltd | Horizon Care Connect | EMIS, TPP |
| Gorgemead Ltd | myCohens | EMIS, TPP |
| Health Intelligence | HI Hub | EMIS |
| Healthcare Monitors UK Ltd | PatientPod 1.1 | EMIS |
| Healthcheck Services | Keito K9 | EMIS, TPP |
| Healthera Ltd | Healthera | EMIS, TPP |
| Healthy. IO (UK) LTD | Minuteful for Wound | TPP |
| Hero Doctor Limited | Hero Health | EMIS, TPP |
| Hippo Labs Ltd | Hippo Recaller | EMIS |
| iatro | Practice365 | EMIS |
| Informatica (BMJ) | iCAP Server (Skyline) | EMIS, TPP |
| inVita Intelligence | INRstar | EMIS |
| iGPR Technologies | Check my record | EMIS, TPP |
| iGPR Technologies | iGPR | EMIS, TPP |
| Informatica (BMJ) | Audit+ | EMIS |
| Informatica (BMJ) | Front Desk | EMIS, Cegedim |
| Informatica (BMJ) | iCAP Contract+ | EMIS |
| Informatica (BMJ) | iCAP Server (Skyline) | EMIS |
| Innox Trading Limited | Chemist 4 U API Services | EMIS, TPP |
| iPlato | MyGP | EMIS, TPP |
| iPlato Healthcare Ltd | MyGP Connect | EMIS |
| Jayex | Connect Platform | EMIS, TPP |
| Joy | Joy App | EMIS, TPP |
| MedAdvisor Welam UK | Day Lewis App | EMIS, TPP |
| MedAdvisor Welam UK | MedAdvisor App | EMIS, TPP |
| Medicalchain.com Ltd | MyClinic.com | EMIS |
| Medicinechest Limited | The Pharmacy Centre website/app platform | EMIS, TPP |
| Medidata Exchange Limited | eMR | EMIS, TPP Cegedim |
| Medlink Solutions Ltd | MedLink Recall | EMIS |
| Medlink Solutions Ltd | Medlink Workflow | EMIS |
| Medloop | Medloop Patient V1 | EMIS |
| Medloop | Medloop Doctor V1 | EMIS |
| Medloop | Medloop Doctor V2 | EMIS |
| Mendelian | MendelScan | TPP |
| Metabolic Healthcare | Echo | EMIS, TPP |
| Metadvice Ltd | Analytics Metadvice | EMIS, TPP |
| Microtech | Healthportal | EMIS |
| MJog Limited | MJog Premium | EMIS |
| Mondago | UC Client | EMIS, TPP |
| Monmedical Ltd (trading as Cinapsis) | Cinapsis | TPP |
| My Way Digital | My Diabetes Clinical and Analytics | EMIS, TPP |
| My Way Digital | My Way Diabetes | EMIS, TPP, Cegedim |
| MyRightCare | v3 | EMIS, TPP |
| NHS Digital | NHS App | EMIS, TPP, Cegedim |
| NHS North East London ICB | Discovery Data Service | EMIS, TPP, Cegedim |
| NHS North East London ICB | London Health Data Service | EMIS |
| Norty Limited T/A T-Pro | T-Pro | EMIS |
| Numark Digital Ltd | Hey Pharmacist | EMIS, TPP, Cegedim |
| Numed Holdings Ltd | Envisage Patient Check-in | EMIS, TPP, Cegedim |
| Numed Holdings Ltd (t/a Numed Healthcare) | Intelligent Integration Interface (i3) | EMIS |
| Nurturey Limited | Nurturey | EMIS, TPP |
| Nye Health | Nye v0.1 (Patient) | EMIS |
| Nye Health | Nye v0.1 (Transactional) | EMIS |
| Omron Healthcare | Viso | EMIS, TPP |
| Optimise Health Ltd | Optimise BP | EMIS, TPP |
| Optimum Patient Care Ltd (OPC) | OPC-ONE | EMIS |
| Optum Health Solutions (UK) | Patient Navigator | TPP |
| Optum Health Solutions (UK) | Primary Care Demand Management | EMIS, TPP |
| Patchs Health | Patchs Health | EMIS, TPP |
| Patients Know Best (PKB) | Personal Health Record | EMIS |
| PCTI (Advanced) | Odyssey | EMIS, TPP |
| Pharmacy 2U | P2U-IM1-V1.0 | EMIS, Cegedim |
| PharmacyX | PharmacyX | EMIS |
| Plans4rehab | GPOnCall | EMIS |
| Prescribing Services Limited | Advice and Guidance (Eclipse Live) | EMIS |
| Priority Digital Health Ltd | pdh.platform | TPP |
| Promatica Digital | Social Rx Connect | TPP |
| Qrypta | Swiftly | EMIS |
| Quicksilva | conneQt Toolbar (including Partners Doctrin) | EMIS, TPP |
| Quicksilva | connecQt Toolbar (including Partners Feebris) | EMIS, TPP |
| Rapid Health Limited | Rapid Health | TPP |
| Redwood | Practice Plus | EMIS |
| Remote Check In | Remote Check In | TPP |
| Schappit | FootFall | TPP |
| SmartLife Health | Smart Life | EMIS |
| Solcom | Whzan | EMIS, TPP |
| Spryt | Asa | EMIS |
| Storacall Technology | Surgery Connect | EMIS, TPP |
| Suvera | Suvera Integration API | EMIS |
| Targett Business Technologies | RIVIAM Citizen Portal | TPP |
| TCR Nottingham | Censura, (Healthchecks) | EMIS |
| TCR Nottingham | Censura, (Reporting) | EMIS |
| Technomed Ltd | ECG On-Demand | EMIS |
| Total Billing Solutions | Medibooks | TPP |
| Total Billing Solutions | GP-Billing | EMIS, TPP |
| Umedeor | uMed Life Science Platform | EMIS, TPP |
| Virtually Health Systems Ltd | Virtually Primary and Integrated Care (v2.2) | EMIS, TPP |
| Visiba Uk Ltd | Visiba Care | EMIS |
| Vitalograph | Vitalograph Connect | EMIS |
| Voice Connect | Patient Partner | EMIS |
| World Data Exchange | Digi.me | EMIS |

- Consumer supplier121 Sync
- Product or system name Vpad1
- Provider supplier working with TPP
- Consumer supplier121 Sync
- Product or system name Vpad 1.8.12
- Provider supplier working with EMIS
- Consumer supplierAbtrace
- Product or system name CDSS v1.0
- Provider supplier working with TPP, EMIS
- Consumer supplierAccess Technology Group Limited
- Product or system name Access Elemental (Social Prescribing Platform)
- Provider supplier working with TPP
- Consumer supplierAccenda Ltd
- Product or system name Integrated Care Gateway
- Provider supplier working with EMIS, TPP
- Consumer supplierAccuRx Ltd
- Product or system name accuRx 1.0
- Provider supplier working with EMIS, TPP, Cegedim
- Consumer supplierAdvanced Software Ltd
- Product or system name Odyssey
- Provider supplier working with EMIS, TPP
- Consumer supplierAdvanced Software Ltd
- Product or system name Docman 10
- Provider supplier working with Cegedim
- Consumer supplierApollo
- Product or system name SQL Suite
- Provider supplier working with EMIS, TPP, Cegedim
- Consumer supplierAppconnect Ltd
- Product or system name Appconnect Smartphone App version 1.4.5
- Provider supplier working with EMIS
- Consumer supplierAppt-Health
- Product or system name Appt Patient Engagement
- Provider supplier working with EMIS, TPP
- Consumer supplierAprobrium Limited
- Product or system name Lexacom
- Provider supplier working with EMIS
- Consumer supplierArdens Workplace Ltd
- Product or system name Ardens Manager
- Provider supplier working with EMIS, TPP
- Consumer supplierAT Tech
- Product or system name Dr IQ
- Provider supplier working with EMIS, TPP
- Consumer supplierAT Tech
- Product or system name EZ Analytics
- Provider supplier working with EMIS, TPP
- Consumer supplierAvicenna Ltd
- Product or system name Manage My Meds
- Provider supplier working with EMIS, TPP
- Consumer supplierBabble
- Product or system name Babblevoice
- Provider supplier working with TPP
- Consumer supplierBDM Medical Limited
- Product or system name Doctaly Assist
- Provider supplier working with EMIS
- Consumer supplierBetter Ltd
- Product or system name Shared Care Planning Application (SCPA)
- Provider supplier working with TPP, EMIS
- Consumer supplierBlackPear
- Product or system name Black Pear Core
- Provider supplier working with TPP, EMIS
- Consumer supplierBlinx Solutions Ltd
- Product or system name PACO (Patient and Care Optimiser)
- Provider supplier working with EMIS
- Consumer supplierBoots UK
- Product or system name boot.uk/nhs
- Provider supplier working with EMIS, TPP, Cegedim
- Consumer supplierCtalk Limited
- Product or system name Fire
- Provider supplier working with EMIS
- Consumer supplierC the Signs Ltd
- Product or system name C the Signs Ltd
- Provider supplier working with EMIS, TPP, Cegedim
- Consumer supplierC7 Health
- Product or system name Easy refer v1.0 practice
- Provider supplier working with EMIS
- Consumer supplierCamascope
- Product or system name RPM
- Provider supplier working with EMIS
- Consumer supplierCapri Healthcare
- Product or system name v-Consult
- Provider supplier working with EMIS, TPP
- Consumer supplierCareIQ
- Product or system name CareIQ
- Provider supplier working with EMIS
- Consumer supplierCareIS Apollo
- Product or system name Valida DS
- Provider supplier working with TPP
- Consumer supplierCerner
- Product or system name HealtheIntent
- Provider supplier working with EMIS, TPP
- Consumer supplierCharac Ltd
- Product or system name Charac app
- Provider supplier working with EMIS, TPP
- Consumer supplierCheck Communications
- Product or system name Check Cloud PRS Integration
- Provider supplier working with EMIS
- Consumer supplierCinapsis
- Product or system name Cinapsis
- Provider supplier working with EMIS
- Consumer supplierConsultant Connect Ltd
- Product or system name Consultant Connect (v1)
- Provider supplier working with EMIS
- Consumer supplierContinuum Health Ltd
- Product or system name Anima
- Provider supplier working with EMIS, TPP
- Consumer supplierConvenet
- Product or system name Convenet Platform
- Provider supplier working with EMIS, TPP, Cegedim
- Consumer supplierCrescendo Systems Limited
- Product or system name DigiScribe-XL Digital Dictation Workflow (v5)
- Provider supplier working with EMIS
- Consumer supplierCSharp
- Product or system name Patally
- Provider supplier working with EMIS, TPP, Cegedim
- Consumer supplierCtalk Limited
- Product or system name Fire
- Provider supplier working with EMIS
- Consumer supplierDigital Medical Supply (LIVI)
- Product or system name LIVI UK
- Provider supplier working with EMIS
- Consumer supplierDoctorlink Limited
- Product or system name Doctorlink v1
- Provider supplier working with EMIS, TPP, Cegedim
- Consumer supplierDXS International plc
- Product or system name DXS Point-of-Care
- Provider supplier working with EMIS
- Consumer supplierDXS International plc
- Product or system name Expert Care
- Provider supplier working with EMIS, TPP
- Consumer suppliereConsult Health Ltd
- Product or system name eConsult Toolbar
- Provider supplier working with TPP, EMIS
- Consumer supplierEgton Medical Information System Ltd
- Product or system name Patient Access
- Provider supplier working with TPP
- Consumer supplierEK Interactive Innovations Ltd
- Product or system name Self-screening health kiosk
- Provider supplier working with EMIS
- Consumer supplierEdenbridge
- Product or system name APEX
- Provider supplier working with EMIS
- Consumer supplierEngage Health Systems
- Product or system name Engage Touch
- Provider supplier working with EMIS, TPP
- Consumer supplierEngage Health Systems
- Product or system name Engage Consult
- Provider supplier working with EMIS
- Consumer supplierEvergreen
- Product or system name ELG APP
- Provider supplier working with EMIS, TPP, Cegedim
- Consumer supplierEvergreen
- Product or system name Evergreen Connect
- Provider supplier working with EMIS, TPP
- Consumer supplierFITFILE Group Limited
- Product or system name 

FITFILE

- Provider supplier working with EMIS
- Consumer supplierGamma Telecom Ltd
- Product or system name Horizon Care Connect
- Provider supplier working with EMIS, TPP
- Consumer supplierGorgemead Ltd
- Product or system name myCohens
- Provider supplier working with EMIS, TPP
- Consumer supplierHealth Intelligence
- Product or system name HI Hub
- Provider supplier working with EMIS
- Consumer supplierHealthcare Monitors UK Ltd
- Product or system name 

PatientPod 1.1

- Provider supplier working with EMIS
- Consumer supplierHealthcheck Services
- Product or system name Keito K9
- Provider supplier working with EMIS, TPP
- Consumer supplierHealthera Ltd
- Product or system name Healthera
- Provider supplier working with EMIS, TPP
- Consumer supplierHealthy. IO (UK) LTD
- Product or system name Minuteful for Wound
- Provider supplier working with TPP
- Consumer supplierHero Doctor Limited
- Product or system name Hero Health
- Provider supplier working with EMIS, TPP
- Consumer supplierHippo Labs Ltd
- Product or system name Hippo Recaller
- Provider supplier working with EMIS
- Consumer supplieriatro
- Product or system name Practice365
- Provider supplier working with EMIS
- Consumer supplierInformatica (BMJ)
- Product or system name iCAP Server (Skyline)
- Provider supplier working with EMIS, TPP
- Consumer supplierinVita Intelligence
- Product or system name INRstar
- Provider supplier working with EMIS
- Consumer supplieriGPR Technologies
- Product or system name Check my record
- Provider supplier working with EMIS, TPP
- Consumer supplieriGPR Technologies
- Product or system name iGPR
- Provider supplier working with EMIS, TPP
- Consumer supplierInformatica (BMJ)
- Product or system name Audit+
- Provider supplier working with EMIS
- Consumer supplierInformatica (BMJ)
- Product or system name Front Desk
- Provider supplier working with EMIS, Cegedim
- Consumer supplierInformatica (BMJ)
- Product or system name iCAP Contract+
- Provider supplier working with EMIS
- Consumer supplierInformatica (BMJ)
- Product or system name iCAP Server (Skyline)
- Provider supplier working with EMIS
- Consumer supplierInnox Trading Limited
- Product or system name Chemist 4 U API Services
- Provider supplier working with EMIS, TPP
- Consumer supplieriPlato
- Product or system name MyGP
- Provider supplier working with EMIS, TPP
- Consumer supplieriPlato Healthcare Ltd
- Product or system name MyGP Connect
- Provider supplier working with EMIS
- Consumer supplierJayex
- Product or system name Connect Platform
- Provider supplier working with EMIS, TPP
- Consumer supplierJoy
- Product or system name Joy App
- Provider supplier working with EMIS, TPP
- Consumer supplierMedAdvisor Welam UK
- Product or system name Day Lewis App
- Provider supplier working with EMIS, TPP
- Consumer supplierMedAdvisor Welam UK
- Product or system name MedAdvisor App
- Provider supplier working with EMIS, TPP
- Consumer supplierMedicalchain.com Ltd
- Product or system name MyClinic.com
- Provider supplier working with EMIS
- Consumer supplierMedicinechest Limited
- Product or system name The Pharmacy Centre website/app platform
- Provider supplier working with EMIS, TPP
- Consumer supplierMedidata Exchange Limited
- Product or system name eMR
- Provider supplier working with EMIS, TPP Cegedim
- Consumer supplierMedlink Solutions Ltd
- Product or system name MedLink Recall
- Provider supplier working with EMIS
- Consumer supplierMedlink Solutions Ltd
- Product or system name Medlink Workflow
- Provider supplier working with EMIS
- Consumer supplierMedloop
- Product or system name Medloop Patient V1
- Provider supplier working with EMIS
- Consumer supplierMedloop
- Product or system name Medloop Doctor V1
- Provider supplier working with EMIS
- Consumer supplierMedloop
- Product or system name Medloop Doctor V2
- Provider supplier working with EMIS
- Consumer supplierMendelian
- Product or system name MendelScan
- Provider supplier working with TPP
- Consumer supplierMetabolic Healthcare
- Product or system name Echo
- Provider supplier working with EMIS, TPP
- Consumer supplierMetadvice Ltd
- Product or system name Analytics Metadvice
- Provider supplier working with EMIS, TPP
- Consumer supplierMicrotech
- Product or system name Healthportal
- Provider supplier working with EMIS
- Consumer supplierMJog Limited
- Product or system name MJog Premium
- Provider supplier working with EMIS
- Consumer supplierMondago
- Product or system name UC Client
- Provider supplier working with EMIS, TPP
- Consumer supplierMonmedical Ltd (trading as Cinapsis)
- Product or system name Cinapsis
- Provider supplier working with TPP
- Consumer supplierMy Way Digital
- Product or system name My Diabetes Clinical and Analytics
- Provider supplier working with EMIS, TPP
- Consumer supplierMy Way Digital
- Product or system name My Way Diabetes
- Provider supplier working with EMIS, TPP, Cegedim
- Consumer supplierMyRightCare
- Product or system name v3
- Provider supplier working with EMIS, TPP
- Consumer supplierNHS Digital
- Product or system name NHS App
- Provider supplier working with EMIS, TPP, Cegedim
- Consumer supplierNHS North East London ICB
- Product or system name Discovery Data Service
- Provider supplier working with EMIS, TPP, Cegedim
- Consumer supplierNHS North East London ICB
- Product or system name London Health Data Service
- Provider supplier working with EMIS
- Consumer supplierNorty Limited T/A T-Pro
- Product or system name T-Pro
- Provider supplier working with EMIS
- Consumer supplierNumark Digital Ltd
- Product or system name  Hey Pharmacist
- Provider supplier working with EMIS, TPP, Cegedim
- Consumer supplierNumed Holdings Ltd
- Product or system name Envisage Patient Check-in
- Provider supplier working with EMIS, TPP, Cegedim
- Consumer supplierNumed Holdings Ltd (t/a Numed Healthcare)
- Product or system name Intelligent Integration Interface (i3)
- Provider supplier working with EMIS
- Consumer supplierNurturey Limited
- Product or system name Nurturey
- Provider supplier working with EMIS, TPP
- Consumer supplierNye Health
- Product or system name Nye v0.1 (Patient)
- Provider supplier working with EMIS
- Consumer supplierNye Health
- Product or system name Nye v0.1 (Transactional)
- Provider supplier working with EMIS
- Consumer supplierOmron Healthcare
- Product or system name Viso
- Provider supplier working with EMIS, TPP
- Consumer supplierOptimise Health Ltd
- Product or system name Optimise BP
- Provider supplier working with EMIS, TPP
- Consumer supplierOptimum Patient Care Ltd (OPC)
- Product or system name OPC-ONE
- Provider supplier working with EMIS
- Consumer supplierOptum Health Solutions (UK)
- Product or system name Patient Navigator
- Provider supplier working with TPP
- Consumer supplierOptum Health Solutions (UK)
- Product or system name Primary Care Demand Management
- Provider supplier working with EMIS, TPP
- Consumer supplierPatchs Health
- Product or system name Patchs Health
- Provider supplier working with EMIS, TPP
- Consumer supplierPatients Know Best (PKB)
- Product or system name Personal Health Record
- Provider supplier working with EMIS
- Consumer supplierPCTI (Advanced)
- Product or system name Odyssey
- Provider supplier working with EMIS, TPP
- Consumer supplierPharmacy 2U
- Product or system name P2U-IM1-V1.0
- Provider supplier working with EMIS, Cegedim
- Consumer supplierPharmacyX
- Product or system name PharmacyX
- Provider supplier working with EMIS
- Consumer supplierPlans4rehab
- Product or system name GPOnCall
- Provider supplier working with EMIS
- Consumer supplierPrescribing Services Limited
- Product or system name Advice and Guidance (Eclipse Live)
- Provider supplier working with EMIS
- Consumer supplierPriority Digital Health Ltd
- Product or system name pdh.platform
- Provider supplier working with TPP
- Consumer supplierPromatica Digital
- Product or system name Social Rx Connect
- Provider supplier working with TPP
- Consumer supplierQrypta
- Product or system name Swiftly
- Provider supplier working with EMIS
- Consumer supplierQuicksilva
- Product or system name conneQt Toolbar (including Partners Doctrin)
- Provider supplier working with EMIS, TPP
- Consumer supplierQuicksilva
- Product or system name connecQt Toolbar (including Partners Feebris)
- Provider supplier working with EMIS, TPP
- Consumer supplierRapid Health Limited
- Product or system name Rapid Health
- Provider supplier working with TPP
- Consumer supplierRedwood
- Product or system name Practice Plus
- Provider supplier working with EMIS
- Consumer supplierRemote Check In
- Product or system name Remote Check In
- Provider supplier working with TPP
- Consumer supplierSchappit
- Product or system name FootFall
- Provider supplier working with TPP
- Consumer supplierSmartLife Health
- Product or system name Smart Life
- Provider supplier working with EMIS
- Consumer supplierSolcom
- Product or system name Whzan
- Provider supplier working with EMIS, TPP
- Consumer supplierSpryt
- Product or system name Asa
- Provider supplier working with EMIS
- Consumer supplierStoracall Technology
- Product or system name Surgery Connect
- Provider supplier working with EMIS, TPP
- Consumer supplierSuvera
- Product or system name Suvera Integration API
- Provider supplier working with EMIS
- Consumer supplierTargett Business Technologies
- Product or system name RIVIAM Citizen Portal
- Provider supplier working with TPP
- Consumer supplierTCR Nottingham
- Product or system name Censura, (Healthchecks)
- Provider supplier working with EMIS
- Consumer supplierTCR Nottingham
- Product or system name Censura, (Reporting)
- Provider supplier working with EMIS
- Consumer supplierTechnomed Ltd
- Product or system name ECG On-Demand
- Provider supplier working with EMIS
- Consumer supplierTotal Billing Solutions
- Product or system name Medibooks
- Provider supplier working with TPP
- Consumer supplierTotal Billing Solutions
- Product or system name GP-Billing
- Provider supplier working with EMIS, TPP
- Consumer supplierUmedeor
- Product or system name uMed Life Science Platform
- Provider supplier working with EMIS, TPP
- Consumer supplierVirtually Health Systems Ltd
- Product or system name Virtually Primary and Integrated Care (v2.2)
- Provider supplier working with EMIS, TPP
- Consumer supplierVisiba Uk Ltd
- Product or system name Visiba Care
- Provider supplier working with EMIS
- Consumer supplierVitalograph
- Product or system name Vitalograph Connect
- Provider supplier working with EMIS
- Consumer supplierVoice Connect
- Product or system name Patient Partner
- Provider supplier working with EMIS
- Consumer supplierWorld Data Exchange
- Product or system name Digi.me
- Provider supplier working with EMIS

---

### Other Services

Services available directly to patients have been broken down by system supplier. They can be accessed on the following links.

Last edited: 28 October 2024 1:34 pm
