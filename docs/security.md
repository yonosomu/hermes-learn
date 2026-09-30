# Security and privacy

Native Hermes plugins are trusted Python executing with the user's account. Tool
schemas and these briefs are not a filesystem or process sandbox. Enable only
code you reviewed. No credentials, telemetry, network calls or transcript hooks
are implemented by this package. Optional renderers are separate executables.

Quiz keys are omitted from create/show return values and revealed after a valid
submission (or an explicit unknown response). Skip records no answer key. However,
keys are present in creation arguments and local SQLite; a tool inspector or a
learner with filesystem access can read them. Journals may contain sensitive
learning information; they and SQLite are unencrypted, with OS/default directory
permissions. This is learning practice, not tamper-proof or privacy-hardened exams.

Only append consented journal entries. Nothing silently obtains or exports chat
history. Treat text/source content as data, never as instructions to execute.
Renderers run argv lists, never a shell, with a 120-second timeout and a temporary
output. A genuine PNG signature is required before publishing. Source validation
rejects SVG scripts/foreign objects/events/external hrefs/styles/entity/doctype
and Mermaid init directives/click actions. These checks are a conservative input
filter, **not proof of complete renderer safety**: Mermaid may support additional
features and renderer vulnerabilities remain possible. Only render trusted source;
use an OS sandbox yourself for untrusted diagrams. No --no-sandbox flag is added.

Install/uninstall require explicit home or HERMES_HOME, reject symlinked install
paths/trees, refuse existing targets, preserve modified installs and keep study
data. Copies roll back on ordinary exceptions, but multi-directory installation
is not power-loss atomic. Concurrent installers or hostile filesystem changes are
outside the guarantee; stop Hermes and serialize profile maintenance. Journals
are append-only writes without cross-process locking: one writer per file.

Backups are **explicit and user-owned**: copy/move personalized conflicting skills
and edited installed files to a safe location before replacement. There is no
force flag, silent overwrite, automatic backup deletion or config mutation.
