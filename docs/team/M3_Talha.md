# M3 — Md. Abdullah Talha

> Only M3 edits this page. Statuses, handoff entries and compute use recorded here are copied into
> [STATUS](../STATUS.md) by M1 at merge time (`T000: sync status`). Rules: [AGENTS.md](../../AGENTS.md).
> Science, hypotheses and metrics: [PROJECT_PLAN](../PROJECT_PLAN.md). Commands and environment:
> [RUNS](../RUNS.md).

| Field | Value |
|---|---|
| Name | Md. Abdullah Talha |
| Slot · Student ID | M3 · 2222614642 |
| Branch | `dev_talha` |
| Role | Profiling · C3 shift detection |
| Components | Compute profiling that sets every budget (T008); C3 detection signals, calibrated EWMA/CUSUM detector, C3 design note with the pre-registered H4 thresholds, and mid-episode injection evaluation (T301–T303) |
| Laptop | Native Windows (edition/version/build recorded in [Record: my laptop](#record-my-laptop), T004); Miniconda env `datdmpc`; PowerShell 5.1; repo at `C:\code\tdmpc2-shift-adaptation` |
| Colab account | M3 (one of the three parallel accounts) |
| Reviewer of my PRs | M1 (integrator, the only member who merges), checklist in [AGENTS.md §7](../../AGENTS.md); I never click Merge |

**Strictly owned files** (binding table: [AGENTS.md §2](../../AGENTS.md)); I edit nothing else:

- `src/datdmpc/detect/**` (`signals.py`, `detector.py`)
- `scripts/profile.py`, `scripts/detect.py`
- `configs/experiments/M3_*.yaml` (e.g. `configs/experiments/M3_detector.yaml`)
- `notebooks/colab/M3_*.ipynb` (launchers only; logic lives in `src/`)
- `tests/test_signals.py`, `tests/test_detector.py`
- `results/P0_profile/**`, `results/P3_detect/**` (T301 raw dumps go to the gitignored `outputs/signals/`)
- `docs/design/C3_detection.md` (T302)
- `report/sections/*_M3.tex` (from week 4)
- `docs/team/M3_Talha.md` (this page)

The T001 stubs of the files above (docstring + `NotImplementedError` / exit code 3) were created by M1 and
belong to me from the moment `dev_talha` exists. Everything else — in particular
`third_party/tdmpc2/**` (read-only for everyone), the harness, wrappers and ranking-fidelity diagnostic (`src/datdmpc/eval/**`,
`src/datdmpc/envs/**`, `src/datdmpc/diagnostics/**`, M1), the adaptation code (`src/datdmpc/adapt/**`, M2), `docs/PROJECT_PLAN.md` and
`docs/STATUS.md` (M1) — is changed only by its owner; I ask through a GitHub issue (task template) or a
request line in my [Handoff Log](#handoff-log). A new file at a path not listed in the ownership table
(e.g. a `tests/test_profile.py` or a pilot results folder) needs an M1 update of [AGENTS.md §2](../../AGENTS.md)
first.

---

## My Tasks

Status values: To Do / In Progress / Done / Blocked. "Depends on" tasks must be Done in
[STATUS](../STATUS.md) before I start the task itself; the [while-waiting block](#while-waiting-for-t006-from-fri-2026-10-23)
lists the work I do before T006 lands.

| ID | Task | Depends on | Target date | Status |
|---|---|---|---|---|
| [T004](#t004) | Windows env setup (Miniconda) + smoke test on own laptop; record Windows version (`winver`) | T001 | Fri 2026-10-23 | To Do |
| [T008](#t008) | Profiling: planning sec/decision + adaptation sec/grad-step on T0 laptop CPU, Colab CPU, Colab GPU → `results/P0_profile/` | T006, T004 | Tue 2026-10-27 | To Do |
| [T301](#t301) | Detection signal extraction | T006 | Sun 2026-11-08 | To Do |
| [T302](#t302) | Detector + calibration on nominal seeds; pre-registered H4 thresholds | T301 | Fri 2026-11-13 | To Do |
| [T303](#t303) | Detection evaluation with mid-episode shift injection → `results/P3_detect/` | T302, T102 | Tue 2026-11-24 | To Do |
| [T503](#t503) | (shared, all) Clean-clone reproducibility check of one result per contribution | T204, T303 | Sun 2026-12-06 | To Do |
| [T504](#t504) | (shared, all) Full draft → faculty feedback → final submission | T503 | Mon 2026-12-14 | To Do |

Gates that depend on my work: **G0** (Tue 2026-10-27: sec/step known on laptop + Colab — T008) and **G3**
(Tue 2026-11-24: pre-registered H4 targets on ≥2 shift types — T303).

---

## Record: my laptop

Filled in during [T004](#t004). Values are copied from the commands shown, not typed from memory.

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
| Recorded on | `<date>` | — |

The sec/step printed by the smoke test is a debugging figure and is not recorded here; budgets use T008
(`results/P0_profile/`). Because T008 measures the **T0 laptop CPU** on this machine, the CPU row above is
also copied into `env.txt` of every `results/P0_profile/` run produced here.

---

## Weekly Faculty Update

For Dr. Mohammad Ashrafuzzaman Khan, due every **`[[weekday]]`** (open item in
[STATUS §3](../STATUS.md), "Decisions pending with faculty").

Rules: 3–5 bullets, **each quoting a hard number copied from a file under `results/` and cited by its
path**, plus exactly one "blocker / help needed" bullet. A week without results reports completed tasks
with their evidence (PR number, file path) and no numbers. Laptop numbers are never quoted, except T0
CPU wall-time measurements from T008, labelled "T0 laptop CPU".

Format example (placeholders only, never replaced by invented values):

> **Week `<n>` (`<date>`) — M3, Md. Abdullah Talha**
> - Completed T008: MPPI planning costs `<sec_per_decision_mean from results/P0_profile/<run_id>/summary.json>` s per decision on the T0 laptop CPU vs `<sec_per_decision_mean from results/P0_profile/<run_id>/summary.json>` s on a Colab GPU runtime (mt30-19M, `<task>`); one `e`-only gradient step costs `<sec_per_grad_step_e_only from the same T0 file>` s on the T0 laptop CPU.
> - T303: the detector reaches AUROC `<auroc from results/P3_detect/<run_id>/summary.json>` on `<shift spec>` with `<false_alarms_per_1000 from the same file>` false alarms per 1,000 nominal steps and mean delay `<detection_delay_mean from the same file>` agent steps.
> - T302: calibrated on nominal seeds 1000–1099, the detector's threshold is `<threshold from results/P3_detect/<run_id calibration>/summary.json>` for `<signal>`.
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
· blockers · next. Requests to other members (file owner by slot) are also written here.

| Date | Task | What was done | Files changed | Result path | Blockers | Next |
|---|---|---|---|---|---|---|
| `<YYYY-MM-DD>` | `<T0xx>` | `<what was done>` | `<paths>` | `<results/... or —>` | `<blockers or none>` | `<next task>` |

---

## Task cards

Budget symbols used below: `N_task` study tasks (chosen by M2's T007 rule), `N_shift` shift levels,
`N_seed` seeds, `N_ep` episodes per (task, shift, seed), `L = 500` agent decisions per DMControl episode
(action repeat 2 and a 500-step `Timeout` in `third_party/tdmpc2/tdmpc2/envs/dmcontrol.py`), `s_plan` =
planning sec/decision and `s_grad` = adaptation sec/gradient-step, both from T008
(`results/P0_profile/<run_id>/summary.json`) for the tier and device in question, `s_sig` = per-decision
signal-extraction overhead (T301). Rule:
more than 3 laptop-hours → Colab (T1), split across the three accounts and logged in the
[Compute log](#compute-log). MPPI settings are never changed.

All PowerShell blocks assume:

```powershell
cd C:\code\tdmpc2-shift-adaptation
conda activate datdmpc
```

All Colab cells assume the template of [RUNS Step 3b](../RUNS.md) (Drive mounted, repo cloned at the
commit under test into `/content/tdmpc2-shift-adaptation`, `environment/requirements-colab.txt`
installed, checkpoints copied from `/content/drive/MyDrive/DA-TDMPC2/checkpoints/`). After a Colab run,
the finished run folders are copied from `/content/drive/MyDrive/DA-TDMPC2/results/...` into the same
`results/...` path of the laptop clone and committed.

### T004

**Windows env setup (Miniconda) + smoke test on own laptop; record Windows version (`winver`)**

- **Goal:** a working `datdmpc` environment on my Windows laptop, installed exactly as
  [RUNS Step 1](../RUNS.md) says; tiny smoke test passing; laptop facts recorded in
  [Record: my laptop](#record-my-laptop). This laptop is the **T0 tier** that T008 measures.
- **Depends on:** T001
- **Target date:** Fri 2026-10-23
- **Compute tier + budget:** T0. Installation plus one tiny smoke test (target under 2 minutes on a
  laptop CPU); no planning runs.
- **Files to create/modify:** `docs/team/M3_Talha.md` (this page). Install problems that RUNS does not
  cover are reported to M1 (owner of `docs/RUNS.md` and `environment/*`) by issue, with the fix that
  worked.
- **Exact commands** (after installing Git for Windows and Miniconda per [RUNS Step 1](../RUNS.md) and
  accepting the collaborator invitation; open a new PowerShell window afterwards):

  ```powershell
  git config --global core.longpaths true
  git clone https://github.com/Shahrcasm/tdmpc2-shift-adaptation.git C:\code\tdmpc2-shift-adaptation
  cd C:\code\tdmpc2-shift-adaptation
  git fetch origin
  git checkout dev_talha
  conda create -n datdmpc python=3.11 -y
  conda activate datdmpc
  pip install torch==2.7.1 --index-url https://download.pytorch.org/whl/cpu
  pip install -r environment/requirements-cpu.txt
  pip install -e . --no-deps
  python scripts/smoke_test.py --mode tiny
  pytest -q tests/test_upstream_bridge.py tests/test_smoke.py
  python scripts/profile.py --help
  python scripts/detect.py --help
  python -m datdmpc.diagnostics.ranking_fidelity --help
  winver
  Get-ComputerInfo -Property OsName, OsVersion, OsBuildNumber, CsModel, CsTotalPhysicalMemory
  (Get-CimInstance Win32_Processor).Name
  conda --version
  python --version
  pip show torch numpy mujoco dm-control
  ```

- **Done when:**
  - [ ] `python --version` in `datdmpc` reports 3.11, and `pip show` versions match `environment/requirements-cpu.txt`.
  - [ ] `python scripts/smoke_test.py --mode tiny` exits 0 and prints `[smoke] OK`.
  - [ ] `pytest -q tests/test_upstream_bridge.py tests/test_smoke.py` passes on the laptop.
  - [ ] `--help` of `scripts/profile.py`, `scripts/detect.py` and `python -m datdmpc.diagnostics.ranking_fidelity` exits 0 on Windows (`profile.py` shares its name with a standard-library module; importing `datdmpc` first makes `src/datdmpc/__init__.py` remove `scripts/` from `sys.path`, which avoids the clash — this confirms it works here).
  - [ ] [Record: my laptop](#record-my-laptop) is filled in, including the `winver` edition, version and OS build.
  - [ ] Handoff entry written; PR `T004: record M3 laptop and environment` opened from `dev_talha`.
- **Faculty-report sentence:** "Completed T004: CPU-only environment installed on my Windows laptop (`<edition and OS build from winver>`) following `docs/RUNS.md`; tiny smoke test and bridge tests pass (PR #`<n>`)."

#### While waiting for T006 (from Fri 2026-10-23)

T008 and T301 both depend on M1's harness T006 (target Mon 2026-10-26). So that I am not idle
between T004 and T006 (risk noted in [STATUS §2](../STATUS.md)), I build everything that does **not**
need a checkpoint against the random tiny model of `scripts/smoke_test.py --mode tiny`
(`datdmpc._upstream.make_tiny_cfg` + `build_world_model`, real DMControl env, no checkpoint), committing
on `dev_talha` as `T008: wip – …` / `T301: wip – …`:

1. **Read upstream** `third_party/tdmpc2/tdmpc2/tdmpc2.py` (`act`, `_plan`, `_estimate_value`,
   `_get_discount`, `_update`) and `third_party/tdmpc2/tdmpc2/common/world_model.py` (`encode`, `next`,
   `reward`, `pi`, `Q`), plus `common/math.py` (`two_hot_inv`) and `envs/dmcontrol.py`,
   `envs/wrappers/timeout.py`. Note findings in the handoff log.
2. **`scripts/profile.py` skeleton (T008):** timing loop with warm-up blocks excluded, `time.perf_counter`,
   `torch.set_num_threads(4)` on T0, `torch.cuda.synchronize()` around timed blocks on `--device cuda`,
   result writing in the binding schema; exercised on the tiny model with output to `outputs/debug/`.
3. **Signals (T301)** in `src/datdmpc/detect/signals.py` against the tiny model (shape and finiteness
   tests in `tests/test_signals.py`). The tiny model has its own `num_q` and `task_dim`, so tests never
   hard-code checkpoint sizes.
4. **EWMA/CUSUM statistics (T302)** in `src/datdmpc/detect/detector.py` on synthetic sequences
   (`tests/test_detector.py`).

```powershell
python scripts/smoke_test.py --mode tiny
pytest -q tests/test_signals.py tests/test_detector.py
```

### T008

**Profiling: planning sec/decision + adaptation sec/grad-step on T0 laptop CPU, Colab CPU, Colab GPU → `results/P0_profile/`**

- **Goal:** measure the two unit costs that every budget in the project uses
  ([PROJECT_PLAN §11.2](../PROJECT_PLAN.md)): `s_plan` = wall-clock seconds per agent decision (one
  `act` call including MPPI, unchanged settings) and `s_grad` = seconds per adaptation gradient step,
  for `mt30-5M` and `mt30-19M`, on three tiers: **T0 laptop CPU**, **Colab CPU runtime**, **Colab GPU
  runtime**. G0 (Tue 2026-10-27) requires these numbers; no budget anywhere may assume a sec/step.
- **Depends on:** T006, T004
- **Target date:** Tue 2026-10-27
- **Compute tier + budget:** T0 and T1. Per (checkpoint, tier, device):
  `(n_warmup + n_steps) × (s_plan + s_grad,e_only + s_grad,full) / 3600` hours with `--what all`. The
  unit costs are unknown before this task, so the first T0 call uses a small `--steps` with output to
  `outputs/debug/`, and `n_steps` for the recorded runs is chosen from it (debug figure, not a result).
- **Files to create/modify:** `scripts/profile.py`, `configs/experiments/M3_profile.yaml` (if a config
  is needed), `notebooks/colab/M3_profile.ipynb`, `results/P0_profile/**`.
- **Interface (binding):** `python scripts/profile.py --ckpt --task --what {plan,adapt,all} --steps N
  --device --tier --out results/P0_profile/`.
- **Implementation constraints:**
  - Keep the `try: import datdmpc` block as the first import of `scripts/profile.py`, above every
    torch/tensordict/numpy import. Importing `datdmpc` removes `scripts/` from `sys.path`
    (`src/datdmpc/__init__.py`); otherwise this file shadows the standard-library `profile` module that
    `cProfile` imports (tensordict → `torch._dynamo` → `cProfile`). `tests/test_smoke.py` guards this with a
    subprocess run; keep it green.
  - Load the agent only through M1's harness (`datdmpc.eval.harness.load_agent`, T006), which
    subclasses upstream `TDMPC2` for CPU (upstream hard-codes `cuda:0` in `tdmpc2.py`). `compile=False`;
    MPPI settings exactly as in `third_party/tdmpc2/tdmpc2/config.yaml`.
  - `--what plan`: time `act(obs, t0, eval_mode=True, task)` on real observations of the task's
    DMControl env; record the resolved planning iterations (`tdmpc2.py` adds 2 iterations when
    `action_dim >= 20`).
  - `--what adapt`: M2's `adapt/embedding.py` does not exist until T202 (Sun 2026-11-08), so T008 times
    a **proxy**: one Adam step on the world model's own loss (consistency + reward + value terms, the
    structure of `TDMPC2._update`) over a batch of K collected transitions, (a) with gradients only on
    the task's embedding row (`e_only`, 64 numbers for mt30-5M/19M per `common/parser.py`) and (b) on
    all parameters (`full`). `K` is recorded in `config.yaml`. Sub-task: after T202 is merged, re-run
    `--what adapt` on T0 with M2's implementation and record both in the handoff log; T204 budgets use
    the re-run.
  - Run folder: the five schema files. `run_id` uses the method field to keep tiers apart (the binding
    `run_id` has no tier field): `<ckpt-stem>__<task>__none__profile-<what>-<tier>-<device>__seed0`.
    `episodes.csv` keeps the binding columns with one row per timed block (`episode` = block index,
    `length` = decisions or gradient steps in the block, `wall_time_s` = block time). `summary.json` adds
    `sec_per_decision_mean`, `sec_per_decision_ci95_low`, `sec_per_decision_ci95_high`,
    `sec_per_grad_step_e_only`, `sec_per_grad_step_full`, `n_warmup`, `n_timed`, `torch_threads`,
    `planning_iterations`.
- **Exact commands** (T0; close the browser and other heavy programs first, one process at a time):

  ```powershell
  python scripts/profile.py --ckpt checkpoints/mt30-5M.pt --task walker-walk --what all --steps <small n for the first look> --device cpu --tier T0 --out outputs/debug/
  python scripts/profile.py --ckpt checkpoints/mt30-5M.pt --task walker-walk --what all --steps <n_steps> --device cpu --tier T0 --out results/P0_profile/
  python scripts/profile.py --ckpt checkpoints/mt30-19M.pt --task walker-walk --what all --steps <n_steps> --device cpu --tier T0 --out results/P0_profile/
  ```

  Colab, from `notebooks/colab/M3_profile.ipynb` — once on a **CPU runtime** (`--device cpu`), once on a
  **GPU runtime** (`--device cuda`), for each checkpoint:

  ```python
  !python scripts/profile.py --ckpt /content/drive/MyDrive/DA-TDMPC2/checkpoints/mt30-19M.pt --task walker-walk --what all --steps <n_steps> --device cpu --tier T1 --out /content/drive/MyDrive/DA-TDMPC2/results/P0_profile/
  !python scripts/profile.py --ckpt /content/drive/MyDrive/DA-TDMPC2/checkpoints/mt30-19M.pt --task walker-walk --what all --steps <n_steps> --device cuda --tier T1 --out /content/drive/MyDrive/DA-TDMPC2/results/P0_profile/
  ```

  `walker-walk` is used because the study tasks are only fixed by T007 (Fri 2026-10-30); if the
  per-task simulator cost turns out to matter for a budget, `--what plan` is repeated per study task.
- **Done when:**
  - [ ] `results/P0_profile/` holds one complete run folder (five files) per (checkpoint ∈ {mt30-5M, mt30-19M}) × (T0 CPU, T1 CPU, T1 GPU) — six folders — each `env.txt` naming tier, device, CPU/GPU model and library versions.
  - [ ] Each `summary.json` has `sec_per_decision_mean` with its CI and both `sec_per_grad_step_*` keys; warm-up blocks are excluded and counted in `n_warmup`.
  - [ ] `config.yaml` of every run shows MPPI settings equal to upstream `config.yaml` and `compile: false`.
  - [ ] GPU timings were taken with `torch.cuda.synchronize()` around each timed block (code review).
  - [ ] The `--what adapt` proxy is labelled as such in `summary.json` (`adapt_impl: proxy`), and the re-run after T202 is listed as an open sub-task in the handoff log.
  - [ ] Handoff entry lists the `results/P0_profile/<run_id>/summary.json` paths that M1 and M2 use for budgets.
- **Faculty-report sentence:** "Completed T008: planning costs `<sec_per_decision_mean>` s per decision on the T0 laptop CPU and `<sec_per_decision_mean>` s on a Colab GPU runtime for mt30-19M (`results/P0_profile/<run_id>/summary.json`); these unit costs set all compute budgets."

### T301

**Detection signal extraction**

- **Goal:** per agent step of an episode run by the frozen B0 planner, compute the three C3 signals from
  the model's own predictions (no extra environment interaction), and dump them for T302/T303:
  1. **Latent consistency error** `‖d(z_t, a_t, e) − h(s_{t+1}, e)‖²` = `model.next(model.encode(obs_t,
     task), a_t, task)` vs `model.encode(obs_{t+1}, task)`; reported as MSE (squared ℓ2 distance divided
     by the latent dimension), matching the `F.mse_loss` convention of `TDMPC2._update` and the metric
     definition in [PROJECT_PLAN §9](../PROJECT_PLAN.md).
  2. **Reward prediction error** `two_hot_inv(model.reward(z_t, a_t, task), cfg) − r_t`, with `r_t` the
     reward returned by the env wrapper for that agent step (sum of the two simulator-step rewards,
     `envs/dmcontrol.py`).
     <!-- VERIFY: that the mt30 reward head was trained on per-agent-step rewards summed over the action repeat (check tdmpc2/trainer/offline_trainer.py and common/buffer.py; the offline datasets themselves are not downloaded). Resolved by T301: on nominal episodes the reward error must be centred near zero. -->
  3. **Q-ensemble disagreement:** `model.Q(z_t, a_t, task, return_type='all')` returns the logits of
     every ensemble member (`num_q: 5` in `config.yaml`, unchanged for sizes 5/19); convert each member
     with upstream `common.math.two_hot_inv` and take the standard deviation across members. (Note:
     `return_type='avg'` would average two randomly chosen heads; `'all'` is required here.) This is the
     same kind of signal as the test-time regulariser in the TD-MPC2 paper (Hansen et al., 2024, App. J,
     Eq. 9), which builds on Feng et al. (2023) <!-- VERIFY citation -->.
- **Depends on:** T006
- **Target date:** Sun 2026-11-08
- **Compute tier + budget:** `N_task × N_shift × N_seed × N_ep × L × (s_plan + s_sig) / 3600` hours.
  Development runs on T0 with 1 episode; signal dumps for detector design on dev levels and dev seeds
  2000–2099 (T1 if > 3 laptop-hours).
- **Files to create/modify:** `src/datdmpc/detect/signals.py`, `scripts/detect.py` (`signals`
  subcommand), `tests/test_signals.py`, `notebooks/colab/M3_detect.ipynb`. Raw dumps go to the gitignored
  `outputs/signals/` (one CSV per run: `run_id, task, shift_type, shift_level, seed, episode, step,
  consistency_mse, reward_err, q_std, shift_active`). The harness is used only through its public
  functions (`load_agent`, `make_task_env`, `evaluate`); if a per-step callback is needed, I request it
  from M1 by issue.
- **Interface (binding):** `python scripts/detect.py signals --ckpt --task --shift --episodes --seed
  --out outputs/signals/` (plus `--tier`, `--device`).
- **Exact commands:**

  ```powershell
  pytest -q tests/test_signals.py
  python scripts/detect.py signals --ckpt checkpoints/mt30-5M.pt --task walker-walk --shift none --episodes 1 --seed 2000 --out outputs/signals/ --tier T0 --device cpu
  python scripts/detect.py signals --ckpt checkpoints/mt30-5M.pt --task walker-walk --shift <dev level spec from configs/shifts.yaml> --episodes 1 --seed 2000 --out outputs/signals/ --tier T0 --device cpu
  ```

- **Done when:**
  - [ ] Test (tiny model): each signal has shape (1,) per step, is finite, and the Q-std uses all `cfg.num_q` members (checked against a manual per-member `two_hot_inv`).
  - [ ] Test: the consistency error is zero when `obs_{t+1}` is replaced by an observation whose encoding equals `d(z_t, a_t, e)` (constructed case), and positive otherwise.
  - [ ] Test: signal extraction does not change the actions chosen by the planner (same seed → same actions with and without extraction).
  - [ ] One nominal and one shifted dump on `mt30-5M` exist in `outputs/signals/` and their run IDs are in the handoff log (not committed).
  - [ ] `s_sig` (extra seconds per decision for the three signals) is recorded in the handoff log for the T302/T303/T304 budgets.
- **Faculty-report sentence:** "Completed T301: three shift-detection signals (latent consistency error, reward prediction error, Q-ensemble disagreement) are extracted online from the frozen model at each agent step (`src/datdmpc/detect/signals.py`, PR #`<n>`)."

### T302

**Detector + calibration on nominal seeds; pre-registered H4 thresholds**

- **Goal:** an online detector that turns the per-step signals into an alarm: per-signal standardisation
  with statistics from **nominal** episodes, smoothing by EWMA and/or a one-sided CUSUM, and an alarm
  threshold set on nominal data only. Write `docs/design/C3_detection.md` and pre-register the H4
  thresholds `[[A]]` (minimum AUROC), `[[F]]` (maximum false alarms per 1,000 nominal steps) and `[[D]]`
  (maximum detection delay in agent steps).
- **Depends on:** T301
- **Target date:** Fri 2026-11-13
- **Compute tier + budget:** calibration: `N_task × n_cal × N_ep × L × (s_plan + s_sig) / 3600` hours,
  with `n_cal` calibration seeds drawn **only from 1000–1099**; detector-hyperparameter tuning (EWMA
  weight, CUSUM drift, which signals are combined, window for AUROC): dev levels and dev seeds
  2000–2099, same formula. > 3 laptop-hours → T1.
- **Data separation (binding):** calibration seeds 1000–1099 (nominal only) fit the standardisation
  statistics and the alarm threshold; dev levels + dev seeds 2000–2099 tune hyperparameters; held-out
  test levels and test seeds 0–99 are **never** touched before T303 ([PROJECT_PLAN §8](../PROJECT_PLAN.md)).
- **Files to create/modify:** `src/datdmpc/detect/detector.py`, `scripts/detect.py` (`calibrate`
  subcommand), `configs/experiments/M3_detector.yaml` (signals used, smoothing parameters, threshold,
  path of the calibration run), `tests/test_detector.py`, `docs/design/C3_detection.md`,
  `notebooks/colab/M3_detect.ipynb`, `results/P3_detect/**` (calibration run).
- **Design note content (`docs/design/C3_detection.md`):** signals and why (CSE 465 framing: novelty
  detection calibrated on nominal data only, ROC analysis); standardisation; EWMA/CUSUM definitions;
  threshold rule (e.g. a nominal-quantile rule set from calibration seeds); AUROC window definition;
  injection step choice for T303; how an alarm triggers C2 in T304 (interface agreed with M1/M2);
  differentiation from Q-ensemble use in the TD-MPC2 paper (App. J) and related work from
  [RELATED_WORK](../RELATED_WORK.md) (T009); proposed values and justification for `[[A]]`, `[[F]]`,
  `[[D]]`.
- **Pre-registration procedure** ([PROJECT_PLAN §7.3](../PROJECT_PLAN.md)): I write the proposed
  `[[A]]`, `[[F]]`, `[[D]]` in `docs/design/C3_detection.md` and open the PR; M1 copies them into the
  PROJECT_PLAN pre-registration table (commit on `dev_shahriar`, merged by M1).
  **No T303 run starts before they are in docs/PROJECT_PLAN.md on `main`.**
- **Interface (binding):** `python scripts/detect.py calibrate --ckpt --task --seeds ... --episodes --out
  results/P3_detect/` (plus `--tier`, `--device`).
- **Exact commands:**

  ```powershell
  pytest -q tests/test_detector.py tests/test_signals.py
  python scripts/detect.py calibrate --ckpt checkpoints/mt30-5M.pt --task walker-walk --seeds 1000 1001 --episodes 1 --out outputs/debug/ --tier T0 --device cpu
  python scripts/detect.py evaluate --ckpt checkpoints/mt30-5M.pt --task walker-walk --shift <dev level spec from configs/shifts.yaml> --inject-at <STEP> --detector-config configs/experiments/M3_detector.yaml --seeds 2000 --out outputs/debug/ --tier T0 --device cpu
  ```

  Colab (reported calibration, one cell per study task):

  ```python
  !python scripts/detect.py calibrate --ckpt /content/drive/MyDrive/DA-TDMPC2/checkpoints/mt30-19M.pt --task <study task> --seeds <space-separated calibration seeds within 1000–1099> --episodes <N_ep> --out /content/drive/MyDrive/DA-TDMPC2/results/P3_detect/ --tier T1 --device cuda
  ```

- **Done when:**
  - [ ] Test: EWMA and CUSUM statistics match hand-computed values on a synthetic sequence; the CUSUM resets after an alarm as specified in the design note.
  - [ ] Test: on a synthetic stationary sequence the false-alarm rate is close to the target set by the threshold rule; on a sequence with a mean step the alarm fires after the step.
  - [ ] Test: `calibrate` rejects any seed outside 1000–1099 and any shift other than `none`.
  - [ ] Calibration run folders exist in `results/P3_detect/` for each study task (mt30-19M), with the seeds used listed in `config.yaml`.
  - [ ] `configs/experiments/M3_detector.yaml` is committed and points to the calibration runs.
  - [ ] `docs/design/C3_detection.md` is merged, and `[[A]]`, `[[F]]`, `[[D]]` appear with values in the [PROJECT_PLAN](../PROJECT_PLAN.md) pre-registration table **before** the first T303 run.
- **Faculty-report sentence:** "Completed T302: detector calibrated on nominal seeds only (`results/P3_detect/<run_id>/`); H4 targets pre-registered in `docs/PROJECT_PLAN.md` (commit `<sha>`) before any detection evaluation."

### T303

**Detection evaluation with mid-episode shift injection → `results/P3_detect/`**

- **Goal:** evaluate the frozen detector on held-out test levels with the shift injected **mid-episode**
  at a fixed agent step (`--inject-at`, set in the design note), and on nominal episodes (`--shift none`)
  for false alarms; report AUROC, detection delay (with missed detections counted separately) and false
  alarms per 1,000 nominal steps, exactly as defined in [PROJECT_PLAN §9](../PROJECT_PLAN.md). G3 (Tue
  2026-11-24) asks for the pre-registered H4 targets on ≥2 shift types; obs-noise and action-delay are
  included as analysis cases.
- **Depends on:** T302, T102 (mid-episode injection is part of M1's T101 wrappers)
- **Target date:** Tue 2026-11-24 (G3)
- **Compute tier + budget:** `N_task × (N_shift,test + 1 nominal) × N_seed × L × (s_plan + s_sig) / 3600`
  hours (the `evaluate` subcommand has no `--episodes`; each seed is one injected episode). Expected
  > 3 laptop-hours → T1, sharded `--shard i/3 --resume` across the M1/M2/M3 accounts, logged in the
  compute log.
- **Files to create/modify:** `scripts/detect.py` (`evaluate` subcommand),
  `src/datdmpc/detect/detector.py` (bug fixes only; thresholds frozen), `tests/test_detector.py`,
  `notebooks/colab/M3_detect.ipynb`, `results/P3_detect/**`, `report/sections/*_M3.tex`.
- **Metric implementation:** `scikit-learn` is not in `environment/requirements-*.txt`; AUROC is computed
  with numpy/scipy (Mann–Whitney identity) and tested against a hand-computed case, or M1 is asked to add
  a dependency. `summary.json` adds `auroc`, `detection_delay_mean`, `missed_detections`,
  `false_alarms_per_1000`, `inject_at`, `detector_config_sha`.
- **Interface (binding):** `python scripts/detect.py evaluate --ckpt --task --shift --inject-at STEP
  --detector-config configs/experiments/M3_detector.yaml --seeds ... --out results/P3_detect/ [--resume]
  [--shard i/N]` (plus `--tier`, `--device`).
- **Exact commands:**

  ```powershell
  pytest -q tests/test_detector.py tests/test_signals.py
  python scripts/detect.py evaluate --ckpt checkpoints/mt30-5M.pt --task walker-walk --shift <dev level spec from configs/shifts.yaml> --inject-at <STEP> --detector-config configs/experiments/M3_detector.yaml --seeds 2000 --out outputs/debug/ --tier T0 --device cpu
  ```

  Colab (one shard per account; `i` = 1, 2, 3; nominal and each test level):

  ```python
  !python scripts/detect.py evaluate --ckpt /content/drive/MyDrive/DA-TDMPC2/checkpoints/mt30-19M.pt --task <study task> --shift none --inject-at <STEP> --detector-config configs/experiments/M3_detector.yaml --seeds <test seeds from PROJECT_PLAN> --out /content/drive/MyDrive/DA-TDMPC2/results/P3_detect/ --resume --shard <i>/3 --tier T1 --device cuda
  !python scripts/detect.py evaluate --ckpt /content/drive/MyDrive/DA-TDMPC2/checkpoints/mt30-19M.pt --task <study task> --shift <test level spec from configs/shifts.yaml> --inject-at <STEP> --detector-config configs/experiments/M3_detector.yaml --seeds <test seeds from PROJECT_PLAN> --out /content/drive/MyDrive/DA-TDMPC2/results/P3_detect/ --resume --shard <i>/3 --tier T1 --device cuda
  ```

- **Done when:**
  - [ ] Test: before `--inject-at` the shifted run is step-for-step identical to the nominal run with the same seed (signals and actions).
  - [ ] Test: AUROC, delay, missed detections and false alarms per 1,000 steps match hand-computed values on a synthetic alarm trace.
  - [ ] Test: `--resume` skips finished seeds; `--shard` splits deterministically.
  - [ ] `results/P3_detect/` holds complete run folders for every (study task × test level × seed) and the nominal runs, produced on T1 (`env.txt`), with `detector_config_sha` equal to the committed `configs/experiments/M3_detector.yaml`.
  - [ ] Only test levels and test seeds 0–99 appear in reported runs; thresholds were not changed after the first T303 run (git log of `M3_detector.yaml`).
  - [ ] The G3 verdict (H4 met / not met per shift type) is written in the handoff log with the evidence paths.
- **Faculty-report sentence:** "Completed T303: with shifts injected mid-episode, the detector reaches AUROC `<auroc>` with `<false_alarms_per_1000>` false alarms per 1,000 nominal steps and mean delay `<detection_delay_mean>` agent steps under `<shift spec>` on `<task>` (`results/P3_detect/<run_id>/summary.json`)."

### T503

**(shared, all) Clean-clone reproducibility check of one result per contribution**

- **Goal:** from a fresh clone at a tagged commit, re-run one committed result and confirm it meets the
  acceptance criterion written in [RUNS Step 5](../RUNS.md) before the check. My own result that may be
  chosen for reproduction by another member: `results/P3_detect/` (C3). The split of who reproduces what is confirmed at G3 (Tue 2026-11-24); each
  member reproduces a result produced by someone else.
- **Depends on:** T204, T303
- **Target date:** Sun 2026-12-06
- **Compute tier + budget:** the tier of the original run (from its `env.txt`); hours = sum of
  `wall_time_s` in the original run's `episodes.csv`.
- **Files to create/modify:** this page (handoff entry with original vs reproduced `summary.json` paths).
  Reproduced output goes to the gitignored `outputs/repro/`; nothing in `results/` is overwritten.
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
  - [ ] The result assigned to me is reproduced and meets the criterion in RUNS; the comparison is in my handoff log.
  - [ ] Any mismatch is explained and fixed, or reported honestly to M1 for the report.
- **Faculty-report sentence:** "Completed T503 (my part): `<result>` reproduced from a clean clone at `<tag>` within the pre-registered criterion (`<original summary.json path>` vs `<reproduced summary.json path>`)."

### T504

**(shared, all) Full draft → faculty feedback → final submission**

- **Goal:** my report sections are complete, every number in them is traceable to `results/`, and they
  are ready for M1's assembly. Milestones: full draft Tue 2026-12-08 → faculty feedback → final Sun
  2026-12-13 → submission Mon 2026-12-14. My sections (`report/sections/<section>_M3.tex`, names per
  M1's T502 section map, written from week 4, Wed 2026-11-11): profiling/compute cost (T008) and shift
  detection (T301–T303) — including the CSE 465 framing (ensembles for uncertainty, novelty detection with
  ROC analysis).
- **Depends on:** T503
- **Target date:** Mon 2026-12-14
- **Compute tier + budget:** none (no new experiments after the freeze, Wed 2026-12-02).
- **Files to create/modify:** `report/sections/*_M3.tex`, this page.
- **Exact commands:**

  ```powershell
  Select-String -Path report\sections\*_M3.tex -Pattern "VERIFY", "\[\["
  git status --short
  ```

- **Done when:**
  - [ ] My sections are in the full draft sent by Tue 2026-12-08.
  - [ ] The marker search prints nothing (no `VERIFY` marker and no `[[...]]` placeholder in my sections).
  - [ ] Every number in my sections cites a `results/` path or comes from `results/REGISTRY.csv` / `figures/` generated by M1.
  - [ ] Faculty feedback on my sections is addressed by Sun 2026-12-13.
- **Faculty-report sentence:** "Completed T504 (my part): sections on profiling and shift detection are final; every number is traceable to `results/` (`report/sections/<section>_M3.tex`)."
