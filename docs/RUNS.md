# RUNS — Reproducibility and Execution Guide (DA-TDMPC2)

Owner: M1 (see the file ownership table in [AGENTS.md](../AGENTS.md)). Created in T001 (2026-10-21).
Members who find an error or a missing troubleshooting case report it to M1 through an issue or their
team-page handoff log; M1 updates this file.

Related documents: [STATUS](STATUS.md) (task board, compute ledger) · [PROJECT_PLAN](PROJECT_PLAN.md)
(hypotheses, metrics, protocol) · [REPO_SETUP](REPO_SETUP.md) (GitHub settings) · [AGENTS](../AGENTS.md)
(rules, binding script interfaces) · team pages: [M1](team/M1_Shahriar.md), [M2](team/M2_Ishtiak.md),
[M3](team/M3_Talha.md).

**Conventions used on this page**

- Laptop commands are **Windows PowerShell 5.1**. `&&` does not exist there: commands are written one per
  line, or as `cmd1; if ($?) { cmd2 }`.
- Every laptop command runs from the repository root `C:\code\tdmpc2-shift-adaptation` inside the Python 3.11
  virtual environment (`.venv`, activated via `.\.venv\Scripts\Activate.ps1`) or conda environment (`datdmpc`).
- Colab cells use `!` and `%cd`; the Colab clone lives at `/content/tdmpc2-shift-adaptation`; the shared
  Drive folder is `/content/drive/MyDrive/DA-TDMPC2/`.
- `<...>` is a placeholder: replace it, **including the angle brackets**, before running (PowerShell
  rejects a literal `<`). The repository URL used in every clone command is
  `https://github.com/Shahrcasm/tdmpc2-shift-adaptation.git`.
- No measured number appears on this page. Every value below is a date, a task ID, an upstream fact
  cited with its file, a published checkpoint size/hash, or a placeholder.

Contents: [Step 1 — Windows environment and checkpoints](#step-1--windows-environment-and-checkpoints-once-per-laptop)
· [Step 2 — Preprocessing: manifest and config verification](#step-2--preprocessing-manifest-and-config-verification)
· [Step 3 — Running](#step-3--running)
· [Step 4 — Commit vs ignore](#step-4--commit-vs-ignore)
· [Step 5 — Regenerate report numbers and clean-clone check](#step-5--regenerate-report-numbers-and-clean-clone-check-t503)

---

## Step 1 — Windows environment and checkpoints (once per laptop)

Tasks: T002 (M1), T003 (M2), T004 (M3). Record the outcome and the Windows version in your own team page.

### 1.1 Prerequisites (Git and Python 3.11)

1. **Git for Windows** (includes Git Credential Manager, which handles the GitHub login on first clone):
   install from <https://git-scm.com/download/win> with default options, or in PowerShell:

   ```powershell
   winget install -e --id Git.Git
   ```

2. **Python 3.11** (matching upstream `third_party/tdmpc2/docker/environment.yaml`; CI uses Python 3.11):
   - **Recommended (native `venv`, lightest on laptops):** Install official Python 3.11 from python.org or via `winget install Python.Python.3.11`.
   - **Alternative (Miniconda):** `winget install -e --id Anaconda.Miniconda3` if you prefer managing environments through conda.

3. In VS Code / Cursor: set the default terminal profile to **PowerShell** (Command Palette →
   "Terminal: Select Default Profile"), select the interpreter of the `.venv` environment once created
   (Command Palette → "Python: Select Interpreter" → `.\.venv\Scripts\python.exe`).

### 1.2 Clone and create the environment

Using native Python 3.11 `venv` (recommended for laptops with 12 GB RAM):

```powershell
git config --global core.longpaths true
git config --global user.name "<your full name>"
git config --global user.email "<email registered on your GitHub account>"
New-Item -ItemType Directory -Force C:\code
git clone https://github.com/Shahrcasm/tdmpc2-shift-adaptation.git C:\code\tdmpc2-shift-adaptation
cd C:\code\tdmpc2-shift-adaptation
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python --version
pip install torch==2.7.1 --index-url https://download.pytorch.org/whl/cpu
pip install -r environment/requirements-cpu.txt
pip install -e . --no-deps
pip check
pip show torch tensordict mujoco dm-control numpy
pytest -q
python scripts/smoke_test.py --mode tiny
```

*(Alternative with Conda: `conda create -n datdmpc python=3.11 -y; conda activate datdmpc`, then run the pip commands above).*

- The clone must be at `C:\code\tdmpc2-shift-adaptation`: a short path outside OneDrive, Documents and
  Desktop (OneDrive sync locks files and long paths break some installs).
- **Install order matters** (from `environment/requirements-cpu.txt`): CPU torch first from the PyTorch
  CPU index, then the pinned requirements, then our package in editable mode **without dependencies**
  (`pyproject.toml` declares none on purpose; all pins live in `environment/`).
- `python --version` must print Python 3.11.x; `pip show torch` must show `2.7.1+cpu` and `tensordict`
  `0.8.3`.
- `python scripts/smoke_test.py --mode tiny` must end with `[smoke] OK` (details in
  [Step 2](#21-smoke-test)).

**Rendering is off on laptops.** No video is saved and no window is opened. Do **not** set `MUJOCO_GL`
yourself on a laptop: `configure_rendering()` in `src/datdmpc/_upstream.py` is the single place in our
code that handles it (with rendering off it sets `MUJOCO_GL=disable`, and it respects a value you already
set). Tested on M1's Windows 11 laptop on 2026-10-21 (Python 3.11 venv with the pinned packages):
`disable` is set automatically when unset and the tiny smoke test passes. **Never set `MUJOCO_GL=egl` on
Windows**: it breaks environment creation with a misleading error (troubleshooting table below). `egl` is
used only on a Colab GPU runtime when videos are wanted. Details: T001 note on
[M1's team page](team/M1_Shahriar.md#t001-note-mujoco_gl-on-windows); T002/T003/T004 repeat the check
inside each member's Miniconda env.

### 1.3 Dependencies: what we keep and what we skip

Upstream reference: `third_party/tdmpc2/docker/environment.yaml` at the pinned commit
`e9f59321933cbc8e11a002b842adc7d4ffae8ff1` (`third_party/tdmpc2/UPSTREAM_COMMIT.txt`). We only evaluate
released checkpoints on DMControl state-based tasks, without rendering, so we keep only what that needs.

| Upstream entry | Upstream pin | Ours (laptop + CI: `requirements-cpu.txt`) | Reason |
|---|---|---|---|
| `python` | 3.11 | 3.11 (conda) | match upstream |
| `torch` | 2.7.1 | 2.7.1, CPU build | laptops have no usable CUDA |
| `numpy` | 1.24.4 | 1.24.4 (Colab: 1.26.4, see [3(b)](#3b-colab-template-t1)) | match upstream |
| `mujoco` | 3.1.2 | 3.1.2 | physics |
| `dm-control` | 1.0.16 | 1.0.16 | DMControl tasks |
| `gymnasium` | 0.29.1 | 0.29.1 | imported by upstream `envs/` |
| `tensordict` | 0.8.3 | 0.8.3 | imported by upstream `common/world_model.py` |
| `hydra-core`, `omegaconf` | 1.3.2, 2.3.0 | 1.3.2, 2.3.0 | upstream config handling (`common/parser.py` imports `hydra`) |
| `termcolor`, `pandas` | 2.4.0, 2.0.3 | 2.4.0, 2.0.3 | imported by upstream `common/logger.py` |
| `torchrl` | 0.8.1 | skipped | imported only by upstream `common/buffer.py` (replay buffer for training); our code does not import that module. If B1/B2 (T203) need it, M2 asks M1 for a PR that adds the upstream pin. |
| `kornia`, `h5py`, `tqdm` | 0.7.2, 3.11.0, 4.66.4 | skipped | not needed for DMControl state-based evaluation |
| `wandb`, `submitit`, `hydra-submitit-launcher` | 0.17.4, 1.5.1, 1.2.0 | skipped | experiment tracking / cluster launching |
| `glfw`, `imageio`, `imageio-ffmpeg`, `moviepy`, `ffmpeg`; conda `glew`, `glib` | (various) | skipped | rendering and video only |
| `gym==0.21.0`, `mujoco-py`, ManiSkill2, Meta-World, MyoSuite, box2d | commented out upstream | skipped | other benchmarks |
| — | — | `pyyaml`, `scipy`, `matplotlib`, `pytest` | our additions (configs, statistics, figures, tests) |

### 1.4 Troubleshooting (Windows install)

Add every new problem and the fix that worked to this table (report it to M1, who edits this file).

| Symptom | Likely cause | Fix |
|---|---|---|
| `ImportError: DLL load failed while importing ...` or `OSError: [WinError 126] ... error loading ... .dll or one of its dependencies` when importing `torch` or `mujoco` | Microsoft Visual C++ Redistributable (x64) missing or outdated | Install the latest **Microsoft Visual C++ Redistributable for Visual Studio (x64)** from Microsoft, reboot, reopen PowerShell, run `conda activate datdmpc`, retry the import. |
| `Filename too long` during `git clone` / `git checkout`, or `pip install` failing with `No such file or directory` on a very long path | Windows 260-character path limit | `git config --global core.longpaths true`; keep the clone at `C:\code\tdmpc2-shift-adaptation`. If pip still fails, enable long paths in Windows from an **administrator** PowerShell: `New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force`, then reboot. |
| `conda : The term 'conda' is not recognized ...` in the VS Code / Cursor terminal (works in Anaconda Prompt) | `conda init powershell` not run, or the editor was not restarted, or the terminal is cmd / Git Bash | Run `conda init powershell` in **Anaconda PowerShell Prompt (Miniconda3)**; close the editor completely and reopen; set the default terminal profile to PowerShell (Step 1.1, item 4). |
| `... profile.ps1 cannot be loaded because running scripts is disabled on this system` when a PowerShell window opens, and `conda activate` fails | PowerShell execution policy blocks the conda profile script | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` (no administrator rights needed), then reopen the terminal. |
| `Python was not found; run without arguments to install from the Microsoft Store` or `python --version` is not 3.11 | Environment not active; the Windows Store alias is used | `conda activate datdmpc`; check with `Get-Command python` that the path is inside the Miniconda `envs\datdmpc` folder; optionally turn off the `python.exe` / `python3.exe` App execution aliases in Windows Settings. |
| `conda create` stops with a message that the Terms of Service have not been accepted for a channel <!-- VERIFY: whether the Miniconda version installed in T002 asks for channel Terms-of-Service acceptance; record the exact message and the command that fixed it here (T002) --> | Recent conda versions require accepting the default channels' terms once | Run the `conda tos accept ...` commands that the error message prints, then rerun `conda create`. |
| `ValueError: Failed to make environment "<task>": please verify that dependencies are installed and that the task exists.` on a laptop, or any error mentioning `MUJOCO_GL`, `egl`, OpenGL or GLFW | `MUJOCO_GL=egl` (a Linux-only backend) is set on Windows, often copied from a Colab snippet or set as a Windows user variable; upstream `envs/__init__.py` hides the real import error behind this message | Rendering is off on laptops; do not set `MUJOCO_GL`. Remove it for the session: `Remove-Item Env:MUJOCO_GL`; remove a permanent user variable: `[Environment]::SetEnvironmentVariable("MUJOCO_GL", $null, "User")` and reopen the terminal. `python scripts/smoke_test.py --mode tiny` prints the value in effect as `mujoco_gl`. |
| `import tensordict` fails or warns that its C++ extension could not be loaded; errors inside `tensordict` when building the world model | `torch` and `tensordict` versions do not match (another install replaced torch, or a CUDA build was pulled in) | `pip show torch tensordict` must show `2.7.1+cpu` and `0.8.3`. Repair: `pip install --force-reinstall --no-deps torch==2.7.1 --index-url https://download.pytorch.org/whl/cpu`, then `pip install --force-reinstall --no-deps tensordict==0.8.3`, then `pip check`. |
| `ModuleNotFoundError: No module named 'datdmpc'` | Editable install missing, or done in another environment | `conda activate datdmpc`, then `pip install -e . --no-deps` from the repository root. |
| A script prints "not implemented yet — see T0xx (owner Mx)" and exits with code 3 | Expected: the script is a T001 stub until its owner's task is merged | Use `--help` to see the binding interface; wait for the task in [STATUS](STATUS.md). |

**Fallback** (risk R8 in [PROJECT_PLAN](PROJECT_PLAN.md)): if MuJoCo / dm_control cannot be made to work
on a laptop by the task's target date, that member codes and runs the unit tests with the tiny model
where possible and runs everything else on Colab; log it as a blocker in the team page.

### 1.5 Checkpoints

Only the two released multitask checkpoints are used. Never download the mt30/mt80 training datasets.
Available from T005 (M1, target Sat 2026-10-24):

```powershell
python scripts/get_checkpoints.py --models mt30-5M mt30-19M
```

The script downloads from the Hugging Face URL pattern
`https://huggingface.co/nicklashansen/tdmpc2/resolve/main/multitask/<name>.pt` into the gitignored
`checkpoints/` folder (`--dest` to change it), checks sha256, and writes `checkpoints/MANIFEST.csv`
(`name,size_bytes,sha256,url`; the only committed file in `checkpoints/`). Re-check existing files with
`--verify-only`. Published values (Hugging Face API, `nicklashansen/tdmpc2`, folder `multitask/`,
retrieved 2026-10-21):

| File | Size (bytes) | sha256 | URL |
|---|---|---|---|
| `mt30-5M.pt` | 33,299,935 | `f3c6909e3282f115ce57b2ab29a88e654b4728d819d2c93a4ca079bad63b1455` | `https://huggingface.co/nicklashansen/tdmpc2/resolve/main/multitask/mt30-5M.pt` |
| `mt30-19M.pt` | 99,246,424 | `10773c9124ac23f157d46d33c29ab877322e29e63c2b0bf4bd3434a25b97ac86` | `https://huggingface.co/nicklashansen/tdmpc2/resolve/main/multitask/mt30-19M.pt` |

Independent PowerShell check (prints the hash; compare with the table; the comparison form prints `True`):

```powershell
Get-FileHash checkpoints\mt30-5M.pt -Algorithm SHA256
Get-FileHash checkpoints\mt30-19M.pt -Algorithm SHA256
(Get-FileHash checkpoints\mt30-5M.pt -Algorithm SHA256).Hash -eq "f3c6909e3282f115ce57b2ab29a88e654b4728d819d2c93a4ca079bad63b1455"
(Get-FileHash checkpoints\mt30-19M.pt -Algorithm SHA256).Hash -eq "10773c9124ac23f157d46d33c29ab877322e29e63c2b0bf4bd3434a25b97ac86"
```

**Shared Drive copy:** M1 uploads both verified files to the shared Google Drive folder
`DA-TDMPC2/checkpoints/` (T005). Colab sessions copy them from there; a laptop may also copy them from
Drive instead of downloading, but must then run `--verify-only` (or `Get-FileHash`).

Model facts that matter when loading (verified upstream, see [AGENTS §4.2](../AGENTS.md)): both
checkpoints use a **64-dimensional task embedding** (`dim(e) = 64` for mt30-5M/19M per upstream
`common/parser.py`; 96 only for mt80 and for the 1M/317M models), i.e. a 30 × 64 embedding table of which
C2 adapts one row; for mt30-19M `latent_dim` is overridden to 512 (`common/parser.py`).

### 1.6 Memory and laptop hygiene (12 GB RAM, 2-core CPU)

- **One evaluation process at a time** on a laptop. Do not run `pytest` and an evaluation in parallel.
- Close browser tabs, Teams/Zoom and other heavy applications during runs; check memory in Task Manager,
  or `Get-Process python | Select-Object Id, ProcessName, WS`.
- Use `mt30-5M.pt` for laptop debugging; `mt30-19M.pt` (primary) is the larger file (sizes above).
- Our code sets `torch.set_num_threads(4)`, `compile=False`, rendering off, no video; do not override them.
  No multiprocessing on laptops (`num_workers=0`).
- **For T0 CPU wall-time measurements** (the C2 cost claim): laptop plugged in, the same Windows power
  mode for every compared run, nothing else running, `--tier T0`. Note the power mode in your handoff
  entry; `env.txt` records the software versions, OS and CPU.
- Keep at least the checkpoint sizes plus some margin of free disk space on `C:`; `outputs/` and
  `logs/` grow and are never committed; delete old debug folders there when needed.

### 1.7 Workload split: Windows 11 laptop (Tier T0) vs. Google Colab (Tier T1)

To protect your laptop hardware (Lenovo IdeaPad 320, Intel Core i3, 12 GB RAM) from thermal throttling and out-of-memory crashes while ensuring maximum research velocity, tasks are strictly partitioned:

| Workload Category | Windows 11 Laptop (Tier T0: Core i3 CPU, 12 GB RAM) | Google Colab (Tier T1: Nvidia GPU, 12–15 GB VRAM) |
|---|---|---|
| **Development & Testing** | **All coding, debugging, tests:** `pytest`, git branch operations, stub implementations, linting, CLI `--help` checks. | None (do not develop interactively on Colab). |
| **Smoke & Sanity Runs** | **Tiny smoke test:** `python scripts/smoke_test.py --mode tiny` (< 30 seconds). Single-step MuJoCo physics checks. | None. |
| **Model Debugging** | **Single-episode debug runs** with `mt30-5M.pt` (`--episodes 1 --steps 50`) to verify tensor shapes and logging schemas. | Multi-episode verification and all `mt30-19M.pt` rollouts. |
| **C2 Embedding Adaptation** | **Local algorithm verification:** Adapting only the 64-number vector `e` for 1 episode / a few gradient steps (takes negligible CPU memory). | **Full C2 experimental sweeps** (multiple shift types × levels × seeds). |
| **C3 Shift Detection** | **Algorithm verification & calibration:** Testing EWMA/CUSUM on nominal seed traces. | Long evaluation rollouts with mid-episode shift injection. |
| **Baselines (B1/B2 Finetuning)**| **Strictly blocked:** Never run full/partial backprop on the 12 GB laptop (causes RAM thrashing / OOM). | **All B1 / B2 finetuning runs.** |
| **Long Sweeps (> 3 hrs)** | **Strictly blocked:** Any run estimated > 3 hours goes to Colab. | **All experimental sweeps,** sharded across M1/M2/M3 accounts (`--shard i/3`). |
| **Analysis & Figures** | **All report plotting & registry building:** `scripts/build_registry.py` and `scripts/make_figures.py` (reads lightweight CSVs). | None. |

---

## Step 2 — "Preprocessing": manifest and config verification

There is no dataset preprocessing in this project. "Preprocessing" means: verify the environment, the
checkpoints and the shift configuration before any run. Do this at the start of every session (the
start-of-session protocol in [AGENTS §3](../AGENTS.md) runs the smoke test).

### 2.1 Smoke test

Interface (binding, `scripts/smoke_test.py`, owner M1):
`[--mode {auto,tiny,full}] [--ckpt checkpoints/mt30-5M.pt] [--task walker-walk] [--steps 50] [--shift mass:1.5] [--seed 0]`.
Target: under 2 minutes on a laptop CPU. It must end with `[smoke] OK`.

| Mode | Available | What it does |
|---|---|---|
| `tiny` | **now** (T001); this is what CI runs | Random tiny multitask `WorldModel` on CPU + a real DMControl env; `--steps` nominal steps, then scales body masses by the `mass:<k>` factor, asserts the MuJoCo parameter changed, `--steps` more steps, prints sec/step. No checkpoint. Only `--shift mass:<k>` is accepted. |
| `full` | after **T006** (harness) **and T101** (wrappers) are merged | Loads the checkpoint through the T006 harness and runs a `--steps`-step nominal and a `--steps`-step perturbed rollout with MPPI. Fails (exit 1) if the checkpoint is missing or the harness is not implemented. |
| `auto` (default) | now | `full` if the checkpoint exists and the harness is implemented, otherwise `tiny` with a printed notice. |

```powershell
python scripts/smoke_test.py --mode tiny
python scripts/smoke_test.py
python scripts/smoke_test.py --mode full --ckpt checkpoints/mt30-5M.pt --task walker-walk --steps 50 --shift mass:1.5 --seed 0
```

The sec/step printed by the smoke test is for debugging only; budgets use T008 profiling
(`results/P0_profile/`), never smoke-test output.

### 2.2 Checkpoint manifest

After T005:

```powershell
python scripts/get_checkpoints.py --models mt30-5M mt30-19M --verify-only
```

Exit code 0 means both files match the sha256 values in [1.5](#15-checkpoints).

### 2.3 `configs/shifts.yaml`

Available after **T102** (M1, target Sat 2026-10-31), which defines shift types, levels and the dev vs
held-out test split. Syntax check (prints nothing on success, a YAML error otherwise):

```powershell
python -c "import yaml; yaml.safe_load(open('configs/shifts.yaml'))"
```

Semantic check: scripts that accept `--shifts-from configs/shifts.yaml --split {dev,test,all}` (first
`scripts/eval.py`, T006) must parse every entry against the shift SPEC grammar (type ∈ {`mass`,
`friction`, `actuator`, `gravity`, `obs_noise`, `action_delay`}, numeric level) and stop with an error
**before** running any episode if an entry is invalid. Requirement on T006/T102: a unit test covers this.
Never tune on `test` levels (see [PROJECT_PLAN](PROJECT_PLAN.md) evaluation protocol).

### 2.4 Other quick checks

```powershell
pytest -q
python scripts/eval.py --help
```

Every script prints its binding interface with `--help` from T001 on; stubs exit with code 3 until their
task is merged.

---

## Step 3 — Running

Rules (from [AGENTS §4.4](../AGENTS.md)): every run needs a task card with its budget
(`#tasks × #shifts × #seeds × #episodes × steps × sec/step = hours`, sec/step from T008); more than 3
laptop-hours → Colab (T1); every Colab run uses `--resume` and `--shard i/N`; MPPI settings are never
changed. A result counts only if produced on Colab (or reproduced there); laptop runs are for debugging,
except T0 CPU wall-time measurements.

### Results folder schema (binding)

Every run writes `results/<phase>_<exp>/<run_id>/` (or `outputs/...` for debugging) with:

| File | Content |
|---|---|
| `config.yaml` | all CLI arguments plus the resolved config |
| `episodes.csv` | one row appended and flushed per finished episode: `run_id,task,task_idx,shift_type,shift_level,method,seed,episode,return,length,wall_time_s,tier,shard,timestamp` |
| `summary.json` | at minimum `run_id, n_episodes, mean_return, ci95_low, ci95_high` (plus method-specific keys) |
| `env.txt` | python, torch, mujoco, dm_control, numpy versions; OS; CPU; device; tier (`T0`, `T1`, `T1b`) |
| `git_sha.txt` | the commit the run was made from (run from a committed state) |

- `run_id` = `<ckpt-stem>__<task>__<shift>__<method>__seed<seed>` with `:` replaced by `-`, e.g.
  `mt30-19M__walker-walk__mass-1.5__B0__seed0`.
- `--resume` skips episodes already present in `episodes.csv`; an interrupted episode is simply rerun.
- Seed ranges (a convention): evaluation/test 0–99; detector calibration 1000–1099; dev tuning 2000–2099.
- Result phase folders and owners: `P1_degradation`, `P2_adapt` (M2); `P0_profile`, `P3_detect` (M3);
  `P0_nominal`, `P1_ranking`, `P2_ranking_after_adapt`, `P3_closedloop` (M1). T301 raw signal dumps go
  to the gitignored `outputs/signals/`.

### 3(a) Laptop example commands per contribution (T0)

Debug runs write to the gitignored `outputs/debug/`. Values such as `<K>` come from the task card or
the design note; never invent them on the command line. Each command works only once its task is merged
(column "From").

| Contribution | From | Example (PowerShell, repository root, `datdmpc` active) |
|---|---|---|
| Frozen model B0, nominal | T006 | `python scripts/eval.py --ckpt checkpoints/mt30-5M.pt --task walker-walk --shift none --episodes 1 --seed 0 --out outputs/debug/ --resume` |
| Frozen model B0, shifted (P1) | T006 + T101 | `python scripts/eval.py --ckpt checkpoints/mt30-5M.pt --task walker-walk --shift mass:1.5 --episodes 1 --seed 0 --out outputs/debug/ --resume` |
| Profiling (P0, T0 wall-time is a reported quantity) | T008 | `python scripts/profile.py --ckpt checkpoints/mt30-5M.pt --task walker-walk --what all --steps <N> --device cpu --tier T0 --out results/P0_profile/` |
| Ranking-fidelity diagnostic (C1 core) | T104 | `python -m datdmpc.diagnostics.ranking_fidelity --ckpt checkpoints/mt30-5M.pt --task walker-walk --shift mass:1.5 --states <N> --candidates <M> --horizon <H> --seed 0 --out outputs/debug/` |
| Ranking fidelity after adaptation | T205 | same as above plus `--embedding <run folder>/adapted_embedding.json` |
| C2 `e`-only adaptation (Ours-C2) | T202 | `python scripts/adapt.py --ckpt checkpoints/mt30-5M.pt --task walker-walk --shift mass:1.5 --method e_only --K <K> --grad-steps <G> --lr <LR> --seed 0 --episodes 1 --out outputs/debug/ --resume` |
| Baselines B3 / B1 / B2 | T203 | same as C2 with `--method rand_e`, `--method full_ft` or `--method partial_ft` |
| G2 fallback (`e` + LayerNorm affine) | T201/T204, only if G2 fails | same as C2 with `--method e_ln` |
| C3 signals | T301 | `python scripts/detect.py signals --ckpt checkpoints/mt30-5M.pt --task walker-walk --shift mass:1.5 --episodes 1 --seed 2000 --out outputs/signals/` |
| C3 calibration (nominal seeds) | T302 | `python scripts/detect.py calibrate --ckpt checkpoints/mt30-5M.pt --task walker-walk --seeds 1000 --episodes 1 --out outputs/debug/` |
| C3 detection with mid-episode injection | T303 | `python scripts/detect.py evaluate --ckpt checkpoints/mt30-5M.pt --task walker-walk --shift mass:1.5 --inject-at <STEP> --detector-config configs/experiments/M3_detector.yaml --seeds 0 --out outputs/debug/ --resume` |
| Closed loop detect → adapt | T304 | `python -m datdmpc.closed_loop --ckpt checkpoints/mt30-5M.pt --task walker-walk --shift mass:1.5 --inject-at <STEP> --detector-config configs/experiments/M3_detector.yaml --adapt-config configs/experiments/M2_adapt.yaml --seeds 0 --episodes 1 --out outputs/debug/ --resume` |
| C1 ranking loss (stretch) | T401 decision | no script yet; an interface is defined only if G2 passes by Tue 2026-11-17 and the pilot is approved |

`mass:1.5` above is the smoke-test default used as an example, not a chosen level; real levels come from
`configs/shifts.yaml` (T102) via `--shifts-from configs/shifts.yaml --split dev` or `--split test`. For
`detect.py` the subcommand comes first, then its flags.

### 3(b) Colab template (T1)

Notebooks live in `notebooks/colab/<owner>_<exp>.ipynb` (`M1_`, `M2_`, `M3_` prefix; each member edits
only their own). They are **launchers only**: all logic is in `src/` and `scripts/`. Every cell below is a
separate notebook cell, run top to bottom. After a disconnect, start a new runtime and run all cells
again: `--resume` skips finished episodes.

**Cell 1 — parameters (the only cell you edit per sweep)**

```python
COMMIT = "<full commit SHA on main used by this sweep>"   # identical on all three accounts
SHARD = "1/3"            # M1: "1/3", M2: "2/3", M3: "3/3"
PHASE = "<phase folder from the task card, e.g. P0_nominal>"
DEVICE = "cuda"          # "cuda" on a GPU runtime, "cpu" on a CPU runtime
DRIVE = "/content/drive/MyDrive/DA-TDMPC2"
REPO_URL = "https://github.com/Shahrcasm/tdmpc2-shift-adaptation.git"
```

**Cell 2 — mount Drive**

```python
from google.colab import drive
drive.mount("/content/drive")
```

The shared folder `DA-TDMPC2` must appear at `/content/drive/MyDrive/DA-TDMPC2`. M2 and M3, who receive it
as a shared folder, add it to their own Drive with "Add shortcut to Drive" (placed in My Drive).
<!-- VERIFY: that a shortcut to the shared DA-TDMPC2 folder appears under /content/drive/MyDrive/ in Colab and is writable from the M2 and M3 accounts; first checked in T005 (Colab --verify-only cell) and T007 -->

**Cell 3 — clone the repository at the sweep commit**

While the repository is private, cloning needs a GitHub token with read access to this repository, typed
at run time and never stored in the notebook, in Drive or in the repository.
<!-- VERIFY: which GitHub token type works for a collaborator on a private personal repository (fine-grained token with this repository selected, or a classic token with repo scope) and that this clone cell works on Colab; first checked in T005 -->

```python
import getpass, subprocess
token = getpass.getpass("GitHub token (read access; not stored): ")
auth_url = REPO_URL.replace("https://", "https://" + token + "@")
r = subprocess.run(["git", "clone", "-q", auth_url, "/content/tdmpc2-shift-adaptation"], capture_output=True)
print("clone exit code:", r.returncode)   # output is not printed so the token never appears
subprocess.run(["git", "-C", "/content/tdmpc2-shift-adaptation", "remote", "set-url", "origin", REPO_URL])
del token, auth_url
```

Once the repository is public, `!git clone {REPO_URL} /content/tdmpc2-shift-adaptation` suffices.

**Cell 4 — check out the commit**

```python
%cd /content/tdmpc2-shift-adaptation
!git checkout -q {COMMIT}
!git rev-parse HEAD
```

**Cell 5 — torch**

```python
!python --version
!pip show torch
!pip install -q torch==2.7.1
!python -c "import torch; print(torch.__version__, torch.cuda.is_available())"
```

<!-- VERIFY: Colab's Python version and preinstalled torch at run time (python --version; pip show torch) match environment/requirements-colab.txt, and torch==2.7.1 from PyPI sees the GPU on a Colab GPU runtime; record in the handoff entry (T007) -->

**Cell 6 — requirements and our package**

```python
!pip install -q -r environment/requirements-colab.txt
!pip install -q -e . --no-deps
```

`requirements-colab.txt` keeps the laptop pins for mujoco, dm-control, gymnasium, tensordict, hydra-core,
omegaconf and termcolor; it uses `numpy==1.26.4` (numpy 1.24.4 has no wheel for Python 3.12; 1.26.4 has
wheels for 3.11 and 3.12), leaves `pandas` unpinned and has no `pytest`; torch is installed in Cell 5. If
pip cannot find a wheel for any pin on Colab's Python version: stop, record the problem in your handoff
log and ask M1 before changing any pin.
<!-- VERIFY: mujoco 3.1.2 / tensordict 0.8.3 wheel availability for Colab's Python version (cp312/cp313) on PyPI; checked at the first Colab run in T007 --> pip may warn about conflicts with packages preinstalled on Colab; only a
failing import of our dependencies is a problem. All runs below start new `python` processes, so the
freshly installed versions are used.

**Cell 7 — checkpoints from Drive**

```python
!mkdir -p checkpoints
!cp {DRIVE}/checkpoints/mt30-5M.pt {DRIVE}/checkpoints/mt30-19M.pt checkpoints/
!python scripts/get_checkpoints.py --models mt30-5M mt30-19M --verify-only
```

**Cell 8 — rendering (normally not run)**

```python
import os
# Only on a GPU runtime AND only for a run that renders video. Evaluation never renders: leave commented.
# os.environ["MUJOCO_GL"] = "egl"
```

**Cell 9 — smoke test**

```python
!python scripts/smoke_test.py
```

**Cell 10 — the run (command from the task card; example: T007 nominal sweep)**

```python
!python scripts/eval.py --ckpt checkpoints/mt30-19M.pt --task all --shift none --episodes 10 --seeds 0 1 2 --out {DRIVE}/results/{PHASE}/ --resume --shard {SHARD} --tier T1 --device {DEVICE}
```

The output path is always `/content/drive/MyDrive/DA-TDMPC2/results/<phase>/`, so every finished episode is
on Drive immediately. Use `--tier T1` on Colab (device and versions go to `env.txt` automatically).

**Free-tier limits.** Colab free sessions have a maximum length, disconnect when idle, and a GPU is not
guaranteed. <!-- VERIFY current Colab limits: maximum session length, idle timeout and GPU availability of the free tier at the time of the first sweep; record what you observe (not numbers from memory) in the T007 / T008 handoff entries --> Do **not** use
keep-alive scripts, auto-clickers or similar tricks: they violate the intended use and are unnecessary
because every run is resume-safe. If no GPU is available, run the same shard on a CPU runtime with
`DEVICE = "cpu"`, or wait; switch to Kaggle (3(d)) only if Colab GPU is unavailable for more than one day.

**Copying finished results back into the repository (laptop).** Only the owner of the result folder
(ownership table in [AGENTS](../AGENTS.md); e.g. `P1_degradation` belongs to M2 even when M1 and M3 ran
shards) copies and commits it, on their own branch:

1. In the browser, open Google Drive → `DA-TDMPC2/results/<phase>/`, select the finished `<run_id>`
   folders (a folder is finished when `summary.json` exists and `episodes.csv` has the planned number of
   rows) and choose **Download** (Drive creates a zip).
2. Extract into the repository:

   ```powershell
   cd C:\code\tdmpc2-shift-adaptation
   git checkout dev_<name>
   Expand-Archive -Path "$HOME\Downloads\<zip file name>.zip" -DestinationPath results\<phase>\
   ```

   Check the layout is `results\<phase>\<run_id>\` with the five files; if the zip added an extra top-level
   folder, move the `<run_id>` folders up one level.
3. Check sizes (must print nothing; no file over 5 MB is committed):

   ```powershell
   Get-ChildItem results\<phase> -Recurse -File | Where-Object { $_.Length -gt 5MB }
   ```

4. Commit only the result folders, by path, and push:

   ```powershell
   git add results/<phase>/<run_id>
   git status --short
   git commit -m "T<ID>: add <phase> results (shards 1/3, 2/3, 3/3)"
   git push origin dev_<name>
   ```

Never edit a result file by hand and never overwrite an existing run folder in `results/`.

### 3(c) Sharding a sweep across the M1/M2/M3 accounts and the compute ledger

1. **Plan (owner of the task):** in the task card, write the budget formula with T008's sec/step for the
   tier, the exact command, the commit SHA, and `N = 3`. Add one row per shard to the compute log of your
   team page with the estimated hours.
2. **Run:** each member runs the same notebook with the same `COMMIT` and command, changing only
   `SHARD`: M1 `1/3`, M2 `2/3`, M3 `3/3`, each on their own Colab account. `--shard i/N` (1-based) splits
   the job list deterministically, so the three shards never write the same run folder. Keep `N` fixed for
   the whole sweep, and never run the same shard in two sessions at the same time.
3. **Interrupted or unavailable account:** rerun the same shard later with `--resume`, or another member
   takes it over (same `SHARD` value) after the original session has stopped; note the change in both
   members' compute logs.
4. **Record hours:** each member who ran a shard adds a row to the **Compute log of their own team page**
   (date, task, run family, tier, Colab account = own slot, shard, estimated hours, actual hours). Actual
   hours = sum of `wall_time_s` over the shard's episodes divided by 3600, e.g. after the results are on
   the laptop:

   ```powershell
   (Get-ChildItem results\<phase> -Recurse -Filter episodes.csv | ForEach-Object { Import-Csv $_.FullName } | Where-Object { $_.shard -eq "<i>/3" } | Measure-Object -Property wall_time_s -Sum).Sum / 3600
   ```

   This excludes install and setup time; note large overheads in the Notes column.
5. **Ledger:** M1 copies the team-page rows into the compute ledger of [STATUS §5](STATUS.md) at the next
   merge-time sync. Members never edit STATUS.md.

### 3(d) Kaggle backup recipe (T1b, short)

Use only if Colab GPU is unavailable for more than one day; record `--tier T1b`.
<!-- VERIFY: Kaggle specifics before first use (whoever first needs T1b): accelerator options and weekly GPU quota, phone verification required for internet access, dataset mount path under /kaggle/input/, writable output folder /kaggle/working/, maximum session length, and how to download outputs -->

1. Create a Kaggle notebook; in its settings enable a GPU accelerator and internet access.
2. Upload `mt30-5M.pt` and `mt30-19M.pt` once as a **private** Kaggle dataset and attach it to the
   notebook; copy them into `checkpoints/` and run `get_checkpoints.py --verify-only` as in Cell 7.
3. Clone and install exactly as in Cells 3–6 (clone into `/kaggle/working/tdmpc2-shift-adaptation`).
4. Run the same command as on Colab with the same `COMMIT` and the shard you are covering, `--tier T1b`,
   and `--out /kaggle/working/results/<phase>/`.
5. Kaggle has no Drive mount: before the session ends, download the finished run folders and copy them
   into the shared Drive folder `DA-TDMPC2/results/<phase>/`, so a later Colab `--resume` sees them and
   the owner can commit them as in 3(b).

---

## Step 4 — Commit vs ignore

**Commit:**

- code (`src/`, `scripts/`, `tests/`), configs (`configs/shifts.yaml`, `configs/experiments/<owner>_*.yaml`),
  Colab launcher notebooks (without large outputs);
- per run: `config.yaml`, `episodes.csv`, `summary.json`, `env.txt`, `git_sha.txt` (and small
  method-specific files such as `adapted_embedding.json`);
- `results/REGISTRY.csv` and `figures/` (PNG/PDF, each under 2 MB) — generated, committed by M1 only;
- design notes, docs, team pages, report sources;
- reference PDFs in `docs/references/` (small);
- `checkpoints/MANIFEST.csv` (the only file under `checkpoints/`).

**Never commit:** `checkpoints/` contents and any `*.pt` / `*.pth` / `*.ckpt`, datasets, `outputs/`,
`logs/`, `videos/`, `wandb/`, `.env`, `*.ipynb_checkpoints`, Hugging Face / Google / GitHub tokens, Drive
paths containing personal e-mail addresses, and **any file larger than 5 MB**. Git cannot ignore by size:
check the byte size of every file your branch changes before every PR (prints nothing = OK; `git diff
--stat` counts lines, not bytes, so it cannot check this):

```powershell
git fetch origin
git diff --name-only --diff-filter=d origin/main... | ForEach-Object { $size = (Get-Item -LiteralPath $_).Length; if ($size -gt 5MB) { "$_  $size bytes" } }
```

The authoritative file is `.gitignore` at the repository root (owner M1). Its content at T001:

```gitignore
# --- Large / private artifacts (never commit) ---
checkpoints/*
!checkpoints/MANIFEST.csv
*.pt
*.pth
*.ckpt
*.npz
outputs/
logs/
videos/
wandb/
*.mp4
*.gif
.env
.env.*

# --- Python ---
__pycache__/
*.py[cod]
*.egg-info/
.eggs/
build/
dist/
.venv/
venv/
.pytest_cache/
.mypy_cache/
.ruff_cache/

# --- Notebooks ---
.ipynb_checkpoints/
*.ipynb_checkpoints

# --- Hydra (if upstream entry points are ever run locally; outputs/ is ignored above) ---
multirun/

# --- LaTeX build files ---
report/**/*.aux
report/**/*.log
report/**/*.out
report/**/*.bbl
report/**/*.blg
report/**/*.synctex.gz
report/**/*.fdb_latexmk
report/**/*.fls

# --- OS / editor ---
.DS_Store
Thumbs.db
desktop.ini
.idea/
.vscode/

# Files larger than 5 MB must not be committed; git cannot enforce size by pattern,
# so the integrator checks the byte size of every changed file at merge time (AGENTS.md §7).
```

If this block and the file ever differ, the file wins; M1 updates this block in the same PR.

---

## Step 5 — Regenerate report numbers and clean-clone check (T503)

### 5.1 Regenerate registry and figures

Available after T501 (M1, target Tue 2026-11-10). Both scripts read `results/` only (never Drive, never
`outputs/`). Run by M1 after merging new results; others may run it locally but do not commit the output
(`results/REGISTRY.csv` and `figures/` are M1-only):

```powershell
python scripts/build_registry.py; if ($?) { python scripts/make_figures.py }
```

Defaults: `build_registry.py --results results --out results/REGISTRY.csv` (reads
`results/*/*/summary.json` and `config.yaml`); `make_figures.py --registry results/REGISTRY.csv --out figures`
(PNG + PDF, each under 2 MB). Every number in the report is copied from these outputs or from a cited
`results/` file.

### 5.2 Clean-clone reproducibility procedure (T503, all members, by Sun 2026-12-06)

Goal: show that one committed result per contribution can be regenerated from the repository alone:
C2 (`results/P2_adapt/`), C3 (`results/P3_detect/`), and the ranking-fidelity diagnostic
(`results/P1_ranking/`). Each member reproduces a result produced by someone else; M1 coordinates.

**Acceptance criterion** (fixed here before the first reproduction run): for return-based runs, the
reproduced `mean_return` lies inside the original run's `[ci95_low, ci95_high]` from its `summary.json`.
For runs whose headline metric is not return (ranking fidelity, detection), the same rule applies to
that metric's 95% CI if the original `summary.json` reports one; otherwise the criterion is
`[[pre-register before run]]` and is written here before reproducing. Exact equality is not expected
(GPU non-determinism, different hardware).

1. **Fresh clone into a new folder and a new environment** (laptop, PowerShell):

   ```powershell
   git clone https://github.com/Shahrcasm/tdmpc2-shift-adaptation.git C:\code\tdmpc2-repro
   cd C:\code\tdmpc2-repro
   git checkout <SHA from the original run's git_sha.txt>
   conda create -n datdmpc-repro python=3.11 -y
   conda activate datdmpc-repro
   pip install torch==2.7.1 --index-url https://download.pytorch.org/whl/cpu
   pip install -r environment/requirements-cpu.txt
   pip install -e . --no-deps
   python scripts/get_checkpoints.py --models mt30-5M mt30-19M
   pytest -q
   python scripts/smoke_test.py
   ```

   This checks that the documented install and the checkpoint download still work from scratch. Using a
   separate environment keeps the editable install of the main clone untouched.
2. **Rerun one run per contribution** on the **tier of the original run** (`env.txt`): reconstruct the
   command from the original `config.yaml` (same script, checkpoint, task, shift, method, seed(s) and the
   same `--episodes` value), changing only `--out`:
   - laptop (T0): `--out outputs/repro/<phase>/`;
   - Colab (T1): the template in 3(b) with `COMMIT` = the original `git_sha.txt`, a new runtime, and
     `--out /content/drive/MyDrive/DA-TDMPC2/repro/<phase>/`.

   Nothing under `results/` is overwritten.
3. **Compare** the original `results/<phase>/<run_id>/summary.json` with the reproduced
   `summary.json` against the acceptance criterion; also check `env.txt` for version differences.
4. **Record:** each member writes the comparison (both `summary.json` paths, pass/fail, explanation of
   any mismatch) in their team-page handoff log; M1 records the outcome and evidence paths for T503 in
   [STATUS](STATUS.md) at the next sync. A failed reproduction is either explained and fixed, or reported
   honestly in the report.
5. **Clean up** (optional): `conda env remove -n datdmpc-repro` and delete `C:\code\tdmpc2-repro`.
