# Roadmap

The roadmap communicates direction, not a delivery promise. A capability belongs in the supported table only after its generator behavior, documentation, and representative output are tested.

## Supported now

- Deterministic `python-cli`, `web-saas`, and `ai-service` profiles.
- Requirements, architecture, task, decision, and changelog scaffolding.
- Repository-scoped Codex skills and focused review agents.
- Next.js, FastAPI, PostgreSQL, Docker Compose, and GitHub Actions baselines.
- OpenAI and Amazon Bedrock provider adapters selected only when requested.
- Deterministic local retrieval and background-task extension seams.
- A configurable semantic UI system with responsive and accessibility guidance.

## Next

### Release and maintenance foundation

- Publish versioned templates and documented Copier update guidance.
- Add changelog validation and automated package build checks.
- Publish a minimal support and compatibility policy.
- Exercise installation from the built wheel in CI.

### AWS serverless profile

- Python Lambda handler and local unit-test harness.
- API Gateway and EventBridge entry-point options.
- Least-privilege IAM policy inputs without account-specific identifiers.
- Infrastructure that synthesizes reviewable Terraform, with remote state left to the consuming project.
- Packaging and deployment validation that does not require live AWS credentials in pull requests.

### Event-driven service profile

- Explicit event schemas and versioning.
- Queue/topic adapters with deterministic local fakes.
- Idempotency, retry, dead-letter, and replay acceptance criteria.
- Trace-context propagation and structured operational diagnostics.

### Agentic AI profile

- Tool interfaces separated from model and orchestration layers.
- MCP-compatible tool/resource examples with authorization boundaries.
- Evaluation datasets, deterministic graders, and regression thresholds.
- Prompt/version records, output validation, guardrails, and trace hooks.
- Provider-neutral orchestration with optional Bedrock and OpenAI adapters.

## Later, after repeated demand

- Kubernetes service/operator profile.
- Offline edge-agent and synchronization profile.
- Multi-service workspace composition.
- Optional deployment targets with documented cost and security tradeoffs.

## Explicit non-goals

- Generating a production platform from feature flags alone.
- Shipping account IDs, organization policies, secrets, or customer-specific infrastructure.
- Installing every supported integration in default projects.
- Treating generated AI output as verified without tests and human review.

