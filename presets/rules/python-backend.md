# Python Backend Rules

- Use strict PEP 8 formatting (Black/Ruff).
- Enforce type hints on all function signatures.
- Prefer `uv` or `poetry` for dependency management. No global pip installs.
- For APIs, use FastAPI with Pydantic v2 schemas for robust validation.
- Never leave `except Exception:` blocks empty. Always log errors appropriately.