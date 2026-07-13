---
created: 2026-02-05T19:55:23+00:00
modified: 2026-07-13T08:52:22+00:00
permalink: llmeon/30-library/200-projects/nightly-cargo-run-key-gen
project_category: refined_deployment
project_name: Refined Deployment
project_status: active
title: nightly cargo run -- key-gen
type: null
uuid: 933d0f4e-318d-4bee-a5ed-9e0ac7172dcf
---

```bash
unset RUSTUP_TOOLCHAIN
cargo +nightly update -p ahash --precise 0.8.12
cargo +nightly run -- key-gen
```

- [x] Update the ude key gen instructions^2026-02-11T07-59-32 [completion:: 2026-03-31]
	- [📱 View in Todoist app](todoist://task?id=10006834737) (Created: 📝 2026-02-11T08:00)
