# M2 — Md. Ishtiak Ahmed Moyen

> Only M2 edits this page. Statuses, handoff entries and compute use recorded here are copied into
> [STATUS](../STATUS.md) by M1 at merge time (`T000: sync status`). Rules: [AGENTS.md](../../AGENTS.md).
> Science, hypotheses and metrics: [PROJECT_PLAN](../PROJECT_PLAN.md). Commands and environment:
> [RUNS](../RUNS.md). C2 design: [C2 design note](../design/C2_embedding_adaptation.md) (written in T201).

| Field | Value |
|---|---|
| Name | Md. Ishtiak Ahmed Moyen |
| Slot · Student ID | M2 · 2131580642 |
| Branch | `dev_ishtiak` |
| Role | **C2 embedding adaptation** · baselines · degradation sweep · related work (I never click Merge; M1 merges every PR) |
| Components | B0 degradation sweep (T103), C2 design note and pre-registration of H2/H3 (T201), `e`-only adaptation (T202), baselines B1/B2/B3 (T203), main C2 sweep on held-out levels (T204), related work (T009) |
| Laptop | Native Windows (edition/version/build recorded in [Record: my laptop](#record-my-laptop), T003); Miniconda env `datdmpc`; PowerShell 5.1; repo at `C:\code\tdmpc2-shift-adaptation` |
| Colab account | M2 (one of the three parallel accounts) |

**Strictly owned files** (binding table: [AGENTS.md §2](../../AGENTS.md)); I edit nothing else:

- `src/datdmpc/adapt/**` (`embedding.py`, `baselines.py`, `__init__.py`)
- `scripts/adapt.py`
- `tests/test_embedding.py`, `tests/test_baselines.py`
- `configs/experiments/M2_*.yaml`
- `notebooks/colab/M2_*.ipynb` (launchers only; logic lives in `src/`)
- `results/P1_degradation/**` (T103), `results/P2_adapt/**` (T204)
- `report/sections/*_M2.tex` (from week 4)
- `docs/RELATED_WORK.md` (T009), `docs/design/C2_embedding_adaptation.md` (T201)
- `docs/team/M2_Ishtiak.md` (this page)

The T001 stubs of `src/datdmpc/adapt/embedding.py`, `src/datdmpc/adapt/baselines.py` and
`scripts/adapt.py` were created by M1 and are mine from the moment `dev_ishtiak` exists. Their CLI is the
binding interface in [AGENTS.md §5](../../AGENTS.md); changing it needs my PR that also updates that table
and [RUNS](../RUNS.md) (via M1 for M1-owned docs). I never edit `third_party/`, `docs/STATUS.md`,
`docs/PROJECT_PLAN.md`, `configs/shifts.yaml`, `scripts/eval.py`, `results/REGISTRY.csv` or `figures/`;
requests to their owners go through an issue or my [Handoff Log](#handoff-log).

---

## My Tasks

Status values: To Do / In Progress / Done / Blocked. "Depends on" tasks must be Done in
[STATUS](../STATUS.md) before I start.

| ID | Task | Depends on | Target date | Status |
|---|---|---|---|---|
| [T003](#t003) | Windows env setup (Miniconda) + smoke test on own laptop; record Windows version (`winver`) | T001 | Fri 2026-10-23 | To Do |
| [T009](#t009) | `docs/RELATED_WORK.md`: read the guardrail papers, 2–3 sentences each in own words | T001 | Tue 2026-10-27 | To Do |
| [T103](#t103) | Degradation sweep of B0 → `results/P1_degradation/` | T102, T006 | Tue 2026-11-03 | To Do |
| [T201](#t201) | C2 design note + pre-registered H2 (and H3) thresholds | T103 | Thu 2026-11-05 | To Do |
| [T202](#t202) | `adapt/embedding.py` + test proving only `e` changes | T201 | Sun 2026-11-08 | To Do |
| [T203](#t203) | Baselines B1/B2/B3 | T202 | Wed 2026-11-11 | To Do |
| [T204](#t204) | Main C2 sweep on held-out test levels → `results/P2_adapt/` | T203, T102 | Tue 2026-11-17 | To Do |
| [T503](#t503) | (shared, all) Clean-clone reproducibility check of one result per contribution | T204, T303 | Sun 2026-12-06 | To Do |
| [T504](#t504) | (shared, all) Full draft → faculty feedback → final submission | T503 | Mon 2026-12-14 | To Do |

**Week 1–2 plan (no idle days).** T003 first (Oct 22–23), then T009 (due Tue 2026-10-27). T103 can start
only after M1's T102 (target Sat 2026-10-31), which needs M1's nominal evaluation T007 (study tasks,
`results/P0_nominal/`). From Wed 2026-10-28 until then, without a checkpoint: prepare the T103 Colab
launcher `notebooks/colab/M2_degradation.ipynb`; draft the T201 design-note sections that do not depend on
T103 results ([C2 note](../design/C2_embedding_adaptation.md)); and build the `e`-only adaptation code and
its "only `e` changes" test against the random tiny model of `scripts/smoke_test.py --mode tiny`
(`datdmpc._upstream.make_tiny_cfg` + `build_world_model`), committing as `T202: wip – …` on `dev_ishtiak`.

**Merging.** I work only on `dev_ishtiak` and open a PR to `main` for each task; M1 reviews, approves and
merges it. I never click Merge. M1 merges his own PRs (including `T000: sync status`) without my approval;
I may still read them and leave comments, e.g. if STATUS copies my team page incorrectly (statuses,
evidence paths, compute log).

---

## Record: my laptop

Filled in during [T003](#t003). Values are copied from the commands shown, not typed from memory.

| Field | Value | Source |
|---|---|---|
| Windows edition | `<edition from winver>` | `winver` |
| Windows version | `<version from winver>` | `winver` |
| OS build | `<OS build from winver>` | `winver` |
| OsName · OsVersion · OsBuildNumber | `<output>` | `Get-ComputerInfo -Property OsName, OsVersion, OsBuildNumber` |
| Laptop model | `<output>` (bootstrap brief: Lenovo IdeaPad 320; confirm) | `Get-ComputerInfo -Property CsModel` |
| CPU | `<output>` (bootstrap brief: Core i3, 2 cores / 4 threads; confirm) | `(Get-CimInstance Win32_Processor).Name` |
| RAM | `<output>` (bootstrap brief: 12 GB; confirm) | `Get-ComputerInfo -Property CsTotalPhysicalMemory` |
| conda | `<output>` | `conda --version` |
| Python | `<output>` (must be 3.11) | `python --version` |
| torch · numpy · mujoco · dm-control | `<versions>` (must match `environment/requirements-cpu.txt`) | `pip show torch numpy mujoco dm-control` |
| `MUJOCO_GL` in effect during the smoke test | `<value printed as mujoco_gl by the smoke test>` | `python scripts/smoke_test.py --mode tiny` |
| Smoke test (tiny) | `<pass/fail, date>` | exit code of the command above |
| `pytest -q` | `<pass/fail, date>` | exit code of `pytest -q` |
| Recorded on | `<date>` | — |

The sec/step printed by the smoke test is a debugging figure and is not recorded here; budgets use T008
(`results/P0_profile/`).

---

## Weekly Faculty Update

For Dr. Mohammad Ashrafuzzaman Khan, due every **`[[weekday]]`** (open item in
[STATUS](../STATUS.md), "Decisions pending with faculty").

Rules: 3–5 bullets, **each quoting a hard number copied from a file under `results/` and cited by its
path**, plus exactly one "blocker / help needed" bullet. A week without results reports completed tasks
with their evidence (PR number, file path) and no numbers. Laptop numbers are never quoted, except T0
CPU wall-time measurements labelled as such.

Format example (placeholders only, never replaced by invented values):

> **Week `<n>` (`<date>`) — M2, Md. Ishtiak Ahmed Moyen**
> - T009: related-work summaries for `<n>` guardrail papers are in `docs/RELATED_WORK.md` (PR #`<n>`).
> - T103: frozen mt30-19M retains `<retention from results/P1_degradation/<run_id>/summary.json>` of nominal return under `<shift spec>` on `<task>`.
> - T204: `e`-only adaptation (64 parameters) recovers `<gap recovery from results/P2_adapt/<run_id>/summary.json>` of the nominal–shifted gap on `<task>` under held-out `<shift spec>`, versus `<gap recovery from results/P2_adapt/<run_id of full_ft>/summary.json>` for full finetuning.
> - T204 cost: adaptation wall-time on T0 CPU `<adapt_wall_time_s from results/P2_adapt/<run_id>/summary.json>` s for `e_only` vs `<adapt_wall_time_s>` s for `full_ft` (same file family, tier T0 in `env.txt`).
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
· blockers · next. At the end of each session also list the files changed (`git status --short` and
the commit list).

| Date | Task | What was done | Files changed | Result path | Blockers | Next |
|---|---|---|---|---|---|---|
| `<YYYY-MM-DD>` | `T<ID>` | `<what was done>` | `<paths>` | `<results/... or —>` | `<blocker or none>` | `<next task>` |

---

## Task cards

Budget symbols (same quantities as [PROJECT_PLAN §11.2](../PROJECT_PLAN.md) and M1's page):
`N_task` tasks, `N_shift` shift levels, `N_method` methods, `N_seed` seeds, `N_ep` episodes per
(task, shift, method, seed), `L = 500` agent decisions per DMControl episode (action repeat 2, 500-step
timeout in `third_party/tdmpc2/tdmpc2/envs/dmcontrol.py`), `s_plan` = planning sec/decision and
`s_grad(method)` = seconds per adaptation gradient step, both from T008
(`results/P0_profile/<run_id>/summary.json`) for the tier and device actually used — never assumed.
`N_grad` = gradient steps per adaptation, `K` = transitions per adaptation. Rule: more than 3
laptop-hours → Colab (T1), split with `--shard i/3` across the M1/M2/M3 accounts, always `--resume`,
each sharded sweep recorded in the [Compute log](#compute-log). MPPI settings are never changed.

All PowerShell blocks assume:

```powershell
cd C:\code\tdmpc2-shift-adaptation
conda activate datdmpc
```

Colab cells follow the template in [RUNS](../RUNS.md) Step 3(b) (mount Drive, clone at a given commit,
install `environment/requirements-colab.txt`, copy checkpoints from
`/content/drive/MyDrive/DA-TDMPC2/checkpoints/`); only the run cells are shown below. Finished run folders
are copied from `/content/drive/MyDrive/DA-TDMPC2/results/<phase>/` into the same `results/<phase>/` path
of the laptop clone and committed (no file larger than 5 MB).

<a id="t003"></a>

### T003

**Windows env setup (Miniconda) + smoke test on own laptop; record Windows version (`winver`)**

- **Goal:** a working `datdmpc` environment on my native-Windows laptop that runs the tests and the tiny
  smoke test, with the laptop recorded in [Record: my laptop](#record-my-laptop).
- **Depends on:** T001
- **Target date:** Fri 2026-10-23
- **Compute tier + budget:** T0; install time only (no experiment).
- **Files to create/modify:** `docs/team/M2_Ishtiak.md` (this page: laptop record, status, handoff).
- **Exact commands** (PowerShell 5.1; install Git for Windows and Miniconda first, see
  [RUNS](../RUNS.md) Step 1 and its troubleshooting table):

  ```powershell
  git config --global core.longpaths true
  git clone https://github.com/Shahrcasm/tdmpc2-shift-adaptation.git C:\code\tdmpc2-shift-adaptation
  cd C:\code\tdmpc2-shift-adaptation
  git checkout dev_ishtiak
  conda create -n datdmpc python=3.11 -y
  conda activate datdmpc
  pip install torch==2.7.1 --index-url https://download.pytorch.org/whl/cpu
  pip install -r environment/requirements-cpu.txt
  pip install -e . --no-deps
  python scripts/smoke_test.py --mode tiny
  pytest -q
  python scripts/adapt.py --help
  winver
  Get-ComputerInfo -Property OsName, OsVersion, OsBuildNumber
  Get-ComputerInfo -Property CsModel
  (Get-CimInstance Win32_Processor).Name
  Get-ComputerInfo -Property CsTotalPhysicalMemory
  conda --version
  python --version
  pip show torch numpy mujoco dm-control
  ```

  Python 3.11 and the pins follow upstream `third_party/tdmpc2/docker/environment.yaml` (see
  `environment/requirements-cpu.txt`).
- **Done when:**
  - [ ] `python scripts/smoke_test.py --mode tiny` exits 0 on my laptop.
  - [ ] `pytest -q` passes on my laptop.
  - [ ] `python scripts/adapt.py --help` prints the interface and exits 0.
  - [ ] Every row of [Record: my laptop](#record-my-laptop) is filled from the command output, including the Windows version from `winver`.
  - [ ] Any install problem and its fix is in the handoff log (and reported to M1 if [RUNS](../RUNS.md) needs a new troubleshooting row).
- **Faculty-report sentence:** "Completed T003: `datdmpc` environment installed on M2's Windows laptop (`<Windows version from winver>`); tiny smoke test and test suite pass (PR #`<n>`)."

<a id="t007"></a>

### T009

**`docs/RELATED_WORK.md`: read the guardrail papers, 2–3 sentences each in own words**

- **Goal:** an authoritative, read-by-us summary of each novelty-guardrail paper with a verified
  citation, and for each the axis on which our work differs. These texts replace the "T009" cells and
  the `VERIFY citation` markers of [PROJECT_PLAN §6](../PROJECT_PLAN.md) (M1 copies them at merge).
- **Depends on:** T001
- **Target date:** Tue 2026-10-27
- **Compute tier + budget:** none (reading).
- **Files to create/modify:** `docs/RELATED_WORK.md`, this page.
- **Papers** (identifiers as given in the bootstrap prompt, not yet checked):
  <!-- VERIFY citation: all identifiers in this list come from the bootstrap prompt; confirm authors, title, venue/year and arXiv ID on each paper's own first page or arXiv abstract page, and find the full reference of AdaJEPA (none known yet); resolved in T009 -->
  - TD-M(PC)² (Lin et al., arXiv:2502.03550; L4DC 2026) — policy-constraint fix for value overestimation.
  - BMPC — Bootstrapped MPC (Wang et al., ICLR 2025) — policy imitates the MPC planner.
  - TD-GRPC (arXiv:2505.13549) — group-relative ranking of candidate trajectories; closest to C1.
  - JEPA-TTT (arXiv:2610.00722) and AdaJEPA — test-time training of latent world models under dynamics shift; closest to C2.
  - RMA (Kumar et al., 2021); "World Models as Reference Trajectories for Rapid Motor Adaptation" (arXiv:2505.15589).
  - Feng et al., 2023 — Finetuning Offline World Models in the Real World (uncertainty signals; cited by Hansen et al., 2024, App. J, Eq. 9).
  - Base paper, already verified: TD-MPC2 (Hansen, Su, Wang, ICLR 2024, arXiv:2310.16828; PDF in `docs/references/`).
- **Per-paper entry format:** full citation · what it adapts or learns · signals used · cost (training
  vs test time) · 2–3 sentences in my own words · "How we differ" (one sentence, for C1, C2 or C3) ·
  `Read by M2 on <date>`. Remove a paper's `VERIFY citation` marker only after reading it; a paper not
  read by the target date keeps its marker and is listed as a blocker.
- **Exact commands:**

  ```powershell
  Select-String -Path docs\RELATED_WORK.md -Pattern "VERIFY"
  git add docs/RELATED_WORK.md docs/team/M2_Ishtiak.md
  git commit -m "T009: summarise guardrail papers in RELATED_WORK"
  git push origin dev_ishtiak
  ```

- **Done when:**
  - [ ] Every paper above has an entry in the format above, written in my own words (no copied abstract text).
  - [ ] Every remaining `VERIFY` marker in `docs/RELATED_WORK.md` belongs to a paper not yet read, and is listed in the handoff entry.
  - [ ] The C2 differentiation against JEPA-TTT and AdaJEPA is stated concretely enough to reuse in T201.
  - [ ] The handoff entry asks M1 to copy the "T009" cells into PROJECT_PLAN §6.
- **Faculty-report sentence:** "Completed T009: `<n>` guardrail papers read and summarised in `docs/RELATED_WORK.md` (PR #`<n>`); closest neighbours: TD-GRPC for C1, JEPA-TTT/AdaJEPA for C2."

<a id="t103"></a>

### T103

**Degradation sweep of B0 → `results/P1_degradation/`**

- **Goal:** return of the frozen model (B0) on each study task at every shift level of
  `configs/shifts.yaml` (dev and held-out test splits), as evidence for H1 and gate G1 (≥3 shift types
  give clear drops, non-overlapping 95% CIs, on ≥3 tasks), and as the floor `R_shift` for T204.
- **Depends on:** T102, T006
- **Target date:** Tue 2026-11-03 (G1)
- **Compute tier + budget:** T1 if above 3 laptop-hours.
  `hours = N_task × N_shift × 1 × N_seed × N_ep × L × s_plan(mt30-19M, tier) / 3600` with
  `N_task` = study tasks from M1's T007, `N_shift` = all levels in `configs/shifts.yaml` (dev + test),
  `N_seed ≥ 3`, `N_ep ≥ 10`. `R_nominal` is taken from `results/P0_nominal/` (same checkpoint, seeds and
  episodes), not re-run.
- **Files to create/modify:** `notebooks/colab/M2_degradation.ipynb`,
  `configs/experiments/M2_degradation.yaml`, `results/P1_degradation/<run_id>/…`, this page.
- **H1 pre-registration (return part; before the first T103 run, on this page, copied by M1 into
  [PROJECT_PLAN §7.3](../PROJECT_PLAN.md)):**
  - Test for "monotonic with severity": `[[pre-register before run]]`
  - What counts as a "clear drop" beyond the G1 criterion: `[[pre-register before run]]`
  - Committed in PR #`<n>` on `<date>`.
- **Exact commands.** Colab, one cell per study task and account (`<study-task>` from M1's T007, `i` = 1, 2, 3):

  ```
  !python scripts/eval.py --ckpt checkpoints/mt30-19M.pt --task <study-task> --shifts-from configs/shifts.yaml --split dev --episodes 10 --seeds 0 1 2 --out /content/drive/MyDrive/DA-TDMPC2/results/P1_degradation/ --resume --shard <i>/3 --tier T1 --device cuda
  !python scripts/eval.py --ckpt checkpoints/mt30-19M.pt --task <study-task> --shifts-from configs/shifts.yaml --split test --episodes 10 --seeds 0 1 2 --out /content/drive/MyDrive/DA-TDMPC2/results/P1_degradation/ --resume --shard <i>/3 --tier T1 --device cuda
  ```

  Laptop single-episode check (debugging only):

  ```powershell
  python scripts/eval.py --ckpt checkpoints/mt30-5M.pt --task <study-task> --shift mass:1.5 --episodes 1 --seed 0 --out outputs/debug/ --resume
  ```

  B0 results on **test** levels are evaluation-only floors for T204; they are never used to choose `K`,
  `N_grad` or the learning rate (those come from dev levels and dev seeds 2000–2099 in T201).
- **Done when:**
  - [ ] The H1 return criteria above are on `main` before the first T103 run.
  - [ ] `results/P1_degradation/` has a complete run folder for every (study task, level, seed) of both splits, each with `config.yaml`, `episodes.csv`, `summary.json`, `env.txt` (tier T1/T1b), `git_sha.txt`.
  - [ ] The G1 evaluation (which shift types and tasks show non-overlapping 95% CIs against `results/P0_nominal/`) is written in the handoff entry with the `summary.json` paths, for the gate meeting on Tue 2026-11-03.
  - [ ] If G1 fails, the request for higher severity levels is sent to M1 (T102) and the affected cells are re-run.
- **Faculty-report sentence:** "Completed T103: frozen mt30-19M retains `<retention>` of nominal return under `<shift spec>` on `<task>` (`results/P1_degradation/<run_id>/summary.json`)."

<a id="t201"></a>

### T201

**Design note C2 + pre-registered H2 (and H3) thresholds → `docs/design/C2_embedding_adaptation.md`**

- **Goal:** fix every design choice of `e`-only adaptation **before** any T204 run, using only dev levels
  and dev seeds (2000–2099), and pre-register the H2 and H3 thresholds (procedure:
  [PROJECT_PLAN §7.3](../PROJECT_PLAN.md); M1 copies the values into the pre-registration table).
- **Depends on:** T103
- **Target date:** Thu 2026-11-05
- **Compute tier + budget:** dev tuning on dev levels. `hours = N_task_dev × N_shift_dev × |K grid| ×
  |N_grad grid| × |lr grid| × N_seed_dev × (K × s_plan + N_grad × s_grad(e_only) + N_ep × L × s_plan) / 3600`
  (collection of K transitions + adaptation + evaluation). T0 if ≤ 3 laptop-hours, else T1 sharded.
- **Files to create/modify:** `docs/design/C2_embedding_adaptation.md`,
  `configs/experiments/M2_c2_dev.yaml` (grid), `notebooks/colab/M2_c2_dev.ipynb`, this page.
  Dev-tuning runs write to `results/P2_adapt/` and are identified by dev seeds (2000–2099) and dev levels
  in their `run_id`/`config.yaml`; they are never reported as test results.
- **Facts the note builds on** (verified in `third_party/tdmpc2/`):
  - `self._task_emb = nn.Embedding(len(cfg.tasks), cfg.task_dim, max_norm=1)` (`tdmpc2/common/world_model.py`);
    for mt30-5M/19M `task_dim = 64` (`tdmpc2/common/parser.py`), table 30 × 64, so **one task's `e` is
    64 numbers**. Upstream initialises embeddings uniformly in [-0.02, 0.02] (`tdmpc2/common/init.py`).
  - `e` is concatenated to the input of the encoder, dynamics, reward, policy prior and every Q head
    (`world_model.py`), so changing `e` changes all five components at once.
  - Upstream loss (`tdmpc2/tdmpc2.py` `_update`): `consistency_coef · Σ_t ρ^t MSE(d(z_t,a_t,e), h(s_{t+1},e)) / H
    + reward_coef · Σ_t ρ^t CE(R̂_t, r_t) / H + value_coef · Σ_t ρ^t CE(Q̂_t, TD_target_t) / (H · num_q)`;
    targets `h(s_{t+1})` and `TD_target` are computed under `torch.no_grad()`; TD target uses `pi(next_z)`
    and the target Q-ensemble (`return_type='min'`) with the per-task discount.
  - Defaults (`tdmpc2/config.yaml`): `consistency_coef: 20`, `reward_coef: 0.1`, `value_coef: 0.1`,
    `rho: 0.5`, `horizon: 3`, `lr: 3e-4`, `grad_clip_norm: 20`, `batch_size: 256`, `dropout: 0.01`
    (Q heads), `episodic: false` (termination loss inactive). Upstream optimises with Adam and calls
    `self.model.train()` during `_update` (dropout active).
  - Motivation: embedding similarity "appears to align more closely with task dynamics (embodiment,
    objects) than objective" (Hansen et al., 2024, §4.1, Fig. 7).
- **Decisions the note must fix** (each: choice · justification · dev evidence path if tuned):
  1. **Loss.** Default: reuse the upstream terms and coefficients (consistency 20, reward 0.1, value 0.1,
     ρ 0.5; `config.yaml`). Any change is justified with a dev-level result. Also fix: how the TD target
     is formed at test time (stop-gradient as upstream; recomputed each step with the current `e` or
     fixed at the initial `e`), and whether the target Q-ensemble stays frozen (no Polyak update).
  2. **Data and sequence structure.** How K transitions become length-H training windows (one
     contiguous segment of K transitions gives `K − H + 1` windows of H transitions with H = 3), mini-batch
     vs full batch per step.
  3. **Optimizer.** Adam (upstream) or SGD; learning rate grid on dev levels; gradient clipping
     (upstream `grad_clip_norm: 20`) kept or dropped; no weight decay on the embedding table (see 6).
  4. **K grid** (number of transitions) with upper bound `[[K_max]]`, and **gradient-step grid**
     (`N_grad`), both chosen on dev levels only.
  5. **Norm constraint.** `max_norm=1` renormalises the looked-up row **in place** at lookup time, so an
     optimizer step may leave the unit ball and the next lookup projects the row back: adaptation is
     effectively projected gradient descent on the unit ball. Decide: keep this behaviour (and save the
     projected row, norm ≤ 1) or adapt a separate 64-d parameter with explicit projection; log `‖e‖`
     of the checkpoint row and of the adapted row in `summary.json`.
     <!-- VERIFY: in torch 2.7.1, nn.Embedding with max_norm renormalises the looked-up rows in place under no_grad (gradient does not flow through the renormalisation), and its documentation requires cloning the weight if it is used in a differentiable op before the lookup; check the PyTorch docs/source in T201 -->
  6. **Which parameters require grad.** Only `model._task_emb.weight`, restricted to row `task_idx`
     (gradient mask, or a separate 64-d parameter written back into the row); every other parameter
     `requires_grad=False`. With Adam, rows that receive zero gradient stay unchanged only if there is no
     weight decay; the T202 test proves it.
  7. **Train vs eval mode** during adaptation (upstream `_update` uses train mode, Q-head dropout active).
  8. **Online vs batch.** Batch: B0 collects K transitions on the shifted env (behaviour policy = frozen
     planner, seed = adaptation seed), then `N_grad` steps on them, then `N_ep` evaluation episodes with
     the adapted `e`. Online: sliding window of the last K transitions, updates during the episode
     (closer to the closed loop, T304). State which one T204 uses; every method sees the identical K
     transitions for a given (task, level, seed).
  9. **Budget matching** (pre-registered): matched gradient steps across methods, wall-time reported for
     every method (default in [PROJECT_PLAN §8](../PROJECT_PLAN.md)): `[[pre-register before run]]`.
  10. **Differentiation** from JEPA-TTT and AdaJEPA (from T009): we update only one 64-number row `e`
      of a multitask TD-MPC2 model, use reward and value losses in addition to latent consistency,
      trigger adaptation by detection (C3), and report T0 CPU cost.
      <!-- VERIFY citation: what JEPA-TTT (arXiv:2610.00722) and AdaJEPA adapt and which losses they use; taken from T009 summaries, not from memory -->
      Also relate B3 to the paper's few-shot finetuning, which initialises `e` from a semantically similar
      task (Hansen et al., 2024, App. E, Table 7).
  11. **G2 fallback** (only if G2 fails on Tue 2026-11-17): `e` + LayerNorm affine parameters (LayerNorm
      sits in upstream `NormedLinear`, `tdmpc2/common/layers.py`), run with `scripts/adapt.py --method e_ln`
      (already in the binding interface); this note fixes which LayerNorms are included.
- **Pre-registered thresholds** (copied by M1 into [PROJECT_PLAN §7.3](../PROJECT_PLAN.md)):

  | Hypothesis | Quantity | Value | Justification |
  |---|---|---|---|
  | H2 | Maximum transitions | `[[K_max]]` | `<from dev grid, results/P2_adapt/... dev runs>` |
  | H2 | Minimum gap recovery (%) | `[[X]]` | `<reason>` |
  | H2 | Maximum wall-time relative to B1 (%) | `[[Y]]` | `<reason; same tier and device for B1 and Ours-C2>` |
  | H2 | Budget-matching rule | `[[pre-register before run]]` | `<reason>` |
  | H3 | "Poorly corrected" bound for `obs_noise` and `action_delay` | `[[pre-register before run]]` | `<reason>` |

- **Exact commands** (dev grid; `<dev-level spec>` from the dev split of `configs/shifts.yaml`):

  ```powershell
  python scripts/adapt.py --ckpt checkpoints/mt30-5M.pt --task <study-task> --shift <dev-level spec> --method e_only --K <K> --grad-steps <N_grad> --lr <lr> --seeds 2000 2001 2002 --episodes 10 --out results/P2_adapt/ --resume
  ```

  Colab (primary checkpoint): the same with `--ckpt checkpoints/mt30-19M.pt --out /content/drive/MyDrive/DA-TDMPC2/results/P2_adapt/ --shard <i>/3 --tier T1 --device cuda`.
- **Done when:**
  - [ ] `docs/design/C2_embedding_adaptation.md` fixes decisions 1–11, each with a justification and, if tuned, a dev-run path.
  - [ ] `[[K_max]]`, `[[X]]`, `[[Y]]`, the budget-matching rule and the H3 bound are filled in the table above and in the design note, merged to `main` before the first T204 run, and copied into PROJECT_PLAN §7.3.
  - [ ] Every dev-tuning run used dev levels and seeds 2000–2099 only.
- **Faculty-report sentence:** "Completed T201: C2 design fixed and H2 pre-registered (K ≤ `<K_max>`, recovery ≥ `<X>`%, wall-time ≤ `<Y>`% of full finetuning) in `docs/design/C2_embedding_adaptation.md` (PR #`<n>`), before any held-out run."

<a id="t202"></a>

### T202

**`adapt/embedding.py` + test proving only `e` changes**

- **Goal:** implement the T201 design in `src/datdmpc/adapt/embedding.py` (`adapt_embedding(agent,
  transitions, task_idx, grad_steps, lr, **kwargs)`) and the `e_only` path of `scripts/adapt.py`, with a
  test that proves **only the 64-d embedding row of the adapted task changes** and every other parameter
  and buffer is bit-identical.
- **Depends on:** T201
- **Target date:** Sun 2026-11-08
- **Compute tier + budget:** T0. Tests use the tiny random model (seconds on CPU, also in CI). One dev
  run on the laptop: `K × s_plan + N_grad × s_grad(e_only) + N_ep × L × s_plan` seconds (mt30-5M).
- **Files to create/modify:** `src/datdmpc/adapt/embedding.py`, `src/datdmpc/adapt/__init__.py`,
  `scripts/adapt.py`, `tests/test_embedding.py`, this page.
- **Required behaviour of `scripts/adapt.py --method e_only`:** writes the results schema
  (`config.yaml`, `episodes.csv`, `summary.json`, `env.txt`, `git_sha.txt`) and `adapted_embedding.json`
  (task, task_idx, checkpoint, the 64 values, `‖e‖` before/after, K, grad steps, lr, seed);
  method-specific `summary.json` keys at least `n_params_updated`, `adapt_wall_time_s`, `K`,
  `grad_steps`, `lr`.
- **`tests/test_embedding.py` must contain:**
  1. Tiny multitask model with a 64-d embedding and at least 2 task rows:
     `_upstream.make_tiny_cfg(obs_dim, action_dim, tasks=(...), task_dim=64)` +
     `_upstream.build_world_model(cfg)`; synthetic transitions; fixed torch seed.
  2. Snapshot **after one forward pass** (so any `max_norm` renormalisation of the looked-up row has
     already happened): every tensor in `model.state_dict()`, plus every tensor of
     `model._detach_Qs_params` and `model._target_Qs_params` and every buffer, regardless of whether
     they appear in `state_dict()`.
  3. Run `adapt_embedding` for ≥ 1 gradient step on row `task_idx`.
  4. Assert: row `task_idx` of `_task_emb.weight` changed; every other row `torch.equal` to the
     snapshot; every other tensor `torch.equal` to the snapshot (bit-identical); no frozen parameter has a
     non-`None` `.grad`; `requires_grad` flags restored afterwards; adapted row norm ≤ 1 within a float
     tolerance fixed in the test (if T201 keeps the unit-ball constraint); `n_params_updated == 64`.
  5. A checkpoint test, skipped when `checkpoints/mt30-5M.pt` is absent (CI): after loading through the
     T006 harness, `_task_emb.weight.shape == (30, 64)` and the same "only one row changes" assertion.
- **Exact commands:**

  ```powershell
  pytest -q tests/test_embedding.py
  python scripts/smoke_test.py
  python scripts/adapt.py --ckpt checkpoints/mt30-5M.pt --task <study-task> --shift <dev-level spec> --method e_only --K <K> --grad-steps <N_grad> --lr <lr> --seed 2000 --episodes 1 --out outputs/debug/ --resume
  ```

- **Done when:**
  - [ ] `pytest -q tests/test_embedding.py` passes locally and in CI (check `tests`, both OS legs); the checkpoint test passes locally.
  - [ ] The debug run writes all five schema files and `adapted_embedding.json` with 64 values.
  - [ ] No file outside my owned paths is changed (`git diff --name-only origin/main...`).
- **Faculty-report sentence:** "Completed T202: `e`-only adaptation implemented; `tests/test_embedding.py` proves that only the 64 numbers of the adapted task's embedding change and all other parameters stay bit-identical (PR #`<n>`)."

<a id="t203"></a>

### T203

**Baselines B1/B2/B3**

- **Goal:** implement the baselines in `src/datdmpc/adapt/baselines.py` and the `full_ft`,
  `partial_ft`, `rand_e` paths of `scripts/adapt.py`, all using the T201 loss, the identical K
  transitions and the T201 budget-matching rule.
- **Depends on:** T202
- **Target date:** Wed 2026-11-11
- **Compute tier + budget:** tests on T0 (tiny model). Dev sanity runs: `Σ_method (K × s_plan +
  N_grad × s_grad(method) + N_ep × L × s_plan)` per (task, dev level, seed); B1 on mt30-19M runs on Colab
  (12 GB RAM, risk R9). `s_grad(full_ft)` and `s_grad(partial_ft)` come from T008 if measured there,
  else from `adapt_wall_time_s` of these runs. <!-- VERIFY: whether scripts/profile.py --what adapt (T008, M3) measures full_ft and partial_ft gradient steps or only e_only; ask M3 before T204 budgeting -->
- **Definitions:**
  - **B1 `full_ft` (full finetune):** every parameter in upstream's world-model optimizer
    (`tdmpc2/tdmpc2.py`: encoder with `enc_lr_scale: 0.3`, dynamics, reward, Q-ensemble, task embedding;
    termination absent because `episodic: false`). Policy prior (upstream updates it separately with
    `pi_optim`) and target-Q handling as fixed in T201.
  - **B2 `partial_ft` (partial finetune, reward + Q heads):** all parameters of `model._reward` and
    `model._Qs`; everything else frozen, including `e`. If T201 narrows "heads" to the final layers, the
    note says so.
  - **B3 `rand_e` (ablation):** row `task_idx` re-initialised randomly (default: upstream's embedding
    init, uniform in [-0.02, 0.02], `tdmpc2/common/init.py`; seeded by the adaptation seed), then exactly
    the Ours-C2 procedure. Tests whether the pretrained `e` matters as an initialisation.
  - Parameter counts are computed from the loaded model (`sum(p.numel())` over updated parameters) and
    written as `n_params_updated` in `summary.json`, never by hand.
- **Files to create/modify:** `src/datdmpc/adapt/baselines.py`, `scripts/adapt.py`,
  `tests/test_baselines.py`, `configs/experiments/M2_baselines.yaml`, this page.
- **`tests/test_baselines.py` must prove** (tiny model): B2 changes only `_reward`/`_Qs` tensors (all
  others bit-identical); B3 changes only row `task_idx` and starts from a re-initialised row; B1 changes
  the parameters listed above; all three consume the identical transition set (same object or hash).
- **Exact commands:**

  ```powershell
  pytest -q tests/test_embedding.py tests/test_baselines.py
  python scripts/smoke_test.py
  python scripts/adapt.py --ckpt checkpoints/mt30-5M.pt --task <study-task> --shift <dev-level spec> --method rand_e --K <K> --grad-steps <N_grad> --lr <lr> --seed 2000 --episodes 1 --out outputs/debug/ --resume
  python scripts/adapt.py --ckpt checkpoints/mt30-5M.pt --task <study-task> --shift <dev-level spec> --method partial_ft --K <K> --grad-steps <N_grad> --lr <lr> --seed 2000 --episodes 1 --out outputs/debug/ --resume
  ```

  Colab (B1): `!python scripts/adapt.py --ckpt checkpoints/mt30-19M.pt --task <study-task> --shift <dev-level spec> --method full_ft --K <K> --grad-steps <N_grad> --lr <lr> --seed 2000 --episodes 1 --out /content/drive/MyDrive/DA-TDMPC2/outputs/debug/ --resume --tier T1 --device cuda`
- **Done when:**
  - [ ] `pytest -q tests/test_embedding.py tests/test_baselines.py` passes locally and in CI.
  - [ ] Each method writes all five schema files with `n_params_updated` and `adapt_wall_time_s` in `summary.json`.
  - [ ] B1/B2/B3 definitions above match the design note.
- **Faculty-report sentence:** "Completed T203: baselines B1 (full finetune, `<n_params_updated>` parameters), B2 (reward + Q heads, `<n_params_updated>`) and B3 (random `e`, 64) implemented on identical transitions (PR #`<n>`)."

<a id="t204"></a>

### T204

**Main C2 sweep on held-out test levels → `results/P2_adapt/`**

- **Goal:** evaluate Ours-C2 (`e_only`), B1 (`full_ft`), B2 (`partial_ft`) and B3 (`rand_e`) on the
  **held-out test levels only** (test split of `configs/shifts.yaml`), with the frozen T201 settings, and
  test H2 (mass and friction decide G2) and H3 (obs_noise, action_delay). B0 floor and nominal ceiling come
  from `results/P1_degradation/` and `results/P0_nominal/`.
- **Depends on:** T203, T102
- **Target date:** Tue 2026-11-17 (G2)
- **Compute tier + budget:** T1, sharded.
  `adapt_hours = N_task × N_shift_test × 4 × N_seed × N_grad × s_grad(method) / 3600` (summed per method),
  `eval_hours = N_task × N_shift_test × 4 × N_seed × N_ep × L × s_plan / 3600`,
  `collect_hours = N_task × N_shift_test × N_seed × K × s_plan / 3600` (once per (task, level, seed),
  shared by all methods), `total = adapt + eval + collect`; `N_seed ≥ 3`, `N_ep ≥ 10`.
  Wall-time for H2's `[[Y]]` (Ours-C2 vs B1) is measured on the **same tier and device** (T0 CPU), never
  laptop against Colab.
- **Files to create/modify:** `notebooks/colab/M2_c2_main.ipynb`, `configs/experiments/M2_c2_main.yaml`
  (command list), `results/P2_adapt/<run_id>/…`, `report/sections/*_M2.tex` (results text from
  week 4), this page.
- **Exact commands.** `scripts/adapt.py` takes one `--shift` per call (no `--shifts-from`), so the
  launcher issues one call per (study task, **test** level, method), using the T201 values. Every account
  runs the same command list with its own `--shard <i>/3`:

  ```
  !python scripts/adapt.py --ckpt checkpoints/mt30-19M.pt --task <study-task> --shift <test-level spec> --method e_only --K <K> --grad-steps <N_grad> --lr <lr> --seeds 0 1 2 --episodes 10 --out /content/drive/MyDrive/DA-TDMPC2/results/P2_adapt/ --resume --shard <i>/3 --tier T1 --device cuda
  !python scripts/adapt.py --ckpt checkpoints/mt30-19M.pt --task <study-task> --shift <test-level spec> --method rand_e --K <K> --grad-steps <N_grad> --lr <lr> --seeds 0 1 2 --episodes 10 --out /content/drive/MyDrive/DA-TDMPC2/results/P2_adapt/ --resume --shard <i>/3 --tier T1 --device cuda
  !python scripts/adapt.py --ckpt checkpoints/mt30-19M.pt --task <study-task> --shift <test-level spec> --method partial_ft --K <K> --grad-steps <N_grad> --lr <lr> --seeds 0 1 2 --episodes 10 --out /content/drive/MyDrive/DA-TDMPC2/results/P2_adapt/ --resume --shard <i>/3 --tier T1 --device cuda
  !python scripts/adapt.py --ckpt checkpoints/mt30-19M.pt --task <study-task> --shift <test-level spec> --method full_ft --K <K> --grad-steps <N_grad> --lr <lr> --seeds 0 1 2 --episodes 10 --out /content/drive/MyDrive/DA-TDMPC2/results/P2_adapt/ --resume --shard <i>/3 --tier T1 --device cuda
  ```

  T0 wall-time measurement for H2 (laptop, CPU; returns from these runs are debugging-only, the
  `adapt_wall_time_s` values are the reported C2 cost). `<s_T0>` is an evaluation seed (0–99) not used by
  any T1 run, because `run_id` does not contain the tier and a shared seed would put laptop and Colab
  episodes into the same run folder:

  ```powershell
  python scripts/adapt.py --ckpt checkpoints/mt30-19M.pt --task <study-task> --shift <test-level spec> --method e_only --K <K> --grad-steps <N_grad> --lr <lr> --seed <s_T0> --episodes 1 --out results/P2_adapt/ --resume --tier T0 --device cpu
  python scripts/adapt.py --ckpt checkpoints/mt30-19M.pt --task <study-task> --shift <test-level spec> --method full_ft --K <K> --grad-steps <N_grad> --lr <lr> --seed <s_T0> --episodes 1 --out results/P2_adapt/ --resume --tier T0 --device cpu
  ```

- **Done when:**
  - [ ] Every run used a test-split level and evaluation seeds 0–99; no setting differs from the T201 note on `main`.
  - [ ] `results/P2_adapt/` has a complete run folder for every (study task, test level, method, seed), each with the five schema files and `adapted_embedding.json` for `e_only`/`rand_e`.
  - [ ] Gap recovery `(R_adapt − R_shift) / (R_nominal − R_shift)` per (task, level, method) is computable from the committed `summary.json` files together with `results/P1_degradation/` and `results/P0_nominal/` (T501 computes it; nothing typed by hand).
  - [ ] The G2 verdict (H2 thresholds on mass and friction, held-out levels) and the H3 outcome are in the handoff entry with `summary.json` paths, for the gate meeting on Tue 2026-11-17; if G2 fails, the fallback is started as decided at the gate.
  - [ ] Each shard is in the [Compute log](#compute-log).
- **Faculty-report sentence:** "Completed T204: on held-out `<shift spec>` levels, `e`-only adaptation of 64 parameters recovers `<gap recovery>` of the nominal–shifted gap on `<task>` vs `<gap recovery>` for full finetuning, at `<adapt_wall_time_s>` s vs `<adapt_wall_time_s>` s on T0 CPU (`results/P2_adapt/<run_id>/summary.json`)."

<a id="t503"></a>

### T503

**(shared, all) Clean-clone reproducibility check of one result per contribution**

- **Goal:** my share of the clean-clone check: reproduce the result assigned to me at G3 (proposed
  split: each member reproduces a result produced by someone else; M1 coordinates), following the
  procedure and acceptance criterion in [RUNS](../RUNS.md) Step 5 and M1's T503 card.
- **Depends on:** T204, T303
- **Target date:** Sun 2026-12-06
- **Compute tier + budget:** the tier of the original run (its `env.txt`); hours = sum of `wall_time_s`
  in the original `episodes.csv` (plus adaptation time for `results/P2_adapt/` runs).
- **Files to create/modify:** this page (handoff entry with the comparison). Reproduced output goes to the
  gitignored `outputs/repro/`; nothing in `results/` is overwritten.
- **Exact commands:** follow [RUNS Step 5.2](../RUNS.md) exactly (fresh clone into
  `C:\code\tdmpc2-repro` from `https://github.com/Shahrcasm/tdmpc2-shift-adaptation.git`, check out the SHA
  from the original run's `git_sha.txt`, separate env `datdmpc-repro`, full install,
  `python scripts/get_checkpoints.py --models mt30-5M mt30-19M`), then re-run the command recorded in the
  original `config.yaml` with `--out outputs/repro/<phase>/`.
- **Done when:**
  - [ ] The assigned result is reproduced within the pre-registered criterion, or the mismatch is explained in the handoff entry and reported honestly.
  - [ ] Original and reproduced `summary.json` paths are both listed in the handoff entry.
- **Faculty-report sentence:** "Completed T503 (M2 share): `<result>` reproduced from a clean clone at `<tag>` within the pre-registered criterion (`<original summary.json>` vs `<reproduced summary.json>`)."

<a id="t504"></a>

### T504

**(shared, all) Full draft → faculty feedback → final submission**

- **Goal:** my report sections, written from week 4 (Nov 11+) in `report/sections/<section>_M2.tex`
  (file names follow M1's T502 skeleton): related work (from T009), C2 method (from T201), degradation
  results (T103) and C2 results (T204). Milestones: full draft Tue 2026-12-08 → faculty feedback → final
  Sun 2026-12-13 → submission Mon 2026-12-14. Report template:
  `[[report template: IEEE conference unless the course specifies otherwise]]`.
- **Depends on:** T503
- **Target date:** Mon 2026-12-14
- **Compute tier + budget:** none (no new experiments after the freeze, Wed 2026-12-02).
- **Files to create/modify:** `report/sections/*_M2.tex`, this page.
- **Exact commands:**

  ```powershell
  Select-String -Path report\sections\*_M2.tex -Pattern "VERIFY", "\[\["
  git add report/sections docs/team/M2_Ishtiak.md
  git commit -m "T504: update M2 report sections"
  git push origin dev_ishtiak
  ```

- **Done when:**
  - [ ] My sections are in the full draft by Tue 2026-12-08 and revised after faculty feedback by Sun 2026-12-13.
  - [ ] The marker search prints nothing for my sections.
  - [ ] Every number in my sections is traceable to `results/REGISTRY.csv` or a cited `results/` path; every cited paper was read (T009).
- **Faculty-report sentence:** "Completed T504 (M2 share): related-work, C2 method and C2 results sections final in `report/sections/` (PR #`<n>`); all numbers from `results/REGISTRY.csv`."
