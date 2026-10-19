# Releasing

Releases are deliberate maintainer actions. Automation may prepare and validate a release, but it must not merge, push, or create a tag without maintainer review.

## Prepare a release

1. Confirm the working tree contains only intended changes.
2. Review `CHANGELOG.md` and move the intended entries from `Unreleased` to the release version and date.
3. Keep these versions aligned:
   - `pyproject.toml` project version;
   - `ProjectMetadata.template_version` in `src/project_factory/config.py`;
   - `template_version` defaults in every `templates/*/copier.yml`.
4. Run the complete local validation:

   ```bash
   uv sync --extra dev
   uv run ruff format --check .
   uv run ruff check .
   uv run pytest
   uv run python scripts/scan_secrets.py
   cd gallery && npm test
   ```

5. Build the package and inspect its contents:

   ```bash
   uv build
   python -m zipfile -l dist/*.whl
   ```

6. Generate one project from the built tool in a clean temporary environment and run its documented checks.
7. Open and review the pull request for the release branch.

## Merge and tag

After CI passes and the release change is merged into the default branch, the maintainer can create an annotated tag:

```bash
git switch main
git pull --ff-only
git tag -a v0.2.0 -m "AI Project Factory v0.2.0"
git push origin v0.2.0
```

Replace the example version with the reviewed release version. Never tag the feature branch or an unreviewed working tree.

## Public release notes

State which profiles and capabilities are implemented. Describe feature flags that create extension seams as extension seams; do not imply production authentication, billing, queues, vector infrastructure, or cloud deployment when those remain application work.

