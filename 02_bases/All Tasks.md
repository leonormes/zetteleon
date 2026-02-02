---
created: 2026-02-02T12:56:14+00:00
modified: 2026-02-02T13:57:08+00:00
title: All Tasks
---

```tasks
not done
short mode
group by function task.file.path
```

## Task Management Dashboard

This dashboard centralises all embedded tasks from across your vault using the Tasks plugin. It is designed to prioritise immediate actions and organise work by project context without requiring separate files for each task.

### 1. The Daily Driver

This view shows items that are overdue or due today. It also includes tasks without a due date to ensure they are not forgotten during daily planning.

Code snippet

```tasks
not done
(due on or before today) OR (no due date)
group by due
short mode
```

---

### 2. High Priority Focus

A dedicated list for "Must-Do" items. This ignores due dates to highlight critical work that may require early attention.

Code snippet

```tasks
not done
priority is high
group by filename
```

---

### 3. Project-Based Overview

This view organises tasks by the specific project note they belong to. It is ideal for visualising progress across different workstreams.

> [!TIP]
>
> Ensure your project notes are stored in a folder named `Projects` for this query to function correctly.

Code snippet

```tasks
not done
path includes Projects/
group by filename
sort by due
```

---

### 4. Accomplishment Log

A list of everything completed today. This is useful for tracking productivity and performing end-of-day reviews.

Code snippet

```tasks
done
done date is today
```
