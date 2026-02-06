---
created: 2026-02-05T19:55:23+00:00
modified: 2026-02-05T20:00:28+00:00
title: nightly
---

```bash
unset RUSTUP_TOOLCHAIN
cargo +nightly update -p ahash --precise 0.8.12
cargo +nightly run -- key-gen
```
