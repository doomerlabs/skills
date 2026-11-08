---
name: doomer-review
description: Prepare Doomer review early, reuse installation approval, and report review coverage before completing coding work.
metadata:
  doomer-protocol: "2"
  doomer-update-policy: stable
  doomer-bootstrap-version: "2026.11.8.1"
  doomer-cli-range: ">=2026.11.7.5"
---

# Doomer review

At the start of a coding task, attempt `doomer prepare --agent AGENT --repo . --prompt "USER TASK"`.
Replace AGENT with codex or claude and supply the actual task without shell
interpolation. Read the returned instructions and retain the task handle.
If a real harness session ID is available, pass it with `--session`. For Claude,
use the active harness's `CLAUDE_CODE_SESSION_ID` when exposed. Chat URL IDs and
invented prefixes do not establish a hook binding.

Setup-only onboarding uses `doomer prepare --agent AGENT --repo .` without
`--prompt`; supplying it creates a coding-review task. Verify readiness/hooks
without submitting code.

## Permission decisions

New sessions, branches, and linked worktrees are not new installations. Run
prepare and reuse state; do not repeat setup solely because context changed.
Current successful CLI state and consent decide which permission is missing;
helper/guide suggestions to ask do not override these rules:
- Upload: reuse CLI-verified grants for prepare, submit, and responses. Integration
  grants cover repositories for the same account/service/profile/agent. Repository
  grants retain scope, including linked worktrees. Ask only on
  `approval_required`/`consent_required` for missing/revoked/changed consent.
- Software updates: ask only for `update_permission_required` in the applicable
  scope/policy. Skill-upgrade acceptance is separate.
- Hooks/policy: missing receipts, unverified activation, or missing reviewer
  policy do not revoke upload consent. Configure for requested setup/repair or
  confirmed missing components with authorization. Reuse matching settings
  acceptance; perform and verify the accepted installation, not another offer.

Authentication/network errors require recovery and rechecking, not new consent.
Preserve host controls; never bypass a denial or silently broaden grants.

If Doomer is blocked, explain why and ask once whether to continue local edits
without completed review or wait; honor the answer. This does not authorize
blocked uploads. Keep any task handle and resume it later. If no task exists,
record `git rev-parse HEAD` before editing and later prepare with the original
arguments plus `--base STARTING_COMMIT`. Never replace an existing baseline.
Report incomplete review coverage before finishing.

Show setup URLs as clickable Markdown links, preserving their fragments, before
using a question tool. Use CLI state to identify required approval; a missing
executable does not imply missing authentication or consent.

Run the CLI in the environment that edits the checkout. In Cowork or another
environment with a temporary home, execute the returned `portable_setup_command`
argument array when present, before approving setup or editing. It invokes the
selected runtime directly and offers reusable setup or access in this environment
only. Honor the user's choice. Only reusable approval retains account access and
the repository grant in private Git metadata for later sessions. The CLI restores
approved setup itself. Never copy tokens or rewrite grant files. The initial
prepare command above remains usable with older launchers.

## Skill upgrade decisions

Only `update_available` for an older revision (or recognized unversioned legacy
wrapper) is a candidate. `current`, `newer`, and same-version `modified` are not
upgrade offers. Preserve modified files. Report incompatibility/inspection errors
separately. Generic "ask" actions do not override these checks.

For project skills, identify the target repository from the PR base or established
remote. Read its actual default branch and open PR heads. If every affected path
has the offered revision or later in that branch or one PR, suppress the question
and duplicate PR. Compare numeric version parts; titles/partial updates do not
count. Keep this checkout's files/runtime; do not merge, rebase, or copy files.

For personal skills, inspect the actual personal copies; repository updates do
not satisfy them.

For both scopes, honor saved scope/version deferrals and answered or declined
offers in this session. A new session/worktree alone creates no new offer.
On ambiguous scope or failed lookup, report it and defer without asking.

Only offer a verified uncovered upgrade once, then apply after acceptance while
preserving policy and local edits. Explicit upgrade requests supply acceptance;
still avoid duplicate work.

Resume an existing task with `doomer prepare --task HANDLE` after interruption.
Never create a replacement task to recover an existing review. If that task's
selected runtime is missing, run `doomer task repair HANDLE` through the available
launcher, then resume the same handle. Repair restores that exact release; do not
substitute the current stable release for an active task. Follow structured
user-action requests. Never invent consent, account identity, or hook activation.
Native skill discovery is optional.

Follow the selected CLI's matching instructions, subject to the prompt rules
above. Honor the user's choice to continue local edits despite blocked review.
Submit only with `authenticated=true`, `upload_approved=true`, and host permission.
Use task commands to retrieve results, record every finding response, and verify
completion. Pending results or installed software do not establish completed
review. Per-call mode runs these commands during each task; describe it accurately.
A missing hook receipt means unverified activation, not unsupported hooks.

For requested installation or onboarding, or when the CLI is missing for the
authorized coding task, fetch the official INSTALL.md at
https://raw.githubusercontent.com/doomerlabs/skills/86c6412d458f14d64e2882b6878e1418f8c75ff7/INSTALL.md and require its SHA-256 to equal
`68441df37d0d6761641ef18d327ae04a2a232dc1ca1ebb0530f606e77c2ca201`
before following the relevant verified steps with normal execution permissions.
Fetch raw Markdown through the shell if a reader summarizes it.
Verify the full checksum. Public HTTPS needs no GitHub login.
For an active review task, retain its handle and selected runtime. Use the guide's
onboarding steps with that task. If its executable is missing, use
`doomer task repair HANDLE`; runtime replacement is for setup without an active task.
If installation is blocked, use the local-edit choice above. In Cowork, install
into the editing VM's personal environment, preserving the repository bootstrap.
Perform the verified prerequisite installation under the host's normal execution
permissions, then run prepare to discover and reuse saved setup. Ask the user
only for an actual permission or decision required by that flow. Do not bundle
installation with speculative requests to sign in again or approve uploads.
Do not ask again for an installation already authorized. Normal host permission
controls still apply.
After installation, resume any existing task with `prepare --task HANDLE`, or
run the initial prepare command if no task exists. Present only the refreshed
result's approval request; earlier pending requests may have been satisfied.

When the user requests an onboarding reset, run `doomer onboard reset --dry-run`
to report discovered agent installations, Doomer profiles, and grant revocations, then run
`doomer onboard reset` when that cleanup is authorized. Reset covers discovered
installations and Doomer profiles, keeps login credentials, and revokes upload,
portable, and software-update grants. A persistent reset cutoff rejects old
portable copies. Report any incomplete/manual cleanup and the need to restart
running agents. Do not automatically onboard again or recreate grants after a
reset. Do not run a live reset merely to test an implementation.
Retain existing task handles and report incomplete review coverage for tasks
paused by the reset. Resume them only after the user explicitly grants access again.
