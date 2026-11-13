---
name: doomer
description: >-
  Review code changes with Doomer Quick Look. Use for coding tasks and requested
  code reviews. Use the Node manager to install the Go CLI and automatic
  review hooks for Claude Code or Codex when setup is requested.
metadata:
  author: doomerlabs
  version: "0.1.0"
---

# Doomer

Doomer Quick Look reviews source changes. The Node manager package
`@doomerlabs/doomer` installs and configures the native Go `doomer` executable.
Node handles setup; Go performs reviews and watches. This skill governs only
this workflow. The separate managed `doomer-review` skill governs its own
installation; this skill does not use `prepare`, `task`, or `install.md`.

The Node package is not published yet. For authorized source testing, use the
user-provided checkout of `https://github.com/doomerlabs/doomer-node` or a
tarball built from that reviewed source, and only with the user's authorization.
Do not substitute a third-party checkout, URL, or package. Registry commands below apply once
the package is published. If npm reports it unavailable, report the blocker;
do not substitute another package or change a live installation.

## Setup

Installing this skill through skills.sh does not install the persistent CLI or
agent hooks. For fresh setup, run `npx @doomerlabs/doomer install`.
When this skill is already installed, complete the same setup with:

```sh
npx @doomerlabs/doomer onboard
```

This installs `~/.local/bin/doomer` and configures the chosen agents. For
noninteractive setup, use `--agent claude`, `--agent codex`, or
`--agent claude,codex` only for agents the user selected. Use `--no-hooks` for
standalone reviews. This global Node-managed workflow does not require
committing skill copies or discovery files to a project. Do not apply this
rule to a separate managed team installation governed by `doomer-review`.

Use `npx @doomerlabs/doomer doctor --json` to check an existing installation without changing
it. Run this check after setup too and follow its `next` action if incomplete.
If `doomer` is not on PATH, use the exact absolute `executable` path returned by
the manager, or have the user add its directory to PATH. Do not rerun installation
merely to repair PATH. Doctor's `ready` describes installed configuration, not
native trust or proof that hooks have run.

The user must review/trust hooks through native controls. For Codex, setup's
`codexReload.reloaded` and `codexReload.restartRequired` report live reload;
`npx @doomerlabs/doomer refresh-hooks --json` returns top-level `reloaded` and
`restartRequired`. Identify which command produced the JSON before reading it:
for setup read `codexReload.restartRequired`; for refresh-hooks read
`restartRequired`. A missing field is unknown, not false. When that field is
true, start a new Codex session. For Claude
Code, start a new session after trusting newly installed hooks if the running
session has not loaded them. Verify that a permitted coding change actually
starts a review before claiming automatic reviews are active. A reload response
alone is insufficient; if no review starts, check trust and start a fresh session.
Never modify trust records.
`npx @doomerlabs/doomer install-hooks --agent AGENT` repairs hooks when requested.

Both `install` and `onboard` install the CLI and configure the selected agents.
`onboard` reuses this skill when already present; `install` refreshes it through
the official skills CLI.

## Coding tasks and reviews

Before using an existing `doomer` command, check the Node manager's
`doctor --json` result. Require both `ready: true` and
`capabilities.watchAgentHook: true`; a legacy executable with the same name is
not proof of readiness. If either is false or missing, report the installation
blocker and obtain setup authorization before repairing or replacing it.
Do not use the legacy binary merely because `ready` is true.

Enabled, trusted `UserPromptSubmit` hooks start or reuse the Go filesystem
watcher. It reviews settled changes, including manual edits, without pre/post
tool hooks. The `Stop` hook checks the latest source and waits for Quick results.
This does not depend on the agent choosing to use the skill. Read the
findings, address applicable issues, and allow another review after fixes.
Explain findings you decline.

Without active hooks, record `git rev-parse HEAD` before editing, then review
with that exact starting commit:

```sh
doomer review --base STARTING_COMMIT --deep-review=false --format json
```

If `doomer` is unavailable, complete setup with
`npx @doomerlabs/doomer onboard` before reviewing. The Node manager installs
and configures the Go CLI; reviews run directly through `doomer`. If the user
declines the persistent installation, do not install it or invent a Node review
command: report that the review could not run and continue authorized local work.
For an explicit review of existing changes, `doomer review --deep-review=false --format json` selects the
local default-branch baseline. Use `--path /absolute/path` when needed; review
each repository for cross-repository edits. Manual reviews may include changes
that predate this task; do not represent them as exclusively your edits.

## Permission and results

Review uploads baseline and current source snapshots and the diff. The skill
and hook installation do not grant upload permission. Reuse a valid saved
global service approval (or an existing approval limited to this repository and
agent); otherwise ask the user. Onboarding offers one global permission for all
Doomer reviews across repositories and agents. Never supply
`--approve-upload` or `--approve-uploads` on your own authority. Never bypass
host denials or upload by an alternate route after a refusal.

This workflow requires the Go CLI with direct `watch agent-hook` support; the
manager checks that capability. It does not support the old managed CLI output.
Quick readiness is `early_assessment.status: ready` in the Go CLI result (under
`data` when using its JSON envelope), independent
of aggregate `status`. Deep is disabled on this path. Read `leads` and review
again after fixes. No leads means no Quick findings were returned, not that
the source is proven bug-free. Resume pending results with:

```sh
doomer review get REVIEW_ID --workspace --format json
```

Do not claim completion after a timeout, denial, network failure, or missing
hooks. Report the blocker and continue authorized local work unless the user
explicitly required waiting. `npx @doomerlabs/doomer update` updates the CLI and skill and
repairs configured hooks when requested. `npx @doomerlabs/doomer uninstall`
removes the managed hooks, skill, CLI and local installation data when requested.
