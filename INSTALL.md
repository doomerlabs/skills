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
determine the active agent.

Use a repository-local installation for the active agent.

| Agent | Destination relative to the Git root |
| --- | --- |
| Codex | `.agents/skills/doomer-review/` |
| Claude Code | `.claude/skills/doomer-review/` |

Keep the skill project-local. Install for both agents only when requested.
The CLI and its private installation metadata use the locations defined by the
skill's installation reference.

### 2. Choose local setup or a team PR

Before changing files, ask once, unless the user already specified their choice.

> Would you like local setup only, or should I create a dedicated branch,
> commit the shareable Doomer setup, and open a pull request for your team?

Offer **Local setup only** first and **Create a team PR** second. Wait for the
answer before making changes. A team-PR choice authorizes creating the branch,
committing the scoped setup files, pushing that branch, and opening the PR.

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
| `agents` | Nonempty list of requested agents, drawn from `codex` and `claude` |
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

On restart, select the record matching the active `agent` and current
`setupRoot`, or a unique non-abandoned record matching `originalRoot` and
`agent`. Retain its UUID and original root. Reconcile its recorded operations
with the actual local and remote Git state before retrying. Never create a
second attempt when one can be resumed. A new attempt requires an explicit
user request and a new UUID, preserving earlier records. If multiple records
match, required fields are missing, values violate this schema, or recorded
resources belong to another repository or attempt, ask for clarification.
Null operation fields are valid only before those operations are confirmed.

Serialize record updates with an exclusive lock beside the file, re-read the
latest records while holding it, preserve all other UUID entries, and atomically
replace the JSON. Release the lock after the write. An existing lock means
another attempt may be active; wait or report it, without bypassing the lock or
overwriting its data. Store no secrets or consent in this record.

Treat the requested team PR as part of setup. After the skill reaches its
setup-only completion step, finish the authorized publication steps below
before ending the task.

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
`doomer-review` and `references/install.md`. Read both files. Copy the complete
skill directory, including its supporting files, into the destination above.
Keep temporary checkout files outside the user's repository, and remove only
the temporary files you created after installation.

If you cannot fetch or identify the source, report the failure and stop
installation.

If the destination already exists, compare its full file inventory and file
contents with the fetched skill, including `SKILL.md` and `references/install.md`.
Reuse it only when these match. A different CLI pin, missing file, extra file,
or changed content requires explaining the difference and obtaining approval
before replacing it. Preserve a backup for any approved replacement. Preserve unrelated skills,
agent settings, and repository changes.

### 4. Run the installed skill's setup workflow

Read `SKILL.md` and `references/install.md` from the installed destination and
follow their setup-only instructions in this conversation. You can read and
follow the files directly even if the agent's skill selector has not refreshed.
Use those files as the source of truth for the CLI version, verified release
download, existing-installation handling, onboarding commands, and activation.

The direct skill download above replaces the `npx skills add` step. The optional
cached npm update check may be unavailable without Node.js. Follow the section
**Check for updates once per coding session** in `SKILL.md`, which
handles a missing cached checker or incompatible Node by retaining the current
pin and recording the attempted check. This is separate from the CLI's local
managed-binary check and verified bootstrap in `references/install.md`, which
must still run as directed.

For an authorized team PR, this guide's publication steps explicitly override
the setup-only "Then stop" instruction in `SKILL.md`. After onboarding reaches
its completion message, continue to step 5. Preserve all consent, trust, and
activation requirements. A required user action still pauses onboarding;
retain the publication state and resume when the user completes that action.

Explain that repository snapshots and edited content, including documentation,
configuration, tests, and application code, plus task context and agent review
responses, can be sent to `doomer.ai`. Have the user complete repository consent
and any agent hook-trust prompts themselves. Reuse valid saved consent and
setup as directed by the skill. Keep required execution permissions separate
from repository consent. Respect an existing paused watcher.

Complete the skill's activation checks. If a restart or other user action is
required, give the exact next step and retain the setup state for resumption.
Report installation, configuration, and verified activation separately. Claim
end-to-end review delivery only after a hook actually delivers a result.

### 5. Publish the optional team PR

For the team-PR choice, review the complete diff against the selected base.
Include the installed skill and its supporting files, plus portable integration
instructions added to `AGENTS.md` or `CLAUDE.md` by the setup workflow. Include
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
Honor the repository's commit and PR conventions. Describe the installed agent,
skill source commit, validation performed, and any per-developer activation
steps. If activation is pending, state that explicitly. Follow through after
any required restart without repeating completed commits or opening a second
PR. Reuse an existing PR for this setup branch.

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

### 6. Report the result

Give the installed skill path, source commit ID, verified CLI version, and
activation status. Include any pending user action or concrete failure.
For local setup, list the uncommitted installation paths. For team setup,
include the branch, commit, PR link, and checkout configured. Distinguish
completed installation from pending activation or publication.
For a setup-only request, finish when setup is ready and invite the user's
next coding task.

## Skill locations

These repository-local destinations follow the agents' documented skill
discovery locations. See the [Codex skill documentation](https://learn.chatgpt.com/docs/build-skills)
and [Claude Code skill documentation](https://code.claude.com/docs/en/skills).
