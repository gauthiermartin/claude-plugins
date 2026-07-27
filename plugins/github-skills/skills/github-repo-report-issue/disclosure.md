# Coordinated Disclosure

The security branch. A vulnerability goes to the maintainers **privately** first, never the public tracker — a public issue is a zero-day announcement with no fix available.

## Route, in priority order

1. **`SECURITY.md`** (root, `.github/`, or `docs/`) — the project's stated channel. Follow it exactly; it overrides everything below.
2. **GitHub private vulnerability reporting** — if enabled, `Security → Advisories → Report a vulnerability` (a private GHSA draft). Check with `gh api repos/{owner}/{repo} --jq '.security_and_analysis'` or by looking for the "Report a vulnerability" button on the Security tab.
3. **A security contact** — `security@`/`security.txt` (`/.well-known/security.txt`), or a maintainer's listed address. Encrypt if a PGP key is published.
4. **No channel exists** — do **not** open a public issue describing the exploit. Open a minimal, non-actionable issue asking only how to report a security problem privately, or reach a maintainer through a private channel. Say what class of issue it is, never the exploit.

## What the report contains

- The finding: affected component, version/commit, and impact (what an attacker gains).
- A minimal proof of concept, enough to reproduce, no more.
- Suggested remediation if you have one.
- Whether it's already public anywhere, and your disclosure-timeline expectations.

## What stays out of anything public

Until there's a fix and the maintainers agree to disclose: no exploit code, no vulnerable file/line, no PoC, and no "security" issue titles that point at the weakness. Redact secrets you found from the report body itself.

## After sending

Give maintainers reasonable time to respond before any public mention (commonly up to 90 days). Let them drive the advisory and CVE. Get approval before submitting — the user decides what leaves privately, just as with a public issue.
