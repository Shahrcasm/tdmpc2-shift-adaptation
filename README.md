# DA-TDMPC2 — Detect-and-Adapt TD-MPC2

**Question.** Dynamics shift after training (body mass, friction, actuator strength) can silently corrupt how a pretrained multitask TD-MPC2 world model ranks candidate actions. We ask whether **a 64-number task-embedding update** can repair this: every network weight stays frozen, only the current task's embedding row `e` is adapted from K recent transitions with the world model's own losses (latent consistency, reward, value), and the update is triggered automatically when the model's own prediction errors signal a shift. We compare this against no adaptation and full/partial finetuning on return, samples, CPU wall-time and parameters updated, using the released `mt30-5M` and `mt30-19M` (primary) checkpoints on perturbed DMControl tasks. No model is trained from scratch. (`dim(e) = 64` for mt30-5M/19M per upstream `third_party/tdmpc2/tdmpc2/common/parser.py`; 96 only for mt80 and for the 1M/317M models. The paper lists 96 for all sizes, but the code decides the shape of the released mt30 checkpoints.)

**Course.** CSE 465 — Pattern Recognition and Neural Network. Faculty: Dr. Mohammad Ashrafuzzaman Khan. The final report is written in research-paper format.

## Team

| Slot | Name | Student ID | Role |
|---|---|---|---|
| M1 | Md. Shahriar Rakib Rabbi | 2321937642 | Integrator (merges every PR, including his own) · infra · evaluation harness · perturbation suite · nominal evaluation · ranking-fidelity diagnostic · closed loop · C1 design (stretch) · figures · report assembly |
| M2 | Md. Ishtiak Ahmed Moyen | 2131580642 | C2 embedding adaptation · baselines · degradation sweep · related work |
| M3 | Md. Abdullah Talha | 2222614642 | Profiling · C3 detection |

## Contributions (ordered by feasibility)

- **C2 — Embedding-only test-time adaptation (core).** Freeze all weights and adapt only `e`, using the world model's own losses. Baselines: B0 frozen, B1 full finetune, B2 partial finetune (reward + Q heads), B3 random-`e` initialisation plus adaptation.
- **C3 — Automatic shift detection (core-light).** Latent consistency error, reward prediction error and Q-ensemble disagreement, calibrated on nominal episodes, used online to trigger C2.
- **C1 — Better action comparison (stretch).** A ranking-fidelity diagnostic that compares the model's ranking of candidate actions with ground truth obtained by saving and restoring simulator state. A ranking loss is trained only if gate G2 passes by 2026-11-17.

The proposal in `docs/references/` lists these three in the order C1, C2, C3 and already marks detection as optional. This README orders them by feasibility.

**Status.** For the current week, gates and task board, see [docs/STATUS.md](docs/STATUS.md). M1 syncs that file at merge time. Key dates: start 2026-10-21 · experiment freeze 2026-12-02 · final submission 2026-12-14.

## Repository map

```
AGENTS.md  CLAUDE.md  README.md  LICENSE  pyproject.toml  .gitignore  .gitattributes
.github/                 PR + issue templates, workflows/ci.yml (pytest + tiny smoke test, Windows + Linux)
environment/             requirements-cpu.txt (laptops, CI) · requirements-colab.txt
third_party/tdmpc2/      vendored upstream at a pinned commit; READ-ONLY
src/datdmpc/             our package: _upstream.py (bridge), envs/, eval/, adapt/, detect/,
                         diagnostics/, ranking/, closed_loop.py
configs/                 shifts.yaml · experiments/<owner>_*.yaml
scripts/                 get_checkpoints · smoke_test · eval · profile · adapt · detect ·
                         build_registry · make_figures
notebooks/colab/         <owner>_*.ipynb launchers only (logic lives in src/)
tests/                   test_<module>.py, one per owned module
results/                 <phase>_<exp>/<run_id>/ run folders · REGISTRY.csv (generated)
figures/                 generated from results/ only
report/                  main.tex · sections/<section>_<owner>.tex
docs/                    STATUS · PROJECT_PLAN · RUNS · RELATED_WORK · REPO_SETUP · design/ · team/ · references/
checkpoints/ outputs/ logs/ videos/ wandb/   gitignored (except checkpoints/MANIFEST.csv)
```

File ownership is binding. See the ownership table in [AGENTS.md](AGENTS.md). Every member, M1 included, works only on their own `dev_*` branch and never pushes to `main`. Changes reach `main` through pull requests that only M1 merges (merge workflow in [AGENTS.md](AGENTS.md); the T001 commit and branch-creation sequence in [docs/REPO_SETUP.md](docs/REPO_SETUP.md)).

## Quickstart (Windows laptop, PowerShell)

Prerequisites: Git for Windows and Python 3.11 (native or Miniconda). Clone to the short path below, not inside OneDrive, Documents or Desktop. Windows PowerShell 5.1 does not support `&&`, so run one command per line.

```powershell
git config --global core.longpaths true
git clone https://github.com/Shahrcasm/tdmpc2-shift-adaptation.git C:\code\tdmpc2-shift-adaptation
cd C:\code\tdmpc2-shift-adaptation
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install torch==2.7.1 --index-url https://download.pytorch.org/whl/cpu
pip install -r environment/requirements-cpu.txt
pip install -e . --no-deps
python scripts/smoke_test.py --mode tiny
```

Tiny mode does not need a checkpoint. It builds a small randomly initialised multitask world model on CPU, runs 50 nominal steps and 50 steps with scaled body masses in a real DMControl environment, checks that the parameter changed, and prints sec/step. Rendering is off on laptops and in CI (`MUJOCO_GL=disable`, set automatically by `src/datdmpc/_upstream.py`). Never set `MUJOCO_GL=egl` on Windows. Use `egl` only on a Colab GPU runtime when you want videos. Run the test suite with `pytest -q`. Checkpoints come from `python scripts/get_checkpoints.py --models mt30-5M mt30-19M` once T005 is merged. Troubleshooting is covered in [docs/RUNS.md](docs/RUNS.md).

**Colab.** All reported results come from Colab (Linux), or must be reproduced there. For the notebook template, Drive layout, sharding (`--shard i/N`) and resume (`--resume`), see [docs/RUNS.md](docs/RUNS.md).

## Documentation

| Document | Purpose |
|---|---|
| [AGENTS.md](AGENTS.md) | Rules for humans and AI agents: ownership, session protocols, merge checklist |
| [docs/STATUS.md](docs/STATUS.md) | Task board, gates, compute ledger, handoff log (M1 only) |
| [docs/PROJECT_PLAN.md](docs/PROJECT_PLAN.md) | Research questions, hypotheses, evaluation protocol, metrics, roadmap, risks |
| [docs/RUNS.md](docs/RUNS.md) | Environment setup, smoke test, laptop and Colab runs, what to commit |
| [docs/REPO_SETUP.md](docs/REPO_SETUP.md) | GitHub settings checklist, the T001 commit and branch-creation sequence (single source), merge settings and branch protection |
| [docs/RELATED_WORK.md](docs/RELATED_WORK.md) | Novelty guardrails and differentiation (T009) |
| [docs/design/C2_embedding_adaptation.md](docs/design/C2_embedding_adaptation.md) | C2 design note (M2, T201) |
| [docs/design/C3_detection.md](docs/design/C3_detection.md) | C3 design note (M3, T302) |
| [docs/design/C1_ranking.md](docs/design/C1_ranking.md) | C1 design note (M1, T401) |
| [docs/team/M1_Shahriar.md](docs/team/M1_Shahriar.md) · [M2_Ishtiak.md](docs/team/M2_Ishtiak.md) · [M3_Talha.md](docs/team/M3_Talha.md) | Per-member tasks, task cards, handoff log, faculty updates |
| [docs/references/](docs/references/) | TD-MPC2 paper and project proposal PDFs |

## Reproducibility

Every run writes one folder `results/<phase>_<exp>/<run_id>/` containing `config.yaml` (all CLI arguments and the resolved config), `episodes.csv` (one row per finished episode, flushed immediately, so `--resume` can skip finished episodes), `summary.json` (at minimum `run_id, n_episodes, mean_return, ci95_low, ci95_high`), `env.txt` (Python, torch, MuJoCo, dm_control and numpy versions; OS; CPU; device; tier) and `git_sha.txt`. `run_id` is `<ckpt-stem>__<task>__<shift>__<method>__seed<seed>` with `:` replaced by `-`, for example `mt30-19M__walker-walk__mass-1.5__B0__seed0`. `results/REGISTRY.csv` and `figures/` are generated from these folders by `scripts/build_registry.py` and `scripts/make_figures.py`.

**Numbers only from `results/`.** No number may appear in docs, the report or faculty updates unless it is copied from a file in `results/` and cited by its path.

## Upstream attribution

`third_party/tdmpc2/` is a vendored, unmodified copy of [nicklashansen/tdmpc2](https://github.com/nicklashansen/tdmpc2) at commit `e9f59321933cbc8e11a002b842adc7d4ffae8ff1`, released under the MIT License (copyright Nicklas Hansen). The included and excluded files and the re-vendoring procedure are listed in [third_party/tdmpc2/UPSTREAM_COMMIT.txt](third_party/tdmpc2/UPSTREAM_COMMIT.txt). The folder is read-only. Our code extends upstream by subclassing or wrapping from `src/datdmpc/`. Two upstream limits explain why we need our own harness (T006). First, the upstream entry points `evaluate.py` and `train.py` assert CUDA. Second, upstream does not support single-task evaluation of multitask checkpoints. Pretrained checkpoints come from Hugging Face `nicklashansen/tdmpc2`.

## Citation

If you use this repository, cite TD-MPC2. The following entries are copied from `third_party/tdmpc2/README.md`, which also asks users to cite the original TD-MPC paper:

```bibtex
@inproceedings{hansen2024tdmpc2,
  title={TD-MPC2: Scalable, Robust World Models for Continuous Control},
  author={Nicklas Hansen and Hao Su and Xiaolong Wang},
  booktitle={International Conference on Learning Representations (ICLR)},
  year={2024}
}

@inproceedings{hansen2022tdmpc,
  title={Temporal Difference Learning for Model Predictive Control},
  author={Nicklas Hansen and Xiaolong Wang and Hao Su},
  booktitle={International Conference on Machine Learning (ICML)},
  year={2022}
}
```

## License

Our code is released under the MIT License (see [LICENSE](LICENSE)). The vendored upstream code keeps its own MIT License (see [third_party/tdmpc2/LICENSE](third_party/tdmpc2/LICENSE)).
