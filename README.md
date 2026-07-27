# Claude Code plugin bundle

Martin Gauthier's personal [Claude Code](https://docs.anthropic.com/en/docs/claude-code) plugin marketplace. It publishes four locally maintained plugins and an `essentials` bundle that installs them with selected third-party tools.

## Install

The repository is private, so Git must be able to authenticate with GitHub.

Register the third-party marketplaces used by `essentials`, add this marketplace, then install the bundle:

```bash
claude plugin marketplace add mattpocock/skills
claude plugin marketplace add DietrichGebert/ponytail
claude plugin marketplace add gauthiermartin/claude-code-plugin-bundle
claude plugin install essentials@claude-code-plugin-bundle
```

Claude Code's official marketplace supplies the `playwright` dependency. From a local checkout, replace the third marketplace command with:

```bash
claude plugin marketplace add .
```

Install one local plugin without the aggregate bundle using `claude plugin install <name>@claude-code-plugin-bundle`.

## Marketplace plugins

| Plugin | Owner | Purpose |
| --- | --- | --- |
| `essentials` | Martin Gauthier | Aggregate bundle described below |
| `git-skills` | Martin Gauthier | Semantic branch and Conventional Commit workflows |
| `github-skills` | Martin Gauthier | GitHub ruleset administration and upstream issue reporting |
| `obsidian-skills` | Martin Gauthier | Obsidian vault operations and persistent research workflows |
| `youtube-skills` | Martin Gauthier | YouTube transcript extraction and summarization |

## Essentials bundle

`essentials` installs every Martin-authored plugin above plus these third-party dependencies:

| Plugin | Marketplace | Owner |
| --- | --- | --- |
| `mattpocock-skills` | `mattpocock` | Matt Pocock |
| `playwright` | `claude-plugins-official` | Anthropic / Microsoft |
| `ponytail` | `ponytail` | Dietrich Gebert |

The third-party plugins are referenced as dependencies; their source is not copied into this repository.

## Update

```bash
claude plugin marketplace update claude-code-plugin-bundle
claude plugin update essentials@claude-code-plugin-bundle
```

## Repository layout

```text
.claude-plugin/marketplace.json   Marketplace catalog
plugins/essentials/               Aggregate dependency plugin
plugins/git-skills/               Git workflow skill
plugins/github-skills/            GitHub administration skills
plugins/obsidian-skills/          Obsidian and research skills
plugins/youtube-skills/           YouTube transcript skills
```

Each plugin has its own `.claude-plugin/plugin.json`; Claude Code auto-discovers its `skills/` directory.

## Development

Validate the marketplace and every local plugin manifest before pushing:

```bash
claude plugin validate .
```

## Attribution

`obsidian-skills` includes work derived from [iusztinpaul/ai-research-os-workshop](https://github.com/iusztinpaul/ai-research-os-workshop). Its upstream MIT notice is retained in `plugins/obsidian-skills/LICENSE-upstream` and `plugins/obsidian-skills/skills/research/LICENSE-upstream`.

Imported changelogs retain links to their original commits in `gauthiermartin/claude-marketplace`; those links document history and are not installation instructions.
