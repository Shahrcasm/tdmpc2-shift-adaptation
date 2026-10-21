# AGENTS.md: Rules of Engagement (humans and AI agents)

Project: **DA-TDMPC2 (Detect-and-Adapt TD-MPC2)**, CSE 465 (Pattern Recognition and Neural Network), faculty: Dr. Mohammad Ashrafuzzaman Khan.
Repository: `tdmpc2-shift-adaptation`. Team-standard clone path: `C:\code\tdmpc2-shift-adaptation`.

This file is binding for every team member and every AI assistant (Claude Code, Cursor, others) working in this repository. AI assistants must read it completely before doing anything else. `CLAUDE.md` and `.cursor/rules/agents.mdc` only point here.

Related documents: [STATUS](docs/STATUS.md) (task board, single source of truth) · [PROJECT_PLAN](docs/PROJECT_PLAN.md) (science, hypotheses, metrics) · [RUNS](docs/RUNS.md) (environment, commands, Colab) · [REPO_SETUP](docs/REPO_SETUP.md) (GitHub settings) · team pages: [M1](docs/team/M1_Shahriar.md), [M2](docs/team/M2_Ishtiak.md), [M3](docs/team/M3_Talha.md).

Key dates (calendar-fixed, see [STATUS](docs/STATUS.md)): G0 Tue 2026-10-27 · G1 Tue 2026-11-03 · G2 Tue 2026-11-17 · G3 Tue 2026-11-24 · experiment freeze Wed 2026-12-02 (G4 stretch decision) · full draft Tue 2026-12-08 · final Sun 2026-12-13 · submission Mon 2026-12-14.

---

## 1. Team role matrix

M1 acts as **integrator**. All three members (M1 included) work only on their own `dev_*` branch and never push to `main`. **Only M1 merges** pull requests into `main`, every branch including his own `dev_shahriar`: M1 reviews, approves and merges the PRs of M2 and M3, and merges his own PRs without waiting for another member's approval (repository owner bypass of the approval rule, [REPO_SETUP §8](docs/REPO_SETUP.md)). M1 never bypasses the CI check `tests` and never pushes directly to `main`. M2 and M3 never click Merge, even though their Write role allows it (team rule; it cannot be enforced by settings on a personal-account repo <!-- VERIFY: GitHub 'restrict who can push' availability for personal repos -->). GitHub handles are not recorded anywhere in this repository; people are identified by slot and name only.

| Slot | Name | Student ID | Branch | Role |
|---|---|---|---|---|
| M1 | Md. Shahriar Rakib Rabbi | 2321937642 | `dev_shahriar` | Integrator (merges every PR, including his own) · infra · evaluation harness · perturbation suite · nominal evaluation · ranking-fidelity diagnostic · closed loop · C1 design (stretch) · figures · report assembly |
| M2 | Md. Ishtiak Ahmed Moyen | 2131580642 | `dev_ishtiak` | C2 embedding adaptation · baselines · degradation sweep · related work |
| M3 | Md. Abdullah Talha | 2222614642 | `dev_talha` | Profiling · C3 detection |

Owned paths for each slot: §2 below (the only copy).

---

## 2. File ownership table (binding)

This is the **only** copy of the ownership table; every other document links here instead of repeating it. If a path is not listed, nobody creates it until M1 has added it to this table (open an issue first).

| Path | Owner | Notes |
|---|---|---|
| `AGENTS.md`, `CLAUDE.md`, `README.md`, `LICENSE`, `.gitignore`, `.gitattributes`, `pyproject.toml` | M1 | `pyproject.toml` added in T001 so `pip install -e .` makes `datdmpc` importable |
| `.github/**` (PR template, issue templates, `workflows/ci.yml`) | M1 | |
| `.cursor/rules/agents.mdc` | M1 | |
| `environment/requirements-cpu.txt`, `environment/requirements-colab.txt` | M1 | |
| `third_party/tdmpc2/**` | M1 (read-only for everyone) | re-vendoring only via a dedicated M1 PR |
| `src/datdmpc/__init__.py`, `src/datdmpc/_upstream.py` | M1 | `_upstream.py` = bridge to vendored upstream (added in T001) |
| `src/datdmpc/envs/**` (`perturb.py`) | M1 | |
| `src/datdmpc/eval/**` (`harness.py`, `logging.py`) | M1 | |
| `src/datdmpc/closed_loop.py` | M1 | |
| `src/datdmpc/adapt/**` (`embedding.py`, `baselines.py`) | M2 | |
| `src/datdmpc/diagnostics/**` (`ranking_fidelity.py`) | M1 | T104, T205 |
| `src/datdmpc/detect/**` (`signals.py`, `detector.py`) | M3 | |
| `src/datdmpc/ranking/**` | M1 | stretch (C1) |
| `configs/shifts.yaml` | M1 | |
| `configs/experiments/M1_*.yaml` / `M2_*.yaml` / `M3_*.yaml` | M1 / M2 / M3 | owner prefix in filename |
| `scripts/get_checkpoints.py`, `scripts/smoke_test.py`, `scripts/eval.py`, `scripts/build_registry.py`, `scripts/make_figures.py` | M1 | |
| `scripts/adapt.py` | M2 | |
| `scripts/profile.py`, `scripts/detect.py` | M3 | |
| `notebooks/colab/M1_*.ipynb` / `M2_*.ipynb` / `M3_*.ipynb` | M1 / M2 / M3 | launchers only |
| `tests/conftest.py`, `tests/test_upstream_bridge.py`, `tests/test_smoke.py`, `tests/test_get_checkpoints.py`, `tests/test_perturb.py`, `tests/test_harness.py`, `tests/test_logging.py`, `tests/test_registry.py`, `tests/test_closed_loop.py`, `tests/test_ranking_fidelity.py`, `tests/test_ranking.py` | M1 | |
| `tests/test_embedding.py`, `tests/test_baselines.py` | M2 | |
| `tests/test_signals.py`, `tests/test_detector.py` | M3 | |
| `results/P1_degradation/**`, `results/P2_adapt/**` | M2 | produced by T103, T204 |
| `results/P0_profile/**`, `results/P3_detect/**` | M3 | T008, T302–T303 (T301 raw dumps go to `outputs/signals/`) |
| `results/P0_nominal/**`, `results/P1_ranking/**`, `results/P2_ranking_after_adapt/**`, `results/P3_closedloop/**` | M1 | T007, T104, T205, T304 |
| `results/REGISTRY.csv`, `figures/**` | M1 only | GENERATED by `build_registry.py` / `make_figures.py` |
| `report/main.tex`, `report/sections/*_M1.tex` | M1 | template `[[report template: IEEE conference unless the course specifies otherwise]]` |
| `report/sections/*_M2.tex` / `*_M3.tex` | M2 / M3 | from week 4 |
| `docs/STATUS.md`, `docs/PROJECT_PLAN.md`, `docs/RUNS.md`, `docs/REPO_SETUP.md` | M1 | STATUS.md edited by M1 only, at merge time |
| `docs/RELATED_WORK.md` | M2 | T009 |
| `docs/design/C2_embedding_adaptation.md` | M2 | T201 |
| `docs/design/C1_ranking.md` | M1 | T401 |
| `docs/design/C3_detection.md` | M3 | T302 |
| `docs/team/M1_Shahriar.md` / `M2_Ishtiak.md` / `M3_Talha.md` | M1 / M2 / M3 | each member edits only their own page |
| `docs/references/**` | M1 | paper + proposal PDFs |
| `checkpoints/MANIFEST.csv` | M1 | committed (T005); everything else in `checkpoints/` is gitignored |

**T001 scaffolding note.** In T001, M1 created placeholder stubs (a docstring describing the contract plus `NotImplementedError` pointing at the task ID) for every module and script in the layout, including those owned by M2 and M3. From the moment the `dev_*` branches exist, each stub belongs to the owner in the table above; the owner replaces it. Every script stub already defines its full `--help` interface (see §5.3) and exits with code 3 and the message "not implemented yet — see T0xx (owner Mx)".

Result folders: T007 writes `results/P0_nominal/`; T205 writes `results/P2_ranking_after_adapt/`. T301 raw per-step signal dumps go to the gitignored `outputs/signals/`; T302 calibration summaries and T303 evaluation summaries go to `results/P3_detect/`. The C3 design note `docs/design/C3_detection.md` is written in T302.

---

## 3. Start-of-session protocol (every session, PowerShell)

Laptops run Windows PowerShell 5.1, which does not support `&&`; run the lines below one at a time, in order. Set `$branch` to your own branch (M1 `dev_shahriar`, M2 `dev_ishtiak`, M3 `dev_talha`).

```powershell
cd C:\code\tdmpc2-shift-adaptation
$branch = "dev_ishtiak"
git status
git fetch origin
git checkout $branch
git merge origin/main
.\.venv\Scripts\Activate.ps1   # or: conda activate datdmpc
python scripts/smoke_test.py
```

Then:

1. `git status` must report a clean working tree before you fetch. If it does not, commit or finish the previous session's work first (end-of-session protocol, §6).
2. `git merge origin/main`: resolve conflicts **only in files you own**. A conflict in a file you do not own means you edited it by mistake: run `git merge --abort`, then tell M1 (issue or handoff log) instead of resolving it yourself.
3. `python scripts/smoke_test.py` runs in `auto` mode (full mode if the checkpoint and the T006 harness are available, otherwise `--mode tiny` with a printed notice); target under 2 minutes on a laptop CPU. If it fails, fix that first or log it as a blocker; do not start new work on a broken environment.
4. Read [docs/STATUS.md](docs/STATUS.md) (gates, task board, compute ledger), then your own team page in `docs/team/`.
5. Pick the **lowest-numbered unblocked task** you own (all its "Depends on" tasks are Done in STATUS.md) and open its task card in your team page. No experiment runs without a task card.

If activating the environment is not recognised in the editor terminal, see the troubleshooting table in [RUNS](docs/RUNS.md).

---

## 4. In-session rules

### 4.1 Strict file ownership
- Edit only paths you own (§2). Need a change in someone else's file? Open a GitHub issue (task template) addressed to the owner by slot, or add a request to the handoff log on your own team page. Never "just fix it".
- `third_party/tdmpc2/` is **read-only for everyone**, including M1 and AI assistants. Extend upstream behaviour by subclassing or wrapping from `src/datdmpc/`, importing it through `src/datdmpc/_upstream.py` (which puts `third_party/tdmpc2/tdmpc2/` on `sys.path`, because upstream modules import each other as top-level packages, e.g. `from common import ...`). Re-vendoring happens only in a dedicated M1 PR; the pinned commit is recorded in `third_party/tdmpc2/UPSTREAM_COMMIT.txt` (`e9f59321933cbc8e11a002b842adc7d4ffae8ff1`).
- `docs/STATUS.md`, `results/REGISTRY.csv` and `figures/` are **M1-only**. Members report progress on their own team page; M1 syncs STATUS.md at merge time (§7).
- New files go only under paths you own. A new file at an unlisted path needs an M1 update of §2 first.

### 4.2 Zero-hallucination
- **No number** appears in docs, the report, PR descriptions or faculty updates unless it is copied from a file under `results/` and cited by its path (e.g. `results/P1_degradation/<run_id>/summary.json`). The only other allowed numbers are dates, task IDs, upstream config values cited with their file, and pre-registration placeholders (`[[X]]`, `[[K_max]]`, etc.).
- **No invented citations.** A paper reference that no team member has read stays marked `<!-- VERIFY citation -->`. Any other unverified external fact is marked `<!-- VERIFY: what to check -->` and gets a verification sub-task in the owning task card.
- **AI assistants must open the upstream file** in `third_party/tdmpc2/` before naming any upstream function, class, attribute, config key or CLI flag, and must answer "unknown" rather than guess. The same applies to our own scripts: use only the flags defined in §5.3; never invent new ones in docs or commands.
- **Pre-registration.** Hypothesis thresholds (`[[X]]`, `[[Y]]`, `[[A]]`, `[[F]]`, `[[D]]`, `[[K_max]]`) are proposed by the owner in their design note (C2: M2 in T201; C3: M3 in T302; C1: M1 in T401) and copied by M1 into the Pre-registration section of [PROJECT_PLAN](docs/PROJECT_PLAN.md) in the same merge, **before** any corresponding run. A run whose threshold is not in `docs/PROJECT_PLAN.md` on `main` must not start. Thresholds are never edited after results exist.

Verified upstream facts that override older descriptions (including the bootstrap brief and the paper's Table 9):

| Fact | Source |
|---|---|
| The task embedding `e` of our checkpoints `mt30-5M` and `mt30-19M` is **64-dimensional**: `cfg.task_dim = 96 if cfg.task == 'mt80' or cfg.get('model_size', 5) in {1, 317} else 64`. The embedding table is 30 × 64; C2 adapts one row (64 numbers). Never write "96" for our checkpoints. | `third_party/tdmpc2/tdmpc2/common/parser.py` |
| `e` is `nn.Embedding(len(cfg.tasks), cfg.task_dim, max_norm=1)` (ℓ2-norm ≤ 1 enforced at lookup, in place on the weight row). | `third_party/tdmpc2/tdmpc2/common/world_model.py` |
| For `task == 'mt30'` and `model_size == 19`, `latent_dim` is overridden to 512. | `third_party/tdmpc2/tdmpc2/common/parser.py` |
| Upstream `evaluate.py` and `train.py` assert CUDA; `TDMPC2` hard-codes `cuda:0` (also `common/scale.py`, `common/buffer.py`). On CPU we subclass or wrap in `src/datdmpc/eval/harness.py` (T006); never edit upstream. `WorldModel` has no device hard-coding. | `third_party/tdmpc2/tdmpc2/tdmpc2.py`, `evaluate.py`, `train.py` |
| Upstream does not support single-task evaluation of a multitask checkpoint; our harness (T006) does it with a fixed `task_idx`. | `third_party/tdmpc2/README.md`, `evaluate.py` |
| DMControl episodes: each agent action is applied twice (action repeat 2), 500 agent decisions per episode. | `third_party/tdmpc2/tdmpc2/envs/dmcontrol.py` |

### 4.3 Reproducibility
- Every run writes its own folder `results/<phase>_<exp>/<run_id>/` containing `config.yaml`, `episodes.csv`, `summary.json`, `env.txt`, `git_sha.txt`. Runs are started only through our scripts (§5.3), which write these files.
- **Results schema (binding, summary; full definition in [RUNS](docs/RUNS.md)):**
  - `run_id` = `<ckpt-stem>__<task>__<shift>__<method>__seed<seed>` with `:` replaced by `-` (Windows-safe), e.g. `mt30-19M__walker-walk__mass-1.5__B0__seed0`.
  - `config.yaml`: all CLI arguments plus the resolved config.
  - `episodes.csv`: one row appended and flushed per finished episode, columns `run_id,task,task_idx,shift_type,shift_level,method,seed,episode,return,length,wall_time_s,tier,shard,timestamp`.
  - `summary.json`: at minimum `run_id, n_episodes, mean_return, ci95_low, ci95_high` (plus method-specific keys).
  - `env.txt`: python, torch, mujoco, dm_control, numpy versions; OS; CPU; device; tier (`T0`, `T1`, `T1b`).
  - `git_sha.txt`: the commit the run was made from. Run from a committed state.
- **Seed convention** (a convention, not a result): evaluation/test seeds 0–99; detector calibration seeds 1000–1099; dev-tuning seeds 2000–2099. These ranges are disjoint by construction; never reuse a seed range for another purpose.
- Shift levels are split into dev (tuning) and held-out test (reported only) in `configs/shifts.yaml` (T102). Never tune on test levels.

### 4.4 Compute discipline
- T008 profiling decides all budgets; never assume a sec/step value. Every task card states `#tasks × #shifts × #seeds × #episodes × steps × sec/step = hours` before the run.
- More than 3 laptop-hours → run on Colab (T1), sharded across the three accounts with `--shard i/N` (1-based) and always with `--resume`. Kaggle (T1b) only if Colab GPU is unavailable for more than one day. Record every sweep in the compute ledger via your team page (M1 copies it into STATUS.md).
- Laptops (T0): `torch.set_num_threads(4)`, one evaluation process at a time, no video saving, `compile=False`, `--device cpu` (T0 is the CPU tier). Which task runs where: [RUNS §1.7](docs/RUNS.md).
- **MPPI settings are never changed in reported results.** They are the upstream defaults in `third_party/tdmpc2/tdmpc2/config.yaml` (`iterations: 6`, `num_samples: 512`, `num_elites: 64`, `num_pi_trajs: 24`, `horizon: 3`, `min_std: 0.05`, `max_std: 2`, `temperature: 0.5`), plus the upstream heuristic in `tdmpc2.py` that adds 2 iterations when `action_dim >= 20`.
- Never download the mt30/mt80 training datasets. Only the released checkpoints `mt30-5M.pt` and `mt30-19M.pt` are used, fetched by `scripts/get_checkpoints.py` and verified by sha256.

### 4.5 Privacy and licensing
- Never commit: `*.pt` or any checkpoint, datasets, videos, Hugging Face / Google tokens, `.env`, any file larger than 5 MB, or Drive paths containing personal e-mail addresses. Checkpoints live in the shared Drive folder `DA-TDMPC2/checkpoints/` and in the gitignored local `checkpoints/`. No Git LFS.
- Do not record GitHub handles anywhere in the repository.
- Our code is MIT (`LICENSE`). Upstream TD-MPC2 is MIT; its `LICENSE` stays in `third_party/tdmpc2/` unchanged. The repository stays private until the course is graded.

### 4.6 Commits
- Format: `T<ID>: <imperative summary>`, e.g. `T202: add e-only adaptation loop`. One task per commit.
- Work in progress on your own branch: `T<ID>: wip - <what>`.
- `T000` is reserved for the integrator's status syncs (§7). Merge commits keep GitHub's default message.
- Stage files explicitly by path (`git add src/datdmpc/adapt/embedding.py`); do not stage with `git add -A` or `git add .` without first checking `git status` for files you do not own.

### 4.7 AI-assistant rules
- Read this file first, then [STATUS](docs/STATUS.md) and the team page of the human you are working for. Determine the slot from the current branch (`git branch --show-current`); if it is not one of the three `dev_*` branches, ask before editing anything.
- Never run `git push --force` (or `--force-with-lease`), `git reset --hard`, `git rebase`, or `git commit --amend` on pushed commits. Never push to `main`.
- Never edit outside the owned paths of the current slot; never edit `third_party/`.
- Never delete or overwrite anything under `results/`. Rerun interrupted runs with `--resume`; a changed configuration gets a new `run_id`.
- Never weaken, skip or delete a test to make it pass; never change MPPI settings; never download training datasets.
- Use only the script interfaces in §5.3 and upstream facts you have opened in `third_party/tdmpc2/`; otherwise say "unknown" or write a `<!-- VERIFY: ... -->` marker.
- Write PowerShell 5.1 commands for laptops (no `&&`; one command per line, or `cmd1; if ($?) { cmd2 }`); Colab cells may use `!`, `%cd` and `&&`.
- End every session by listing the files changed (`git status --short`) and stating which task ID they belong to.

### 4.8 Windows and code rules (we develop on native Windows; results come from Colab/Linux)
- All code runs unchanged on Windows and Linux: use `pathlib.Path` for every path; never hard-code `C:\` or `/content/`. Paths in docs use forward slashes.
- No shell scripts (`.sh`, `.bat`, `.ps1`): every tool is a Python script under `scripts/`.
- No multiprocessing on laptops (`num_workers=0`).
- **Rendering and `MUJOCO_GL`.** Upstream sets `MUJOCO_GL` (default `egl`) only at the top of its CLI entry points `evaluate.py` and `train.py`; its library modules do not set it. Our code never imports those entry points. `src/datdmpc/_upstream.py` is the **single place** in our code that handles `MUJOCO_GL`, before `dm_control` is imported, and it only sets the variable if you have not set it yourself: with rendering off (laptops, CI, all evaluation runs) it sets `MUJOCO_GL=disable` on every OS (an official dm_control no-renderer value); with `render=True` it sets `egl` on Linux only (Colab GPU runtime, videos). Physics stepping never needs a GL context. CI sets `MUJOCO_GL: disable` explicitly. Rule for everyone: rendering is off on laptops and CI; `egl` is used only on a Colab GPU runtime when videos are wanted. **Never set `MUJOCO_GL=egl` on Windows**: upstream `envs/__init__.py` then raises the misleading `ValueError: Failed to make environment "walker-walk": please verify that dependencies are installed and that the task exists.` (fix: `Remove-Item Env:MUJOCO_GL` in PowerShell, and check it is not set in your user environment variables). Do not set `MUJOCO_GL` anywhere else in our code. Tested on M1's Windows 11 laptop on 2026-10-21 in a Python 3.11 venv with the pinned packages (T001); the env check on each laptop is T002–T004.
- **Scripts import `datdmpc` first.** Every script under `scripts/` must `import datdmpc` (the `try`/`except` block used by the existing stubs) before importing torch, tensordict or any other heavy module. `python scripts/<x>.py` puts `scripts/` first on `sys.path`, so `scripts/profile.py` would shadow the standard-library `profile` module that `cProfile` needs (imported via tensordict → `torch._dynamo`). `src/datdmpc/__init__.py` removes `scripts/` from `sys.path` on import. `tests/test_smoke.py` guards this with a real subprocess run.
- Line endings are LF, enforced by `.gitattributes` (`* text=auto eol=lf`).
- Long paths: `git config --global core.longpaths true` (see [RUNS](docs/RUNS.md)); keep the clone at `C:\code\tdmpc2-shift-adaptation`, never inside OneDrive, Documents or Desktop.
- A result counts only if it was produced on Colab or reproduced there. Laptop numbers are for debugging only, **except** T0 CPU wall-time measurements, which are the point of the C2 cost claim (record `--tier T0`).

---

## 5. Reference: environments, tiers and script interfaces

### 5.1 Tiers
| Tier | Where | Use |
|---|---|---|
| T0 | Native Windows laptop, Python 3.11 venv (`.venv`) or Conda, PowerShell, CPU torch | Coding, tests, smoke tests, wrappers, single-episode checks, `e`-only adaptation, detector calibration, plots, CPU wall-time |
| T1 | Google Colab (free), three accounts in parallel | Evaluation sweeps (sharded), B1/B2 finetuning baselines, any C1 pilot |
| T1b | Kaggle (backup) | Only if Colab GPU is unavailable for more than one day |

### 5.2 Environment
Python 3.11 (per `third_party/tdmpc2/docker/environment.yaml`). Install order and pins: [RUNS](docs/RUNS.md) and `environment/requirements-cpu.txt` / `environment/requirements-colab.txt`.

### 5.3 Our script interfaces (binding; use exactly these flags)
Every script runs as `python scripts/<name>.py ...` from the repository root. Shared flags where applicable: `--ckpt PATH` · `--task NAME` (mt30 task name, or `all`) · `--shift SPEC` · `--episodes N` · `--seed S` or `--seeds S1 S2 ...` · `--out DIR` · `--resume` · `--shard i/N` (1-based) · `--tier {T0,T1,T1b}` (default T0) · `--device {cpu,cuda}` (default cpu).
Shift `SPEC`: `none` or `<type>:<level>`, type ∈ {`mass`, `friction`, `actuator`, `gravity`, `obs_noise`, `action_delay`}; alternative `--shifts-from configs/shifts.yaml --split {dev,test,all}`. Concrete levels are chosen in T102.

| Script / module | Owner · Task | Interface |
|---|---|---|
| `scripts/get_checkpoints.py` | M1 · T005 | `--models mt30-5M mt30-19M [--dest checkpoints] [--verify-only]` |
| `scripts/smoke_test.py` | M1 · T001 / T006+T101 | `[--mode {auto,tiny,full}] [--ckpt checkpoints/mt30-5M.pt] [--task walker-walk] [--steps 50] [--shift mass:1.5] [--seed 0]` |
| `scripts/eval.py` | M1 · T006 | `--ckpt --task --shift [--shifts-from --split] --episodes --seed/--seeds --out [--resume] [--shard i/N] [--tier] [--device] [--model-size {5,19}]` (method label always `B0`) |
| `scripts/profile.py` | M3 · T008 | `--ckpt --task --what {plan,adapt,all} --steps N --device --tier --out results/P0_profile/` |
| `scripts/adapt.py` | M2 · T202–T204 | `--ckpt --task --shift --method {e_only,e_ln,rand_e,full_ft,partial_ft} --K N --grad-steps N --lr LR --seed/--seeds --episodes N --out [--resume] [--shard i/N] [--tier] [--device]` (`e_ln` = G2 fallback: task embedding + LayerNorm affine parameters) |
| `scripts/detect.py` | M3 · T301–T303 | `signals --ckpt --task --shift --episodes --seed --out outputs/signals/` · `calibrate --ckpt --task --seeds ... --episodes --out results/P3_detect/` · `evaluate --ckpt --task --shift --inject-at STEP --detector-config configs/experiments/M3_detector.yaml --seeds ... --out results/P3_detect/ [--resume] [--shard i/N]` |
| `python -m datdmpc.diagnostics.ranking_fidelity` | M1 · T104/T205 | `--ckpt --task --shift --states N --candidates M --horizon H --seed --out results/P1_ranking/ [--embedding PATH/adapted_embedding.json]` |
| `python -m datdmpc.closed_loop` | M1 · T304 | `--ckpt --task --shift --inject-at STEP --detector-config ... --adapt-config ... --seeds ... --episodes --out results/P3_closedloop/ [--resume] [--shard i/N]` |
| `scripts/build_registry.py` | M1 · T501 | `[--results results] [--out results/REGISTRY.csv]` |
| `scripts/make_figures.py` | M1 · T501 | `[--registry results/REGISTRY.csv] [--out figures]` |

Changing an interface requires a PR by the script's owner that updates this table and [RUNS](docs/RUNS.md) in the same PR (via M1 for M1-owned docs).

---

## 6. End-of-session protocol (PowerShell)

Run your own tests (M1: `tests/test_upstream_bridge.py tests/test_smoke.py tests/test_get_checkpoints.py tests/test_perturb.py tests/test_harness.py tests/test_logging.py tests/test_registry.py tests/test_closed_loop.py tests/test_ranking_fidelity.py tests/test_ranking.py`; M2: `tests/test_embedding.py tests/test_baselines.py`; M3: `tests/test_signals.py tests/test_detector.py`), then the smoke test, then commit and push. Run only the test files that already exist (pytest stops with an error on a missing file). Example for M2 working on T202 (`tests/test_baselines.py` is created only in T203):

```powershell
cd C:\code\tdmpc2-shift-adaptation
$branch = "dev_ishtiak"
pytest -q tests/test_embedding.py
python scripts/smoke_test.py
git status --short
git add src/datdmpc/adapt/embedding.py tests/test_embedding.py docs/team/M2_Ishtiak.md
git commit -m "T202: add e-only adaptation loop"
git push origin $branch
```

Before committing, update your own team page:
1. Task status in **My Tasks** (To Do / In Progress / Done / Blocked).
2. A **handoff log** entry (date · task · what was done · files changed · result path · blockers · next).
3. Faculty-update bullets for the week, each with a number copied from and cited to a `results/` file.
4. Compute used (tier, account, hours) for any run, so M1 can copy it into the compute ledger.

Then, on GitHub, open or refresh the pull request from your branch to `main`, titled `T<ID>: <summary>`, with the "Done when" checklist from the task card ticked (only tick what is verifiably true). Before closing the editor, list the files changed in the session (`git status --short` and the commit list) in the handoff entry.

---

## 7. Integrator merge protocol (M1)

`main` is protected (pull request required, 1 approval, required status check `tests` from workflow `ci`, shown in the GitHub UI as `ci / tests`; no force pushes; administrators included). Merges therefore happen **only through the GitHub pull-request page**, using **"Create a merge commit"**. Squash and rebase merging are disabled because the `dev_*` branches are long-lived. Do not delete `dev_*` branches after merging.

M1 reviews and merges PRs from M2 and M3. **Only M1 merges pull requests into `main`.** M1 merges his own PRs (from `dev_shahriar`) after checking them with the same checklist, without waiting for another member's approval (repository owner bypass of the approval rule only; never of the CI check `tests`; never a direct push to `main`). M2 and M3 never click Merge, even though their Write role allows it (team rule; it cannot be enforced by settings on a personal-account repo <!-- VERIFY: GitHub 'restrict who can push' availability for personal repos -->).

Set `$pr` to the branch under review (`dev_ishtiak`, `dev_talha`; for M2/M3 reviewing M1: `dev_shahriar`).

```powershell
cd C:\code\tdmpc2-shift-adaptation
$pr = "dev_ishtiak"
git fetch origin
git log --oneline --no-merges "origin/main..origin/$pr"
git diff --name-only "origin/main...origin/$pr"
git log --name-only --format="" "origin/main..origin/$pr"
git diff --stat "origin/main...origin/$pr"
git diff --name-only --diff-filter=d "origin/main...origin/$pr" | ForEach-Object { $size = [long](git cat-file -s "origin/${pr}:$_"); if ($size -gt 5MB) { "$_  $size bytes" } }
```

Review checklist (all must be true before approving):

- [ ] **CI green**: the `tests` check (aggregating the `windows-latest` and `ubuntu-latest` legs) passed on the PR.
- [ ] **Only owned paths touched**: every path printed by `git diff --name-only "origin/main...origin/$pr"`, and every path touched by any commit (`git log --name-only ...`), belongs to the PR author in §2. Nothing under `third_party/`, `docs/STATUS.md`, `results/REGISTRY.csv` or `figures/` from M2/M3.
- [ ] **Commit messages** follow `T<ID>: <imperative summary>` (one task per commit; `wip -` commits allowed).
- [ ] **"Done when" verifiably satisfied**: open the result files named in the task card and PR, e.g. `git show "origin/${pr}:results/P1_degradation/<run_id>/summary.json"`, and check the run folder has `config.yaml`, `episodes.csv`, `summary.json`, `env.txt`, `git_sha.txt`, and that `env.txt` shows the tier required for a reported result (T1/T1b, or T0 for CPU wall-time).
- [ ] **No file larger than 5 MB** (the byte-size command above, the last one, prints nothing; `git diff --stat` counts lines, not bytes, so it cannot show this) and no `*.pt`, dataset, video, token or `.env` in any commit.
- [ ] **Numbers in docs match `results/`**: every number in changed docs, report sections and the faculty-update bullets is cited to a `results/` path and matches that file.
- [ ] No weakened or deleted tests; no MPPI setting changed; no new script flags beyond §5.3.
- [ ] Approve (M2/M3 PRs). M1 then merges on GitHub with **"Create a merge commit"** (never squash, never rebase). For M1's own PRs no approval is needed: M1 merges with the owner bypass once `tests` is green.

After merging, sync STATUS in a **separate `T000: sync status` commit** on `dev_shahriar`. Because `main` accepts changes only through reviewed PRs, the sync reaches `main` through a PR titled `T000: sync status`, which M1 merges once CI is green (several merges on the same day may share one sync):

```powershell
cd C:\code\tdmpc2-shift-adaptation
git status
git checkout dev_shahriar
git fetch origin
git merge origin/main
# edit docs/STATUS.md now (see below), then:
git add docs/STATUS.md
git commit -m "T000: sync status"
git push origin dev_shahriar
```

At the comment line, edit `docs/STATUS.md`: task statuses (Done by & date, evidence path or PR number), gate table, compute ledger, the global handoff log (copied from the merged team page), and "Last synced". Then open (or refresh) the PR `T000: sync status` from `dev_shahriar` to `main` and merge it once `tests` is green. The PR shows every `dev_shahriar` commit not yet in `main`; M1 checks all of them with the checklist above before merging.

**Gate tags.** On each gate day, after all three members have decided the gate and the corresponding `T000: sync status` PR is merged, tag the resulting `main` commit with an annotated tag recording the outcome (Passed, or Failed→fallback) and the evidence path:

```powershell
git fetch origin
git tag -a g0 origin/main -m "G0 2026-10-27: <Passed|Failed->fallback>; evidence: <results path>"
git push origin g0
```

| Tag | Gate | Date |
|---|---|---|
| `g0` | G0: harness evaluates one mt30 task; sec/step known on laptop and Colab | Tue 2026-10-27 |
| `g1` | G1: shift benchmark gives clear drops | Tue 2026-11-03 |
| `g2` | G2: pre-registered C2 recovery threshold on mass/friction | Tue 2026-11-17 |
| `g3` | G3: pre-registered C3 detection targets | Tue 2026-11-24 |
| `g4` | G4 (stretch): C1 pilot decision / H5, only if G2 passed by 2026-11-17 | Wed 2026-12-02 (freeze) |

Gate criteria in full: [PROJECT_PLAN](docs/PROJECT_PLAN.md) and [STATUS](docs/STATUS.md). Tags are never moved or deleted.
