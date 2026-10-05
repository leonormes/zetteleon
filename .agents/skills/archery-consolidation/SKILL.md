---
name: archery-consolidation
description: >-
  Extracts actionable form cues, biomechanics, and coaching details from raw archery notes,
  video summaries, or practice session logs, and consolidates them into the 10-step Archery
  Shot Process notes in the LLMeon vault. Use when the user shares archery notes, YouTube clips,
  or asks to update archery shot mechanics and technique.
---

# Archery Shot Process - Knowledge Consolidation

You are an expert in archery biomechanics, form training, and personal knowledge management. Your task is to take a new raw captured note (containing coach feedback, video summaries, or practice session notes) and consolidate it into the existing 10-Step Archery Shot Process notes within `30_Library/100_zettelkasten/`.

Your goal is to extract every piece of actionable advice, form check, and biomechanical detail, and place it into the correct step note without introducing redundancy or duplication.

---

## Hard Constraints & Guards

- **Own-Words Guard:** Never edit, merge into, rename, move, or delete a protected note, and never set or change `own_words` ([[AGENTS]] §6). Protected notes are any note with `own_words: true` and every existing note in `01_journals/` and `20_Thinking/`. Skip them as write targets and report suggestions in chat or in a new `00_Inbox/` note.
- **Shale Evidence:** Call `shale intent "<brief description>"` before editing any files, and `shale done` after completing edits.

---

## Target Notes Taxonomy

All step notes live in `30_Library/100_zettelkasten/`:

1. `[[Archery Shot Process - Stance]]`: Foot positioning, angle, shoulder-width base, weight distribution.
2. `[[Archery Shot Process - Posture]]`: Core engagement, hip/torso positioning, head alignment, baseline trunk stability.
3. `[[Archery Shot Process - Setup]]`: Setting the hook on the string (knuckle placement, tension distribution) and grip on the riser (pressure point in the pit of the hand, relaxed fingers).
4. `[[Archery Shot Process - Raise]]`: Raising the bow straight up, keeping the bow-side shoulder set low, internally rotating the bow arm.
5. `[[Archery Shot Process - Pre-draw]]`: Core rotation check, verifying tall posture and set shoulder before drawing.
6. `[[Archery Shot Process - Loading]]`: Drawing mechanics (leading with the elbow, drawing shoulder as a unit), back tension (scapular retractors, shoulder extensors), keeping head stationary, aiming path from above.
7. `[[Archery Shot Process - Anchor]]`: Jaw reference contact points, aligning the index finger and bow shelf simultaneously.
8. `[[Archery Shot Process - Expansion]]`: Continuing dynamic tension to clicker activation, push-and-pull balance, laser beam aiming.
9. `[[Archery Shot Process - Release]]`: Involuntary response to the clicker, relaxing the fingers naturally.
10. `[[Archery Shot Process - Follow-through]]`: Draw hand flying straight back (neck/ear region), bow hand remaining fully relaxed, bow jumping/falling naturally on the sling.

### Ancillary Targets
- **General Practice & Mental Focus:** `[[Archery Practice Drills]]`
- **Equipment & Tuning:** `[[Archery Safety & Equipment]]` (aliases: `Archery Equipment & Tuning`)

---

## Consolidation Protocol

Follow these steps autonomously:

### 1. Analysis & Mapping
- Read the input note/summary and identify each unique technical instruction, coaching cue, or mental trick.
- Map each instruction to one (or more) of the 10 step notes, or to an ancillary target.

### 2. Current State Audit
- Read the current contents of the target step notes before making edits.
- Compare incoming cues against existing content to prevent duplication.

### 3. Redundancy & Conflict Check
- **Redundant:** If the information is already fully covered, discard it.
- **New detail:** If it provides a fresh angle, cue, or biomechanical clarification, integrate it.
- **Contradiction:** If there is a disagreement across coaching systems (e.g. KSL vs. standard recurve), do not delete the existing instruction. Document it under an `### Alternative Views / Corrections` subheading in the target note.

### 4. File Update Execution
- Call `shale intent "<brief description>"` before editing files.
- Use file editing tools (`replace_file_content`) or Obsidian 1MCP tools to apply targeted edits.
- Preserve existing YAML frontmatter, updating `modified` to the current ISO timestamp (`YYYY-MM-DDTHH:MM:SS+01:00`).
- Integrate new details cleanly under `The Steps`, `Why It Works`, or `Faults & Diagnostics` using bolded terms for readability.
- If citations or video links are provided, append them under `### References`.
- Call `shale done` once edits are complete.

---

## Output Format

Do not output raw file dumps or large markdown diffs. Keep responses concise using this structure:

### 1. Extraction & Mapping Summary
List each extracted cue and where it was mapped (e.g., New detail merged, or Redundant/skipped).

### 2. Updates Applied
List the updated files and a one-line summary of what was added.
