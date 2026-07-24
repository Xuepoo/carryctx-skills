# Code Review SOP

## 1. High-Level Architecture
- Does the PR align with the overall system design?
- Are there any architectural violations (e.g., UI layer accessing DB)?

## 2. Logic & Correctness
- Does the code solve the described problem?
- Are edge cases handled? 

## 3. Security & Performance
- Are inputs sanitized?
- Are database queries efficient? Is there an N+1 problem?

## 4. Maintainability
- Are names descriptive?
- Are functions reasonably sized?

## 5. Conclusion
- Provide a summary and explicit approval or request for changes.