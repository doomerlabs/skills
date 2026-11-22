---
name: check-skill
description: Scan an agent skill with CheckSkill, fix actionable findings, and rescan. Use when asked to check a SKILL.md or skill folder before publishing.
---

# CheckSkill

Scan the current version of the selected skill at `https://checkskill.ai/api/scan`.

- For just `SKILL.md`, POST its contents as `text/markdown`.
- For a skill with supporting files, POST JSON as `application/json`. Send a `files` array with one `{ "path": "...", "content": "..." }` object per UTF-8 file in the skill package, including `SKILL.md`. Use paths relative to the upload root.

Resolve the directory containing the selected regular `SKILL.md` and use it as the upload root. For a folder scan, walk that directory recursively and skip symlinked files and directories. Before reading each file, verify its resolved path is inside the upload root. Exclude parent and sibling directories, including files linked from the skill.

If a file contains a live secret or cannot be sent, resolve that before uploading it. Report any gap in the files checked.

Use the returned `findings` and `snykForecast.issues` to locate errors and warnings. Read the cited passages and fix the underlying behavior while preserving the skill's purpose and safeguards. Resubmit the full set after each edit.

A clean scan requires `limited: false`, an empty `snykForecast.issues` array, and no remaining errors or warnings in `findings`. If you cannot reach a clean scan, report the blocker and remaining findings.
