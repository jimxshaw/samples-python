#!/bin/bash
# Run every tests/exN.var + tests/exN.con in both modes and diff the result
# against tests/exN-none.out and tests/exN-fc.out (if those files exist).
# If the program crashes, its error message is shown instead of hidden.
# Usage:  bash run_tests.sh
cd "$(dirname "$0")"
pass=0; fail=0
errfile=$(mktemp)
for var in tests/*.var; do
    base="${var%.var}"
    for mode in none fc; do
        expected="${base}-${mode}.out"
        [ -f "$expected" ] || continue
        actual=$(python3 main.py "$var" "${base}.con" "$mode" 2>"$errfile")
        if [ -s "$errfile" ]; then
            echo "CRASH $(basename "$base") $mode"; fail=$((fail+1))
            sed 's/^/      /' "$errfile"
        elif diff <(echo "$actual") "$expected" > /dev/null; then
            echo "PASS  $(basename "$base") $mode"; pass=$((pass+1))
        else
            echo "FAIL  $(basename "$base") $mode"; fail=$((fail+1))
            diff <(echo "$actual") "$expected" | sed 's/^/      /'
        fi
    done
done
rm -f "$errfile"
echo "-- $pass passed, $fail failed"