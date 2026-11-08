# Doomer review skill

Doomer brings quick-review questions into Codex and Claude Code while you work.
Your coding agent investigates them and records its decisions. Quick reviews are
free and need no Doomer account; repository uploads still need your approval.

## Get started

Open your repository in your coding agent and paste:

```text
Read https://doomer.ai/install.md and follow the instructions to set up Doomer in this repository.
Use a personal installation.
```

For a shared installation, replace the second sentence with “Use a team
installation.” Follow the browser upload-approval link, then give your agent a
small coding task. Ask it to confirm a completed review of the latest changes
and share the review link. A completed review may have no findings; installed
files alone do not confirm that a review ran.

See [the first-review walkthrough](https://doomer.ai/docs/reviews/quick/first-review)
and [what is uploaded](https://doomer.ai/docs/reviews/quick/data-and-permissions).

## Managed releases

Install once. Doomer manages compatible CLI releases and their matching review
instructions outside the repository. Each task keeps one release until it ends.

## Team installation

Ask your coding agent to read and follow [INSTALL.md](INSTALL.md). Choose team
installation to add the small bootstrap to `.agents/skills/doomer-review/SKILL.md`
and `.claude/skills/doomer-review/SKILL.md`. Review and commit those files once.
Each developer completes their own repository upload approval and any required
hook trust. Account sign-in is optional for quick reviews. Ordinary managed
upgrades leave repository files alone.

## Personal installation

Choose personal installation. The same bootstrap is installed in the user's
agent directories, making it available across projects. Repository policy wins
when both personal and project bootstraps exist. Runtime files and credentials
are local to the environment that actually edits the checkout.

## Upgrade policy

Policy is string-valued metadata inside SKILL.md. Keep both project copies in
agreement. There is no separate committed configuration file.

- `doomer-protocol: "2"` selects this bootstrap contract.
- `doomer-update-policy: stable` uses verified eligible stable releases.
- `doomer-update-policy: delayed` also requires `doomer-delay-hours: "24"` (or another delay).
- `doomer-update-policy: pinned` requires `doomer-version: YYYY.M.D.N`.
- `doomer-update-policy: manual` requires approval to advance beyond the selected release.

The developer explicitly authorizes software updates during onboarding. This is
separate from permission to upload repository content and trust agent hooks.
Doomer downloads signed releases side by side. Tasks retain their selected
release even when another task or repository upgrades. Team policy changes are
intentional repository edits; ordinary product releases require no PR.

## Remote and ephemeral environments

The bootstrap can be read directly even when absent from a native skill catalog.
`doomer prepare` returns a durable task handle. Its task commands work across
separate invocations without a persistent watcher or localhost browser callback.
Device login runs in the editing environment and can resume after a tool exits.
Task state needs persistent storage between calls. A destroyed VM without its
state cannot resume a local handle; do not claim otherwise or copy credentials
from another machine.

## License

Apache 2.0.
