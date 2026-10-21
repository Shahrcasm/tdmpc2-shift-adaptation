# M1 — Md. Shahriar Rakib Rabbi

> Only M1 edits this page. Statuses, handoff entries and compute use recorded here are copied into
> [STATUS](../STATUS.md) by M1 at merge time (`T000: sync status`). Rules: [AGENTS.md](../../AGENTS.md).
> Science, hypotheses and metrics: [PROJECT_PLAN](../PROJECT_PLAN.md). Commands and environment:
> [RUNS](../RUNS.md).

| Field | Value |
|---|---|
| Name | Md. Shahriar Rakib Rabbi |
| Slot · Student ID | M1 · 2321937642 |
| Branch | `dev_shahriar` |
| Role | **Integrator** (the only member who merges PRs into `main`: reviews, approves and merges M2/M3 PRs, and merges my own PRs from `dev_shahriar` without another approval, only when CI `tests` is green) · infrastructure · evaluation harness · perturbation suite · nominal evaluation · ranking-fidelity diagnostic · closed loop · C1 design (stretch) · figures · report assembly |
| Components | Upstream bridge (`_upstream.py`), single-task-of-multitask harness + resume-safe logging (T006), checkpoint fetching (T005), shift wrappers and shift configuration (T101, T102), nominal evaluation of both checkpoints and study-task selection (T007), ranking-fidelity diagnostic nominal vs shifted (T104) and after adaptation (T205), closed-loop detect→adapt (T304), C1 design note and, only if G2 passes by 2026-11-17, the ranking-loss pilot (T401, T402/T403), registry + figures (T501), report skeleton and assembly (T502, T504) |
| Laptop | Native Windows 11 (edition/version/build recorded in [Record: my laptop](#record-my-laptop), T002); Python 3.11 venv (`.venv`); PowerShell 5.1; repo at `C:\code\tdmpc2-shift-adaptation` |
| Colab account | M1 (one of the three parallel accounts) |

**Strictly owned files** (binding table: [AGENTS.md §2](../../AGENTS.md)); I edit nothing else:

- Root: `AGENTS.md`, `CLAUDE.md`, `README.md`, `LICENSE`, `.gitignore`, `.gitattributes`, `pyproject.toml`
- `.github/**`, `.cursor/rules/agents.mdc`, `environment/requirements-cpu.txt`, `environment/requirements-colab.txt`
- `third_party/tdmpc2/**` (read-only for everyone, including me; re-vendoring only in a dedicated PR)
- `src/datdmpc/__init__.py`, `src/datdmpc/_upstream.py`, `src/datdmpc/envs/**`, `src/datdmpc/eval/**`, `src/datdmpc/diagnostics/**`, `src/datdmpc/ranking/**` (stretch, C1), `src/datdmpc/closed_loop.py`
- `configs/shifts.yaml`, `configs/experiments/M1_*.yaml`
- `scripts/get_checkpoints.py`, `scripts/smoke_test.py`, `scripts/eval.py`, `scripts/build_registry.py`, `scripts/make_figures.py`
- `notebooks/colab/M1_*.ipynb`
- `tests/conftest.py`, `tests/test_upstream_bridge.py`, `tests/test_smoke.py`, `tests/test_get_checkpoints.py`, `tests/test_perturb.py`, `tests/test_harness.py`, `tests/test_logging.py`, `tests/test_registry.py`, `tests/test_closed_loop.py`, `tests/test_ranking_fidelity.py`, `tests/test_ranking.py`
- `results/P0_nominal/**` (T007), `results/P1_ranking/**` (T104), `results/P2_ranking_after_adapt/**` (T205), `results/P3_closedloop/**` (T304); generated: `results/REGISTRY.csv`, `figures/**`
- `report/main.tex`, `report/sections/*_M1.tex`
- `docs/STATUS.md`, `docs/PROJECT_PLAN.md`, `docs/RUNS.md`, `docs/REPO_SETUP.md`, `docs/design/C1_ranking.md` (T401), `docs/team/M1_Shahriar.md`, `docs/references/**`
- `checkpoints/MANIFEST.csv` (everything else in `checkpoints/` is gitignored)

The T001 stubs for M2- and M3-owned modules and scripts belong to their owners from the moment the
`dev_*` branches exist; I do not edit them after that.

---

## My Tasks

Status values: To Do / In Progress / Done / Blocked. "Depends on" tasks must be Done in
[STATUS](../STATUS.md) before I start.

| ID | Task | Depends on | Target date | Status |
|---|---|---|---|---|
| [T001](#t001) | Repo scaffolding, vendored upstream at pinned SHA, all docs + `.github/` files | — | Thu 2026-10-22 | In Progress |
| [T002](#t002) | Windows env setup (Python 3.11 venv) + smoke test on own laptop; record Windows version | T001 | Fri 2026-10-23 | Done |
| [T005](#t005) | `scripts/get_checkpoints.py` + `checkpoints/MANIFEST.csv`; upload to shared Drive | T002 | Sat 2026-10-24 | To Do |
| [T006](#t006) | Single-task-of-multitask evaluation harness + resume-safe logging + tests | T005 | Mon 2026-10-26 | To Do |
| [T101](#t101) | Perturbation wrappers + tests proving the physical parameter changed | T002 | Thu 2026-10-29 | To Do |
| [T007](#t007) | Nominal eval of mt30-5M and mt30-19M on all 30 tasks (Colab, sharded) → `results/P0_nominal/`; study-task selection rule written before any shifted result | T006, T003 | Fri 2026-10-30 | To Do |
| [T102](#t102) | `configs/shifts.yaml`: types × levels; dev vs held-out test split | T101, T007 | Sat 2026-10-31 | To Do |
| [T104](#t104) | Ranking-fidelity diagnostic, nominal vs shifted → `results/P1_ranking/` | T006, T101 | Tue 2026-11-03 | To Do |
| [T501](#t501) | `build_registry.py` + `make_figures.py` (read `results/` only) | T103 | Tue 2026-11-10 | To Do |
| [T502](#t502) | Report skeleton; M2/M3 write own `report/sections/*_<owner>.tex` from week 4 | T501 | Thu 2026-11-12 | To Do |
| [T205](#t205) | Ranking fidelity after C2 adaptation → `results/P2_ranking_after_adapt/` | T104, T202 | Fri 2026-11-27 | To Do |
| [T304](#t304) | Closed-loop detect→adapt evaluation → `results/P3_closedloop/` | T303, T204 | Tue 2026-12-01 | To Do |
| [T401](#t401) | C1 design note + differentiation vs TD-GRPC/BMPC/TD-M(PC)² (pilot T402/T403 only if G2 passed by Nov 17) | T104 | Wed 2026-12-02 | To Do |
| [T503](#t503) | (shared, all) Clean-clone reproducibility check of one result per contribution | T204, T303 | Sun 2026-12-06 | To Do |
| [T504](#t504) | (shared, all) Full draft → faculty feedback → final submission | T503 | Mon 2026-12-14 | To Do |

Recurring integrator duties (not task-numbered): review, approve and merge M2/M3 PRs with the checklist in
[AGENTS.md §7](../../AGENTS.md); merge my own PRs from `dev_shahriar` (no approval needed, CI `tests`
green, same checklist); sync STATUS in `T000: sync status`; tag gates `g0`–`g4` on the gate days
(G0 Tue 2026-10-27, G1 Tue 2026-11-03, G2 Tue 2026-11-17, G3 Tue 2026-11-24, G4 at the freeze Wed
2026-12-02).

---

## Record: my laptop

Filled in during [T002](#t002). Values are copied from the commands shown, not typed from memory.

| Field | Value | Source |
|---|---|---|
| Windows edition | Windows 11 Home Single Language | `winver` / CIM |
| Windows version | 23H2 (10.0.22631) | `winver` / CIM |
| OS build | 22631 | `winver` / CIM |
| OsName · OsVersion · OsBuildNumber | Microsoft Windows 11 Home Single Language · 10.0.22631 · 22631 | `Get-CimInstance Win32_OperatingSystem` |
| Laptop model | Lenovo 80XG (IdeaPad 320) | `(Get-CimInstance Win32_ComputerSystem).Model` |
| CPU | Intel(R) Core(TM) i3-6006U CPU @ 2.00GHz (2 cores, 4 logical processors) | `(Get-CimInstance Win32_Processor).Name` |
| RAM | 12 GB (12,753,539,072 bytes) | `(Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory` |
| Environment | Python 3.11 venv (`.venv`) | `.\.venv\Scripts\python.exe --version` |
| Python | 3.11.9 | `python --version` |
| torch · numpy · mujoco · dm-control | torch 2.7.1+cpu · numpy 1.24.4 · mujoco 3.1.2 · dm-control 1.0.16 | `pip show torch numpy mujoco dm-control` |
| `MUJOCO_GL` in effect during the smoke test | disable | `python scripts/smoke_test.py --mode tiny` |
| Smoke test (tiny) | Pass, 2026-10-22 (46.8s total wall time) | exit code 0 |
| Recorded on | 2026-10-22 | — |

The sec/step printed by the smoke test is a debugging figure and is not recorded here; budgets use T008
(`results/P0_profile/`).

---

## Pre-registration: ranking-fidelity design (H1, T104)

[PROJECT_PLAN §7.3](../PROJECT_PLAN.md) assigns the ranking-fidelity part of H1 to me and lets H1 be
pre-registered on this page. Everything in this table is fixed and committed (PR merged to `main`)
**before the first T104 run that writes to `results/P1_ranking/`**; debug runs go to `outputs/debug/`
only. Values are never edited after results exist; a change is a new, dated row.

| Item | Value | Notes |
|---|---|---|
| Severity-ordering test for "monotonic" (Kendall τ vs shift level) | `[[pre-register before run]]` | e.g. a rank-correlation test across levels, per shift type and task |
| What counts as a "degraded" ranking fidelity | `[[pre-register before run]]` | stated relative to the nominal CI from the same run family |
| Shift types and levels reported | `[[pre-register before run]]` | levels taken from `configs/shifts.yaml` (T102); state whether dev, test or both splits are reported |
| Number of start states per (task, shift, seed) `--states` | `[[pre-register before run]]` | budget from the T104 formula |
| Candidates per state `--candidates` (M) | `[[pre-register before run]]` | |
| Horizon `--horizon` (H) | `[[pre-register before run]]` | recommended: the planner's own `horizon` from `third_party/tdmpc2/tdmpc2/config.yaml`, so that the model score equals what MPPI uses |
| How start states are sampled | `[[pre-register before run]]` | recommended: states visited by the frozen B0 planner in the shifted env (deployment distribution) |
| How the M candidates are generated | `[[pre-register before run]]` | recommended: drawn from the planner's own final MPPI sampling distribution plus policy-prior sequences (what MPPI actually compares); alternatives: Gaussian noise around the MPPI mean, or uniform in [-1, 1] |
| Treatment of the Q bootstrap in the comparison | `[[pre-register before run]]` | see [T104](#t104) "two score variants" |
| Seeds | test seeds from 0–99 for reported runs; dev seeds 2000–2099 for debugging | seed convention from T001 ([PROJECT_PLAN §8](../PROJECT_PLAN.md)) |

---

## Weekly Faculty Update

For Dr. Mohammad Ashrafuzzaman Khan, due every **`[[weekday]]`** (open item in
[STATUS §3](../STATUS.md), "Decisions pending with faculty").

Rules: 3–5 bullets, **each quoting a hard number copied from a file under `results/` and cited by its
path**, plus exactly one "blocker / help needed" bullet. A week without results reports completed tasks
with their evidence (PR number, file path) and no numbers. Laptop numbers are never quoted, except T0
CPU wall-time measurements labelled as such.

Format example (placeholders only, never replaced by invented values):

> **Week `<n>` (`<date>`) — M1, Md. Shahriar Rakib Rabbi**
> - Completed T006: the harness evaluates one task of the mt30 checkpoint on CPU; nominal `<task>` return `<mean_return from results/P0_nominal/<run_id>/summary.json>` (95% CI `<ci95_low>`–`<ci95_high>`, same file).
> - T101/T102: `<count of shift types>` shift types × `<count of levels>` levels defined, split into dev and held-out test levels (`configs/shifts.yaml`, commit `<sha>`).
> - T104: on `<task>`, Kendall τ between model-predicted and true candidate returns is `<kendall_tau_mean from results/P1_ranking/<run_id nominal>/summary.json>` nominal vs `<kendall_tau_mean from results/P1_ranking/<run_id shifted>/summary.json>` under `<shift spec>`.
> - Closed loop (T304): detection-triggered adaptation recovers `<gap recovery from results/P3_closedloop/<run_id>/summary.json>` of the nominal–shifted gap on `<task>` under `<shift spec>`.
> - Integration: `<n>` PRs merged this week (`#<n>`, `#<n>`); gate `<G?>` decided `<Passed | Failed→fallback>` (evidence `<results path>`).
> - Blocker / help needed: `<one concrete item, or "none">`.

| Week | Date sent | Bullets (copy) | Evidence paths |
|---|---|---|---|
| | | | |

---

## Compute log

Copied into the STATUS compute ledger at each sync. Estimated hours from the task card formula; actual
hours from `wall_time_s` in the run's `episodes.csv`.

| Date | Task | Run family | Tier | Colab account | Shard | Estimated hours | Actual hours |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

---

## Handoff Log

Reverse-chronological (newest first). Format: date · task · what was done · files changed · result path
· blockers · next.

| Date | Task | What was done | Files changed | Result path | Blockers | Next |
|---|---|---|---|---|---|---|
| 2026-10-21 | T001 | Vendored upstream TD-MPC2 at commit `e9f5932` (full SHA `e9f59321933cbc8e11a002b842adc7d4ffae8ff1`, commit date 2026-07-13) into `third_party/tdmpc2/` with its MIT `LICENSE` and `UPSTREAM_COMMIT.txt`; wrote the docs (`AGENTS.md`, STATUS, PROJECT_PLAN, RUNS, REPO_SETUP, team pages); `.github/` files and CI workflow `ci` (matrix `windows-latest` + `ubuntu-latest`, aggregator check `tests`); package skeleton `datdmpc` with owner stubs (full `--help` interfaces, exit code 3), upstream bridge `_upstream.py`, `scripts/smoke_test.py --mode tiny`, M1 tests | Root files (`AGENTS.md`, `CLAUDE.md`, `README.md`, `LICENSE`, `.gitignore`, `.gitattributes`, `pyproject.toml`); `.github/`, `.cursor/`, `docs/`, `environment/`, `src/datdmpc/`, `scripts/`, `tests/`, `third_party/tdmpc2/` | — | None. Tested on my Windows 11 laptop in a Python 3.11 venv with the pinned packages (torch 2.7.1+cpu, mujoco 3.1.2, dm-control 1.0.16, tensordict 0.8.3, numpy 1.24.4): `pytest -q` passes and `python scripts/smoke_test.py` passes (auto → tiny fallback, no checkpoint yet); `MUJOCO_GL` behaviour confirmed (note below). Open: the same check inside the Miniconda env `datdmpc` (T002); CI result pending the first push | T002 |

### T001 note: MUJOCO_GL on Windows

Referenced by [AGENTS.md §4.8](../../AGENTS.md).

- Upstream sets `MUJOCO_GL` (default `egl`) only at the top of its CLI entry points
  `third_party/tdmpc2/tdmpc2/evaluate.py` and `train.py`; we never import those.
- Our single point of control is `configure_rendering()` in `src/datdmpc/_upstream.py`: a value already
  set by the user is respected; with `render=False` (all evaluation runs, laptops, CI) it sets
  `MUJOCO_GL=disable` on every platform; with `render=True` it sets `egl` on Linux only and leaves the
  library default on Windows. `disable` is an official dm_control "no renderer" value
  (`dm_control/_render/constants.py`).
- Windows test result (2026-10-21, my Windows 11 laptop, Python 3.11 venv with the pinned packages):
  - with `MUJOCO_GL` unset, `disable` is set automatically; `mujoco` and `dm_control` import and step
    `walker-walk` (smoke test prints `mujoco_gl: disable`); `pytest -q` passes.
  - with `MUJOCO_GL=egl` on Windows, environment creation fails with the misleading upstream error
    `ValueError: Failed to make environment "walker-walk": please verify that dependencies are installed and that the task exists.`
    (upstream `envs/__init__.py` hides the real import error). Fix: `Remove-Item Env:MUJOCO_GL` and make
    sure it is not set in the Windows user environment variables. Never set `egl` on Windows.
- Remaining sub-task of T002: repeat `python scripts/smoke_test.py --mode tiny` inside the Miniconda env
  `datdmpc` and record pass/fail in [Record: my laptop](#record-my-laptop).

---

## Task cards

Budget symbols used below: `N_task` study tasks, `N_shift` shift levels, `N_seed` seeds, `N_ep` episodes
per (task, shift, seed), `L = 500` agent decisions per DMControl episode (action repeat 2, 500-step
timeout in `third_party/tdmpc2/tdmpc2/envs/dmcontrol.py`), `s_plan` = planning sec/step and `s_adapt` =
seconds per adaptation call, both taken from T008 (`results/P0_profile/<run_id>/summary.json`) for the
tier in question. Rule: more than 3 laptop-hours → Colab (T1), sharded with `--shard i/N` and always
`--resume`. MPPI settings are never changed.

All PowerShell blocks assume:

```powershell
cd C:\code\tdmpc2-shift-adaptation
conda activate datdmpc
```

### T001

**Repo scaffolding, vendored upstream at pinned SHA, all docs + `.github/` files**

- **Goal:** a repository every member can clone and work in on day 2: binding rules, task board, plan,
  run guide, team pages, CI that is green without checkpoints, a package skeleton with an agreed CLI for
  every script, and upstream TD-MPC2 vendored read-only at a pinned commit.
- **Depends on:** —
- **Target date:** Thu 2026-10-22
- **Compute tier + budget:** none (documentation and scaffolding). CI runs on GitHub-hosted runners.
- **Files to create/modify:** all M1-owned paths listed in the header that exist at T001 (root files,
  `.github/**`, `.cursor/rules/agents.mdc`, `environment/*`, `third_party/tdmpc2/**`, `src/datdmpc/**`
  stubs, `scripts/*` stubs, M1 tests, `docs/*`, `docs/team/*`). The M2/M3 stubs are created once here and
  then handed over.
- **Exact commands:** pre-commit checks (need a Python env with the requirements installed):

  ```powershell
  git status --short
  python scripts/eval.py --help
  python scripts/get_checkpoints.py --help
  python -m datdmpc.closed_loop --help
  pytest -q
  python scripts/smoke_test.py --mode tiny
  ```

  The first commit, `git push -u origin main`, waiting for CI, enabling branch protection, creating the
  three `dev_*` branches and switching to `dev_shahriar`: follow [REPO_SETUP §6–§9](../REPO_SETUP.md)
  exactly; that page is the single source for this sequence. (`git add -A` is acceptable only for this
  bootstrap commit, after the checks listed there.)
- **Done when:**
  - [ ] `third_party/tdmpc2/UPSTREAM_COMMIT.txt` records `e9f59321933cbc8e11a002b842adc7d4ffae8ff1`, and the upstream `LICENSE` is present unchanged.
  - [ ] CI check `tests` (aggregating `windows-latest` and `ubuntu-latest`) is green on `main`.
  - [ ] Every script and module entry point prints `--help` (exit 0) and its stub exits with code 3 and the "not implemented yet — see T0xx (owner Mx)" message (`tests/test_smoke.py`).
  - [ ] `tests/test_upstream_bridge.py` passes, including the check that `task_dim` is 64 for `mt30` with model sizes 5 and 19.
  - [ ] No member's GitHub handle appears in any committed file (the repository URL `https://github.com/Shahrcasm/tdmpc2-shift-adaptation.git` is allowed by team decision).
  - [ ] Branches `dev_shahriar`, `dev_ishtiak`, `dev_talha` exist on GitHub; branch protection, merge settings and collaborators match the [REPO_SETUP](../REPO_SETUP.md) checklist.
  - [ ] The GitHub repository description no longer says "~96-parameter"; it says "64-number embedding update" ([STATUS §4](../STATUS.md)).
  - [ ] The TD-MPC2 paper PDF and the project proposal PDF are in `docs/references/` (copied by hand).
- **Faculty-report sentence:** "Completed T001: repository scaffolded with upstream TD-MPC2 vendored at commit `e9f5932` (`third_party/tdmpc2/UPSTREAM_COMMIT.txt`) and CPU-only CI on Windows and Linux (PR #`<n>`)."

### T002

**Windows env setup (Python 3.11 venv) + smoke test on own laptop; record Windows version**

- **Goal:** a working `datdmpc` environment on my Windows 11 laptop, installed exactly as
  [RUNS Step 1](../RUNS.md) says, so that RUNS is validated by the integrator first; tiny smoke test
  passing; laptop facts recorded in [Record: my laptop](#record-my-laptop).
- **Depends on:** T001
- **Target date:** Fri 2026-10-23
- **Compute tier + budget:** T0. Installation plus one tiny smoke test (target under 2 minutes on a
  laptop CPU); no planning runs.
- **Files to create/modify:** `docs/team/M1_Shahriar.md` (this page). If RUNS turns out to be wrong
  for Windows: `docs/RUNS.md` and/or `environment/requirements-cpu.txt`, in the same PR.
- **Exact commands** (after installing Git for Windows and Miniconda per [RUNS Step 1](../RUNS.md);
  open a new PowerShell window afterwards):

  ```powershell
  git config --global core.longpaths true
  cd C:\code\tdmpc2-shift-adaptation
  git checkout dev_shahriar
  py -3.11 -m venv .venv
  .\.venv\Scripts\Activate.ps1
  pip install torch==2.7.1 --index-url https://download.pytorch.org/whl/cpu
  pip install -r environment/requirements-cpu.txt
  pip install -e . --no-deps
  python scripts/smoke_test.py --mode tiny
  pytest -q tests/test_upstream_bridge.py tests/test_smoke.py
  winver
  Get-ComputerInfo -Property OsName, OsVersion, OsBuildNumber, CsModel, CsTotalPhysicalMemory
  (Get-CimInstance Win32_Processor).Name
  python --version
  pip show torch numpy mujoco dm-control
  ```

- **Verification sub-task:** the `MUJOCO_GL` Windows check in the [T001 note](#t001-note-mujoco_gl-on-windows).
- **Done when:**
  - [x] `python --version` in `datdmpc` reports 3.11.9, and `pip show` versions match `environment/requirements-cpu.txt`.
  - [x] `python scripts/smoke_test.py --mode tiny` exits 0 and prints `[smoke] OK`.
  - [x] `pytest -q tests/test_upstream_bridge.py tests/test_smoke.py` passes on the laptop (21 passed).
  - [x] [Record: my laptop](#record-my-laptop) is filled in, including the `winver` edition, version and OS build.
  - [x] The `MUJOCO_GL` result is recorded as `disable` on Windows.
  - [x] Python 3.11 venv documented in `RUNS.md` as recommended lightweight route for 12GB laptops.
- **Faculty-report sentence:** "Completed T002: CPU-only environment installed on a Windows 11 laptop (build 22631) following `docs/RUNS.md`; tiny smoke test and bridge tests pass (PR #`<n>`)."

### T005

**`scripts/get_checkpoints.py` + `checkpoints/MANIFEST.csv`; upload to shared Drive**

- **Goal:** fetch exactly the two released checkpoints we use, verify them by sha256, record a manifest,
  and place them in the shared Drive folder `DA-TDMPC2/checkpoints/` for Colab.
- **Depends on:** T002
- **Target date:** Sat 2026-10-24
- **Compute tier + budget:** T0, no planning compute. Download size per the Hugging Face API
  (retrieved 2026-10-21): `mt30-5M.pt` 33,299,935 bytes, `mt30-19M.pt` 99,246,424 bytes. Never download
  any training dataset.
- **Files to create/modify:** `scripts/get_checkpoints.py`, `checkpoints/MANIFEST.csv`,
  `tests/test_get_checkpoints.py` (hash-mismatch test), `docs/RUNS.md` (only if the procedure changes).
- **Interface (binding):** `--models mt30-5M mt30-19M [--dest checkpoints] [--verify-only]`. Source URL
  pattern `https://huggingface.co/nicklashansen/tdmpc2/resolve/main/multitask/<name>.pt`. Manifest
  columns `name,size_bytes,sha256,url`.
- **Exact commands:**

  ```powershell
  python scripts/get_checkpoints.py --models mt30-5M mt30-19M --dest checkpoints
  python scripts/get_checkpoints.py --models mt30-5M mt30-19M --verify-only
  (Get-FileHash checkpoints\mt30-5M.pt -Algorithm SHA256).Hash -eq "f3c6909e3282f115ce57b2ab29a88e654b4728d819d2c93a4ca079bad63b1455"
  (Get-FileHash checkpoints\mt30-19M.pt -Algorithm SHA256).Hash -eq "10773c9124ac23f157d46d33c29ab877322e29e63c2b0bf4bd3434a25b97ac86"
  pytest -q tests/test_get_checkpoints.py
  ```

  Upload both `.pt` files to Drive `DA-TDMPC2/checkpoints/` in the browser, then check from a Colab cell:

  ```python
  !python scripts/get_checkpoints.py --models mt30-5M mt30-19M --dest /content/drive/MyDrive/DA-TDMPC2/checkpoints --verify-only
  ```

- **Done when:**
  - [ ] sha256 of `checkpoints/mt30-5M.pt` is `f3c6909e3282f115ce57b2ab29a88e654b4728d819d2c93a4ca079bad63b1455` (both the script and `Get-FileHash` agree; the PowerShell line prints `True`).
  - [ ] sha256 of `checkpoints/mt30-19M.pt` is `10773c9124ac23f157d46d33c29ab877322e29e63c2b0bf4bd3434a25b97ac86` (same two checks).
  - [ ] `checkpoints/MANIFEST.csv` has exactly two rows with columns `name,size_bytes,sha256,url`, sizes 33299935 and 99246424, and the URLs from the pattern above.
  - [ ] `--verify-only` exits non-zero on a hash mismatch (unit test with a temporary file and a patched expected hash in `tests/test_get_checkpoints.py`).
  - [ ] `git status --short` shows `checkpoints/MANIFEST.csv` as the only file under `checkpoints/` (no `.pt` staged).
  - [ ] The Colab `--verify-only` cell on the Drive copies exits 0.
- **Faculty-report sentence:** "Completed T005: released checkpoints mt30-5M and mt30-19M fetched and verified against their published sha256 values (`checkpoints/MANIFEST.csv`), shared via Drive for Colab runs."

### T006

**Single-task-of-multitask evaluation harness + resume-safe logging + tests**

- **Goal:** evaluate **one** task of the 30-task checkpoint (frozen, method label `B0`), on CPU or GPU,
  nominal or shifted, writing the results schema with resume support. This is what upstream cannot do:
  its README states that single-task evaluation of multi-task checkpoints is not supported, and
  `evaluate.py` / `train.py` assert CUDA. G0 (Tue 2026-10-27) depends on this task.
- **Depends on:** T005
- **Target date:** Mon 2026-10-26
- **Compute tier + budget:** T0 for development. Debug runs: `1 task × 1 shift × 1 seed × N_ep × L ×
  s_plan,T0 / 3600` hours. `s_plan,T0` is not known yet (T008 depends on this task), so the first run
  uses `--episodes 1` and the cost is read from `wall_time_s` in its `episodes.csv` (debug figure, not a
  result). Debug output goes to the gitignored `outputs/debug/`, never to `results/`.
- **Files to create/modify:** `src/datdmpc/eval/harness.py`, `src/datdmpc/eval/logging.py`,
  `scripts/eval.py`, `scripts/smoke_test.py` (full mode wiring), `tests/test_harness.py`,
  `tests/test_logging.py`, `tests/conftest.py`, `configs/experiments/M1_*.yaml` (if a debug config is
  needed), `notebooks/colab/M1_*.ipynb` (one launcher to check the harness on Colab).
- **Implementation constraints (verified in the vendored code):**
  - `TDMPC2.__init__` hard-codes `torch.device('cuda:0')` (`third_party/tdmpc2/tdmpc2/tdmpc2.py`, also
    the multitask discount tensor), as does `RunningScale` (`common/scale.py`). The harness defines a
    subclass (e.g. `CPUTDMPC2`) that re-implements `__init__` with a configurable device and
    `compile=False` and reuses upstream `act` / `_plan` / `_estimate_value` unchanged. `WorldModel`
    (`common/world_model.py`) has no device hard-coding. Nothing under `third_party/` is edited.
  - Config: model size 5 or 19 (`--model-size`, else inferred from the filename); `parser.py` sets
    `latent_dim = 512` for mt30 at size 19 and `task_dim = 64` for mt30 at sizes 5 and 19. Per-task
    observation/action dims and episode lengths come from upstream's multitask env construction
    (`make_multitask_env` in `envs/__init__.py`).
  - Open check (sub-task of T006): upstream `parse_cfg` (`common/parser.py`) calls
    `hydra.utils.get_original_cwd()`; whether it can run outside a Hydra app is unconfirmed. If it cannot,
    the harness replicates only the lines it needs (`bin_size`, `MODEL_SIZE`, mt30 `latent_dim` override,
    `task_dim`, `tasks`).
    <!-- VERIFY: whether upstream parse_cfg (third_party/tdmpc2/tdmpc2/common/parser.py) can be called outside a running Hydra app, given it calls hydra.utils.get_original_cwd(). Resolved by T006. -->
  - Loading uses upstream `TDMPC2.load` (handles old-format checkpoints via `api_model_conversion`;
    strict `load_state_dict`).
- **Exact commands:**

  ```powershell
  pytest -q tests/test_harness.py tests/test_logging.py tests/test_upstream_bridge.py
  python scripts/eval.py --ckpt checkpoints/mt30-5M.pt --task walker-walk --shift none --episodes 1 --seed 0 --out outputs/debug/ --tier T0 --device cpu
  python scripts/eval.py --ckpt checkpoints/mt30-5M.pt --task walker-walk --shift none --episodes 1 --seed 0 --out outputs/debug/ --tier T0 --device cpu --resume
  python scripts/eval.py --ckpt checkpoints/mt30-5M.pt --task walker-walk --shift none --episodes 2 --seed 0 --out outputs/debug/ --tier T0 --device cpu --resume
  python scripts/eval.py --ckpt checkpoints/mt30-19M.pt --task walker-walk --shift none --episodes 1 --seed 0 --out outputs/debug/ --tier T0 --device cpu
  pytest -q
  ```

  Colab check (CPU or GPU runtime) from `notebooks/colab/M1_*.ipynb`:

  ```python
  !python scripts/eval.py --ckpt /content/drive/MyDrive/DA-TDMPC2/checkpoints/mt30-5M.pt --task walker-walk --shift none --episodes 1 --seed 0 --out /content/drive/MyDrive/DA-TDMPC2/results/debug/ --tier T1 --device cuda --resume
  ```

- **Done when:**
  - [ ] After loading `mt30-5M.pt` and `mt30-19M.pt`, a test asserts `model._task_emb.weight.shape == (30, 64)` (never 96 for these checkpoints).
  - [ ] Loading reports no missing or unexpected state-dict keys for either checkpoint.
  - [ ] One episode of one task (`walker-walk`, task index 1 in `TASK_SET['mt30']`) runs to completion **on CPU** through the subclass/wrapper, with no CUDA call and no file under `third_party/` modified (`git diff --name-only -- third_party` prints nothing).
  - [ ] The run folder contains `config.yaml`, `episodes.csv`, `summary.json`, `env.txt`, `git_sha.txt`; `run_id` follows `<ckpt-stem>__<task>__<shift>__<method>__seed<seed>` with `:` → `-`; `episodes.csv` has exactly the binding columns.
  - [ ] Resume works: rerunning the same command with `--resume` adds 0 rows; rerunning with `--episodes 2 --resume` adds exactly 1 row; `tests/test_logging.py` covers an interrupted run (no duplicate and no lost finished episode).
  - [ ] `--shard i/N` splits a multi-task job list deterministically into disjoint parts whose union is the full list (unit test).
  - [ ] MPPI settings in the resolved `config.yaml` equal upstream `config.yaml` (`iterations`, `num_samples`, `num_elites`, `num_pi_trajs`, `horizon`, `min_std`, `max_std`, `temperature`) (unit test).
  - [ ] The Colab cell above completes and writes the same five files on Drive.
  - [ ] `pytest -q` passes locally and CI `tests` is green.
- **Faculty-report sentence:** "Completed T006: our harness evaluates a single task of the mt30 multitask checkpoint on CPU and GPU with resume-safe per-episode logging; nominal `<task>` return `<mean_return from results/P0_nominal/<run_id>/summary.json>` (PR #`<n>`)."

### T101

**Perturbation wrappers + tests proving the physical parameter changed**

- **Goal:** `src/datdmpc/envs/perturb.py` implements the shift SPEC grammar (`none` or `<type>:<level>`,
  type ∈ {`mass`, `friction`, `actuator`, `gravity`, `obs_noise`, `action_delay`}) for any mt30 DMControl
  task, applied at episode start or injected mid-episode (needed by T303/T304).
- **Depends on:** T002
- **Target date:** Thu 2026-10-29
- **Compute tier + budget:** T0. Unit tests and short rollouts only; checkpoint-based debug episodes:
  `1 × N_shift × 1 × 1 × L × s_plan,T0 / 3600` hours (s_plan,T0 from T008 once available).
- **Files to create/modify:** `src/datdmpc/envs/perturb.py`, `src/datdmpc/envs/__init__.py`,
  `tests/test_perturb.py`, `scripts/smoke_test.py` (full mode uses the wrappers),
  `src/datdmpc/eval/harness.py` (`make_task_env` applies the shift).
- **Mechanism:** physical shifts edit the innermost dm_control env's MuJoCo model
  (`datdmpc._upstream.unwrap_dm_env(env).physics.model`): `body_mass`, `geom_friction`,
  `actuator_gear`, `opt.gravity`; `mass`/`friction`/`actuator`/`gravity` levels are multiplicative.
  `obs_noise` adds Gaussian noise with std = level to observations; `action_delay` delays actions by
  level agent steps. Each agent step is two simulator steps (action repeat 2, `envs/dmcontrol.py`), so a
  delay is counted in agent steps.
- **Exact commands:**

  ```powershell
  pytest -q tests/test_perturb.py
  python scripts/smoke_test.py --mode tiny --shift mass:1.5
  python scripts/smoke_test.py --mode full --ckpt checkpoints/mt30-5M.pt --task walker-walk --steps 50 --shift mass:1.5 --seed 0
  python scripts/eval.py --ckpt checkpoints/mt30-5M.pt --task walker-walk --shift friction:<level> --episodes 1 --seed 0 --out outputs/debug/ --tier T0 --device cpu
  pytest -q
  ```

- **Done when:**
  - [ ] `parse_shift` accepts every type of the grammar and `none`, and rejects unknown types or malformed levels (test).
  - [ ] For each of `mass`, `friction`, `actuator`, `gravity`: after applying `<type>:k` with k ≠ 1, the corresponding `physics.model` array equals k × the nominal array (exact or `allclose`), on at least two mt30 domains, one of them a custom task from `third_party/tdmpc2/tdmpc2/envs/tasks/` (test per type).
  - [ ] For each physical type, `<type>:1.0` leaves the array identical to nominal (test).
  - [ ] Each physical change survives `env.reset()` and persists for the whole episode (test).
  - [ ] `obs_noise:<std>` with std > 0 changes observations relative to an un-noised env with the same seed, and `obs_noise:0` does not (test).
  - [ ] `action_delay:<d>` makes the action applied at agent step t equal the action issued at step t − d (test with a scripted action sequence).
  - [ ] Mid-episode injection: applying a shift at step `t_inject` leaves steps before `t_inject` identical to a nominal run with the same seed (test).
  - [ ] `python scripts/smoke_test.py --mode full ...` (after T006 is merged) exits 0 and prints `[smoke] OK`.
  - [ ] `pytest -q` passes and CI `tests` is green.
- **Faculty-report sentence:** "Completed T101: six shift types implemented as wrappers on DMControl; unit tests confirm each physical parameter (mass, friction, actuator gear, gravity) is changed by exactly the requested factor (`tests/test_perturb.py`, PR #`<n>`)."

### T007

**Nominal eval of mt30-5M and mt30-19M on all 30 tasks; choose 4–6 study tasks by a pre-written rule**

- **Goal:** (1) nominal (`--shift none`) B0 returns of both released checkpoints on all 30 mt30 tasks,
  produced on Colab and stored in `results/P0_nominal/`; (2) the 4–6 study tasks for all later phases,
  chosen by a **rule written and committed before any shifted result exists**. mt30-19M is the primary
  checkpoint and runs first; mt30-5M follows (fast-iteration model).
- **Depends on:** T006, T003 (sweep start also needs `s_plan` on the sweep tier from T008, gate G0)
- **Target date:** Fri 2026-10-30
- **Compute tier + budget:** T1 (Colab), sharded across the three accounts.
  `hours(ckpt) = 30 × 1 × 1 × N_seed × N_ep × L × s_plan(ckpt, tier) / 3600`;
  `total = hours(mt30-19M) + hours(mt30-5M)`; per account ≈ `total / 3` with `--shard i/3`.
  Protocol minimum: `N_seed ≥ 3`, `N_ep ≥ 10` ([PROJECT_PLAN §8](../PROJECT_PLAN.md)).
- **Files to create/modify:** `notebooks/colab/M1_nominal.ipynb`, `configs/experiments/M1_nominal.yaml`
  (command list for the launcher), `results/P0_nominal/<run_id>/…`, this page (selection rule, its
  output, status, compute log).
- **Study-task selection rule (write it here, merge it to `main`, then apply it).** Fill in the rule
  below and open the PR **before** any T103 or other shifted run exists (best: before opening the T007
  results). M1 copies it into [PROJECT_PLAN §8](../PROJECT_PLAN.md) in the same merge. The rule must have
  all of these properties:
  1. **Uses nominal data only:** inputs are the `results/P0_nominal/` summaries (and the mt30 task list in
     `third_party/tdmpc2/tdmpc2/common/__init__.py`); never shifted, ranking-fidelity or adaptation results.
  2. **Deterministic and mechanical:** anyone applying it to `results/P0_nominal/` gets the same list;
     ties are broken by a fixed key (e.g. mt30 task index order).
  3. **Names the checkpoint whose scores decide** (primary: mt30-19M) and the statistic used (e.g. mean
     return and its 95% CI from `summary.json`).
  4. **Leaves room to measure degradation:** excludes tasks whose nominal return is too low for a
     nominal–shifted gap to be measurable (gap recovery divides by `R_nominal − R_shift`); the cut-off is
     `[[pre-register before run]]`.
  5. **Physical-shift applicability:** every selected task can receive the mass, friction and actuator
     shifts of the T101 wrappers (checked against the wrapper, not assumed).
  6. **Diversity:** limits tasks per domain (walker, cheetah, reacher, acrobot, pendulum, cartpole, cup,
     finger, fish, hopper) to `[[pre-register before run]]`, and states whether the 11 custom mt30 tasks
     are eligible.
  7. **Yields 4–6 tasks** and fits the T103/T204 budgets computed with the formulas below.
  8. **States what happens on failure** (fewer than 4 eligible tasks): which criterion is relaxed, in
     which order.

  Rule text: `[[pre-register before run: write the rule here]]`
  Committed in PR #`<n>` on `<date>` (before the first T103 run).
  Output (filled only after applying the rule): `<task 1>`, `<task 2>`, `<task 3>`, `<task 4>`, …
- **Exact commands.** Colab, one run cell per account (`i` = 1 for M1, 2 for M2, 3 for M3; GPU runtime
  `--device cuda`, CPU runtime `--device cpu`):

  ```
  !python scripts/eval.py --ckpt checkpoints/mt30-19M.pt --task all --shift none --episodes 10 --seeds 0 1 2 --out /content/drive/MyDrive/DA-TDMPC2/results/P0_nominal/ --resume --shard <i>/3 --tier T1 --device cuda
  !python scripts/eval.py --ckpt checkpoints/mt30-5M.pt --task all --shift none --episodes 10 --seeds 0 1 2 --out /content/drive/MyDrive/DA-TDMPC2/results/P0_nominal/ --resume --shard <i>/3 --tier T1 --device cuda
  !python --version
  !pip show torch
  ```

  <!-- VERIFY: Colab's Python version and preinstalled torch at run time (python --version; pip show torch) match environment/requirements-colab.txt; record in the handoff entry (T007) -->
  Laptop check before the sweep (debugging only, output to the gitignored `outputs/`):

  ```powershell
  python scripts/eval.py --ckpt checkpoints/mt30-5M.pt --task walker-walk --shift none --episodes 1 --seed 0 --out outputs/debug/ --resume
  ```

  Sanity comparison: compare nominal scores with any per-task mt30 scores published by the paper or
  upstream. <!-- VERIFY: which per-task mt30 nominal scores the TD-MPC2 paper or upstream repository publish for comparison (also open in PROJECT_PLAN risk R1); resolved in T007 -->
- **Done when:**
  - [ ] The selection rule is on `main` (PR #`<n>`) before any shifted run exists, and M1 copied it into PROJECT_PLAN §8.
  - [ ] `results/P0_nominal/` has one run folder per (checkpoint, task, seed) for both checkpoints and all 30 tasks, each with `config.yaml`, `episodes.csv`, `summary.json`, `env.txt` (tier T1 or T1b), `git_sha.txt`.
  - [ ] Every `episodes.csv` has `N_ep` rows per seed (no gaps after `--resume`).
  - [ ] The rule has been applied mechanically and its output (4–6 study tasks) is written above, with the `summary.json` paths it used.
  - [ ] Each account's shard is in the [Compute log](#compute-log) (account, shard, estimated and actual hours).
- **Faculty-report sentence:** "Completed T007: nominal returns of mt30-5M and mt30-19M on all 30 tasks (`results/P0_nominal/`); study tasks `<list>` selected by the rule committed in PR #`<n>` before any shifted run."

<a id="t009"></a>

### T102

**`configs/shifts.yaml`: types × levels; dev vs held-out test split**

- **Goal:** one committed file that defines every shift type and level used anywhere in the project,
  split into **dev** levels (tuning: adaptation lr/steps/K, detector thresholds) and **held-out test**
  levels (reported only). The split is recorded **before any adaptation run** (T202–T204) and before any
  detector tuning (T302), and is never edited for levels that already have results.
- **Depends on:** T101, T007
- **Target date:** Sat 2026-10-31
- **Compute tier + budget:** none for the file itself. If a level is checked for a visible effect before
  freezing the file, use T0 debug episodes with dev seeds 2000–2099 only:
  `N_task × N_shift × 1 × 1 × L × s_plan,T0 / 3600` hours (> 3 h → Colab).
- **Files to create/modify:** `configs/shifts.yaml`, `tests/test_perturb.py` (config validation),
  `docs/PROJECT_PLAN.md` (level-selection rule, written before levels are chosen), `docs/RUNS.md`
  (schema of the file).
- **Rules for choosing levels:** the selection rule is written into PROJECT_PLAN first; levels are not
  chosen by looking at adaptation results. Study tasks are those chosen by M2's T007 rule
  (`results/P0_nominal/`). `obs_noise` and `action_delay` are included as the expected-negative cases (H3).
  If G1 fails (Tue 2026-11-03), severity is raised by **adding** new levels; existing entries are not
  edited.
- **Exact commands:**

  ```powershell
  pytest -q tests/test_perturb.py
  python scripts/eval.py --ckpt checkpoints/mt30-5M.pt --task walker-walk --shifts-from configs/shifts.yaml --split dev --episodes 1 --seed 2000 --out outputs/debug/ --tier T0 --device cpu
  git log -1 --format=%H -- configs/shifts.yaml
  ```

- **Done when:**
  - [ ] The level-selection rule is in [PROJECT_PLAN](../PROJECT_PLAN.md), committed before `configs/shifts.yaml` gets its levels (commit order visible in `git log`).
  - [ ] Every one of the six shift types has at least one dev level and at least one test level; dev ∩ test = ∅ for every type (test).
  - [ ] Every entry parses with `datdmpc.envs.perturb.parse_shift` (test).
  - [ ] `scripts/eval.py --shifts-from configs/shifts.yaml --split {dev,test,all}` enumerates exactly the listed levels (test).
  - [ ] The commit SHA of the merged `configs/shifts.yaml` is recorded in this page's handoff log and in [STATUS](../STATUS.md) **before** the first `scripts/adapt.py` or detector-tuning run.
- **Faculty-report sentence:** "Completed T102: `<count>` shift types × `<count>` levels fixed in `configs/shifts.yaml` (commit `<sha>`), with tuning levels and held-out test levels separated before any adaptation run."

### T104

**Ranking-fidelity diagnostic, nominal vs shifted → `results/P1_ranking/`**

- **Goal:** measure whether dynamics shift corrupts how the frozen world model **ranks** candidate
  action sequences — the first half of the unifying story and the C1 diagnostic. For each sampled start
  state, save the simulator state, roll out M candidate action sequences of H agent steps in the **real**
  (nominal or shifted) simulator, restoring the state between candidates, and compare the true
  short-horizon returns with the model's predicted returns by Kendall τ and top-1 agreement
  ([PROJECT_PLAN §9](../PROJECT_PLAN.md)), nominal vs each shift level. Part of the minimum deliverable.
- **Depends on:** T006, T101
- **Target date:** Tue 2026-11-03 (G1)
- **Compute tier + budget:** per (task, shift level, seed):
  `(t_last × s_plan + N_states × M × (H × s_sim + s_pred)) / 3600` hours, where `t_last` is the agent
  step of the last sampled start state (the frozen B0 planner must run to reach it). Total =
  `N_task × N_shift × N_seed ×` that. `s_plan` from T008; `s_sim`, `s_pred` from the first debug run.
  > 3 laptop-hours → T1 (likely for mt30-19M).
- **Files to create/modify:** `src/datdmpc/diagnostics/ranking_fidelity.py`,
  `tests/test_ranking_fidelity.py`, `configs/experiments/M1_ranking.yaml` (if needed),
  `notebooks/colab/M1_ranking.ipynb`, `results/P1_ranking/**`, this page
  ([Pre-registration](#pre-registration-ranking-fidelity-design-h1-t104)).
- **Interface (binding):** `python -m datdmpc.diagnostics.ranking_fidelity --ckpt --task --shift
  --states N --candidates M --horizon H --seed --out results/P1_ranking/ [--embedding
  PATH/adapted_embedding.json]` (plus `--tier`, `--device`). The interface has no `--resume` / `--shard`:
  each invocation covers one (task, shift, seed), so a lost Colab session costs one run, and the three
  accounts split the (task, shift) list by hand (recorded in the compute log).
- **Method (verified against the vendored upstream code):**
  - *Save/restore:* the raw dm_control env is reached with `datdmpc._upstream.unwrap_dm_env(env)`; its
    `physics.get_state()` / `physics.set_state()` save and restore the simulator state. Shift wrappers
    (T101) change `physics.model` parameters, which save/restore does not touch, so the shift persists
    across candidates. Wrapper-level state is **not** in `physics`: upstream `Timeout`
    (`envs/wrappers/timeout.py`) counts steps in `self._t`, and our `action_delay`/`obs_noise` wrappers
    keep a buffer / RNG. Candidate rollouts must save and restore these too, or roll out without them —
    request to M1 by issue if `envs/perturb.py` needs a get/set-state hook.
    <!-- VERIFY: whether physics.set_state() must be followed by physics.forward() (or done inside physics.reset_context()) so that observations and rewards after a restore equal those of the original trajectory, in dm_control 1.0.16 / mujoco 3.1.2. Resolved by the T104 determinism and counterfactual tests. -->
    <!-- VERIFY: whether the dm_control control.Environment keeps its own step counter / time limit that candidate rollouts advance (possibly triggering an automatic reset at the next step); check the installed dm_control/rl/control.py. Resolved by T104 (save/restore that counter, or use states with enough remaining steps). -->
  - *True return:* each candidate step goes through the upstream `DMControlWrapper.step`, which applies the
    action twice and sums the reward (`envs/dmcontrol.py`), so true and predicted rewards are on the same
    per-agent-step scale. Discounting uses the task's planner discount `agent.discount[task_idx]`
    (`TDMPC2._get_discount` from the episode length and `discount_denom` / `discount_min` /
    `discount_max` in `config.yaml`).
  - *Model score:* as upstream `TDMPC2._estimate_value` (`tdmpc2.py`): sum over H steps of discounted
    predicted rewards (`two_hot_inv` of `model.reward`, latent rolled forward with `model.next`) plus the
    discounted `Q(z_H, pi(z_H), return_type='avg')` bootstrap. Two implementation facts from the code:
    `_estimate_value` sizes its termination mask with `cfg.num_samples`, so evaluating M candidates needs
    a config view with `num_samples = M` (or a line-by-line re-implementation tested against upstream) —
    the planner's own config is never changed; and the score is stochastic, because `pi` samples Gaussian
    noise and `Q(return_type='avg')` averages two **randomly** chosen ensemble heads
    (`common/world_model.py`), so the torch seed is fixed per state and recorded.
  - *Two score variants (both reported, primary one pre-registered):* (i) **reward-only** — model
    discounted reward sum over H vs true discounted reward sum over H (isolates dynamics + reward model);
    (ii) **planner score** — full `_estimate_value` vs true H-step return, with the treatment of the
    bootstrap tail fixed in the [pre-registration table](#pre-registration-ranking-fidelity-design-h1-t104).
  - *Metrics:* Kendall τ (tau-b via `scipy.stats.kendalltau`) and top-1 agreement per state, aggregated
    over states with a 95% bootstrap CI; `summary.json` adds `kendall_tau_mean`, `kendall_tau_ci95_low`,
    `kendall_tau_ci95_high`, `top1_agreement`, `n_states`, `n_candidates`, `horizon`, `score_variant`.
    Per-state rows (state index, step, τ, top-1) are written as an extra CSV in the run folder;
    `episodes.csv` keeps the binding columns for the B0 episode(s) used to reach the states.
- **Exact commands:**

  ```powershell
  pytest -q tests/test_ranking_fidelity.py
  python -m datdmpc.diagnostics.ranking_fidelity --ckpt checkpoints/mt30-5M.pt --task walker-walk --shift none --states <N> --candidates <M> --horizon <H> --seed 2000 --out outputs/debug/ --tier T0 --device cpu
  python -m datdmpc.diagnostics.ranking_fidelity --ckpt checkpoints/mt30-5M.pt --task walker-walk --shift <dev level spec from configs/shifts.yaml> --states <N> --candidates <M> --horizon <H> --seed 2000 --out outputs/debug/ --tier T0 --device cpu
  ```

  Colab (reported runs; one cell per (task, shift, seed); nominal first, then every pre-registered level):

  ```python
  !python -m datdmpc.diagnostics.ranking_fidelity --ckpt /content/drive/MyDrive/DA-TDMPC2/checkpoints/mt30-19M.pt --task <study task> --shift none --states <N> --candidates <M> --horizon <H> --seed <test seed> --out /content/drive/MyDrive/DA-TDMPC2/results/P1_ranking/ --tier T1 --device cuda
  !python -m datdmpc.diagnostics.ranking_fidelity --ckpt /content/drive/MyDrive/DA-TDMPC2/checkpoints/mt30-19M.pt --task <study task> --shift <level spec from configs/shifts.yaml> --states <N> --candidates <M> --horizon <H> --seed <test seed> --out /content/drive/MyDrive/DA-TDMPC2/results/P1_ranking/ --tier T1 --device cuda
  ```

- **Done when:**
  - [ ] The [pre-registration table](#pre-registration-ranking-fidelity-design-h1-t104) is filled in and on `main` before the first run writing to `results/P1_ranking/`.
  - [ ] Test (determinism): from a restored state, executing the same action sequence twice gives identical observations and true returns.
  - [ ] Test (counterfactual): the true return computed for a candidate from a restored state equals the return obtained by actually executing that candidate in an uninterrupted copy of the episode (same seed, same shift).
  - [ ] Test: the diagnostic leaves the main episode unchanged — the B0 episode with the diagnostic enabled has the same per-step observations as without it (same seed).
  - [ ] Test: Kendall τ and top-1 agreement on hand-computed small examples (including ties); model score equals upstream `_estimate_value` for the same inputs and torch seed (tiny model).
  - [ ] Test: with a shift applied, the shifted physical parameter is still in effect after every restore.
  - [ ] `results/P1_ranking/` has a complete run folder for nominal and every pre-registered shift level on each study task (mt30-19M primary), produced on T1 or reproduced there (`env.txt`), MPPI settings unchanged in `config.yaml`.
  - [ ] Handoff entry lists the evidence paths for G1 (Tue 2026-11-03).
- **Faculty-report sentence:** "Completed T104: on `<task>`, Kendall τ between the frozen mt30-19M model's predicted and the true short-horizon returns of `<M>` candidates is `<kendall_tau_mean>` nominally and `<kendall_tau_mean>` under `<shift spec>` (`results/P1_ranking/<run_id>/summary.json`)."

### T501

**`build_registry.py` + `make_figures.py` (read `results/` only)**

- **Goal:** every number and figure in the report is regenerated from committed results by two scripts:
  `build_registry.py` collects every run folder into `results/REGISTRY.csv`; `make_figures.py` draws
  every figure from the registry into `figures/`. No number is typed by hand.
- **Depends on:** T103
- **Target date:** Tue 2026-11-10
- **Compute tier + budget:** T0, no planning compute (file reading and plotting only).
- **Files to create/modify:** `scripts/build_registry.py`, `scripts/make_figures.py`,
  `results/REGISTRY.csv` (generated), `figures/**` (generated), `tests/test_registry.py` (registry
  tests), `docs/RUNS.md` (registry columns).
- **Interface (binding):** `build_registry.py [--results results] [--out results/REGISTRY.csv]` reads only
  `results/*/*/summary.json` and `config.yaml`; `make_figures.py [--registry results/REGISTRY.csv] [--out
  figures]` writes PNG + PDF, each < 2 MB.
- **Exact commands** (PowerShell 5.1 has no `&&`; run in order):

  ```powershell
  python scripts/build_registry.py --results results --out results/REGISTRY.csv
  python scripts/make_figures.py --registry results/REGISTRY.csv --out figures
  pytest -q tests/test_registry.py
  Get-ChildItem figures -File | Where-Object { $_.Length -gt 2MB }
  ```

- **Done when:**
  - [ ] `REGISTRY.csv` has one row per run folder containing a `summary.json`, and every row's values equal the source `summary.json` / `config.yaml` (test on a synthetic `results/` tree in a temp dir).
  - [ ] Running `build_registry.py` twice produces byte-identical `REGISTRY.csv` (test).
  - [ ] Neither script reads anything outside `results/` (registry) or `results/REGISTRY.csv` (figures).
  - [ ] Every figure exists as PNG and PDF; the size check prints nothing.
  - [ ] On the committed T103 results (`results/P1_degradation/`), the degradation figure is produced without manual steps.
- **Faculty-report sentence:** "Completed T501: all report tables and figures are regenerated from `results/` by two scripts; the registry currently indexes `<row count of results/REGISTRY.csv>` runs (`results/REGISTRY.csv`)."

### T502

**Report skeleton; M2/M3 write own `report/sections/*_<owner>.tex` from week 4**

- **Goal:** `report/main.tex` in research-paper format with the section structure, owner of each section,
  figure inclusion from `figures/`, and the CSE 465 concept mapping (representation learning, embeddings,
  ensembles, distribution shift, anomaly detection with ROC analysis, parameter-efficient adaptation)
  placed in the sections where it belongs. Template:
  `[[report template: IEEE conference unless the course specifies otherwise]]` until the faculty decides
  ([STATUS §3](../STATUS.md)).
- **Depends on:** T501
- **Target date:** Thu 2026-11-12 (writing of method + setup sections starts in week 4, from Wed 2026-11-11)
- **Compute tier + budget:** none.
- **Files to create/modify:** `report/main.tex`, `report/sections/*_M1.tex`, `docs/PROJECT_PLAN.md`
  (section → owner map). M2 and M3 create their own `report/sections/*_M2.tex` / `*_M3.tex`; `main.tex`
  includes them with `\InputIfFileExists` so the skeleton compiles before they exist.
- **Exact commands:**

  ```powershell
  python scripts/build_registry.py --results results --out results/REGISTRY.csv
  python scripts/make_figures.py --registry results/REGISTRY.csv --out figures
  Select-String -Path report\main.tex, report\sections\*.tex -Pattern "VERIFY"
  ```

  (The LaTeX toolchain, local or Overleaf, is decided in this task and recorded in [RUNS](../RUNS.md).)
- **Done when:**
  - [ ] `report/main.tex` compiles with no section files from M2/M3 present, and again with placeholder files for them.
  - [ ] Every figure is included from `figures/` (no figure files under `report/`).
  - [ ] The section → owner map (file names `<section>_<owner>.tex`) is in [PROJECT_PLAN](../PROJECT_PLAN.md) and announced to M2 and M3 in the handoff log.
  - [ ] Each section has a comment naming the `results/` paths its numbers must come from.
  - [ ] The template placeholder remains until the faculty decision is recorded in STATUS §3.
- **Faculty-report sentence:** "Completed T502: report skeleton in research-paper format with section owners assigned; method and setup sections are being written from week 4 (`report/main.tex`, PR #`<n>`)."

### T205

**Ranking fidelity after C2 adaptation → `results/P2_ranking_after_adapt/`**

- **Goal:** show whether `e`-only adaptation restores the model's ranking of candidate actions — the
  mechanism behind any return recovery in T204. Re-run the T104 diagnostic at the **same start states**
  with the adapted embedding row loaded (`--embedding .../adapted_embedding.json`, 64 numbers for
  mt30-5M/19M per `common/parser.py`), and compare with the frozen embedding (T104) and the nominal
  ceiling.
- **Depends on:** T104, T202. Reported runs use the adapted embeddings saved by M2's T204 runs
  (`results/P2_adapt/<run_id>/adapted_embedding.json`, T204 target Tue 2026-11-17), on the held-out test
  levels. The JSON format is M2's (T202); I read it through M2's public loader if one exists.
- **Target date:** Fri 2026-11-27
- **Compute tier + budget:** as T104 with `N_shift` = test levels used in T204; no adaptation cost
  (embeddings are reused, not re-trained).
- **Files to create/modify:** `src/datdmpc/diagnostics/ranking_fidelity.py` (`--embedding` path),
  `tests/test_ranking_fidelity.py`, `notebooks/colab/M1_ranking.ipynb`,
  `results/P2_ranking_after_adapt/**`, `report/sections/*_M1.tex`.
- **Pairing rule:** with `--embedding`, the start states are still those visited by the **frozen** B0
  planner for the same (task, shift, seed), so every T205 row is paired with a T104 row at the same
  state. The adapted row is written into `model._task_emb.weight[task_idx]` only; the `max_norm=1`
  renormalisation of `nn.Embedding` applies at lookup (`common/world_model.py`).
- **Exact commands:**

  ```powershell
  pytest -q tests/test_ranking_fidelity.py
  python -m datdmpc.diagnostics.ranking_fidelity --ckpt checkpoints/mt30-5M.pt --task walker-walk --shift <dev level spec from configs/shifts.yaml> --states <N> --candidates <M> --horizon <H> --seed 2000 --out outputs/debug/ --embedding outputs/debug/<adapt run_id>/adapted_embedding.json --tier T0 --device cpu
  ```

  Colab (reported; task, shift and seed must match the T204 run that produced the embedding):

  ```python
  !python -m datdmpc.diagnostics.ranking_fidelity --ckpt /content/drive/MyDrive/DA-TDMPC2/checkpoints/mt30-19M.pt --task <study task> --shift <test level spec> --states <N> --candidates <M> --horizon <H> --seed <test seed> --out /content/drive/MyDrive/DA-TDMPC2/results/P2_ranking_after_adapt/ --embedding results/P2_adapt/<run_id>/adapted_embedding.json --tier T1 --device cuda
  ```

- **Done when:**
  - [ ] Test: loading an embedding changes only row `task_idx` of `_task_emb.weight`; every other parameter is bit-identical.
  - [ ] Test: with and without `--embedding`, the sampled start states (simulator states) are identical for the same seed.
  - [ ] `results/P2_ranking_after_adapt/` holds a run folder for every T204 (study task × test level × seed) whose embedding exists, each `config.yaml` citing the source `adapted_embedding.json` path, N, M, H equal to the T104 pre-registration.
  - [ ] The handoff log pairs each T205 run with its T104 run (same task, shift, seed) for M1's figures.
- **Faculty-report sentence:** "Completed T205: after `e`-only adaptation, Kendall τ on `<task>` under `<shift spec>` moves from `<kendall_tau_mean, results/P1_ranking/<run_id>/summary.json>` to `<kendall_tau_mean, results/P2_ranking_after_adapt/<run_id>/summary.json>`."

### T304

**Closed-loop detect→adapt evaluation → `results/P3_closedloop/`**

- **Goal:** Ours-C2+C3: a shift is injected mid-episode; the C3 detector (M3, `datdmpc.detect`) monitors
  the model's own signals; when it fires, `e`-only adaptation (M2, `datdmpc.adapt.embedding`) updates the
  task's embedding row (64 numbers for mt30-5M/19M, per `common/parser.py`) from the K most recent
  transitions, and planning continues with the adapted row. Evaluated on held-out test levels only.
- **Depends on:** T303, T204
- **Target date:** Tue 2026-12-01 (experiment freeze Wed 2026-12-02)
- **Compute tier + budget:** `N_task × N_shift,test × N_seed × N_ep × (L × (s_plan + s_signal) + n_adapt ×
  s_adapt) / 3600` hours, with `s_plan`, `s_adapt` from T008 for the tier used, `s_signal` (per-step
  detector overhead) measured from T301/T302 outputs, and `n_adapt` the number of adaptation calls per
  episode set by the adapt config. > 3 laptop-hours → T1, sharded across the M1/M2/M3 accounts with
  `--shard i/3 --resume`, logged in the compute log above.
- **Files to create/modify:** `src/datdmpc/closed_loop.py`, `tests/test_closed_loop.py`,
  `configs/experiments/M1_*.yaml`, `notebooks/colab/M1_*.ipynb`, `results/P3_closedloop/**`. M2/M3 code
  is used only through their public functions; any change there is requested by issue.
- **Interface (binding):** `python -m datdmpc.closed_loop --ckpt --task --shift --inject-at STEP
  --detector-config ... --adapt-config ... --seeds ... --episodes --out results/P3_closedloop/ [--resume]
  [--shard i/N]` (plus `--tier`, `--device`).
- **Exact commands:**

  ```powershell
  pytest -q tests/test_closed_loop.py
  python -m datdmpc.closed_loop --ckpt checkpoints/mt30-5M.pt --task walker-walk --shift <dev level spec from configs/shifts.yaml> --inject-at <STEP> --detector-config configs/experiments/M3_detector.yaml --adapt-config configs/experiments/M2_adapt.yaml --seeds 2000 --episodes 1 --out outputs/debug/ --tier T0 --device cpu
  ```

  Colab (one shard per account; `i` = 1, 2, 3):

  ```python
  !python -m datdmpc.closed_loop --ckpt /content/drive/MyDrive/DA-TDMPC2/checkpoints/mt30-19M.pt --task <study task> --shift <test level spec from configs/shifts.yaml> --inject-at <STEP> --detector-config configs/experiments/M3_detector.yaml --adapt-config configs/experiments/M2_adapt.yaml --seeds <test seeds from PROJECT_PLAN> --episodes <N_ep from PROJECT_PLAN> --out /content/drive/MyDrive/DA-TDMPC2/results/P3_closedloop/ --resume --shard <i>/3 --tier T1 --device cuda
  ```

  Then copy the finished run folders into `results/P3_closedloop/` on the laptop and commit them.
- **Done when:**
  - [ ] Test (tiny model): no adaptation happens before the detector fires; after it fires, only the current task's embedding row changes and every other parameter is bit-identical.
  - [ ] Test: with the detector disabled, the closed loop reproduces B0 for the same seed (same per-episode returns).
  - [ ] Test: `--resume` skips finished episodes; `--shard` splits deterministically.
  - [ ] `results/P3_closedloop/` contains a complete run folder (five files) for every (study task × test level × seed) in the plan, produced on T1 (`env.txt`), with detection step, adaptation count and adaptation wall-time in `summary.json`.
  - [ ] Only test levels and test seeds 0–99 were used; dev levels/seeds appear only in `outputs/debug/`.
  - [ ] MPPI settings in every `config.yaml` equal upstream.
- **Faculty-report sentence:** "Completed T304: with detection-triggered `e`-only adaptation, frozen mt30-19M recovers `<gap recovery from results/P3_closedloop/<run_id>/summary.json>` of the nominal–shifted gap on `<task>` under `<shift spec>`, detecting the shift `<detection delay from the same file>` steps after injection."

### T401

**C1 design note + differentiation vs TD-GRPC/BMPC/TD-M(PC)² (pilot T402/T403 only if G2 passed by Nov 17)**

- **Goal:** `docs/design/C1_ranking.md` — what T104/T205 show about ranking errors under shift, a
  concrete ranking-aware objective that could fix them (implemented only by subclassing in
  `src/datdmpc/ranking/`, never by editing upstream), the H5 pre-registration, and an explicit
  differentiation from the closest work. With 6 weeks, C1 is expected to remain this design note plus the
  diagnostic.
- **Depends on:** T104 (drafting can start after G1, Tue 2026-11-03)
- **Target date:** Wed 2026-12-02 (experiment freeze; G4 decided the same day)
- **Compute tier + budget:** none for the note. Pilot (only if approved): finetuning runs on T1,
  budget `N_task × N_seed × n_grad_steps × s_grad,full / 3600` + evaluation by the
  [PROJECT_PLAN §11.2](../PROJECT_PLAN.md) formula, `s_grad,full` from T008.
- **Files to create/modify:** `docs/design/C1_ranking.md`; only if the pilot is approved:
  `src/datdmpc/ranking/**`, `tests/test_ranking.py`, `configs/experiments/M1_*.yaml`,
  `notebooks/colab/M1_*.ipynb`, and a pilot results folder that M1 first adds to the ownership table.
- **Differentiation table (in the note; citations stay marked until a team member has read the paper —
  M2's T009 summaries in [RELATED_WORK](../RELATED_WORK.md) are the source):**

  | Work | What it changes | Signal used | How C1 differs |
  |---|---|---|---|
  | TD-GRPC (arXiv:2505.13549) <!-- VERIFY citation --> | `<from T009>` | `<from T009>` | `<written in T401>` — closest to C1 |
  | BMPC — Bootstrapped MPC (Wang et al., ICLR 2025) <!-- VERIFY citation --> | `<from T009>` | `<from T009>` | `<written in T401>` |
  | TD-M(PC)² (Lin et al., arXiv:2502.03550) <!-- VERIFY citation --> | `<from T009>` | `<from T009>` | `<written in T401>` |

- **Pilot rule:** T402/T403 exist only if G2 is marked Passed in STATUS by Tue 2026-11-17. Then the H5
  thresholds (minimum Kendall τ gain and return non-inferiority margin, `[[pre-register before run]]`) are
  proposed in this note and copied into PROJECT_PLAN by M1 **before any pilot run**; the design is fixed
  before Tue 2026-11-24 (stop rule: no new ideas after Nov 24); all pilot runs finish before the freeze
  Wed 2026-12-02. If G2 fails or is late, the note says so and C1 = T104 + T205 + this note.
- **Exact commands:**

  ```powershell
  Select-String -Path docs\design\C1_ranking.md -Pattern "VERIFY"
  git diff --name-only origin/main...
  ```

- **Done when:**
  - [ ] `docs/design/C1_ranking.md` is merged with: evidence section citing `results/P1_ranking/` and `results/P2_ranking_after_adapt/` paths (no uncited numbers), proposed objective, differentiation table, H5 placeholders or pre-registered values, and the G2/G4 decision record.
  - [ ] Each related-work row is either backed by a T009 summary (marker removed) or still marked `VERIFY citation`.
  - [ ] If the pilot ran: `tests/test_ranking.py` passes, results are in the M1-approved pilot folder, and H5 values were on `main` before the first pilot run.
  - [ ] No file under `third_party/` was modified (`git diff --name-only origin/main... -- third_party` prints nothing).
- **Faculty-report sentence:** "Completed T401: C1 design note with differentiation from TD-GRPC, BMPC and TD-M(PC)² (`docs/design/C1_ranking.md`); the ranking-loss pilot `<ran / was not run because G2 was not passed by 2026-11-17>`."

### T503

**(shared, all) Clean-clone reproducibility check of one result per contribution**

- **Goal:** from a fresh clone at a tagged commit, re-run one committed result per contribution (C2:
  `results/P2_adapt/`, C3: `results/P3_detect/`, ranking-fidelity diagnostic: `results/P1_ranking/`) and
  confirm it matches. Proposed split (confirm at G3, Tue 2026-11-24): each member reproduces a result
  produced by someone else; M1 coordinates and records the outcome.
- **Depends on:** T204, T303
- **Target date:** Sun 2026-12-06
- **Compute tier + budget:** the tier of the original run (from its `env.txt`); hours from the original
  run's `episodes.csv` `wall_time_s` sum.
- **Files to create/modify:** `docs/RUNS.md` (Step 5 procedure and acceptance criterion, written
  before the check: `[[pre-register before run]]`), this page (handoff entry). Reproduced output goes to
  the gitignored `outputs/repro/`; nothing in `results/` is overwritten.
- **Exact commands** (same as [RUNS Step 5.2](../RUNS.md); a separate env so the main `datdmpc` env is
  untouched):

  ```powershell
  git clone https://github.com/Shahrcasm/tdmpc2-shift-adaptation.git C:\code\tdmpc2-repro
  cd C:\code\tdmpc2-repro
  git checkout <tag or SHA from the original run's git_sha.txt>
  conda create -n datdmpc-repro python=3.11 -y
  conda activate datdmpc-repro
  pip install torch==2.7.1 --index-url https://download.pytorch.org/whl/cpu
  pip install -r environment/requirements-cpu.txt
  pip install -e . --no-deps
  python scripts/get_checkpoints.py --models mt30-5M mt30-19M
  pytest -q
  python scripts/smoke_test.py
  ```

  Then re-run the exact command recorded in the original run's `config.yaml`, replacing only `--out`
  with `outputs/repro/<phase>/` (on Colab: the same with the Drive path).
- **Done when:**
  - [ ] The acceptance criterion is in [RUNS](../RUNS.md) before the first reproduction run.
  - [ ] One result per contribution is reproduced and meets the criterion; the comparison (original vs reproduced `summary.json` paths) is in each member's handoff log.
  - [ ] Any mismatch is either explained and fixed, or reported honestly in the report.
- **Faculty-report sentence:** "Completed T503: from a clean clone at `<tag>`, `<result>` was reproduced within the pre-registered criterion (`<original summary.json path>` vs `<reproduced summary.json path>`)."

### T504

**(shared, all) Full draft → faculty feedback → final submission**

- **Goal:** submit the report on time with every number traceable to `results/`. Milestones: full draft
  Tue 2026-12-08 → faculty feedback → final Sun 2026-12-13 → submission Mon 2026-12-14. M1 assembles
  `report/main.tex`, writes `*_M1.tex` sections, and regenerates registry and figures last.
- **Depends on:** T503
- **Target date:** Mon 2026-12-14
- **Compute tier + budget:** none (no new experiments after the freeze, Wed 2026-12-02).
- **Files to create/modify:** `report/main.tex`, `report/sections/*_M1.tex`, `results/REGISTRY.csv`,
  `figures/**`, `docs/STATUS.md`.
- **Exact commands:**

  ```powershell
  python scripts/build_registry.py --results results --out results/REGISTRY.csv
  python scripts/make_figures.py --registry results/REGISTRY.csv --out figures
  Select-String -Path report\main.tex, report\sections\*.tex -Pattern "VERIFY", "\[\["
  git status --short
  ```

- **Done when:**
  - [ ] The full draft is sent to the faculty by Tue 2026-12-08.
  - [ ] The marker search prints nothing: no `VERIFY` marker and no `[[...]]` placeholder remains in the report.
  - [ ] Every number in the report is traceable to `results/REGISTRY.csv` or a cited `results/` path; every figure was regenerated from the final registry.
  - [ ] Every citation has been read by a team member (no `VERIFY citation` left).
  - [ ] The submitted version is tagged on `main` and recorded in STATUS.
- **Faculty-report sentence:** "Completed T504: final report submitted on `<date>`; all numbers regenerated from `results/REGISTRY.csv` at commit `<sha>`."
