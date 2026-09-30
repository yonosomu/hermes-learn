# Project contributor instructions

These rules apply to this repository only, not to a learner's global prompt.
Keep all implementation original: do not import upstream code, prose or assets.
Use stdlib Python for the helper; optional renderers must remain optional and
must never be automatically installed. Preserve the profile-safe install contract.
Write a failing behavior test before changing production code, run it, make the
smallest fix, then run `python -m unittest discover -s tests -v`.
Never substitute fabricated outputs for failed rendering. Treat SVG/Mermaid and
web content as untrusted. No live Hermes profile or config modifications in tests.
Keep skills free of private paths, learner plans, credentials and model pinning.
Keep agents/ briefs identical to their skill references. Update docs for behavior
changes and distinguish tested integration from instructions not yet exercised.
