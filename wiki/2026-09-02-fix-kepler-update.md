---
type: wiki
title: 'Fix: Kepler GitKraken ADE Update not Installing'
tags:
- hermes
- solution
- kepler
- gitkraken
- update
- macos
actor: agent/hermes/mechanical-lead
generated: 2026-09-02 07:50:00+01:00
verified: 2026-09-02 07:50:00+01:00
stale_after: 2027-03-01
permalink: llmeon/wiki/2026-09-02-fix-kepler-update
---

# Fix: Kepler GitKraken ADE Update Not Installing

## Problem

Kepler's auto-updater (Squirrel) downloaded 0.9.2 but couldn't install it, showing "move Kepler to Applications" even though it was already in `/Applications/`. Ownership change didn't help.

## Root Cause

Two layers to the problem:

1. **Initial failure** — `/Applications/Kepler.app` was owned by `root:admin` after first DMG install. Squirrel couldn't write a new version alongside the old one.

2. **Persistent failure after chown** — macOS Sequoia `/Applications/` directory itself isn't user-writable (`root:admin` but permission checks via `NSFileManager isWritableFileAtPath:` fail). Squirrel's `install refused: bundle cannot be replaced in place — reason: "read-only"` is triggered by the parent directory, not the app bundle.

## Fix

Manual update from the already-cached pending ZIP:

```bash
# 1. Quit Kepler
osascript -e 'quit app "Kepler"'
pkill -9 -f "Kepler.app"

# 2. Extract pending update (already auto-downloaded to cache)
cd /tmp
unzip -q ~/Library/Caches/kepler-updater/pending/kepler-arm64-mac.zip

# 3. Replace app bundle (needs sudo because /Applications/ is root-owned)
sudo mv /Applications/Kepler.app /Applications/Kepler.app.old
sudo cp -R /tmp/kepler-update/Kepler.app /Applications/
sudo chown -R leon.ormes:admin /Applications/Kepler.app

# 4. Clean up old & cache
sudo rm -rf /Applications/Kepler.app.old
rm -rf /tmp/kepler-update
rm -rf ~/Library/Caches/kepler-updater/pending

# 5. Relaunch
open /Applications/Kepler.app
```

## Verification

Logs after relaunch confirm:
- `[updater] Update for version 0.9.2 is not available (latest version: 0.9.2, downgrade is disallowed).`
- `[updater] up to date {"version":"0.9.2","channel":"production"}`

## Download URLs

- Update manifest: `https://kepler.gitkraken.com/production/latest-mac.yml`
- Direct ARM64 ZIP: `https://kepler.gitkraken.com/production/0.9.2/kepler-arm64-mac.zip`
- Download page: `https://gitkraken.com/kepler/download`