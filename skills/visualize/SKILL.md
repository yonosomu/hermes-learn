---
name: visualize
description: Use when a learning concept benefits from an accurate minimal SVG or Mermaid diagram.
license: MIT
---

# Visualize

Start with the exact learning obstacle: an order, dependency, relationship,
location, direction, or proportion. Skip decoration. A diagram must answer one
question and must not introduce unverified facts.

Use Mermaid for processes, state transitions, sequence, dependencies, or trees;
use SVG for coordinate geometry, vectors, physical layouts, and precise position.
Give each arrow a meaning (causes, implies, contains, precedes); do not blend them.
For spatial diagrams derive coordinates with tools. Mark not-to-scale drawings.
Include a short textual alternative for accessibility and sources for factual data.

Read `references/mermaid-maker.md` or `references/svg-maker.md` with skill_view
file_path (also mirrored in repository agents/) and pass topic, known facts, exact relationships, audience, desired
output folder, labels, and acceptance checks to delegate_task if available.
Tool restrictions in a brief are instructions, not an OS sandbox. When delegation
is unavailable, perform the same workflow yourself.

Use learn_visual or the helper to write source, make exact unique edits, and
request PNG rendering. Sources .svg/.mmd are real artifacts even without a renderer;
report source-only honestly. No dependency is installed automatically. A returned
rendered=true proves only a PNG was produced. Inspect it with an available image
viewer/vision tool before claiming correctness. If none is available, say it is
not visually inspected. Check arrows, coordinates, overlap, clipping and labels.
Iterate until these checks pass; do not substitute attractive invented data.

Publish to an agreed project folder using a new filename, never a fixed personal
vault path. Return actual source and image paths, renderer status, inspection
status, alt text, and limitations. Embed only files that really exist.
