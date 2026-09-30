# Feature map and intentional differences

Feature inspection covered upstream README, both skills, all three agent briefs,
quiz/ask-user-question/md-log extensions, and visual-tools index/common/Mermaid/
SVG implementations plus package metadata. No upstream files/assets were copied.

| Original component | Hermes implementation | Limits / deliberate adaptation |
|---|---|---|
| teach skill | `skills/teach` | Generic learner goals, adaptive prerequisite checks, dependency-aware small lessons, retrieval and transfer; no private learner plans or mandated Obsidian |
| visualize skill | `skills/visualize` | Real source authoring/edit/render tools; inspection is explicitly separate; main-session fallback allowed |
| ask-user-question popup | Native Hermes `clarify` | Preference clarification only; host controls UI; chat fallback, no Pi UI lock or custom popup |
| Graded quiz extension | `learn_quiz` + CLI | Single/multi-select, exact grading, explanation after attempt, note, unknown and skip, persisted history; no custom interactive modal or secure key isolation |
| md-log extension | `learn_journal` + CLI | Explicit typed Markdown appends; no hooks, backfill, automatic mirroring, slash log link or full-chat capture |
| researcher | Portable linked delegation brief | Primary-source verification with host search/extract, no provider/model pin or safe_bash dependency |
| mermaid-maker | Portable linked brief + visual helper | Optional existing mmdc; no bundled Node dependencies, Chromium download or disabled sandbox |
| svg-maker | Portable linked brief + visual helper | Conservative static SVG with optional rsvg-convert; no ImageMagick fallback |
| write/edit/render tool trios | One `learn_visual` action tool + CLI | Explicit source paths and new output filenames rather than process-global managed staging |
| Visual publication and inline images | Returned real source/PNG paths and normal Markdown | User-selected folder; no vault-specific name resolution, tool-return image attachment or automatic embedding |
| Pi interactive-subagents registration | Hermes `delegate_task` instruction briefs | No named agent registry is assumed; main-session workflow works without delegation |

The helper handles executable persistence/validation/visualization, while skills
handle pedagogy. It does not provide autonomous course creation, review scheduling,
external note synchronization, learner analytics, or open-ended automatic grading.
