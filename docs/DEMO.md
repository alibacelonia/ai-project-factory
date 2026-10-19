# 90-second demo

This walkthrough demonstrates deterministic generation, explicit capability selection, offline-safe testing, and the handoff into requirements-driven development. It does not claim that the selected capabilities are production deployments.

## Prepare

From the repository root:

```bash
uv sync --extra dev
```

Use the automated walkthrough:

```bash
./scripts/demo.sh
```

The script creates a new temporary directory, generates an AI service, runs its tests and lint checks, and leaves the output available for inspection. It does not use an API key or call a live model.

## Recording outline

### 0:00-0:15 — State the problem

> Starting a project is easy; keeping its requirements, architecture, tests, AI instructions, and CI aligned is harder. AI Project Factory creates a small, validated starting point for that workflow.

Show the three profiles:

```bash
uv run project-factory list-templates
```

### 0:15-0:40 — Generate

Run `./scripts/demo.sh`. Point out that the command selects AI integration, a provider boundary, Bedrock, retrieval, document processing, and background-task extension seams. The destination did not exist and is populated only after Copier succeeds.

### 0:40-1:05 — Inspect the contract

Open these files from the generated path printed by the script:

- `project.yaml` — validated technology and capability selections;
- `docs/PROJECT.md` — product requirements and acceptance criteria;
- `docs/ARCHITECTURE.md` and `docs/DECISIONS.md` — derived engineering context;
- `.agents/skills/` and `.codex/agents/` — focused implementation and review workflows;
- `.github/workflows/ci.yml` — generated quality gates.

### 1:05-1:20 — Prove the baseline

Show the passing test and lint output. Explain that the default mock provider is deterministic, so development and CI do not require paid services or credentials.

### 1:20-1:30 — Set expectations

> The result is a tested engineering baseline, not a finished production system. Provider credentials, durable storage, deployment infrastructure, security controls, and service objectives are implemented from the project's actual requirements.

## Optional live API segment

From the generated directory:

```bash
uv run uvicorn knowledge_api.main:app --reload
```

In another terminal:

```bash
curl http://127.0.0.1:8000/health
curl -X POST http://127.0.0.1:8000/v1/generate \
  -H 'content-type: application/json' \
  -d '{"input":"Explain deterministic project generation."}'
```

Keep the recorded demo under two minutes. Do not display local environment files, cloud account details, tokens, customer names, or internal URLs.

