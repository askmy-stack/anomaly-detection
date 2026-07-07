# Contributing

Thank you for your interest in contributing to anomaly-detection!

## Getting started

1. Fork the repository and clone your fork.
2. Create a virtual environment and install in editable mode with dev dependencies:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -e ".[dev]"
   ```

3. Create a feature branch from `main`:

   ```bash
   git checkout -b your-branch-name
   ```

## Development workflow

1. Make your changes following existing project structure and conventions.
2. Run lint and tests locally before opening a pull request:

   ```bash
   ruff check src tests
   pytest tests/ -q
   ```

3. Open a pull request against `main` with a clear description of the change.

## Pull request requirements

- CI must pass (ruff + pytest).
- Keep changes focused; prefer small, reviewable PRs aligned with [docs/EXECUTION_PLAN.md](docs/EXECUTION_PLAN.md).
- Do not commit secrets, large raw datasets, or local virtual environments.

## Code of conduct

This project follows the [Contributor Covenant](CODE_OF_CONDUCT.md). Please be respectful and constructive in all interactions.
