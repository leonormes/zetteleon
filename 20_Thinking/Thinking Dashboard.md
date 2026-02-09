---
created: 2026-02-06T09:45:00+00:00
modified: 2026-02-08T21:01:19+00:00
tags: [automated, dashboard, question, thinking]
title: Thinking Dashboard
---

## Thinking Dashboard

> [!INFO]
> This dashboard replicates the views from `Thinking.base` using Dataview.
> Invariant Filters: `type = "head"` AND `path!= "10_System"`

### All Open

_Active thoughts that are not filed away or deferred._

```dataview
TABLE WITHOUT ID file.link AS "Note", status, file.tags AS "Tags", file.size AS "Size"
FROM ""
WHERE type = "head"
  AND !startswith(file.path, "10_System")
  AND status != "someday"
  AND status != "archived"
SORT status ASC, file.ctime ASC
```

### Active Work HEADs

_Work-focused items currently in flight._

```dataview
TABLE WITHOUT ID file.link AS "Note", status, type, AoL
FROM ""
WHERE type = "head"
  AND !startswith(file.path, "10_System")
  AND AoL = "Work"
  AND (status = "active" OR status = "processing")
SORT file.ctime DESC
```

### Active Personal HEADs

_Personal items currently in flight._

```dataview
TABLE WITHOUT ID file.link AS "Note", status, type, AoL
FROM ""
WHERE type = "head"
  AND !startswith(file.path, "10_System")
  AND AoL = "Personal"
  AND (status = "active" OR status = "processing")
SORT file.ctime DESC
```

### Someday

_Deferred items._

```dataview
TABLE WITHOUT ID file.link AS "Note", status, AoL
FROM ""
WHERE type = "head"
  AND !startswith(file.path, "10_System")
  AND status = "someday"
SORT file.ctime DESC
```

### Questions

_Open questions (tagged with question or type=question)._

```dataview
TABLE WITHOUT ID file.link AS "Note", status
FROM ""
WHERE type = "question"
SORT file.ctime DESC
```
