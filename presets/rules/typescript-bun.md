# Bun & TypeScript Development Guidelines

## Toolchain & Runtime Rules
1. **Runtime**: Use Bun ESM runtime (`bun run`, `bun test`, `bun build`).
2. **Type Safety**: Enable strict TypeScript checks (`"strict": true`, `"noImplicitAny": true`).
3. **Database**: Use native `bun:sqlite` for local embedded database interactions with parameterized queries.

## Coding Standards
1. **Module Syntax**: Use clean ESM `import`/`export` syntax exclusively.
2. **Error Handling**: Use explicit error result types or structured exception envelopes.
3. **Quality Gates**: Run `bun test`, `prettier`, and `eslint` before completing tasks.
