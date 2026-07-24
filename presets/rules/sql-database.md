# Domain Rules: SQL Database Development

Whenever working on a project that reads or writes a SQL database within this repository, you must adhere to the following absolute constraints:

## 1. Parameterized Queries

- Never build SQL by string concatenation or f-strings/template literals with interpolated values; always use placeholders (`?`, `$1`, `:name`) bound through the driver's parameter API.
- User input, including values used in `LIKE`, `IN`, or `ORDER BY`, must go through parameter binding or an explicit allowlist, never raw interpolation.

## 2. Migration Discipline

- Every schema change is a versioned migration file with a monotonic prefix (timestamp or sequence number); never edit a migration that has already shipped.
- Each migration contains exactly one logical change (e.g. add a column, add an index) so it can be reviewed and reverted independently.
- Every migration must have a working reverse/down migration, or be explicitly documented as irreversible with the reason stated.

## 3. Indexing Rules

- Index every foreign key column and every column used in frequent `WHERE`, `JOIN`, or `ORDER BY` clauses.
- Do not add speculative indexes on write-heavy tables; each index adds write cost, so justify it against an observed or expected query pattern.
- Prefer composite indexes ordered by selectivity over multiple single-column indexes when queries filter on the same column set together.

## 4. Transaction Boundaries

- Wrap logically related writes (e.g. insert order + insert order_items) in a single transaction so they commit or roll back together.
- Keep transactions as short as possible; never hold a transaction open across a network call, external API request, or user interaction.
- Choose the isolation level explicitly when the default is insufficient (e.g. read committed vs. serializable), rather than relying on driver defaults silently.

## 5. Schema Change Safety

- Prefer additive, backward-compatible migrations (add nullable column, add table) over destructive ones (drop column, rename) that break running application code.
- When a destructive change is required, stage it: add the new shape, migrate reads/writes to it, then remove the old shape in a later deploy.
- Avoid `ALTER TABLE` operations that require a full table lock on large tables during peak traffic hours; use online/concurrent schema-change tooling where the database supports it (e.g. `CREATE INDEX CONCURRENTLY` in PostgreSQL).
