# Ruleset API reference

## Endpoints (repository rulesets)

- List: `gh api repos/{owner}/{repo}/rulesets` — returns summaries only; `rules` and `bypass_actors` are absent. Always GET by id before diffing.
- Get: `gh api repos/{owner}/{repo}/rulesets/{id}`
- Create: `gh api -X POST repos/{owner}/{repo}/rulesets --input <file>`
- Update: `gh api -X PUT repos/{owner}/{repo}/rulesets/{id} --input <file>`
- Delete: `gh api -X DELETE repos/{owner}/{repo}/rulesets/{id}`

Organization rulesets (`orgs/{org}/rulesets`) are out of scope for this skill.

## Normalization before any diff or capture

Strip the server-added fields:

```sh
jq 'del(.id, .source, .source_type, .created_at, .updated_at, .node_id, ._links, .current_user_can_bypass)'
```

Then sort `rules` by `.type` and `bypass_actors` by `.actor_id` on both sides — the API does not guarantee order, and an order-only diff is false drift.

## Bypass actors

| actor_type | actor_id | Meaning |
|---|---|---|
| RepositoryRole | 5 | Repository admin |
| RepositoryRole | 4 | Maintain |
| RepositoryRole | 2 | Write |
| Integration | the App's integration id | A GitHub App |
| Team | team id | An org team |
| OrganizationAdmin | 1 | Org admins |

`bypass_mode` is `always` (bypasses direct pushes too) or `pull_request` (bypass only via PR).

Release-bot note: a fine-grained PAT authenticates as its human owner, so an admin's PAT is already covered by the `RepositoryRole 5` bypass in both templates. If release automation moves to a GitHub App, replace that entry with `{ "actor_id": <integration id>, "actor_type": "Integration", "bypass_mode": "always" }` — the id comes from `gh api /apps/{app-slug} --jq .id`.

## Injecting required status checks (apply time)

Templates carry no `required_status_checks` rule because check names are repo-specific — requiring a check that never reports blocks every merge to the branch.

1. Enumerate candidate names from what actually ran, not from memory:
   `gh api repos/{owner}/{repo}/commits/{default_branch}/check-runs --jq '.check_runs[].name' | sort -u`
   (Fallback for a repo with no runs yet: job `name:` values in `.github/workflows/*.yml`; a job without `name:` reports as its YAML key.)
2. Ask the user which checks to require (AskUserQuestion).
3. Append to the template-derived request body:

```json
{
  "type": "required_status_checks",
  "parameters": {
    "strict_required_status_checks_policy": false,
    "required_status_checks": [{ "context": "<exact check name>" }]
  }
}
```

The `context` must match the reported check name exactly.

## Plan-tier limits

- Metadata rules (`commit_message_pattern`, `commit_author_email_pattern`, `branch_name_pattern`, …) are **Enterprise-only** — this includes the whole `semantic-branch-names` template. Applying it on Free/Pro/Team fails at the API; on those plans, enforce conventional commits in CI (commitlint) and require that check instead.
- Rulesets on **private** repos need Pro/Team/Enterprise; public repos get them on every plan.
