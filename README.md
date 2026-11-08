# Doomer managed skill

Install once. Doomer manages compatible CLI releases and their matching review
instructions outside the repository. Each task keeps one release until it ends.

## Team installation

Ask your coding agent to read and follow [INSTALL.md](INSTALL.md). Choose team
installation to add managed discovery blocks to `AGENTS.md` and `CLAUDE.md`,
and the small bootstrap to `.agents/skills/doomer-review/SKILL.md`
and `.claude/skills/doomer-review/SKILL.md`. Review and commit those files once.
Each developer completes their own account login, repository upload approval,
and optional hook trust. Ordinary managed upgrades leave repository files alone.

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
