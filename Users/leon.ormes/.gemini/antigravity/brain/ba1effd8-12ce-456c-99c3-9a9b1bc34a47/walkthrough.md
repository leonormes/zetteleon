

## MinHash Usage & Verification Guide

Follow these instructions to build, test, and run the new MinHash implementation.

### 1. Build the Release Binary

Ensure you have a clean release build for maximum performance.

```bash
cargo build --release
```

### 2. Run Unit Tests

Verify that the MinHash implementation and join logic are working correctly.

```bash
cargo test strategies::min_hash
```

You should see output indicating `test_minhash_join_correctness` passed.

### 3. End-to-End Benchmark Example

1. **Generate Data** (Optional, if you don't have datasets):
   ```bash
   mkdir -p tests/data/bench_1m
   ./target/release/ude_worker generate-dataset \
     --output-path tests/data/bench_1m/ \
     --dataset-length 1000000 \
     --match-percentage 0.5 \
     --uniform \
     --no-match-length 0
   ```

2. **Create MinHash Signatures** (Left & Right):
   ```bash
   # Left Dataset
   ./target/release/ude_worker create \
     --dataset tests/data/bench_1m/left_dataset.json \
     --dataset-type json \
     --schema-json tests/data/bench_1m/dataset_schema.json \
     --output-dataset tests/data/bench_1m/left_hashed.parquet \
     --output-dataset-format parquet \
     --output-schema-json tests/data/bench_1m/left_schema.json \
     --ude-key "secret" \
     --key-fields "signature=id" \
     --salt "mysalt" \
     min-hash

   # Right Dataset
   ./target/release/ude_worker create \
     --dataset tests/data/bench_1m/right_dataset.json \
     --dataset-type json \
     --schema-json tests/data/bench_1m/dataset_schema.json \
     --output-dataset tests/data/bench_1m/right_hashed.parquet \
     --output-dataset-format parquet \
     --output-schema-json tests/data/bench_1m/right_schema.json \
     --ude-key "secret" \
     --key-fields "signature=id" \
     --salt "mysalt" \
     min-hash
   ```
   *Note: Using Parquet output is recommended for binary signature performance.*

3. **Run MinHash Match**:
   ```bash
   /usr/bin/time -l ./target/release/ude_worker match \
     --dataset tests/data/bench_1m/left_hashed.parquet \
     --dataset-type parquet \
     --schema-json tests/data/bench_1m/left_schema.json \
     --input-ciphers tests/data/bench_1m/right_hashed.parquet \
     --input-ciphers-type parquet \
     --join-type inner \
     --key-fields "signature=signature" \
     --ude-key "secret" \
     --output-dataset tests/data/bench_1m/match_output.parquet \
     --output-dataset-format parquet \
     --output-schema-json tests/data/bench_1m/match_schema.json \
     min-hash
   ```

### 4. Verification
The `match_output.parquet` should contain 500,000 rows (given the 50% match rate generated above). You can inspect the results using a Parquet viewer or the provided `examples/inspect.rs` script.
