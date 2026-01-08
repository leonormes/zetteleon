---
aliases: []
alias: []
confidence:
created: 2025-10-18T13:25:33Z
energy: 5
epistemic:
focus: 5
habit_meds: false
habit_water: 0
horse_stance_target: 300
last_reviewed:
migraine: false
migraine_notes: ""
migraine_severity: 0
modified: 2026-01-08T08:10:22+00:00
mood: 5
purpose:
review_interval:
see_also: []
source_of_truth: []
status:
tags: [daily]
title: daily
type: daily
uid:
updated:
---

```journal-nav

```

## Habits

- [ ] Meds
- [ ] Water (goal: 8)
- [ ] Exercise
- [ ] Reading
- [ ] Journaling

### Physical Ledger

- **Horse Stance Total**: `$= dv.current().file.lists.where(l => l.text.includes("stance::")).array().reduce((acc, l) => acc + (Number((l.text.match(/stance::\s*(\d+)/) || [])[1]) || 0), 0)` seconds

---

<%*

const birthDate = new Date("1973-11-03");

const today = new Date(tp.date.now("YYYY-MM-DD"));

// Days

const lifeDay = Math.floor((today - birthDate) / (1000 * 60 * 60 * 24));

// Weeks

const lifeWeek = Math.floor(lifeDay / 7);

const lifeWeekPct = ((lifeWeek / 4000) * 100).toFixed(1); // 1 decimal place

// Months

let lifeMonth = (today.getFullYear() - birthDate.getFullYear()) * 12 + (today.getMonth() - birthDate.getMonth());

// Years

let lifeYear = today.getFullYear() - birthDate.getFullYear();

if (today.getMonth() < birthDate.getMonth() || (today.getMonth() === birthDate.getMonth() && today.getDate() < birthDate.getDate())) {

  lifeYear--;

}

tR += `**Life Day:** ${lifeDay}\n**Life Week:** ${lifeWeek} (${lifeWeekPct}%)\n**Life Month:** ${lifeMonth}\n**Life Year:** ${lifeYear}`;

%>

---
