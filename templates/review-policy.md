## Required Doomer review workflow

INSTALLED_AGENT_SKILL_PATHS

For an active agent listed above, if its skill or required reference files are missing,
continue the normal task and report the missing installation. Do not infer
permission to reinstall it. Otherwise, before each user turn that will edit
repository files, read its installed doomer-review skill and
references/install.md from disk. Follow the skill for documentation, configuration,
tests, and application code, including small edits and requests that do not
explicitly mention review.

Run the skill's local CLI version and managed-installation check once per
editing turn before making changes. Use the current on-disk pin and the skill's
saved approval decisions. A version remembered from an earlier turn or a
previously completed setup does not satisfy this check. Keep the online skill
update check scoped to once per coding session as the skill directs.

Follow the skill's setup and review workflow. Reuse valid repository consent
and verified hook activation. Keep repository upload consent and agent hook
trust as user choices, preserve a paused watcher, and honor explicit skip
decisions and the skill's read-only and skill-maintenance exemptions.

Use trusted hooks to capture changes and deliver review results. Investigate
feedback, fix confirmed issues within the user's scope, and record responses
as the hooks direct. Follow the skill's completion gate for the current
revision and include the complete Doomer review link when a review is delivered,
including a review with no findings.
