---
type: dashboard
---
# Projects Dashboard

Here is an overview of all projects categorised by status and type using Dataview.

## 🟢 Active Projects
```dataview
TABLE project_category AS "Category", project_name AS "Project Name", file.mtime AS "Last Modified"
FROM "30_Library/200_Projects"
WHERE type = "project" AND project_status = "active"
SORT project_category ASC
```

## 🏗️ Infrastructure Projects
```dataview
TABLE project_status AS "Status", project_name AS "Project Name", file.mtime AS "Last Modified"
FROM "30_Library/200_Projects"
WHERE type = "project" AND project_category = "infrastructure"
SORT file.mtime DESC
```

## 💻 Development Projects
```dataview
TABLE project_status AS "Status", project_name AS "Project Name", file.mtime AS "Last Modified"
FROM "30_Library/200_Projects"
WHERE type = "project" AND project_category = "development"
SORT file.mtime DESC
```

## 👤 Personal Projects
```dataview
TABLE project_status AS "Status", project_name AS "Project Name", file.mtime AS "Last Modified"
FROM "30_Library/200_Projects"
WHERE type = "project" AND project_category = "personal"
SORT file.mtime DESC
```

## 🧠 ProdOS Core
```dataview
TABLE project_status AS "Status", file.mtime AS "Last Modified"
FROM "30_Library/200_Projects"
WHERE type = "project" AND project_category = "prodos"
SORT file.mtime DESC
```

## 📦 Archived / Other Projects
```dataview
TABLE project_category AS "Category", file.mtime AS "Last Modified"
FROM "30_Library/200_Projects"
WHERE type = "project" AND project_status = "archived"
SORT file.mtime DESC
```
