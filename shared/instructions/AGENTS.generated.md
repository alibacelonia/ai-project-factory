# Project engineering instructions

Treat `project.yaml` and `docs/PROJECT.md` as the primary requirements sources. If they conflict with each other or with repository instructions, stop and report the conflict.

- Follow the selected architecture and existing patterns; preserve separation of concerns and avoid speculative abstractions.
- Use consistent naming, explicit error handling, appropriate validation, and no unrelated edits.
- Never hardcode or log secrets. Apply least privilege, validate authorization boundaries, and avoid unsafe shell commands.
- Add tests for new behavior and regression tests for fixes. Never claim a check passed unless it was executed.
- Do not commit, push, deploy, overwrite user changes, or run destructive Git commands automatically.
- Update `docs/TASKS.md` as work progresses and record significant architecture changes in `docs/DECISIONS.md`.
- When `design.enabled` is true for a graphical frontend, treat style, layout, and effects
  as separate requirements. Preserve semantic tokens, shared accessible components, and
  application behavior; use `$ui-design` for visual changes and load only the selected
  style reference.

Use repository skills for detailed bootstrap, requirements, UI design, feature, testing, and review workflows. Use `ui-ux-engineer` for review-only frontend design and accessibility analysis when appropriate.

