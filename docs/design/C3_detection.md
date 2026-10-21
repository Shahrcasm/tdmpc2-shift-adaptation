# C3 — Automatic shift detection (design note)

| Field | Value |
|---|---|
| Owner | M3 — Md. Abdullah Talha |
| Task | [T302](../team/M3_Talha.md#t302) — detector, calibration, pre-registration of H4 (signals from T301; evaluation in T303) |
| Due | Fri 2026-11-13 (H4 values must be on `main` before the first T303 run) |
| Status | Template — no decision taken yet |

Template created in T001 by M1; owned by M3 from now on.

Related documents: [PROJECT_PLAN](../PROJECT_PLAN.md) (§7 H4 and pre-registration, §8 evaluation
protocol, §9 metric definitions) · task cards [T301](../team/M3_Talha.md#t301),
[T302](../team/M3_Talha.md#t302), [T303](../team/M3_Talha.md#t303) · [RELATED_WORK](../RELATED_WORK.md)
(T009) · [C2 design note](C2_embedding_adaptation.md) (what an alarm triggers).

How to use this template: every `<to fill in T302>` is replaced by a choice and a one-line
justification; a choice tuned on data cites its dev run (dev levels, dev seeds 2000–2099). No number
enters this note unless it is a config value cited to its file or copied from a `results/` file with its
path.

CSE 465 framing: C3 is a **novelty / anomaly detection** problem. The detector is fitted on nominal data
only (one-class setting), and evaluated with ROC analysis (AUROC), detection delay and false-alarm rate.

---

## 1. Signals

Computed per agent step by the frozen model, from its own predictions, with no extra environment
interaction (T301, `src/datdmpc/detect/signals.py`). Notation: `e` = task-embedding row of the current
task, `z_t = h(s_t, e)` = `model.encode(obs_t, task)`, `a_t` = the action executed by the planner.
Upstream methods: `third_party/tdmpc2/tdmpc2/common/world_model.py`.

| Signal | Formula | Upstream calls | Notes |
|---|---|---|---|
| Latent consistency error | `‖d(z_t, a_t, e) − h(s_{t+1}, e)‖²`, reported as MSE = squared ℓ2 distance / latent dim (convention of `F.mse_loss` in `TDMPC2._update`, [PROJECT_PLAN §9](../PROJECT_PLAN.md)) | `model.next(z_t, a_t, task)` vs `model.encode(obs_{t+1}, task)` | latent dim is 512 for mt30-5M and mt30-19M (`tdmpc2/common/__init__.py` MODEL_SIZE; `common/parser.py` overrides mt30-19M to 512) |
| Reward prediction error | `two_hot_inv(R(z_t, a_t, e)) − r_t`; signed, absolute or squared: `<to fill in T302>` | `model.reward(z_t, a_t, task)`, `common/math.two_hot_inv` | `r_t` = reward returned by the env wrapper for the agent step (sum over the action repeat of 2, `envs/dmcontrol.py`) |
| Q-ensemble disagreement | standard deviation across the `num_q` members of `two_hot_inv(Q_q(z_t, a_t, e))` | `model.Q(z_t, a_t, task, return_type='all')`, then `two_hot_inv` per member | `num_q: 5` (`tdmpc2/config.yaml`); `return_type='avg'` would average two **randomly** chosen heads, so `'all'` is required |

<!-- VERIFY: that the mt30 reward head was trained on per-agent-step rewards summed over the action repeat (check tdmpc2/trainer/offline_trainer.py and common/buffer.py); resolved in T301 by checking that nominal reward errors are centred near zero -->

Which signals enter the detector (single signal, combination, or one detector per signal) and why:
`<to fill in T302>`. H4 names consistency error and Q-ensemble disagreement; the reward error is
reported `<as a third detector / as analysis only — to fill in T302>`.

Extra cost per decision for the signals (`s_sig`, from the T301 handoff log, not from this note):
`<value from the T301 handoff entry>`.

## 2. Calibration protocol

- **Data separation (binding, [PROJECT_PLAN §8](../PROJECT_PLAN.md)):**
  - calibration: **nominal** episodes (`--shift none`) with seeds **1000–1099** only — fit the
    standardisation statistics and the alarm threshold;
  - hyperparameter tuning (EWMA weight, CUSUM drift, signal combination, window definition): dev levels
    with dev seeds 2000–2099;
  - held-out test levels and test seeds 0–99: untouched until T303.
- Calibration seeds used: `<list within 1000–1099 — to fill in T302>`; episodes per seed: `<to fill in T302>`.
- Standardisation per (task, signal): `<mean/std, or median/IQR, or nominal quantiles — to fill in T302>`.
- Threshold rule (set on calibration data only, e.g. a nominal-quantile rule chosen to respect `[[F]]`):
  `<to fill in T302>`.
- Tier/device: reported calibration runs on T1 (or reproduced there), on the **same tier and device** as
  the T303 evaluation they feed: `<to fill in T302>`.
- Command (binding interface, [T302 card](../team/M3_Talha.md#t302)):

  ```powershell
  python scripts/detect.py calibrate --ckpt checkpoints/mt30-5M.pt --task walker-walk --seeds 1000 1001 --episodes 1 --out outputs/debug/ --tier T0 --device cpu
  ```

  Reported calibration runs write to `results/P3_detect/`; their run folders are referenced from
  `configs/experiments/M3_detector.yaml`.

## 3. Detector

Let `x_t` be the standardised detection score at agent step t (Section 1–2).

| Detector | Statistic | Alarm | Parameters to choose (dev only) |
|---|---|---|---|
| EWMA | `m_t = λ · x_t + (1 − λ) · m_{t−1}` | `m_t > h_E` | `λ`, `h_E`, initial `m_0`: `<to fill in T302>` |
| One-sided CUSUM | `S_t = max(0, S_{t−1} + x_t − k)` | `S_t > h_C` | drift `k`, threshold `h_C`, reset rule after an alarm: `<to fill in T302>` |

Chosen detector(s) for H4 and why: `<to fill in T302>`. All values are stored in
`configs/experiments/M3_detector.yaml` (committed; its hash is written as `detector_config_sha` in every
T303 `summary.json`) and are **frozen** after the first T303 run.

Alarm → adaptation interface for the closed loop (T304, agreed with M1 and M2): what the detector
returns, whether it resets after an adaptation, and which transitions the adapter receives:
`<to fill in T302>`.

## 4. Mid-episode injection protocol

- An episode has 500 agent decisions (upstream `Timeout(max_episode_steps=500)`, action repeat 2,
  `tdmpc2/envs/dmcontrol.py`). The shift is switched on at agent step `--inject-at STEP` by the T101
  wrappers (M1); before `STEP` the episode must be step-for-step identical to the nominal episode with
  the same seed (T303 test).
- Injection step(s): `<to fill in T302>`. Constraints: enough post-injection steps to observe a delay up to
  `[[D]]`; enough pre-injection steps to contribute to the false-alarm count.
  <!-- VERIFY: that changing physics.model parameters (body_mass, geom_friction, actuator_gear, opt.gravity) in the middle of an episode takes effect at the next step in mujoco 3.1.2 / dm-control 1.0.16 without recomputing derived constants; resolved by the T101 wrapper tests (M1) before T303 -->
- Nominal episodes for false alarms: `scripts/detect.py evaluate --shift none` (`--inject-at` is
  required by the interface; with `--shift none` nothing is injected, and every monitored step counts
  as a nominal step).
- Shift types and levels: held-out test levels from `configs/shifts.yaml` (T102). `obs_noise` and
  `action_delay` are included as analysis cases (H3 counterpart).
- Command (binding interface, [T303 card](../team/M3_Talha.md#t303)):

  ```powershell
  python scripts/detect.py evaluate --ckpt checkpoints/mt30-5M.pt --task walker-walk --shift <dev level spec from configs/shifts.yaml> --inject-at <STEP> --detector-config configs/experiments/M3_detector.yaml --seeds 2000 --out outputs/debug/ --tier T0 --device cpu
  ```

## 5. Metrics

Definitions are those of [PROJECT_PLAN §9](../PROJECT_PLAN.md); this note only fixes the open choices.

| Metric | Definition | Open choice |
|---|---|---|
| AUROC | area under the ROC curve of the detection score separating nominal from shifted windows | window definition (length, position relative to `--inject-at`, which score per window): `<to fill in T302>` |
| Detection delay | (first alarm step ≥ injection step) − (injection step), in agent steps; no alarm after injection = missed detection, reported separately | how alarms before injection are treated in the delay: `<to fill in T302>` |
| False alarms per 1,000 nominal steps | 1000 × (alarms on nominal episodes or before injection) / (nominal agent steps monitored) | whether the detector resets after a false alarm: `<to fill in T302>` |

`summary.json` keys added by T303: `auroc`, `detection_delay_mean`, `missed_detections`,
`false_alarms_per_1000`, `inject_at`, `detector_config_sha`. AUROC is computed with numpy/scipy
(Mann–Whitney identity) unless M1 adds a dependency.

## 6. Pre-registered H4 thresholds

**Fill BEFORE the first T303 run.** Procedure ([PROJECT_PLAN §7.3](../PROJECT_PLAN.md)): M3 writes the
values and justifications here and opens the PR; M1 copies them into the PROJECT_PLAN pre-registration
table (commit on `dev_shahriar`, merged by M1). **No T303 run may start before these
values are in docs/PROJECT_PLAN.md on `main`.**

H4: consistency error and Q-ensemble disagreement detect shifts with AUROC ≥ `[[A]]`, false alarms ≤
`[[F]]` per 1,000 nominal steps, delay ≤ `[[D]]` steps.

| Quantity | Value | Justification (calibration / dev evidence path) |
|---|---|---|
| Minimum AUROC | `[[A]]` | |
| Maximum false alarms per 1,000 nominal steps | `[[F]]` | |
| Maximum detection delay (agent steps) | `[[D]]` | |
| Window definition for AUROC | `[[pre-register before run]]` | |
| Shift types counted for G3 (≥2 required, Tue 2026-11-24) | `[[pre-register before run]]` | |
| Aggregation across tasks and seeds | `[[pre-register before run]]` | |

Date the values were merged to `main`: `<YYYY-MM-DD, commit sha>`.

## 7. Relation to Feng et al. 2023 and TD-MPC2 App. J

The TD-MPC2 paper describes a test-time regulariser based on the standard deviation of the Q-ensemble,
taken from Feng et al. (2023) (Hansen et al., 2024, App. J, Eq. 9). This is the closest in-paper
precedent for our Q-disagreement signal.
<!-- VERIFY citation: Feng et al., 2023, "Finetuning Offline World Models in the Real World" — authors, venue (check the TD-MPC2 reference list), arXiv id; take from the T009 entry in RELATED_WORK.md -->

| Axis | TD-MPC2 App. J / Feng et al. 2023 | DA-TDMPC2 (C3) |
|---|---|---|
| How the ensemble std is computed (heads, action, latent) | `<to fill in T302 after reading App. J, Eq. 9 in docs/references/ and the T009 entry>` | std across all `num_q` heads of `two_hot_inv(Q(z_t, a_t, e))` at the executed action (Section 1) |
| What it is used for | `<to fill in T302>` | an **online detection score**, calibrated on nominal seeds, whose alarm triggers C2 |
| Other signals | `<to fill in T302>` | latent consistency error and reward prediction error |
| Evaluation | `<to fill in T302>` | AUROC, delay, false alarms per 1,000 nominal steps under mid-episode injection |

Differentiation in one paragraph (for the report): `<to fill in T302>`.

## 8. Decision log

One row per decision or change, newest first. A change to `configs/experiments/M3_detector.yaml` after
the first T303 run is a new row and the affected runs are marked exploratory.

| Date | Decision | Choice | Evidence (path / PR) | Decided by |
|---|---|---|---|---|
| 2026-10-21 | Template created | — | T001 | M1 |
