---
aliases: []
confidence: 
created: 2025-10-28T10:01:08Z
epistemic: 
last_reviewed: 
modified: 2025-10-31T09:09:17Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [topic/pkm]
title: Quick add macro
type:
uid: 
updated: 
version:
---

**Planning QuickAdd macro**I'm designing a QuickAdd macro for users to automatically create atomic notes with different types and specific YAML schemas. The macro will use Templater and minimize prompts to streamline note creation.
Awesome—let’s give you a **single QuickAdd macro** that quickly creates any **atomic** note (concept, strategy, definition, instructional, question, quote, person), enforces your YAML, and drops in a minimal, context‑free body.

You’ll get:

- ✅ One command: **“➕ New Atomic Note”**  
- ✅ Branching by type with the right fields per your schema  
- ✅ ISO timestamps for `created` / `updated`  
- ✅ Guardrails for `epistemic`, `purpose`, `status`, and type‑specific fields  
- ✅ Automatic foldering (e.g., `Atomic/Concepts`, `Atomic/Quotes`, …)

---

## 1) Setup (2 minutes)

1. **Install QuickAdd** (Community Plugins → *QuickAdd*).
2. Create a scripts folder (if not present):

```sh
.obsidian/plugins/quickadd/scripts/
```

3. **Create a new file** here named `atomic.js` and paste the script below.
4. In **QuickAdd → Macros**:
   - Click **“+ Add Macro”** → name it `➕ New Atomic Note`.
   - **Add a Step → User Script** → select `atomic.js`.
5. (Optional) Add a hotkey via **Settings → Hotkeys** for `QuickAdd: ➕ New Atomic Note`.

---

## 2) The QuickAdd User Script

> This is a self-contained script (no Templater needed). It generates YAML and a minimal body appropriate for each atomic type and creates the note in a sensible folder.

```js
// File: .obsidian/plugins/quickadd/scripts/atomic.js
// Macro: "➕ New Atomic Note"
// Creates context-free atomic notes with strict YAML per type.

module.exports = async (params) => {
  const { app, quickAddApi: qa } = params;

  // ====== CONFIG (edit to taste) ======
  const FOLDERS = {
    concept: "Atomic/Concepts",
    strategy: "Atomic/Strategies",
    definition: "Atomic/Definitions",
    instructional: "Atomic/Instructionals",
    question: "Atomic/Questions",
    quote: "Atomic/Quotes",
    person: "Atomic/People"
  };

  const DEFAULTS = {
    statusAtomic: "seedling",
    statusQuote: "evergreen",
    statusPerson: "evergreen",
    confidence: 0.6,
    reviewInterval: 90,        // days
    instructionalReview: 180   // days
  };

  const EPISTEMIC = ["fact","axiom","principle","opinion","hypothesis","NA"];
  // sensible defaults per type
  const TYPE_DEFAULT_EPISTEMIC = {
    concept: "principle",
    strategy: "principle",
    definition: "fact",
    instructional: "NA",
    question: "NA",
    quote: "fact",
    person: "fact"
  };

  // ====== HELPERS ======
  const nowIso = () => new Date().toISOString().replace(/\.\d{3}Z$/, "Z");
  const today = () => new Date().toISOString().slice(0,10); // YYYY-MM-DD
  const sanitize = (s) => (s ?? "").trim();
  const quoteYaml = (s) => `"${String(s).replace(/"/g, '\\"')}"`;
  const toArrayYaml = (arr) => (arr && arr.length ? `[${arr.map(quoteYaml).join(", ")}]` : "[]");

  async function ensureFolder(path) {
    const parts = path.split("/");
    let curr = "";
    for (const p of parts) {
      curr = curr ? `${curr}/${p}` : p;
      const af = app.vault.getAbstractFileByPath(curr);
      if (!af) {
        try { await app.vault.createFolder(curr); } catch (_) {}
      }
    }
  }

  async function uniqueFilePath(folder, title) {
    let base = `${folder}/${title}.md`;
    if (!app.vault.getAbstractFileByPath(base)) return base;
    // Try with " (n)" suffix
    let i = 2;
    while (app.vault.getAbstractFileByPath(`${folder}/${title} (${i}).md`)) i++;
    return `${folder}/${title} (${i}).md`;
  }

  async function promptType() {
    const types = ["concept","strategy","definition","instructional","question","quote","person"];
    const choice = await qa.suggester(types.map(t => `${t}`), types);
    if (!choice) throw new Error("Cancelled");
    return choice;
  }

  // ====== FLOW ======
  const type = await promptType();
  const title = sanitize(await qa.inputPrompt(`Title for new ${type}:`));
  if (!title) throw new Error("Title required");

  const created = nowIso();
  const updated = created;

  // Common fields
  let status = DEFAULTS.statusAtomic;
  let epistemic = TYPE_DEFAULT_EPISTEMIC[type] || "NA";
  let purpose = "NA";
  let confidence = DEFAULTS.confidence;
  let last_reviewed = today();
  let review_interval = DEFAULTS.reviewInterval;
  let aliases = [];
  let tags = [];
  let see_also = [];

  // Type-specific prompts
  if (["concept","strategy","definition"].includes(type)) {
    epistemic = await qa.suggester(EPISTEMIC, EPISTEMIC) ?? TYPE_DEFAULT_EPISTEMIC[type];
    purpose = sanitize(await qa.inputPrompt("One-line purpose (or leave blank for NA):")) || "NA";
    status = await qa.suggester(["seedling","growing","evergreen"], ["seedling","growing","evergreen"]) ?? DEFAULTS.statusAtomic;

    const confStr = sanitize(await qa.inputPrompt("Confidence 0–1 (default 0.6):")) || `${DEFAULTS.confidence}`;
    const conf = Number(confStr);
    if (!Number.isNaN(conf) && conf >= 0 && conf <= 1) confidence = conf;

    const riStr = sanitize(await qa.inputPrompt("Review interval days (default 90):")) || `${DEFAULTS.reviewInterval}`;
    const ri = parseInt(riStr, 10);
    if (!Number.isNaN(ri) && ri > 0) review_interval = ri;

  } else if (type === "instructional") {
    purpose = sanitize(await qa.inputPrompt("What is this checklist for?")) || "Checklist";
    review_interval = DEFAULTS.instructionalReview;
    status = DEFAULTS.statusAtomic;
    epistemic = "NA";

  } else if (type === "question") {
    status = DEFAULTS.statusAtomic;
    epistemic = "NA";

  } else if (type === "quote") {
    status = DEFAULTS.statusQuote;
    epistemic = "fact";

  } else if (type === "person") {
    status = DEFAULTS.statusPerson;
    epistemic = "fact";
  }

  // Optional aliases/tags input (lightweight)
  const addAliases = await qa.yesNoPrompt("Add aliases?");
  if (addAliases) {
    const al = sanitize(await qa.inputPrompt("Aliases (comma-separated):"));
    if (al) aliases = al.split(",").map(s => s.trim()).filter(Boolean);
  }
  const addTags = await qa.yesNoPrompt("Add tags?");
  if (addTags) {
    const tg = sanitize(await qa.inputPrompt("Tags without #: comma-separated"));
    if (tg) tags = tg.split(",").map(s => s.trim()).filter(Boolean);
  }

  // Build frontmatter by type
  let frontmatter = [
    "---",
    `created: ${created}`,
    `updated: ${updated}`,
    `type: ${type}`,
    `status: ${status}`,
    `epistemic: ${epistemic}`,
    `purpose: ${quoteYaml(purpose)}`,
    `confidence: ${confidence}`,
    `last_reviewed: ${last_reviewed}`,
    `review_interval: ${review_interval}`,
    `see_also: ${toArrayYaml(see_also)}`,
    `aliases: ${toArrayYaml(aliases)}`,
    `tags: ${toArrayYaml(tags)}`,
  ];

  // Per-type extra fields & body
  let body = `# ${title}\n\n`;
  switch (type) {
    case "concept":
      body += [
        "**Summary:** One-sentence, context-free definition.",
        "",
        "**Details:** 2–4 sentences max. No application stories.",
      ].join("\n");
      break;

    case "strategy":
      body += [
        "**What:** One-line tactic.",
        "**How:**",
        "- Step 1",
        "- Step 2",
        "- Step 3",
        "",
        "**Failure modes:**",
        "- …",
        "",
        "**Example (1 max):**",
        "- …"
      ].join("\n");
      break;

    case "definition":
      body += [
        "**Definition:** Clear, short, reusable.",
        "",
        "**Notes:** Keep context minimal; link only to atomic notes in `see_also`."
      ].join("\n");
      break;

    case "instructional":
      frontmatter = frontmatter.map(l => l); // same keys; epistemic already NA
      body += [
        "**Checklist:**",
        "- [ ] Step 1",
        "- [ ] Step 2",
        "- [ ] Step 3",
        "",
        "**Verification:**",
        "- [ ] Result meets acceptance criteria"
      ].join("\n");
      break;

    case "question":
      body += [
        "**Context (optional):**",
        "- …",
        "",
        "**Lines of inquiry:**",
        "- …",
        "",
        "**Next step:**",
        "- …"
      ].join("\n");
      break;

    case "quote": {
      // Add source + loc to frontmatter
      const source = sanitize(await qa.inputPrompt("Source (e.g., [[Book Title]] or URL):")) || "";
      const loc = sanitize(await qa.inputPrompt("Location (page/timestamp):")) || "";
      frontmatter.push(`source: ${quoteYaml(source)}`);
      frontmatter.push(`loc: ${quoteYaml(loc)}`);

      body += [
        "> Paste the quote here.",
        "",
        "**Context (optional):**",
        "- …"
      ].join("\n");
      break;
    }

    case "person": {
      const affiliation = sanitize(await qa.inputPrompt("Affiliation (optional):")) || "";
      const role = sanitize(await qa.inputPrompt("Role (optional):")) || "";
      frontmatter.push(`affiliation: ${quoteYaml(affiliation)}`);
      frontmatter.push(`role: ${quoteYaml(role)}`);
      frontmatter.push(`links: []`);

      body += [
        "**Bio (factual, brief):**",
        "- …",
        "",
        "**Topics associated (atomic only):**",
        "- [[…]]"
      ].join("\n");
      break;
    }
  }

  // Finalize frontmatter
  frontmatter.push("---");
  const content = `${frontmatter.join("\n")}\n\n${body}\n`;

  // Create file
  const folder = FOLDERS[type] || "Atomic";
  await ensureFolder(folder);
  const filePath = await uniqueFilePath(folder, title);
  await app.vault.create(filePath, content);

  return filePath;
};
```

---

## 3) What it Enforces (in line with Your system)

- **Binary invariant:** Only atomic types are available in this macro.
- **Epistemic + Purpose:** Prompted for relevant types; `purpose: "NA"` for those that don’t need it.
- **Status gates (lightweight):** Defaults (`seedling`, `evergreen` for quotes/person).
- **Review cadence:** Adds `last_reviewed` + `review_interval` (defaults adjustable at top).
- **No structural creep:** Body templates are minimal and context-free; any contextual narrative should live in **structural** notes.

---

## 4) Optional: Templater Variants (if You Prefer templates)

If you’d rather keep the body in Templater templates and let QuickAdd just supply variables, I can generate **seven `.md` templates** and a **QuickAdd Choice** for each atomic type that fills variables like `{{TITLE}}`, `{{EPISTEMIC}}`, `{{PURPOSE}}`, etc. Just say the word and I’ll drop them in.

---

## 5) Want Folder Names or Defaults Tweaked

I set:

- `Atomic/Concepts`, `Atomic/Strategies`, `Atomic/Definitions`, `Atomic/Instructionals`, `Atomic/Questions`, `Atomic/Quotes`, `Atomic/People`.
- Defaults: `confidence=0.6`, `review_interval=90d` (instructionals: 180d).

If you’d like different folders, default `epistemic` per type, or to add/remove fields (e.g., `uid`), tell me your preferences and I’ll adjust the script in seconds.
