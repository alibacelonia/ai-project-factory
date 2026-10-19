# AI Project Factory

AI Project Factory is a local, Copier-based generator for small projects that are ready for requirements-driven development with OpenAI Codex. It creates independently runnable applications with concise repository instructions, reusable skills, project-scoped custom agents, tests, and CI. Generation itself makes no AI API calls and requires no paid service.

## Prerequisites

- Python 3.12 or newer
- [uv](https://docs.astral.sh/uv/)
- Node.js 20.9+ and Docker Compose only when working with the web SaaS profile
- Codex CLI or a Codex-enabled editor for the optional AI-assisted workflow

## Install

For development:

```bash
git clone <this-repository-url> ai-project-factory
cd ai-project-factory
uv sync --extra dev
uv run project-factory list-templates
```

Install the command as an isolated local tool:

```bash
uv tool install .
project-factory --help
```

Templates are packaged into the wheel, so an installed tool does not need to run from this repository.

## Generate a project

Interactive:

```bash
project-factory create
```

Non-interactive:

```bash
project-factory create \
  --name my-cli \
  --type python-cli \
  --description "Automate a recurring local task" \
  --output ./projects/my-cli
```

Repeat `--feature` for supported optional capabilities:

```bash
project-factory create \
  --name knowledge-api \
  --type ai-service \
  --feature ai_integration \
  --feature llm_provider \
  --feature openai_api \
  --output ./projects/knowledge-api
```

For a frontend project, choose visual style, composition, theme, palette, typography, motion, and optional effects independently:

```bash
project-factory create \
  --name luminous-dashboard \
  --type web-saas \
  --ui-style glassmorphism \
  --ui-layout dashboard \
  --theme dark \
  --color-palette indigo-cyan \
  --typography sans \
  --animation subtle \
  --ui-effect glass-surfaces \
  --output ./projects/luminous-dashboard
```

Run `project-factory list-ui-styles` for the concise catalog or `project-factory list-ui-styles --details` for recommended uses, default layouts, and theme behavior. Interactive `create` asks design questions only for `web-saas`; backend-only and CLI projects remain lightweight, and passing UI options to them is rejected.

The destination must not exist. Generation occurs in a temporary sibling directory and is moved into place only after Copier succeeds, so existing directories are never silently overwritten.

## Starter profiles

| Profile | Stack | Default local behavior |
| --- | --- | --- |
| `python-cli` | Python, Typer, Rich, pytest, Ruff, uv | Full CLI starter with configuration, structured logs, expected-error handling, and unit tests |
| `web-saas` | Next.js, TypeScript, FastAPI, PostgreSQL, Docker Compose | Separate frontend/backend; `/health` and backend tests do not require PostgreSQL |
| `ai-service` | Python, FastAPI, Pydantic, pytest | Deterministic mock provider, external prompt file, dependency-injected provider test, and no required API key |

Run `project-factory list-templates` to see the optional feature names allowed for each profile. Unsupported features and incompatible selections are rejected. For example, subscriptions require authentication, external AI adapters require both `ai_integration` and `llm_provider`, and RAG requires both AI integration and a vector database selection.

Optional selections create explicit extension seams and only selected external provider dependencies. They are not a claim that production-grade authentication, billing, email, queues, or RAG infrastructure has been designed before the product requirements exist.

## UI design system

The `web-saas` profile includes one shared, accessible component layer and a data-driven catalog of 22 distinct presets. Each preset defines intentional light and dark semantic colors, typography, surface treatment, borders, shadows, interaction, responsive behavior, and accessible fallbacks. Layout and effects remain independent, so a dashboard need not use a dashboard-oriented style and a visual preset need not force animation.

| Identifier | Visual identity | Recommended for |
| --- | --- | --- |
| `neumorphism` | Soft raised/inset tonal surfaces | Productivity apps and widgets |
| `glassmorphism` | Frosted panels and luminous layered edges | SaaS and premium dashboards |
| `claymorphism` | Inflated rounded forms and soft dimensional color | Consumer and education apps |
| `skeuomorphism` | Tactile physical metaphors and material cues | Simulators and specialized controls |
| `flat-design` | Direct color blocks and minimal depth | Utilities and data dashboards |
| `material-design` | Tonal layers, elevation, state feedback, and structured shells | Cross-platform and form-heavy apps |
| `brutalism` | Raw type, exposed grids, and stark edges | Experimental and cultural sites |
| `neo-brutalism` | Vivid blocks, heavy outlines, and hard offset shadows | Startups, creative SaaS, and portfolios |
| `minimalism` | Restrained color, whitespace, and quiet hierarchy | Enterprise apps and portfolios |
| `maximalism` | Layered color, ornament, and dense storytelling | Creative brands and arts projects |
| `bento-grid` | Multi-size modular cards and scan-friendly grouping | Landing pages and overview dashboards |
| `aurora-ui` | Blurred spectral gradients behind stable content surfaces | AI products and landing pages |
| `liquid-glass` | Fluid translucent layering and soft highlights | Premium interfaces |
| `swiss-international` | Strict grid, typographic rigor, and precise alignment | Enterprise and editorial systems |
| `editorial-ui` | Magazine pacing, display type, and content-led layouts | Blogs, portfolios, and publications |
| `dark-luxe` | Deep tailored surfaces and restrained metallic light | Developer tools and premium SaaS |
| `cyberpunk` | Dark technical surfaces and controlled neon signals | Gaming and technology products |
| `retro-y2k` | Gloss, chrome, pixel accents, and nostalgic color | Music, fashion, and creative sites |
| `terminal-ui` | Monospace command hierarchy with modern controls | Developer and CloudOps platforms |
| `spatial-3d` | Perspective and layered depth with 2D alternatives | Product showcases and immersive apps |
| `organic-ui` | Natural curves, asymmetric rhythm, and earth tones | Wellness and lifestyle products |
| `kinetic-ui` | Typography-led movement and narrative transitions | Interactive landing pages and campaigns |

Supported layouts are `standard`, `dashboard`, `bento-grid`, `editorial`, `landing-page`, `sidebar-application`, `split-screen`, and `full-screen`. Optional effects are `none`, `subtle-transitions`, `aurora-gradients`, `glass-surfaces`, `kinetic-animation`, and `spatial-depth`. Theme mode is `light`, `dark`, or `system`; the latter is the default.

The semantic token contract covers background, foreground, primary, secondary, accent, surface, muted, destructive, border, focus, typography, spacing, radius, elevation, transparency, blur, and motion. Buttons, form controls, cards, dialogs, dropdowns, tables, tabs, badges, alerts, navigation, sidebars, headers, tooltips, loading states, and empty states share that contract rather than being copied 22 times.

Material Design is an inspired preset, not a complete implementation of Google's Material component library. Liquid Glass uses CSS translucent surfaces with opaque fallbacks rather than platform-native materials. Spatial 3D uses CSS depth by default and provides a readable two-dimensional path; it does not install or require WebGL.

### Preview the gallery

The gallery belongs to the factory rather than generated production applications. It uses the same preset data and component contract, works without credentials, and supports style browsing, light/dark switching, layouts, viewports, representative components, token inspection, and configuration copying.

```bash
cd ai-project-factory/gallery
npm run dev
```

Open `http://127.0.0.1:4173`. The small local server gives the shared Jinja CSS template the correct stylesheet content type. Generated applications receive the selected production design system and representative home page, not the whole gallery.

### Change a generated project's style

1. Back up or commit application work.
2. Change `design.style` in `project.yaml`; adjust layout and effects only when the requirements call for it.
3. Ask Codex to use `$ui-design`, which reads only the selected style reference.
4. Apply the choice to the generated design configuration and shared semantic tokens, preserving business logic, state, API integration, authentication, and custom component behavior.
5. Review any proposed structural change before implementation, then run frontend checks and inspect both themes, responsive widths, keyboard paths, and reduced motion.

Custom colors must be six-digit hex values such as `#6366F1`. The schema rejects unknown styles/layouts, `none` combined with another effect, glass effects without transparency and blur, kinetic motion without a reduced-motion alternative, and UI configuration on profiles without a graphical frontend.

### Add a UI preset

1. Add its stable identifier to `UIStyle` in `src/project_factory/design.py`.
2. Add one complete light/dark entry to `templates/web-saas/template/frontend/design-system/presets.json` with all required token and capability fields.
3. Add `.agents/skills/ui-design/references/<identifier>.md` to the factory and web template.
4. Extend the standalone Copier choices and documentation.
5. Add registry, generation, gallery, semantic-token, and build coverage; verify responsive, focus, contrast, and reduced-motion behavior manually.

Do not add a per-style copy of every component. Add a specialized variant only when the visual language genuinely requires different presentation while retaining the shared accessible behavior.

## Project configuration

Every generated project contains `project.yaml`, validated by the factory's Pydantic schema. It records:

- project identity, type, stage, and template version;
- selected language, backend, frontend, and database;
- profile-specific feature flags;
- local deployment and Docker choices;
- testing, linting, CI, cost, and offline-development constraints.
- for graphical frontends, an optional `design` section containing style, layout, theme, typography, surfaces, effects, responsive targets, and accessibility policy.

A complete frontend example is available at `examples/web-design-project.yaml`. The core design shape is:

```yaml
design:
  enabled: true
  style: glassmorphism
  layout: dashboard
  theme:
    mode: system
    palette: indigo-cyan
    primary_color: "#6366F1"
    accent_color: "#22D3EE"
  typography:
    preset: sans
    heading: Inter
    body: Inter
    scale: default
  surfaces:
    border_radius: medium
    shadow_intensity: medium
    transparency: medium
    blur_intensity: medium
  effects:
    animation: subtle
    enhancements: [glass-surfaces]
  responsive:
    mobile: true
    tablet: true
    desktop: true
  accessibility:
    target: WCAG-2.2-AA
    reduced_motion: true
```

Define the product by editing only:

1. `project.yaml` for structured technology and capability choices.
2. `docs/PROJECT.md` for the problem, users, requirements, scope, and acceptance criteria.

Codex is instructed to report conflicts between those sources instead of choosing an interpretation silently. The remaining files under `docs/` are maintained as derived engineering artifacts:

- `ARCHITECTURE.md` — stack, components, data flow, security, and deployment;
- `TASKS.md` — prioritized tasks, status, dependencies, and acceptance criteria;
- `DECISIONS.md` — durable architecture decisions and tradeoffs;
- `CHANGELOG.md` — notable project changes.

## Use with Codex

Open the generated directory as the project root. Codex automatically reads the concise root `AGENTS.md` and discovers repository skills from `.agents/skills/`.

A typical workflow is:

```text
Use $project-bootstrap to validate this generated project.
Use $requirements-analysis to turn docs/PROJECT.md into an MVP task plan.
Use $feature-development to implement the first ready P0 task.
Use $testing to add and run the appropriate checks.
Use $code-review to review the completed changes.
Use $ui-design for frontend screens, design tokens, responsive work, or a visual restyle.
```

The five common skills, plus the frontend-only `ui-design` skill, are focused workflows rather than copies of `AGENTS.md`. Each has the required `name` and `description` YAML frontmatter described by the [official Skills documentation](https://developers.openai.com/api/docs/guides/tools-skills).

Generated projects also contain standalone custom agents in `.codex/agents/` using the current `name`, `description`, and `developer_instructions` format:

- `software-architect` evaluates design choices and implementation risk.
- `security-reviewer` reports actionable security findings by severity.
- `ui-ux-engineer` reviews style fidelity, semantic-token use, reusable components, responsive behavior, interactions, accessibility, and performance-sensitive effects.

Ask Codex to delegate an independent review to one of those names when appropriate. Their default instructions are analysis-only, but custom-agent instructions are not a filesystem permission boundary: subagents inherit the parent session's sandbox and approvals, as documented in the [official Subagents guide](https://learn.chatgpt.com/docs/agent-configuration/subagents).

For UI work, `$ui-design` progressively loads only `.agents/skills/ui-design/references/<design.style>.md`. A useful request is:

```text
Use $ui-design to implement the new portfolio projects page using project.yaml.
Preserve existing behavior and validate both themes, mobile layout, keyboard access,
focus visibility, contrast, and reduced motion. Then ask ui-ux-engineer to review it.
```

Accessibility takes priority over exact decorative fidelity. Automated tests cannot prove WCAG conformance; use them alongside manual keyboard, zoom, contrast, reading-order, and assistive-technology checks. Prefer CSS, system/local font fallbacks, reduced effect density on mobile, no layout-shifting decoration, and lazy loading for any genuinely required complex effect.

## Run generated applications

Python CLI:

```bash
cd projects/my-cli
uv sync --extra dev
uv run my-cli hello Codex
uv run pytest
```

AI service:

```bash
cd projects/knowledge-api
uv sync --extra dev
uv run uvicorn knowledge_api.main:app --reload
```

Web SaaS:

```bash
cd projects/my-saas
cp .env.example .env
docker compose up --build
```

Each generated README contains profile-specific non-Docker and test commands.

## Develop and test the factory

```bash
uv sync --extra dev
uv run ruff format --check .
uv run ruff check .
uv run pytest
```

The suite validates names, profile/feature/design compatibility, all 22 preset records, semantic token completeness, layouts and effects, safe destinations, YAML, skill metadata, agent TOML, file substitution, representative generations, generated Python tests, gallery coverage, theme behavior, and the dependency-free frontend smoke test. Run the generated frontend's type check, tests, and production build for release validation. GitHub Actions runs its configured checks without secrets, cloud credentials, live models, or production databases.

## Add a starter profile

1. Add a new `ProjectType` and allowed feature set in `src/project_factory/config.py`.
2. Add its display metadata in `src/project_factory/generator.py`.
3. Create a self-contained `templates/<profile>/copier.yml` and `template/` tree.
4. Include the shared project contract: configuration, requirements docs, `AGENTS.md`, skills, agents, README, tests, environment example, ignore rules, and CI.
5. Add representative generation and isolated smoke tests.
6. Ensure the wheel still contains the new template and direct Copier generation works.

Keep starters small. A profile should not add services or dependencies that its default application does not need.

## Add a skill

Create `.agents/skills/<skill-name>/SKILL.md` with lowercase hyphenated naming and YAML frontmatter containing a matching `name` and a discriminating `description`. Put reusable workflow guidance in the body. Add `references/`, `scripts/`, or `assets/` only when they provide concrete value, and validate both the factory copy and generated copies.

When a skill belongs in every generated project, add it to each self-contained template and extend the metadata integration test. This small intentional duplication keeps each Copier root and every generated project portable.

## Add a custom agent

Add `.codex/agents/<name>.toml` with `name`, `description`, and `developer_instructions`; mirror it into applicable templates and extend TOML parsing tests. Keep the role narrow. Do not put sandbox or approval claims in the file: configure permissions on the parent Codex session.

## Safely update a generated project

Copier writes `.copier-answers.yml`, and `project.yaml` records `template_version`. To update:

1. Commit or back up application changes.
2. Use the same versioned template source (prefer a released Git tag when this repository is published).
3. Run Copier's update flow or generate the newer template beside the project.
4. Review the complete diff and resolve conflicts deliberately.
5. Re-run format, lint, unit, integration, and smoke checks.

The factory does not include a custom migration framework and does not promise automatic conflict-free upgrades. Local template paths in Copier metadata may need to be replaced with the published repository URL before updating on another machine.

## Repository layout

```text
ai-project-factory/
├── .agents/skills/          # Factory development workflows
├── .codex/agents/           # Factory-scoped specialist agents
├── .github/workflows/       # Factory CI
├── gallery/                 # Local, dependency-free 22-style explorer
├── shared/                  # Canonical guidance and engineering references
├── src/project_factory/     # CLI, schema, generator, and validation
├── templates/               # Three independently usable Copier roots
├── tests/                   # Unit and generation/smoke integration tests
└── examples/                # Example structured configuration
```

## End-to-end example

```bash
uv sync --extra dev
uv run project-factory create \
  --name release-notes \
  --type python-cli \
  --description "Create release notes from local Git history" \
  --output /tmp/release-notes
cd /tmp/release-notes
uv sync --extra dev
uv run release-notes hello "first run"
uv run pytest
```

Then edit `project.yaml` and `docs/PROJECT.md`, open `/tmp/release-notes` in Codex, and start with `$requirements-analysis`.

