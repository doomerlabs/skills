# Doomer skills

Agent skills for [Doomer](https://doomer.ai).

## Install

Run this from the repository you want Doomer to review:

```sh
npx skills add doomerlabs/skills --skill doomer-review
```

Select Codex or Claude Code when the installer asks, then open that agent and start a coding task. Explicitly invoke `$doomer-review` in Codex or `/doomer-review` in Claude Code if it is not selected automatically.

Codex installs under `.agents/skills/`; Claude Code installs under `.claude/skills/`.

## doomer-review

The skill supports Codex and Claude Code on macOS and Linux (Intel and ARM). It installs Doomer CLI **2026.11.3.3**, sets up the active agent's hooks, and delivers free initial code-review feedback in your coding conversation. No Doomer account is required.

The CLI owns onboarding and saved task context. Trusted hooks deliver assessments, including zero-finding results, and review links; the skill does not poll internal state or require Python helpers.

Before uploading code, Doomer opens a browser consent page for that repository. Installing the skill alone does not authorize uploads. Claude verifies live hook delivery and continues without a restart when hooks respond. Codex may need a restart; the skill provides the steps. Approve any trust prompt in the coding agent yourself. Declining leaves you free to continue coding without Doomer.

Reviews use `https://doomer.ai/api`. Local development builds and beta releases are not used. Existing installations are verified, and replacements require approval with a backup. The skill does not automatically request paid Deep reviews.

See [the skill instructions](skills/doomer-review/SKILL.md) for the full workflow.

## Update

```sh
npx skills update
```

## License

[Apache 2.0](LICENSE).
