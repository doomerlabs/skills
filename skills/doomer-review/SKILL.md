---
name: doomer-review
description: Use Doomer's coding-agent hooks to review code changes, investigate leads, and report a review link. Set up missing CLI integration once, preserving human upload consent and hook trust.
---

# Doomer review

Use Doomer's hooks for code review during coding tasks. The hooks capture the
task and changes, request hypotheses, deliver the free Look Closer assessment,
and record the agent's responses. Use profile `default` and
`https://doomer.ai/api`. No account is required. Do not start a paid Deep review.
Skip setup for requests solely discussing or editing this skill.

## Set up once

Resolve the Git root. If this conversation already confirms Doomer setup for
this repository, continue the task without repeating setup or status checks.

Install or verify the CLI following [installation](references/install.md).
Use stable CLI **2026.11.3.2**, which provides the consolidated onboarding command.
Probe `doomer onboard --help` before using the new workflow. If unavailable,
report that the installed release needs updating; do not invent the command,
recreate removed helpers, or claim setup succeeded.

Use the verified executable's absolute path. Preserve the original user request
and relevant corrections verbatim in a private temporary file, excluding
unrelated conversation. Do not search other chats. Run one onboarding command:

```sh
"$HOME/.local/bin/doomer" --profile default --api-url https://doomer.ai/api onboard --repo "$doomer_repo_root" --agent codex --session "$CODEX_THREAD_ID" --task-stdin < "$task_request_file"
```

Add `--restart` if the CLI was installed or replaced during this turn, because
the prompt may have arrived before its hooks could run. Remove the temporary
input file after successful onboarding. If the session ID is unavailable, do
not guess it: omit `--session` and `--task-stdin`, and retain the original task
in this conversation for resumption.

Onboarding owns repository consent, matching hooks, the background watcher,
AGENTS.md's marked Doomer instructions, and saved task context. It reuses valid
consent and an existing watcher. **Do not separately run `watch add`, `watch
task`, `watch start`, a status polling loop, or scripts that read Doomer's state.**
Do not directly write Doomer's grant, hook definitions, or saved task files.

Let the CLI's browser page obtain the user's upload decision. Never use `--yes`,
accept consent for them, or write Codex trust records. Do not infer consent from
the skill installation. Respect a refusal or pause; continue coding without
Doomer and do not repeatedly ask in the same session. A failed setup is not a
successful review; explain the concrete error briefly.

## A required restart

If onboarding says a restart is needed, stop before editing application code.
Show the CLI's actual command with these clear steps:

1. **Copy the command below first.**
2. **Exit Codex** with Ctrl+C until you see your normal terminal prompt.
3. **Paste the command and press Enter.**

The command should use `codex resume` with the known session ID and the short
prompt `"Resume after doomer.ai setup"`. Use `--last` only when the ID is unknown,
and explain that it selects the latest session. Keep the CLI's correctly quoted
repository path. Do not embed the original task in the command.

After restart, the trusted UserPromptSubmit hook supplies the saved original
task once. Resume that task and its constraints. **Do not call onboarding or a
breadcrumb-consumption command again.** If hook trust is still pending, ask the
user to review the named Doomer hooks in `/hooks`; never select trust for them.
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
