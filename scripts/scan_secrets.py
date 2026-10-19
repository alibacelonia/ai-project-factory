"""Fail when detect-secrets reports a likely secret in a publishable file."""

from __future__ import annotations

import json
import subprocess
import sys


def publishable_files() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        check=True,
        capture_output=True,
    )
    return [item.decode() for item in result.stdout.split(b"\0") if item]


def main() -> int:
    files = publishable_files()
    result = subprocess.run(
        ["detect-secrets", "scan", *files],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(result.stderr or "detect-secrets failed", file=sys.stderr)
        return result.returncode

    report = json.loads(result.stdout)
    findings = report.get("results", {})
    if findings:
        print("Potential secrets detected:", file=sys.stderr)
        for filename, matches in sorted(findings.items()):
            lines = ", ".join(str(match["line_number"]) for match in matches)
            print(f"- {filename}: line(s) {lines}", file=sys.stderr)
        print("Review each finding; never allowlist a real credential.", file=sys.stderr)
        return 1

    print(f"Secret scan passed for {len(files)} publishable files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
