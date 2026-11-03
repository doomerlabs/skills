---
name: doomer-review
description: Review application code after edits in Codex or Claude Code using Doomer's coding-agent hooks. Use when asked to set up Doomer, or on coding tasks that add features, change code, fix bugs, or refactor, even when the user does not explicitly ask for a review. Set up missing integration before editing, then let hooks deliver reviews and links. Not for discussion-only requests.
---

# Doomer review

Use Doomer's hooks for code review during coding tasks. The hooks capture the
task and changes, request hypotheses, deliver the free Look Closer assessment,
and record the agent's responses. Use profile `default` and
`https://doomer.ai/api`. No account is required. Do not start a paid Deep review.
Skip setup for requests solely discussing or editing this skill.

## Setup-only requests

Treat `set up $doomer-review` (or an equivalent request to enable Doomer) as
setup-only when the user has not also supplied a coding task. This is an
onboarding request, not a discussion-only request. Use the same installation,
repository consent, watcher, and hook activation flow below, but do not invent
a coding task or start editing application code.

For setup-only onboarding, retain the active session argument but omit
`--task-stdin` and its input redirection from the commands below. Do not create
a task file or save the setup request as a coding-task handoff. Still add
`--restart` for Codex when required and complete the applicable activation steps.

After setup, report whether it is ready or still needs restart, hook trust, or
live verification. When ready, say: **“Doomer is set up for this repo. Send your
coding task whenever you’re ready.”** Then stop. A repeated setup-only request
for this already-configured repository needs no new onboarding; report any
remaining activation step instead. On the next
coding prompt, use the configured hooks without repeating setup unless a
concrete error requires repair. Preserve this setup-only intent and the known
setup/activation state in the conversation summary across restart or compaction.
If setup is declined or fails, report that outcome without claiming readiness.

## Required during setup and coding

Once this skill is invoked for a coding task, complete missing Doomer onboarding
before editing application code. Task size, expected review value, installation
effort, and a required restart are not reasons to skip onboarding. Only the user
may choose to continue without Doomer; respect any such choice immediately.

Request installation permissions and repository upload consent through the
normal approval flow. Never approve them yourself. If setup needs user action,
present that step instead of silently opting out. If a concrete technical error
prevents setup, report it accurately and follow the failure guidance below.

## Set up once

Resolve the Git root. If this conversation already confirms Doomer setup for
this repository, continue the task without repeating setup or status checks.

Install or verify the CLI following [installation](references/install.md).
Use stable CLI **2026.11.3.4**, which provides the consolidated onboarding command.
Probe `doomer onboard --help` before using the new workflow. If unavailable,
report that the installed release needs updating; do not invent the command,
recreate removed helpers, or claim setup succeeded.

Use the verified executable's absolute path. For a coding task, preserve the
original user request and relevant corrections verbatim in a private temporary file, excluding
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

For Codex, add `--restart` if the CLI was installed or replaced during this turn,
because the prompt may have arrived before its hooks could run. Claude uses the
live-hook check below instead of an automatic restart. Remove the temporary
input file after successful onboarding. If the session ID is unavailable, do
not guess it: omit `--session` and `--task-stdin`, and retain the original task
in this conversation for resumption, if there is one.

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

- `ready`: finish setup-only onboarding, or continue the original coding task
  immediately. Do not ask the user to restart or accept a separate hook-trust prompt.
- `waiting_for_hooks`: retry the same check once after the tool result. The
  check's own tool events can finish activation. Do not poll beyond that retry.
- For setup-only onboarding, `waiting_for_hooks` after the one retry can mean
  there is no captured task yet. Report that Doomer is configured but live
  delivery is unverified until the next coding prompt. Do not fabricate a task,
  claim readiness, or require a restart solely for this result. Let that prompt
  supply the task to the hooks; investigate a concrete hook failure normally.
- Still unconfirmed during coding, or `setup_unavailable`: report that live
  delivery could not be verified. Ask the user to inspect `/hooks` and any workspace trust prompt
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

After a setup-only restart there is no saved coding task to replay. Retain the
setup-only intent, handle any pending hook trust, then finish onboarding and wait
for a coding prompt. Do not treat “Resume after doomer.ai setup” as a coding task
or ask the user to repeat an original task that was never supplied.

For onboarding with a coding task, the trusted UserPromptSubmit hook supplies
the saved original task once after restart. Resume that task and its constraints.
For either mode, **do not call onboarding or a breadcrumb-consumption command
again.** If hook trust is still pending, ask the
user to review Doomer hooks in that agent's `/hooks` interface and complete any
workspace trust prompt themselves; never select trust for them.
For a coding task, if no saved context is supplied, use the original request
already in this chat; ask for it only if neither is available. Unknown trust alone must not trigger
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
