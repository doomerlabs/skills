---
name: doomer-review
description: Required Doomer review workflow for repository edits in Codex or Claude Code. Use before changing repository files, including documentation, README text, configuration, tests, and application code—even for small edits, renames, or requests that do not mention review. Also use for Doomer setup. Complete missing onboarding before edits; hooks deliver reviews and links. Exclude read-only discussion and edits solely to this skill.
---

# Doomer review

Use Doomer's hooks to review repository changes. The hooks capture the
task and changes, request hypotheses, deliver the free Look Closer assessment,
and record the agent's responses. Use profile `default` and
`https://doomer.ai/api`. No account is required. Do not start a paid Deep review.
Requests solely discussing or editing this skill and its supporting files are
exempt from this review workflow, including setup and update checks. Explicit
requests to install or update Doomer still use the corresponding flow below.

## Setup-only requests

Treat `set up $doomer-review` (or an equivalent request to enable Doomer) as
setup-only when the user has not also supplied a coding task. This is an
onboarding request, not a discussion-only request. Use the same installation,
repository consent, watcher, and hook activation flow below, but do not invent
a coding task or start editing application code.

For setup-only onboarding, use the setup-only command for the active agent
below. Do not create a task file or save the setup request as a coding-task
handoff. Add `--restart` only for a Codex terminal session when required.

Keep configuration and activation separate in the conversation summary:
repository, active agent/session when known, consent outcome, required restart,
and pending or verified hook activation. Successful installation alone is not
readiness. For Claude, only a `ready` result for the current repository/session
confirms live activation. For Codex, complete any required restart and user hook
trust before describing setup as ready; do not claim end-to-end review delivery
until a hook actually delivers a result.

When ready, say: **“Doomer is set up for this repo. Send your coding task whenever
you’re ready.”** Otherwise report the actual pending step or unverified state.
Then stop. Do not invent a coding task. This also overrides installation
reference instructions to “continue the coding task” when no task was supplied.
A refusal or failure ends setup-only onboarding with an accurate outcome.

A repeated setup-only request must report remaining activation steps, not
reinstall or repeat consent. The no-status-check shortcut below applies only to
confirmed activation, not configured-but-unverified state. Use the bounded
Claude check/recovery below when its activation is pending; for Codex, handle
any outstanding restart/trust step. Preserve this state across compaction.

## Required before repository edits

Except for the skill-maintenance exemption above, a "coding task" includes any
requested repository edit, including documentation-only changes. Renaming a docs
heading, updating a README, changing configuration, and editing tests all use
this workflow. A request need not
mention Doomer or code review. This includes requested edits to tracked dotfiles,
lockfiles, and generated files. Do not treat docs-only or trivial edits as exempt.

Complete missing Doomer onboarding before the first repository content edit.
Read-only inspection may continue while preparing setup. The absence of an
AGENTS.md or CLAUDE.md instruction does not make this loaded skill optional;
onboarding creates the integration instructions. Task size, expected review
value, installation effort, and a required restart are not reasons to skip
onboarding. Only the user may choose to continue without Doomer; respect any
such choice immediately.
An update refusal is not automatically a refusal of Doomer. If the retained
CLI cannot support this skill, explain the concrete incompatibility and ask
whether to continue without reviews. Reuse an existing explicit skip decision;
do not repeat the update offer or invent a compatibility requirement. Retain
this outcome as `compatibilityDecision: pending | use_doomer | skip` in the
same durable task summary. No answer leaves it `pending`: keep the binary,
do not re-probe or re-ask automatically. End the current turn with the question
instead of polling, sleeping, or keeping a tool running. Repository edits wait
for the explicit choice; the agent is not left executing an indefinite loop.
Silence is neither permission to skip nor permission to change the installation.
An explicit user choice resumes the corresponding flow.

Every explicit session-wide skip sets `compatibilityDecision: skip` in the
shared durable task summary before work resumes. All installation, update,
onboarding, and activation paths consult it before probing or prompting. Reuse
it across turns, restarts, and compaction until the user explicitly resumes
Doomer. An execution rejection alone is a blocked setup, not a user skip.

Request installation permissions and repository upload consent through the
normal approval flow. Explain before consent that repository snapshots and
edited content, including documentation, README text, configuration, tests,
and application code, plus task context and agent review responses, can be
uploaded to doomer.ai. A prior approval explicitly limited to application code
does not authorize the broader scope. Obtain the user's explicit approval of
that scope before edits or capture in that case, retaining the decision in the
durable summary. Reuse valid repository-wide consent reported by the CLI.
Never approve permissions yourself. If setup needs user action,
present that step instead of silently opting out. If a concrete technical error
prevents setup, report it accurately and follow the failure guidance below.
The same user-choice rule covers manifest validation, download, and bootstrap/
updater failures, not only version incompatibility. For a coding task, offer
only the bounded recovery allowed by the installation reference or an explicit
skip; end the turn if the choice is pending. For setup-only requests, report
the failed/pending setup and stop without inventing coding work.

### When onboarding needs authorization

First apply the saved-setup check under **Set up once**. Missing conversation
history is not evidence that setup or consent is missing. Do not request setup
authorization merely because this is a new chat or context.

Keep installation, onboarding authorization, repository upload consent, and
hook activation distinct. A verified installed CLI is not completed onboarding.
After installation succeeds, proceed to the onboarding command below; do not
stop at explaining installation commands or propose skipping merely because
onboarding needs permission.

Use the agent's normal execution-approval mechanism for the actual onboarding
command when required. Describe its real effects: it configures review hooks,
obtains repository consent, and may start the watcher and send repository code
and task context to Doomer when consent is recorded. Include documentation,
configuration, and the other repository content described above in this
explanation. Do not describe onboarding
as only opening a browser or assume installation authorized uploads.

If automatic approval review rejects onboarding for missing authorization,
do not retry unchanged or work around the rejection. Ask the user explicitly:
**“May I finish Doomer setup for this repository? It configures review hooks and
enables sending repository content, including documentation and configuration,
task context, and agent review responses to
doomer.ai after repository consent. Or would you prefer to skip Doomer for this
session?”** Offer **“Allow Doomer setup”** and **“Skip Doomer this session”** when
structured choices are available. Briefly identify the automatic approval
rejection and its stated reason. Do not offer only to continue without review.

Retain `onboardingAuthorization: pending | allowed | blocked | skip_session`
for this repository in the durable task summary shared with the installation
reference. Record `pending` before asking and wait for the answer. Reuse a
recorded `allowed` decision across turns and restarts without re-asking. If the
user skips, record `skip_session` and `compatibilityDecision: skip` before
resuming work. Missing history never supplies approval.

If authorized, record `allowed` and resume the documented onboarding command
through the normal approval mechanism without reinstalling the verified CLI.
The human must still make any repository-consent or hook-trust choice; never
click, record, or fabricate it on their behalf. Reuse valid recorded consent
through the CLI rather than demanding it again. If the user declines, continue
the original task without Doomer using the recorded skip. If approval is
rejected again, record `blocked` with the reason, report it, and stop setup.
Retain the blocked state across turns without automatic retries or re-prompts.
Resume only when the user explicitly requests recovery or the stated blocker
changes; do not loop or bypass it.

## Check the local pin each turn

At the start of each user turn that uses this skill, reread `SKILL.md` and
`references/install.md` from the active skill's canonical on-disk directory.
Do this before reusing a prior setup decision. The files may have been updated
outside this chat. Use their current CLI pin, not a version remembered from an
earlier turn. Skip this check for read-only discussion or edits solely to this
skill, and honor an explicit session-wide choice to skip Doomer.

Run the installation reference's local managed check once in that turn. A
matching managed binary needs no update prompt. A changed pin follows the
version-specific decision below. A completed setup or update from an earlier
turn does not bypass this check. This local check does not trigger an online
skill check or repeat repository consent or hook trust.

## Check online for skill updates once per coding session

Keep `updateCheckAttempted` for the online skill check separate from the local
check above. Share `updateDecision` (`not_asked`, `approved`, `declined`, or
`finished`) with the installation reference, keyed by the active canonical
skill path and target CLI version. Keep each target's decision in the durable
conversation summary, together with the last observed pin and CLI version.
Returning to a previously declined or completed target reuses its decision.
Outside an in-flight approved attempt, a newly observed target version begins
at `not_asked`; approval for an earlier version does not authorize a later one.
An explicit session-wide skip still wins over a new target.

Also share `adoptionDecision: not_asked | approved | declined | finished` with
[installation](references/install.md), keyed by canonical skill path,
destination path, and target CLI version. Keep it in the durable summary
across turns, restarts, and compaction. It is separate from `updateDecision`;
its `finished` means the approved launcher migration succeeded. Consult it before
replacement offers, retain declines, and keep approvals until that replacement
completes. A session-wide skip suppresses both decision flows, including pending
work; retain its record for an explicit user resumption.

Resolve the skill directory's real path before keying either decision. For a
replacement destination, resolve the parent directory and retain the final
filename so approval replaces the link itself rather than its target. Persist
these resolved paths and reuse them after restart. If relocation makes the
record's identity uncertain, report the conflict without re-offering or
transferring approval automatically.

Adoption approval covers exactly its recorded target version. A pending
adoption resumes only with that same pin. If the pin changed, retain the
original record and report the conflict before replacement; do not carry its
approval to a different version. A successful adoption therefore records
`finished` against the same version that was approved.

The combined offer below covers this active skill and its matching managed CLI
in either order. If an approved skill update reveals a different pin, carry
that approval only into completing that same update attempt, then record
`finished` against its resulting version. It never authorizes adoption of an
unmanaged binary or updating independent skill copies. Keep `approved` until
the whole requested attempt completes.

Before starting an approved update, retain `updateAttempt` in the durable
summary with the canonical skill path, original target, resulting pin when
known, and completed/pending halves. Persist the resulting pin immediately
after rereading the updated skill. On later turns or after compaction, consult
this record before version-scoped decisions and resume the pending half with
the same approval. A permission interruption leaves the attempt pending. If
local files changed to an unrelated pin, stop and report the conflict rather
than extending that approval. Clear the record on completion or explicit
abandonment, recording the outcome for the original and resulting targets.
A failed or abandoned attempt must not trigger an automatic fresh offer.

Mark the online check attempted before starting it, at most once per session,
even if a later turn discovers a changed local pin. If an earlier decision
cannot be recovered after compaction, still perform the local check, but do not
repeat an update offer without an explicit user update request. Do not add a
state file or scan other chats. A separate coding session has its own decisions.

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
offer. Continue with the current pin and verify its exact version-specific
installation. A missing release follows the installation reference.
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
If this checkout's selected release is missing, install that exact pin through
the installation reference. A different release elsewhere is independent. Fresh install
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

After success, use file-read tools to reread the newly installed `SKILL.md` and
`references/install.md` from this skill's canonical on-disk directory.
Use only the newly read pin and instructions afterward, not remembered text.
Continue the approved update using this newly read pin; do not ask again.
Unknown, manually replaced, or Homebrew-linked binaries require the explicit
adoption choice in the installation reference. Record `finished` after the
whole requested attempt; update permission never grants upload consent.

Release binaries are shared only among checkouts using the same pin. Updating
this skill does not authorize rewriting other repositories' or agents'
independent skill copies. Shared aliases of the same canonical skill update
together. Other checkouts retain their own pins and versioned runtimes.

## Set up once

Resolve the Git root of the repository being edited, not the org directory that
contains the chat. After the per-turn local pin check, if this conversation
already verified its saved setup and no update replaced the CLI, continue
without repeated setup/status checks.

### Reuse saved setup across chats

After verifying the installed CLI through the installation reference, check
saved setup once for this repository in a new chat or when setup history is
unknown. Run this standalone, read-only command before any normal `onboard`
command or onboarding-authorization question. Installation/update permissions
and the read-only `self-update --check` probe precede this check when needed to
obtain a verified compatible executable. A declined update does not prevent
checking saved setup with a compatible retained CLI.

In the command templates below, set `doomer_cli` to the verified, pinned
executable at `~/.local/share/doomer/versions/VERSION/doomer` and `doomer_repo_root` to the Git root resolved from the actual
checkout being edited. Assign both in the executing shell before using them;
never run a template with either value empty or unresolved.

```sh
"${doomer_cli:?Set the verified CLI path}" --profile default --api-url https://doomer.ai/api watch status --json "${doomer_repo_root:?Set the target Git root}"
```

This inspects saved consent, installed hooks, and watcher status. It does not
install hooks, start a watcher, or upload repository content. Do not combine it
with onboarding, updates, or other writes in the same command.

- If `approved` is true, `paused` is false, `running` is true, and
  `hooks_installed` is true for the active agent, and `repository_status` is
  `Watching`, reuse that configuration. Continue through the activation gate
  below before treating reviews as ready. For this complete configuration,
  do not rerun installation/onboarding, save a restart task, reopen browser
  consent, or ask to enable Doomer again, except for the bounded Claude
  activation recovery below. For setup-only requests, report the saved
  configuration and its actual activation state.
- `hook_trust: "user_managed"` is a statement of who controls trust, not a
  report that trust is missing. Do not demand `/hooks`, a restart, or another
  confirmation solely because this value is present. Let the coding agent
  enforce its trust controls. Do not claim live review delivery until observed.
- If `paused` is true, respect the pause and continue without Doomer; do not
  resume it unless the user explicitly asks. Never rewrite consent to resume.
- If consent or the active agent's hooks are missing, use normal onboarding
  below. If consent and hooks exist but the watcher is stopped or this checkout
  is not `Watching`, repair only that missing setup through onboarding,
  retaining saved consent. Explain the specific missing part if execution
  authorization is required; do not ask for repository upload consent again
  when the CLI reports it valid. A new linked worktree is not proof of missing
  consent: check its own resolved path first.
- If the check fails, report the actual error. An unreadable result is not a
  negative consent decision or proof that hooks need reinstalling. Do not
  blindly invoke onboarding as a diagnostic fallback.

Saved configuration does not establish live activation. Retain activation as
`pending`, `unverified`, or `verified` for the current repository and active
agent/session in the durable summary. A current-session hook callback or
Claude's current-session `ready` check can establish verification. Status flags
alone cannot. A summary for another session does not establish current-session
activation, and missing history leaves it `unverified`.

For pending or unverified Claude activation, use **Complete pending Claude
activation** below. For Codex, a current-session Doomer hook callback confirms
loaded hooks. Without that evidence, report configured but unverified, have the
user inspect Doomer's hook approval controls for the active client, and retain
the activation gate before repository edits. In Codex desktop, use **Review hooks**
beside the composer or **Settings > Hooks**. In the terminal, use `/hooks`. Follow an actual outstanding restart requirement
or the user's confirmation that hooks are unloaded; missing history alone does
not prove a restart is necessary. If verification remains unavailable, use the
shared user-choice rule to continue without verified reviews only by explicit
choice. Do not reinstall or rewrite saved task state to diagnose activation.

These rules reuse configuration while preserving the activation gate. A
non-`Watching` checkout uses the repair branch even when the other flags are
true. A pending restart, failed activation, or configured-but-unverified state
always follows the activation path; saved status never overrides it.

Install or verify the checkout-pinned CLI following [installation](references/install.md), including its managed ownership and runtime-protocol checks.
Use stable CLI **2026.11.3.7**, which provides the consolidated onboarding command.
Probe `doomer onboard --help` before using the new workflow. If unavailable,
report that the installed release needs updating; do not invent the command,
recreate removed helpers, or claim setup succeeded.

Use the verified executable's absolute path. For a coding task, preserve the
original user request and relevant corrections verbatim in a private temporary file, excluding
unrelated conversation. Do not search other chats. Choose the active coding
agent, not another agent merely installed on the machine. Run one onboarding
command for that agent.

**Codex:** use its current `CODEX_THREAD_ID`. Distinguish the desktop app from
the terminal using the active client context. `CODEX_INTERNAL_ORIGINATOR_OVERRIDE`
set to `Codex Desktop` identifies a desktop session. If it is absent, use the
active client context or the user's statement. Absence alone does not identify
a terminal session. If still uncertain, ask whether the user is using Codex
desktop or Codex in a terminal before selecting the onboarding flow. Desktop
onboarding stays in the current chat and uses the hook approval controls below.
For setup-only:

```sh
# In Codex terminal only, append --restart if the CLI was installed or replaced this turn.
"${doomer_cli:?Set the verified CLI path}" --profile default --api-url https://doomer.ai/api onboard --repo "${doomer_repo_root:?Set the target Git root}" --agent codex --session "$CODEX_THREAD_ID"
```

With a coding task:

```sh
# In Codex terminal only, append --restart if the CLI was installed or replaced this turn.
"${doomer_cli:?Set the verified CLI path}" --profile default --api-url https://doomer.ai/api onboard --repo "${doomer_repo_root:?Set the target Git root}" --agent codex --session "$CODEX_THREAD_ID" --task-stdin < "$task_request_file"
```

**Claude Code:** the current skill session is `${CLAUDE_SESSION_ID}`. This is
Claude's skill substitution, not a shell environment variable. Use its expanded
value as the session argument. For setup-only:

```sh
"${doomer_cli:?Set the verified CLI path}" --profile default --api-url https://doomer.ai/api onboard --repo "${doomer_repo_root:?Set the target Git root}" --agent claude --session '${CLAUDE_SESSION_ID}'
```

With a coding task:

```sh
"${doomer_cli:?Set the verified CLI path}" --profile default --api-url https://doomer.ai/api onboard --repo "${doomer_repo_root:?Set the target Git root}" --agent claude --session '${CLAUDE_SESSION_ID}' --task-stdin < "$task_request_file"
```

If the substitution is still literal or empty, treat the session ID as unknown;
do not pass the literal placeholder or borrow a Codex session ID.

After installing a new selected release, discard old capability results and run
`onboard --help` on its verified absolute executable. If the checkout's pin
changed, use normal onboarding for that checkout to start or reuse its selected
runtime with existing consent. Preserve the original task and follow the
active agent's hook activation flow. The stable hook dispatcher is shared, so
a new release pin alone does not require reinstalling or trusting a changed
hook definition. Verify actual hook delivery before claiming activation.

Do not refresh or stop the old version's watcher merely because this checkout
changed pins. Other checkouts may still require it. An unchanged pin with
verified active hooks reuses its runtime.

For normal Codex terminal onboarding, add `--restart` if the CLI was installed
or replaced during this turn, because the prompt may have arrived before its
hooks could run. In Codex desktop, omit `--restart` and follow the desktop
activation flow below, including when an older CLI prints terminal restart
instructions.
An already-configured matching runtime does not require rerunning normal
onboarding or rewriting the saved task. Claude uses the
live-hook check below instead of an automatic restart. Remove the temporary
input file after successful onboarding. If the session ID is unavailable, do
not guess it: omit `--session` and `--task-stdin` (including its redirection),
and retain a coding task in this conversation if one exists. For Claude, no
session means no live check: skip `--check-hooks`, report configured but
unverified, and retain session resolution as a pending step. Never print the
ready message or invent a session argument. Resolve it on the next invocation;
if still unavailable, report the limitation and let the user choose whether to
continue without verified reviews.

Onboarding owns repository consent, matching hooks, the background watcher,
the marked Doomer instructions in `AGENTS.md` for Codex or `CLAUDE.md` for Claude
Code, and saved task context. It reuses valid
consent and an existing watcher. The one-time read-only saved-setup check above
is allowed. **Do not separately run `watch add`, `watch task`, `watch start`, a
status polling loop, or scripts that read Doomer's state.**
Do not directly write Doomer's grant, hook definitions, or saved task files.

Let the CLI's browser page obtain the user's upload decision. Never use `--yes`,
accept consent for them, or write coding-agent trust records. Do not infer consent from
the skill installation. Respect a refusal or pause; continue coding without
Doomer and do not repeatedly ask in the same session. A failed setup is not a
successful review; explain the concrete error briefly.

## Codex desktop: approve hooks in the current chat

After onboarding, direct the user to **Review hooks** beside the composer. If
that button is absent, use **Settings > Hooks** to inspect and approve Doomer's
hooks. Then ask for a follow-up message in this chat and check for an actual
current-session hook callback. Preserve the original task in the conversation;
missing its initial prompt capture alone does not require a restart.

The approval controls belong to Codex. Do not claim that Doomer opened the
approval dialog, invoke a terminal resume command, or write hook trust settings
on the user's behalf. If approval or live delivery remains unverified, report
that specific pending step and retain the activation gate. Use a restart only
when the user confirms the hook definitions have not loaded and chooses that
fallback. For that desktop fallback, have the user quit and reopen the Codex
desktop app, reopen this same chat, and send the setup request again. Reuse the
saved setup and original task, then finish the pending hook approval and live
activation checks. Desktop recovery stays in the desktop app.

## Claude: verify live hooks before asking for a restart

Claude can reload hooks during a running session. With a valid current session,
after Claude onboarding returns, run its printed `onboard --agent claude --session … --check-hooks`
command. This checks real hook callbacks and task capture in this session; it
neither installs hooks again nor starts another review.

- `ready`: finish setup-only onboarding, or continue the original coding task
  immediately. Do not ask the user to restart or accept a separate hook-trust prompt.
- `waiting_for_hooks`: retry the same check once after the tool result. The
  check's own tool events can finish activation. Do not poll beyond that retry.
- For setup-only onboarding, `waiting_for_hooks` after the retry does not identify
  a cause. It may reflect no captured prompt, unloaded hooks, pending trust, or
  policy restrictions. Report configuration with live activation unverified;
  ask the user to inspect `/hooks` and any workspace trust prompt. Do not infer
  either working hooks or missing trust, fabricate a task, or require restart
  solely from this status. Retain activation as pending for the next prompt.
- Still unconfirmed during coding, or `setup_unavailable`: report that live
  delivery could not be verified. Ask the user to inspect `/hooks` and any workspace trust prompt
  or managed-policy restriction. A restart is only a fallback if the hook
  definitions have not loaded; do not claim missing evidence proves missing
  trust. The user may choose to continue without Doomer.

If the user confirms the definitions have not loaded and chooses to restart,
show the Claude resume command below. Otherwise do not interrupt their session
with restart instructions. Keep the original task in context. Never write or
accept trust settings on their behalf.

### Complete pending Claude activation

On a repeated setup-only request or the first coding prompt after unverified
setup, do not take the setup-once shortcut. Resolve the current session and run
the same `--check-hooks` command once, with one retry for `waiting_for_hooks`.
Use only statuses actually returned; this CLI does not return a diagnostic
reason for `waiting_for_hooks`.

If still unconfirmed on that first coding prompt, run normal onboarding once
with this real coding request as `--task-stdin` and the current session, then
use the bounded check above. This renews the short-lived activation receipt
and binds the actual task, reusing existing consent and configuration. Do not
save the old setup request or loop through onboarding. If activation remains
unconfirmed, surface the `/hooks`/trust/policy checks and let the user decide
whether to proceed without verified reviews. Do not silently start coding.
For a setup-only repeat, stop with the unverified outcome rather than inventing
a task to renew activation. A missing session follows the limitation above.

## A required restart

For a Codex terminal restart or a Claude terminal reload fallback,
stop before editing repository content, including documentation.
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
setup-only intent, handle any pending hook trust, then report the activation state and wait
for a coding prompt. Do not treat “Resume after doomer.ai setup” as a coding task
or ask the user to repeat an original task that was never supplied.

For onboarding with a coding task, the trusted UserPromptSubmit hook supplies
the saved original task once after restart. Resume that task and its constraints.
For either mode, **do not repeat onboarding merely because of restart or run a
breadcrumb-consumption command.** The bounded pending-Claude-activation recovery
above is the exception when a later real coding prompt needs a fresh receipt.
If hook trust is still pending, ask the
user to review Doomer hooks in `/hooks` for Codex terminal or Claude Code,
or **Review hooks / Settings > Hooks** for Codex desktop. Have the user complete
any workspace trust prompt themselves. Never select trust for them.
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

Complete pending activation as described above. Otherwise, only troubleshoot
when requested or when the hook reports a concrete error.
Use the CLI's `watch status --json` for operational diagnosis, not as a normal
per-edit or final-answer step. Never replace hook delivery with manual reviews.
