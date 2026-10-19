---
name: feature-development
description: Implement a requested feature in an existing project after its requirements and acceptance criteria are understood.
---

# Feature development

1. Inspect relevant code, tests, `project.yaml`, and requirements documentation.
2. Confirm the smallest complete change that satisfies the acceptance criteria.
3. Follow existing architecture and dependency patterns; avoid unrelated refactors.
4. Implement explicit validation and error handling at system boundaries.
5. Add focused tests, including failure cases that protect the new behavior.
6. Run relevant format, lint, and test commands and report their actual results.
7. Update `docs/TASKS.md`, and update architecture or decisions only when they changed.

When a feature changes a graphical screen, component, layout, interaction, theme, or design token, use the `ui-design` workflow and the selected-style reference when available. Preserve application behavior and the existing design system; do not redesign unrelated screens. Skip this route for non-UI work.

