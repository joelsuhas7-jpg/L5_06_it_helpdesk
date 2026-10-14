# Lab 5 — Static Code Analysis Issues

The issue list below records the source-code problems identified during review. Run Pylint, Bandit, and Flake8 locally and update line numbers/messages to match the reports generated on your machine.

| Issue | Type | Line(s) in original | Description | Fix Approach |
|---|---|---:|---|---|
| Shell command injection risk | Security / High | 33–34 | A hostname is concatenated into a command string and passed with `shell=True`. Untrusted input could alter the command. | Validate the hostname and pass arguments as a list to `subprocess.run()` with `shell=False` and a timeout. |
| Hardcoded administrator password | Security / High | 6, 49 | A credential is stored directly in source code. Anyone who can read the file can discover it. | Read the expected password from `HELPDESK_ADMIN_PASSWORD`; do not commit the secret. |
| Broad exception suppressed | Reliability / Medium | 18–21 | A bare `except` catches unrelated errors and hides failures, making debugging difficult. | Validate ticket existence and raise a clear `ValueError`. |
| Mutable default argument | Correctness / Medium | 8 | `audit_trail=[]` reuses the same list across calls when omitted. | Use `None` as the default and create/use a list explicitly. |
| Invalid urgency accepted | Correctness / Medium | 11, 43 | Negative priorities and values outside the documented 1–5 range can be stored. | Convert and validate urgency before creating a ticket. |
| File handling without context manager | Reliability / Medium | 37–39 | A write failure can leave the file handle open, and errors are not explained. | Use `with open(...)` (or `Path.open`) and handle/report `OSError`. |
| Missing ticket validation | Correctness / Medium | 15, 19, 25 | Assignment, note addition, and closing can fail or behave unexpectedly for unknown IDs. | Centralize existence checks and report invalid ticket IDs. |
| Non-idiomatic function name and `None` comparison | Maintainability / Low | 27–30 | `unresolvedHighPriority` does not follow PEP 8, and `== None` is discouraged. | Rename to `unresolved_high_priority()` and use `is None`. |

## Verification checklist

- [ ] Run `python helpdesk_system.py` and test valid urgency values.
- [ ] Try urgency `-7`, `0`, `6`, and non-numeric input; no invalid ticket should be created.
- [ ] Try adding a note to an unknown ticket; a clear error should be shown rather than silently ignored.
- [ ] Review `ping_user_machine()` to confirm it does not use `shell=True`.
- [ ] Run Pylint, Bandit, and Flake8 after saving this file; record the actual output and remaining warnings.
