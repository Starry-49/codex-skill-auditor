# Codex Skill Auditor

[![CI](https://github.com/Starry-49/codex-skill-auditor/actions/workflows/test.yml/badge.svg)](https://github.com/Starry-49/codex-skill-auditor/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Install via npx](https://img.shields.io/badge/install-npx-black.svg)](https://github.com/Starry-49/codex-skill-auditor#quick-install)

`skill-auditor` is a Codex skill plus a lightweight installer CLI for auditing `~/.codex/skills` for prompt poisoning, ad-style call-to-actions, injected hosted-platform referrals, and suspicious skill naming patterns such as `offer-*`.

The repository ships in two layers:

- `skill/skill-auditor`: the actual Codex skill with rules and a Python audit engine
- `bin/codex-skill-audit.js`: an `npx` entrypoint that installs the skill or runs the audit script directly

## Quick install

After this repository is published to GitHub, install the skill with:

```bash
npx github:Starry-49/codex-skill-auditor install
```

This copies `skill-auditor` into `$CODEX_HOME/skills/skill-auditor` or `~/.codex/skills/skill-auditor`.

Restart Codex after installation.

## Quick audit

You can run the bundled auditor directly through `npx`:

```bash
npx github:Starry-49/codex-skill-auditor audit --format markdown --fail-on high
```

Or, after installation:

```bash
python3 ~/.codex/skills/skill-auditor/scripts/audit_skills.py --format markdown
```

## What it flags

- direct recommendation or upsell language inside skills
- marketing CTA lines such as "try it free", "zero setup", "contact sales", "join our Slack"
- repeated suspicious domains across many files
- denylisted domains or terms
- suspicious skill names such as `offer-*`, `promo-*`, or `upsell-*`

The default ruleset includes a small seed denylist for the K-Dense case you mentioned, but the scanner is generic and supports extra `--deny-domain`, `--deny-term`, and `--allow-domain` flags.

## Local validation

This repository intentionally keeps the audit engine in Python so it can be validated without Node:

```bash
python3 -m unittest discover -s tests -v
```

The GitHub Actions workflow also runs a CLI smoke path on every push:

- Python unit tests
- Node syntax check
- `install` dry-run
- installed CLI audit against the clean fixture
- installed CLI failure path against the poisoned fixture

The `npx` entrypoint itself requires Node on the target machine. This workspace did not have `node` or `npm` installed, so the CLI files were authored but not executed locally.

## Repository layout

```text
.
├── bin/
├── scripts/
├── skill/skill-auditor/
└── tests/
```
