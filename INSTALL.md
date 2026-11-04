# Install Doomer with your coding agent

Open Codex or Claude Code in the repository you want reviewed, then send this
prompt.

```text
Read https://raw.githubusercontent.com/doomerlabs/skills/main/INSTALL.md and
follow it to install and set up Doomer for this repository. Ask whether I want
local setup only or a dedicated branch, commit, and pull request for my team.
```

The agent downloads the Doomer skill directly and uses it to install the CLI
and configure reviews. This installation path needs no `npx` or Node.js.
Supported systems are macOS and Linux on Intel/AMD 64-bit or ARM64.
Both options install the skill in this project. Local setup leaves the changes
uncommitted. Team setup publishes the shareable installation changes in a PR.
Each developer completes their own CLI setup, repository consent, and hook trust.

## Instructions for the coding agent

Follow this workflow when the user asks you to install or set up Doomer using
this guide. Treat the request as setup-only unless the user also gives you a
coding task.

### 1. Identify the repository and agent

Resolve the Git root of the user's target repository. If the current folder
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
answer before making changes. Reuse this choice after a restart or interrupted
setup. A team-PR choice authorizes creating the branch, committing the scoped
setup files, pushing that branch, and opening the PR.

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
against that worktree's Git root. Consent and watcher state may be
checkout-specific. Report which checkout has verified activation and any
remaining setup for the user's original checkout. A PR alone does not activate
reviews for other developers.

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

If Git is unavailable, download an archive of this same public repository over
HTTPS, resolve and record its commit ID, and extract the skill into a temporary
directory before copying. If you cannot fetch or identify the source, report
the failure and stop installation.

If the destination already exists, inspect it first. Reuse a complete existing
installation and continue its setup workflow. If it is incomplete, modified,
or needs replacement, explain the conflict and obtain approval before replacing
it. Preserve a backup for any approved replacement. Preserve unrelated skills,
agent settings, and repository changes.

### 4. Run the installed skill's setup workflow

Read `SKILL.md` and `references/install.md` from the installed destination and
follow their setup-only instructions in this conversation. You can read and
follow the files directly even if the agent's skill selector has not refreshed.
Use those files as the source of truth for the CLI version, verified release
download, existing-installation handling, onboarding commands, and activation.

The direct skill download above replaces the `npx skills add` step. The skill's
optional cached update check may be unavailable without Node.js. Follow its
documented fallback and continue with the installed skill's pinned CLI.

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
