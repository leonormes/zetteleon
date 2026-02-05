```bash
unset RUSTUP_TOOLCHAIN
cargo +nightly update -p ahash --precise 0.8.12
cargo +nightly run -- key-gen
```