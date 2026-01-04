---
aliases: []
tags: []
title: "Wiki: Presentation Architecture with Gemini"
type: ""
status: ""
confidence: ""
epistemic: ""
purpose: ""
modified: 2026-01-03T23:58:38+00:00
last_reviewed: ""
review_interval: ""
see_also: []
source_of_truth: []
created: 2026-01-03T23:58:28+00:00
---

Here is a synthesised wiki note on the architecture and operational workflows for creating presentations with Gemini, consolidated from the provided video analyses.

---

# Wiki: Presentation Architecture with Gemini

## **1. Conceptual Framework**

The Gemini presentation ecosystem operates on a **bimodal architecture**, splitting the workload between "Macro-Creation" (Drafting) and "Micro-Refinement" (Editing).

- **The Drafting Engine (Gemini Canvas):** Functions as a "Text-to-Structure" generator. It assumes the role of a Junior Architect, creating the comprehensive skeleton, narrative arc, and visual layout of a deck from raw inputs. It produces an 80% complete draft, shifting the user's role to high-level strategy and polish.
- **The Refinement Engine (Gemini in Slides):** Functions as an embedded toolset within the Google Slides interface. It handles asset generation, summarisation, and specific content injection without altering the document's core structure.

---

## **2. Primary Workflows (Macro-Creation)**

These workflows utilise **Gemini Canvas** (`gemini.google.com` $\rightarrow$ Tools $\rightarrow$ Canvas) to generate full decks.

### **Vector A: Ex Nihilo (Zero-to-One)**

- **Use Case:** Brainstorming, rapid prototyping, or ideation without existing data.
- **Logic:** The system hallucinates structure, brand concepts, and copy based on a high-level intent.
- **Process:**
    
    1. Activate **Canvas** mode.
    2. Prompt: _"Create a pitch deck for [Concept]"_.
    3. System generates a 10+ slide narrative with placeholder imagery.

### **Vector B: Synthesis (Data-to-Deck)**

- **Use Case:** Transforming proprietary IP (reports, transcripts, code) into a presentation.
- **Logic:** An **ETL (Extract, Transform, Load)** operation. The system extracts unstructured data from uploaded files, transforms it into a pedagogical sequence, and loads it into a slide schema.
- **Process:**
    
    1. Click **Add File (+)** and upload source documents (PDFs, Drive files).
    2. Prompt: _"Turn these notes into a strategic review presentation"_.
    3. System maps specific data points (dates, quotes) to slides, minimising hallucination.

### **Vector C: Design Refactoring (Draft-to-Polish)**

- **Use Case:** Upgrading existing, low-fidelity slide decks (e.g., text-heavy drafts).
- **Logic:** Asset-to-Asset transformation. The system applies a "Presentation Layer" over existing content, re-architecting the visual hierarchy while preserving the core message.
- **Process:**
    
    1. Upload the rough Google Slide file via **Add from Drive**.
    2. Prompt: _"Transform this into a professional presentation with a [Blue/White] colour scheme"_.
    3. System generates a new, visually refined file (preserving the original).

### **Vector D: The Hybrid Research Pipeline (NotebookLM Bridge)**

- **Use Case:** High-stakes presentations requiring rigorous citation and factual density.
- **Logic:** Decouples logic from design. **NotebookLM** acts as the _Logic Engine_ (sourcing, citing, structuring), while **Gemini Canvas** acts as the _Design Engine_.
- **Process:**
    
    1. **NotebookLM:** Aggregate sources $\rightarrow$ Generate a text-based, cited slide outline.
    2. **Transfer:** Copy the text outline.
    3. **Gemini Canvas:** Paste outline $\rightarrow$ Prompt _"Convert this grounded outline into slides"_ $\rightarrow$ Export.

---

## **3. Operational Procedures**

### **The "Export Bridge"**

The critical interoperability step for all Canvas workflows is the **Export to Slides** function.

- Gemini generates a proprietary draft format.
- Clicking **Export** converts this object into a standard **Google Slides (.pptx compatible)** file, stored in Google Drive.
- Once exported, the file is fully editable and decoupled from the AI model.

### **Embedded Micro-Tools (Inside Google Slides)**

For granular editing within an open presentation:

- **Visual Generation:** _Insert $\rightarrow$ Image $\rightarrow$ Help me create an image_. (Generates assets like "Photorealistic running shoe").
- **Slide Generation:** _Ask Gemini Sidebar_ $\rightarrow$ _"Create a slide about [Topic]"_.
- **Data Grounding:** Use the **`@`** symbol in the sidebar to reference specific Drive files (Docs/Sheets) to generate a single slide based on that data.
- **Rewriting:** Select a text box $\rightarrow$ Prompt _"Rewrite to be concise"_.

---

## **4. System Constraints & Optimisation**

- **Template Repetition:** The generation engine relies on a finite library of layout patterns; frequent use may result in structural homogeneity across different decks.
- **Speed vs. Aesthetics:** Optimised for _structural efficiency_ within Workspace. For bespoke, high-art visuals, external design tools may still be superior.
- **Ephemeral Memory:** In the embedded workspace (Slides sidebar), chat history is session-based. Closing the tab erases the prompt history; only inserted content is saved.
- **Mode Discipline:** Always ensure **"Thinking Mode"** is active in Canvas for complex logical structuring, or the output may lack narrative coherence.
