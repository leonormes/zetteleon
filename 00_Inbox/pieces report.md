---
title: pieces report
type: note
permalink: llmeon/00-inbox/pieces-report
---

Pieces for Developers does not offer a built-in setting to redirect its Long-Term Memory (LTM) database to a different drive, but the storage folder is a plain, movable directory, so you can relocate it to your external HDD using a macOS symlink — and there are several official settings that reduce how much data accumulates on your internal disk in the first place.

## Where Pieces stores LTM data

On macOS, Pieces keeps all of its on-device data — LTM-2.7 context, snippets, settings, Conversational Search history, and logs — inside `~/Library/com.pieces.os/`, with the actual database living in the `production` subfolder. The Desktop App itself stores a smaller amount of separate data (settings, logs) in `~/Library/com.pieces.pfd/`. Pieces is explicitly local-first: everything stays on-device unless you turn on Personal Cloud or a cloud model provider, so the bulk of your disk usage is this one folder.[^1][^2]

## No native "change storage path" setting — but relocation is supported unofficially

The team has confirmed there is currently no UI option to pick a custom install/data path. In a 2024 support thread, a Pieces engineer stated they were "not yet working on the ability to choose your own file path but it is in the pipeline". A separate GitHub issue about resetting the logs location confirms this is still a known limitation. However, the official docs explicitly say you can "copy, compress, or relocate" the `com.pieces.os` folder — this is the same mechanism they document for migrating to a new machine or syncing via OneDrive. That means moving the real files to your external HDD and leaving a symbolic link in their place at `~/Library/com.pieces.os` is a supported-in-spirit (if manual) approach.[^3][^4][^1]

## Step-by-step: relocate the LTM folder to your external HDD

1. Quit Pieces Desktop App and PiecesOS completely (menu bar icon → Quit; use Activity Monitor to force-quit if needed).[^5]
2. Confirm your external HDD is reliably mounted at boot (e.g., `/Volumes/YourExternalHDD`) — if it's not always connected, skip to the storage-reduction section instead, since Pieces will fail to start if the folder is missing.
3. Move (not copy) the folders to the external drive:
```bash
mv ~/Library/com.pieces.os /Volumes/YourExternalHDD/PiecesData/com.pieces.os
mv ~/Library/com.pieces.pfd /Volumes/YourExternalHDD/PiecesData/com.pieces.pfd
```
4. Create symlinks at the original locations pointing to the new external paths:
```bash
ln -s /Volumes/YourExternalHDD/PiecesData/com.pieces.os ~/Library/com.pieces.os
ln -s /Volumes/YourExternalHDD/PiecesData/com.pieces.pfd ~/Library/com.pieces.pfd
```
5. Relaunch PiecesOS and the Desktop App and verify it reads/writes correctly (check that new snippets or memories appear, then check file timestamps on the external drive).

This general symlink technique for redirecting an app's `~/Library` data folder to an external volume is a well-established macOS practice for apps without native path settings. Two important caveats specific to Pieces: the official docs warn that installing PiecesOS itself into a cloud-synced or non-standard location (OneDrive, iCloud Drive) has caused install failures and broken updates, so treat this as a data-folder relocation, not an app-install relocation, and always fully quit both PiecesOS and the Desktop App before touching the folder. Also, because the external HDD must be mounted before Pieces starts, expect errors or a fresh empty database being auto-created if you boot without the drive attached — an alternative if your external drive isn't always connected is the sparse-disk-image method some Mac users use for portable/optional volumes, though this adds complexity for a database that's actively written to.[^6][^7][^8]

## Reducing how much data Pieces stores in the first place

Regardless of relocation, several native settings can shrink the LTM footprint noticeably:

- **Long-Term Memory Engine toggle**: Turn LTM off entirely, or scope it down, from `User Profile → Settings → Long-Term Memory`, in the *Memory Formation* section.[^9]
- **App Access Control / Proactive Deny List**: Restrict which applications Pieces is allowed to capture context from — fewer monitored apps means less captured screen/text data. The deny list lets you block apps (e.g., password managers, but equally any app whose context you don't need retained) before Pieces ever indexes them.[^10]
- **LTM Audio**: This is a preview feature (system audio + microphone capture) that adds meaningfully to storage if enabled; leave it off if you don't need meeting-transcript memories.[^9]
- **Clear Long-Term Memory Data**: Under *Stored Data* in the Long-Term Memory settings, you can open "Clear Long-Term Memory Data..." and scope deletions by time period, capture method (modality), and application source — useful for periodically trimming old context rather than keeping the full nine-month history.[^11][^9]
- **Optimize System RAM Usage**: This only affects memory (RAM), not disk, but is worth knowing about if you're also chasing performance, not just storage.[^9]

Pieces' CTO has stated that LTM-2.5's design goal is to store roughly 0.2 GB per month of workflow history, versus ~16 GB/month for comparable "record everything" tools like Rewind, because Pieces filters and summarizes rather than storing raw screenshots/video. If your `com.pieces.os/production` folder is far larger than that, it likely reflects a long capture history (LTM-2 stores up to nine months by default), and using the Clear Stored Data controls to prune older time periods is the quickest way to reclaim internal disk space without any symlink work.[^12][^13]

## Practical recommendation

Given your setup, the lowest-risk path is to first use "Clear Long-Term Memory Data" to trim anything older than you actually query, and tighten App Access Control so Pieces isn't indexing every application, since at ~0.2 GB/month that alone should meaningfully cut growth. If the existing folder is still too large after pruning, only then use the manual `mv` + `ln -s` symlink relocation to the external HDD, making sure the drive is always connected before Pieces launches, since there's no supported way to change the path from within the app itself yet.[^1][^12][^3][^9]

---

## References

1. [On-Device Storage & Logs - Pieces Docs](https://docs.pieces.app/products/core-dependencies/on-device-storage) - Inside com.pieces.os , the production folder contains your LTM-2.7 context and all other Pieces data...

2. [What is PiecesOS? - Pieces Docs](https://docs.pieces.app/products/core-dependencies/pieces-os) - All data captured by PiecesOS is stored locally on your device. Capture, indexing, and storage happe...

3. [database files for Pieces OS stored inside documents folder · Issue #7 · pieces-app/support](https://github.com/pieces-app/support/issues/7) - Note: this issue was created automatically from a service ticket. I installed Pieces on my Windows 1...

4. [Can't reset pieces logs location · Issue #404 · pieces-app/support](https://github.com/pieces-app/support/issues/404) - Software Desktop Application Operating System / Platform Windows Your Pieces OS Version 10.1.6 Early...

5. [Complete Uninstall Guide | macOS - Pieces Docs](https://docs.pieces.app/products/meet-pieces/macos-installation-guide/uninstall) - Learn how to completely uninstall Pieces from macOS, including removing all application data, prefer...

6. [How can I use Symlinks to store applications on an ...](https://www.reddit.com/r/mac/comments/1ew9rbf/how_can_i_use_symlinks_to_store_applications_on/) - You have to hold down command during drag and drop to actual move files to an external drive and not...

7. [Troubleshooting PiecesOS - Pieces Docs](https://docs.pieces.app/products/core-dependencies/pieces-os/troubleshooting) - If you installed PiecesOS to OneDrive, iCloud Drive, or another synced folder, you may see install f...

8. [Any better way to move app library path to external drive ...](https://apple.stackexchange.com/questions/381615/any-better-way-to-move-app-library-path-to-external-drive-than-using-symbolic-li) - My solution: Use Disk Utility.app to create a new blank image with sparseimage type and save it at t...

9. [Long-Term Memory Settings in Pieces Desktop](https://docs.pieces.app/products/desktop/configuration/long-term-memory) - To access Long-Term Memory settings, click your User Profile in the top left, then hover over Settin...

10. [Long Term Memory Settings](https://docs.pieces.app/products/organizations-and-teams/settings-ltm-sources) - Learn how to configure LTM context capture, application sources, denied websites, and default models...

11. [Configuring Pieces Desktop Application](https://docs.pieces.app/products/desktop/configuration) - Configure the Long-Term Memory Engine, control which applications Pieces can access, manage system p...

12. [How We Built a Second Brain for Developers: Inside Pieces LTM 2.5 and Pieces MCP Server](https://www.youtube.com/watch?v=0XXq1X5YeR4) - What really happens behind the scenes of Pieces Long-Term Memory? In this in-depth interview, Pieces...

13. [LTM-2 and the Workstream Activity timeline — Pieces Updates](https://pieces.app/updates/ltm-2-workstream-activity-our-biggest-update-yet) - Now, instead of juggling multiple chats or searching through scattered notes, you can rely on one un...