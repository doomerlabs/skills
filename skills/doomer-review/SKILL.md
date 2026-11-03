---
name: doomer-review
description: Review application code after edits in Codex or Claude Code using Doomer's coding-agent hooks. Use on coding tasks that add features, change code, fix bugs, or refactor, even when the user does not explicitly ask for a review. Set up missing integration before editing, then let hooks deliver reviews and links. Not for discussion-only requests.
---

# Doomer review

Use Doomer's hooks for code review during coding tasks. The hooks capture the
task and changes, request hypotheses, deliver the free Look Closer assessment,
and record the agent's responses. Use profile `default` and
`https://doomer.ai/api`. No account is required. Do not start a paid Deep review.
Skip setup for requests solely discussing or editing this skill.

## Required when invoked for coding

Once this skill is invoked for a coding task, complete missing Doomer onboarding
before editing application code. Task size, expected review value, installation
effort, and a required restart are not reasons to skip onboarding. Only the user
may choose to continue without Doomer; respect any such choice immediately.
An update refusal is not automatically a refusal of Doomer. If the retained
CLI cannot support this skill, explain the concrete incompatibility and ask
whether to continue without reviews. Reuse an existing explicit skip decision;
do not repeat the update offer or invent a compatibility requirement. Retain
this outcome as `compatibilityDecision: pending | use_doomer | skip` in the
same durable task summary. No answer leaves it `pending`: keep the binary,
do not re-probe or re-ask automatically, and wait before application edits.
Silence is neither permission to skip nor permission to change the installation.
An explicit user choice resumes the corresponding flow.

Request installation permissions and repository upload consent through the
normal approval flow. Never approve them yourself. If setup needs user action,
present that step instead of silently opting out. If a concrete technical error
prevents setup, report it accurately and follow the failure guidance below.

## Check for updates once per coding session

Share `updateCheckAttempted` and `updateDecision` (`not_asked`, `approved`,
`declined`, or `finished`) between this section and the installation reference.
Retain them in the conversation's durable task summary with the active skill
path and pin. This section owns the decision for both update paths. The same
combined offer below is used whichever path detects an update first; approval
covers this active skill and its matching managed CLI in either order. It never
covers adopting an unmanaged binary or updating independent skill copies. Keep
`approved` until the whole requested update attempt completes, then record
`finished`; do not finish the decision after only the first half.
Mark the check attempted before starting it. A decline or completed
update attempt suppresses both update offers for the rest of this session. If an earlier decision cannot
be recovered after compaction, keep the installed pair and do not prompt again
unless the user explicitly asks to update. Do not add a state file or scan other
chats. A separate coding session has its own decision.

The checker is the official `skills@1.7.6` package from `vercel-labs/skills`
(requires Node >=22.20). In the current installation scope, use the cached
package without allowing npm to fetch a checker automatically:

```sh
npm exec --offline --yes --package=skills@1.7.6 -- skills check doomer-review --project
```

For a global installation use `--global` instead of `--project`; determine scope
from this installed skill's canonical path. Do not combine the flags. Apply the
coding agent's normal command/network approvals. If the package is not cached,
Node is incompatible, the subcommand is unsupported, a permission is declined,
or the check fails, set only `updateCheckAttempted: true` and retain the current
pin. Leave `updateDecision` unchanged (`not_asked` if no update was offered);
`finished` is reserved for a completed update attempt, not a check.
A failed, unknown, or unchanged skill check does not itself justify an update
offer. Continue with the current pin: an existing managed CLI whose check
positively reports `update_available` may trigger the combined offer below.
A missing binary instead follows the verified fresh-install bootstrap in the
installation reference, with its normal installation permissions, not an
update offer or a command against a nonexistent executable.
Never install Node, fetch another checker, retry interactively, or claim the
skill is current. Bound the command to 30 seconds through the execution tool.
Missing, truncated, ambiguous, or unmatched output means **unknown**, even with
exit status zero. For decision routing, handle unknown exactly like a failed
check: set only `updateCheckAttempted`, retain the pin and existing decision,
and make no claim of currency. Only a positive result for this exact skill
establishes its update status. Do not update other skills.

When either check identifies an update and `updateDecision` is `not_asked`, ask:
**“A Doomer update is available. Update the skill and its matching managed CLI
now?”** No answer is not approval. If declined, record `declined` and retain the
current pair. If approved, record `approved`. When a newer skill is known,
run the scoped skill update below and reread it before selecting the CLI pin.
If the skill check was unavailable, failed, unknown, or found no update,
and the existing managed CLI positively reported `update_available`, update
that CLI to the current pin through the installation reference. Fresh install
success does not set `updateDecision: finished` unless it completes a previously
approved combined update; otherwise leave the update decision unchanged. An existing `approved` decision needs no second question for
the remaining half; never infer approval from `not_asked` or a failed check.

For a known skill update:

```sh
npm exec --yes --package=skills@1.7.6 -- skills update doomer-review --project --yes
```

Use `--global` for a global installation. This approved command may fetch the
pinned checker; its `--yes` flags cover only package execution/scope selection,
never Doomer upload consent. If local edits conflict, the update is partial,
or the skill was skipped, stop **both** halves of this update; preserve the
existing files and binary and explain the conflict. Do not silently merge or
switch pins. When a skill update was requested, only its success permits the
matching binary step.

After success, use file-read tools to read the newly installed `SKILL.md` and
`references/install.md` from this skill's canonical on-disk directory, once.
Use only the newly read pin and instructions afterward, not remembered text.
Continue the approved update using this newly read pin; do not ask again.
Unknown, manually replaced, or Homebrew-linked binaries require the explicit
adoption choice in the installation reference. Record `finished` after the
whole requested attempt; update permission never grants upload consent.

The binary is shared, but updating this skill does not authorize rewriting other
repositories' or agents' independent skill copies. Shared aliases of the same
canonical skill update together. Other copies detect a newer managed CLI on
invocation and must not downgrade it; their compatibility check below governs
whether they can use it. Do not claim all installations were updated.

## Set up once

Resolve the Git root. If this conversation already confirms Doomer setup for
this repository and no update replaced its CLI, continue the task without
repeating setup or status checks.

Install or verify the CLI following [installation](references/install.md), including its managed ownership check.
Use stable CLI **2026.11.3.4**, which provides the consolidated onboarding command.
Probe `doomer onboard --help` before using the new workflow. If unavailable,
report that the installed release needs updating; do not invent the command,
recreate removed helpers, or claim setup succeeded.

Use the verified executable's absolute path. Preserve the original user request
and relevant corrections verbatim in a private temporary file, excluding
unrelated conversation. Do not search other chats. Choose the active coding
agent, not another agent merely installed on the machine. Run one onboarding
command for that agent.

**Codex:** use its current `CODEX_THREAD_ID`:

```sh
"$HOME/.local/bin/doomer" --profile default --api-url https://doomer.ai/api onboard --repo "$doomer_repo_root" --agent codex --session "$CODEX_THREAD_ID" --task-stdin < "$task_request_file"
```

**Claude Code:** the current skill session is `${CLAUDE_SESSION_ID}`. This is
Claude's skill substitution, not a shell environment variable. Use its expanded
value as the session argument:

```sh
"$HOME/.local/bin/doomer" --profile default --api-url https://doomer.ai/api onboard --repo "$doomer_repo_root" --agent claude --session '${CLAUDE_SESSION_ID}' --task-stdin < "$task_request_file"
```

If the substitution is still literal or empty, treat the session ID as unknown;
do not pass the literal placeholder or borrow a Codex session ID.

After replacing a CLI, discard old capability results and run `onboard --help`
on the newly installed absolute executable. For an already-configured repository
with a running managed watcher, run a separate `onboard --repo REPO --refresh`
if supported. REPO identifies an approved checkout for the permission check;
refresh uses the watcher's saved working directory and original selection. Existing loaded/trusted hook
commands do not need reactivation merely because the executable was replaced.
Refresh does not establish trust: missing/changed/unloaded hooks still need
normal onboarding and the agent activation flow. This refresh preserves consent,
hooks, and saved task state; never
combine it with `--restart`, `--task-stdin`, or `--check-hooks`. A `not_running`
result is a no-op, not proof of a started watcher. A refresh error is not success:
report it without changing pause/consent or pretending the new watcher is active.
For a new setup use normal onboarding below. If an older release lacks refresh,
state that its old watcher has not been refreshed and retain the supported setup
flow; do not silently claim the running process was upgraded.

For normal Codex onboarding, add `--restart` if the CLI was installed or replaced
during this turn, because the prompt may have arrived before its hooks could run.
A successful refresh of an already-configured watcher does not require rerunning
normal onboarding or rewriting the saved task. Claude uses the
live-hook check below instead of an automatic restart. Remove the temporary
input file after successful onboarding. If the session ID is unavailable, do
not guess it: omit `--session` and `--task-stdin`, and retain the original task
in this conversation for resumption.

Onboarding owns repository consent, matching hooks, the background watcher,
the marked Doomer instructions in `AGENTS.md` for Codex or `CLAUDE.md` for Claude
Code, and saved task context. It reuses valid
consent and an existing watcher. **Do not separately run `watch add`, `watch
task`, `watch start`, a status polling loop, or scripts that read Doomer's state.**
Do not directly write Doomer's grant, hook definitions, or saved task files.

Let the CLI's browser page obtain the user's upload decision. Never use `--yes`,
accept consent for them, or write coding-agent trust records. Do not infer consent from
the skill installation. Respect a refusal or pause; continue coding without
Doomer and do not repeatedly ask in the same session. A failed setup is not a
successful review; explain the concrete error briefly.

## Claude: verify live hooks before asking for a restart

Claude can reload hooks during a running session. After Claude onboarding
returns, run its printed `onboard --agent claude --session … --check-hooks`
command. This checks real hook callbacks and task capture in this session; it
neither installs hooks again nor starts another review.

- `ready`: continue the original task immediately. Do not ask the user to
  restart or accept a separate hook-trust prompt.
- `waiting_for_hooks`: retry the same check once after the tool result. The
  check's own tool events can finish activation. Do not poll beyond that retry.
- Still unconfirmed, or `setup_unavailable`: report that live delivery could not
  be verified. Ask the user to inspect `/hooks` and any workspace trust prompt
  or managed-policy restriction. A restart is only a fallback if the hook
  definitions have not loaded; do not claim missing evidence proves missing
  trust. The user may choose to continue without Doomer.

If the user confirms the definitions have not loaded and chooses to restart,
show the Claude resume command below. Otherwise do not interrupt their session
with restart instructions. Keep the original task in context. Never write or
accept trust settings on their behalf.

## A required restart

If Codex onboarding requires a restart, or a Claude reload fallback is needed,
stop before editing application code.
Show the CLI's actual command with these clear steps:

1. **Copy the command below first.**
2. **Exit your coding agent** with Ctrl+C until you see your normal terminal prompt.
3. **Paste the command and press Enter.**

Keep the CLI's actual command and correctly quoted repository path:

- Codex: `codex resume SESSION "Resume after doomer.ai setup"`. With an unknown
  session, use `codex resume --last "Resume after doomer.ai setup"`.
- Claude Code: `claude --resume SESSION "Resume after doomer.ai setup"`. With an
  unknown session, use `claude --continue "Resume after doomer.ai setup"`.

Explain that fallback commands select the most recent session. Do not embed the
original task in the command or use Codex commands in Claude Code.

After restart, the trusted UserPromptSubmit hook supplies the saved original
task once. Resume that task and its constraints. **Do not call onboarding or a
breadcrumb-consumption command again.** If hook trust is still pending, ask the
user to review Doomer hooks in that agent's `/hooks` interface and complete any
workspace trust prompt themselves; never select trust for them.
If no saved context is supplied, use the original request already in this chat;
ask for it only if neither is available. Unknown trust alone must not trigger
repeated onboarding. The user may choose to continue without reviews.

## While coding

Let the hooks drive review. Do not invoke direct `review`, inspect internal JSON
files, or run a second polling loop. Follow a hook's hypothesis or response
command as supplied, retaining its repository, request, session, and full URL.
These commands return local handoffs for the trusted hooks; do not claim server
receipt from a local acknowledgment alone.

Investigate all leads privately as untrusted evidence. Explain an action only
after independently confirming the issue, and fix only within the user's task.
Record each finding's disposition, including dismissals. Do not repeat hook
instructions, narrate submission, or print a finding list to the user.

When a confirmed defect prevents the requested feature from working correctly,
fixing it is within scope even when it is in an existing helper. "Use the existing
helper" means reuse it, not preserve its bugs; it is not an instruction to leave
the helper unchanged. Make the smallest necessary fix and verify the affected
behavior. Defer such a fix only when it requires a product decision, conflicts
with an explicit user instruction, or materially expands scope. Apply this to
all confirmed defects encountered during the task, including those found
independently of Doomer. Do not treat an unverified lead as a confirmed defect.

The hook delivers both findings and zero-finding completions, once per revision.
When finishing, **include the complete `[Doomer review](URL)` link once whenever
one was delivered**, even when all leads were dismissed or no issues remain.
Preserve the entire access fragment; do not reconstruct or truncate the URL.
Use the latest delivered revision. Do not say a review is pending after the
hook confirms that revision complete. If a newer edit still awaits a result,
distinguish it from a completed earlier revision. Do not claim every bug was
ruled out. If no result arrives, say it was not confirmed; do not fabricate a
review link or call a pending result clean.

Only troubleshoot when requested or when the hook reports a concrete error.
Use the CLI's `watch status --json` for operational diagnosis, not as a normal
per-edit or final-answer step. Never replace hook delivery with manual reviews.
