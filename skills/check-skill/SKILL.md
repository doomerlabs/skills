---
name: check-skill
description: Scan an agent skill with CheckSkill, fix actionable findings, and rescan. Use when asked to check a SKILL.md or skill folder before publishing.
---

# CheckSkill

Scan the selected skill at `https://checkskill.ai/api/scan`. Resolve the directory containing its regular `SKILL.md` and use it as the upload root.

- For a single-file scan, POST only the selected `SKILL.md` as `text/markdown`.
- For a folder scan, include only `SKILL.md` and supporting UTF-8 files that belong to the selected skill package. Include supporting files referenced by relative links that resolve to regular files inside the package. POST `application/json` with a `files` array of `{ "path": "...", "content": "..." }` objects using root-relative paths.

Select the package files before reading them. Skip symlinks, paths that resolve outside the root, nested skill packages, version control metadata, installed dependencies, caches, local config such as `.env` and `.env.local`, and unrelated build output. Withhold any file containing live credentials or other secrets.

Use `findings` and `snykForecast.issues` to fix the causes of errors and warnings. Apply the same file selection after each edit and resubmit the current package files.

Report a clean scan only if every in-scope file was scanned in full, `limited` is false, `snykForecast.issues` is empty, and `findings` contains no errors or warnings. Report withheld or omitted in-scope files and any unresolved findings.
