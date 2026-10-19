# Generated examples

`knowledge-api/` is a committed output snapshot used by the public demo. It was created with:

```bash
uv run project-factory create \
  --name knowledge-api \
  --type ai-service \
  --description "Reference AI service generated for the public demonstration" \
  --feature ai_integration \
  --feature llm_provider \
  --feature aws_bedrock \
  --feature vector_database \
  --feature rag \
  --feature document_processing \
  --feature background_jobs \
  --output examples/generated/knowledge-api
```

The generated Copier source path was normalized from the maintainer's absolute local path to the repository-relative `../../../templates/ai-service` before publication. No application behavior was changed.

The example proves the generated file contract and offline test path. Its in-memory retrieval and FastAPI background task are local extension seams, not production vector storage or a durable job queue.
