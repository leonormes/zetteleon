---
aliases: [Atomic Chores Inventory, Chores List, Cleaning SOPs, Home Maintenance Registry]
conformant: false
created: 2025-12-30T10:00:00+00:00
last_reviewed: '2025-12-30'
modified: 2026-07-20T14:53:14+00:00
non_conformance_reason: "Bulk inferred type. Needs review."
permalink: llmeon/30-library/so-t/so-t-master-household-chores-inventory
status: proposal
tags: [chores, family, inventory, system]
title: SoT - Master Household Chores Inventory
type: sot
updated: null
---

## SoT - Master Household Chores Inventory

### 1. Governance Principles

- Atomic Design: Tasks are broken down into their smallest executable units (e.g., "Load" vs. "Unload") to allow for micro-assignments and precise definition of done.
- Frequency Definitions:
    - Daily: Required to maintain operational baseline (avoiding entropy).
    - Weekly: Hygiene and deep resets.
    - Monthly/Quarterly: Infrastructure maintenance.

---

### 2. Zone: Kitchen & Dining

_The engine room of the house. High throughput, high hygiene requirement._

#### Daily (Operational)

- [Atomic] Clear Table: Remove all crockery, glasses, and debris from dining table.
- [Atomic] Wipe Table: Spray and wipe dining table surface (crumb-free).
- [Atomic] Load Dishwasher: Place dirty items in racks; ensure spray arms spin freely.
- [Atomic] Unload Dishwasher: Return clean, dry items to cupboards.
- [Atomic] Wipe Counters: Sanitize food preparation surfaces.
- [Atomic] Sink Reset: Empty strainer, scrub sink basin, rinse away foam/debris.
- [Atomic] Floor Spot-Sweep: Sweep up visible crumbs/debris after meals.

#### Weekly (Hygiene)

- [Atomic] Deep Floor Clean: Vacuum edges and mop entire floor area.
- [Atomic] Microwave Interior: Steam/wipe inside of microwave.
- [Atomic] Hob Clean: Scrub stovetop and splashback.
- [Atomic] Cabinet Fronts: Wipe down cupboard doors/handles (fingerprints).

#### Monthly (Maintenance)

- [Atomic] Fridge Audit: Check dates, discard expired, wipe shelves.
- [Atomic] Bin Deep Clean: Disinfect inside of kitchen bin.
- [Atomic] Dishwasher Filter: Remove and rinse filter.

##### [SOP] Cold Storage (Fridge)
- **Definition of Done (DoD):** No visible spills, no expired items, and the drainage hole at the back is clear of ice/debris.
- **Steps:**
  1. **Extraction:** Clear one shelf at a time.
  2. **Audit:** Check Use-By dates. Wipe sticky jars.
  3. **Sanitisation:** Spray anti-bacterial; wipe with damp cloth; dry with microfibre.
  4. **Restock:** Ready-to-eat (Top), Raw Meat (Bottom/Sealed), Veg (Drawers).

---

### 3. Zone: Front Room (Living Area)

_Shared social space. Focus on clutter control and comfort._

#### Daily (Reset)

- [Atomic] Floor Clear: Remove items (shoes, toys, mugs) that do not belong.
- [Atomic] Cushion Plumping: Reset sofa cushions and fold throw blankets.

#### Weekly (Clean)

- [Atomic] Dust Surfaces: TV stand, shelves, skirting boards.
- [Atomic] Vacuum Floor: Including under coffee table and sofa edges.
- [Atomic] Glass Clean: Wipe TV screen (microfibre only) and mirrors/glass surfaces.

---

### 4. Zone: Bathrooms (X2)

_Sanitation critical zones._

#### Daily (Maintenance)

- [Atomic] Towel Reset: Hang up damp towels; put dirty ones in hamper.
- [Atomic] Sink Rinse: Rinse toothpaste/soap marks from basin.

#### Weekly (Deep Clean)

- [Atomic] Toilet Sanitation: Bleach/scrub bowl, wipe seat, lid, and flush handle.
- [Atomic] Bath/Shower Scrub: Remove grime ring/hair; rinse thoroughy.
- [Atomic] Sink Polish: Clean basin and polish taps (water-spot free).
- [Atomic] Mirror Clean: Glass cleaner for spot-free reflection.
- [Atomic] Floor Mop: Disinfectant mop of bathroom floor.
- [Atomic] Bin Empty: Empty small bathroom bin to main refuse.

##### [DoD] Bathrooms Deep Clean
- **Reflection:** Mirrors/Chrome have zero spots.
- **Surface:** No hair/dust on basin or toilet lid.
- **Sanitation:** Toilet bowl clear and smells disinfected.
- **Inventory:** Hand towel fresh, loo roll restocked.

---

### 5. Zone: Transit Areas (Hall, Stairs, Landing)

_First impressions and connecting arteries._

#### Daily

- [Atomic] Shoe Rack Tidy: Ensure shoes are paired and on the rack/in box.
- [Atomic] Coat Rack Audit: Hang up coats; remove items not currently in use.

#### Weekly

- [Atomic] Stair Vacuum: Vacuum treads and risers (corners focus).
- [Atomic] Hall/Landing Vacuum: Vacuum walkways.
- [Atomic] Dust Banisters: Wipe down handrails and spindles.

---

### 6. Zone: Private Quarters (Girls' Rooms X3 + Loft)

_Individual responsibility zones._

#### Daily (Occupant Responsibility)

- [Atomic] Bed Making: Duvet pulled up, pillows arranged.
- [Atomic] Floor Clear: No clothes or rubbish on the floor.
- [Atomic] Laundry Extraction: Dirty clothes moved to Downstairs Basket.

#### Bessie—The Night-Before Reset: Academic Kit Review

Completed each evening before downtime (by 21:00). Binary check—every item is yes/no:

- [ ] Laptop packed, charger enclosed, and device battery verified at >=80%.
- [ ] Blue-paper study notebooks, overlays, and specialist visual materials checked inside her binder.
- [ ] School/AP uniform and sensory-friendly base layers laid out.

Verification: parent sight-check at evening handover. If an item cannot be completed (e.g., laptop not charged in time), it is logged neutrally and resolved in the morning ledger—it is not carried as a fault.

#### Weekly (Occupant/Deep)

- [Atomic] Change Bedding: Strip sheets, put on fresh linen.
- [Atomic] Dust Surfaces: Desk, bedside tables, shelves.
- [Atomic] Vacuum Room: Thorough vacuum of carpet.
- [Atomic] Bin Empty: Empty room bin to main refuse.

---

### 7. Global Systems

_Tasks that span the whole house._

#### Laundry Cycle

- [Atomic] Wash Load: Separate colors, load machine, add detergent, start cycle.
- [Atomic] Transfer to Dry: Move wet clothes to dryer or hang on airer/line.
- [Atomic] Fold/Sort: Fold dry clothes and sort into piles by owner.
- [Atomic] Put Away: Return folded clothes to drawers/wardrobes.

##### [DoD] Laundry Loop (Daily)
- Bedroom floor is clear of clothes; all dirty items are inside the downstairs basket (not just near it).

#### Waste Management

- [Atomic] Indoor Consolidation: Collect bags from all indoor bins (Kitchen, Bathrooms, Bedrooms).
- [Atomic] Outdoor Disposal: Place consolidated bags into Wheelie Bins.
- [Atomic] Bin Presentation: Drag Wheelie Bins to curb for collection (Sunday/Monday).

##### [DoD] Waste Management (Weekly)
- **Extraction:** All indoor bins (Bathrooms, Bedrooms, Office, Kitchen) emptied into outdoor Wheelie Bins.
- **Hygiene:** Bin liners replaced if soiled/full.
- **Completion:** Outdoor bins presented for collection on Sunday evening.

---

### 8. Definition of Done (DoD)—Bessie's Study Workspace

The Study Sprint may begin only when every line below is true. All items are binary.

- Workspace: Free of non-study visual clutter.
- Technology: Only authorised school apps/sites are open on her laptop. Phone is placed in the "Kitchen drawer proxy" to bypass distraction.
- Materials: Work has been translated onto preferred blue paper; target task is broken down into exactly 3 physical, verb-driven actions.
- Sensory: Low-stimulation headphones are active, and work is paired with a high-interest Spotify playlist or podcast under the Interest Pairing rule—this content is only available while actively completing the task.

Reset note: if the sprint stalls, re-run this DoD from the top before restarting. The checklist is the restart mechanism; no discussion required.

---

### 8. Zone: Mobile & Vehicle (Car)

#### [SOP] Mobile Node (Car Interior Valet)
- **Frequency:** Weekly
- **Definition of Done (DoD):** No rubbish in door pockets, mats are grit-free, and windows are smear-free.
- **Steps:**
  1. **De-clutter:** Remove all loose items.
  2. **Gravity Clean:** Brush crumbs to floor; shake mats outside.
  3. **Suction:** Vacuum seats then footwells (use crevice tool).
  4. **Clarity:** Glass cleaner on interior windows (spray cloth, not glass).
  5. **Touch-Points:** Wipe steering wheel/gear stick with anti-bacterial.

---

### 9. Global Systems: Pet Care

_Routines to ensure the health and safety of the family animals._

#### [SOP] Dog Medical Care (Parent-Only)
- **Frequency:** Daily & Monthly
- **Definition of Done (DoD):** Medication administered on schedule, warning symptoms monitored, stress levels minimised.
- **Rules:**
  - **Daily Steroid Tablets:** Give steroid tablets (prednisone/prednisolone) every morning with food to replace cortisol. *Crucial: Missing doses risks a relapse of symptoms.*
  - **Monthly Injection:** Schedule and attend vet-administered Zycortal/fludrocortisone injection.
  - **Stress Management:** Keep routines consistent and handling calm to prevent Addisonian crises. Consult vet about temporary dose increases before stressful events (fireworks, moves, boarding).
  - **Watch-list Symptoms:** Same-day vet contact is mandatory if the dog shows lethargy, vomiting, diarrhoea, loss of appetite, or collapse.
  - **Medication Safety:** NSAIDs (Rimadyl, Metacam, Meloxicam) are unsafe; only give vet-approved pain relief (Tramadol, Gabapentin).
  - **Blood Tests:** Monitor electrolytes (sodium/potassium) every 2-3 months.

#### [SOP] Cat & Snake Care (Shared/Rotating)
- **Frequency:** Daily & Weekly
- **Definition of Done (DoD):** Animals fed, enclosures cleaned, environment verified.
- **Rules:**
  - **Cat Care:** Feed morning and evening, clean litter tray daily, groom/brush regularly.
  - **Snake Care (2 Snakes):**
    - *Daily Check:* Verify temperature gradient and humidity levels in the enclosures.
    - *Feeding:* Feed every 1-2 weeks according to the schedule (check calendar).
    - *Water & Substrate:* Provide fresh water daily; spot-clean substrate as needed.
    - *Shedding:* Monitor for incomplete sheds (especially around eyes/tail).

---

## Related

- [[SoT - Family Household Governance]] — _The home is a Distributed System where maintenance is a shared operational requirement._
- [[Emotional Labor is the Invisible Work of Managing a Household and Family]] — _The mental load required to manage a family and household._
- [[For pet care we have a dog who has addisons diseas]] — _Original pet care research and context._
