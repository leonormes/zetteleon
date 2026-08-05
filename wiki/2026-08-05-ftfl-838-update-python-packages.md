---
type: agent/solution
title: 'FTFL-838: Update Python packages (setuptools 70.0, urllib3 2.7.0)'
actor: agent/hermes/v4
generated: '2026-08-05'
verified: '2026-08-05'
stale_after: '2027-02-05'
tags:
- python
- poetry
- sftp-loader
- emis-processing
- medcat
- nhs-pet
- workflows-api
permalink: llmeon/wiki/2026-08-05-ftfl-838-update-python-packages
---

# FTFL-838: Update Python packages (setuptools 70.0, urllib3 2.7.0)

SBOM for NUH flagged outdated Python packages across the repo's Poetry-managed projects.

## Changes made

| Package | Task | Old | New |
|---------|------|-----|-----|
| setuptools | medcat-annotation | 69.5.1 | 83.0.0 |
| setuptools | set_intersection_estimator | 69.5.1 | 83.0.0 |
| urllib3 | workflows-api | 2.5.0 | 2.7.0 |
| urllib3 | emis-processing | 2.0.7 | 2.7.0 |
| urllib3 | medcat-annotation | 2.2.1 | 2.7.0 |
| urllib3 | nhs-pet | 2.5.0 | 2.7.0 |
| urllib3 | set_intersection_estimator | 2.2.1 | 2.7.0 |
| urllib3 | sftp-loader | 1.26.16 | 2.7.0 |

## Issues encountered

### Default-exit-handler
`poetry update urllib3` failed: "not a dependency of this project". The project only depends on `pika`. Old lock file had urllib3 from a prior artifact. Lock regenerated without it.

### Emis-processing + sftp-loader (boto3 pin)
Botocore 1.31.85 pins urllib3 to `<2.1` for Python 3.9. To allow urllib3 >= 2.7.0, updated `boto3` from exact `'1.28.85'` to `'^1.35.0'`. This bumps botocore to 1.42.97 which opens the urllib3 constraint to `<3.0` for Python 3.10+.

For **emis-processing** (Python ^3.9.16): botocore 1.42.97 still constrains urllib3 to `<1.27` for Python < 3.10. Lock file ended up with dual urllib3 versions: 1.26.20 (Python 3.9) and 2.7.0 (Python 3.10+). To get 2.7.0 on Python 3.9, would need to bump the project's minimum Python version.

### Default-exit-handler pyproject.toml
Had `repository = ""` — Poetry 2.x rejects this. Removed the empty field.

### Setuptools >=72.0 removed pkg_resources (medcat breakage)
`poetry update setuptools` upgraded to 83.0.0, which removed the `pkg_resources` module. The `medcat` package imports `pkg_resources.get_distribution()` at import time, breaking medcat-annotation and set_intersection_estimator tests. Fixed by pinning `setuptools = "70.0"` as a direct dependency in both projects.

## Git
- Branch: `feature/FTFL-838-update-python-packages`
- Commits: `945b3481c`, `199388f4e`
- 12 files changed, 678 insertions, 191 deletions