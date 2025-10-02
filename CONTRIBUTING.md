### Contributing to Dotmotion

Thank you for considering a contribution! This guide helps you set up a dev environment, follow our style, and submit high-quality changes.

## Getting started

- Use Python 3.9+.
- We recommend `uv` for environment and dependency management, but `pip` works too.

```bash
# Clone
git clone https://github.com/MontaQLabs/DotMotion.git
cd DotMotion

# Recommended: uv
uv venv
uv pip install -e .

# Or: pip
python -m venv .venv && source .venv/bin/activate
pip install -e .
```

Install media/tooling for optional features:

- ffmpeg (required for narration/subtitles/music helpers)
- gTTS (optional) for text-to-speech

## Development workflow

- Keep edits focused and readable. Prefer small PRs.
- Update or add example scenes under `examples/`.
- Include or update docs in `README.md` when adding features.
- Ensure examples render without errors: `manim -qh examples/dotmotion_demo.py PolkadotOverview`.

## Code style

- Prefer descriptive names and clear control flow.
- Handle edge cases first; avoid deep nesting.
- Keep comments short; explain "why" over "how".
- Match existing formatting; do not reformat unrelated code.

## Assets and paths

- Place logos in `assets/` and refer to them via `assets/...` paths.
- Use `assets/polkadot-logo.svg` as the default/fallback brand mark.
- Do not add duplicate assets to the repo root.

## Tests and demos

- Manually verify example scripts render at least at `-qm`.
- When adding new helpers, add a minimal usage snippet to `README.md`.

## Submitting changes

1. Open an issue describing the change (bug, enhancement, refactor).
2. Create a feature branch.
3. Commit logically with clear messages.
4. Open a PR and include:
   - Summary of changes and motivation
   - Before/after visuals if applicable
   - Notes on any breaking changes

We appreciate your contributions!


