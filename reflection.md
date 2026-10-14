# Lab 5 — Reflection

## 1. Which issues were the easiest to fix, and which were the hardest? Why?

The easiest issues were style and readability problems, such as renaming `unresolvedHighPriority()` to `unresolved_high_priority()` and changing `== None` to `is None`. These changes are small and do not alter the program's intended behavior. The hardest issue was the unsafe ping command because it required both validating user input and changing how the operating-system command is executed. Removing the hardcoded administrator password also required changing the program's configuration and testing procedure.

## 2. Did the static analysis tools report any false positives? If so, describe one example.

A static-analysis warning is not automatically proof of an exploitable bug. A tool may flag a pattern without knowing how the value is used at runtime. For example, a subprocess-related warning may need manual review to determine whether input can actually be controlled by a user. I would classify a finding as a false positive only after inspecting the relevant code and verifying that the reported risk does not apply. The exact false positives, if any, should be based on the reports generated during this lab rather than assumed in advance.

## 3. How would static analysis improve software quality and security?

Static analysis checks source code without requiring every execution path to be run. Tools such as Pylint, Flake8, and Bandit can identify style problems, likely defects, and risky coding patterns early. Fixing these issues improves readability, consistency, maintainability, and security. Static analysis complements, but does not replace, tests and manual review because tools can miss bugs or report findings that need contextual verification.

## 4. What did you learn, and what would you improve in the future?

I learned that code can appear to work while still containing unsafe input handling, hidden exceptions, invalid data, and resource-management problems. I would improve the project by adding automated unit tests for urgency validation, unknown ticket IDs, password configuration, and ticket-file saving. I would also run the analysis tools after each meaningful change and keep their reports so that improvements can be demonstrated with evidence.
