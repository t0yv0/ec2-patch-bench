#!/usr/bin/env bash

set -euo pipefail

cd patch-testing

bench_one () {
    opt="$1"
    rc="$2"
    rp="$3"
    export PULUMI_OPTIMIZED_CHECKPOINT_PATCH="$opt"
    stack="bench-$opt-$rc-$rp-$RANDOM"
    pulumi stack init "$stack"
    pulumi stack select "$stack"
    pulumi config set patch-testing:resource_count "$rc"
    pulumi config set patch-testing:resource_payload_bytes "$rp"
    /usr/bin/time -o "time-$stack.txt" pulumi up --yes >"stdout-$stack.log" 2>"stderr-$stack.log" || echo "ERROR in $stack"
}

bench() {
    rc="$1"
    rp="$2"
    bench_one true "$rc" "$rp"
    bench_one false "$rc" "$rp"
}

bench 1  2
bench 2  2
bench 4  2
bench 8  2
bench 16 2
bench 32 2
bench 48 2
bench 64 2

bench 1  8192
bench 2  8192
bench 4  8192
bench 8  8192
bench 16 8192
bench 32 8192
bench 48 8192
bench 64 8192

bench 1  32768
bench 2  32768
bench 4  32768
bench 8  32768
bench 16 32768
bench 32 32768
bench 48 32768
bench 64 32768

bench 1  131072
bench 2  131072
bench 4  131072
bench 8  131072
bench 16 131072
bench 32 131072
bench 48 131072
bench 64 131072

bench 1  524288
bench 2  524288
bench 4  524288
bench 8  524288
bench 16 524288

bench 1  2097152
bench 2  2097152
bench 4  2097152
bench 8  2097152
bench 16 2097152

bench 4  8388608
bench 8  8388608
bench 12 8388608
bench 16 8388608
bench 20 8388608

bench 4  16777216
bench 8  16777216
bench 12 16777216
bench 16 16777216
bench 20 16777216

bench 4  25165824
bench 8  25165824
bench 12 25165824
bench 16 25165824
bench 20 25165824

bench 4  33554432
bench 8  33554432
bench 12 33554432
bench 16 33554432
bench 20 33554432
