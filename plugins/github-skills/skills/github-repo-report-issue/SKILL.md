---
name: github-repo-report-issue
description: Report a bug, vulnerability, or feature request to an external open-source repo the right way.
disable-model-invocation: true
---

# Report Issue

Report one finding to an open-source repo you don't control, so a maintainer can act on it without a round-trip. Two things drive every decision:

- the target repo's **house rules** — its own issue templates, `CONTRIBUTING`, `SECURITY` policy, and label vocabulary. You adopt them; you do not impose your own.
- whether the finding is a security vulnerability — which forks the whole workflow. **Never open a public issue for a vulnerability.**

Classify first, then work the steps in order.

## Step 1 — Classify: bug/feature, or vulnerability?

Decide the branch before any other legwork. If the finding lets someone do something they shouldn't — read others' data, run code, bypass auth, exfiltrate secrets, take the service down — it is a **vulnerability**: switch to `disclosure.md` and do not use the public-tracker steps below.

Completion: you have named the branch, and if it is security, handed off to `disclosure.md`.

## Step 2 — Read the repo's house rules

Fetch and read, on the default branch:

- `SECURITY.md` (root, `docs/`, or `.github/`) — the disclosure channel, even for the public branch (confirms it's *not* the route for this one).
- `CONTRIBUTING.md` — reporting rules, required info, label conventions.
- `.github/ISSUE_TEMPLATE/*` and `.github/ISSUE_TEMPLATE/config.yml` — the actual templates and `blank_issues_enabled` / `contact_links`.
- Whether Issues are enabled at all, or redirected to Discussions or an external tracker (Jira, Bugzilla, a mailing list).

`gh repo view`, `gh api repos/{owner}/{repo}/contents/.github/ISSUE_TEMPLATE`, and a plain fetch of the raw files cover this.

Completion: you know the destination channel, which template applies, and the project's label vocabulary. If issues are disabled or redirected, you have the correct alternate destination.

## Step 3 — Dedupe

Search **open and closed** issues *and* pull requests for the same thing — a fix may already be merged, or a report may have been closed as wontfix. Match on the behaviour, not your wording.

`gh search issues --repo owner/repo "<terms>"`, `gh search prs --repo owner/repo "<terms>"`, and vary the terms.

If a live match exists, add a comment there (a fresh repro, your environment, a "still happening on vX") instead of filing a new issue, and stop. A closed-as-fixed match means verify against current code (Step 4) before deciding it's new.

Completion: you have either linked an existing match and stopped, or confirmed none exists across open+closed issues and PRs.

## Step 4 — Verify it's current and reproducible

Confirm the problem exists on the **default branch or latest release**, not a stale or shallow checkout — a fix may have landed since. Point to the exact current file and line. Build the smallest repro that shows it, and capture the version/commit, OS, and runtime you observed it on.

For a feature request, "reproduce" becomes: state the concrete current-state limitation, verified against current code, that motivates it.

Completion: you can cite the exact current code and a minimal repro (or, for a feature, a verified current-state motivation).

## Step 5 — Draft a triage-ready report

Fill the repo's actual template fields. If it has none, use the default in `report-anatomy.md`. A report is **triage-ready** when a maintainer can act on it without asking you a question.

See `report-anatomy.md` for the anatomy and the default template.

Completion: every required template field is filled and the report clears the triage-ready bar.

## Step 6 — Get approval before posting

Show the user the exact destination (repo, channel, labels), the title, and the full body. Filing is public and irreversible-in-spirit — it reaches maintainers and gets indexed. Do not submit until the user approves; apply their edits.

Completion: the user has approved the final text and destination.

## Step 7 — Submit and report back

- Public issue: `gh issue create --repo owner/repo --title … --body-file … [--label …]`, applying the project's labels only if you're confident they're right.
- Alternate channel (Discussions / external tracker / security): follow the destination from Step 2 or `disclosure.md`.

Return the resulting URL. Do not close or edit anyone else's issues.

Completion: the report is filed and you've returned its URL.
