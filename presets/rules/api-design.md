# Domain Rules: REST API Design

Whenever designing or reviewing a REST API within this repository, you must adhere to the following absolute constraints:

## 1. Resource Naming

- Use plural nouns for collections (`/users`, not `/user`).
- Nest resources to express ownership, capped at two levels (`/users/{id}/orders`, not `/users/{id}/orders/{id}/items/{id}`).
- Never put verbs in URLs (`/users/{id}/deactivate` is wrong; use `PATCH /users/{id}` with a status field or a sub-resource like `POST /users/{id}/deactivations`).

## 2. Versioning

- Version via URL path (`/v1/users`), not headers, unless the API already commits to header-based content negotiation.
- Bump the major version only on breaking changes (removed fields, changed types, altered semantics). Additive fields never require a bump.
- Support at most two major versions concurrently; deprecate the older one with a published sunset date.

## 3. Error Response Shape

- Every error response uses a fixed envelope: `{ "error": { "code": "string", "message": "string", "details": {} } }`.
- `code` is a stable machine-readable identifier (e.g. `RESOURCE_NOT_FOUND`), never a raw HTTP status string.
- `message` is human-readable and safe to display; never leak stack traces, SQL, or internal paths into it.
- `details` holds structured, field-level context (e.g. validation errors per field), and is omitted (not null) when empty.

## 4. Pagination

- Use cursor-based pagination for any collection that can grow unbounded; offset-based pagination is acceptable only for small, stable datasets.
- Cursor endpoints accept `cursor` and `limit` query params and return `next_cursor` (null when exhausted) alongside the page.
- Never let `limit` be unbounded; enforce a server-side max and document the default.

## 5. Idempotency

- `POST` endpoints that create a resource must accept an `Idempotency-Key` header; replaying the same key returns the original result instead of creating a duplicate.
- `PUT` and `DELETE` must be naturally idempotent by design (same request repeated has the same effect), so clients can safely retry on timeout without an idempotency key.
- Never make `GET` or `DELETE` have side effects beyond the resource they name; retries must be safe by construction.
