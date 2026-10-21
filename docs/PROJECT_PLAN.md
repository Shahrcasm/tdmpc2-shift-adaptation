# PROJECT PLAN — DA-TDMPC2 (Detect-and-Adapt TD-MPC2)

Scientific and technical specification for the CSE 465 (Pattern Recognition and Neural Network) research
project. Owner: M1 (integrator). Created in T001 on 2026-10-21.

- Rules of engagement: [AGENTS.md](../AGENTS.md) · task board and gate status: [STATUS.md](STATUS.md) ·
  how to run: [RUNS.md](RUNS.md) · related work: [RELATED_WORK.md](RELATED_WORK.md) · repository
  settings: [REPO_SETUP.md](REPO_SETUP.md).
- Design notes: [C1_ranking.md](design/C1_ranking.md) (M1) ·
  [C2_embedding_adaptation.md](design/C2_embedding_adaptation.md) (M2) ·
  [C3_detection.md](design/C3_detection.md) (M3).
- Reference PDFs (TD-MPC2 paper, our proposal): [`docs/references/`](references/).

**How this file is used.** Hypotheses and thresholds are written here **before** the corresponding runs
(stop rule, Section 10.4). Thresholds marked `[[...]]` are proposed by the named owner in their own
design note and copied into this file by M1 before the deadline in Section 7.3 (procedure in Section
7.3); once a run has started, a filled threshold is never edited (a change is recorded as a new dated
line, with the reason, and both are reported). This file contains no experimental result. Every number
is a date, a task ID, a configuration value or count cited to its upstream file (Section 4), or a
placeholder.

**Citation conventions.** "(Hansen et al., 2024, §x)" refers to the TD-MPC2 paper (arXiv:2310.16828,
ICLR 2024) in `docs/references/`. Upstream file paths are relative to `third_party/tdmpc2/` (vendored at
commit `e9f59321933cbc8e11a002b842adc7d4ffae8ff1`). Claims about other papers carry
`<!-- VERIFY citation -->` until a team member has read the paper (T009, owner M2).

---

## 1. Problem statement

TD-MPC2 (Hansen et al., 2024) is a decoder-free latent world model for continuous control. A single
multitask model is trained on a fixed set of tasks and then used, frozen, to plan with MPPI. Its released
mt30 checkpoints (trained on 30 DMControl tasks) are evaluated in the nominal simulator only. In
deployment, the physical system often differs from the training system: a heavier body, a slipperier
floor, a weaker actuator, noisy sensors, delayed actions. Such a **post-training dynamics shift** changes
the true transition function while the world model, its reward and value predictions, and therefore the
planner's ranking of candidate actions stay as they were.

We study three questions on a laptop-CPU compute budget, without training any model from scratch:

1. **Measurement.** How much does a frozen TD-MPC2 model degrade under controlled dynamics shifts, and
   does the degradation show up as a loss of *ranking fidelity* (the model ordering candidate actions
   differently from the real simulator)?
2. **Adaptation (C2).** Can the model be repaired at test time by updating only its task embedding `e`
   (64 numbers for our checkpoints, Section 2), using a small number K of transitions from the shifted
   system and the world model's own training losses?
3. **Detection (C3).** Can the model's own prediction errors detect that a shift has happened, online,
   with few false alarms, so that adaptation is triggered automatically?

Hard constraints: no training from scratch; no change of MPPI settings in reported results; laptops are
native Windows, CPU-only; all reported results are produced (or reproduced) on Google Colab (Linux),
except T0 CPU wall-time measurements, which are the point of the C2 cost claim.

---

## 2. Unifying story

> *Dynamics shift silently corrupts how a TD-MPC2 world model ranks candidate actions. A 64-number task
> embedding update, triggered automatically by the model's own prediction errors, restores much of the
> lost performance at a fraction of the cost of finetuning — on a laptop CPU.*

"Restores much of" and "a fraction of" are the claims under test; they become quantitative only through
the pre-registered thresholds of H2 and H4 (Section 7). The story is reported as stated only if G2 (and,
for "triggered automatically", G3) pass; otherwise the report states which part failed.

**Embedding dimension (correction of the original prompt and repo description).** Our checkpoints use a
64-dimensional task embedding: dim(e) = 64 for mt30-5M/19M per upstream `tdmpc2/common/parser.py`
(`cfg.task_dim = 96 if cfg.task == 'mt80' or cfg.get('model_size', 5) in {1, 317} else 64`); it is 96 only for mt80
and for the 1M/317M models. The paper's hyperparameter table lists 96 for all model sizes, but the
upstream code carries an explicit comment ("Account for slight inconsistency in task_dim for the mt30
experiments") that makes 64 authoritative for the released mt30-5M and mt30-19M checkpoints. The whole
embedding table therefore has 30 rows × 64 = 1,920 parameters, and C2 adapts **one row = 64 numbers**.
The "~96-parameter" wording in the GitHub repo description is to be changed to "64-number" (checklist
item in [REPO_SETUP.md](REPO_SETUP.md)); T006 asserts `model._task_emb.weight.shape == (30, 64)` after
loading.

---

## 3. Contributions and methods

### 3.1 Contributions (ordered by feasibility)

| ID | Name | Status in plan | Owner | Core question |
|---|---|---|---|---|
| **C2** | Lightweight test-time adaptation | **CORE** | M2 | Freeze every network weight; adapt only the task-embedding row `e` of the current task from K recent transitions using the world model's own losses (latent consistency + reward + value). Compare with no adaptation and full/partial finetuning on return, samples, T0 CPU wall-time and parameters updated. |
| **C3** | Automatic shift detection | **CORE-LIGHT** | M3 | Monitor latent consistency error, reward prediction error and Q-ensemble disagreement; calibrate on nominal episodes; detect shifts online; trigger C2 automatically. |
| **C1** | Better action comparison | **STRETCH** (expected to remain a diagnostic + design note) | M1 | Ranking-fidelity diagnostic: save/restore the simulator state, roll out M candidate actions in the real simulator, compare their true short-horizon returns with the model's predicted returns (Kendall τ, top-1 agreement). A ranking-loss pilot is trained only if G2 passes by 2026-11-17. |

Shift types (C2/C3): body mass, friction, actuator strength, gravity (positive cases); observation noise
and action delay (expected-negative cases, H3). Concrete levels and the dev/test split are fixed in
T102 (`configs/shifts.yaml`); none are given here.

**Ordering relative to the proposal.** The project proposal (`docs/references/`) lists the
contributions as (1) action comparison/ranking, (2) embedding-only adaptation, (3) shift detection, with
(3) marked "(optional)". This plan reorders them by feasibility (C2 core, C3 core-light, C1 stretch).
The reordering is consistent with the proposal: detection was already optional there, and C1 keeps its
diagnostic part (T104, T205, T401) in every scope.

### 3.2 Methods evaluated

| Label | Method | What is updated | Tool and method flag (binding interface from T001; `--help` on each script) |
|---|---|---|---|
| **B0** | Frozen TD-MPC2 on the shifted env | nothing | `scripts/eval.py` (method label always `B0`) |
| **B1** | Full finetune | all world-model parameters | `scripts/adapt.py --method full_ft` |
| **B2** | Partial finetune | reward head + Q heads | `scripts/adapt.py --method partial_ft` |
| **B3** | Random-`e` init + adaptation (ablation) | the task's embedding row, re-initialised randomly before adaptation | `scripts/adapt.py --method rand_e` |
| **Ours-C2** | `e`-only adaptation | the task's embedding row (64 numbers) | `scripts/adapt.py --method e_only` |
| **Ours-C2+C3** | Detection-triggered `e`-only adaptation | as Ours-C2, started by the C3 detector | `python -m datdmpc.closed_loop` (T304) |
| **Ceiling** | Frozen model on the nominal env | nothing | `scripts/eval.py --shift none` |
| *(G2 fallback)* | `e` + LayerNorm affine parameters | embedding row + LayerNorm scale/shift | `scripts/adapt.py --method e_ln` (used only if G2 fails; which LayerNorms are included is fixed in T201) |

B3 tests whether the pretrained embedding matters as an initialisation; it is motivated by the paper's
few-shot finetuning, which initialises `e` from a semantically similar task (Hansen et al., 2024, App. E,
Table 7). All adaptation methods receive the identical set of K transitions (Section 8).

---

## 4. Background facts the method relies on

Every statement below is either from the TD-MPC2 paper (section cited) or was read in the vendored
upstream code at the pinned commit (file cited). Paths are relative to `third_party/tdmpc2/`.

### 4.1 Components and conditioning

- Five learned components, every one conditioned on the task embedding `e` (Hansen et al., 2024, §3.1,
  Eq. 2): encoder `h`, latent dynamics `d`, reward `R`, terminal value ensemble `Q`, policy prior `p`.
- Upstream API (`tdmpc2/common/world_model.py`): `encode(obs, task)` = h, `next(z, a, task)` = d,
  `reward(z, a, task)` = R (logits over 101 bins), `pi(z, task)` = p,
  `Q(z, a, task, return_type={'min','avg','all'}, target=False, detach=False)`. `return_type='all'`
  returns the logits of every ensemble member; scalar values per member come from
  `common/math.two_hot_inv` (needed for Q-ensemble disagreement, C3). Per the method's docstring,
  `'avg'` is the average of two randomly subsampled Q-values.
- Conditioning mechanism: `WorldModel.task_emb(x, task)` looks up the embedding row and **concatenates**
  it to the component input (`common/world_model.py`); the encoder's first layer takes
  `obs_dim + task_dim` inputs (`common/layers.py`, `enc`).
- Multitask models zero-pad observations and mask actions to the maximum dimension over the 30 tasks
  (`common/world_model.py` `_action_masks`; `envs/wrappers/multitask.py`).
- Latent representation: SimNorm activation with `simnorm_dim: 8` (`common/layers.py` `SimNorm`;
  `tdmpc2/config.yaml`).
- Value and reward are predicted as distributions over `num_bins: 101` bins spanning `vmin: -10` to
  `vmax: +10` **in symlog space** (`tdmpc2/config.yaml`; `common/math.py` `two_hot` applies `symlog`
  before binning and `two_hot_inv` applies `symexp`), trained with soft cross-entropy on two-hot targets.
- Model sizes (`common/__init__.py` MODEL_SIZE + `common/parser.py`): size 5 → enc_dim 256, mlp_dim
  512, latent_dim 512, 2 encoder layers; size 19 → enc_dim 1024, mlp_dim 1024, 3 encoder layers, and
  latent_dim 512 for mt30 (`parser.py` overrides the size-19 default: "This checkpoint is slightly
  smaller"). `num_q` = 5 for both.

### 4.2 Task embedding

- `self._task_emb = nn.Embedding(len(cfg.tasks), cfg.task_dim, max_norm=1)` (`common/world_model.py`),
  i.e. ℓ2-norm ≤ 1 (Hansen et al., 2024, §3.3). PyTorch enforces `max_norm` at lookup by renormalising
  the looked-up row **in place** on the weight. Consequence for C2 (to be handled in the T201 design
  note): an optimiser step can push the row outside the unit ball, and the next lookup projects it back,
  so `e`-only adaptation is effectively projected gradient descent on the unit ball unless T201 chooses
  otherwise.
- dim(e) = 64 for mt30-5M and mt30-19M (`common/parser.py`; Section 2). Embedding table: 30 × 64.
- mt30 task index order (`common/__init__.py` TASK_SET['mt30']), index 0..29: walker-stand,
  walker-walk, walker-run, cheetah-run, reacher-easy, reacher-hard, acrobot-swingup, pendulum-swingup,
  cartpole-balance, cartpole-balance-sparse, cartpole-swingup, cartpole-swingup-sparse, cup-catch,
  finger-spin, finger-turn-easy, finger-turn-hard, fish-swim, hopper-stand, hopper-hop,
  walker-walk-backwards, walker-run-backwards, cheetah-run-backwards, cheetah-run-front,
  cheetah-run-back, cheetah-jump, hopper-hop-backwards, reacher-three-easy, reacher-three-hard,
  cup-spin, pendulum-spin.
- **Motivation for C2.** The paper's t-SNE of learned embeddings reports that "embedding similarity
  appears to align more closely with task dynamics (embodiment, objects) than objective" (Hansen et al.,
  2024, §4.1, Fig. 7). If `e` encodes dynamics, moving `e` is a natural, low-dimensional way to absorb a
  dynamics change while keeping all network weights frozen.

### 4.3 Training losses reused by C2 (and monitored by C3)

The model objective (Hansen et al., 2024, §3.1, Eq. 3) as implemented in `tdmpc2/tdmpc2.py` `_update`,
over a horizon H with temporal weight ρ^t:

```
total_loss = consistency_coef * [ sum_t rho^t * MSE( d(z_t, a_t, e), h(s_{t+1}, e) ) ] / H
           + reward_coef      * [ sum_t rho^t * CE( R_hat_t, r_t ) ] / H
           + value_coef       * [ sum_t rho^t * CE( Q_hat_t, TD_target_t ) ] / (H * num_q)
```

Coefficients (`tdmpc2/config.yaml`): `consistency_coef: 20`, `reward_coef: 0.1`, `value_coef: 0.1`,
`rho: 0.5`; optimiser defaults `lr: 3e-4`, `enc_lr_scale: 0.3`, `grad_clip_norm: 20`. The code also has
a termination term (`termination_coef: 1`) that is active only when `episodic` is true; `episodic:
false` in `tdmpc2/config.yaml`, so it is zero for DMControl. Whether C2 keeps these coefficients, and how
the TD target is formed at test time, is decided in T201.

### 4.4 Planning (MPPI) — never changed in reported results

From `tdmpc2/config.yaml`: `mpc: true`, `iterations: 6`, `num_samples: 512`, `num_elites: 64`,
`num_pi_trajs: 24`, `horizon: 3`, `min_std: 0.05`, `max_std: 2`, `temperature: 0.5`.
`tdmpc2/tdmpc2.py` adds 2 iterations when `action_dim >= 20`; in the multitask model `action_dim` is the
padded maximum over the 30 tasks <!-- VERIFY: padded mt30 action_dim and hence whether the +2 iterations apply; T006 prints cfg.action_dim and cfg.iterations after loading -->.
Trajectory value (`_estimate_value`): discounted sum of predicted rewards over the horizon plus the
discounted `Q(z_H, pi(z_H), return_type='avg')`. On laptops we set `compile=False` and disable video;
these do not change planning.

### 4.5 Environment and episode

- `tdmpc2/envs/dmcontrol.py`: `suite.load(domain, task, task_kwargs={'random': cfg.seed})`, actions
  rescaled to [-1, 1], `DMControlWrapper.step` applies each action **twice (action repeat 2)** and sums
  the reward, `Timeout(max_episode_steps=500)` ⇒ **one episode = 500 agent decisions = 1000 simulator
  steps** (consistent with Hansen et al., 2024, Table 6). DMControl rewards lie in [0, 1] per simulator
  step, so an episode return lies in [0, 1000] by construction.
- The raw dm_control env is `DMControlWrapper.env`, exposing `.physics` (`physics.model.body_mass`,
  `physics.model.geom_friction`, `physics.model.actuator_gear`, `physics.model.opt.gravity`,
  `physics.get_state()` / `set_state()`), which the perturbation wrappers (T101) and the
  ranking-fidelity save/restore (T104) use.
- `tdmpc2/evaluate.py` reports the multitask normalized score for DMControl as `ep_reward / 10`.
- Known limitation (upstream README): single-task evaluation of multitask checkpoints is not
  supported; our harness (T006) builds the 30-task model, loads the checkpoint and plans with a fixed
  `task_idx` on a single padded env.

### 4.6 Related signal in the paper

The paper describes a test-time regulariser using Q-ensemble standard deviation, attributed to Feng et
al. (2023) (Hansen et al., 2024, App. J, Eq. 9). This is the closest in-paper precedent for the C3
Q-disagreement signal.

---

## 5. CSE 465 concept mapping

| Course concept | Where it appears in the project | Contribution / task | Report section owner |
|---|---|---|---|
| Representation learning | Decoder-free latent `z = h(s, e)` with SimNorm activation, trained by latent consistency instead of reconstruction | Background; C3 signal (consistency error) | M1 (method), M3 (C3) |
| Embeddings as learned conditioning vectors | Task embedding `e` concatenated to every component input; ℓ2-norm ≤ 1 | C2 adapts exactly this vector | M2 |
| Parameter-efficient adaptation | Updating 64 of all model parameters vs full / partial finetuning; parameter count reported per method | C2, B1–B3 (T202–T204) | M2 |
| Distribution shift | Post-training dynamics shift (mass, friction, actuator, gravity) vs observation-side shift (noise, delay) | H1, H3; T103 | M2 |
| Ensembles for uncertainty | 5-member Q ensemble; disagreement as epistemic-uncertainty proxy | C3 signal (T301) | M3 |
| Anomaly / novelty detection, ROC analysis | Detector calibrated on nominal data only; AUROC, detection delay, false-alarm rate; EWMA/CUSUM thresholding | C3 (T301–T303), H4 | M3 |
| Classification as regression surrogate | Reward and value predicted as 101-bin distributions with two-hot targets and soft cross-entropy | Background; C2 loss terms | M1 |
| Learning to rank / rank correlation | Kendall τ and top-1 agreement between model-predicted and true candidate returns | C1 diagnostic (T104, T205), H5 | M1 |
| Statistical evaluation | Bootstrap confidence intervals, IQM with stratified bootstrap, disjoint calibration/test seeds, pre-registration | All results (T501) | M1 |

---

## 6. Related-work differentiation

The authoritative summaries are written by M2 in [RELATED_WORK.md](RELATED_WORK.md) (T009, target
2026-10-27). Until then, every cell describing another paper is a working assumption taken from the
bootstrap prompt and is marked for verification. Cells reading "T009" are left for M2 to fill after
reading the paper; nobody fills them from memory.

| Method | What it adapts / learns | Signals used | Cost | How we differ |
|---|---|---|---|---|
| TD-M(PC)² (Lin et al., arXiv:2502.03550; L4DC 2026) <!-- VERIFY citation --> | Policy-constraint modification of TD-MPC2 training to fix value overestimation <!-- VERIFY citation --> | T009 | Requires (re)training <!-- VERIFY citation --> | We do not change training; we adapt a frozen model at test time under dynamics shift. Relevant to C1 only as a training-time fix to how actions are valued. |
| BMPC — Bootstrapped MPC (Wang et al., ICLR 2025) <!-- VERIFY citation --> | Policy prior trained to imitate the MPC planner <!-- VERIFY citation --> | T009 | Requires (re)training <!-- VERIFY citation --> | No retraining; no change to the policy prior; C1 measures ranking fidelity against the real simulator rather than imitating the planner. |
| TD-GRPC (arXiv:2505.13549) <!-- VERIFY citation --> | Group-relative ranking of candidate trajectories <!-- VERIFY citation --> | T009 | T009 | **Closest to C1.** Our C1 core is a diagnostic using simulator save/restore ground truth under shift; any ranking-loss pilot (H5, stretch) must be differentiated in T401. |
| JEPA-TTT (arXiv:2610.00722) <!-- VERIFY citation --> | Test-time training of a latent world model under dynamics shift <!-- VERIFY citation --> | Latent prediction error <!-- VERIFY citation --> | T009 | **Closest to C2.** We update only `e` (64 numbers) of a multitask TD-MPC2 model, use reward and value losses in addition to latent consistency, trigger adaptation by detection (C3), and report T0 CPU cost. |
| AdaJEPA <!-- VERIFY citation: full reference and identifier not yet known --> | Test-time adaptation of a latent (JEPA-style) world model under dynamics shift <!-- VERIFY citation --> | T009 | T009 | Same differentiation as JEPA-TTT. |
| RMA — Rapid Motor Adaptation (Kumar et al., 2021) <!-- VERIFY citation --> | An adaptation module that infers environment factors from recent state-action history <!-- VERIFY citation --> | Recent history <!-- VERIFY citation --> | Trained in simulation with privileged information before deployment <!-- VERIFY citation --> | No adaptation module is trained in advance; we optimise the existing embedding with the world model's own losses, and only after a detected shift. |
| World Models as Reference Trajectories for Rapid Motor Adaptation (arXiv:2505.15589) <!-- VERIFY citation --> | T009 | T009 | T009 | T009 (M2 writes the differentiation after reading; expected axis: what is adapted and whether a world model is updated or only used as a reference). |
| Feng et al., 2023 — Finetuning Offline World Models in the Real World <!-- VERIFY citation --> | Finetuning of an offline-pretrained world model online <!-- VERIFY citation --> | Uncertainty (Q-ensemble std) as a test-time regulariser (as described in Hansen et al., 2024, App. J, Eq. 9) | T009 | We use ensemble disagreement as a **detection** signal (C3), not as a planning regulariser, and adapt only `e`. |

Each design note (C1, C2, C3) repeats the differentiation for its closest neighbours.

---

## 7. Research questions, hypotheses and pre-registration

### 7.1 Research questions

- **RQ1 (measurement).** How do controlled dynamics shifts affect the return and the ranking fidelity
  of a frozen TD-MPC2 multitask model?
- **RQ2 (C2).** How much of the shift-induced gap does `e`-only adaptation recover, at what sample and
  CPU cost, compared with full and partial finetuning?
- **RQ3 (limits).** Which shift types does `e`-only adaptation *not* correct?
- **RQ4 (C3).** Can the model's own prediction errors detect a shift online, with bounded delay and
  false-alarm rate?
- **RQ5 (C1, stretch).** Does a ranking auxiliary loss improve ranking fidelity without hurting return?

### 7.2 Hypotheses (thresholds are placeholders until pre-registered)

- **H1:** Mass/friction/actuator shifts degrade frozen TD-MPC2 return monotonically with severity and
  degrade ranking fidelity.
- **H2:** `e`-only adaptation with K ≤ `[[K_max]]` transitions recovers ≥ `[[X]]`% of the
  nominal–shifted gap at ≤ `[[Y]]`% of full-finetune wall-time, on held-out levels.
- **H3:** Observation noise and action delay are poorly corrected by `e`-only adaptation (expected
  negative result, defines the method's limits).
- **H4:** Consistency error and Q-ensemble disagreement detect shifts with AUROC ≥ `[[A]]`, false
  alarms ≤ `[[F]]` per 1,000 nominal steps, delay ≤ `[[D]]` steps.
- **H5 (stretch):** a ranking auxiliary loss raises Kendall τ without lowering return at matched
  steps/seeds.

### 7.3 Pre-registration table

A threshold is pre-registered when it is on `main` in this file before the first run that tests it.
Procedure (respects strict file ownership): the owner writes the proposed value and its justification in
their own design note (C2: T201; C3: T302; C1: T401) or, for H1, on their team page, and opens the PR.
After merging that PR, M1 copies the value into the table below in a commit on `dev_shahriar` (it may
share the `T000: sync status` PR), which M1 merges once CI is green. **A run whose threshold
is not in this file on `main` must not start**; the integrator rejects PRs that contain such runs.

| Hypothesis | Quantity to fix | Placeholder | Who fixes it | Deadline (before the corresponding run) |
|---|---|---|---|---|
| H1 | Severity ordering test for "monotonic" (return and Kendall τ); what counts as a "clear drop" beyond the G1 criterion | `[[pre-register before run]]` | M2 (return, T103) · M1 (ranking fidelity, T104) | Before the first T103 / T104 run (T102 target 2026-10-31 fixes the levels) |
| H2 | Maximum number of transitions | `[[K_max]]` | M2 (T201) | T201, 2026-11-05 |
| H2 | Minimum gap recovery (%) | `[[X]]` | M2 (T201) | T201, 2026-11-05 |
| H2 | Maximum wall-time relative to B1 (%) | `[[Y]]` | M2 (T201) | T201, 2026-11-05 |
| H2 | Budget-matching rule (Section 8) | `[[pre-register before run]]` | M2 (T201) | T201, 2026-11-05 |
| H3 | Definition of "poorly corrected" (gap-recovery bound for noise and delay) | `[[pre-register before run]]` | M2 (T201) | T201, 2026-11-05 |
| H4 | Minimum AUROC | `[[A]]` | M3 (T302) | T302, 2026-11-13 |
| H4 | Maximum false alarms per 1,000 nominal steps | `[[F]]` | M3 (T302) | T302, 2026-11-13 |
| H4 | Maximum detection delay (agent steps) | `[[D]]` | M3 (T302) | T302, 2026-11-13 |
| H5 | Minimum Kendall τ gain and return non-inferiority margin | `[[pre-register before run]]` | M1 (T401) | T401, before any pilot run (T402/T403 only if G2 passed by 2026-11-17) |

---

## 8. Evaluation protocol

- **Study tasks.** 4–6 study tasks chosen by the T007 rule. The rule is written into T007's task card
  and committed **before** any shifted result is looked at; the candidate pool is the 30 mt30 tasks
  (Section 4.2).
- **Checkpoints.** `mt30-5M.pt` for fast iteration; **`mt30-19M.pt` is primary** for reported results.
- **Shift levels.** Split in `configs/shifts.yaml` (T102) into **dev** levels (used for tuning learning
  rate, gradient steps, K, detector thresholds) and **held-out test** levels (reported only, never used
  for tuning). Scripts select them with `--shifts-from configs/shifts.yaml --split {dev,test,all}`.
- **Seeds (convention fixed in T001, not a result).** Evaluation/test seeds 0–99; detector calibration seeds 1000–1099;
  dev-tuning seeds 2000–2099 — disjoint by construction. Calibration seeds are therefore never test
  seeds.
- **Replication.** ≥3 adaptation seeds × ≥10 evaluation episodes per (task, shift, method).
- **Statistics.** Per task: mean ± 95% bootstrap CI over episodes and seeds. Across tasks: interquartile
  mean (IQM) with stratified bootstrap CIs (e.g. `rliable`) <!-- VERIFY: rliable is not in environment/requirements-*.txt; T501 either adds it through an M1 PR (check its install on Python 3.11 / Windows) or implements IQM and stratified bootstrap with numpy/scipy -->.
  Number of bootstrap resamples and CI method: `[[pre-register before run]]` (fixed in T501, before the
  first figure is generated).
- **Identical data.** Every adaptation method (B1, B2, B3, Ours-C2, G2 fallback `e_ln`) sees the identical K
  transitions for a given (task, shift level, seed). How these transitions are collected (behaviour
  policy, online vs batch) is fixed in T201.
- **Budget matching.** The primary comparison **matches gradient steps** across adaptation methods
  **and reports wall-time** (T0 CPU) for every method; the final choice is confirmed in T201:
  `[[pre-register before run]]`. Wall-time comparisons (H2's `[[Y]]`) use measurements from the **same
  tier and device** for B1 and Ours-C2 (via `scripts/profile.py --what adapt` on T0, T008) — never a
  laptop time against a Colab time.
- **Evaluation after adaptation.** The adapted model is evaluated with unchanged MPPI settings on the
  same shift level for ≥10 episodes; the adapted embedding is saved as `adapted_embedding.json` in the
  run folder.
- **Ceiling and floor.** Ceiling = frozen model on the nominal env (`--shift none`); floor = B0 on the
  shifted env. Gap recovery is computed between them (Section 9).
- **Where results count.** A reported number is produced on Colab (T1) or reproduced there; laptop runs
  are for debugging, except T0 CPU wall-time measurements. Detector calibration that feeds a reported
  result follows the same rule.
- **Example commands** (PowerShell, from `C:\code\tdmpc2-shift-adaptation`; `walker-walk` is an example
  task, study tasks come from T007; levels are examples until T102):

```powershell
python scripts/eval.py --ckpt checkpoints/mt30-19M.pt --task walker-walk --shift none --episodes 10 --seeds 0 1 2 --out results/P1_degradation/ --resume
python scripts/eval.py --ckpt checkpoints/mt30-19M.pt --task walker-walk --shifts-from configs/shifts.yaml --split test --episodes 10 --seeds 0 1 2 --out results/P1_degradation/ --resume
python scripts/adapt.py --ckpt checkpoints/mt30-19M.pt --task walker-walk --shift mass:1.5 --method e_only --K <K> --grad-steps <steps> --lr <lr> --seeds 0 1 2 --episodes 10 --out results/P2_adapt/ --resume
```

Result folders follow the T001 results schema (see [RUNS.md](RUNS.md)): `results/<phase>_<exp>/<run_id>/{config.yaml, episodes.csv,
summary.json, env.txt, git_sha.txt}` with `run_id = <ckpt-stem>__<task>__<shift>__<method>__seed<seed>`
(`:` replaced by `-`).

---

## 9. Metrics

Notation: `R_nominal` = mean return of the frozen model on the nominal env (ceiling); `R_shift` = mean
return of B0 on the shifted env; `R_adapt` = mean return after adaptation on the same shifted env. All
means are over the episodes and seeds of one (task, shift level, method) cell.

| Metric | Definition (plain formula) | Source / tool |
|---|---|---|
| Episode return | sum over the 500 agent decisions of the per-decision reward (each the sum of 2 simulator-step rewards); range [0, 1000] | `episodes.csv` column `return` |
| Normalized score | return / 10 (per upstream `tdmpc2/evaluate.py`); range [0, 100] | derived in T501 |
| Retention | R_shift / R_nominal | T103 |
| Gap recovery | (R_adapt − R_shift) / (R_nominal − R_shift); undefined and reported as such when R_nominal − R_shift is not significantly positive (95% CIs overlap) | T204 |
| Samples to 80% | smallest number of shifted-env transitions K in the pre-registered K grid at which gap recovery ≥ 0.8; "not reached" if none | T204 |
| Adaptation wall-time (T0 CPU) | wall-clock seconds from the start of the first gradient step to the adapted parameters being ready, single process, `torch.set_num_threads(4)`, laptop CPU; data-collection time reported separately | T008 (`--what adapt`), T204 |
| Parameters updated | number of scalar parameters receiving gradient updates. Ours-C2 (`e_only`) = 64 (one embedding row, `common/parser.py`); B3 (`rand_e`) = the same row; B1, B2 and the G2 fallback (`e_ln`) are counted from the loaded model in T203 (`sum(p.numel())` over the updated parameters), never written by hand | T202 test, T203 |
| Latent consistency error | mean over transitions of MSE( d(z_t, a_t, e), h(s_{t+1}, e) ), i.e. squared ℓ2 distance divided by latent dimension, matching the `F.mse_loss` convention in `tdmpc2/tdmpc2.py` `_update` | T301 |
| Kendall τ | for M candidates at one state: (concordant pairs − discordant pairs) / (M·(M−1)/2) between model-predicted and true short-horizon returns (tau-b when ties occur); averaged over states | T104, T205 |
| Top-1 agreement | fraction of evaluated states where the candidate with the highest model-predicted return is also the one with the highest true return | T104, T205 |
| AUROC | area under the ROC curve of the detection score separating nominal from shifted windows (window definition fixed in T302) | T303 |
| Detection delay | (first alarm step at or after the injection step) − (injection step), in agent steps; episodes with no alarm after injection are counted as missed detections and reported separately | T303 |
| False alarms per 1,000 nominal steps | 1000 × (number of alarms raised on nominal episodes or before injection) / (number of nominal agent steps monitored) | T303 |
| Planning time per step | wall-clock seconds per agent decision (one `act` call including MPPI), reported per tier and device | T008 |

Q-ensemble disagreement (C3 signal, not a reported outcome metric): standard deviation across the
`num_q` members of `two_hot_inv` applied to `Q(z, a, task, return_type='all')`; the action used is fixed
in T301.

---

## 10. Roadmap, gates and scope

### 10.1 Calendar-fixed roadmap

| Week | Dates | Phase | Tasks (owner) | Deliverable | Gate (decided by all 3 on the last day) |
|---|---|---|---|---|---|
| 1 | Oct 21 – Oct 27 | P0 Setup & reproduction | T001 (M1), T002 (M1), T003 (M2), T004 (M3), T005 (M1), T006 (M1), T008 (M3), T009 (M2); T007 starts (M1) | Miniconda env on all three Windows laptops; repo; checkpoints; single-task harness; profiling; nominal scores started on Colab | **G0 (Tue Oct 27)** |
| 2 | Oct 28 – Nov 3 | P1 Shift benchmark | T007 (M1, Oct 30), T101 (M1, Oct 29), T102 (M1, Oct 31), T103 (M2, Nov 3), T104 (M1, Nov 3) | Wrappers; study-task selection; degradation curves; ranking-fidelity diagnostic | **G1 (Tue Nov 3)** |
| 3–4 | Nov 4 – Nov 17 | P2 C2 adaptation | T201 (M2, Nov 5), T202 (M2, Nov 8), T203 (M2, Nov 11), T204 (M2, Nov 17); T501 (M1, Nov 10), T502 (M1, Nov 12) | `e`-only adaptation + baselines on held-out shift levels; registry/figure scripts; report skeleton | **G2 (Tue Nov 17)** |
| 4–5 | Nov 11 – Nov 24 (parallel, M3) | P3 C3 detection | T301 (M3, Nov 8), T302 (M3, Nov 13), T303 (M3, Nov 24) | Signals, calibration, mid-episode injection, AUROC/delay/FAR | **G3 (Tue Nov 24)** |
| 6 | Nov 25 – Dec 2 | Integration | T205 (M1, Nov 27), T304 (M1, Dec 1), T401 (M1, Dec 2) | Closed-loop detect→adapt; ranking fidelity after adaptation; all figures regenerated; C1 design note | **Experiment freeze (Wed Dec 2)**; G4 (stretch) decided at freeze |
| 7–8 | Dec 3 – Dec 14 | Writing | T503 (all, Dec 6), T504 (all, Dec 14) | Full draft Tue Dec 8 → faculty feedback → final Sun Dec 13 → submit Mon Dec 14 | Clean-clone reproducibility check passed |

Writing starts in week 4 (method and setup sections from Nov 11; M2/M3 write their own
`report/sections/*_<owner>.tex`). Nothing except writing (T504) and the reproducibility check (T503) is
scheduled after Dec 2.

### 10.2 Gates

| Gate | Date | Pass criterion | Evidence | If failed → fallback |
|---|---|---|---|---|
| G0 | Tue 2026-10-27 | Harness evaluates one mt30 task (single task of the multitask checkpoint); sec/step known on laptop **and** Colab | T006 PR; `results/P0_profile/<run_id>/summary.json` | Fix the harness before any sweep; if Colab is unavailable, record laptop sec/step and repeat on Colab at the first opportunity; P1 sweeps do not start until sec/step on the sweep tier is known |
| G1 | Tue 2026-11-03 | ≥3 shift types give clear drops (non-overlapping 95% CIs) on ≥3 study tasks | `results/P1_degradation/<run_id>/summary.json` | Raise severity (new levels in `configs/shifts.yaml`, T102) and re-run the affected cells; report the shift types that never produce a drop as such |
| G2 | Tue 2026-11-17 | Pre-registered H2 threshold met on mass and friction, held-out levels | `results/P2_adapt/<run_id>/summary.json` | Adapt `e` + LayerNorm affine parameters (G2 fallback, Section 3.2); report the `e`-only result honestly; C1 pilot (G4) is cancelled |
| G3 | Tue 2026-11-24 | Pre-registered H4 targets met on ≥2 shift types | `results/P3_detect/<run_id>/summary.json` | Present C3 as an analysis (no detection claim); T304 closed loop runs with the detector as-is and is reported as exploratory |
| G4 (stretch) | Wed 2026-12-02 | H5 pilot (T402/T403) result available; runs only if G2 passed by 2026-11-17 | pilot folder defined in T401 | C1 remains the diagnostic + design note (T104, T205, T401) |

On every decision M1 tags the merge commit (`g0` … `g4`) and records status and evidence in
[STATUS.md](STATUS.md).

### 10.3 Scope levels

- **Minimum deliverable (guaranteed):** P0 + P1 + P2 + ranking-fidelity diagnostic (T001–T009,
  T101–T104, T201–T204, T501–T504).
- **Full scope:** minimum + P3 (T301–T303) + closed loop (T304) + ranking fidelity after adaptation
  (T205).
- **Stretch:** C1 ranking-loss pilot (T402/T403, H5) only if G2 passed on time; otherwise C1 = T104 +
  T205 + T401 design note.

### 10.4 Stop rules

1. No new ideas after Nov 24 (G3). New ideas before that date enter as an issue and a task card, never
   as an unplanned run.
2. No experiment without a task card (goal, budget formula, commands, Done-when) on the owner's team page.
3. Hypotheses and thresholds are written into this file before the corresponding runs (Section 7.3).
4. Writing starts in week 4 (method + setup sections), not in week 7.
5. MPPI settings are never changed in reported results.
6. Experiment freeze Wed Dec 2: after it, no new runs except re-running an already registered
   configuration for T503.

---

## 11. Compute plan

### 11.1 Tiers

| Tier | Where | What runs there |
|---|---|---|
| T0 — Laptop | Native Windows, Miniconda env `datdmpc`, PowerShell 5.1; repo at `C:\code\tdmpc2-shift-adaptation` (outside OneDrive/Documents/Desktop); CPU `torch`; `torch.set_num_threads(4)`; rendering off; one evaluation process at a time | Coding, tests, smoke tests, wrappers, single-episode checks, `e`-only adaptation, detector development, plots; T0 CPU wall-time measurements (the C2 cost claim) |
| T1 — Colab free | Three members' accounts in parallel (`--shard 1/3`, `2/3`, `3/3`); checkpoints from shared Drive `DA-TDMPC2/checkpoints/`; GPU runtime when available, CPU otherwise; results to `/content/drive/MyDrive/DA-TDMPC2/results/` with `--resume` | Evaluation sweeps (sharded), B1/B2 finetuning baselines, any C1 pilot; every reported result |
| T1b — Kaggle (backup) | Only if Colab GPU is unavailable for more than 1 day | Same as T1 |

Upstream `train.py`/`evaluate.py` and the upstream agent require CUDA (Section 12); every tier runs
through our harness, which builds the model on the device given by `--device {cpu,cuda}`.

### 11.2 Budget formula (symbols only)

Every task card computes its budget with these formulas **before** running. `sec_per_decision` and
`sec_per_grad_step` come only from T008 (`results/P0_profile/`) for the tier and device actually used;
no other source and no assumed value is allowed.

```
eval_hours  = n_tasks × n_shifts × n_methods × n_seeds × n_episodes × 500 decisions × sec_per_decision / 3600
adapt_hours = n_tasks × n_shifts × n_adapt_methods × n_seeds × n_grad_steps × sec_per_grad_step / 3600
total_hours = eval_hours + adapt_hours
```

- 500 decisions per episode follows from `max_episode_steps=500` with action repeat 2
  (`tdmpc2/envs/dmcontrol.py`).
- `n_methods = 1` for a pure B0 sweep (T103); for T204 `eval_hours` counts the post-adaptation
  evaluation of each method.
- Ranking fidelity (T104/T205): `n_states × n_candidates × (simulator rollout of horizon H + model
  prediction) × sec_per_unit / 3600`, with the unit costs measured in T008 or T104's first run.
- Detection (T302/T303): the `eval_hours` formula with the calibration seeds (calibration) or test seeds
  (evaluation) plus signal extraction cost per decision from T008.

**Tier rule.** If `total_hours` on T0 exceeds 3 laptop-hours, the run goes to Colab (T1) and is split
with `--shard i/3` across the three accounts. Each sharded sweep is recorded in the compute ledger in
[STATUS.md](STATUS.md) (run family, tier, Colab account M1/M2/M3, estimated hours, actual hours). Every
Colab run is resume-safe (one CSV row per finished episode, flushed immediately; `--resume` skips
finished rows); no keep-alive tricks.

---

## 12. Risk register

Likelihood and impact are qualitative judgements (Low / Med / High) made at T001 and revisited at every
gate.

| # | Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|---|
| R1 | Harness mismatch with upstream (our single-task evaluation of a multitask checkpoint does not reproduce upstream behaviour: padding, action masks, task index, discount) | Med | High | T006 builds the full 30-task model, asserts `_task_emb.weight.shape == (30, 64)`, uses the TASK_SET index order, and compares nominal scores against the paper's reported mt30 scores where available <!-- VERIFY: which per-task mt30 nominal scores the paper or upstream publish for comparison; checked in T007 -->; G0 blocks sweeps until fixed | M1 |
| R2 | Upstream agent hard-codes CUDA: `TDMPC2` uses `torch.device('cuda:0')` (`tdmpc2/tdmpc2.py`, device and multitask discount tensor); `common/scale.py` and `common/buffer.py` also hard-code `cuda:0`; `evaluate.py`/`train.py` assert CUDA | High (confirmed) | High | Harness constructs the model and planner on a configurable device by subclassing/wrapping (e.g. a CPU-capable agent class in `src/datdmpc/eval/harness.py`, `compile=False`); never edit `third_party/`; `WorldModel` itself has no device hard-coding; tests run on CPU in CI | M1 |
| R3 | Colab GPU unavailable or session disconnects | High | Med | Resume-safe logging (`--resume`), sharding across three accounts, CPU runtime fallback, Kaggle backup after more than 1 day without GPU; budgets re-estimated with the sec/step of the tier actually used | M1 (infra), each run owner |
| R4 | `e` too low-capacity to absorb dynamics shift | Med | High | H2 pre-registered; dev levels used to tune lr/steps/K before held-out runs; G2 fallback (`e` + LayerNorm affine); negative result reported honestly with parameter counts | M2 |
| R5 | Embedding is 64-dimensional, not 96 as assumed in the original plan (lower capacity than assumed) | High (confirmed) | Med | All docs and the report state 64 with the `common/parser.py` citation; repo description corrected (REPO_SETUP.md); R4 mitigation applies; the paper/code discrepancy is stated in one sentence in the report | M1 (docs), M2 (C2) |
| R6 | Detector false alarms (nominal variability triggers adaptation) | Med | Med | Calibrate on nominal seeds 1000–1099 only; EWMA/CUSUM smoothing; H4 bounds `[[F]]`; G3 fallback = present C3 as analysis | M3 |
| R7 | C1 overlaps TD-GRPC | High | Med | C1 kept as diagnostic + design note unless G2 passes; T401 writes the differentiation vs TD-GRPC/BMPC/TD-M(PC)² after T009 | M1 |
| R8 | Windows-only install failures for MuJoCo/dm_control or upstream Linux assumptions | Med | High | Pinned cp311 wheels (`environment/requirements-cpu.txt`); troubleshooting table in [RUNS.md](RUNS.md); CI on `windows-latest` and `ubuntu-latest`; fallback: that member codes locally (tests with the tiny model) and runs everything on Colab | Each member for own laptop; M1 for CI |
| R9 | 12 GB RAM pressure on laptops (mt30-19M + MPPI + browser) | Med | Med | One evaluation process at a time; close browser tabs during runs; `num_workers=0`; mt30-5M for development; memory-heavy runs (B1) on Colab | Each member |
| R10 | Embedding norm constraint interacts with optimisation (`max_norm=1` renormalises the row in place at lookup) | Med | Med | T201 specifies the projection/constraint explicitly; T202 test checks that only `e` changes and that its norm stays ≤ 1 | M2 |
| R11 | Unverified related-work claims leak into the report | Med | High | Every claim marked `<!-- VERIFY citation -->` until T009; integrator merge checklist rejects unmarked citations | M2 (T009), M1 (review) |
| R12 | A member falls behind | Med | High | **Reassignment rule:** a task that is not started (no commit referencing its ID) 2 days after all its dependencies are Done is discussed at the next gate meeting and may be reassigned by majority vote (2 of 3); the reassigned task keeps its ID, the new owner is recorded in STATUS.md and both team pages, and file ownership for that task's paths transfers through a PR to the ownership table in [AGENTS.md §2](../AGENTS.md). Minimum deliverable tasks take priority over full-scope and stretch tasks | All three; M1 records |

---

## 13. File ownership

The binding file ownership table, the T001 scaffolding note and the result-folder assignments live only
in [AGENTS.md §2](../AGENTS.md). They are not repeated here, so there is one place to update.

Changes to this file go through M1 (pre-registered thresholds: procedure in Section 7.3).
