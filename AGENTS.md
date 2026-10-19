# AI Project Factory instructions

- Treat `project.yaml` and `docs/PROJECT.md` in generated projects as the primary requirements sources. Report conflicts instead of guessing.
- Keep the factory modular: validation, configuration, generation, and CLI concerns stay separate.
- Preserve Copier template independence and generated-project independence.
- Make the smallest complete change; do not add optional infrastructure by default.
- Never hardcode or log secrets. Validate inputs and handle errors explicitly.
- Add tests for behavior changes and regression tests for fixes. Run relevant checks before claiming success.
- Do not commit, push, deploy, overwrite user changes, or use destructive Git commands automatically.
- Update documentation, `TASKS.md`, and architecture decisions when behavior or architecture changes.

