# Install Doomer

Follow this guide when the user asks to install Doomer. Determine whether the
user wants a team/repository or personal installation. Honor an already stated
choice. When this skill is already active for a coding task in Cowork and only
the editing VM lacks the CLI, use a personal installation inside that VM and
preserve repository files. This is prerequisite setup for the existing skill.
Otherwise, if the choice is unstated, ask personal versus team and wait for the
answer before writing any installation files. Work in the environment that actually edits the target checkout.

## Verified first installation

If a review task is already active, retain its handle and selected runtime.
Continue with the integration-authorization section using that task. If its
executable is missing, use `doomer task repair HANDLE` and resume the same handle.
First-installation and runtime-replacement steps apply when no task is active.
If the active runtime lacks a required onboarding capability, finish or explicitly
stop that task before starting setup with a compatible runtime.

1. If a managed-protocol-2 Doomer CLI is already installed, use it. Check
   `doomer runtime-info` and require `managed_protocol: 2`. If the command fails
   or returns another protocol, use the verified installer in step 2. Do not
   run installation commands through that unsupported executable.
2. Otherwise inspect the installer at
   `https://raw.githubusercontent.com/doomerlabs/skills/bfca6c0edee445d531440fd6f67fac383af85355/scripts/install.py`.
   Download it once to a private temporary directory. Require SHA-256
   `24e71dce733bdeea4fcffa027061b7139013ffcd265872aa82afc4d2941d2bf8`.
   Inspect that same local file, verify the digest again immediately before
   execution, and run that exact file with Python 3. Stop on a digest mismatch;
   never fetch an alternative script or execute a second download. The
   installer gets the official GitHub release manifest, verifies the archive,
   and runs the verified CLI to install the signed runtime and bootstraps.
   Use `--personal` for a personal install or `--repo ABSOLUTE_PATH` for a team
   install. Preserve normal download and execution approval controls.
3. Only with an existing CLI verified as protocol 2 in step 1, run `doomer install --runtime --personal` or
   `doomer install --runtime --repo ABSOLUTE_PATH` as appropriate.
4. Existing conflicting bootstrap files or unmanaged launchers require explicit
   reconciliation. Never silently overwrite them or add `--adopt` without the
   user's specific approval.

## Authorize the coding-agent integration

Run `doomer prepare --agent codex|claude --repo ABSOLUTE_PATH`. Include the actual
coding task through `--prompt` if one was provided. Retain the returned handle.
If setup-only, do not invent a coding task or submit a review.

Attempt preparation before editing so the CLI can retain the starting revision.
If Doomer is blocked by setup, authentication, network access, or host approval,
explain the blocker and ask once whether to continue local edits without a
completed Doomer review or wait for Doomer. Honor the answer for the rest of the
task. Continuing local edits does not approve a blocked upload or a settings
change. Retain the task handle and resume it if Doomer becomes available. If no
task was created, run `git rev-parse HEAD` before local edits and retain that
starting commit. When preparation becomes available, create the task with
`doomer prepare --agent AGENT --repo PATH --prompt "USER TASK" --base STARTING_COMMIT`.
An existing task keeps its original baseline. Report any
incomplete review before finishing.

For Cowork and other environments with a temporary home, add `--portable`.
Install and run inside the environment that edits the checkout. The browser
approval explicitly covers saving account access and the repository grant in
private Git metadata for reuse by later sessions. An existing approved portable
setup is restored by the CLI, including after a mount-path change. Do not copy
credential files or edit grants by hand. A Mac installation is optional.

Use the returned state to decide whether permission is needed. Only for
`update_permission_required`, ask “Allow Doomer to stay up to date automatically?”
Offer “Allow automatic updates (recommended)” first and “Not now” second. After
explicit approval, resume the same handle with
`doomer prepare --task HANDLE --allow-updates`. Reuse an existing approval for
that repository and policy across its branches, linked worktrees, and chats.
When prepare returns ready or another already-authorized state, continue from
that state without asking again. A changed policy or a missing approval may
require a new decision; never manufacture an approval to get past that state.

Before presenting the installation approval, explain that Codex setup also saves
the same authorization in its local approval-reviewer policy so future chats
can reuse it. Include that settings change in the one installation decision.
For `approval_required`, show the exact returned approval URL and ask the user
to open it. The page explicitly authorizes this coding agent to send repository
snapshots, task context, and finding responses to the displayed Doomer service
across all current and future repositories. Sign in there if needed, then choose
Allow. Resume the same handle with `doomer prepare --task HANDLE` after the
browser decision. Reuse the saved approval across repositories, worktrees, and
chats with the same coding agent, Doomer account, service, and profile. Changing
Codex accounts alone does not change the Doomer account or expand this grant.
Never replace the browser decision with an inferred or fabricated approval.

Existing repository-specific grants remain valid for their original scope.
During onboarding, if the returned consent lacks `all_repositories: true`,
explain the integration-wide scope above and ask once to upgrade it. Only after
explicit approval, run `doomer task consent HANDLE --allow --all-repositories`.
Ordinary coding tasks reuse existing grants without repeating onboarding.
An installation request alone does not record upload permission.

Use `doomer.ai` as the production service name in user-facing explanations.
Keep the configured `/api` address in CLI arguments and internal state.
Use `doomer task revoke HANDLE --all-repositories` to revoke the integration-wide
grant. Respect revoked approval and account, service, profile, or agent changes.
A new repository, branch, worktree, or chat under the same integration needs no
additional upload approval. If authentication fails, restore the same account
and recheck the saved grant before asking for upload permission again.

For Codex, the returned `codex_review_policy` describes the same approved scope.
After the combined installation decision, persist that exact authorization in
Codex's approval-reviewer settings using the returned instructions and normal
settings permissions. Reuse the installation answer without another question
when it explicitly covered that settings change and the scope matches. Preserve other
settings. Explain when the host requires a fresh chat or reload before it uses
the policy. Saving a policy does not prove a running reviewer has loaded it.
If the host still blocks Doomer, ask whether to continue local edits as described
above. Report the host limitation and any incomplete review accurately.

## Finish agent integration

For Codex or Claude Code, configure the active agent's hooks during onboarding
with `doomer hooks --agent AGENT`. Installation authorizes adding Doomer’s hook
entries while preserving unrelated hooks. Follow the harness's normal trust
controls and clearly report whether hooks are configured or actually active.
Do not postpone configuration until the next coding request. A headless or
noninteractive invocation can still write hook configuration for future sessions.
Do not skip `doomer hooks` merely because this invocation has no active hook
receipt or session binding. Configure first, then report activation separately.
If configuration actually fails or the harness is unsupported, report that
evidence and use the per-call workflow.

Pass a real session ID to prepare when starting the next actual coding task.
A setup-only task is not that coding task. Native hook callbacks or the normal
per-call commands handle review delivery after edits.

Read and follow the full instructions returned by prepare. They belong to the
same selected release that implements the task commands. Complete an actual
review and record finding responses before claiming review delivery works.

## Team distribution

Team installation includes opening the initial bootstrap pull request unless
the user explicitly requested local-only setup. Use a dedicated branch and stage
only the generated project bootstrap files. Preserve unrelated work, reuse an
existing setup PR when present, and report the PR link before calling team
installation complete. If GitHub access is unavailable, leave the prepared
changes intact and explain what is needed to publish them. Personal installation
does not create a repository PR.

Routine releases do not change the bootstrap files or require upgrade PRs.
Each teammate performs local account and repository onboarding.

## Operational limits

Report network failures with the required host and operation. Do not display
credentials or signed storage URLs. Reuse the task handle after recovery.
An offline environment needs an already verified release permitted by its policy.
A process may terminate between calls, but its private task storage must survive.
