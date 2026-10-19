# Python engineering standard

- Support Python 3.12 or newer and use a `src/` package layout.
- Manage environments and dependencies with `uv`.
- Use Ruff for formatting and linting and pytest for behavior-focused tests.
- Keep imports side-effect free; external clients and credentials are initialized lazily.
- Prefer typed, small functions and explicit domain exceptions over catch-all error handling.

