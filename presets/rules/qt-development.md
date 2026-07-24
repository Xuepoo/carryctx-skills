# Qt Development Rules

- Use signals and slots for loosely coupled communication between objects.
- Never block the main GUI thread; use `QThread` or `QtConcurrent` for heavy computations.
- Parent all `QObject` instances correctly to prevent memory leaks via Qt's object tree ownership.
- Prefer modern `connect` syntax (function pointers) over the old `SIGNAL()` / `SLOT()` macros for compile-time type safety.
- Use CMake instead of qmake for modern Qt 6 projects.
