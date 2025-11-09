---
aliases: []
confidence: 
created: 2025-10-30T15:56:41Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:13Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: highly-connected-notes
type: 
uid: 
updated: 
---

## Highly Connected Notes

Notes with more than 5 links to or from them.

### Notes with 5+ Outgoing Links

```dataview
TABLE length(file.outlinks) as "Outgoing Links"
FROM "100_zettelkasten"
WHERE length(file.outlinks) > 5 AND type != "map"
SORT length(file.outlinks) DESC
```

### Notes with 5+ Incoming Links

```dataview
TABLE length(file.inlinks) as "Incoming Links"
FROM "100_zettelkasten"
WHERE length(file.inlinks) > 5 AND type != "map"
SORT length(file.inlinks) DESC
```

### Notes with 5+ Total Links (Combined)

```dataview
TABLE 
  length(file.outlinks) as "Out",
  length(file.inlinks) as "In",
  (length(file.outlinks) + length(file.inlinks)) as "Total"
FROM "100_zettelkasten"
WHERE (length(file.outlinks) + length(file.inlinks)) > 5 AND type != "map"
SORT (length(file.outlinks) + length(file.inlinks)) DESC
```
