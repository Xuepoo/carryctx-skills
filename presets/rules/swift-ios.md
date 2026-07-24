# Domain Rules: Swift / iOS Development

Whenever working on a Swift or iOS project within this repository, you must adhere to the following absolute constraints:

## 1. Optionals Discipline

- Never force-unwrap (`!`) outside of test targets or where a crash is truly impossible (e.g. `IBOutlet`s wired in Interface Builder).
- Prefer `guard let ... else { return }` for early exits and `if let` for scoped unwrapping.
- Use `??` to provide a default only when a sensible default genuinely exists; don't use it to silently mask a missing value that should be handled explicitly.

## 2. Memory Management

- Capture `self` as `weak` in closures stored beyond the current scope (completion handlers, `Combine` sinks, `Task` bodies held by long-lived objects) to avoid retain cycles.
- Use `unowned` only when the closure's lifetime is provably shorter than or equal to the captured object's (e.g. a delegate callback guaranteed to fire before deallocation).
- Delegate properties on the delegating side must be declared `weak var delegate: SomeDelegate?`, never strong, to avoid owner/delegate retain cycles.

## 3. SwiftUI vs UIKit Conventions

- In SwiftUI, use `@State` for view-local mutable state, `@Binding` to share mutable state with a child view, and `@Observable` (or `@StateObject`/`@ObservedObject` on older targets) for shared reference-type models. Never reach for `@State` on a reference type that needs external mutation.
- Compose views from small, single-purpose `View` structs instead of building massive view bodies; extract subviews once a `body` exceeds roughly one screen of code.
- In UIKit, avoid Massive View Controllers: move business logic into view models or dedicated coordinator/data-source objects, keeping the view controller responsible only for lifecycle and wiring.

## 4. Concurrency

- Prefer structured concurrency (`async`/`await`, `Task`, `TaskGroup`) over nested completion-handler callback pyramids for new asynchronous code.
- Isolate shared mutable state behind an `actor` rather than guarding it with manual locks or `DispatchQueue` synchronization.
- Mark UI-facing types and methods `@MainActor` explicitly rather than relying on incidental thread hops; never touch UIKit/SwiftUI state from a background `Task` without hopping back to the main actor first.
