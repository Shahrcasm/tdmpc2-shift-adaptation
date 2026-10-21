# STATUS — DA-TDMPC2 Task Board and Single Source of Truth

> **Rule: members never edit this file.** M2 and M3 update only their own team page
> ([M2_Ishtiak](team/M2_Ishtiak.md), [M3_Talha](team/M3_Talha.md)); M1 updates
> [M1_Shahriar](team/M1_Shahriar.md). M1 (integrator, and the only member who merges into `main`) syncs
> this file **at merge time only**, in a separate commit `T000: sync status` on `dev_shahriar`, copying
> statuses, evidence paths and handoff entries from the team pages. That commit reaches `main` through a
> PR titled `T000: sync status`, which M1 merges once CI is green (no other approval needed); several
> merges on the same day may share one sync. Nobody pushes to `main` directly. If this file and a team page disagree, the team page is the newer record and M1 fixes this
> file at the next sync. Rules of engagement: [AGENTS.md](../AGENTS.md). Plan, hypotheses and gates in
> detail: [PROJECT_PLAN.md](PROJECT_PLAN.md).

| Field | Value |
|---|---|
| Project | **DA-TDMPC2 — Detect-and-Adapt TD-MPC2** (CSE 465 — Pattern Recognition and Neural Network) |
| Current week · phase | Week 1 (Oct 21 – Oct 27) · **P0 Setup & reproduction** |
| Next gate | **G0 — Tuesday 2026-10-27** |
| Days to experiment freeze (Wed 2026-12-02) | 42 |
| Days to final submission (Mon 2026-12-14) | 54 |
| Last synced | 2026-10-21 (T001 bootstrap, M1) |

Day counts are computed on the "Last synced" date and go stale between syncs; M1 recomputes them at every
sync.

---

## 1. Gates

Gates are decided by all three members on the gate date. Status values: **Pending** / **Passed** /
**Failed→fallback** (name the fallback taken). On a decision, M1 tags the merge commit on `main`
(`g0`, `g1`, `g2`, `g3`, `g4`) and records the evidence path.

**Pre-registration.** Thresholds marked `[[...]]` are proposed by the owner in their design note (C2 →
M2 in T201, C3 → M3 in T302, C1 → M1 in T401) and copied by M1 into the pre-registration table of
[PROJECT_PLAN.md](PROJECT_PLAN.md) in the same merge, **before** any corresponding run. A run whose
threshold is not yet in PROJECT_PLAN.md on `main` must not start.

| Gate | Criterion (from the roadmap) | Fallback if failed | Date | Status | Evidence |
|---|---|---|---|---|---|
| G0 | Harness evaluates one mt30 task (single task of a multitask checkpoint, T006); sec/step known on laptop **and** Colab (T008) | Decided by all three at the gate; see the risk register in [PROJECT_PLAN.md](PROJECT_PLAN.md) | Tue 2026-10-27 | Pending | `results/P0_profile/<run_id>/summary.json` · T006 PR #`<n>` |
| G1 | ≥3 shift types give clear drops (non-overlapping 95% CIs) on ≥3 study tasks | Raise shift severity (new levels in `configs/shifts.yaml`, T102) and re-run | Tue 2026-11-03 | Pending | `results/P1_degradation/<run_id>/summary.json` |
| G2 | Pre-registered recovery threshold (H2: `[[X]]`% gap recovery at ≤ `[[Y]]`% of full-finetune wall-time, K ≤ `[[K_max]]`) met on mass and friction, held-out levels | Adapt `e` + LayerNorm affine parameters (`scripts/adapt.py --method e_ln`); report the `e`-only result honestly | Tue 2026-11-17 | Pending | `results/P2_adapt/<run_id>/summary.json` |
| G3 | Pre-registered detection targets (H4: AUROC ≥ `[[A]]`, false alarms ≤ `[[F]]` per 1,000 nominal steps, delay ≤ `[[D]]` steps) met on ≥2 shift types | Present C3 as an analysis (no detection claim) | Tue 2026-11-24 | Pending | `results/P3_detect/<run_id>/summary.json` |
| G4 (stretch) | C1 ranking-loss pilot (H5): ranking auxiliary loss raises Kendall τ without lowering return at matched steps/seeds. Pilot (T402/T403) runs **only if G2 passed by 2026-11-17** | C1 remains the ranking-fidelity diagnostic + design note (T104, T205, T401) | Wed 2026-12-02 (freeze) | Pending | `docs/design/C1_ranking.md` · pilot result folder `<defined in T401 if G2 passed>` |

Experiment freeze: **Wed 2026-12-02**. After the freeze only writing (T504) and the clean-clone
reproducibility check (T503) are scheduled.

---

## 2. Task board (grouped by member)

Status values: **To Do** / **In Progress** / **Done** / **Blocked** (state the blocker in the handoff
log). "Done by & date" is filled by M1 at merge time. Evidence is a `results/` path or the PR number;
result folders follow the ownership table in [PROJECT_PLAN.md](PROJECT_PLAN.md) and
[AGENTS.md](../AGENTS.md).

**Dependency check.** The dependency graph of the seed board below was checked for cycles: it is
**acyclic** (a topological order exists: T001 → T002, T003, T004, T009 → T005 → T006, T101 → T007, T008,
T104, T301 → T102 → T103, … → T503 → T504). Every dependency's target date is on or before the
dependent task's target date.

**Task assignment.** M1 owns
infrastructure, the harness, shifts, the nominal evaluation (T007), the ranking-fidelity diagnostic
(T104, T205), the closed loop (T304), the C1 note (T401), registry/figures and report assembly; M2 owns
related work (T009), the degradation sweep (T103) and C2 (T201–T204); M3 owns profiling (T008) and C3
detection (T301–T303).

**Idle-risk mitigation (weeks 1–2).** M3 is blocked on T006 (target Oct 26) between finishing T004
(Oct 23) and starting T008. Mitigation, written into M3's task cards: from Oct 23, M3 develops
`scripts/profile.py`, the detection signals (`src/datdmpc/detect/signals.py`) and the EWMA/CUSUM
statistics against the `--mode tiny` random model of `scripts/smoke_test.py`, and reads upstream
`third_party/tdmpc2/tdmpc2/tdmpc2.py` and `third_party/tdmpc2/tdmpc2/common/world_model.py`. M2 has T009
until Oct 27; from Oct 28 until T102 lands (Oct 31) M2 prepares the T103 launcher, drafts the T201 note
and builds the T202 adaptation code against the tiny model (written into M2's page). No member is idle.

**Unblocked once T001 is merged:** T002 (M1), T003 (M2), T004 (M3), T009 (M2).

### M1 — Md. Shahriar Rakib Rabbi (`dev_shahriar`) · integrator

| Task ID | Task | Depends on | Target date | Status | Done by & date | Evidence |
|---|---|---|---|---|---|---|
| T001 | Repo scaffolding, vendored upstream at pinned SHA, all docs + `.github/` files | — | Oct 22 | In Progress | — | `third_party/tdmpc2/UPSTREAM_COMMIT.txt` · PR #`<n>` |
| T002 | Windows env setup (Python 3.11 venv) + smoke test on own laptop; record Windows version in team page | T001 | Oct 23 | To Do | — | [M1 team page](team/M1_Shahriar.md) handoff entry · PR #`<n>` |
| T005 | `scripts/get_checkpoints.py` + `checkpoints/MANIFEST.csv` (name, size, sha256, URL); upload to shared Drive | T002 | Oct 24 | To Do | — | `checkpoints/MANIFEST.csv`, `tests/test_get_checkpoints.py` · PR #`<n>` |
| T006 | Single-task-of-multitask evaluation harness + resume-safe logging + tests | T005 | Oct 26 | To Do | — | `tests/test_harness.py`, `tests/test_logging.py` · PR #`<n>` |
| T101 | Perturbation wrappers + tests proving the physical parameter changed | T002 | Oct 29 | To Do | — | `tests/test_perturb.py` · PR #`<n>` |
| T007 | Nominal eval of mt30-5M and mt30-19M on all 30 tasks (Colab, sharded); choose 4–6 study tasks by a rule written *before* looking at shifted results | T006, T003 | Oct 30 | To Do | — | `results/P0_nominal/<run_id>/` |
| T102 | `configs/shifts.yaml`: types × levels; split into dev vs held-out test levels | T101, T007 | Oct 31 | To Do | — | `configs/shifts.yaml` · PR #`<n>` |
| T104 | Ranking-fidelity diagnostic, nominal vs shifted | T006, T101 | Nov 3 | To Do | — | `results/P1_ranking/<run_id>/` |
| T501 | `build_registry.py` + `make_figures.py` (read `results/` only) | T103 | Nov 10 | To Do | — | `results/REGISTRY.csv`, `figures/`, `tests/test_registry.py` · PR #`<n>` |
| T502 | Report skeleton; M2/M3 write own `report/sections/*_<owner>.tex` from week 4 | T501 | Nov 12 | To Do | — | `report/main.tex` · PR #`<n>` |
| T205 | Ranking fidelity after C2 adaptation | T104, T202 | Nov 27 | To Do | — | `results/P2_ranking_after_adapt/<run_id>/` |
| T304 | Closed-loop detect→adapt evaluation | T303, T204 | Dec 1 | To Do | — | `results/P3_closedloop/<run_id>/` |
| T401 | C1 design note + differentiation vs TD-GRPC/BMPC/TD-M(PC)² (pilot T402/T403 only if G2 passed by Nov 17) | T104 | Dec 2 | To Do | — | `docs/design/C1_ranking.md` · PR #`<n>` |

### M2 — Md. Ishtiak Ahmed Moyen (`dev_ishtiak`)

| Task ID | Task | Depends on | Target date | Status | Done by & date | Evidence |
|---|---|---|---|---|---|---|
| T003 | Windows env setup (Miniconda) + smoke test on own laptop; record Windows version (`winver`) in team page | T001 | Oct 23 | To Do | — | [M2 team page](team/M2_Ishtiak.md) handoff entry · PR #`<n>` |
| T009 | `docs/RELATED_WORK.md`: read guardrail papers, 2–3 sentences each in own words | T001 | Oct 27 | To Do | — | `docs/RELATED_WORK.md` · PR #`<n>` |
| T103 | Degradation sweep of B0 | T102, T006 | Nov 3 | To Do | — | `results/P1_degradation/<run_id>/` |
| T201 | Design note C2 (loss, optimizer, K grid, steps, norm constraint, online vs batch, differentiation) + pre-registered H2 thresholds | T103 | Nov 5 | To Do | — | `docs/design/C2_embedding_adaptation.md` · PR #`<n>` |
| T202 | `adapt/embedding.py` + test proving only `e` changes | T201 | Nov 8 | To Do | — | `tests/test_embedding.py` · PR #`<n>` |
| T203 | Baselines B1/B2/B3 | T202 | Nov 11 | To Do | — | `tests/test_baselines.py` · PR #`<n>` |
| T204 | Main C2 sweep on held-out levels | T203, T102 | Nov 17 | To Do | — | `results/P2_adapt/<run_id>/` |

### M3 — Md. Abdullah Talha (`dev_talha`)

| Task ID | Task | Depends on | Target date | Status | Done by & date | Evidence |
|---|---|---|---|---|---|---|
| T004 | Windows env setup (Miniconda) + smoke test on own laptop; record Windows version (`winver`) in team page | T001 | Oct 23 | To Do | — | [M3 team page](team/M3_Talha.md) handoff entry · PR #`<n>` |
| T008 | Profiling: planning + adaptation sec/step on laptop vs Colab CPU/GPU | T006, T004 | Oct 27 | To Do | — | `results/P0_profile/<run_id>/` |
| T301 | Detection signal extraction | T006 | Nov 8 | To Do | — | `tests/test_signals.py` · PR #`<n>` (raw dumps in gitignored `outputs/signals/`) |
| T302 | Detector + calibration on nominal seeds; pre-registered H4 thresholds | T301 | Nov 13 | To Do | — | `docs/design/C3_detection.md` · `results/P3_detect/<run_id>/` (calibration) |
| T303 | Detection eval with mid-episode shift injection | T302, T102 | Nov 24 | To Do | — | `results/P3_detect/<run_id>/` |

T402/T403 (C1 pilot) are not on the seed board; M1 adds them here only if G2 is marked Passed by
2026-11-17.

### All members

| Task ID | Task | Depends on | Target date | Status | Done by & date | Evidence |
|---|---|---|---|---|---|---|
| T503 | Clean-clone reproducibility check of one result per contribution | T204, T303 | Dec 6 | To Do | — | Handoff log entry citing the reproduced `results/` paths · PR #`<n>` |
| T504 | Full draft (Tue Dec 8) → faculty feedback → final (Sun Dec 13) → submission (Mon Dec 14) | T503 | Dec 14 | To Do | — | `report/main.tex` · PR #`<n>` |

---

## 3. Decisions pending with faculty

Open items to settle with Dr. Mohammad Ashrafuzzaman Khan. Until decided, the generated docs carry the
placeholder shown; M1 replaces it everywhere once decided and records the decision date here.

| Item | Placeholder used in docs | Where it appears | Status | Decided on |
|---|---|---|---|---|
| Final report template | `[[report template: IEEE conference unless the course specifies otherwise]]` | `report/main.tex`, [PROJECT_PLAN.md](PROJECT_PLAN.md) | Open | — |
| Weekday of the weekly faculty update | `[[weekday]]` | Team pages ([M1](team/M1_Shahriar.md), [M2](team/M2_Ishtiak.md), [M3](team/M3_Talha.md)) | Open | — |

---

## 4. Open corrections

| Item | Issue | Action | Owner | Status |
|---|---|---|---|---|
| GitHub repository description | Says "~96-parameter embedding update". For our checkpoints `mt30-5M` and `mt30-19M` the task embedding is **64-dimensional**: `third_party/tdmpc2/tdmpc2/common/parser.py` sets `cfg.task_dim = 96 if cfg.task == 'mt80' or cfg.get('model_size', 5) in {1, 317} else 64`. C2 therefore adapts one row of the embedding table = 64 numbers. (The TD-MPC2 paper lists 96 for all sizes; the code is authoritative for the released mt30 checkpoints.) | Change the description to "64-number embedding update" (checklist item in [REPO_SETUP.md](REPO_SETUP.md)). T006 asserts `model._task_emb.weight.shape == (30, 64)` after loading. | M1 | Open |

---

## 5. Compute ledger

One row per sweep shard (or per single run on Colab). Estimated hours come from the budget formula in the
task card (`#tasks × #shifts × #seeds × #episodes × steps × sec/step`, sec/step from T008); actual hours
from the run's `episodes.csv` (`wall_time_s`). Tier: T0 laptop · T1 Colab free · T1b Kaggle backup.
Shard uses the `--shard i/N` value of the run. Planning procedure: [RUNS.md](RUNS.md).

| Run family | Task ID | Tier | Colab account (M1/M2/M3) | Shard | Estimated hours | Actual hours | Notes |
|---|---|---|---|---|---|---|---|
| | | | | | | | |
| | | | | | | | |
| | | | | | | | |

---

## 6. Global handoff log (reverse-chronological)

Newest entry first. M1 copies entries from the team pages at each sync. Format:

`date · member · task · what was done · files changed · result path · blockers · next step`

| Date | Member | Task | What was done | Files changed | Result path | Blockers | Next step |
|---|---|---|---|---|---|---|---|
| 2026-10-21 | M1 | T001 | Bootstrap scaffolding (docs, `.github/` files, package skeleton with owner stubs, tiny smoke test, vendored upstream at pinned commit) | Root files (`AGENTS.md`, `CLAUDE.md`, `README.md`, `LICENSE`, `.gitignore`, `.gitattributes`, `pyproject.toml`); folders `.github/`, `.cursor/`, `docs/`, `environment/`, `src/`, `scripts/`, `tests/`, `third_party/` | — | none | T002 |
