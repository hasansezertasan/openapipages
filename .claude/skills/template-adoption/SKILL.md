---
name: template-adoption
description: Reconcile an initial copier-pyproject adoption, an update to a newer template version, or a post-update audit against the project's existing behavior. Use for overlapping workflows, Copier conflicts, custom tooling, stale commands, and documentation drift. Repository-settings setup belongs to repo-setup.
---

# Reconcile template adoption and updates

Audit the repository you are in, using its actual Copier answers and history.
Template output is a proposed baseline, not automatic authority over existing
project behavior. Keep project-specific functionality unless the user chooses
to change it. This skill does not require issue filing, commits, pushes, or PRs.

## Establish the baseline

Choose the entry mode from the user's request and repository evidence:

- **Initial adoption:** compare the project before adoption with the rendered
  result. If rendering has not happened, agree on answers and a target version,
  then render into a separate scratch directory for comparison before applying
  changes to the project. Do not overwrite the existing tree blindly.
- **Version update:** record the previous and target template versions and
  compare the update with the project before it. If an update has not happened,
  review new or changed questions before running it; do not silently accept
  defaults that enable dependencies or behavior. Use Copier's update flow for
  an already-adopted project, rather than a new overwrite copy.
- **Post-update audit:** inspect the already-applied update, including committed
  changes. Do not rerun Copier merely to obtain a diff or invent a pre-update
  version from the current answers.

Read repository instructions and `.copier-answers.yml` (`_src_path`, `_commit`,
and feature answers). Inspect working-tree status, staged and unstaged diffs,
untracked files, and relevant history. Identify the pre-adoption/update commit
from history or the user; do not assume it is `HEAD`, `HEAD~1`, or `origin/main`.
Record the baseline commit, prior/target versions, answers, and comparison range.
Read available template release notes and the adoption/update diff, including
added, deleted, and renamed files. Separate template changes from project changes
and user work. If the baseline, release notes, settings, or a version cannot be
retrieved, state what is unavailable and what conclusions remain uncertain.

Preserve existing staged, unstaged, and untracked work. Do not reset, clean,
stash, or restore whole files over it. When user edits overlap reconciliation,
leave those hunks intact and request a decision or a usable baseline.

## Find behavior that needs reconciliation

Inspect conflict markers, unmerged paths, and Copier reject (`.rej`) files,
including in committed update output. Review deletions even when there is no
conflict marker: they can remove project code or custom configuration silently.
Resolve conflicts from the behavior on both sides; do not take all template
config or all project prose wholesale.

Inventory workflows, lint/test/build commands, dependency groups and extras,
Python versions and OS matrices, packaging, release automation, docs, and runtime
entry points. Trace references before calling a config or command obsolete.
Compare the project's previous behavior, its current behavior, and template
defaults, with file/line or commit evidence for each material difference.

Check particularly:

- **Lost check coverage:** inventory every old hook and quality/security job
  before deleting a hook config. Classify each as retained, replaced, missing,
  intentionally omitted, or optional. Record old/new hook IDs or rule sets,
  stages (pre-commit/pre-push/CI), file/type filters, exclusions, dependencies,
  execution environments, suppressions, and feedback timing, with evidence.
  Verify supported IDs and positive/negative file matches against the pinned
  upstream manifest; a similar tool name is not proof of equivalent coverage.
  Ruff UP may replace pyupgrade only for the selected rules/Python target;
  Ruff S and SAST overlap Bandit without proving exact equivalence.
  Local detect-secrets and history-scanning CI gitleaks are complementary.
  CI pip-audit is later feedback than a local pre-push dependency audit;
  check-toml does not replace tox Taplo formatting. Preserve uv-backed local
  basedpyright/slotscheck environments that need project dependencies.
  Keep SQLFluff/djLint project-specific; djLint does not extract embedded HTML
  from Python strings. A local no-commit-to-branch hook requires explicit CI
  skips for legitimate default-branch runs. Preserve generator-owned bytes,
  including cobo-managed `.gitignore`, when introducing fixing hooks.
  Ask before removing a check or accepting reduced coverage/later feedback.
- **Overlapping workflows:** compare events, branch/path filters, schedules,
  manual dispatch, job conditions, permissions, secrets, concurrency,
  dependencies (`needs`), runner platforms, commands, artifacts, and failure
  propagation. Two jobs invoking prek are not necessarily equivalent.
- **Required status checks:** before deleting or renaming a workflow/job,
  inspect check names (including matrix names), aggregate gates, downstream
  references, and repository branch protection and rulesets. Compare local
  `.github/settings.yml` / ruleset definitions with live settings when read
  access is available. Local files alone do not prove the active requirements.
  If live requirements are unavailable, record that gap and defer removal or
  renaming of potentially required checks until the user supplies evidence.
- **Project customizations:** preserve source behavior, meaningful tests,
  coverage expectations, dependency/extra contracts, supported Python/OS
  combinations, package data and wheels, public CLI/API behavior, docs exclusions,
  real project prose, changelog history, and the current release/version state.
  Newly generated skeletons or placeholder tests do not replace real code/tests.
- **Stale tooling and docs:** follow references in mise, tox, prek, pyproject,
  CI, contributor instructions, README, docs, and issue templates. Compare
  examples with actual installed commands and enabled components. Check that
  formatting or lint auto-fixes will not rewrite custom source unexpectedly.

## Obtain consequential decisions

For each consequential change, present the evidence, a recommendation,
alternatives (including keeping the current behavior), and the behavioral
impact. Obtain an explicit user decision before applying it. Use the harness's
native question tool when available; otherwise ask in chat and wait.

This includes removing or merging workflows, changing triggers or required
checks, supported platforms/Python versions, dependencies/extras, test or
coverage scope, packaging or release behavior, and custom functionality.
An authorization to audit is not a decision to discard project behavior.
When answers are pending, continue independent inspection and leave the
dependent changes untouched. Record decisions and any deferred items.

Apply agreed changes with focused edits that preserve user work. Straightforward
mechanical cleanup can proceed without a new decision when equivalence is proven
and it changes no behavior: for example, updating a stale documentation command
to the already-established replacement. If equivalence is uncertain, ask.

Repository-settings changes, credentials, trusted publishing, and App setup
belong to the sibling **repo-setup** skill and `docs/maintaining/setup.rst`.
Use their guidance for setup; do not mutate live settings as audit cleanup.

## Validate and report

Discover the project's validation commands from its instructions and config.
Run relevant lint/type, test, build/package, and docs checks for the changed
surfaces. Inspect auto-fix settings before running tools that write files, then
review the final diff against both the baseline and the starting user edits.
Recheck conflicts, command references, workflow gates, and retained customizations.
Report checks that failed or could not run with reasons; do not call untested
behavior equivalent merely because the files parse or CI is green.

Finish with the baseline and versions, changes applied, decisions made,
customizations retained, validation results, and unresolved tasks or unavailable
evidence. Include any required-status/settings handoff to repo-setup.
Include the per-check coverage classifications, timing changes, evidence for
replacements, and user decisions on genuine gaps; flag unverified equivalence.

## Example: an existing prek workflow

An adopter has `check-prek.yml`; template CI also has a hooks job. Read both
workflows before proposing deletion. Suppose the existing job runs on pull
requests and manual dispatch, while the generated job runs only on pull
requests and pushes, and branch protection requires the old check name.

Recommend keeping the old workflow until its manual path and required check are
accounted for. Offer retaining both, or consolidating while preserving dispatch
and arranging the required-check transition through repo-setup. Show how each
option changes execution and merge requirements, then wait for the user.
If live protection is unreadable, leave removal deferred. After an agreed
consolidation and verified check transition, validate the YAML, event/condition
paths, commands, and gate dependencies; report any execution paths not tested.
The same comparison works before adoption, during an update, or after the update
was merged—the evidence range changes, not the decision rule.
