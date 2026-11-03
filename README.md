# Doomer skills

Agent skills for [Doomer](https://doomer.ai).

## Install

Run this from the repository you want Doomer to review:

```sh
npx skills add doomerlabs/skills --skill doomer-review
```

Then open Codex and start a coding task. You can explicitly invoke `$doomer-review` if it is not selected automatically.

## doomer-review

The first version supports Codex on macOS and Linux (Intel and ARM). It installs Doomer CLI **2026.11.2.1**, sets up Codex hooks, and delivers free initial code-review feedback in your coding conversation. No Doomer account is required.

Before uploading code, Doomer opens a browser consent page for that repository. Installing the skill alone does not authorize uploads. You may also need to restart Codex and trust the installed hooks; the skill provides the steps. Declining leaves you free to continue coding without Doomer.

Reviews use `https://doomer.ai/api`. Local development builds and beta releases are not used. Existing installations are verified, and replacements require approval with a backup. The skill does not automatically request paid Deep reviews.

See [the skill instructions](skills/doomer-review/SKILL.md) for the full workflow.

## Update

```sh
npx skills update
```

## License

[Apache 2.0](LICENSE).
