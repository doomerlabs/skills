---
name: check-skill
description: Scan an agent skill with CheckSkill, fix actionable findings, and rescan. Use when asked to check a SKILL.md or skill folder before publishing.
---

# CheckSkill

Scan the selected skill at `https://checkskill.ai/api/scan`. Resolve the directory containing its regular `SKILL.md` and use it as the upload root.

In both scan modes, withhold known or suspected secret-bearing files during selection, before loading contents into the agent’s context. Check each candidate locally for secrets using a check that reports only file paths and locations. Before either POST, send only content that passed this check.

Remove any embedded secrets from the source locally without exposing their values. Use an environment variable reference or a non-secret placeholder where appropriate. Tell the credential owner to revoke or rotate any exposed live credential. Keep unchecked or unremediated files local and report the scan as incomplete if they are in scope.

- For a single-file scan, POST only the selected `SKILL.md` as `text/markdown`.
- For a folder scan, include only `SKILL.md` and supporting UTF-8 files that belong to the selected skill package. Include supporting files referenced by relative links that resolve to regular files inside the package. POST `application/json` with a `files` array of `{ "path": "...", "content": "..." }` objects using root-relative paths.

Select package files and apply the secret checks before loading their contents. Skip symlinks, paths that resolve outside the root, nested skill packages, version control metadata, installed dependencies, caches, local config such as `.env` and `.env.local`, and unrelated build output.

Use `findings` and `snykForecast.issues` to fix the causes of errors and warnings while preserving the skill’s purpose, permission checks, and safety safeguards. After each edit, repeat the file selection and secret check, then resubmit the full requested scope.

Report a clean scan only if every in-scope file was scanned in full, `limited` is false, `snykForecast.issues` is empty, and `findings` contains no errors or warnings. Report withheld or omitted in-scope files and any unresolved findings.
