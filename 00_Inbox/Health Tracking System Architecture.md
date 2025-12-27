---
aliases: []
tags: []
title: Health Tracking System Architecture
type: ""
status: ""
confidence: ""
epistemic: ""
purpose: ""
modified: 2025-12-27T11:55:00+00:00
last_reviewed: ""
review_interval: ""
see_also: []
source_of_truth: []
created: 2025-12-27T10:59:38+00:00
---

## 1. System Stack

- **Data Warehouse:** Fitbit (via Pixel Watch 4).
- **Capture Interface:** Nutracheck (UK-specific database).
- **Intelligence Layer:** Gemini (Custom Gems).
- **Planning Layer:** Mealia / Samsung Food (UK Supermarket integration).

---

## 2. Interface Layer (Daily Execution)

### A. Nutritional Capture (Nutracheck)

- **Logic:** Use for all food logging due to UK barcode accuracy.
- **Efficiency Hack:** Use the **"My Meals"** feature to create composite objects (e.g., "Alpen + 150ml Semi-Skimmed Milk"). This eliminates "silent deficits" and reduces daily taps.
- **Water Log:** Log water via the **Pixel Watch 4 Tile** or **Google Assistant** ("Log 500ml of water to Fitbit") to ensure it hits the core database.

### B. Biometric Capture (Pixel Watch 4)

- **Passive:** Heart Rate, Sleep, HRV, and Activity Load.
- **Active:** Use the "Exercise" app for specific sessions to ensure high-fidelity caloric expenditure data.

---

## 3. Integration Layer (Data Flow)

|**Source**|**Direction**|**Destination**|**Data Payload**|
|---|---|---|---|
|**Nutracheck**|$\rightarrow$|**Fitbit**|Calories, Protein, Carbs, Fat, Fibre, Salt.|
|**Fitbit**|$\rightarrow$|**Nutracheck**|Steps, Active Minutes, TEE (Total Energy Expenditure).|
|**Fitbit Cloud**|$\rightarrow$|**Google Takeout**|Granular JSON/CSV files for LLM ingestion.|

---

## 4. Intelligence Layer (Analysis Workflow)

### The "Health Data Architect" Gem

**Frequency:** Weekly or Monthly.

1. **Extract:** Download your archive via [Google Takeout](https://takeout.google.com/) (select only Fitbit data; format: JSON).
2. **Ingest:** Upload the `Global Export Data` folder/files to your Gemini Gem.
3. **Execute:** Use the "Heuristic Audit" prompt to identify systemic errors.

**Core Gem Logic:**

> - **Audit:** Flag dry foods without liquids or raw proteins without fats.
> - **Metabolic Ratio:** Analyse the Delta between logged intake and TEE vs. biometric trends.
> - **Synthesis:** Output "Architectural Adjustments" for the coming week.

---

## 5. Feedback Loop (Planning)

### The "UK Nutritional Architect" Gem

**Frequency:** Weekly (post-analysis).

- **Input:** The findings from the Health Data Architect Gem.
- **Output:** A 7-day high-density meal plan.
- **Constraint:** Must prioritise UK supermarket availability (Tesco/Sainsbury's/Waitrose).
- **Next Step:** Export list to **Mealia** or **Samsung Food** to populate your grocery delivery basket.

---

## 6. Maintenance Checklist

- [ ] **Monthly:** Purge old Google Takeout archives to prevent data clutter.
- [ ] **Quarterly:** Review "My Meals" in Nutracheck to ensure calorie/macro density still aligns with current metabolic goals.

---
