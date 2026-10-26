"""
Test runner for main.py.

For every tests/NN_name_in.txt, runs `python3 main.py` on it and compares
stdout to tests/NN_name_out.txt. Windows (CRLF) line endings are ignored,
since the prof's example files use them.

Usage:
    python3 run_tests.py
"""

import os
import subprocess
import sys

TESTS_FOLDER = "tests"
INPUT_SUFFIX = "_in.txt"
OUTPUT_SUFFIX = "_out.txt"
PROGRAM = "main.py"


def normalize(text):
    """Strip CRLF so Windows and Linux line endings compare equal."""
    return text.replace("\r\n", "\n").rstrip("\n")


def run_one_test(input_path, expected_path):
    """Return (passed, actual_text, expected_text)."""
    result = subprocess.run(
        [sys.executable, PROGRAM, input_path],
        capture_output=True,
        text=True,
    )
    with open(expected_path) as expected_file:
        expected_text = normalize(expected_file.read())
    actual_text = normalize(result.stdout)
    return actual_text == expected_text, actual_text, expected_text


def main():
    input_files = sorted(
        name for name in os.listdir(TESTS_FOLDER) if name.endswith(INPUT_SUFFIX)
    )
    passed_count = 0

    for input_name in input_files:
        test_name = input_name[: -len(INPUT_SUFFIX)]
        input_path = os.path.join(TESTS_FOLDER, input_name)
        expected_path = os.path.join(TESTS_FOLDER, test_name + OUTPUT_SUFFIX)

        passed, actual_text, expected_text = run_one_test(input_path, expected_path)
        if passed:
            passed_count += 1
            print("PASS  " + test_name)
        else:
            print("FAIL  " + test_name)
            print("  --- expected ---")
            print("  " + expected_text.replace("\n", "\n  "))
            print("  --- actual ---")
            print("  " + actual_text.replace("\n", "\n  "))

    print("\n%d / %d passed" % (passed_count, len(input_files)))


if __name__ == "__main__":
    main()
