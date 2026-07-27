---
name: repo-manage-rulesets
description: Create GitHub repos and audit/capture/reconcile branch rulesets against the plugin's templates.
disable-model-invocation: true
---

Rulesets are managed GitOps-style. The templates in `${CLAUDE_PLUGIN_ROOT}/skills/repo-manage-rulesets/templates/` are the single source of truth; the gap between a template and a repo's live rulesets is **drift**. Every branch of this skill ends when drift is zero — or, for the read-only branch, fully reported.

Consult [`RULESETS.md`](RULESETS.md) before any `gh api` ruleset call — it holds the endpoints, the normalization rules for diffing, bypass-actor IDs, and plan-tier limits.

## Preflight (every run)

1. `gh auth status` — the token must be able to administer the target repo.
2. Resolve the target repo as `owner/name`: from the user's words, else `gh repo view` in the current directory, else ask.
3. List the available templates from `templates/`.

## Pick a branch

Infer from the user's phrasing; ask only if genuinely ambiguous:

| They say | Branch |
|---|---|
| "new repo", "create", "bootstrap" | Create |
| "save this ruleset", "make this the standard" | Capture |
| "check", "diff", "compliant?", "what's the drift" | Audit |
| "apply", "enforce", "fix the drift" | Reconcile |

## Create

1. `gh repo create <owner>/<name>` with the visibility and options the user asked for.
2. Ask which default-branch template applies — `default-branch-zero-review` (PR gate, no approvals; a solo maintainer cannot approve their own PR) or `default-branch-peer-review` (1 approval, squash-only, linear history) — and whether to add `semantic-branch-names` (branch-name pattern; Enterprise-only, see RULESETS.md). Skip whatever the user already stated.
3. POST the template to the new repo (see RULESETS.md).
4. Inject required status checks per RULESETS.md. A fresh repo with no CI workflows gets no check rule — tell the user this is known drift to close once CI exists.
5. **Done when** an audit of the new repo reports zero drift (or only the recorded no-CI gap).

## Capture

1. Fetch the live ruleset by id.
2. Normalize it: strip server-only fields and any `required_status_checks` rule — check names are repo-specific and templates stay portable.
3. Write it to `templates/<name>.json`. Overwriting an existing template changes the standard for every repo this skill manages — show the diff and confirm first.
4. **Done when** re-auditing the source repo against the new template shows zero drift.

## Audit — read-only, modifies nothing

1. Fetch every live ruleset targeting the default branch (GET each by id — the list endpoint omits rules).
2. Normalize both sides per RULESETS.md and diff against each template.
3. Report drift per ruleset: missing, extra, or changed rules, and bypass-actor differences. List live `required_status_checks` separately as informational — templates deliberately omit them.
4. **Done when** every template and every live default-branch ruleset appears in the report, each marked in-sync or drifted.

## Reconcile

1. Run Audit first and show the full diff.
2. Confirm before every mutation: POST rulesets that are missing, PUT ones that drifted. Never DELETE a live ruleset without showing its full JSON and getting explicit confirmation.
3. Inject required status checks per RULESETS.md.
4. **Done when** a fresh audit reports zero drift.

## Safety rules (all branches)

- Request bodies come from the template file (plus the injected check rule) — never hand-reconstructed JSON.
- Never print tokens or `Authorization` headers.
- A live edit made outside this skill is drift by definition: reconcile it away or capture it into the template — never leave the two silently diverged.
