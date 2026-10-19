# Security policy

## Reporting a vulnerability

Do not open a public issue containing credentials, exploit details, personal data, or customer information. Until a private security contact is published, provide a minimal public report that asks the maintainer for a private channel and contains no sensitive reproduction material.

## Credential handling

- The factory and generated tests must run without production credentials.
- Commit `.env.example` placeholders only; never commit `.env` files.
- Read provider credentials from the environment and initialize external providers lazily.
- Keep cloud account IDs, secret names, internal URLs, customer names, and email addresses out of examples.
- Review generated infrastructure and least-privilege permissions in the consuming project.

## Local scanning

Run:

```bash
uv sync --extra dev
uv run python scripts/scan_secrets.py
```

The check scans Git-tracked files and unignored untracked files using `detect-secrets`. Placeholder local PostgreSQL URLs are explicitly allowlisted on their source lines. Every allowlist is a review decision, not proof that a value is safe.

Secret scanning is one control. Before publishing, also inspect the complete Git history, review staged changes, and confirm that screenshots, demo recordings, build artifacts, and generated examples contain no sensitive information.

