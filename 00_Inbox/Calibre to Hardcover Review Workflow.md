---
conformant: true
created: 2026-11-24 12:00:00+00:00
modified: 2026-11-24 12:00:00+00:00
status: draft
tags:
- topic/reading
- tool/calibre
- tool/hardcover
title: Calibre to Hardcover Review Workflow
type: protocol
permalink: llmeon/00-inbox/calibre-to-hardcover-review-workflow
---

# Calibre to Hardcover Review Workflow

Purpose: rate and review fiction I love in Calibre so Hardcover can recommend similar books. Verified 2026-11-24 against the Hardcover Sync plugin v0.3.1 source and the [hardcover-docs repo](https://github.com/hardcoverapp/hardcover-docs/). docs.hardcover.app itself blocks automated fetches (Cloudflare 403).

## How sync works
- Only the plugin columns sync: `#hc_rating` (half stars), `#review`, `#hc_status`, `#hc_notes`, `#hc_quotes`. The built-in Rating column does NOT sync.
- Auto-push is on (`auto_push: true`): editing a plugin column pushes it shortly after, for books with a Hardcover identifier (`hardcover-id`, `hardcover-slug` or `hardcover-edition`).
- Pulling is manual: Pull Rating / Review / Status from the plugin menu.
- A first rating also sets the book to Read (status 3) on Hardcover.
- Rating scale: Hardcover 0-5 with halves; the plugin converts from Calibre 0-10.
- Reviews are flattened to plain paragraphs on push (no bold, italics or links). The plugin does not set the spoiler flag.
- API limits (Free): 5,000 requests a day, 60 a minute, burst 10. Plugin is set to 30 a minute.
- Tokens made before August 2026 have full access. A new token needs `read:library` and `write:library` (plus `read:lists`/`write:lists` for the Lists column).

## One-off setup
1. Bind shortcuts: Preferences, Keyboard shortcuts, group Hardcover Sync (Push Review, Pull Rating, Pull Status).
2. Check default reading privacy on Hardcover so reviews are not private.

## Per book
1. Download metadata from Hardcover to get an identifier; check the edition is right.
2. Set `#hc_status`.
3. Set `#hc_rating` (not the built-in Rating).
4. Write `#review` as plain text, for discovery: tone and pace, who it suits, two or three comparable books, what made it land.
5. Let auto-push run; a red pin on the row means the push failed (no identifier or a 403 scope error). Spot-check on Hardcover.

## Weekly
- Select all, Pull Rating / Review / Status to catch changes made in the Hardcover app.
- Use Hardcover recommendations; add candidates to the Hardcover Lists column or Want to Read.

## Back catalogue (2026-11-24 count)
520 books; 70 have a built-in rating, all 70 linked to Hardcover; 4 already have `#hc_rating`, so 65 need copying into `#hc_rating`.