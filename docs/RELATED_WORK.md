# Related work — DA-TDMPC2

| Field | Value |
|---|---|
| Owner | M2 — Md. Ishtiak Ahmed Moyen |
| Task | [T009](team/M2_Ishtiak.md#t009) — read the guardrail papers, 2–3 sentences each in own words |
| Due | Tue 2026-10-27 (G0) |
| Status | Template — no paper read yet |

Template created in T001 by M1; owned by M2 from now on.

Related documents: [PROJECT_PLAN §6](PROJECT_PLAN.md) (differentiation table that M1 fills from this
file) · design notes [C1](design/C1_ranking.md) (M1) · [C2](design/C2_embedding_adaptation.md) (M2) ·
[C3](design/C3_detection.md) (M3) · [STATUS](STATUS.md).

---

## 1. Purpose

This file is the project's **only** source of statements about other papers. It exists to (a) protect
the novelty of C1–C3 against the closest published work ("novelty guardrails" of the bootstrap prompt),
(b) give the design notes and the report a differentiation that a team member has actually read, and
(c) keep every citation verifiable. The design notes and [PROJECT_PLAN §6](PROJECT_PLAN.md) copy from
here; they never describe a paper from memory.

Everything below the entry headings is **empty on purpose**. The identifiers in each stub are copied
from the bootstrap prompt and have not been checked; nobody has read these papers for this project yet.

## 2. Reading protocol (binding for T009 and for any later addition)

1. **Open the paper itself** (arXiv abstract page `https://arxiv.org/abs/<id>` or the venue
   proceedings). Do not summarise from abstracts of other papers, blog posts, or AI-generated summaries.
   PDFs of related papers are not committed (`docs/references/` is M1-owned and holds only the TD-MPC2
   paper and our proposal); link to the paper instead.
2. **Verify the citation** from the paper's own first page / arXiv page: authors, title, venue, year,
   arXiv id. Correct any identifier below that turns out to be wrong and note the correction in the
   change log (Section 6).
3. **Write the entry in your own words** — 2–3 sentences, no copied abstract text, no numbers from the
   paper unless they are needed for the differentiation (then cite section/table).
4. Fill the fixed fields of the entry: what the method **adapts or learns**, which **signals** it uses
   (losses, uncertainty, rewards, history…), its **cost** (training-time vs test-time; whether it needs
   retraining, privileged information or extra data), which of our contributions it is **closest to**
   (C1 / C2 / C3 / none), and **how DA-TDMPC2 differs** (one concrete sentence, reusable in a design note).
5. Set `Status` to `read`, add `Read by M2 on <YYYY-MM-DD>`, and only then delete the entry's
   `VERIFY citation` marker. A paper not read by the due date keeps its marker and is listed as a
   blocker in the handoff entry on [your team page](team/M2_Ishtiak.md).
6. Fill the matching row of the summary table (Section 3) and ask M1 in the handoff entry to copy the
   row into [PROJECT_PLAN §6](PROJECT_PLAN.md).

Statuses: `unread` → `skimmed` (citation verified, entry not written) → `read` (entry complete).

## 3. Summary table (filled in T009; copied by M1 into PROJECT_PLAN §6)

| Paper | Status | What it adapts / learns | Signals | Cost | Closest to | How DA-TDMPC2 differs |
|---|---|---|---|---|---|---|
| TD-MPC2 (base) | unread | | | | base model | |
| TD-MPC (base) | unread | | | | base model | |
| TD-M(PC)² | unread | | | | | |
| BMPC | unread | | | | | |
| TD-GRPC | unread | | | | | |
| JEPA-TTT | unread | | | | | |
| AdaJEPA | unread | | | | | |
| RMA | unread | | | | | |
| World Models as Reference Trajectories for Rapid Motor Adaptation | unread | | | | | |
| Feng et al., 2023 | unread | | | | | |

## 4. Entries

Entry fields (copy this block for any additional paper):

```text
Citation:          <authors, title, venue, year, arXiv id — verified from the paper itself>
Status:            unread | skimmed | read
Read by / date:    <M2, YYYY-MM-DD>
Summary (own words, 2–3 sentences):
What it adapts / learns:
Signals used:
Cost (training-time vs test-time; retraining? privileged info?):
Closest to (C1 / C2 / C3 / none):
How DA-TDMPC2 differs (one sentence):
```

### 4.1 Base references

#### TD-MPC2 (Hansen, Su, Wang — ICLR 2024)

- **Citation:** Nicklas Hansen, Hao Su, Xiaolong Wang. *TD-MPC2: Scalable, Robust World Models for
  Continuous Control.* International Conference on Learning Representations (ICLR), 2024.
  arXiv:2310.16828. (Authors, title, venue and year as in the BibTeX of the vendored upstream
  `third_party/tdmpc2/README.md`; arXiv id from the bootstrap prompt and the project facts sheet.) PDF in
  `docs/references/`.
- **Status:** unread
- **Read by / date:**
- **Summary (own words, 2–3 sentences):**
- **What it learns:**
- **Signals used:**
- **Cost:**
- **Closest to:** base model of all three contributions.
- **How DA-TDMPC2 differs:**
- **Sections the project already relies on** (pointers only, to read first): task embedding conditioning
  and norm constraint (§3.1, §3.3), embedding t-SNE (§4.1, Fig. 7), few-shot finetuning that initialises
  `e` from a similar task (App. E, Table 7; relevant to B3), test-time regulariser from Feng et al. 2023
  (App. J, Eq. 9; relevant to C3). Note for the summary: the released mt30 checkpoints use a
  64-dimensional task embedding per upstream `tdmpc2/common/parser.py`, although the paper's
  hyperparameter table lists 96 ([PROJECT_PLAN §2](PROJECT_PLAN.md)).

#### TD-MPC (Hansen et al., 2022)

- **Citation:** Nicklas Hansen, Xiaolong Wang, Hao Su. *Temporal Difference Learning for Model
  Predictive Control.* International Conference on Machine Learning (ICML), 2022. (As given in the BibTeX
  of the vendored upstream `third_party/tdmpc2/README.md`.)
  <!-- VERIFY citation: TD-MPC (Hansen et al., 2022) — confirm authors, title, venue, year from the paper itself and add the arXiv id (not recorded anywhere in the repo yet); resolved in T009 -->
- **Status:** unread
- **Read by / date:**
- **Summary (own words, 2–3 sentences):**
- **What it learns:**
- **Signals used:**
- **Cost:**
- **Closest to:** base model (predecessor of TD-MPC2).
- **How DA-TDMPC2 differs:**

### 4.2 Novelty-guardrail papers

#### TD-M(PC)²

- **Citation (from the bootstrap prompt, unchecked):** Lin et al., arXiv:2502.03550; L4DC 2026.
  <!-- VERIFY citation: TD-M(PC)² — authors, full title, venue (prompt says L4DC 2026), year, arXiv id 2502.03550; resolved in T009 -->
- **Status:** unread
- **Read by / date:**
- **Summary (own words, 2–3 sentences):**
- **What it adapts / learns:**
- **Signals used:**
- **Cost:**
- **Closest to:** to decide after reading (listed in the C1 differentiation of [T401](team/M1_Shahriar.md#t401)).
- **How DA-TDMPC2 differs:**

#### BMPC — Bootstrapped MPC

- **Citation (from the bootstrap prompt, unchecked):** Wang et al., ICLR 2025.
  <!-- VERIFY citation: BMPC (Bootstrapped MPC) — authors, full title, venue (prompt says ICLR 2025), year, arXiv id (none given in the prompt); resolved in T009 -->
- **Status:** unread
- **Read by / date:**
- **Summary (own words, 2–3 sentences):**
- **What it adapts / learns:**
- **Signals used:**
- **Cost:**
- **Closest to:** to decide after reading (listed in the C1 differentiation of [T401](team/M1_Shahriar.md#t401)).
- **How DA-TDMPC2 differs:**

#### TD-GRPC

- **Citation (from the bootstrap prompt, unchecked):** arXiv:2505.13549.
  <!-- VERIFY citation: TD-GRPC — authors, full title, venue, year, arXiv id 2505.13549 (no authors given in the prompt); resolved in T009 -->
- **Status:** unread
- **Read by / date:**
- **Summary (own words, 2–3 sentences):**
- **What it adapts / learns:**
- **Signals used:**
- **Cost:**
- **Closest to:** C1 according to the bootstrap prompt — confirm or correct after reading.
- **How DA-TDMPC2 differs:**

#### JEPA-TTT

- **Citation (from the bootstrap prompt, unchecked):** arXiv:2610.00722.
  <!-- VERIFY citation: JEPA-TTT — authors, full title, venue, year, arXiv id 2610.00722 (an October-2026 identifier; confirm it resolves to this paper); resolved in T009 -->
- **Status:** unread
- **Read by / date:**
- **Summary (own words, 2–3 sentences):**
- **What it adapts / learns:**
- **Signals used:**
- **Cost:**
- **Closest to:** C2 according to the bootstrap prompt — confirm or correct after reading.
- **How DA-TDMPC2 differs:** (write after reading; the working hypothesis to test against the paper is
  in [PROJECT_PLAN §6](PROJECT_PLAN.md): only one 64-number row `e` of a multitask TD-MPC2 model,
  reward/value losses in addition to latent consistency, detection-triggered, T0 CPU cost reported.)

#### AdaJEPA

- **Citation (from the bootstrap prompt, unchecked):** AdaJEPA (no authors, venue or identifier given).
  <!-- VERIFY citation: AdaJEPA — find the paper and record authors, full title, venue, year, arXiv id; if it cannot be found, say so here and in the handoff entry; resolved in T009 -->
- **Status:** unread
- **Read by / date:**
- **Summary (own words, 2–3 sentences):**
- **What it adapts / learns:**
- **Signals used:**
- **Cost:**
- **Closest to:** C2 according to the bootstrap prompt — confirm or correct after reading.
- **How DA-TDMPC2 differs:**

#### RMA

- **Citation (from the bootstrap prompt, unchecked):** Kumar et al., 2021.
  <!-- VERIFY citation: RMA (Kumar et al., 2021) — full title, all authors, venue, year, arXiv id; resolved in T009 -->
- **Status:** unread
- **Read by / date:**
- **Summary (own words, 2–3 sentences):**
- **What it adapts / learns:**
- **Signals used:**
- **Cost:**
- **Closest to:** to decide after reading.
- **How DA-TDMPC2 differs:**

#### World Models as Reference Trajectories for Rapid Motor Adaptation

- **Citation (from the bootstrap prompt, unchecked):** "World Models as Reference Trajectories for Rapid
  Motor Adaptation", arXiv:2505.15589.
  <!-- VERIFY citation: World Models as Reference Trajectories for Rapid Motor Adaptation — authors, exact title, venue, year, arXiv id 2505.15589; resolved in T009 -->
- **Status:** unread
- **Read by / date:**
- **Summary (own words, 2–3 sentences):**
- **What it adapts / learns:**
- **Signals used:**
- **Cost:**
- **Closest to:** to decide after reading.
- **How DA-TDMPC2 differs:**

#### Feng et al., 2023 — Finetuning Offline World Models in the Real World

- **Citation (from the bootstrap prompt, unchecked):** Feng et al., 2023, *Finetuning Offline World
  Models in the Real World*. The TD-MPC2 paper refers to Feng et al. (2023) for a test-time regulariser based on Q-ensemble
  standard deviation (Hansen et al., 2024, App. J, Eq. 9).
  <!-- VERIFY citation: Feng et al., 2023 — full author list, exact title, venue (check the TD-MPC2 reference list and the paper itself), arXiv id; resolved in T009 -->
- **Status:** unread
- **Read by / date:**
- **Summary (own words, 2–3 sentences):**
- **What it adapts / learns:**
- **Signals used:**
- **Cost:**
- **Closest to:** to decide after reading (the uncertainty signal is relevant to C3; see
  [C3 design note](design/C3_detection.md)).
- **How DA-TDMPC2 differs:**

### 4.3 Additional papers found while reading

Add an entry here (same fields) for any further paper a team member reads and considers close to C1–C3.
New papers after the stop rule date (Tue 2026-11-24, no new ideas) are recorded for the report's related
work section only; they do not change the design.

## 5. Open questions for the design notes

Questions that reading should answer, one line each, with the design note that consumes the answer:

- C2 ([T201](team/M2_Ishtiak.md#t201)): which parameters do JEPA-TTT and AdaJEPA update at test time, and which losses do they use? `<answer after reading>`
- C1 ([T401](team/M1_Shahriar.md#t401)): what exactly do TD-GRPC, BMPC and TD-M(PC)² change in TD-MPC2-style training or planning? `<answer after reading>`
- C3 ([T302](team/M3_Talha.md#t302)): how is the Q-ensemble uncertainty of Feng et al. 2023 defined and used? `<answer after reading>`

## 6. Change log

| Date | Member | Change |
|---|---|---|
| 2026-10-21 | M1 | Template created in T001 (identifiers copied from the bootstrap prompt; nothing read yet). |
