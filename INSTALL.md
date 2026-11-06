# Install Doomer

Follow this guide when the user asks to install Doomer. Determine whether the
user wants a team/repository or personal installation. Honor an already stated
choice. If the choice is unstated, ask personal versus team and wait for the
answer before writing any installation files. Work in the environment that actually edits the target checkout.

## Verified first installation

1. If a managed-protocol-2 Doomer CLI is already installed, use it. Check
   `doomer runtime-info` and require `managed_protocol: 2`. If the command fails
   or returns another protocol, use the verified installer in step 2. Do not
   run installation commands through that unsupported executable.
2. Otherwise inspect the installer at
   `https://raw.githubusercontent.com/doomerlabs/skills/5c0c3d42d467003228323ddd1e5936cbecfe1457/scripts/install.py`.
   Download it once to a private temporary directory. Require SHA-256
   `3d451a6699450a28f1498a29cd6e9593ab2f852fec0e578e2efe4f03eb4d49d3`.
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

## Onboard the selected repository

Run `doomer prepare --agent codex|claude --repo ABSOLUTE_PATH`. Include the actual
coding task through `--prompt` if one was provided. Retain the returned handle.
If setup-only, do not invent a coding task or submit a review.

Use the returned state to decide whether permission is needed. Only for
`update_permission_required`, explain the requested update policy and ask for
standing software-update and version/task-state reporting permission. After
explicit approval, resume the same handle with
`doomer prepare --task HANDLE --allow-updates`. Reuse an existing approval for
that repository and policy across its branches, linked worktrees, and chats.
When prepare returns ready or another already-authorized state, continue from
that state without asking again. A changed policy or a missing approval may
require a new decision; never manufacture an approval to get past that state.

For `approval_required`, show the exact returned repository-approval URL and
ask the user to open it. That page displays this repository and its linked
worktrees, previous grants, and the upload scope. If needed, the user signs in
there before choosing Allow. After the browser decision, resume the same handle
with `doomer prepare --task HANDLE`. Repeat that command when the decision is
still pending. Approval and sign-in survive separate CLI calls and need no local
browser callback. Never replace this flow with a generic CLI login page or
manufacture a grant in chat. Never copy credentials from another environment.

Use `doomer.ai` as the production service name in user-facing explanations.
Keep the configured `/api` address in CLI arguments and internal state. Require
both authenticated identity and upload permission before claiming setup ready.
If the user declines, leave uploads disabled.

Repository approval already covers the repository's linked worktrees. A new
chat, branch, or linked checkout alone does not require another upload approval.
Reuse the CLI's saved consent evidence when it reports authenticated identity
and upload permission; ask again only when the CLI reports missing or revoked
consent or the requested scope changes.

## Finish agent integration

For Codex or Claude Code, configure the active agent's hooks during onboarding
with `doomer hooks --agent AGENT`. Installation authorizes adding Doomer’s hook
entries while preserving unrelated hooks. Follow the harness's normal trust
controls and clearly report whether hooks are configured or actually active.
Do not postpone configuration until the next coding request. When the harness
cannot load these hooks, explain that limitation and use the per-call workflow.

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
