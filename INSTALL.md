# Install Doomer with your coding agent

Open Codex or Claude Code in the repository you want reviewed, then send this
prompt.

```text
Read https://raw.githubusercontent.com/doomerlabs/skills/main/INSTALL.md and
follow the instructions to set up Doomer in this repository.
```

The agent downloads the Doomer skill directly and uses it to install the CLI
and configure reviews. This installation path needs no `npx` or Node.js.
Supported systems are macOS and Linux on Intel/AMD 64-bit or ARM64, with Git
available. Both options keep the skill repository-local. Local setup installs
in your current checkout and leaves the changes uncommitted. Team setup may
use a linked Git worktree to prepare the shareable installation changes in a PR.
Each developer completes their own CLI setup, repository consent, and hook trust.
CLI releases are installed side by side. Each checkout uses the release pinned
by its installed skill, so updating one repository leaves other pins intact.

## Instructions for the coding agent

Follow this workflow when the user asks you to install or set up Doomer using
this guide. Treat the request as setup-only unless the user also gives you a
coding task.

### 1. Identify the repository and agent

Check that Git is available, then resolve the Git root of the user's target
repository. If Git is missing, explain that it is required and stop setup.
If the current folder
contains several repositories and the target is unclear, ask which to use.
Determine whether you are running in Codex or Claude Code. Ask if you cannot
determine the active agent. For Codex, also identify whether this is the desktop
app or terminal. `CODEX_INTERNAL_ORIGINATOR_OVERRIDE=Codex Desktop` confirms
the desktop app. If that hint is absent, use the active client context or the
user's statement. Absence alone does not identify a terminal session. If the
client is still uncertain, ask whether the user is using Codex desktop or
Codex in a terminal before choosing client-specific steps.
Desktop setup uses **Review hooks** beside the composer or
**Settings > Hooks** and continues in the same chat. Follow the skill's desktop
activation flow even if an older CLI prints terminal restart instructions.
After a CLI replacement, still re-probe the verified executable's
`onboard --help` and follow the installation reference's capability checks.
Keep activation unverified until the active agent's live hook check succeeds
or a real current-session hook callback confirms the target repository.
For Codex, follow the skill's bounded `--check-hooks` verification; a successful
hook may return no chat message.
If approved desktop hooks remain silent after that check and its retry, use the
skill's **Recover silent desktop hooks** flow only when its prerequisites hold.
It offers one app reopen and verification in the same chat while reusing the
existing setup.

Install repository-local support for both Codex and Claude Code by default.
Do not ask which agents the team uses. Honor an explicit request to install
only one agent, but do not infer that restriction from the agent running setup.

| Agent | Destination relative to the Git root |
| --- | --- |
| Codex | `.agents/skills/doomer-review/` |
| Claude Code | `.claude/skills/doomer-review/` |

Keep two regular directory copies of the same staged skill, at the same source
revision; do not use symlinks. The skill contains both agents' workflows.
Installing both copies does not configure both local integrations: run CLI
onboarding, consent, and hook activation only for the active agent. Each teammate
activates their own agent locally.
The CLI and its private installation metadata use the locations defined by the
skill's installation reference.

### 2. Choose local setup or a team PR

Before changing files, ask once, unless the user already specified their choice.

> How would you like to set up Doomer?

Offer these choices in this order, including their descriptions.

- **Set up on this computer**

  Install and configure Doomer for you in this repository. Start using it now.

- **Create a setup PR for the team**

  Open a pull request adding Doomer setup instructions to the repository so
  teammates can use it too. Each teammate completes their own local setup.

Wait for the answer before making changes. A team-PR choice authorizes creating
the branch, committing the scoped setup files, pushing that branch, and opening the PR.
Creating a branch or worktree is only preparation for that choice. Its presence
does not establish that the user requested a PR. If an earlier attempt left
setup changes in a checkout without a confirmed publication choice, ask whether
to keep those changes local or publish them as a PR. Reuse the existing setup
work when possible. Honor an explicit local-only choice without asking again.

Before asking, read the local setup record if present. Use
`git rev-parse --git-common-dir` and resolve its output relative to the command's
working directory to an absolute path. This also works with Git before 2.31.
Store setup progress in `doomer/agent-install.json` under that directory.
Use a JSON object with `schemaVersion: 1` and a `setups` object keyed by a
fresh UUID per setup attempt. This is private Git metadata, outside tracked
files. Linked worktrees share it. Use linked worktrees for isolation, never a
separate clone that would lose access to this record.

Each record has the following fields.

| Field | Allowed value |
| --- | --- |
| `agent` | `codex` or `claude`, identifying the agent that started this attempt |
| `agents` | `["codex", "claude"]` by default; one agent only if explicitly requested |
| `mode` | `local` or `team-pr` |
| `originalRoot`, `setupRoot` | Absolute canonical Git root paths; `setupRoot` may be null until planned |
| `branch`, `base` | Valid Git branch/ref names, or null before planning; null for local mode |
| `remote` | Existing Git remote name, or null before planning; null for local mode |
| `sourceCommit`, `commit` | Full Git commit IDs, or null before the corresponding operation |
| `prUrl` | HTTPS URL returned by the selected host for the recorded repository and branch, or null before publication |
| `originalActivation` | `pending` or `verified`; only the original root's activation checks may set `verified` |
| `phase` | `chosen`, `prepared`, `installed`, `configured`, `committed`, `pushed`, `pr-open`, `complete`, or `abandoned` |

Record the selected mode immediately after the answer with phase `chosen`.
Record the planned branch and setup root before creating them. Advance to
`prepared` when the checkout is ready, `installed` when the skill is verified,
and `configured` when onboarding is configured. Team publication advances
through `committed`, `pushed`, and `pr-open` after verifying each operation.
Local setup moves from `configured` to `complete` after activation. Team setup
moves from `pr-open` to `complete` only after the PR is merged and original-root
activation is verified. Retain the last confirmed phase on failure. A cancelled
attempt becomes `abandoned` and is never automatically resumed.

A re-sent setup prompt or confirmation of the saved mode resumes the same
nonterminal attempt. An unambiguous request for a new attempt, a different
mode, or to start over is a new choice, whether volunteered by the user or
answered in their own words. For example, "start a new local setup" is sufficient.
A bare "yes" to an either/or question requires clarifying the mode. A generic
re-sent prompt or confirmation of an abandoned attempt's old mode is not a new
choice; ask whether the user wants a new local setup or a new team PR.

A new choice supersedes a conflicting nonterminal attempt. Mark only that
attempt `abandoned`, preserve its resources, and offer the cleanup below
before starting a new UUID. Keep resources the user chooses to retain.
Preserve all terminal records permanently with their original outcomes.
This explicit-choice rule takes precedence over automatic resumption.

On restart, inspect records for the active `agent` whose `setupRoot` or
`originalRoot` exactly equals the current canonical Git root. Repository
identity alone is not a root match. Use the first matching case below.
Before selecting a case, report any matching terminal records and offer cleanup
for abandoned resources. This reporting never establishes current readiness;
the selected case determines which activation checks govern the current setup.

1. **At least one nonterminal attempt matches.** Resume a unique match with
   its UUID and original root. If several match, ask which one to continue and
   whether to abandon the others. Persist approved abandonments by setting
   those records' existing `phase` to `abandoned` before resuming. When the user
   keeps several active attempts, have them select the intended worktree and
   resume using its exact `setupRoot` match. Readiness comes from the resumed
   attempt's own checks. Do not run terminal-record readiness checks at the same time.
   Re-run step 4's repository-instructions verification before completing any
   resumed attempt or advancing it from `configured` to `complete`.
   Repair missing or outdated guidance using that step's write rules. Retain
   the last confirmed phase until verification succeeds. If repair needs user
   direction or permission, report the pending action and stop that attempt.
2. **Only terminal records match.** Terminal records do not conflict with each
   other. Never resume abandoned records. For completed records, verify the installed
   skill and the repository instructions required by step 4, then run the
   skill's saved-setup and activation checks for the current root
   before describing that checkout as ready. These checks are part of this
   case, not a separate alternative. Never replay a completed record's commits,
   pushes, or PR creation. If setup is missing or no longer ready, offer a new
   repair attempt. If all matching records are abandoned, obtain a new explicit
   setup choice before creating another UUID. Preserve all terminal records.
3. **No records match.** Use the normal local-or-team setup question. A
   different or moved checkout is a new target, even if another checkout of the
   same repository has completed setup.

An explicit new choice may create a new UUID after terminal outcomes have been
reported. Reconcile any resumed record's operations with local and remote Git
state before retrying. Never create another attempt merely because a session
restarted. If required fields are missing, values violate this schema, or
recorded resources belong to another repository or attempt, ask for clarification.
Null operation fields are valid only before those operations are confirmed.

Serialize record updates with an OS-managed, flock-style advisory lock on
a separate stable lock file beside the JSON. Keep the locking descriptor open
in the same process through the entire read-modify-write operation. Never
replace the lock file; the JSON and its temporary replacement are separate
files. Hold the lock while re-reading the latest records,
preserving other UUID entries, and atomically replacing the JSON. The operating
system must release the lock when its holder exits or crashes. The lock file's
existence alone never means it is held. If another live process holds the lock,
wait briefly or report the contention; never bypass a held lock. Store no
secrets or consent in this record.

Treat the requested team PR as part of setup. Once the shareable setup files
have been installed and verified, finish the authorized publication steps below
before ending the task. Hook approval and live activation may remain pending
while those files are published. Record and report publication and activation
separately.

For local setup, use the current checkout and leave the installation changes
uncommitted. Report the changed paths when finished.

For team setup, inspect the working tree, current branch, remote, and PR base
before editing. Create a fresh, uniquely named branch such as
`chore/setup-doomer` from the intended PR base. Use the repository's default
branch unless the user or repository instructions specify another base. Keep
the PR limited to Doomer setup. If the current checkout has unrelated changes
or commits, use a separate worktree from that base and preserve the original
checkout. Tell the user which checkout will be configured. Resolve an ambiguous
remote or base with the user before publishing.

In a separate worktree, run the remaining installation and onboarding steps
against that worktree's Git root. Treat activation as specific to the exact
root passed to onboarding. Never infer that activation there enables the
original checkout. Record the original checkout as pending until it has its
own installed skill and the skill's saved-setup and activation checks succeed
for that exact root. Its onboarding must obtain any consent the CLI requires;
never copy consent records between checkouts. Report that the user must merge
and update their original checkout, then resume this guide there to complete
that activation. A PR alone does not activate reviews for other developers.

### 3. Download and install the skill

Fetch the public repository `https://github.com/doomerlabs/skills.git` into a
new temporary directory using Git over HTTPS. Use its default branch and
record the resolved commit ID. The source directory is
`skills/doomer-review/` inside that checkout.

Before copying, verify that the source includes `SKILL.md` with the skill name
`doomer-review`, `references/install.md`, and `references/updates.md`. Read
these files. Read and inspect the official source's
`scripts/stage-managed-skill.py`, then run it with the verified source checkout,
its exact full commit ID, a new private staging-directory path, and
`--both-agents` for the default installation. This helper is the only
source-checkout executable permitted by this installation flow. It stages
identical regular skill copies under `.agents/skills/doomer-review/` and
`.claude/skills/doomer-review/`, marking Markdown with its source revision and
path. Validate both complete staging inventories, then copy them to the
corresponding destinations in the target checkout. For an explicitly requested
single-agent installation, omit `--both-agents` and copy its flat staging tree
only to that agent's destination. Preserve the markers, including their
position after SKILL.md's YAML frontmatter.
Validate all relative paths and reject symlinks or special files in the source.
After verifying both full installed inventories and byte-for-byte equality,
record each directory's source revision and file hashes using
`references/updates.md`. For an explicit single-agent install, verify and record
only that directory. Compare installation bytes to the
rendered staging tree, not the unmarked upstream tree. Keep the baseline record in private
installation metadata, outside the repository's tracked files. Do not create
or modify `skills-lock.json`; the direct update flow uses Git and this baseline.
Keep temporary checkout files outside the user's repository, and remove only
the temporary files you created after installation.

If you cannot fetch or identify the source, report the failure and stop
installation.

Preflight all selected destinations before changing any: both for the default
installation, or only the requested path for an explicit single-agent install. If a destination already
exists, compare its full file inventory and file contents with the rendered
staging tree, including `SKILL.md`, `references/install.md`,
and `references/updates.md`. Reuse requires an exact match of the entire
inventory and every file, not just those three named files. A copy missing
`references/updates.md` requires an approved replacement before reuse or
baseline creation. A different CLI pin, missing file, extra file,
or changed content requires explaining the difference and obtaining approval
before replacing it. A symlink is a conflict, even if it points at the other
agent's copy; never follow it for writes. Preserve a backup for any approved
replacement. If a selected destination conflicts, do not partially install or update the
selected set. An out-of-scope companion does not block an explicit single-agent
installation and must remain untouched. Preserve unrelated skills, agent settings, and repository changes.

### 4. Run the installed skill's setup workflow

Read `SKILL.md`, `references/install.md`, and `references/updates.md` from the
active agent's installed destination and follow their setup-only instructions
in this conversation. You can read and
follow the files directly even if the agent's skill selector has not refreshed.
Use those files as the source of truth for the CLI version, verified release
download, existing-installation handling, onboarding commands, and activation.
For both setup modes, complete the repository-instructions step below before
the skill's setup-only completion message ends the task.

The direct skill download above completes the skill installation. Its own
`references/updates.md` defines update checks using Git, with no npm dependency.
The private source record is local to this installation. A teammate cloning
committed skill files establishes their own baseline through that flow.
The CLI's managed-binary check and verified bootstrap in `references/install.md`
still run as directed.

For an authorized team PR, this guide's publication steps explicitly override
the setup-only "Then stop" instruction in `SKILL.md`. After installing and
verifying the shareable files, continue to step 5 even if onboarding awaits
hook approval, a follow-up message, or a restart. Preserve all consent, trust,
and activation requirements for enabling reviews. Publishing the authorized
setup changes does not establish activation. A pending activation step alone
must not leave an authorized PR uncreated.

Explain that repository snapshots and edited content, including documentation,
configuration, tests, and application code, plus task context and agent review
responses, can be sent to `doomer.ai`. Have the user complete repository consent
and any agent hook-trust prompts themselves. Reuse valid saved consent and
setup as directed by the skill. Keep required execution permissions separate
from repository consent. Respect an existing paused watcher.

#### Install the repository instructions

After the onboarding step returns, whether or not it wrote repository
instructions, ensure the Git root contains `AGENTS.md` with the block below.
Verify it again when resuming setup. This is required for both local and team
setup before the final ready report or a requested restart.

Use the skill's existing, repository/session-scoped skip decisions
(`compatibilityDecision: skip` or `onboardingAuthorization: skip_session`) and
record a new skip in the skill's durable task summary as it directs. A current
explicit skip ends this setup attempt with phase `abandoned`; report that setup
was skipped and retain its resources. It is not a permanent repository opt-out.
The skill's durable summary is conversation state, separate from a coding-task
handoff file. The abandoned phase in the existing private setup record also
prevents automatic resumption after a restart. Read that persisted phase before
any step 3 download or step 4 probe: an abandoned attempt reports its outcome
and waits for an explicit new setup choice under the terminal-record rules.
This gate applies even when no conversation summary survives the restart.
When the user explicitly resumes setup, follow the skill's
resumption rules and require the block before reporting setup ready. Maintain
one shared skip decision with the skill.

Before writing either instructions file, inspect its file type and any policy
markers. Recognize only exact standalone policy-marker lines outside fenced
code examples and larger HTML-comment blocks. The one-line marker comments
themselves are valid delimiters. Markers shown in examples are not live policy.
Scan in source order while tracking the current Markdown block context.
Inside a fenced code block, ignore comment tokens until its matching fence
closes (same delimiter character, at least the opening length). Inside an HTML
comment, ignore fence tokens until the next `-->`; comments do not nest.
Only outside both contexts recognize a new fence or comment opener, and treat
standalone policy-marker comments as the live delimiters. Treat unclosed fences
or comments, or uncertain marker context,
as conflicts requiring user direction before any write.
A symlink, another non-regular file, or duplicated, incomplete, or
out-of-order markers requires reporting the conflict and obtaining the user's
direction before changing that file. This check gates all writes below.

If the user authorizes malformed-marker repair, preserve a uniquely named
backup under `doomer/instruction-backups/` in the resolved private Git common
directory. This keeps backups outside the worktree and the team PR. Remove
only the malformed marker lines and obsolete Doomer
content whose boundaries the user has confirmed, preserving all other text.
Then insert one complete block and verify it under the rules below. If those
boundaries remain unclear, request clarification and leave the file intact.

Create `AGENTS.md` if it is missing. Append the block with blank lines around
it only when the existing file contains neither policy marker. If exactly one
start marker and one end marker form a complete ordered block, update only
that block. Preserve all surrounding text and file permissions. Keep the
CLI-owned `doomer-review` block intact; onboarding may regenerate it. These
separate markers keep the per-turn policy from being overwritten on later
onboarding runs. Preserve unmarked repository-specific instructions.
Generate the block for the agents actually installed in this attempt. In the
example below, replace `INSTALLED_AGENT_SKILL_PATHS` with only their verified
paths. For the default installation, use these two lines:
`Codex uses .agents/skills/doomer-review/` and
`Claude Code uses .claude/skills/doomer-review/`. A newly created single-agent list is only for an explicitly restricted
installation with no existing companion entry to preserve.
Do not name a Claude path unless that copy exists, or require a noninstalled
agent to run this policy. On later setup, recheck every existing entry on disk
for its skill and referenced files before preserving it. Drop entries whose
copy or required files are missing, and add all newly installed agents. Preserve
every healthy existing entry even when this attempt installs only one agent;
limiting installation scope does not authorize removing the companion policy. If any
active agent, including a listed agent, encounters this block without its own
installed copy, continue its normal task and explain
how to opt into setup if requested; this block does not authorize installing it.
Use `templates/review-policy.md` at the same verified source commit as the
skill. Render only `INSTALLED_AGENT_SKILL_PATHS` as specified above. Add this
metadata comment immediately after `<!-- doomer-review-policy:start -->`,
then the rendered template and `<!-- doomer-managed:end -->` before the
existing policy end marker. Metadata fields use plain values on separate lines:
`package: doomerlabs/skills`, `revision: FULL_SOURCE_COMMIT`,
`source: templates/review-policy.md`, `kind: block`, and
`agents: codex`, `agents: claude`, or `agents: codex,claude`.
The comment opens with `<!-- doomer-managed` and closes with `-->`.
Keep exactly the template's bytes outside the substituted agent list.
Do not add whole-file exclusions to AGENTS.md or CLAUDE.md.

```markdown
<!-- doomer-review-policy:start -->
## Required Doomer review workflow

INSTALLED_AGENT_SKILL_PATHS

For an active agent listed above, if its skill or required reference files are missing,
continue the normal task and report the missing installation. Do not infer
permission to reinstall it. Otherwise, before each user turn that will edit
repository files, read its installed doomer-review skill and
references/install.md from disk. Follow the skill for documentation, configuration,
tests, and application code, including small edits and requests that do not
explicitly mention review.

Run the skill's local CLI version and managed-installation check once per
editing turn before making changes. Use the current on-disk pin and the skill's
saved approval decisions. A version remembered from an earlier turn or a
previously completed setup does not satisfy this check. Keep the online skill
update check scoped to once per coding session as the skill directs.

Follow the skill's setup and review workflow. Reuse valid repository consent
and verified hook activation. Keep repository upload consent and agent hook
trust as user choices, preserve a paused watcher, and honor explicit skip
decisions and the skill's read-only and skill-maintenance exemptions.

Use trusted hooks to capture changes and deliver review results. Investigate
feedback, fix confirmed issues within the user's scope, and record responses
as the hooks direct. Follow the skill's completion gate for the current
revision and include the complete Doomer review link when a review is delivered,
including a review with no findings.
<!-- doomer-review-policy:end -->
```

When the Claude skill copy is installed (including every default installation),
also ensure the root `CLAUDE.md` loads this shared policy with
an `@AGENTS.md` import on its own line, outside code fences. Create `CLAUDE.md`
with that import if missing. For an existing file, count only a standalone line
whose trimmed text is exactly `@AGENTS.md`, outside fenced code blocks and HTML
comments, as the canonical import. If no such line exists, add it as a new
top-level line. A mention in prose, a comment, or an import inside another file
does not satisfy this check. Preserve its existing text and the CLI-owned Doomer block. When both
agents are installed, keep one shared policy block in `AGENTS.md`.

Preserve the existing permissions of both `AGENTS.md` and `CLAUDE.md`, and
write their changes atomically. If any existing rule
explicitly conflicts with the requested Doomer policy, surface the conflict
instead of silently deleting that rule.

Read the resulting files back. Verify exactly one complete policy block,
unchanged surrounding text, the installed skill paths for every requested
agent, and Claude's import when applicable. Include the instructions files in
the local-change summary or scoped team PR. A setup record marked complete
still requires this guidance check when resuming this guide; repair missing or
outdated guidance using these same rules without repeating completed publication.

Complete the skill's activation checks. If a restart or other user action is
required, give the exact next step and retain the setup state for resumption.
For an authorized team PR, continue to publication while reporting that pending
activation step. If publication itself needs missing information or is blocked,
identify that specific blocker.
Report installation, configuration, and verified activation separately. Claim
end-to-end review delivery only after a hook actually delivers a result.

### 5. Publish the optional team PR

For the team-PR choice, review the complete diff against the selected base.
Include the installed skill and its supporting files, plus portable integration
instructions added to `AGENTS.md` and `CLAUDE.md` by the default setup workflow.
For an explicit single-agent setup, include only its required instructions. Include
other generated configuration only after verifying that it is portable and
appropriate to share. Inspect any hook configuration for absolute paths,
usernames, and machine-specific values before including it.

Keep credentials, tokens, consent records, session IDs, logs, private CLI
metadata, downloaded binaries, temporary files, and machine-specific hook
settings out of the commit. Retain needed local settings outside the commit.
If local values and portable instructions share a file, separate them using
the agent's supported local configuration mechanism. If that is unavailable,
leave that file out and describe the per-developer setup step in the PR.

Stage only the reviewed setup paths or hunks. Check the staged diff, create one
focused commit, push the new branch, and open a PR against the selected base.
Honor the repository's commit and PR conventions. Use the agent-neutral title
"Set up Doomer reviews" unless repository conventions require another title.
Describe both installed agents (or the explicit single-agent restriction),
skill source commit, validation performed, and any per-developer activation
steps. If activation is pending, state that explicitly. Follow through after
any required restart without repeating completed commits or opening a second
PR. Reuse an existing PR for this setup branch.
An isolated checkout or a local commit does not finish a requested PR. Verify
the published PR URL and include it in the result.

If there is no shareable diff, report that outcome instead of creating an empty
commit or PR. If pushing or creating the PR is blocked, preserve the local
branch and commit, identify the failed step, and provide the next action.

#### Resume or abandon publication

Use the saved branch, base, remote, setup root, commit, and PR URL to resume.
Check remote state before retrying a push or PR creation so a completed request
with a lost response does not produce duplicate work. Update `phase` after each
confirmed operation. If the original checkout now contains the merged setup,
complete activation there instead of creating another branch or PR.

If the user cancels publication, preserve completed work and report its exact
locations. Ask before closing a PR, deleting a local or remote branch, removing
a worktree, or unstaging setup hunks. After explicit cleanup approval, operate
only on the recorded setup resources and verified setup hunks. Preserve any
new user edits and leave a worktree intact if it contains them. Mark the record
as abandoned after cleanup, retaining any resources the user chose to keep.

Publication cleanup is limited to those PR, branch, worktree, and staging
operations. Retain installed skills and CLI binaries. Before offering cleanup,
and again before performing it, compare the proposed resources with all active
setup records and live worktrees.
Preserve anything shared with, or needed by, another attempt or the user's
ongoing work. Offer cleanup only for verified attempt-owned, unshared resources.
If the second check finds newly shared, needed, or unowned resources, retain
them and remove them from the cleanup scope. Report these exclusions. If
nothing remains, report that cleanup was skipped. Otherwise obtain approval
for the remaining cleanup subset before performing it. This approval covers
only a subset of the original cleanup operations, subject to all limits above.

### 6. Report the result

Give both installed skill paths (or the explicitly selected single path), source
commit ID, verified CLI version, and
activation status for the active agent. Do not claim that installing a teammate's
skill copy also activated that teammate's hooks. Include any pending user action
or concrete failure.
For local setup, list the uncommitted installation paths. For team setup,
include the branch, commit, PR link, and checkout configured. Distinguish
completed installation from pending activation or publication.
For a setup-only request, finish when setup is ready and invite the user's
next coding task.

## Skill locations

These repository-local destinations follow the agents' documented skill
discovery locations. See the [Codex skill documentation](https://learn.chatgpt.com/docs/build-skills)
and [Claude Code skill documentation](https://code.claude.com/docs/en/skills).
