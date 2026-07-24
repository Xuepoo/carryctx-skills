# React Frontend Rules

- Use modern React with Functional Components and Hooks.
- Avoid prop-drilling; use Context API or state management (Zustand/Redux) when state is shared deeply.
- Use Tailwind CSS or CSS Modules. Do not use inline styles.
- Memoize expensive calculations with `useMemo` and callbacks with `useCallback` only when necessary.
- Ensure all interactive elements are fully accessible (ARIA labels, keyboard navigation).
