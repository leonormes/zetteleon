# Golden Tests

Golden tests are fixed scenarios with expected behaviors used to prevent regressions in the recommendation pipeline.

## Structure

Each `*.json` file defines:

- `name`: scenario identifier
- `description`: human‑readable intent
- `input`: the runtime context
  - `now`: ISO timestamp (optional)
  - `context`: `{ time_available_min, energy, contexts[] }`
  - `tasks`: array of CanonicalTask (see product spec)
- `expected`: assertions
  - `must`: array of conditions `{ field, contains | equals }`
  - `must_not`: conditions to forbid
  - `thresholds`: `{ score_min, confidence_min }`
  - `policy`: `{ protect_renewal, respect_time_window }`

## Usage

- Feed `input` to the pipeline (mock retrieval if needed)
- Compare the top recommendation with `expected`
- Record pass/fail in `reports/`

## Notes

- Keep scenarios minimal but decisive
- Prefer assertions over exact string matches
- Extend with additional scenarios as behaviors evolve
