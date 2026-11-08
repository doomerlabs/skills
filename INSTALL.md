# Install Doomer

Quick reviews need no Doomer account. The browser setup page can approve an
anonymous installation; do not ask the user to sign in for quick reviews.
`authenticated=true` may confirm an installation credential, not an account
login. Account-backed features use a signed-in account when one is selected.

Installation is complete when the skill and CLI are ready, upload approval is
verified, and hook configuration and activation are reported separately.
A setup-only task must not upload source to prove readiness. Verify review
delivery during the user's next coding task, using the checklist below.

## Read the original instructions

Use the complete raw Markdown for installation. WebFetch and other document
readers can summarize away the installer URL or shorten its SHA-256 digest.
If a reader summarizes the guide or omits either exact value, retrieve the
original from the same URL using `curl -fsSL` through the shell. For the public
entry point, use `curl -fsSL https://doomer.ai/install.md`. For a pinned guide,
keep its pinned URL and verify its expected checksum. For a supplied local guide,
read the original file directly. Honor host or user access denials.

Regardless of which reader is used, the installer URL and digest must equal the
pinned values in step 2 below. Stop if another copy supplies different values.

Copy the complete installer URL and all 64 checksum characters from the raw
guide. Keep the full commit and `/scripts/install.py` path. Never reconstruct
them from an abbreviated summary. The guide and pinned installer are public
HTTPS resources; use unauthenticated HTTPS if a GitHub CLI command asks to log in.
If the original guide remains unavailable or verification fails, stop and report
that specific failure.

Follow this guide when the user asks to install Doomer. Determine whether the
user wants a team/repository or personal installation. Honor an already stated
choice. When this skill is already active for a coding task in Cowork and only
the editing VM lacks the CLI, use a personal installation inside that VM and
preserve repository files. This is prerequisite setup for the existing skill.
Otherwise, if the choice is unstated, ask personal versus team and wait for the
answer before writing any installation files. Work in the environment that actually edits the target checkout.

## Verified first installation

Installation writes local runtime and skill files. Creating a team PR is a
separate agent step, omitted for local-only setup.

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
   `https://raw.githubusercontent.com/doomerlabs/skills/270530b0757ddab34ec5ff3a9ea2880ada1074a2/scripts/install.py`.
   Download it once to a private temporary directory. Require SHA-256
   `c156c42a11a08110edd3d0ac0e1837d1886e3f993f6a3ad101b621fb7c26942b`.
   Inspect that same local file, verify the digest again immediately before
   execution, and run that exact file with Python 3. Stop on a digest mismatch;
   never fetch an alternative script or execute a second download. The
   installer reads the official stable channel, verifies the archive,
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
explain the blocker once and continue authorized local edits and tests by default.
Do not ask whether to continue. Explicit user requirements to wait or require
review before editing take precedence. Keep denied uploads and settings changes
blocked, and do not retry explicit reviewer refusals.
Retain the task handle and resume it if Doomer becomes available. If no
task was created, run `git rev-parse HEAD` before local edits and retain that
starting commit. When preparation becomes available, create the task with
`doomer prepare --agent AGENT --repo PATH --prompt "USER TASK" --base STARTING_COMMIT`.
An existing task keeps its original baseline. Follow the skill's final-source
review rules when reporting coverage; never claim unreviewed changes were reviewed.

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

Before presenting upload approval, explain what it covers: repository snapshots
include the baseline source and the current working tree, including unchanged
tracked files, staged/unstaged edits, and non-ignored untracked files. Git metadata
and ignored untracked files are excluded. Adding an already tracked file to
`.gitignore` does not exclude it. Task context and finding responses are also
sent to Doomer. Link to https://doomer.ai/docs/reviews/quick/data-and-permissions
for the data and permission details.

Codex may also offer an optional local approval-reviewer policy to reuse this
authorization in future chats. Explain that this is a separate settings change.
Include it in a combined decision only if the exact proposed text and changes
are available and the user explicitly accepts them; otherwise ask separately
when the proposal is returned. Upload approval alone does not authorize it.
For `approval_required`, show the exact returned approval URL and ask the user
to open it. The page explicitly authorizes this coding agent to send repository
snapshots, task context, and finding responses to the displayed Doomer service
across all current and future repositories for this integration. For quick
reviews, approve without signing in; account sign-in is optional. Resume the same
handle with `doomer prepare --task HANDLE` after the
browser decision. Reuse the saved approval across repositories, worktrees, and
chats with the same coding agent, installation credential or Doomer account,
service, and profile. Changing Codex accounts alone does not expand this grant.
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
After explicit acceptance of the policy proposal, persist that exact authorization in
Codex's approval-reviewer settings using the returned instructions and normal
settings permissions. Reuse the installation answer without another question
when it explicitly covered that settings change and the scope matches. Preserve other
settings. Explain when the host requires a fresh chat or reload before it uses
the policy. Saving a policy does not prove a running reviewer has loaded it.
If the host still blocks Doomer, continue authorized local edits and tests without
asking again, unless the user explicitly required review first. Report the host
limitation once and include the final review status at handoff.

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

## Verify the first coding review

During the next user-authorized coding task, verify all of the following:

1. The review completed for the latest source, not an earlier revision.
2. Every returned hypothesis has an acknowledged agent response. Zero hypotheses
   is a valid completed review; do not invent a defect to demonstrate the service.
3. `doomer task finish HANDLE` confirms completion for that source.
4. Share the returned review link and distinguish completed, pending, blocked,
   or latest changes not reviewed. State separately whether hooks are active or
   explicit task commands delivered the review.

Continue authorized local work if review is unavailable, unless the user made it
a gate. Do not call a pending review, installed CLI, or configured hook a completed
review. Never start an extra coding task just to finish setup.

## Team distribution

Team installation includes opening the initial bootstrap pull request unless
the user explicitly requested local-only setup. Use a dedicated branch and stage
only the generated project bootstrap files. Preserve unrelated work, reuse an
existing setup PR when present, and report the PR link before calling team
installation complete. If GitHub access is unavailable, leave the prepared
changes intact and explain what is needed to publish them. Personal installation
does not create a repository PR.

Routine releases do not change the bootstrap files or require upgrade PRs.
Each teammate performs local setup and upload approval. Quick reviews need no
account; team installation does not share credentials or grants.

## Operational limits

Report network failures with the required host and operation. Do not display
credentials or signed storage URLs. Reuse the task handle after recovery.
An offline environment needs an already verified release permitted by its policy.
A process may terminate between calls, but its private task storage must survive.
