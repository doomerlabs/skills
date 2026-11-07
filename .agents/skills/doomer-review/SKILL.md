---
name: doomer-review
description: Use Doomer before repository edits and finish its review before reporting completion.
metadata:
  doomer-protocol: "2"
  doomer-update-policy: stable
---

# Doomer review

Before editing, run `doomer prepare --agent AGENT --repo . --prompt "USER TASK"`.
Replace AGENT with codex or claude and supply the actual task without shell
interpolation. Read the returned instructions and retain the task handle.
If a real harness session ID is available, pass it with `--session`.

When prepare reports a bootstrap upgrade, check for an existing update before
offering it. Identify the repository this branch is intended to merge into from
the current PR's base repository or the established project remote. Inspect that
repository's actual default branch and open PR heads for the same bootstrap paths.
Do not assume the remote is `origin` or the default branch is `main`. Use read-only
Git or hosting-service queries without changing the working tree. An update is
covered only when every affected repository bootstrap has the offered
`doomer-bootstrap-version` or a later version, comparing numeric version parts.
An unrelated skill change, PR title, or update to only one affected copy is
insufficient evidence.

If the default branch or an open PR already covers the upgrade, suppress the
upgrade question and continue with this branch's bootstrap and selected runtime.
Do not rebase, merge, cherry-pick, replace local files, or adopt instructions from
another branch as part of this check. If neither covers it, offer the upgrade and
apply it only after acceptance, preserving update policy and local edits. If the
target repository is ambiguous or a lookup fails, report verification unavailable,
keep the current version, and defer the upgrade question for this session.

Resume an existing task with `doomer prepare --task HANDLE` after interruption.
Never create a replacement task to recover an existing review. If that task's
selected runtime is missing, run `doomer task repair HANDLE` through the available
launcher, then resume the same handle. Repair restores that exact release; do not
substitute the current stable release for an active task. Follow structured
user-action requests. Never invent consent, account identity, or hook activation.
Reading this file directly is sufficient; native skill discovery is optional.

The selected CLI supplies its matching full instructions. Use its task commands
to submit changes, retrieve results, record every finding response, and verify
completion. A pending result or installed CLI does not establish a completed review.

If `doomer` is missing, read the official INSTALL.md at
https://raw.githubusercontent.com/doomerlabs/skills/b8611b37c4ef8ce47fd66b04af9166e047b9e0f3/INSTALL.md and require its SHA-256 to equal
`6f9566430e2f1646209daaa1e79a7ab1b93857bf6a35997085092eae996932a1`
before following its verified installation flow with the user's normal execution permissions.
