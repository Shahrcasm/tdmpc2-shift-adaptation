# REPO_SETUP: GitHub repository settings and first push

Owner: **M1** (Md. Shahriar Rakib Rabbi), as part of task **T001** (target Thu 2026-10-22).
Members are identified by slot and name only; no member's GitHub handle is recorded in this repository.
The only GitHub account name that appears is the repository owner's, inside the repository URL
`https://github.com/Shahrcasm/tdmpc2-shift-adaptation.git` used in clone commands (team decision).

Related documents: [AGENTS.md](../AGENTS.md) (rules, ownership table §2, merge protocol §7) ·
[STATUS](STATUS.md) · [RUNS](RUNS.md) (Windows environment, Step 1) · [M1 page, T001 card](team/M1_Shahriar.md#t001).

This page is the checklist for every repository setting and the exact order in which to apply them. Tick
each box when it is done and note the date in the T001 handoff entry on the [M1 page](team/M1_Shahriar.md).

---

## 0. Order of operations (why it matters)

| Step | What | Why this order |
|---|---|---|
| 1 | Account, visibility, description, topics, merge settings, collaborators, Actions, labels (§1–§5) | Independent of any commit. |
| 2 | First commit and push of T001 directly to `main` (§6) | `main` is **not yet protected**, so a direct push is still possible. After protection, every change to `main` needs a reviewed pull request. |
| 3 | Wait for the first CI run of workflow `ci` (§7) | The required check `tests` can only be selected in the branch-protection search box after GitHub has seen it run. |
| 4 | Enable branch protection on `main` with required check `tests` (§8) | Right after CI is green: from here on `main` changes only through reviewed pull requests, including M1's. |
| 5 | Create the three `dev_*` branches from the green `main` and switch to `dev_shahriar` (§9) | Creating branches is not a push to `main`, so it works under protection; every member starts from a commit on which CI passed. |
| 6 | M2 and M3 clone and check out their branches (§11) | Needs the collaborator invitations accepted and the branches pushed. |

---

## 1. Account and visibility

- [ ] **Owner:** the repository lives on M1's personal GitHub account (it already exists; do not transfer it).
- [ ] **Visibility:** **private** until the course is graded (made public afterwards, §12).
- [ ] **GitHub Student Developer Pack (only because the repository is private):** M1 applies for the free
      Student Developer Pack, which includes GitHub Pro. Protected branches on a *private* repository owned by
      a personal account require Pro (or Team); on a *public* repository protection is free.
      <!-- VERIFY: at setup time, confirm on GitHub's current plans page that branch protection on private personal-account repositories still requires GitHub Pro, and that the Student Developer Pack still includes Pro (resolves in T001, M1). -->
      If the Pack is not yet approved when §8 is reached, skip §8, do §9 and §11, record "protection pending
      (Pack)" in the T001 handoff entry, and apply §8 the day Pro becomes active. Until then nobody pushes to `main`
      directly; changes still go through pull requests by convention.
- [ ] **License:** do **not** add a license through the GitHub UI. The MIT `LICENSE` is part of the T001
      commit. If GitHub created an initial commit containing a README or license, keep that commit; the T001
      commit overwrites those files. Upstream's MIT license stays at `third_party/tdmpc2/LICENSE`.

## 2. "About" box: description and topics

On the repository's main page, click the gear icon next to **About**.

- [ ] **Description:** replace "~96-parameter" with **"64-number"**. Use:

      ```text
      Can a 64-number embedding update fix a world model under dynamics shift? Shift detection + test-time adaptation for TD-MPC2 on DMControl.
      ```

      Reason: for our checkpoints `mt30-5M` and `mt30-19M` the task embedding is 64-dimensional
      (dim(e)=64 for mt30-5M/19M per upstream `third_party/tdmpc2/tdmpc2/common/parser.py`; 96 for mt80 and
      for the 1M/317M models). That line reads
      `cfg.task_dim = 96 if cfg.task == 'mt80' or cfg.get('model_size', 5) in {1, 317} else 64`. C2 adapts one row of the
      embedding table, i.e. 64 numbers. This closes the open correction in [STATUS §4](STATUS.md).
- [ ] **Topics** (exactly these six): `reinforcement-learning`, `model-based-rl`, `world-models`, `tdmpc2`,
      `test-time-adaptation`, `mujoco`.
- [ ] Leave "Website" empty. Packages, releases and deployments can stay hidden.

## 3. Merge settings

**Settings → General → Pull Requests:**

- [ ] **Allow merge commits:** on.
- [ ] **Allow squash merging:** off.
- [ ] **Allow rebase merging:** off.
- [ ] **Automatically delete head branches:** off.

Reason: the `dev_*` branches are long-lived and are merged into `main` many times. A squash or rebase merge
rewrites the branch's commits on `main`, so every later PR from the same branch would show the old commits
again. Merging with "Create a merge commit" avoids this. Auto-deletion would delete a `dev_*` branch
after its first merge.

## 4. Collaborators

**Settings → Collaborators → Add people:**

- [ ] Invite **M2 (Md. Ishtiak Ahmed Moyen)** with write access.
- [ ] Invite **M3 (Md. Abdullah Talha)** with write access.
- [ ] Both invitations are **accepted** (each member opens the invitation email or the GitHub
      notifications page). Until they accept, they cannot clone the private repository or push.

On a repository owned by a personal account, collaborators get read and write access without a role
selector. <!-- VERIFY: confirm on the Collaborators page that personal-account collaborators receive write (push) access and that no role choice is offered (resolves in T001, M1). -->
Do **not** record anybody's GitHub handle in any file, commit message, issue or PR body. Refer to people as
"M2 (Md. Ishtiak Ahmed Moyen)" etc.

## 5. Actions, secrets, LFS, labels

- [ ] **Actions enabled:** Settings → Actions → General → allow actions, so that the workflow can use
      `actions/checkout` and `actions/setup-python` (see `.github/workflows/ci.yml`).
- [ ] **Actions minutes:** private repositories have a monthly Actions minutes quota, and the
      `windows-latest` leg consumes quota faster than the Linux leg. Check the quota once under the account's
      Billing and plans page.
      <!-- VERIFY: current Actions minutes included for a private repository under GitHub Pro, and the Windows-runner multiplier (resolves in T001, M1; record the result in the T001 handoff entry, not as a number in this file). -->
- [ ] **No secrets:** Settings → Secrets and variables → Actions has **no** repository secrets and none are
      needed (`ci.yml` declares `permissions: contents: read` and downloads no checkpoint; the smoke test in CI
      uses `--mode tiny`). Never commit Hugging Face or Google tokens, `.env` files, or Drive paths that contain
      personal email addresses ([AGENTS.md §4](../AGENTS.md)).
- [ ] **No Git LFS:** do not enable or install LFS tracking. `.gitattributes` must contain no `filter=lfs`
      line. Checkpoints live in the shared Google Drive folder `DA-TDMPC2/checkpoints/` and on each laptop in
      the gitignored `checkpoints/` (only `checkpoints/MANIFEST.csv` is committed, T005). Check with:

      ```powershell
      Select-String -Path .gitattributes -Pattern "filter=lfs"
      ```

      (no output = correct).
- [ ] **Labels:** Issues → Labels → **New label** `task` (used by `.github/ISSUE_TEMPLATE/task.md`). The label
      `bug` (used by `.github/ISSUE_TEMPLATE/bug.md`) is one of GitHub's default labels; create it if it is
      missing.

## 6. T001 commit and first push to `main` (before protection)

Prerequisites: Git for Windows installed; the repository is cloned (team-standard path
`C:\code\tdmpc2-shift-adaptation`); the TD-MPC2 paper PDF and the project proposal PDF have been copied
into `docs/references/` by hand; all generated files have been reviewed.

Run in PowerShell, one command per line (Windows PowerShell 5.1 has no `&&`):

```powershell
cd C:\code\tdmpc2-shift-adaptation
git status --short
git add -A
git status --short
git ls-files | Where-Object { (Get-Item -LiteralPath $_).Length -gt 5MB }
git grep -n --cached "github.com/" -- . ":(exclude)third_party"
git commit -m "T001: bootstrap documentation and repo scaffolding"
git push -u origin main
```

Before `git commit`, check the output of the three inspection commands:

- [ ] `git status --short` lists no `*.pt`, no file under `checkpoints/` other than `MANIFEST.csv`, no
      `outputs/`, `logs/`, `videos/`, `wandb/`, `.env`, `__pycache__/`, `.pytest_cache/` or `*.egg-info/`
      (all are in `.gitignore`).
- [ ] The size command prints **nothing** (no tracked file larger than 5 MB, including the reference PDFs).
      If a PDF is larger, leave it out of the commit and keep it in the shared Drive folder instead.
- [ ] Every line printed by `git grep` is either the repository URL
      `https://github.com/Shahrcasm/tdmpc2-shift-adaptation.git` (allowed by team decision) or an
      upstream/third-party URL (e.g. `nicklashansen`). No other GitHub account name may appear; remove it
      before committing.

The first push goes to an **unprotected** `main`; this is intended and happens only once.

## 7. Wait for the first CI run

- [ ] Open the **Actions** tab. The push starts workflow **`ci`** with three jobs:
      `test-matrix (ubuntu-latest)`, `test-matrix (windows-latest)` and the aggregator **`tests`**.
- [ ] All three jobs are green on `main`.

Why there is an aggregator job: a matrix job reports one check per operating system, named
`test-matrix (<os>)`, and never a single check called `tests`. The job `tests` in `.github/workflows/ci.yml`
(`needs: test-matrix`, `if: always()`) fails unless every matrix leg succeeded, so it is the one check that
branch protection requires (§8). The GitHub UI may display it as `ci / tests`.

If CI is red: fix it on `main` with a follow-up commit `T001: fix CI <what>` and push again (still allowed
because protection is not on yet). Repeat until green, then continue.

## 8. Branch protection on `main`

**Settings → Branches → Add classic branch protection rule**, branch name pattern `main`:

- [ ] **Require a pull request before merging:** on.
  - [ ] **Require approvals:** on, **1** approval. This applies to the PRs of M2 and M3, which M1 approves
        and merges. M1 merges his own PRs from `dev_shahriar` (including `T000: sync status`) **without another
        member's approval**, using the repository owner's bypass enabled below. Only M1 ever clicks Merge
        ([AGENTS.md §7](../AGENTS.md)). This is a team rule: on a personal-account repository GitHub settings
        cannot restrict who may merge.
        <!-- VERIFY: GitHub "restrict who can push / merge" availability for personal-account repositories (resolves in T001, M1). -->
- [ ] **Require status checks to pass before merging:** on. In the search box type **`tests`** and select the
      check from GitHub Actions (it may be shown as `ci / tests`). Do **not** select the two
      `test-matrix (...)` checks; `tests` already aggregates them.
  - If `tests` does not appear in the search box, CI has not run yet (or not recently): go back to §7, run
    the workflow again (Actions → `ci` → **Run workflow** on `main`, enabled by `workflow_dispatch`), wait
    until it finishes, then search again.
  - "Require branches to be up to date before merging": leave **off** (not part of our policy; members
    merge `origin/main` into their branch at the start of every session, [AGENTS.md §3](../AGENTS.md)).
- [ ] **Do not allow bypassing the above settings** (older UI label: **Include administrators**): **off**.
      This lets M1, as repository owner, merge his own PRs without an approval: on his own PR the merge box
      offers a bypass option. Team rules for using it: M1 bypasses **only the approval**, merges only when the
      CI check `tests` is green, always through a PR from `dev_shahriar`, and never pushes directly to `main`.
      <!-- VERIFY: exact label of the owner/admin bypass option in the merge box of the current GitHub UI (resolves in T001, M1). -->
- [ ] **Allow force pushes:** off.
- [ ] **Allow deletions:** off.
- [ ] **Save changes.**

<!-- VERIFY: the setting labels above match the current GitHub UI (classic branch protection; GitHub also offers "rulesets", which can express the same rule). If the labels differ, apply the same five requirements and update this list (resolves in T001, M1). -->

No `CODEOWNERS` file is used, because GitHub handles are not recorded. File ownership is enforced by the
integrator's review checklist ([AGENTS.md §7](../AGENTS.md)), which compares
`git diff --name-only "origin/main...origin/<branch>"` with the ownership table in [AGENTS.md §2](../AGENTS.md).

Consequence: after this step M2 and M3 cannot push to `main`, and M1 (who technically could, as owner) does
not by team rule. All three members work only on their own `dev_*` branch. Status syncs
(`T000: sync status`) are a commit on `dev_shahriar` that reaches `main` through a PR that M1 merges once CI
is green, as described in [AGENTS.md §7](../AGENTS.md).

## 9. Create the three `dev_*` branches

From the green, now-protected `main`, one command per line (creating a branch is not a push to `main`):

```powershell
cd C:\code\tdmpc2-shift-adaptation
git checkout main
git pull origin main
git checkout -b dev_shahriar main
git push -u origin dev_shahriar
git checkout -b dev_ishtiak main
git push -u origin dev_ishtiak
git checkout -b dev_talha main
git push -u origin dev_talha
git checkout dev_shahriar
git ls-remote --heads origin
```

- [ ] `git ls-remote --heads origin` lists `main`, `dev_shahriar`, `dev_ishtiak`, `dev_talha`.
- [ ] Your working copy is on `dev_shahriar` (`git branch --show-current`).

CI does not run on pushes to `dev_*` branches (`ci.yml` triggers on pushes to `main`, on pull requests to
`main`, and manually); it runs on every pull request to `main`, so open your PR early to get CI feedback.
From now on M1 works only on `dev_shahriar` ([AGENTS.md §3](../AGENTS.md), start-of-session protocol).

## 10. Verification

- [ ] Settings → Branches shows the rule for `main` with the items of §8.
- [ ] On the first pull request (e.g. T002 from `dev_shahriar`), the merge box shows the required check
      `tests` and "Review required" before approval, and the merge button offers only **Create a merge commit**.
- [ ] The M1 T001 card's "Done when" items about branches, protection, merge settings, collaborators and the
      repository description are ticked ([M1 page](team/M1_Shahriar.md#t001)).

## 11. M2 and M3: clone to `C:\code` and check out your branch

Prerequisites: the collaborator invitation is accepted (§4); Git for Windows is installed
([RUNS](RUNS.md), Step 1). On the first clone of the private repository, Git Credential Manager (included in
Git for Windows) asks you to sign in to GitHub in the browser.

**M2 (Md. Ishtiak Ahmed Moyen), branch `dev_ishtiak`:**

```powershell
git config --global core.longpaths true
git config --global user.name "Md. Ishtiak Ahmed Moyen"
git config --global user.email "<email address registered on your GitHub account>"
New-Item -ItemType Directory -Force -Path C:\code
git clone https://github.com/Shahrcasm/tdmpc2-shift-adaptation.git C:\code\tdmpc2-shift-adaptation
cd C:\code\tdmpc2-shift-adaptation
git checkout dev_ishtiak
git branch -vv
```

**M3 (Md. Abdullah Talha), branch `dev_talha`:**

```powershell
git config --global core.longpaths true
git config --global user.name "Md. Abdullah Talha"
git config --global user.email "<email address registered on your GitHub account>"
New-Item -ItemType Directory -Force -Path C:\code
git clone https://github.com/Shahrcasm/tdmpc2-shift-adaptation.git C:\code\tdmpc2-shift-adaptation
cd C:\code\tdmpc2-shift-adaptation
git checkout dev_talha
git branch -vv
```

- [ ] `git checkout dev_<name>` creates a local branch that tracks `origin/dev_<name>`; `git branch -vv` shows
      `[origin/dev_ishtiak]` (M2) or `[origin/dev_talha]` (M3) next to the current branch (marked `*`).
- [ ] The clone is at `C:\code\tdmpc2-shift-adaptation`, not inside OneDrive, Documents or Desktop.
- [ ] Never commit on a local `main`. All work happens on your own `dev_*` branch and reaches `main` only
      through a pull request ([AGENTS.md §6](../AGENTS.md)).

Then continue with the environment setup in your task card: T003 ([M2 page](team/M2_Ishtiak.md#t003)) or
T004 ([M3 page](team/M3_Talha.md#t004)), following [RUNS](RUNS.md) Step 1.

## 12. After the course is graded

- [ ] Settings → General → Danger Zone → **Change visibility** → public.
- [ ] Our code stays under MIT (`LICENSE`); upstream's MIT license stays in `third_party/tdmpc2/LICENSE`.
- [ ] Before switching, check that no member handle, token or personal Drive path becomes public (the
      repository URL `https://github.com/Shahrcasm/tdmpc2-shift-adaptation.git` and upstream URLs are expected
      matches). The first command
      searches the current files; the second lists every commit in the history that added or removed a line
      containing the pattern (inspect each with `git show <sha>`):

      ```powershell
      git grep -n "github.com/" -- . ":(exclude)third_party"
      git log --all --oneline -G "github.com/" -- . ":(exclude)third_party"
      ```

      Repeat both commands with the pattern `token` and with `drive.google.com`. A secret found anywhere in the
      history must be revoked at its provider before the repository is made public.
