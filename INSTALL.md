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

Explain the requested update policy and ask for standing software-update
permission. After explicit approval, resume the same handle with
`doomer prepare --task HANDLE --allow-updates`.

For `authentication_required`, run `doomer task login HANDLE`, show its returned
verification URL and user code, and let the user authenticate. Re-run that same
command after approval. It resumes the original device request without a local
browser callback. Never copy credentials from a host into a remote VM.

For `consent_required`, explain that Doomer uploads base/current repository
snapshots, the task prompt, and finding responses to the displayed service.
Only after the user's explicit approval run `doomer task consent HANDLE --allow`.
Resume prepare and require authenticated identity and upload permission.

The per-call workflow works without hooks. For an environment with reliable
session IDs and trusted hooks, the user can opt into `doomer hooks --agent AGENT`
and pass its real session ID to prepare. Configuration is separate from live
activation. A real scoped hook callback establishes activation.

Read and follow the full instructions returned by prepare. They belong to the
same selected release that implements the task commands. Complete an actual
review and record finding responses before claiming review delivery works.

## Team distribution

Team installation creates small project-local bootstraps. Leave them uncommitted
unless the user requested Git publication. Routine future releases do not change
those files or require pull requests. Each teammate performs local onboarding.

## Operational limits

Report network failures with the required host and operation. Do not display
credentials or signed storage URLs. Reuse the task handle after recovery.
An offline environment needs an already verified release permitted by its policy.
A process may terminate between calls, but its private task storage must survive.
