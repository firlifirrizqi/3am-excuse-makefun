#!/usr/bin/env python3
"""The 3 AM Excuse -- make.fun entry.

Writes one line of text -- the excuse a hardware wallet gives for
refusing to sign a transaction at 3 AM -- to /output/entry.txt.

Stdlib only. No network, no secrets, no reading outside this repo.
"""

import os

# The chosen line (91 characters, inside the 1-200 gate).
LINE = (
    "At 3 AM, I stop being your wallet and start being your "
    "designated driver. The answer is no."
)

OUTPUT_PATH = "/output/entry.txt"


def write_entry(path=OUTPUT_PATH, line=LINE):
    """Write the line to path, creating the directory if needed."""
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(line)
    return path


def count_characters(line):
    """Return the character count of the line."""
    return len(line)


def check_gate(line):
    """Check the competition gate: UTF-8 text, 1-200 chars, not only whitespace.

    Returns (ok, reason).
    """
    if not line:
        return False, "empty"
    if line.strip() == "":
        return False, "only whitespace"
    if not 1 <= len(line) <= 200:
        return False, f"length {len(line)} outside 1-200"
    try:
        line.encode("utf-8")
    except UnicodeEncodeError as exc:
        return False, f"not UTF-8 encodable: {exc}"
    return True, "ok"


def read_back(path=OUTPUT_PATH):
    """Read the written file back as UTF-8 text."""
    with open(path, "r", encoding="utf-8") as handle:
        return handle.read()


def verify_entry(path=OUTPUT_PATH, line=LINE):
    """Verify the written file is byte-identical to the chosen line
    and passes the gate. Returns (ok, details dict)."""
    written = read_back(path)
    ok_gate, gate_reason = check_gate(written)
    byte_identical = written == line
    details = {
        "characters": count_characters(written),
        "gate": gate_reason,
        "byte_identical": byte_identical,
    }
    return ok_gate and byte_identical, details


def main():
    path = write_entry()
    ok, details = verify_entry(path)
    print(f"Wrote {details['characters']} characters to {path}")
    print(f"Gate: {details['gate']}")
    print(f"Byte-identical read-back: {details['byte_identical']}")
    if not ok:
        raise SystemExit(f"Verification FAILED: {details}")
    print("Verification PASSED")


if __name__ == "__main__":
    main()
