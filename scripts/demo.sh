#!/usr/bin/env bash
set -euo pipefail

repository_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
demo_parent="$(mktemp -d "${TMPDIR:-/tmp}/ai-project-factory-demo.XXXXXX")"
demo_project="${demo_parent}/knowledge-api"

cd "${repository_dir}"

echo "Available profiles"
uv run project-factory list-templates

echo "Generating knowledge-api in ${demo_project}"
uv run project-factory create \
  --name knowledge-api \
  --type ai-service \
  --description "Demonstrate a tested AI-service baseline" \
  --feature ai_integration \
  --feature llm_provider \
  --feature aws_bedrock \
  --feature vector_database \
  --feature rag \
  --feature document_processing \
  --feature background_jobs \
  --output "${demo_project}"

echo "Validating the generated project without cloud credentials"
cd "${demo_project}"
uv sync --extra dev
uv run ruff format --check .
uv run ruff check .
uv run pytest -q

echo "Demo complete. Inspect the generated project at: ${demo_project}"
