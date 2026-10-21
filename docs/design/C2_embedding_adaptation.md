# C2 — Embedding-only test-time adaptation (design note)

| Field | Value |
|---|---|
| Owner | M2 — Md. Ishtiak Ahmed Moyen |
| Task | [T201](../team/M2_Ishtiak.md#t201) — design + pre-registration of H2 (and H3); implemented in T202–T204 |
| Due | Thu 2026-11-05 (must be on `main` before the first T204 run) |
| Status | Template — no decision taken yet |

Template created in T001 by M1; owned by M2 from now on.

Related documents: [PROJECT_PLAN](../PROJECT_PLAN.md) (§3 methods, §7 hypotheses and pre-registration,
§8 evaluation protocol, §9 metrics) · [T201 card](../team/M2_Ishtiak.md#t201) (decisions 1–11 and their
verified upstream facts) · [RELATED_WORK](../RELATED_WORK.md) (T009) · [C3 design note](C3_detection.md)
(trigger interface).

How to use this template: every `<to fill in T201>` is replaced by a choice **and** a one-line
justification; a choice tuned on data cites the dev run folder (`results/P2_adapt/<run_id>/`, dev levels
and dev seeds 2000–2099 only). Starting proposals below are proposals, not decisions, until the owner
confirms them in the decision log (Section 13). No number enters this note unless it is a config value
cited to its file or copied from a `results/` file with its path.

---

## 1. Goal

Under a post-training dynamics shift, freeze every network weight of the released multitask TD-MPC2
model and adapt **only the task-embedding row `e` of the current task** from K recent shifted-env
transitions, using the world model's own training losses. Compare with no adaptation (B0), full and
partial finetuning (B1, B2) and a random-`e` ablation (B3) on return / gap recovery, samples (K), T0 CPU
wall-time and parameters updated (H2), and characterise the shifts it cannot correct (H3).

Scope statement for the report: `<to fill in T201 — one paragraph>`.

## 2. Setting (verified upstream facts; cite these files, do not restate from memory)

- **Embedding size.** `self._task_emb = nn.Embedding(len(cfg.tasks), cfg.task_dim, max_norm=1)`
  (`third_party/tdmpc2/tdmpc2/common/world_model.py`). For `mt30-5M` and `mt30-19M`, `task_dim = 64`
  (`tdmpc2/common/parser.py`: 96 only for mt80 and for the 1M/317M models). The table is 30 × 64, so
  **one task's `e` is 64 numbers** — not the "~96" of the original prompt and repo description.
- **Where `e` enters.** `WorldModel.task_emb` concatenates `e` to the input of the encoder `h`, the
  dynamics `d`, the reward head `R`, the policy prior `p` and every Q head (`world_model.py`: `encode`,
  `next`, `reward`, `pi`, `Q`). Changing `e` therefore changes all five components at once — including
  the encoder that produces the consistency **target** `h(s_{t+1}, e)`.
- **Initialisation.** Upstream initialises embeddings uniformly in [-0.02, 0.02]
  (`tdmpc2/common/init.py`, `weight_init`); relevant to B3.
- **`max_norm=1` behaviour.** PyTorch renormalises the looked-up rows in place at lookup time, so an
  optimizer step may move the row outside the unit ball and the next lookup projects it back.
  <!-- VERIFY: in torch 2.7.1, nn.Embedding(max_norm=...) renormalises looked-up rows in place without gradient flowing through the renormalisation, and the docs require cloning the weight if it is used in a differentiable op before the lookup; check the PyTorch docs/source in T201 -->
  Decision (keep the implicit projection, or adapt a separate 64-d parameter with explicit projection
  onto the unit ball): `<to fill in T201>`. In every case the saved `adapted_embedding.json` holds the
  row **as used by the model** (norm ≤ 1), and `summary.json` logs `‖e‖` before and after adaptation.
- **Tensors that require grad.** Only `model._task_emb.weight`, restricted to row `task_idx` (gradient
  mask, or a separate 64-d parameter written back into the row); every other parameter has
  `requires_grad=False`. With Adam and no weight decay, rows that never receive a non-zero gradient stay
  unchanged; the T202 test proves "only `e` changes" bit-exactly. Chosen mechanism: `<to fill in T201>`.
- **Train vs eval mode.** Upstream `_update` calls `self.model.train()` (Q-head dropout active,
  `dropout: 0.01` in `tdmpc2/config.yaml`). Mode during adaptation: `<to fill in T201>`.
- **Planning is unchanged.** MPPI settings (`tdmpc2/config.yaml`: `horizon: 3`, `num_samples: 512`,
  `iterations: 6`, …) are never changed in reported results; only the embedding row differs.

## 3. Loss

**Starting proposal (to be confirmed in T201):** reuse the upstream objective of `TDMPC2._update`
(`third_party/tdmpc2/tdmpc2/tdmpc2.py`) with its default coefficients from `tdmpc2/config.yaml`:

```text
L(e) = consistency_coef · Σ_t ρ^t · MSE( d(z_t, a_t, e), sg[h(s_{t+1}, e)] ) / H
     + reward_coef      · Σ_t ρ^t · CE( R̂(z_t, a_t, e), r_t ) / H
     + value_coef       · Σ_t ρ^t · Σ_q CE( Q̂_q(z_t, a_t, e), sg[TD_target_t] ) / (H · num_q)

consistency_coef = 20, reward_coef = 0.1, value_coef = 0.1, rho = 0.5, horizon H = 3, num_q = 5
(tdmpc2/config.yaml); episodic: false, so the termination term is inactive.
```

`sg[·]` = computed under `torch.no_grad()` as upstream does for `next_z` and the TD target. Upstream's TD
target is `r_t + γ_task · Q_target(next_z, pi(next_z), return_type='min')` with the per-task discount
(`tdmpc2.py` `_td_target`).

Decisions:

| # | Question | Choice | Justification / dev evidence |
|---|---|---|---|
| L1 | Keep all three terms and the upstream coefficients? | `<to fill in T201>` | |
| L2 | Consistency target: recomputed with the **current** `e` at every step (moving target, as upstream) or fixed with the **initial** `e`? (`e` enters the encoder, so a moving target can be "fitted" by changing the target itself.) | `<to fill in T201>` | |
| L3 | TD target: recomputed each step or fixed at the initial `e`; target Q-ensemble frozen (no Polyak update)? | `<to fill in T201>` | |
| L4 | Sequence structure: one contiguous segment of K transitions → `K − H + 1` windows of length H; full batch or mini-batch per step | `<to fill in T201>` | |
| L5 | Any loss term dropped or re-weighted (ablation only, justified by a dev result) | `<to fill in T201>` | |

## 4. Optimizer

| Item | Choice | Justification / dev evidence |
|---|---|---|
| Optimizer (upstream uses Adam) | `<to fill in T201>` | |
| Learning-rate grid (dev only; upstream default `lr: 3e-4` in `tdmpc2/config.yaml` is a training value, not a test-time one) | `<to fill in T201>` | |
| Gradient clipping (upstream `grad_clip_norm: 20`) kept or dropped | `<to fill in T201>` | |
| Weight decay | none on the embedding table (required for the "only row `task_idx` changes" guarantee) — confirm | |
| Optimizer state reset between adaptation episodes / seeds | `<to fill in T201>` | |

Interface note: `scripts/adapt.py` exposes only `--K`, `--grad-steps` and `--lr` as tunable flags. Every
other choice in this note is fixed in `src/datdmpc/adapt/embedding.py` defaults and written to the run's
`config.yaml`; a new flag is an interface change approved by M1.

## 5. K grid (number of transitions)

- Grid: `<to fill in T201>` (all values ≤ `[[K_max]]`).
- How K transitions are collected: B0 planner on the shifted env, seeded by the adaptation seed, starting
  from `<episode start / after a burn-in of n steps — to fill in T201>`.
- "Samples to 80%" ([PROJECT_PLAN §9](../PROJECT_PLAN.md)) is evaluated on this grid, so the grid is
  fixed before T204.

## 6. Gradient-step budget

- Grid of `N_grad` (`--grad-steps`): `<to fill in T201>`.
- Budget-matching rule across methods (default in [PROJECT_PLAN §8](../PROJECT_PLAN.md): matched
  gradient steps, wall-time reported for every method): `[[pre-register before run]]`.
- Wall-time is measured on the same tier and device for B1 and Ours-C2 (T0 CPU, `scripts/profile.py
  --what adapt`, T008); data-collection time is reported separately.
- Compute estimate (symbols only, from the T201 card):
  `hours = N_task_dev × N_shift_dev × |K grid| × |N_grad grid| × |lr grid| × N_seed_dev × (K × s_plan + N_grad × s_grad(e_only) + N_ep × L × s_plan) / 3600`,
  with `s_plan`, `s_grad` from `results/P0_profile/` (T008) and `L` = 500 agent decisions per episode
  (`tdmpc2/envs/dmcontrol.py`). > 3 laptop-hours → T1, sharded.

## 7. Online vs batch

| Mode | Procedure | Used in |
|---|---|---|
| Batch | collect K transitions with B0 → `N_grad` steps on them → `N_ep` evaluation episodes with the adapted `e` | `<to fill in T201>` (T204 main sweep?) |
| Online | sliding window of the last K transitions, updates during the episode | `<to fill in T201>` (closest to the closed loop, T304) |

Decision and justification: `<to fill in T201>`. Interface for the closed loop (how `closed_loop.py`
calls the adapter after a C3 alarm, and with which transitions) is agreed with M1 (T304) and M3 (T302):
`<to fill in T201>`.

## 8. Data the adapter may see

- **Identical data for all methods:** B1, B2, B3, Ours-C2 (and the G2 fallback) receive the **identical
  K transitions** for a given (task, shift level, seed) — same object or same hash, checked by
  `tests/test_baselines.py` (T203).
- Allowed: the K shifted-env transitions `(s_t, a_t, r_t, s_{t+1})` of the current task and the frozen
  checkpoint. Proposed default (confirm): no nominal-env data, no data from other tasks, no simulator
  parameters or shift labels (no privileged information).
- Not allowed: test levels or test seeds 0–99 during any tuning; tuning uses dev levels and dev seeds
  2000–2099 only ([PROJECT_PLAN §8](../PROJECT_PLAN.md)).
- Exceptions (if any) and justification: `<to fill in T201>`.

## 9. Baselines B1–B3

All baselines use the loss of Section 3, the data of Section 8 and the budget rule of Section 6.
Parameter counts are computed from the loaded model and written as `n_params_updated` in `summary.json`,
never by hand. Implementation: `src/datdmpc/adapt/baselines.py` (T203).

| Label | `--method` | What is updated | Open choices |
|---|---|---|---|
| B0 | (`scripts/eval.py`) | nothing (frozen model on the shifted env) | — |
| B1 full finetune | `full_ft` | the parameter groups of upstream's world-model optimizer (`tdmpc2.py`: encoder with `enc_lr_scale: 0.3`, dynamics, reward, Q-ensemble, task embedding; termination absent because `episodic: false`) | policy prior (upstream updates it separately with `pi_optim`) updated or frozen; target-Q handling: `<to fill in T201>` |
| B2 partial finetune | `partial_ft` | reward head + Q heads (`model._reward`, `model._Qs`); `e` frozen | whole heads or final layers only: `<to fill in T201>` |
| B3 random-`e` | `rand_e` | row `task_idx`, re-initialised before adaptation, then exactly the Ours-C2 procedure | init distribution (default: upstream embedding init, `common/init.py`), seeded by the adaptation seed: `<to fill in T201>` |
| Ours-C2 | `e_only` | row `task_idx` (64 numbers) | — |
| G2 fallback (only if G2 fails) | `e_ln` | row `task_idx` + LayerNorm affine parameters (`NormedLinear.ln`, `common/layers.py`); count from the loaded model | which LayerNorms: `<to fill in T201>` |

B3 relates to the paper's few-shot finetuning, which initialises `e` from a semantically similar task
(Hansen et al., 2024, App. E, Table 7).

## 10. Pre-registered H2 (and H3) thresholds

**Fill BEFORE the first T204 run.** Procedure ([PROJECT_PLAN §7.3](../PROJECT_PLAN.md)): M2 writes the
values and justifications here and opens the PR; M1 copies them into the PROJECT_PLAN pre-registration
table (commit on `dev_shahriar`, merged by M1). **No T204 run may start before these
values are in docs/PROJECT_PLAN.md on `main`.**

H2: `e`-only adaptation with K ≤ `[[K_max]]` transitions recovers ≥ `[[X]]`% of the nominal–shifted gap
at ≤ `[[Y]]`% of full-finetune wall-time, on held-out levels.

| Hypothesis | Quantity | Value | Justification (dev evidence path) |
|---|---|---|---|
| H2 | Maximum transitions | `[[K_max]]` | |
| H2 | Minimum gap recovery (%) | `[[X]]` | |
| H2 | Maximum wall-time relative to B1 (%) | `[[Y]]` | same tier and device for B1 and Ours-C2 |
| H2 | Budget-matching rule | `[[pre-register before run]]` | |
| H2 | Aggregation (per task / IQM across tasks; which shift types — G2 requires mass and friction) | `[[pre-register before run]]` | |
| H3 | "Poorly corrected" bound for `obs_noise` and `action_delay` | `[[pre-register before run]]` | |

Date the values were merged to `main`: `<YYYY-MM-DD, commit sha>`.

## 11. Differentiation vs JEPA-TTT / AdaJEPA

Closest published work for C2 according to the bootstrap prompt. Fill only from M2's T009 entries in
[RELATED_WORK](../RELATED_WORK.md), never from memory.
<!-- VERIFY citation: JEPA-TTT (arXiv:2610.00722) and AdaJEPA — what each adapts at test time and which losses/signals it uses; take from the T009 entries in RELATED_WORK.md -->

| Axis | JEPA-TTT | AdaJEPA | DA-TDMPC2 (C2) |
|---|---|---|---|
| Parameters updated at test time | `<from T009>` | `<from T009>` | one task-embedding row `e`, 64 numbers (mt30-5M/19M, `common/parser.py`); all network weights frozen |
| Base model | `<from T009>` | `<from T009>` | released multitask TD-MPC2 checkpoints (mt30-5M, mt30-19M) |
| Adaptation signals / losses | `<from T009>` | `<from T009>` | latent consistency + reward + value (Section 3) |
| When adaptation starts | `<from T009>` | `<from T009>` | triggered by the C3 detector (T304) |
| Cost reported | `<from T009>` | `<from T009>` | T0 laptop CPU wall-time and parameters updated |

Differentiation in one paragraph (for the report): `<to fill in T201>`.

## 12. Risks and fallback

| Risk | Early sign (dev runs) | Response |
|---|---|---|
| `e` too low-capacity to absorb the shift (PROJECT_PLAN risk R4) | dev-level gap recovery near zero for all K and `N_grad` | **G2 fallback** (Tue 2026-11-17, only if G2 fails): adapt `e` + LayerNorm affine parameters (LayerNorm sits in upstream `NormedLinear`, `tdmpc2/common/layers.py`); report the `e`-only result honestly with parameter counts. Which LayerNorms (all / per component), parameter count from the loaded model: `<to fill in T201>`. |
| Consistency loss decreases but return does not recover (moving target, L2) | loss falls, return flat | `<to fill in T201>` |
| Overfitting to K transitions / instability | return after adaptation below B0 | `<to fill in T201>` (e.g. fewer steps, lower lr — tuned on dev only) |
| Adapted `e` harms other components (policy prior, Q) | ranking fidelity (T205) or return drops | `<to fill in T201>` |
| B1 on mt30-19M exceeds 12 GB laptop RAM | out-of-memory on T0 | run B1 on Colab (T1); wall-time comparison still on matched tier/device |

G2 fallback interface: `scripts/adapt.py --method e_ln` (task embedding + LayerNorm affine parameters;
used only if G2 fails on Tue 2026-11-17; which LayerNorms are included is fixed in this note in T201).

## 13. Decision log

One row per decision or change, newest first. A decision changed after a T204 run started is a new row
and the affected runs are marked exploratory.

| Date | Decision | Choice | Evidence (path / PR) | Decided by |
|---|---|---|---|---|
| 2026-10-21 | Template created | — | T001 | M1 |
