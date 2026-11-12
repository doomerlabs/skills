---
name: doomer
description: >-
  Review code changes with Doomer Quick Look. Use for coding tasks and requested
  code reviews. Complete setup with npx @doomerlabs/doomer onboard to install
  the global CLI and automatic review hooks for Claude Code or Codex.
metadata:
  author: doomerlabs
  version: "0.1.0"
---

# Doomer

Doomer Quick Look reviews source changes. The Node CLI is published as
`@doomerlabs/doomer` and installs the global `doomer` executable. This skill is
distinct from legacy `doomer-review`; it does not use `prepare`, `task`, or
the `install.md` workflow.

## Setup

Installing this skill through skills.sh does not install the persistent CLI or
agent hooks. When setup is requested, run:

```sh
npx @doomerlabs/doomer onboard
```

This installs `~/.local/bin/doomer` and configures the chosen agents. For
noninteractive setup, use `--agent claude`, `--agent codex`, or
`--agent claude,codex` only for agents the user selected. Use `--no-hooks` for
standalone reviews. Do not commit skill copies or discovery files to a project.

Use `doomer doctor --json` to check an existing installation without changing
it. Follow its next action if setup is incomplete. Hook configuration does not
prove activation: the user must review/trust hooks through native controls and
may need to restart the agent. Never modify trust records.
`doomer install-hooks --agent AGENT` repairs hooks when requested.

For a fresh installation, the recommended command is
`npx @doomerlabs/doomer install`. Onboarding reuses this directly installed skill.

## Coding tasks and reviews

Enabled, trusted hooks capture a local baseline when the prompt is submitted
and directly invoke Quick review before the agent finishes a changed working
tree. This does not depend on the agent choosing to use the skill. Read the
findings, address applicable issues, and allow another review after fixes.
Explain findings you decline.

Without active hooks, record `git rev-parse HEAD` before editing, then review
with that exact starting commit:

```sh
doomer review --base STARTING_COMMIT --json
```

Without a persistent command, use
`npx @doomerlabs/doomer review --base STARTING_COMMIT --json`.
For an explicit review of existing changes, `doomer review --json` selects the
local default-branch baseline. Use `--repo /absolute/path` when needed; review
each repository for cross-repository edits. Manual reviews may include changes
that predate this task; do not represent them as exclusively your edits.

## Permission and results

Review uploads baseline and current source snapshots and the diff. The skill
and hook installation do not grant upload permission. Reuse a valid saved
repository/service/agent approval; otherwise ask the user. Never supply
`--approve-upload` or `--approve-uploads` on your own authority. Never bypass
host denials or upload by an alternate route after a refusal.

Quick readiness is `ready: true` or `early_assessment.status: ready`, independent
of aggregate `status`. Deep is disabled on this path. Read `leads` and review
again after fixes. No leads means no Quick findings were returned, not that
the source is proven bug-free. Resume pending results with:

```sh
doomer review get REVIEW_ID --json
```

Do not claim completion after a timeout, denial, network failure, or missing
hooks. Report the blocker and continue authorized local work unless the user
explicitly required waiting. `doomer update` updates the CLI and skill and
repairs configured hooks when requested.
