Repository setup
================

This page is the single home for the **one-time repository setup** the project
author (not contributors) performs so the automated release and maintenance
workflows work. A contributor opening a pull request never touches any of it —
their workflow is in the
`Contributing Guidelines <https://github.com/hasansezertasan/openapipages/blob/main/.github/CONTRIBUTING.md>`_.

Each step is tagged by who performs it:

- **[AGENT]** — a shell command (the `gh CLI <https://cli.github.com/>`_ or
  similar) an automated setup agent can run unattended.
- **[HUMAN]** — browser-only work that cannot be scripted: signing up for a
  service, minting a credential, installing a GitHub App, or a UI-only toggle.

Steps that mint a credential in a browser and then store it are tagged at each
sub-action. Every step can also be applied from the GitHub UI; the ``gh``
commands are the scriptable equivalent.

Merge and pull-request policy
-----------------------------

Squash merging must be the only merge method, with the squash commit message
defaulting to the PR title — that is the only configuration under which the
lint-validated PR title becomes the commit on ``main`` that release-please
reads. Also delete head branches on merge to keep the branch list clean.

**[AGENT]**

.. code-block:: sh

   gh repo edit hasansezertasan/openapipages \
     --enable-squash-merge \
     --enable-merge-commit=false \
     --enable-rebase-merge=false \
     --enable-auto-merge=false \
     --delete-branch-on-merge \
     --squash-merge-commit-message=pr-title

**[CHECK]**

.. code-block:: sh

   gh api repos/hasansezertasan/openapipages \
     --jq '.allow_squash_merge and (.allow_merge_commit | not) and (.allow_rebase_merge | not) and (.allow_auto_merge | not) and .delete_branch_on_merge and (.squash_merge_commit_title == "PR_TITLE")' | grep -qx true

UI equivalent: **Settings → General → Pull Requests** — enable **Allow squash
merging**, disable merge commits and rebase merging, set the squash **"Default
commit message"** to **"Pull request title"**, and enable **Automatically delete
head branches**.

Branch protection
-----------------

Branch protection and rulesets are free on public repositories, but a
**private** repository needs a paid GitHub plan (Pro, Team or Enterprise) for
them to be enforced. On a free-plan private repository mark this section
**not applicable** and skip its commands and checks.
Also defer the Settings App installation below until required code-owner review
can be enforced; its review safeguard depends on branch protection.
Continue with the remaining applicable steps.

This project ships its branch protection as a repository ruleset
(``.github/rulesets/main.json``) applied by the ``ruleset-sync.yml`` workflow on
every push to the default branch. It enforces squash-only merges, linear
history, and the required CI checks; manual edits in the web UI are reverted on
the next push.

**[HUMAN]** Create a ``REPO_ADMIN_TOKEN`` — a fine-grained PAT with
**Administration: read and write** on this repository (the Actions
``GITHUB_TOKEN`` cannot manage rulesets).

**[HUMAN]** Create the ``ruleset-admin`` environment with yourself (or another
admin) as a **required reviewer**, and limit its **deployment branches** to the
default branch (**Settings → Environments → New environment**). The workflow
job runs in this environment, so the PAT is released only after that review —
anyone who can merge a pull request can edit ``ruleset-sync.yml``, but an edited
workflow cannot reach the PAT without the reviewer's approval. Required
reviewers are available on **public** repositories (and on private ones only on
GitHub Enterprise). On a private Free/Pro/Team repository do **not** store the
PAT: skip the secret below, leave ``ruleset-sync.yml`` inert (it exits cleanly
without it) and apply ``.github/rulesets/main.json`` by hand instead.

**[AGENT]** Store the token as a secret of that environment, never as a
repository secret (a repository secret is readable by any workflow edit):

.. code-block:: sh

   gh secret set REPO_ADMIN_TOKEN --env ruleset-admin --repo hasansezertasan/openapipages

**[AGENT]** Trigger the workflow once (push a change under ``.github/rulesets/``
or run it directly):

.. code-block:: sh

   gh workflow run ruleset-sync.yml --repo hasansezertasan/openapipages

**[CHECK]** The ``Protect main`` ruleset is applied and active — verifying the
end state (not just that the ``REPO_ADMIN_TOKEN`` secret exists), so a repo where
``ruleset-sync.yml`` has not yet run, failed, or had its ruleset deleted is
correctly reported as not-done:

.. code-block:: sh

   gh api --paginate repos/hasansezertasan/openapipages/rulesets \
     --jq 'any(.[]; .name == "Protect main" and .enforcement == "active")' | grep -qx true

Until the ``REPO_ADMIN_TOKEN`` environment secret is set the workflow logs a
notice and exits without error, so the repository is never blocked. Each run
waits for the ``ruleset-admin`` reviewer's approval before it applies anything.

.. _setup-first-pr:

Apply protection *after* the first merge
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``check-pr-title.yml``, ``check-branch-name.yml``, ``check-linked-issues.yml``
and ``task-completed-check.yml`` all trigger on ``pull_request_target``, which
GitHub sources from the **base** branch. On a repository adopting this template
``main`` does not have those workflows yet, so the very first pull request — the
one that adds them — reports none of those four contexts and is permanently
blocked by the protection above. (``check`` is unaffected: ``ci.yml`` runs on
plain ``pull_request``, which GitHub sources from the *head* branch.)

So either apply branch protection only *after* the scaffolding has landed on
``main``, or admin-merge that first pull request. From the second PR onwards the
workflows exist on the base branch and every context reports normally.

.. _setup-release-pr-checks:

Release PRs need a manual nudge
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``release.yml`` runs ``release-please`` with the implicit ``GITHUB_TOKEN``, and
**events created with that token do not start workflow runs** — the same rule
that stops a ``release: published`` event from triggering ``gh-pages.yml``. So
the release pull request opens with none of the required contexts reported and
cannot merge on its own. (Renovate PRs are unaffected: Renovate authenticates as
a GitHub App, not as ``GITHUB_TOKEN``.)

This is not a setup step — there is nothing to configure and no ``[CHECK]``.
It is the recurring workaround, recorded here because it is not discoverable
from the workflows themselves: **close and reopen the release pull request.**
Every required context listens for ``reopened``, so reopening it as yourself
fires all of them under your identity. Do not just edit the PR body — that only
re-fires the three ``pull_request_target`` checks that listen for ``edited``,
missing ``check-branch-name.yml`` and ``ci.yml``.

This is a deliberate trade, not an oversight: the alternative is giving
``release.yml`` a PAT or GitHub App token, which is a standing credential with
write access to ``main``. One manual reopen per release is the cheaper side.

.. _setup-release-workflow-race:

Keep workflow changes out of an active release
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

From merging the release PR until the entire **Release** workflow finishes,
pause merges that change ``.github/workflows/``, including Renovate action-pin
updates and automatically merged PRs. Other PRs can still merge during this
window.

The release targets the release PR's merge commit. If a later merge changes
workflows on ``main``, GitHub can refuse to create the tag or release with
``Resource not accessible by integration`` (403). GitHub's `release API
documentation <https://docs.github.com/en/rest/releases/releases#create-a-release>`_
requires workflow write access when the target commit's workflows differ from
the default branch; ``GITHUB_TOKEN`` cannot receive that permission. Increasing
``contents: write`` or simply re-running the job does not repair the mismatch.
The observed tag-creation failure and recovery are recorded in
`copier-pyproject issue #332
<https://github.com/hasansezertasan/copier-pyproject/issues/332>`_.

Recover a release blocked by this mismatch
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Pause further workflow-changing merges and wait for active Release runs to
   stop. In the failed run, identify the release PR's merge SHA and exact tag
   name (including any ``v`` prefix). Check **Releases**, including drafts, and
   the tag before changing either. This procedure is for the workflow mismatch
   above; a 403 alone does not prove that cause.
2. Compare ``.github/workflows/`` at that merge SHA with current ``main``. For
   example, after fetching ``origin``, replace ``RELEASE_COMMIT_SHA`` below:

   .. code-block:: sh

      git fetch origin
      git diff RELEASE_COMMIT_SHA origin/main -- .github/workflows/

3. If the failed run created a tag **but no GitHub Release**, delete only that
   orphan tag before retrying. Replace ``TAG_NAME`` with the exact failed tag:

   .. code-block:: sh

      gh api -X DELETE repos/hasansezertasan/openapipages/git/refs/tags/TAG_NAME

   Skip deletion if the tag is absent. If a draft release already exists, retain
   its tag and release and use **Re-run failed jobs** after restoring the
   workflows. Do not delete a published release or its tag.
4. Revert the intervening workflow changes through the normal PR process so
   ``main``'s workflow contents match the release commit again. Revert only the
   workflow changes if those commits also contain unrelated changes. Repeat
   the diff above against the updated ``origin/main``; it must be empty.
5. Let the Release run triggered by the revert finish, or re-run the failed
   jobs if a draft already exists. Confirm the complete pipeline succeeds,
   including publishing and finalizing the release, before re-applying the
   reverted changes through a PR and resuming workflow-changing merges.

Let Actions open the release PR
-------------------------------

release-please runs as a GitHub Action and opens/maintains the release pull
request, so the repo must allow Actions to create and approve pull requests.

**[AGENT]**

.. code-block:: sh

   gh api -X PUT repos/hasansezertasan/openapipages/actions/permissions/workflow \
     -F default_workflow_permissions=read \
     -F can_approve_pull_request_reviews=true

**[CHECK]**

.. code-block:: sh

   gh api repos/hasansezertasan/openapipages/actions/permissions/workflow \
     --jq '.can_approve_pull_request_reviews == true and .default_workflow_permissions == "read"' | grep -qx true

UI equivalent: **Settings → Actions → General → Workflow permissions** — enable
**Allow GitHub Actions to create and approve pull requests**.

Release immutability
--------------------

Once published, a release's tag and assets can no longer be moved or
overwritten, which protects the integrity of what gets distributed.

**[HUMAN]** Enable it under **Settings → General → ... → Enable release
immutability** (currently a UI-only toggle).

**[CHECK]** No scriptable check — confirm under **Settings → General** that
release immutability is enabled.

Dependency graph
----------------

``dependency-review.yml`` diffs a pull request's dependency manifests against the
base branch and fails it on a newly introduced vulnerable or disallowed-license
dependency. It reads GitHub's dependency graph for the repository; with the graph
off, the action does not pass vacuously — it errors, so the check is red on the
first pull request:

.. code-block:: text

   Dependency review is not supported on this repository.
   Please ensure that Dependency graph is enabled

**[HUMAN]** Enable it under **Settings → Advanced Security** (**Code security and
analysis** on the older settings layout) → **Dependency graph**. UI-only:
``PATCH /repos/{owner}/{repo}`` accepts
``security_and_analysis[dependency_graph][status]`` and silently no-ops, so there
is no ``[AGENT]`` command.

**[CHECK]** Ask the dependency-review API itself — the same endpoint
``dependency-review-action`` calls, so a clean exit here is exactly the state the
workflow needs. It answers ``403`` while the graph is off. A self-compare needs
no second ref, so this works on a repository with nothing merged yet. (Not the
SBOM export, which also tracks the graph but is closing down on 2026-11-13.)

.. code-block:: sh

   gh api --silent \
     repos/hasansezertasan/openapipages/dependency-graph/compare/main...main

PyPI trusted publishing
-----------------------

The release workflow publishes to PyPI via
`trusted publishing <https://docs.pypi.org/trusted-publishers/>`_ (OIDC — no API
tokens or secrets to manage).

**[HUMAN]** Register the publisher once at
`PyPI → Publishing <https://pypi.org/manage/account/publishing/>`_ under
**"Add a new pending publisher"**:

- **PyPI Project Name:** ``openapipages``
- **Owner:** ``hasansezertasan``
- **Repository name:** ``openapipages``
- **Workflow name:** ``release.yml`` — the publish step lives inline in this
  workflow, so this is the filename PyPI's OIDC check matches.
- **Environment name:** ``publish``

**[CHECK]** No scriptable check — confirm the pending publisher is listed at
`PyPI → Publishing <https://pypi.org/manage/account/publishing/>`_.

Restrict the ``publish`` environment to ``main``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``pypi-publish`` job holds ``id-token: write`` against the ``publish``
environment. The ``build`` job uses the same environment while minting build
provenance attestations. Because ``release.yml`` carries ``workflow_dispatch``,
a manual run
executes the workflow file **from the branch you select**, so the
``release_created`` guard inside the file is not a mitigation: anyone with write
access could push a ``release.yml`` with that guard removed to an unprotected
branch, dispatch it, mint a PyPI trusted-publishing token and publish arbitrary
content. Branch protection on ``main`` is never consulted on that path, and
removing the trigger is not an option — ``finalize-release`` re-dispatches this
workflow with ``gh workflow run`` to reconcile the next release PR.

The containment is the environment's **deployment branch policy**, which GitHub
evaluates outside the workflow file, so editing the file cannot bypass it. Do
this before the first release: GitHub auto-creates the environment
**unprotected** on first use, and a repo scaffolded over an existing project may
also be carrying a stale, unreferenced publish environment from its previous
workflow.

**[AGENT]** The branch/tag policies are a *separate collection* — switching the
environment to ``custom_branch_policies`` does not clear whatever is already in
it, and adding ``main`` only appends. A pre-existing wildcard (say ``*``, the
default someone clicks through in the UI) would stay eligible alongside it, so
delete every policy first and re-add exactly one:

.. code-block:: sh

   gh api -X PUT repos/hasansezertasan/openapipages/environments/publish \
     -F 'deployment_branch_policy[protected_branches]=false' \
     -F 'deployment_branch_policy[custom_branch_policies]=true'
   ids="$(gh api --paginate repos/hasansezertasan/openapipages/environments/publish/deployment-branch-policies \
     --jq '.branch_policies[].id')"
   for id in $ids; do
     gh api -X DELETE "repos/hasansezertasan/openapipages/environments/publish/deployment-branch-policies/$id"
   done
   gh api -X POST repos/hasansezertasan/openapipages/environments/publish/deployment-branch-policies \
     -f name=main -f type=branch

Artifact attestations are enabled automatically for public repositories. For a
private or internal repository on GitHub Enterprise Cloud, opt in after
confirming artifact attestations are available:

.. code-block:: sh

   gh variable set ENABLE_PRIVATE_ATTESTATIONS --body true --repo hasansezertasan/openapipages

**[CHECK]** The collection must be *exactly* one branch policy named ``main`` —
asserting only that ``main`` is present would pass with a wildcard sitting next
to it. Compare the *accumulated* lines rather than folding the comparison into
``--jq``: under ``--paginate`` the jq expression runs once **per page**, so a
per-page ``== ["branch:main"]`` prints ``true`` for a final page holding only
``main`` even while an earlier page still carries a wildcard — and a
``grep -qx true`` over that output would accept it. (``--slurp`` is the
documented way to wrap every page into one array, but ``gh`` rejects it
together with ``--jq``.)

.. code-block:: sh

   policies="$(gh api --paginate repos/hasansezertasan/openapipages/environments/publish/deployment-branch-policies \
     --jq '.branch_policies[] | "\(.type // "branch"):\(.name)"')"
   [ "$policies" = "branch:main" ]

UI equivalent: **Settings → Environments → publish → Deployment branches and
tags** — choose **Selected branches and tags**, delete every rule already listed
(including any ``*``), then add ``main``. While you are there, delete any
leftover environment a previous release workflow created.

Coverage reporting (Codecov)
----------------------------

CI uploads coverage to `Codecov <https://about.codecov.io/>`_ after the test
suite runs. **On a public repository no setup is required** — the upload is
tokenless, so owner pushes and fork PRs both report coverage out of the box. A
``CODECOV_TOKEN`` is only needed for a **private** repository (or to avoid
tokenless rate-limits).

**[HUMAN]** (private repos only) Create a repository upload token in the Codecov
dashboard.

**[AGENT]** (private repos only) Store it as a repository secret:

.. code-block:: sh

   gh secret set CODECOV_TOKEN --repo hasansezertasan/openapipages

**[CHECK]** A public repo needs no token; a private repo needs the secret:

.. code-block:: sh

   priv="$(gh repo view hasansezertasan/openapipages --json isPrivate --jq '.isPrivate' 2>/dev/null)"
   if [ "$priv" = "false" ]; then true
   elif [ "$priv" = "true" ]; then
     gh secret list --repo hasansezertasan/openapipages --json name --jq '.[].name' | grep -qx CODECOV_TOKEN
   else false; fi

The upload is best-effort either way: on a private repo with no token CI records
a ``::notice::`` and skips the upload — the build still passes — rather than
failing every run.

Secret scanning (gitleaks)
--------------------------

The ``gitleaks`` job in ``check-security.yml`` scans the full git history for
committed secrets.
`gitleaks-action <https://github.com/gitleaks/gitleaks-action>`_ is **free for
personal accounts and public repositories** with no setup. Only if this
repository lives under a GitHub **organization** does it require a
``GITLEAKS_LICENSE`` — the secret is already wired into the workflow and stays
empty (and unused) otherwise.

**[HUMAN]** (organization-owned repos only) Obtain a license key from
`gitleaks.io <https://gitleaks.io>`_.

**[AGENT]** (organization-owned repos only) Store it as a repository secret:

.. code-block:: sh

   gh secret set GITLEAKS_LICENSE --repo hasansezertasan/openapipages

**[CHECK]** A user-owned repo needs no license; an organization-owned repo needs
the secret:

.. code-block:: sh

   owner="$(gh api repos/hasansezertasan/openapipages --jq '.owner.type' 2>/dev/null)"
   if [ "$owner" = "User" ]; then true
   elif [ "$owner" = "Organization" ]; then
     gh secret list --repo hasansezertasan/openapipages --json name --jq '.[].name' | grep -qx GITLEAKS_LICENSE
   else false; fi

For a personal/public repo this needs no setup and the check passes with no
secret. On an organization repo the ``gitleaks`` job fails until the license
secret is set; ``check-security.yml`` is a standalone security workflow (not part
of the required ``check`` gate), so this does not block merges, but the scan will
not run until it is provided.

Automated dependency updates (Renovate)
---------------------------------------

Dependency bumps — including the ``prek.toml`` hook ``rev``\ s and pinned GitHub
Action digests — are driven by ``.github/renovate.json``, which is read by the
hosted Renovate GitHub App. The config is inert until the app is installed.

**[HUMAN]** Install it once from
`github.com/apps/renovate <https://github.com/apps/renovate>`_ and grant it
access to this repository. Renovate then opens an onboarding PR; merge it to
start receiving update PRs.

**[CHECK]** No scriptable check — confirm the Renovate app is installed and its
onboarding PR merged (`github.com/apps/renovate <https://github.com/apps/renovate>`_).

Template updates (Renovate copier manager)
------------------------------------------

This project was scaffolded from a
`Copier <https://copier.readthedocs.io/>`_ template, and ``.copier-answers.yml``
records the template source (``_src_path``) and the revision it is pinned to
(``_commit``). Renovate's built-in **copier manager** keeps it current: once the
Renovate App (above) is installed, Renovate watches the template repository for
new **version tags**, and when one lands it runs ``copier update`` and opens a
PR with the re-rendered diff — no extra workflow, secret, or token to configure
(Renovate's App credential can update ``.github/workflows/*``, which a plain
``GITHUB_TOKEN`` cannot). This relies on the template publishing tags; if it
only ever pushes to its default branch without tagging, no update PR is
produced.

Review these PRs carefully. ``copier update`` does a 3-way merge, so where your
local edits diverged from the template the diff can contain conflict markers
(``<<<<<<<``) or ``.rej`` files — and Renovate does **not** currently fail its
check on them
(`renovate#31600 <https://github.com/renovatebot/renovate/issues/31600>`_), so a
copier PR can look mergeable while carrying conflicts. Reconcile before merging:
keep your project identity, adopt the template's tooling/config changes.

Where the project maintains an overlay on a file the template also renders
(e.g. project-specific entries in ``.vscode/launch.json`` that the template
cannot derive from its answers), resolve the conflict in favour of the committed
file and port only genuine template-side improvements instead of taking the
template file wholesale. Re-applying the overlay is expected, not a merge
failure.

If the update touches dependency metadata in ``pyproject.toml`` — the
``dependencies`` list, a dependency group, or the optional-dependency table —
also run ``uv lock`` and commit the refreshed ``uv.lock`` in the same PR.
Renovate's copier manager re-renders files but does not re-lock, and CI, the
``prek`` hooks, and the ``mise`` tasks all run ``uv run --locked``, which fails
outright against a stale lockfile.

Check these even when the update runner reports success:

* **Scan for conflicts.** After checkout, run
  ``git grep -nE '^(<<<<<<<|>>>>>>>)'`` and
  ``find . -name '*.rej' -not -path './.git/*'``, and list silent deletions with
  ``git diff --name-only --diff-filter=D <pre-update-commit> HEAD --``.
* **New questions took their defaults.** Diff ``.copier-answers.yml`` against
  the pre-update commit (``git show <pre-update-commit>:.copier-answers.yml``)
  and review every added or changed key before keeping it: a default can enable
  a dependency or a behaviour.
* **Project-owned release state is reset.** An update deletes ``CHANGELOG.md``
  and resets ``.github/release-please-manifest.json`` to ``0.0.0``. Restore both
  from the pre-update commit (``git restore --source=<pre-update-commit> --
  <path>``) and confirm the manifest holds the last released version.
* **Verify the recorded anchor.** After committing the reconciliation, run
  ``uvx copier@latest update --vcs-ref=<_commit> --pretend --defaults`` pinned
  to the ``_commit`` you reconciled to; it must report
  ``Keeping template version``. An unpinned ``--pretend`` selects the latest
  release tag, which is not divergence from the recorded anchor.
* **Retired ai-rulez output.** If the pre-update ``.copier-answers.yml`` has
  ``include_ai_rulez: true``, the update deletes ``.ai-rulez/`` but leaves the
  host files it generated (``CLAUDE.md``, ``.github/copilot-instructions.md``,
  per-host skill copies, ...) behind, next to the newly rendered ``AGENTS.md``.
  Preferably run ``uvx ai-rulez clean --force --keep-gitignore`` *before*
  updating, while the sources still exist. If the update is already checked
  out, restore the sources and clean, then put back the rendered ``AGENTS.md``,
  which ``clean`` also deletes: ``git checkout <pre-update-commit> --
  .ai-rulez && uvx ai-rulez clean --force --keep-gitignore && git rm -rf
  --ignore-unmatch .ai-rulez && git checkout HEAD -- AGENTS.md``. Move any
  guidance kept in the ``.ai-rulez/`` rule sources into ``AGENTS.md``, and drop
  the ``agents`` dependency group from ``pyproject.toml`` if it remains.
* **Never run** ``copier copy --overwrite`` **on an adopted project.** It
  discards every committed reconciliation; use ``copier update`` (``uvx
  copier@latest`` if a ``copier`` shim cannot resolve a version).
* **Leave the merge to a human.** An update PR with no linked issue takes the
  ``no-issue`` label.

Enable GitHub Discussions
-------------------------

New repositories ship with Discussions disabled, but the community-health files
point contributors there — ``SUPPORT.md``, the issue-template chooser
(``config.yml``), and the **Join The Project Team** section of the Contributing
Guidelines all link to the Discussions tab, so those links 404 until it is
turned on.

**[AGENT]**

.. code-block:: sh

   gh api -X PATCH repos/hasansezertasan/openapipages -F has_discussions=true

**[CHECK]**

.. code-block:: sh

   [ "$(gh repo view hasansezertasan/openapipages --json hasDiscussionsEnabled --jq '.hasDiscussionsEnabled')" = "true" ]

UI equivalent: **Settings → General → Features** — tick **Discussions**.

Optional integrations
---------------------

These are enabled in this project's Copier answers and each needs a one-time
external setup. Until set up, they are inert — CI stays green. They are opt-in: a
red ``[CHECK]`` here means "not configured", which is a fine state to leave.

Repository settings ("Settings" App)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``.github/settings.yml`` declares this repository's description, homepage, and
(when the ``repository_topics`` template answer is set) topics. It is applied by
the `Settings GitHub App <https://github.com/apps/settings>`_ on every push to
the default branch. Nothing syncs until it is installed.

Before installing, enforce **Require review from Code Owners** on the default
branch as described below. On a free-plan private repository, **defer the
Settings App** until that safeguard can be enforced. Record this integration
as deferred and skip its installation and check; the metadata file can stay
in the repository without the App.

**[HUMAN]** Confirm that a distinct trusted reviewer with write access can
approve changes authored by the maintainer and is listed in CODEOWNERS for
``.github/settings.yml`` and ``.github/CODEOWNERS``.
A sole maintainer cannot approve their own pull requests;
defer the Settings App until that reviewer is available.

**[HUMAN]** Once that reviewer is available, use GitHub to edit
``.github/rulesets/main.json`` and set the ``pull_request`` rule's
``require_code_owner_review`` to ``true``.
Land this policy change through a reviewed pull request;
``ruleset-sync.yml`` applies it after merge.
The shipped ruleset leaves this flag off so a solo maintainer's ordinary PRs
remain mergeable before this optional integration is configured.
Keep the committed source in sync; an edit only in the ruleset UI is reverted
by the sync workflow.

**[CHECK]** Prerequisite: required code-owner review is enforced on ``main``.
If the check fails or cannot be verified, defer installation and return to that
policy step; a CODEOWNERS file alone does not enforce review.

.. code-block:: sh


   gh api --paginate repos/hasansezertasan/openapipages/rules/branches/main \
     --jq 'any(.[]; .type == "pull_request" and .parameters.require_code_owner_review == true)' | grep -qx true

**[HUMAN]** Only after the prerequisite check passes, install it once on this repository (or your account) from the
`App page <https://github.com/apps/settings>`_.

**[CHECK]** No scriptable check — confirm the Settings GitHub App is installed.

.. caution::

   The Settings App **escalates anyone with push access to admin**: a merge to
   the default branch syncs whatever is in ``settings.yml``. Mitigate this with
   CODEOWNERS — this project already makes ``@hasansezertasan`` the code owner of
   every file (``.github/CODEOWNERS``), so enabling branch protection's **Require
   review from Code Owners** on the default branch means a ``settings.yml``
   change cannot merge without your review. Note that with the shipped
   ``* @hasansezertasan`` ownership this requires code-owner review for *all*
   files (the whole branch); to scope the requirement to just ``settings.yml``,
   narrow ``.github/CODEOWNERS`` to ``/.github/settings.yml @hasansezertasan``.

The "Include in the home page" activity toggles (Releases / Packages /
Deployments in the About sidebar) are **not** settable through any GitHub API,
so neither this App nor any workflow can manage them — set those in the web UI.
Labels are managed separately by ``.github/labels.yml``, not here.

Optional post-launch integrations
---------------------------------

These integrations become useful only after the project has releases, users,
or downstream packaging. They are deliberately not Copier questions: whether
they are appropriate depends on how the individual project develops. Revisit
this list after the first stable releases and add only the integrations whose
prerequisites are met.

GitHub social preview
~~~~~~~~~~~~~~~~~~~~~

A social preview is the image GitHub shows when the repository link is shared
on social media or messaging services. Add one after the project has stable
branding, a representative screenshot, or another visual that will remain
recognizable across releases.

**[HUMAN]** Upload a PNG, JPG, or GIF under **Settings → General → Social
preview**. Keep it under 1 MB. GitHub recommends an image of at least 640×320
pixels and uses 1280×640 pixels for the best display. Keep essential text and
artwork away from the edges, where previews may be cropped.

**[CHECK]** Share the repository URL in a preview-capable service or inspect the
repository settings and confirm that the image remains legible at thumbnail
size.

Repology packaging status
~~~~~~~~~~~~~~~~~~~~~~~~~

`Repology <https://repology.org/>`_ compares the versions of a project shipped
by package repositories and operating-system distributions. Its vertical badge
is useful once Repology recognizes this project in multiple relevant
repositories; a project represented only by PyPI gains little from it.

Before adding the badge, open
``https://repology.org/project/openapipages/versions`` and verify that
Repology matched the correct project, repositories, and versions. Repository
names are normalized, so the Repology project name may differ from
``openapipages``. If it does, use the name shown by Repology in both
URLs below.

Add the badge to ``README.md`` only after that check:

.. code-block:: markdown

   [![Packaging status](https://repology.org/badge/vertical-allrepos/openapipages.svg)](https://repology.org/project/openapipages/versions)

Do not add ``minversion`` merely to mirror the current release. That parameter
means "minimum acceptable version" and should be used only when the project has
a real support or compatibility policy that makes older downstream packages
unacceptable.

Downstream package repositories
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The optional Homebrew tap and Scoop bucket this project dispatches to are
maintainer-owned distribution channels. After the project has stable releases
and user demand, consider submitting it to community-maintained repositories
such as Homebrew core, Scoop's main buckets, Arch, Debian, or Fedora. Each has
its own acceptance, maintenance, and update requirements; do not promise a
channel in ``README.md`` until its package is accepted and installable.

Once downstream packages exist, periodically compare their versions with the
latest PyPI release. Repology can make that comparison visible when it indexes
the repositories involved.

Research archive and DOI
~~~~~~~~~~~~~~~~~~~~~~~~

For software cited in academic or research work, connect the repository to an
archive such as `Zenodo <https://zenodo.org/>`_ after the release process is
stable. Archive a release, add the resulting DOI badge and citation metadata to
``README.md``, and update ``CITATION.cff`` if the archive supplies identifiers
that should be part of the preferred citation. General-purpose applications and
libraries do not need a DOI solely for completeness.

Adopting into an existing project
---------------------------------

This section is reference material, not part of the setup walkthrough: it has
no ``[AGENT]``, ``[HUMAN]`` or ``[CHECK]`` steps. It applies when the template
was copied over an existing or already-published package. The rendered output is
a proposed baseline, not authority over the project's existing behaviour: keep
project-specific functionality unless the owner chooses to change it, and ask
before any consequential change (removing or merging workflows, changing
triggers or required checks, supported Python versions or platforms,
dependencies, test or coverage scope, packaging or release behaviour).

**Set up the baseline first.** Start from a clean tree with all project work
committed, on a dedicated branch. Record the baseline commit, the last
published version, and the exact template tag rendered. Render onto that
committed branch rather than blindly over uncommitted work: the pre-adoption
commit is the baseline, and the job is restoring the project's side from git.
``_src_path`` in ``.copier-answers.yml`` must be a git URL such as
``https://github.com/hasansezertasan/copier-pyproject.git``; the ``gh:``
shorthand stops Renovate's copier manager from resolving template tags, so no
update PR ever opens.

Then reconcile, in this order of likely damage:

* **Gate ruff before running any tool.** ``pyproject.toml`` sets ``fix = true``,
  ``unsafe-fixes = true`` and ``select = ["ALL"]``, so the first ``ruff check``
  or hook run rewrites ``src/**`` in place. Run ``ruff check --diff`` first and
  add ``per-file-ignores`` for deliberate patterns before letting it fix. The
  ``markdownlint-cli2`` config also sets ``"fix": true`` and rewrites every
  Markdown file it discovers.
* **The source skeleton collides with real code.** The template renders
  ``src/openapipages/__init__.py``, ``__main__.py``, ``__metadata__.py``,
  ``core/`` and ``utils/``, plus tests under ``tests/`` that import them.
  Restore the project's own files from the baseline, decide which skeleton
  modules to keep (enabled components read ``core/app.py``), and update the
  tests that import removed ones.
* **Release state starts at zero.** ``.github/release-please-manifest.json``
  renders as ``0.0.0``; set it to the last published version, checked against
  the release history (the nearest git tag can belong to a draft or unrelated
  release). The version stays dynamic: hatch-vcs reads the tag release-please
  cuts.
* **Dependencies the answers enabled.** A zero-dependency library must not gain
  runtime dependencies from a component toggle; compare
  ``[project] dependencies`` with the baseline before keeping any answer.
* **A raised Python floor is a breaking change.** Mark it with a ``feat!:``
  title or a ``BREAKING CHANGE:`` footer so release-please recognises it; the
  ``bump-minor-pre-major`` policy still uses a minor bump before 1.0.
* **Planted prose passes every gate.** Resolve each ``TODO @hasansezertasan:``
  marker one at a time (write, remove or keep), and rewrite the example bodies
  in ``.github/ISSUE_TEMPLATE/``, including the ``openapipages==0.1.0``
  pin, for the project's real surface.
* **Lost check coverage.** Before deleting a hook config or quality job, list
  every old hook and classify it as retained, replaced, missing or intentionally
  omitted, with its stage (pre-commit, pre-push, CI), file filters, exclusions
  and feedback timing. A similar tool name is not proof of equivalent coverage
  (Ruff ``S`` overlaps Bandit without matching it; a CI ``pip-audit`` is later
  feedback than a local pre-push audit). Ask before accepting reduced coverage.
* **Manifest parity (``pyproject.toml``).** Compare table by table, not as one
  diff, since the template reorders tables. Map each removed env-manager entry
  point (Hatch, PDM or nox envs, Makefile targets) to the tox env, ``mise`` task
  or CI step that now runs it. Treat a lower rendered pin as a downgrade, not an
  update. Check that strictness did not narrow (pytest ``strict`` markers,
  ``filterwarnings``, type-checker ``include`` covering tests), that runtime
  ``dependencies`` match the package's real imports, and that keywords, URLs
  and classifiers keep their old values. Trim template leftovers such as
  keywords describing the template, and prove an ignore is unused by rerunning
  the tool before removing it.
* **Overlapping workflows and required checks.** Compare events, branch and path
  filters, schedules, manual dispatch, permissions, secrets and ``needs`` for
  any workflow that does the same job as a shipped one. Before deleting or
  renaming a workflow or job, inspect check names (including matrix names),
  aggregate gates and the live branch protection or ruleset; if live
  requirements are unreadable, defer the removal.
* **Project customisations.** Preserve source behaviour, meaningful tests,
  coverage expectations, supported Python and OS combinations, package data, the
  public CLI and API, docs exclusions, real prose and changelog history.
  Generated skeletons and placeholder tests do not replace real code or tests.

Validate with the project's own lint, type, test, build and docs commands, and
inspect auto-fix settings before running tools that write files. Report any check
that failed or could not run, and do not call untested behaviour equivalent
merely because files parse or CI is green.
