---
title: pieces_copilot_message_export_august_5_2026_9_34am
type: note
permalink: llmeon/00-inbox/pieces-copilot-message-export-august-5-2026-9-34am
created: 2026-08-05T08:34:32+00:00
modified: 2026-08-05T08:41:18+00:00
---

## Database report: `ff-demo-mysql.mysql.database.azure.com` → `diabetes` schema

**Generated:** Wed Aug 5 2026 09:32 AM (+01:00) — from your live `mysqlsh`/CLI session against `ff-demo-mysql.mysql.database.azure.com:3306`.

**Server context** (from prior tool results this session): Azure Database for MySQL Flexible Server, Burstable B1s tier, 20 GiB storage, created `2023-05-31`, tagged `Owner: JonBradshaw`, `review: true`.

### Databases on the server

```sql
SHOW DATABASES;
```

| Database | Notes |
|---|---|
| `information_schema` | MySQL system schema |
| `diabetes` | Only user database — the focus of this report |
| `mysql` | MySQL system schema |
| `performance_schema` | MySQL system schema |
| `sys` | MySQL system schema |

Only one real application schema exists on this server: **`diabetes`**.

### Tables in `diabetes`

```sql
USE diabetes;
SHOW TABLES;
```

| Table | Row count |
|---|---|
| `diabetes` | 94,041 |
| `diabetes_old` | 94,186 |
| `pet_diabetes` | 90,984 |

Row counts are all in the same ~90-94k range, all populated — none of these are empty/dead tables.

### Structure — `diabetes`

```sql
DESCRIBE diabetes;
```

| Field | Type | Null | Key |
|---|---|---|---|
| `index` | `bigint(20)` | YES | MUL |
| `db-nhsnumber` | `text` | YES | |
| `db-atrialfibrillation` | `bigint(20)` | YES | |
| `db-chronickidneydiseaseindicator` | `bigint(20)` | YES | |
| `db-bloodpressuretreatment` | `bigint(20)` | YES | |
| `db-diabetes` | `text` | YES | |
| `db-type1` | `bigint(20)` | YES | |
| `db-type2` | `bigint(20)` | YES | |
| `db-bmi` | `double` | YES | |
| `db-cholesterolratio` | `double` | YES | |
| `db-systolicbloodpressure` | `double` | YES | |
| `db-smoking` | `text` | YES | |
| `db-familyhistorycoronaryheartdisease` | `bigint(20)` | YES | |
| `db-id` | `bigint(20)` | YES | |
| `db-patientid` | `bigint(20)` | YES | |

`SHOW CREATE TABLE diabetes` confirms:
```sql
CREATE TABLE `diabetes` (
  `index` bigint(20) DEFAULT NULL,
  `db-nhsnumber` text,
  `db-atrialfibrillation` bigint(20) DEFAULT NULL,
  `db-chronickidneydiseaseindicator` bigint(20) DEFAULT NULL,
  `db-bloodpressuretreatment` bigint(20) DEFAULT NULL,
  `db-diabetes` text,
  `db-type1` bigint(20) DEFAULT NULL,
  `db-type2` bigint(20) DEFAULT NULL,
  `db-bmi` double DEFAULT NULL,
  `db-cholesterolratio` double DEFAULT NULL,
  `db-systolicbloodpressure` double DEFAULT NULL,
  `db-smoking` text,
  `db-familyhistorycoronaryheartdisease` bigint(20) DEFAULT NULL,
  `db-id` bigint(20) DEFAULT NULL,
  `db-patientid` bigint(20) DEFAULT NULL,
  KEY `ix_diabetes_index` (`index`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=latin1
```
No primary key — only a non-unique `BTREE` index on `index`. `ENGINE=InnoDB`, `CHARSET=latin1`.

### Structure — `diabetes_old`

```sql
DESCRIBE diabetes_old;
```

Identical column set and order to `diabetes`, with **one difference**: `db-nhsnumber` is `bigint(20)` here instead of `text`.

| Field | Type | Null | Key |
|---|---|---|---|
| `index` | `bigint(20)` | YES | MUL |
| `db-nhsnumber` | `bigint(20)` | YES | |
| `db-atrialfibrillation` | `bigint(20)` | YES | |
| `db-chronickidneydiseaseindicator` | `bigint(20)` | YES | |
| `db-bloodpressuretreatment` | `bigint(20)` | YES | |
| `db-diabetes` | `text` | YES | |
| `db-type1` | `bigint(20)` | YES | |
| `db-type2` | `bigint(20)` | YES | |
| `db-bmi` | `double` | YES | |
| `db-cholesterolratio` | `double` | YES | |
| `db-systolicbloodpressure` | `double` | YES | |
| `db-smoking` | `text` | YES | |
| `db-familyhistorycoronaryheartdisease` | `bigint(20)` | YES | |
| `db-id` | `bigint(20)` | YES | |
| `db-patientid` | `bigint(20)` | YES | |

### Structure — `pet_diabetes`

Not yet run — your query output doesn't include `DESCRIBE pet_diabetes;`. Given the row count (90,984) is close to the other two, it's worth checking whether it shares the same schema or is genuinely unrelated (the name suggests veterinary/pet data rather than the NHS human clinical data in the other two tables).

### Column inventory (information_schema query)

You ran:
```sql
SELECT table_name, column_name, data_type, is_nullable, column_key
FROM information_schema.columns
WHERE table_schema = 'diabetes'
ORDER BY table_name, ordinal_position;
```
The output for this specific query wasn't captured in what you pasted — only `diabetes` and `diabetes_old` structures came through via `DESCRIBE`. Re-run and paste the result if you want `pet_diabetes` folded into this table.

---

## Working conclusions

- **Purpose:** the `diabetes` database holds an NHS-style clinical dataset — NHS number, diabetes type 1/2 flags, cardiovascular risk factors (atrial fibrillation, CKD, BP treatment, BMI, cholesterol ratio, systolic BP, smoking, family history of coronary heart disease), keyed loosely by `db-id` / `db-patientid`. This lines up with the diabetes dataset referenced in your `FTFL-687` Claude session yesterday (*"verify the diabetes database and connections work"*).
- **`diabetes_old`** is almost certainly a prior/backup version of the same table — same schema bar the `db-nhsnumber` type change (`text` → `bigint`), same row-count ballpark (94,186 vs 94,041).
- **`pet_diabetes`** is the outlier — name and possibly schema diverge from the other two; confirm with `DESCRIBE pet_diabetes;` before assuming it's part of the same use case (it may be an unrelated demo/test table, or a genuinely different veterinary dataset that happens to share the server).
- **No table has a primary key** — data integrity/dedup checks will need to rely on `db-id` / `db-patientid` rather than schema constraints.
- **Sensitive data flag:** `db-nhsnumber` is present in both real tables — do not paste raw row samples from this column into any outbound doc, ticket, or Slack message without redacting.

**Before decommissioning:** you still need the connection audit-log data (from the Azure diagnostic settings steps we covered) to confirm nothing is actively depending on this server, plus a check with `JonBradshaw` (the resource `Owner` tag) given `review: true` is set. Want me to draft the `DESCRIBE pet_diabetes;` follow-up query, or pull the `FTFL-687` Jira ticket details next?