#!/usr/bin/env python3
"""Verify an explicitly pinned skill against the runner's canonical bootstrap."""
import argparse
from pathlib import Path
import re
import subprocess
import tempfile


def stable_verification_copy(text: str, version: str) -> str:
    """Change only the three approved policy fields for canonical verification."""
    if not re.fullmatch(r"20\d{2}\.\d{1,2}\.\d{1,2}\.[1-9]\d*", version):
        raise ValueError("expected an exact four-part release version")
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        raise ValueError("skill requires YAML frontmatter")
    header, body = text[4:].split("\n---\n", 1)
    replacements = {
        "doomer-cli-range": (f"  doomer-cli-range: '={version}'", f"  doomer-cli-range: '>={version}'"),
        "doomer-update-policy": ("  doomer-update-policy: pinned", "  doomer-update-policy: stable"),
        "doomer-version": (f"  doomer-version: {version}", None),
    }
    lines = header.split("\n")
    for key, (expected, replacement) in replacements.items():
        matches = [i for i, line in enumerate(lines) if re.match(rf"\s*{re.escape(key)}\s*:", line)]
        if len(matches) != 1 or lines[matches[0]] != expected:
            raise ValueError(f"expected exactly one {expected.strip()}")
        if replacement is None:
            del lines[matches[0]]
        else:
            lines[matches[0]] = replacement
    return "---\n" + "\n".join(lines) + "\n---\n" + body


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runner", type=Path, required=True)
    parser.add_argument("--skill", type=Path, required=True)
    parser.add_argument("--pinned-version", required=True)
    args = parser.parse_args()
    try:
        original = args.skill.read_bytes().decode("utf-8")
        normalized = stable_verification_copy(original, args.pinned_version)
    except (OSError, ValueError) as error:
        parser.exit(1, f"Pinned bootstrap verification failed: {error}\n")
    with tempfile.TemporaryDirectory(prefix="doomer-bootstrap-check-") as directory:
        candidate = Path(directory) / "SKILL.md"
        candidate.write_bytes(normalized.encode("utf-8"))
        result = subprocess.run(
            ["go", "run", "./scripts/verify-skill-bootstrap.go", "--skill", str(candidate)],
            cwd=args.runner,
        )
        if result.returncode:
            parser.exit(result.returncode)
    print(f"Pinned skill matches canonical bootstrap; release locked to {args.pinned_version}")


if __name__ == "__main__":
    main()
