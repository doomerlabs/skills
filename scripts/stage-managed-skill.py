#!/usr/bin/env python3
"""Stage an official skill tree with byte-verifiable provenance markers."""
import argparse
import os
from pathlib import Path
import re
import subprocess


def render(data, source, revision):
    if not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise ValueError("Expected a full source commit")
    marker = ("<!-- doomer-managed\npackage: doomerlabs/skills\n"
              f"revision: {revision}\nsource: {source}\nkind: file\n-->\n").encode()
    if source.endswith("/SKILL.md"):
        end = data.find(b"\n---\n", 4)
        if not data.startswith(b"---\n") or end < 0:
            raise ValueError("SKILL.md requires YAML frontmatter")
        end += 5
        return data[:end] + marker + data[end:]
    return marker + data


PROJECT_SKILL_PATHS = (
    Path(".agents/skills/doomer-review"),
    Path(".claude/skills/doomer-review"),
)


def stage(source_root, destination, revision, *, both_agents=False):
    root = Path(source_root).resolve()
    actual = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
    if actual != revision:
        raise ValueError("Source checkout does not match selected commit")
    source = root / "skills/doomer-review"
    if source.is_symlink() or not source.is_dir():
        raise ValueError("Missing regular skill source directory")
    expected = subprocess.check_output(
        ["git", "-C", str(root), "ls-tree", "-r", "--name-only", revision, "--", "skills/doomer-review/"],
        text=True,
    ).splitlines()
    observed = []
    files = []
    for directory, directories, names in os.walk(source, followlinks=False):
        for name in directories + names:
            item = Path(directory) / name
            if item.is_symlink() or not (item.is_file() or item.is_dir()):
                raise ValueError(f"Unsupported source entry {item}")
        for name in names:
            item = Path(directory) / name
            relative = item.relative_to(root).as_posix()
            observed.append(relative)
            data = item.read_bytes()
            tracked = subprocess.check_output(["git", "-C", str(root), "show", f"{revision}:{relative}"])
            if data != tracked:
                raise ValueError(f"Modified source entry {relative}")
            files.append((item.relative_to(source), render(data, relative, revision) if item.suffix == ".md" else data))
    if sorted(observed) != sorted(expected):
        raise ValueError("Source inventory does not match selected commit")
    for required in ("SKILL.md", "references/install.md", "references/updates.md"):
        if f"skills/doomer-review/{required}" not in observed:
            raise ValueError(f"Missing required source file {required}")
    target = Path(destination)
    target.mkdir(mode=0o700, parents=False, exist_ok=False)
    destinations = PROJECT_SKILL_PATHS if both_agents else (Path("."),)
    for destination in destinations:
        for relative, data in files:
            file = target / destination / relative
            file.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
            file.write_bytes(data)
            file.chmod(0o644)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_root")
    parser.add_argument("revision")
    parser.add_argument("destination", help="New staging directory, never an existing installation")
    parser.add_argument("--both-agents", action="store_true",
                        help="Stage matching regular copies at both project skill paths")
    args = parser.parse_args()
    stage(args.source_root, args.destination, args.revision, both_agents=args.both_agents)
