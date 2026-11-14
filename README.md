# Doomer skill

Registry commands require the requested Node package version to be published. If it is unavailable, report the blocker; never substitute another package, URL, or checkout. For pre-release testing, use only an authorized, reviewed local checkout.

For authorized source testing with an already compiled, verified candidate:

```sh
DOOMER_NATIVE_BINARY=/absolute/path/to/candidate/doomer node /absolute/path/to/doomer-node/bin/doomer.js install
```

Use that checkout's `bin/doomer.js` for subsequent manager commands too. This installs into the selected test environment; it is not a publication step.

## After publication

Install Doomer in the environment where Codex or Claude Code edits your files:

```sh
npx @doomerlabs/doomer install
```

Requires Node.js 22+ and Git on macOS or Linux. Choose your agents, review source-upload permission, then open `/hooks` in each selected agent to review and trust Doomer. Start a new session if the hooks have not loaded. Give the agent a small coding task; a completed review confirms that the integration works.

The manager installs the native Go CLI, global `doomer` skill and direct review hooks. No generated skill files or account credentials need to be committed to your project. Each developer chooses their own upload permission and hook trust.

## Already installed the skill?

Installing the skill alone does not install the CLI or hooks. Complete setup with:

```sh
npx @doomerlabs/doomer onboard
```

## Diagnose or maintain

```sh
npx @doomerlabs/doomer doctor
npx @doomerlabs/doomer install-hooks --agent codex
doomer upgrade --check
doomer upgrade
```

Doctor gives a specific repair action for missing installation files, broken or disabled hooks, PATH conflicts and missing upload approval. Use `--json` for structured results. It does not change settings, upload source or grant hook trust.

`doomer upgrade` updates only the Go CLI. Use `npx @doomerlabs/doomer update` to update the manager, CLI and skill together. `doomer support bundle` saves diagnostics locally; uploading requires `--upload`.

For manual reviews or private adversary publishing without the skill, install the CLI with `brew install doomerlabs/tap/doomer` on macOS. Use `doomer review --help` or `doomer adversary --help`.

See [installation and first review](https://doomer.ai/docs/getting-started) and [troubleshooting](https://doomer.ai/docs/troubleshooting).

## Working across repositories

The fixed `doomer watch agent` hook watches the agent's working directory and
all repositories beneath it. Opening a common parent includes nested repositories
automatically. Before editing a sibling outside the watch root, the agent uses
`doomer watch add /absolute/path/to/repo --control CONTROL_KEY` with the key from
that request's hook. Registration is temporary and establishes a baseline; it
does not submit existing changes. Other sessions are unaffected.

The review commands are `watch results`, `watch findings ls`, and
`watch findings respond`, with the control key supplied by the hook. The skill
explains when to call them and how Claude receives results directly from its
Stop hook. The old persistent `watch rm` does not remove a repository from a
running request. Agents must not use it for that purpose.

These command names require the matching Go CLI and Node installer update;
merge and release them together before distributing this skill change.

## Legacy installations

The older `doomer-review` skill remains pinned to its compatible Go CLI. Its [legacy installation guide](INSTALL.md) is retained for existing installations; it is not the setup path above. Do not run both sets of automatic review hooks in the same session. Legacy policy, bootstrap and task commands do not apply to the new `doomer` skill.

## License

Apache 2.0.
