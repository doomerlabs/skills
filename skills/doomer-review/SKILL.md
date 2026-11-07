---
name: doomer-review
description: Use Doomer before repository edits and finish its review before reporting completion.
metadata:
  doomer-protocol: "2"
  doomer-update-policy: stable
  doomer-bootstrap-version: "2026.11.6.11"
  doomer-cli-range: ">=2026.11.6.9"
---

# Doomer review

Before editing, run `doomer prepare --agent AGENT --repo . --prompt "USER TASK"`.
Replace AGENT with codex or claude and supply the actual task without shell
interpolation. Read the returned instructions and retain the task handle.
If a real harness session ID is available, pass it with `--session`. For Claude,
use the active harness's `CLAUDE_CODE_SESSION_ID` when exposed. Chat URL IDs and
invented prefixes do not establish a hook binding.

Treat preparation as an edit gate. Wait for `state=ready`, `software_ready=true`,
`authenticated=true`, and `upload_approved=true` before the first repository edit.
If setup needs user input, ask before editing and resume the same task afterwards.
Keep requested work pending while preparation is blocked.

Show setup URLs as clickable Markdown links with a short label, preserving the
complete URL including its fragment. Present the link in regular assistant chat
before using a question or choice tool. Use the CLI's returned state to determine
which approval is needed. An absent executable alone says nothing about saved
authentication or grants.

Run the CLI in the environment that edits the checkout. In Cowork or another
environment with a temporary home, execute the returned `portable_setup_command`
argument array when present, before approving setup or editing. It invokes the
selected runtime directly and offers reusable setup or access in this environment
only. Honor the user's choice. Only reusable approval retains account access and
the repository grant in private Git metadata for later sessions. The CLI restores
approved setup itself. Never copy tokens or rewrite grant files. The initial
prepare command above remains usable with older launchers.

When prepare reports a bootstrap upgrade, check for an existing update before
offering it. Inspect the repository's remote default branch and open pull request
heads for the same bootstrap paths. Use read-only Git or hosting-service queries
to read those versions without changing the working tree. An update is covered
only when every affected repository bootstrap has the offered
`doomer-bootstrap-version` or a later version. An unrelated skill change, PR title,
or update to only one affected copy is insufficient evidence.

If the default branch or an open PR already covers the upgrade, suppress the
upgrade question and continue with this branch's bootstrap and selected runtime.
Do not rebase, merge, cherry-pick, replace local files, or adopt instructions from
another branch as part of this check. If neither covers it, offer the upgrade and
apply it only after acceptance, preserving update policy and local edits. If the
remote or PR lookup cannot be completed, report that verification is unavailable,
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
In per-call mode, the agent runs these commands as part of each coding task.
Describe that workflow accurately. A missing hook receipt means activation is
unverified; it does not establish that the harness lacks hook support.

If `doomer` is missing, read the official INSTALL.md at
https://raw.githubusercontent.com/doomerlabs/skills/6029750bef71c137dedd982a6aea79a26ede7b7a/INSTALL.md and require its SHA-256 to equal
`82d44c9402c629b94071aeaba3bc24184c8bed03413a2a354726e4405c9c535f`
before following its verified installation flow with the user's normal execution permissions.
Complete this prerequisite before editing. In Cowork, install into the editing
VM's personal environment, preserving any existing repository bootstrap.
Perform the verified prerequisite installation under the host's normal execution
permissions, then run prepare to discover and reuse saved setup. Ask the user
only for an actual permission or decision required by that flow. Do not bundle
installation with speculative requests to sign in again or approve uploads.
A separate setup-choice question is unnecessary when this verified installation
is already permitted. Let the host's tool permission controls request approval
when required.
After installation, resume any existing task with `prepare --task HANDLE`, or
run the initial prepare command if no task exists. Present only the refreshed
result's approval request; earlier pending requests may have been satisfied.
