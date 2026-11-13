# Doomer skill

Install Doomer in the environment where Codex or Claude Code edits your files:

```sh
npx @doomerlabs/doomer install
```

Requires Node.js 22+ and Git on macOS or Linux. Choose your agents, review source-upload permission, then open `/hooks` in each selected agent to review and trust Doomer. Start a new session if the hooks have not loaded. Give the agent a small coding task; a completed review confirms that the integration works.

The manager installs the native Go CLI, global `doomer` skill and direct review hooks. No generated skill files or account credentials need to be committed to your project. Each developer chooses their own upload permission and hook trust.

These commands describe the new release. Until the Node package is published, use only a reviewed local checkout for authorized testing; do not substitute a similarly named package.

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

## Legacy installations

The older `doomer-review` skill remains pinned to its compatible Go CLI. Its [legacy installation guide](INSTALL.md) is retained for existing installations; it is not the setup path above. Do not run both sets of automatic review hooks in the same session. Legacy policy, bootstrap and task commands do not apply to the new `doomer` skill.

## License

Apache 2.0.
