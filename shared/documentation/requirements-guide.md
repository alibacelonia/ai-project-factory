# Requirements guide

Define product intent in `docs/PROJECT.md` and technical selections in `project.yaml`.
Write observable acceptance criteria, keep non-goals explicit, and update `docs/TASKS.md`
after analysis. Architecture details belong in `docs/ARCHITECTURE.md`; durable tradeoffs
belong in `docs/DECISIONS.md`.

For projects with a graphical frontend, the optional `design` section in `project.yaml`
defines structured UI intent: the primary style, layout, theme, typography, palette,
surface treatment, effects, responsive targets, and accessibility target. Treat these as
inputs to `ARCHITECTURE.md` and `TASKS.md`, not as business logic. Keep custom component
behavior intact when a preset changes, and report conflicts with `PROJECT.md` instead of
silently redesigning unrelated screens.

Style, layout, and effects answer different requirements:

- `style` defines the visual language and semantic token values.
- `layout` defines page composition independently of the style.
- `effects` add optional motion, glass, gradient, or depth treatments.

Requirements should name the intended screens, content hierarchy, interaction states,
responsive priorities, supported themes, and measurable accessibility outcomes. Avoid
subjective acceptance criteria such as “looks modern.” Prefer observable criteria such as
“the primary navigation remains keyboard-operable at 320 CSS pixels” or “reduced-motion
mode removes non-essential travel animation without hiding state changes.”

When changing a preset, scope work to semantic tokens and shared variants first. Preserve
business logic, state, API integration, identity, and data behavior. If the selected style
requires a structural composition change, document it as a separate task and decision
before editing custom screens. Automated accessibility checks are supporting evidence, not
proof of WCAG conformance.

