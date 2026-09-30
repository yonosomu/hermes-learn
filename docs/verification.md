# Verification and known boundaries

## Official Hermes references checked

Fetched the current official docs index (`/docs/llms.txt`), the developer plugin
and creating-skills guides, and inspected the installed Hermes PluginContext API.
Verified the native manifest + register(ctx) contract, ctx.register_tool keywords,
JSON-string handlers receiving args and **kwargs, SKILL.md frontmatter, linked
references, profile-aware HERMES_HOME usage and Plugin Doctor staging behavior.

- https://hermes-agent.nousresearch.com/docs/llms.txt
- https://hermes-agent.nousresearch.com/docs/developer-guide/plugins
- https://hermes-agent.nousresearch.com/docs/developer-guide/creating-skills

No global plugin API version is guessed or declared. The production plugin only
uses documented tool registration; the optional native_smoke.py harness inspects
host registries for testing and is not part of normal installation/discovery.

## Actual local execution

- `python3 -W error::ResourceWarning -m unittest discover -s tests -v`: **19 tests
  passed**, no resource warnings. Final output in tests.txt.
- Behavior slices were implemented through RED/GREEN runs: quiz persistence,
  journal, source helpers, installer, CLI/plugin, then regression fixes. Captured
  regression outputs are tdd-*.txt; paths in captured output are redacted.
- Built a wheel and pip-installed it into an isolated scratch venv: helper command
  help worked. No installation into the system interpreter or Hermes environment.
- Real CLI smoke created a hidden-key quiz, submitted it, re-read persisted
  attempts, appended/read a Markdown goal, and produced actual .mmd/.svg files.
- Real install dry-run, install, uninstall dry-run, uninstall and reinstall ran
  against an isolated profile, preserving study data.
- Hermes Plugin Doctor against the **installed** payload succeeded with three
  tool registrations and zero hooks: see plugin-doctor.txt.
- Direct native PluginContext registration and actual registry-handler invocation
  exercised all three tools (quiz/journal/visual): see native-smoke.txt. This is
  API-level integration, not an end-to-end interactive model/GUI session.

## Honest limitations / blockers

- No mmdc or rsvg-convert was available locally. Both real smoke requests returned
  source-only with renderer-unavailable reasons; no PNG was fabricated. Actual
  successful renderer/PNG inspection is **not locally verified**. Rendering uses
  argv subprocesses, a timeout and PNG-signature checks; provision renderers and
  run the example commands to verify your renderer/browser setup.
- The local packaged Hermes `plugins enable` command failed before activation:
  its PM admission path required a missing `pm/uv.lock`. The host reported config
  and active environment unchanged. No PM repair, global install or live-profile
  workaround was attempted. Use a healthy Hermes installation for end-to-end
  activation; CLI, Plugin Doctor and direct API checks worked independently.
- Plugin Doctor copies only its target directory. The checkout's plugin/ alone
  is unbundled; run Doctor on the directory created by the installer, which embeds
  the runtime. Direct source import is tested, but Doctor staging source plugin/
  alone is not a distributable-payload test.
- Native clarify UI, model-guided pedagogy, vision inspection and delegation are
  host-dependent instructions, not exercised by the stdlib suite.
- Linux/Windows and older Python runs await CI. CI configuration is not a claim
  of completed remote execution. Single-writer journal and serialized installer
  maintenance are documented constraints.

## Reproduce API smoke safely

Create a new disposable profile through this checkout's installer, then use the
Python interpreter belonging to your Hermes installation:

```sh
python -m hermes_learn install --home /absolute/disposable/profile
HERMES_HOME=/absolute/disposable/profile /path/to/hermes/python examples/native_smoke.py
```

The harness registers directly in its own process without writing enablement
config. It appends local study data and creates native-diagram.svg, so use a fresh
profile when re-running (existing visual filenames are intentionally rejected).
Do not substitute the default/live profile.
