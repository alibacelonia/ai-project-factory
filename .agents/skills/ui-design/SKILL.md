---
name: ui-design
description: Design, implement, or review graphical frontend components, page layouts, design tokens, responsive behavior, accessibility, and visual style changes in projects with an enabled design system.
---

# UI design

Use this workflow only for a graphical frontend. Backend services and command-line interfaces do not need UI design work unless their requirements explicitly add a graphical surface.

1. Read `project.yaml`, `docs/PROJECT.md`, `docs/ARCHITECTURE.md`, `docs/TASKS.md`, and applicable `AGENTS.md` files. Treat requirements conflicts as blockers to report, not choices to guess.
2. Read only `references/<design.style>.md` for the selected stable style identifier. If the style is absent or unsupported, report it before changing the interface.
3. Inspect the existing design tokens, reusable components, screens, interactions, tests, and dependency conventions.
4. Identify the smallest screen and interaction set required. Preserve business logic, state, APIs, authentication, and custom behavior during visual changes.
5. Prefer semantic tokens and shared accessible components over hardcoded values or per-page styling. Keep style, layout, theme, and effects independently configurable.
6. Implement semantic HTML, keyboard behavior, visible focus, accessible names and errors, adequate target sizes and contrast, and useful loading, empty, disabled, and error states.
7. Check mobile, tablet, and desktop behavior. Decorative layers must not obscure content or create horizontal overflow.
8. Keep motion purposeful, CSS-first, and optional. Respect `prefers-reduced-motion`; provide two-dimensional and non-blur fallbacks where relevant.
9. Run the repository's relevant format, type, component, build, and practical accessibility checks. Automated checks do not establish complete WCAG conformance.
10. Summarize changed screens and tokens, validation actually run, manual checks still needed, and any deliberate divergence from the selected reference.

## Reference routing

The stable style identifiers are: `neumorphism`, `glassmorphism`, `claymorphism`, `skeuomorphism`, `flat-design`, `material-design`, `brutalism`, `neo-brutalism`, `minimalism`, `maximalism`, `bento-grid`, `aurora-ui`, `liquid-glass`, `swiss-international`, `editorial-ui`, `dark-luxe`, `cyberpunk`, `retro-y2k`, `terminal-ui`, `spatial-3d`, `organic-ui`, and `kinetic-ui`.

Read the matching file in `references/` before implementation or style-compliance review. Do not load all style references. For a style change, read both the current and target references, inventory intentional exceptions, then migrate tokens and shared variants before pages.

Layout and effects are separate from the style. Preserve the configured layout and effects unless the requirements explicitly change them. If a decorative effect conflicts with readability, reduced-motion, input clarity, or performance, keep the style's recognizable structure while reducing the effect.
