---
created: 2026-02-06T09:32:06+00:00
modified: 2026-02-06T21:35:58+00:00
---
```dataview
TABLE file.mtime AS "Last Modified", status AS "Status"
FROM "20_Thinking" OR "HEAD"
WHERE file.name != this.file.name
SORT file.mtime DESC
LIMIT 10

```

```dataview
TABLE rows.file.link AS "Modules", rows.last_reviewed AS "Last Reviewed"
FROM #prodos
WHERE type = "project" OR type = "learning"
GROUP BY status
SORT status ASC

```


```dataview
TABLE last_reviewed AS "Last Reviewed", date(today) - last_reviewed AS "Days Dormant"
FROM "SoT" OR #prodos
WHERE last_reviewed != null AND (date(today) - last_reviewed) > dur(90 days)
SORT last_reviewed ASC

```

```dataview
LIST
FROM #prodos
WHERE contains(file.name, "MOC") OR contains(file.name, "SoT")
SORT file.name ASC

```

