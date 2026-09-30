# Troubleshooting

- **Install says HERMES_HOME required:** pass `--home` with the selected profile's
  canonical home. The installer deliberately refuses an implicit live profile.
- **Conflict at teach/visualize/plugin:** inspect existing files; back up/move them
  yourself. No force overwrite is supported. Dry-run performs the same preflight.
- **Symlink in install path:** provide the real canonical path (on macOS `/var`
  may itself be a symlink). Symlinked targets and installed trees are forbidden.
- **Modified files prevent uninstall:** back up edits and resolve differences
  against the manifest. Extra files also prevent removal. Do not erase edits
  just to make an ownership check pass; manual cleanup is your decision.
- **Tools not visible:** file copy does not enable the plugin. In the same profile,
  run `hermes plugins list`, `hermes plugins enable hermes-learn`, restart Hermes,
  and use tool search. Run Plugin Doctor against the **installed** directory.
  Doctor stages one directory: the checkout's `plugin/` alone lacks the embedded
  runtime that install supplies. Do not claim that unbundled directory is a full
  standalone plugin package; use the installer.
- **Enable fails with missing pm/uv.lock:** this is host package-manager admission,
  not a plugin registration failure. Do not hand-edit config to bypass it. Use
  the helper meanwhile and consult official Hermes troubleshooting for repair.
  Our local enable attempt was blocked; installed Plugin Doctor passed.
- **Older Hermes fails registration:** use the standalone helper. This project
  depends only on documented native ctx.register_tool and JSON-string handlers,
  not an invented global plugin API version. Inspect host diagnostics.
- **Quiz tool says HERMES_HOME missing:** select/export the intended profile's
  home; plugin storage refuses to guess. CLI allows explicit `--data`.
- **No renderer:** .svg and .mmd are usable source artifacts. Install librsvg's
  rsvg-convert or Mermaid CLI's mmdc independently if desired. Mermaid CLI also
  needs a compatible browser setup. The helper never acquires either for you.
- **Renderer failed/timed out:** inspect actual stderr, source syntax and your
  renderer/browser setup. Try a tiny diagram and a new output name. No image is
  produced on failure. Do not disable browser sandboxing to silence an error.
- **Image produced, but not inspected:** open it with a viewer or Hermes vision.
  The `inspected: false` field is intentional; parsing isn't semantic verification.
- **Module not found:** run `python -m hermes_learn` from the complete checkout,
  or install the helper with pip in your own environment. A helper-only wheel
  cannot install repository skills and plugin payloads.
