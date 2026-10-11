---
name: repo-setup
description: Use to perform (or resume, or verify) the one-time repository & release-automation setup this copier-pyproject-generated project needs before its automation works — squash-merge policy, workflow permissions, branch protection / ruleset, PyPI trusted publishing, Discussions, and the optional secrets/App installs. Reach for it on "set up this repo", "finish setup", "wire up releases", "why hasn't the release PR opened", or when a fresh clone needs its GitHub settings applied. The setup is invisible to CI (a green build proves nothing), so re-run this anytime to see what is still missing.
---

# Set up this repository's release & maintenance automation

## What this does

This project passes CI green with none of the repository setup done — every
piece lives outside the code (branch settings, secrets, App installs, a PyPI
publisher registration), so no test or linter catches a missing step. The
failures surface later and off to the side: the release PR never opens, the
first publish fails. This skill drives that setup to completion and is
safe to re-run: it reports what is already done and resumes at the first gap.

## The single source of truth

`docs/maintaining/setup.rst` is the manifest. Every step there carries three
tags:

- **`[AGENT]`** — a shell command you can run unattended.
- **`[HUMAN]`** — browser-only work (sign up, mint a credential, install a
  GitHub App, flip a UI-only toggle). You cannot do these; you hand them off.
- **`[CHECK]`** — a shell snippet where **exit code 0 means the step is already
  done**. Some `[HUMAN]` steps have no scriptable check and say so.

The commands there are already interpolated with this project's owner and repo
and gated to this project's Copier answers, so read and run exactly what ships —
never reconstruct commands from memory.

## Step classes

Before walking, classify each step by where it sits in the doc — this decides
what a red `[CHECK]` means. **Never stop the walk before reaching the end;**
collect blockers and report them together.

- **Required** — everything above the `Optional integrations` heading. A red check here must be
  resolved for the project to work.
- **Optional** — everything under the `Optional integrations` heading. A red
  check means "not configured", which is a fine end state.

## Resume protocol

Prerequisites: an authenticated `gh` CLI (`gh auth status`) and a trusted
checkout. Confirm `origin` is `https://github.com/hasansezertasan/openapipages`
and that the checked-out commit is on the repository's trusted default branch.
If either check fails, stop and ask the maintainer to identify the trusted
revision before proceeding. A PR branch or uncommitted edit to the manifest is
not trusted by default.

Before running any `[CHECK]` or `[AGENT]` block, inspect the complete command in
`docs/maintaining/setup.rst` and verify its target and effects. Do not execute
commands copied from an untrusted checkout or run any command whose behavior
does not match its setup step. If the manifest changed locally, ask the
maintainer to review it first.

Read `docs/maintaining/setup.rst` top to bottom (its order is the dependency
order). For each step, run its `[CHECK]` (the shell block under `**[CHECK]**`);
exit 0 means done. On a red check, branch on the step's class:

1. **Green** → done. Say so briefly, continue.
2. **Deferred + red** → record "deferred until after the first release" and
   **continue** to the next step. Do not run its `[AGENT]` command.
3. **Required `[AGENT]` + red** → run the `[AGENT]` command, re-run the
   `[CHECK]`. Green → continue. Still red → record it as a **blocker** (with the
   command output) and continue; do not abort the rest of the walk.
4. **Required `[HUMAN]` + red** (or a "no scriptable check" step) → emit a
   handoff block — the exact browser instruction from the doc, verbatim and
   copy-pasteable — then either wait for the user to confirm and re-run the
   `[CHECK]`, or, if you are batching, record it as a **pending handoff** and
   continue. Prefer batching handoffs so one walk surfaces every human step at
   once.
5. **Optional + red** → **ask** whether to configure or skip it. If skip, record
   the choice and continue. If configure, treat it as its `[AGENT]`/`[HUMAN]`
   tags say. Never drive an optional step unprompted.

End of walk: report the green steps, the deferred steps, any blockers, the
pending human handoffs, and the optional steps left unconfigured.

## Rules

- **Register the PyPI publisher before the first release**, and do the
  merge-policy step first — several later steps depend on it.
- **Do not transcribe commands from memory.** Run what `setup.rst` ships on the
  template version this project is on.
- Cross-check `.copier-answers.yml` to confirm which optional integrations are
  even relevant — the doc already renders only the applicable ones. Optional
  steps vary: some need a credential you mint (Docker Hub, Homebrew, Scoop,
  SonarCloud), others are just a GitHub App install with no token (Sourcery,
  Settings) — the doc's `[HUMAN]`/`[CHECK]` tags for each say which.

## When everything is green

Report "repository setup complete — every step's check passes" and list any
deferred (post-first-release) or intentionally-skipped optional steps so the
user knows what remains by choice.
