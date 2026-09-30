# hermes-learn

Portable teaching skills and functional local learning tools for **Hermes Agent**.
An original implementation inspired by amosblomqvist/learn, not a Pi extension or
fork. [Русская версия](README.ru.md) · [Parity](docs/feature-parity.md) ·
[Security](docs/security.md) · [Troubleshooting](docs/troubleshooting.md)

## Included

- **teach**: prerequisite probing, small motivated lessons, retrieval practice,
  misconception repair, transfer checks, learner-controlled pace and summaries.
- **visualize**: select Mermaid for relationships or SVG for geometry; author,
  exact-edit, render if available, inspect, and publish actual artifacts.
- Self-contained researcher, SVG maker and Mermaid maker delegation briefs.
- Native Hermes tools **learn_quiz**, **learn_journal**, **learn_visual**, plus a
  standalone Python helper. Quiz attempts persist across sessions in SQLite.
- Explicit structured Markdown journal: never a silent full-chat logger.

Python **3.10+**, no runtime Python dependencies. Optional `mmdc` (Mermaid CLI)
and `rsvg-convert` (librsvg) produce PNGs. Nothing installs renderers automatically.

Preferences use Hermes native **clarify**, not a copied Pi popup; when unavailable,
the teacher asks in chat. Graded quizzes are presented in chat/CLI, not a custom
modal. Create/show results hide keys and explanations; the teacher waits for the
learner's actual answer before submit. Keys remain visible in creation tool
arguments and local storage: **this is not a secure examination system**.

## Try without modifying Hermes

From the repository root:

```sh
python -m hermes_learn --help
python -m hermes_learn --data ./learn-data quiz create examples/quiz.json
# Replace QUIZ_ID with the returned id. Options are 1-based.
python -m hermes_learn --data ./learn-data quiz show QUIZ_ID
python -m hermes_learn --data ./learn-data quiz submit QUIZ_ID --answers 1
python -m hermes_learn --data ./learn-data quiz attempts QUIZ_ID
python -m hermes_learn journal ./session.md goal "Understand prerequisite graphs"
python -m hermes_learn visual write ./viz/dependencies.mmd examples/dependencies.mmd
python -m hermes_learn visual render ./viz/dependencies.mmd ./viz/dependencies.png
python -m hermes_learn visual write ./viz/vector.svg examples/vector.svg
python -m hermes_learn visual edit ./viz/vector.svg 'A rightward vector' 'A horizontal vector'
python -m hermes_learn visual render ./viz/vector.svg ./viz/vector.png
```

Use `quiz submit ID --status unknown` for “I don't know”, or `--status skipped`
without key disclosure. `--note "reasoning"` preserves a note. Multi-select input
JSON uses `"multiple": true` and a list of correct indices; grading is exact set
equality. Invalid, duplicate, boolean and out-of-range selections are rejected.
Free-response evaluation is a teacher/rubric workflow, not automated here.

Successful commands emit JSON. Errors emit JSON to stderr and exit nonzero.
Missing renderers return `rendered: false`, source path and reason, without making
a PNG. Renderer execution failure is an error. Rendering does not prove visual
correctness: use a real image/vision tool or viewer and inspect labels and arrows.
Source writing refuses existing files; edits require one unique changed match;
rendering requires a new .png destination.

## Install into an explicit profile

Use a **complete source checkout**. Optional `python -m pip install .` installs
the `hermes-learn` helper command; the wheel includes only the helper, so skill
and plugin installation must run from the checkout with `python -m hermes_learn`.

```sh
python -m hermes_learn install --home /path/to/profile --dry-run
python -m hermes_learn install --home /path/to/profile
```

Replace the path with the selected profile's actual home. Alternatively set
`HERMES_HOME` and omit `--home`. Installation never defaults to the live profile.
Only `skills/teach`, `skills/visualize`, `plugins/hermes-learn` and a hash ownership
manifest are written. The plugin includes its stdlib runtime; it needs no pip
install into Hermes. No config.yaml, global prompts or credentials are changed.

Existing targets are conflicts, never overwrite candidates. **Back up/move your
existing teach/visualize directories explicitly** before installing. Personalized
skills are never silently replaced. Symlinked paths are rejected: choose the
canonical real path. Installation rolls back copied targets on ordinary failure;
it is not crash-atomic across directories or safe against malicious concurrent
filesystem changes.

Enable the native plugin separately, using Hermes in that same profile, and
restart the session:

```sh
hermes plugins list
hermes plugins enable hermes-learn
hermes plugins doctor /path/to/profile/plugins/hermes-learn --ci
```

The file-copy installer does not edit enablement settings. Native integration uses
the documented `plugin.yaml` + `register(ctx)` / `ctx.register_tool` API. Use the
helper if your host lacks this interface. Discover `teach` and `visualize` with
`skills_list`/`skill_view`, and the three tools with tool search. Ask: “Teach me
[topic]; first check what I know.” No provider, model, vault or editor is assumed.
`agents/` files are delegation briefs, **not automatically registered agents**;
load them from linked skill references and pass their contents with the full task
to `delegate_task`, or follow them in the main session when delegation is absent.

## Journal and state contract

Agree on a .md path and consent first. Each journal call appends exactly the
supplied entry under a UTC heading. Kinds: goal, prerequisites, lesson, question,
attempt, feedback, misconception, sources, visual, reflection, next. No session
hook captures messages or tool payloads. Stop by ceasing calls. Do not record
answer keys before attempts or sensitive information without consent. Journals
are Markdown text, not encrypted storage; a single writer per file is recommended.

CLI state defaults to `$HERMES_HOME/learn-data`, or `~/.hermes/learn-data` when
unset; prefer explicit `--data` for isolation. Native quiz tools **require**
HERMES_HOME and fail rather than guess the active profile. SQLite attempts and
keys are stored locally. Journals and visual sources/images use explicit paths.

## Uninstall, backups and updates

Disable using Hermes in the selected profile first:

```sh
hermes plugins disable hermes-learn
python -m hermes_learn uninstall --home /path/to/profile --dry-run
python -m hermes_learn uninstall --home /path/to/profile
```

Uninstall checks hashes and refuses modified/extra files, preserving your edits.
Back up changed files and resolve ownership conflicts manually; there is no force
delete option. Study state, external journals and images survive intentionally.
Upgrade through backed-up uninstall/reinstall; no automatic updater is included.

## Development

```sh
python -m unittest discover -s tests -v
```

CI defines Linux/macOS/Windows on Python 3.10/3.12/3.14. Defining this matrix does
not claim every runner has executed. [Verification](docs/verification.md) records
actual local results and official API documentation. Native tools run with the
user's permissions, not an OS sandbox. See [attribution](ATTRIBUTION.md) for the
MIT license's scope and the independent implementation's provenance.
