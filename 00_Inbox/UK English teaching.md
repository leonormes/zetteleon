---
aliases: []
tags: []
title: UK English teaching
type: ""
status: ""
confidence: ""
epistemic: ""
purpose: ""
modified: 2026-01-05T16:59:10+00:00
last_reviewed: ""
review_interval: ""
see_also: []
source_of_truth: []
created: 2026-01-04T00:12:42+00:00
---

This is a "Master Workflow" designed specifically for UK English teaching (Key Stages 1-4). It moves from **Constraint Definition** to **Asset Production** using Gemini’s different modes.

### **The Logic: The "Architect & Builder" Model**

We will not ask Gemini to "do everything at once." That leads to generic hallucinations. Instead, we use a cascade approach:

1. **Define Constraints** (The Brief)
2. **Draft the Blueprint** (Gemini Chat/Canvas) -> _Output: Lesson Plan_
3. **Build the Visuals** (Gemini in Slides) -> _Output: Slide Deck_
4. **Fabricate Materials** (Gemini Chat/Docs) -> _Output: Worksheets/Printouts_

---

### **Phase 1: The Blueprint (Lesson Plan)**

**Tool:** `gemini.google.com` (Use **Canvas Mode** if available via "Tools" > "Canvas", otherwise standard chat).

Step 1: Define Your Constraints

Copy this block and fill it in before you prompt. This is your "Context Block."

> **Context Block:**
> - **Role:** UK English Teacher
> - **Year Group:** [e.g., Year 8]
> - **Ability Level:** [e.g., Mixed ability, heavy SEND support needed]
> - **Curriculum Focus:** [e.g., Analysis of Macbeth's soliloquy / Creative Writing: Gothic conventions]
> - **Time:** [e.g., 60 mins]
> - **Learning Objective (LO):** [e.g., To analyse how Shakespeare uses imagery to show guilt]
> - **Standard:** UK National Curriculum (focus on AO2 Analysis)

Step 2: The Planning Prompt

Paste the Context Block above, followed by this instruction:

> "Using the context above, act as a Senior Head of English. Create a comprehensive lesson plan.
>
> **Structure required:**
>
> 1. **Starter (5 mins):** A 'Do Now' activity to hook students immediately.
>     
> 2. **Direct Instruction (15 mins):** Key concepts to teach (include 3 specific Higher Order Questions to ask).
>     
> 3. **Guided Practice (15 mins):** A 'We Do' activity where we model the skill together.
>     
> 4. **Independent Task (20 mins):** A 'You Do' writing task. Include a 'Scaffolded' version for lower ability and a 'Challenge' version for high achievers.
>     
> 5. **Plenary (5 mins):** Assessment for learning check.
>     
> 
> **Tone:** Professional, clear, and pedagogically sound for a UK classroom."

---

### **Phase 2: The Visuals (Slide Deck)**

Tool: Google Slides (Gemini Sidebar)

Note: You cannot currently "upload" the text plan to auto-generate a perfect deck. You must build it section-by-section for quality.

**Step 1: Open Google Slides** and click the **Ask Gemini** (star) icon in the top right.

Step 2: Generate Slide-by-Slide

Use your specific sections from Phase 1 to prompt the slide creator.

- **For the Title/Hook:**
    - _Prompt:_ "Create a title slide for a Year 8 English lesson on 'Macbeth's Guilt'. Then create a second slide with a visually engaging 'Do Now' activity asking: 'If you committed a crime, would you feel guilt or fear first?'"
- **For the Content:**
    - _Prompt:_ "Create a slide explaining the definition of 'metaphor' and 'simile' with Shakespearean examples. Keep text minimal and use bullet points."
- **For the Visuals:**
    - _Prompt:_ "Generate an image of a moody, dark Scottish castle in a gothic art style to use as a background."

---

### **Phase 3: The Materials (Printouts & Worksheets)**

**Tool:** `gemini.google.com` (or Google Docs sidebar)

Return to your main Gemini chat (where your lesson plan is) to ensure it remembers the context.

**For Worksheets:**

> "Based on the 'Independent Task' in the lesson plan above, create a student worksheet.
>
> - **Section A:** 3 comprehension questions about the text.
>     
> - **Section B:** The main writing task.
>     
> - **Section C:** A sentence starter bank for students who are stuck.
>     
> - **Format:** Format this so I can copy-paste it directly into a Google Doc."

**For Assessment (Exit Tickets):**

> "Create a printable 'Exit Ticket' slip. It should have 3 quick questions to check if they met the Learning Objective. Put 4 of these on a single page layout so I can print and guillotine them easily."

**For Model Answers (WAGOLL - What A Good One Looks Like):**

> "Write a model paragraph for the independent task. It should be perfect (Grade 9 standard). Then, write a second version that is a 'Grade 5' standard with common errors (comma splicing, weak vocabulary) for us to critique as a class."

---

### **Phase 4: The Final Polish (Differentiation)**

**Tool:** Google Docs / Gemini

If you have a specific text (e.g., a complex article or Shakespeare excerpt), paste it into Gemini.

- **Differentiation Prompt:** "I am pasting the text we are reading today. Please rewrite this text to a reading age of 9 years old so my EAL (English as Additional Language) students can access the narrative. Keep the key quotes original but simplify the surrounding narration."

### **Summary of the Workflow**

1. **Chat:** Define constraints $\rightarrow$ Generate Lesson Plan.
2. **Slides:** Open Sidebar $\rightarrow$ Prompt specific slides based on the plan.
3. **Chat:** Request "Student Worksheet" based on the Independent Task.
4. **Docs:** Paste Worksheet $\rightarrow$ Print.

**Next Step:** Would you like me to generate the **"Context Block"** for your first lesson right now? Just tell me the Year Group and Topic.
