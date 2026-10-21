---
name: Task
about: A task card for the DA-TDMPC2 task board (one task, one owner, binary "Done when")
title: "T<ID>: "
labels: task
assignees: ''
---

<!--
Title: "T<ID>: <task in imperative form>", e.g. "T103: degradation sweep of B0".
The authoritative task card lives on the owner's team page (docs/team/<SLOT>_<NAME>.md); this issue mirrors it.
docs/STATUS.md is updated by M1 only, at merge time.
Rules: no experiment without a task card; no new ideas after 2026-11-24; hypotheses and thresholds are written
into docs/PROJECT_PLAN.md before the corresponding runs; nothing is scheduled after the experiment freeze
(Wed 2026-12-02) except writing and the reproducibility check.
Do not write GitHub handles; identify people by slot and name.
-->

## Task

- **Task ID:** T<ID>  <!-- seed IDs are in docs/STATUS.md; for a new task, M1 assigns the next free ID -->
- **Owner:** <!-- M1 (Md. Shahriar Rakib Rabbi) / M2 (Md. Ishtiak Ahmed Moyen) / M3 (Md. Abdullah Talha) -->
- **Branch:** `dev_<name>`
- **Task card:** <link to the card on the owner's team page>

## Goal

<!-- One or two sentences: what exists or is known when this task is finished. -->

## Depends on

<!-- Task IDs that must be merged first, e.g. "T006, T101", or "-". The dependency graph must stay acyclic. -->

## Target date

<!-- YYYY-MM-DD, consistent with the 6-week roadmap and gates in docs/PROJECT_PLAN.md. -->

## Compute tier and budget

- **Tier:** <!-- T0 laptop / T1 Colab free / T1b Kaggle backup -->
- **Budget formula:**
  `<#tasks> × <#shifts> × <#seeds> × <#episodes> × <steps> × <sec/step> = <hours>`
  <!-- sec/step comes from results/P0_profile/ (T008); never assume it. Steps per episode: 500 agent decisions
       for DMControl (third_party/tdmpc2/tdmpc2/envs/dmcontrol.py: action repeat 2, max_episode_steps=500).
       More than 3 laptop-hours -> run on Colab, sharded with --shard i/N and --resume. -->
- **Colab accounts / shards:** <!-- e.g. "M1 1/3, M2 2/3, M3 3/3", or "n/a" -->

## Files to create or modify (owned paths only)

<!-- Every path must belong to the owner in the ownership table of AGENTS.md §2. -->

- `<path>`

## Exact commands

<!-- Only our own scripts and the flags defined in AGENTS.md §5 (e.g. scripts/eval.py, scripts/adapt.py,
     scripts/detect.py). PowerShell 5.1 on laptops: one command per line, no "&&". -->

```powershell
<command>
```

## Done when

<!-- Binary checklist; each item verifiable by opening a file or running a command. -->

- [ ] <result folder `results/<phase>_<exp>/<run_id>/` contains config.yaml, episodes.csv, summary.json, env.txt, git_sha.txt>
- [ ] <test `tests/test_<module>.py` passes>
- [ ] <team page updated: status, handoff entry, faculty bullet with cited number>

## Faculty-report sentence

<!-- Template with placeholders, never numbers, e.g.
     "Completed T<ID>: <what> (`<value from results/<phase>_<exp>/<run_id>/summary.json>`)." -->
