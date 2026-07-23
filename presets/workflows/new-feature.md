# Workflow Blueprint: Develop New Feature

**Trigger**: Use this workflow when assigned to develop a new capability or feature in the codebase.

## Steps to Execute:

1. **Understand Requirements**: 
   - Read the issue or task description.
   - If anything is ambiguous, ask the user for clarification before writing any code.
2. **Architecture Design**: 
   - Write a short implementation plan.
   - Check `.carryctx/rules/` to ensure your plan complies with project standards.
3. **Test-Driven Development**: 
   - Write a failing unit test or integration test for the new feature first.
4. **Implementation**: 
   - Write the actual implementation code to make the test pass.
   - Run local formatters and linters (`cargo fmt`, `cargo clippy`, `npm run lint`, etc.).
5. **Documentation**: 
   - Update `CHANGELOG.md` with the new feature.
   - Add docstrings to all new public functions/classes.
6. **Checkpointing**:
   - Run `carryctx checkpoint --task <TASK_ID>` with a message summarizing the completed feature.
