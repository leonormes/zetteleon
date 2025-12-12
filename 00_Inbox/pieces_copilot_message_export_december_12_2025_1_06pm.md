*Shared from Pieces (https://pieces.app) by Leon Ormes (leonormes@gmail.com) on Friday Dec 12, 2025 - 1:06 PM*
---
Here’s a cleaned‑up structure and a proposal you can more or less paste to your manager.

---

## 1. Refine the “routine work” list

Framing principle:  
- Low stress, low context switching  
- Mostly read‑only or scripted changes  
- Helpful for SRE hygiene but non‑blocking if it slips a few days  

### A. Observability & Logs

- **Log watching / observability checks**
  - Scan key dashboards (e.g. Grafana, Loki) once or twice a day.
  - Note recurring warnings / noisy alerts that could be tuned away.
  - Capture “interesting patterns” or possible bugs as Jira tickets.
  - Verify that log pipelines are still working (no obvious gaps).

- **Alert review & light adaptation**
  - Review alerts that fire frequently but rarely need action.
  - Propose threshold tweaks or label changes (someone else can approve/apply).
  - Update alert descriptions so they link to the right runbook or dashboard.

Why low stress: mostly read-only, pattern spotting and note‑taking; changes can be gated behind review.

---

### B. Deployment & Terraform Hygiene

- **Run Terraform via existing workflows**
  - Execute documented `terraform plan/apply` steps in non‑prod or via TFC runs that are already queued.
  - Follow a checklist rather than designing changes (e.g. “run apply for X workspace after code is merged, paste logs into ticket”).

- **Organise deployment code**
  - Standardise README files in deployment repos (what environment, how to run Terraform, known caveats).
  - Tag or group Terraform workspaces/projects correctly in TFC.
  - Help keep module usage up to date in a simple spreadsheet or registry view (which module versions in which envs).

Why low stress: work is constrained by existing docs and scripts; changes can be reviewed before merge; failure modes are low if restricted to non‑prod or supervised.

---

### C. Documentation & Knowledge Capture

- **Write up bugs**
  - Take rough Slack conversations / error messages and turn them into clear Jira bugs:
    - “Steps to reproduce”, “Expected vs actual behaviour”, screenshots/log links.
  - Close the loop by linking tickets to relevant dashboards, runbooks, or repos.

- **Write up features / system behaviour**
  - Turn informal features or behaviours into short docs:
    - “How the backup job works”, “What the new central services module does”, etc.
  - Keep Confluence / internal docs in sync with what we’re actually running where.

- **Test the system (scripted checks)**
  - Run documented smoke tests or checklists (e.g. “can we log into app X”, “backups succeeded last night”, “alerts routed correctly”).
  - Record results in a simple template (pass/fail, notes).

Why low stress: no design decisions; mostly turning reality into clear text, following recipes.

---

### D. Jira & Reporting

- **Manage Jira reports / hygiene**
  - Keep SRE / infra boards tidy:
    - Ensure tickets have the right labels, components, and assignees.
    - Move tickets to the correct status based on comments / GitLab activity.
  - Prepare simple weekly snapshots:
    - “New bugs opened vs closed”
    - “Top recurring alert-related issues”
  - Make sure links exist:
    - Issues ↔ PRs ↔ runbooks ↔ dashboards.

Why low stress: administrative and organisational; high value to the team; can be done at Yasir’s pace.

---

## 2. Draft proposal to your manager

You can adapt this to email or Confluence.

---

Subject: Proposal to adjust Yasir’s workload to low‑stress SRE support tasks

Hi [Manager],

Given that Yasir is currently unwell and operating at reduced capacity, I’d like to suggest a temporary adjustment to his workload so he can still contribute meaningfully without being on the critical path for delivery or on‑call incidents.

**Goals**

- Keep Yasir involved in day‑to‑day SRE work in a low‑stress way.  
- Reduce pressure on the rest of the team by offloading routine but valuable tasks.  
- Avoid putting him in situations where delays or sick days would block deployments or incident response.

**Principles**

- Focus on routine, well‑scoped work with clear checklists.
- Prefer read‑only or low‑risk changes, always behind review.
- Nothing time‑critical; it’s OK if tasks roll over a day or two.

**Proposed areas of work**

1. **Observability & Logs**
   - Regular log and dashboard review for obvious issues or noisy alerts.
   - Raise Jira tickets for recurring errors or suspicious patterns.
   - Suggest (but not directly implement) alert threshold/label changes.

2. **Deployment & Terraform Hygiene**
   - Run scripted Terraform plans/applies in non‑prod or via existing TFC workflows, using our standard checklists.
   - Help organise deployment code and workspaces:
     - Update READMEs for deployment repos.
     - Ensure Terraform workspaces are correctly tagged and described.

3. **Documentation & Knowledge Capture**
   - Turn Slack threads and raw errors into well‑structured Jira bug reports.
   - Write or update concise docs for existing features and infra components.
   - Run simple scripted/system smoke tests and record the results.

4. **Jira & Reporting**
   - Keep our SRE / infra boards clean:
     - Ensure tickets have the right component/labels/status.
   - Prepare simple weekly summaries (e.g. recurring alerts, top infra bugs).
   - Make sure tickets are linked to relevant PRs, dashboards, and runbooks.

**Boundaries / Safeguards**

- No primary on‑call or P1/P2 incident ownership.  
- No unsupervised production changes; anything risky remains with the core SREs.  
- Work items will be small, with clear definitions of done, and can be paused if his health worsens.

If you’re comfortable with this approach, I’m happy to:
- Draft a small backlog of specific tasks in Jira for Yasir under these categories, and  
- Pair with him initially to make sure the scope feels manageable.

Best,  
[Your name]

---

If you’d like, I can turn this into a very short Confluence page or a Jira ticket template so you can spin up individual tasks for him quickly.