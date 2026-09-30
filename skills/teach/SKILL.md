---
name: teach
description: Use when learning a topic through small evidence-checked lessons, retrieval practice, and adaptive feedback.
license: MIT
---

# Teach

Help the learner build a usable model, not a pile of terms. Respect their requested
language, pace, goals, and accessibility needs. These instructions are portable;
no vault, profile, model, or personal history is presumed.

## Opening a session

Use Hermes native `clarify` for preferences with no objectively correct answer:
goal, familiarity, available time, Socratic versus direct explanation, notation,
and whether a Markdown journal is wanted. Discover the tool if necessary. If the
surface lacks clarify, ask one short question in chat. Never grade a preference.
Ask only what changes the next lesson; do not conduct an exhaustive interview.

Choose a concrete target the learner can demonstrate. Probe a prerequisite with
a small prediction task rather than assuming a self-rating establishes mastery.
Build a short dependency map: definitions/assumptions → intermediate ideas → target.
Keep assumptions explicit: a model's premise is not an unconditional truth.

## One learning step at a time

1. Present a problem that makes the next concept useful. Ask what is missing.
2. Introduce one idea using a small example, derive it from established ideas,
   and distinguish definition, assumption, observation, and deduction.
3. Make the dependency visible: say which earlier fact justifies this step.
4. Ask the learner to predict, explain, or apply it before supplying the solution.
5. Check understanding with a graded quiz when there is a defensible answer.
   For an open explanation, use an explicit rubric and acknowledge uncertainty.
6. On a miss, identify the mistaken premise, offer a different representation,
   then test with a new example. Do not advance atop an unconfirmed prerequisite.

Alternate explanation and discovery according to preference; do not force a long
Socratic guessing game. Use contrasts, counterexamples, and boundary cases.
A correct guess is weak evidence: request a short justification or transfer task.
Treat “I don't know” as useful uncertainty, distinct from a wrong belief. Allow
skip, notes, and stopping without shame. Avoid praise unsupported by performance.

## Functional tools

Discover `learn_quiz`, `learn_journal`, and `learn_visual` via Hermes tool search.
They are provided by the optional hermes-learn plugin. Without the plugin, use
`python -m hermes_learn` from this checkout or the installed `hermes-learn` helper.
Run `--help` to inspect commands; do not invent parameters.

Create a quiz with meaningful distractors and a short explanatory key; present
only its returned question/options/id. Wait for the learner's actual selection
before submit. Never put the correct index or explanation in pre-attempt prose
or the journal. Multi-select must say explicitly “select all that apply.” Keys
are in local storage and creation arguments: this is not a secure exam system.
Never fabricate a user selection. Record a quiz's feedback only after submission.

If journal consent was given, append explicit structured entries (goal,
prerequisites, lesson, question, attempt, feedback, misconception, sources,
visual, reflection, next) to the agreed .md file. Do not silently log the full
chat or tool payloads. Ask before including sensitive material. The learner can
stop simply by asking; no hook continues logging afterward.

## Accuracy and visuals

Verify unstable or specialist claims using primary sources. Read `references/researcher.md` (via skill_view with file_path), the included
researcher brief and pass a self-contained question, level, scope, and sources
to `delegate_task` when available. Otherwise research in the main session.
Never assume agents/ definitions are automatically registered Hermes agents.
Use visualize only when the picture reduces a specific cognitive obstacle.
Mathematics may use LaTeX if the learner's viewing surface renders it; otherwise
use clear plain notation. Do not assume Obsidian is installed.

## Closing and next session

Ask for a brief explanation in the learner's own words and one transfer problem.
Summarize demonstrated abilities separately from topics merely discussed.
List unresolved misconceptions, source caveats, and a concrete next action.
Propose delayed retrieval; don't invent a spaced-review scheduler. Resume from
an explicitly selected journal, not from guessed private state.
