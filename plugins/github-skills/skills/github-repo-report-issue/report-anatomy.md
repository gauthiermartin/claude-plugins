# Report Anatomy

Use the repo's own template when it has one — this is the fallback and the quality bar.

## What triage-ready means

A maintainer reading it can reproduce, or decide, without asking you anything. That means:

- **Specific title** — the symptom plus where, not "bug" or "doesn't work". A maintainer should be able to guess the area from the title alone.
- **Version/commit** — exact release or commit SHA, not "latest".
- **Environment** — OS, runtime/language version, and any config that matters.
- **Minimal repro** — the fewest steps or smallest snippet that triggers it. Cut everything not needed to reproduce.
- **Expected vs actual** — both stated plainly. "Expected X, got Y."
- **Evidence** — the error, stack trace, or output, in a fenced block.
- **Scope, not solution** — describe the problem precisely; a proposed fix is welcome but optional and clearly marked as a suggestion.

## Default bug template

```markdown
### Summary
<one sentence: the symptom and where it happens>

### Version / commit
<release tag or commit SHA>

### Environment
- OS:
- Runtime/version:
- Relevant config:

### Steps to reproduce
1.
2.
3.

### Expected
<what should happen>

### Actual
<what happens instead>

<paste the error / stack trace / output>

### Proposed fix (optional)
<only if you have a concrete one; mark it as a suggestion>
```

## Default feature-request template

```markdown
### Problem
<the concrete current-state limitation, verified against current code>

### Why it matters
<who hits it and how often>

### Proposed direction (optional)
<a sketch, not a demand — leave design room for maintainers>

### Alternatives considered
<workarounds you tried and why they fall short>
```

## Etiquette

- One issue per problem. Don't bundle unrelated findings.
- Match the project's tone from `CONTRIBUTING`; skip labels unless you're confident they're the project's conventions.
- Credit prior art: link the related/closed issues you found while deduping.
