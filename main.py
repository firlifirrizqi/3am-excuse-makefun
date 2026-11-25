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
GATE_MIN_CHARS = 1
GATE_MAX_CHARS = 200


def normalize_entry(line):
    """Normalize a candidate line: strip surrounding whitespace and
    collapse any run of whitespace to a single space.

    The chosen line is already clean, so normalizing it is a no-op --
    this guards the entry against accidental double spaces or a stray
    trailing newline if the line is ever edited.
    """
    return " ".join(line.split())


def count_characters(line):
    """Return the character count of the line."""
    return len(line)


def count_words(line):
    """Return the word count of the line."""
    return len(line.split())


def check_single_line(line):
    """Check the entry is exactly one line (no embedded newlines)."""
    if "\n" in line or "\r" in line:
        return False, "contains a newline"
    return True, "ok"


def check_gate(line):
    """Check the competition gate: UTF-8 text, 1-200 chars, not only
    whitespace, and a single line.

    Returns (ok, reason).
    """
    if not line:
        return False, "empty"
    if line.strip() == "":
        return False, "only whitespace"
    if not GATE_MIN_CHARS <= len(line) <= GATE_MAX_CHARS:
        return False, f"length {len(line)} outside 1-200"
    ok_single, single_reason = check_single_line(line)
    if not ok_single:
        return False, single_reason
    try:
        line.encode("utf-8")
    except UnicodeEncodeError as exc:
        return False, f"not UTF-8 encodable: {exc}"
    return True, "ok"


def write_entry(path=OUTPUT_PATH, line=LINE):
    """Write the line to path, creating the directory if needed."""
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(line)
    return path


def read_back(path=OUTPUT_PATH):
    """Read the written file back as UTF-8 text."""
    with open(path, "r", encoding="utf-8") as handle:
        return handle.read()


def summarize_entry(line):
    """Build a small summary dict describing one line: its size in
    characters and words, whether it passes the gate, and whether
    normalizing it would change anything."""
    ok_gate, gate_reason = check_gate(line)
    return {
        "characters": count_characters(line),
        "words": count_words(line),
        "gate": gate_reason,
        "gate_ok": ok_gate,
        "normalized_matches": normalize_entry(line) == line,
    }


def verify_entry(path=OUTPUT_PATH, line=LINE):
    """Verify the written file is byte-identical to the chosen line
    and passes the gate. Returns (ok, details dict)."""
    written = read_back(path)
    summary = summarize_entry(written)
    byte_identical = written == line
    details = {
        "characters": summary["characters"],
        "words": summary["words"],
        "gate": summary["gate"],
        "byte_identical": byte_identical,
        "normalized_matches": summary["normalized_matches"],
    }
    return summary["gate_ok"] and byte_identical, details


def format_report(path, details):
    """Format the verification details as human-readable report lines."""
    return [
        f"Wrote {details['characters']} characters "
        f"({details['words']} words) to {path}",
        f"Gate: {details['gate']}",
        f"Byte-identical read-back: {details['byte_identical']}",
        f"Normalization no-op: {details['normalized_matches']}",
    ]


def validate_line(line):
    """Validate a line before writing: it must already be in
    normalized form (normalizing changes nothing) and it must pass
    the competition gate. Returns (ok, reason)."""
    if normalize_entry(line) != line:
        return False, "line is not in normalized form"
    return check_gate(line)


def main():
    ok_line, line_reason = validate_line(LINE)
    if not ok_line:
        raise SystemExit(f"Line validation FAILED: {line_reason}")
    path = write_entry()
    ok, details = verify_entry(path)
    for report_line in format_report(path, details):
        print(report_line)
    if not ok:
        raise SystemExit(f"Verification FAILED: {details}")
    print("Verification PASSED")


if __name__ == "__main__":
    main()
