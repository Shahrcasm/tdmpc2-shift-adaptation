# C1 — Action ranking under dynamics shift (design note, stretch)

| Field | Value |
|---|---|
| Owner | M1 — Md. Shahriar Rakib Rabbi |
| Task | [T401](../team/M1_Shahriar.md#t401) — C1 design note + differentiation (evidence from T104 and T205; pilot T402/T403 only if G2 passed by 2026-11-17) |
| Due | Wed 2026-12-02 (experiment freeze; G4 decided the same day). Drafting can start after G1 (Tue 2026-11-03). |
| Status | Template — not started |

Template created in T001 by M1; owned by M1.

Related documents: [PROJECT_PLAN](../PROJECT_PLAN.md) (§3 contributions, §7 H1/H5 and pre-registration,
§9 Kendall τ and top-1 definitions) · task cards [T104](../team/M1_Shahriar.md#t104),
[T205](../team/M1_Shahriar.md#t205), [T401](../team/M1_Shahriar.md#t401) ·
[ranking-fidelity pre-registration table](../team/M1_Shahriar.md#pre-registration-ranking-fidelity-design-h1-t104)
· [RELATED_WORK](../RELATED_WORK.md) (T009) · [STATUS](../STATUS.md) (G2/G4 status).

Expected outcome with 6 weeks: C1 remains the ranking-fidelity diagnostic (T104, T205) plus this design
note. No number enters this note unless it is a config value cited to its file or copied from a
`results/` file with its path.

---

## 1. Ranking-fidelity diagnostic — definition

Purpose: measure whether dynamics shift corrupts how the frozen world model **ranks** candidate action
sequences (first half of the unifying story; H1), and whether `e`-only adaptation restores it (T205).
The binding method description, tests and commands are in the [T104 card](../team/M1_Shahriar.md#t104);
the design values (N, M, H, start-state sampling, candidate generation, bootstrap-tail treatment) are
pre-registered in the [table on the M1 page](../team/M1_Shahriar.md#pre-registration-ranking-fidelity-design-h1-t104)
before the first run writing to `results/P1_ranking/`. This section summarises the definition for the
report; it does not override those values.

For one start state `s` reached by the frozen B0 planner (nominal or shifted env, same seed):

1. **Save** the simulator state (`physics.get_state()` on the raw dm_control env, reachable through
   `DMControlWrapper.env`; `third_party/tdmpc2/tdmpc2/envs/dmcontrol.py`) and any wrapper-level state
   (episode step counter, action-delay buffer, observation-noise RNG). The shift lives in
   `physics.model` parameters, so it persists across restores.
2. Generate **M candidate action sequences** `A_1 … A_M`, each of **H agent steps** (generation rule:
   pre-registered).
3. **True return** of each candidate: restore the state, execute `A_m` through the upstream wrapper (each
   agent action applied twice, rewards summed — action repeat 2), and compute
   `G_true(A_m) = Σ_{t<H} γ^t r_t` with the task's planner discount `γ` (`TDMPC2._get_discount`,
   `tdmpc2/tdmpc2.py`). Restore again before the next candidate and before the main episode continues.
4. **Model score** of each candidate (`z_0 = h(s, e)`, `z_{t+1} = d(z_t, a_t, e)`):
   - (i) reward-only: `G_model(A_m) = Σ_{t<H} γ^t · two_hot_inv(R(z_t, a_t, e))`;
   - (ii) planner score: as upstream `TDMPC2._estimate_value` — (i) plus the discounted
     `Q(z_H, pi(z_H), return_type='avg')` bootstrap.
   Primary variant and tail treatment: pre-registered.
5. **Per-state metrics:** Kendall τ (tau-b when ties occur) between `G_model` and `G_true` over the M
   candidates; top-1 agreement = 1 if `argmax G_model = argmax G_true`, else 0. Aggregated over states
   with a 95% bootstrap CI ([PROJECT_PLAN §9](../PROJECT_PLAN.md)).

Horizon note: the planner's own horizon is `horizon: 3` (`tdmpc2/config.yaml`); choosing H equal to it
makes the model score equal to what MPPI compares.

Open verification items (determinism of save/restore, dm_control's own step counter) are tracked as
`VERIFY` markers in the [T104 card](../team/M1_Shahriar.md#t104) and resolved by its tests.

Binding interface:

```powershell
python -m datdmpc.diagnostics.ranking_fidelity --ckpt checkpoints/mt30-5M.pt --task walker-walk --shift none --states <N> --candidates <M> --horizon <H> --seed 2000 --out outputs/debug/ --tier T0 --device cpu
python -m datdmpc.diagnostics.ranking_fidelity --ckpt checkpoints/mt30-5M.pt --task walker-walk --shift <dev level spec from configs/shifts.yaml> --states <N> --candidates <M> --horizon <H> --seed 2000 --out outputs/debug/ --embedding outputs/debug/<adapt run_id>/adapted_embedding.json --tier T0 --device cpu
```

## 2. Findings (fill from results only)

Every cell cites its `summary.json`. Reported runs use mt30-19M on T1 (or reproduced there).

### 2.1 Nominal vs shifted (T104, `results/P1_ranking/`)

| Task | Shift spec | Score variant | Kendall τ (mean, 95% CI) | Top-1 agreement | Source |
|---|---|---|---|---|---|
| `<study task>` | `none` | `<variant>` | `<kendall_tau_mean>` (`<kendall_tau_ci95_low>`–`<kendall_tau_ci95_high>`) | `<top1_agreement>` | `results/P1_ranking/<run_id>/summary.json` |
| `<study task>` | `<shift spec>` | `<variant>` | `<kendall_tau_mean>` (`<ci95>`) | `<top1_agreement>` | `results/P1_ranking/<run_id>/summary.json` |

### 2.2 After `e`-only adaptation (T205, `results/P2_ranking_after_adapt/`)

Paired with the T104 rows at the same start states (same task, shift, seed).

| Task | Shift spec | Kendall τ frozen (T104) | Kendall τ adapted (T205) | Top-1 frozen → adapted | Sources |
|---|---|---|---|---|---|
| `<study task>` | `<test level spec>` | `<value, results/P1_ranking/<run_id>/summary.json>` | `<value, results/P2_ranking_after_adapt/<run_id>/summary.json>` | `<value>` → `<value>` | both paths |

### 2.3 Interpretation

H1 (ranking part) verdict against the pre-registered criteria: `<to fill in T401>`. Where ranking errors
occur (which shift types, which candidate pairs, reward-only vs planner score): `<to fill in T401>`.

## 3. Candidate ranking-loss design (stretch; H5)

Fill only if the findings show a ranking problem worth fixing. The design must be implementable by
subclassing/wrapping in `src/datdmpc/ranking/` — never by editing `third_party/`.

| Item | Proposal |
|---|---|
| Problem it targets (cite Section 2) | `<to fill in T401>` |
| Objective (formula) and which parameters it trains | `<to fill in T401>` |
| Source of ranking supervision (model's own targets vs simulator ground truth) and why it is available at training time | `<to fill in T401>` |
| Starting point (finetune from mt30-5M / mt30-19M) and loss weight relative to upstream terms | `<to fill in T401>` |
| Matched comparison (same steps, same seeds, with vs without the ranking term) | `<to fill in T401>` |
| Compute (symbols only, from the T401 card): `N_task × N_seed × n_grad_steps × s_grad,full / 3600` + evaluation, `s_grad,full` from T008 | `<to fill in T401>` |
| Tests (`tests/test_ranking.py`) | `<to fill in T401>` |

H5 (stretch): a ranking auxiliary loss raises Kendall τ without lowering return at matched steps/seeds.

| Quantity | Value | Justification |
|---|---|---|
| Minimum Kendall τ gain | `[[pre-register before run]]` | |
| Return non-inferiority margin | `[[pre-register before run]]` | |

Procedure ([PROJECT_PLAN §7.3](../PROJECT_PLAN.md)): M3 proposes the values here; M1 copies them into the
PROJECT_PLAN pre-registration table before any pilot run.

## 4. Differentiation vs TD-GRPC / BMPC / TD-M(PC)²

Fill only from the T009 entries in [RELATED_WORK](../RELATED_WORK.md); a row keeps its marker until a
team member has read the paper. TD-GRPC is the closest work according to the bootstrap prompt.

| Work | What it changes | Signal used | How C1 differs |
|---|---|---|---|
| TD-GRPC (arXiv:2505.13549) <!-- VERIFY citation: TD-GRPC — authors, title, venue, year; content from the T009 entry --> | `<from T009>` | `<from T009>` | `<to fill in T401>` |
| BMPC — Bootstrapped MPC (Wang et al., ICLR 2025) <!-- VERIFY citation: BMPC — authors, title, venue, year, arXiv id; content from the T009 entry --> | `<from T009>` | `<from T009>` | `<to fill in T401>` |
| TD-M(PC)² (Lin et al., arXiv:2502.03550) <!-- VERIFY citation: TD-M(PC)² — authors, title, venue, year; content from the T009 entry --> | `<from T009>` | `<from T009>` | `<to fill in T401>` |

Axis already fixed by the plan (to be checked against each paper): C1's core is a **diagnostic** of
ranking fidelity under dynamics shift with simulator save/restore ground truth, applied to a frozen
released model, before and after `e`-only adaptation.

Differentiation in one paragraph (for the report): `<to fill in T401>`.

## 5. Go/no-go rule for the pilot (G4)

- The pilot (T402/T403) exists **only if G2 is marked Passed in [STATUS](../STATUS.md) by Tue
  2026-11-17**. T402/T403 are not on the seed board; M1 adds them (and the pilot results folder, in the
  ownership table) only in that case.
- If approved: H5 values (Section 3) are on `main` before any pilot run; the design is fixed before Tue
  2026-11-24 (stop rule: no new ideas after Nov 24); all pilot runs finish before the experiment freeze,
  Wed 2026-12-02, when G4 is decided.
- If G2 fails or is late: no pilot. This note records that, and C1 = T104 + T205 + this note.

Record:

| Item | Value |
|---|---|
| G2 status on 2026-11-17 (STATUS) | `<Passed / Failed→fallback / late>` |
| Pilot decision | `<run / not run — reason>` |
| G4 outcome on 2026-12-02 | `<H5 met / not met / not tested>` with evidence path |

## 6. Decision log

One row per decision or change, newest first.

| Date | Decision | Choice | Evidence (path / PR) | Decided by |
|---|---|---|---|---|
| 2026-10-21 | Template created | — | T001 | M1 |
