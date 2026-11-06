# Doomer skills

Agent skills for [Doomer](https://doomer.ai).

## Install

### Ask your coding agent

Paste this into Codex or Claude Code while working in your repository.

```text
Read https://raw.githubusercontent.com/doomerlabs/skills/main/INSTALL.md and
follow the instructions to set up Doomer in this repository.
```

[The installation guide](INSTALL.md) downloads the skill directly, without
`npx` or Node.js, and completes CLI setup, repository consent, and hook
activation. It creates or updates `AGENTS.md` with the required review workflow
and per-turn version checks, and connects that policy to `CLAUDE.md` for Claude
Code. It installs matching regular skill copies for both agents by default,
without asking which the team uses. Only the active agent's local hooks are
configured. Both choices keep the skill project-local. Local setup leaves the
changes uncommitted. Team setup opens a focused PR with shareable setup files;
each developer completes their own local activation.

### Use the skills installer

Run this from the repository you want Doomer to review:

```sh
npx skills add doomerlabs/skills --skill doomer-review
```

Select Codex or Claude Code when the installer asks. In your new or existing
Codex chat, send:

```text
Set up $doomer-review for this repo
```

In Claude Code, invoke `/doomer-review` and ask it to set up Doomer for this repo.
Complete repository consent and any required restart or hook-trust steps. Once
setup is ready, send your coding task in the next prompt; you do not need to
mention the skill on every task. Setup alone does not start a coding task.
If a newly installed skill is not available in Codex, restart Codex, reopen the
chat, and send the setup request again.

You can also invoke the skill with a coding task to set up Doomer and then
continue that task.

Codex discovers `.agents/skills/doomer-review/`; Claude Code discovers
`.claude/skills/doomer-review/`. Direct onboarding installs both as regular
copies from one source revision, without symlinks. An explicit single-agent
request is honored. The optional third-party installer retains its own agent
selection; a later approved project update maintains both standard locations.

## doomer-review

The skill supports Codex and Claude Code on macOS and Linux (Intel and ARM). It installs Doomer CLI **2026.11.5.9**, sets up the active agent's hooks, and delivers free initial code-review feedback in your coding conversation. No Doomer account is required.

The CLI owns onboarding and saved task context. Trusted hooks deliver assessments, including zero-finding results, and review links; the skill does not poll internal state or require Python helpers.

Repository snapshots and edited content, including documentation, configuration,
tests, and application code, plus task context and agent review responses, can
be sent to doomer.ai for review. Before uploading, Doomer opens a browser consent page for that repository. Installing the skill alone does not authorize uploads. Claude verifies live hook delivery and continues without a restart when hooks respond. Codex may need a restart; the skill provides the steps. Approve any trust prompt in the coding agent yourself. Declining leaves you free to continue coding without Doomer.

Reviews use `https://doomer.ai/api`. Local development builds and beta releases are not used. Existing installations are verified, and replacements require approval with a backup. The skill does not automatically request paid Deep reviews.

See [the skill instructions](skills/doomer-review/SKILL.md) for the full workflow.

## Update

Ask your coding agent to update Doomer. The skill checks the official Git
source once per session and offers available updates. Its direct update flow
works for agent-installed, npx-installed, and team-committed copies without
Node.js or `skills-lock.json`. Private source records detect local changes;
replacement requires approval and retains a backup. Project updates preflight
and update both standard agent copies together from the same source revision,
including adding a missing companion copy. Local modifications in either copy
are preserved until explicitly reconciled. Other repositories and global
installations are outside that paired update.

## License

[Apache 2.0](LICENSE).

The skill checks for its own updates once per coding session and asks before
updating itself and its matching managed CLI. It preserves the current pin when
you decline. Updater-equipped CLI releases verify ownership by path and checksum,
keep a backup, and never overwrite a Homebrew symlink target or silently downgrade
a newer managed installation. Older releases use the verified bootstrap flow.
