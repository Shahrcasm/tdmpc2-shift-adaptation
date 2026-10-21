---
name: Bug
about: Something fails or gives a wrong result (install, tests, smoke test, scripts, Colab runs)
title: "Bug: "
labels: bug
assignees: ''
---

<!--
Title: "Bug: <short description>", e.g. "Bug: smoke_test.py --mode tiny fails on Windows with ImportError".
The owner of the affected file fixes it (ownership table: AGENTS.md §2). Do not edit files you do not own,
and never edit third_party/ (workarounds go into the owner's module by subclassing or wrapping).
Do not paste tokens, .env contents, or Drive paths containing personal emails. Do not write GitHub handles.
-->

## Reporter and task

- **Reported by:** <!-- M1 (Md. Shahriar Rakib Rabbi) / M2 (Md. Ishtiak Ahmed Moyen) / M3 (Md. Abdullah Talha) -->
- **Blocks task:** T<ID>  <!-- or "none" -->

## Affected file and owner

- **File(s):** `<path>`  <!-- e.g. src/datdmpc/eval/harness.py -->
- **Owner (from AGENTS.md §2):** <!-- M1 / M2 / M3; "upstream (third_party/tdmpc2, read-only)" if the cause is upstream -->

## Environment

<!-- Copy from the run's env.txt if a run folder exists (results/<phase>_<exp>/<run_id>/env.txt).
     Otherwise collect it, in PowerShell inside `conda activate datdmpc` (on Colab prefix the commands with "!"):
       python --version
       pip show torch mujoco dm-control numpy
       git rev-parse --short HEAD
       git branch --show-current
     Windows version: run `winver` (or `Get-ComputerInfo -Property OsName, OsVersion, OsBuildNumber`). -->

| Item | Value |
|---|---|
| Tier | <!-- T0 laptop / T1 Colab / T1b Kaggle / CI (windows-latest or ubuntu-latest) --> |
| OS and version | <!-- e.g. Windows 11 + winver build, or Colab (Linux) --> |
| Device | <!-- cpu / cuda --> |
| Python | |
| torch | |
| mujoco | |
| dm_control | |
| numpy | |
| Git commit (`git rev-parse --short HEAD`) | |
| Branch | |

## Command

<!-- The exact command, run from the repository root (C:\code\tdmpc2-shift-adaptation on laptops,
     /content/tdmpc2-shift-adaptation on Colab). -->

```powershell
<command>
```

## Expected behaviour

<!-- What should have happened (cite the task card, a test, or a results/ file if relevant). -->

## Actual behaviour

<!-- What happened instead. Numbers only if copied from a file, cited by path. -->

## Traceback

```text
<full traceback or error output>
```

## Minimal reproduction

<!-- The smallest command that still fails. Try the tiny random model first, which needs no checkpoint:
       python scripts/smoke_test.py --mode tiny --seed 0
     State whether it also fails in CI, on Colab, or on another member's laptop. -->

## Affected results

<!-- List any committed results/ folders that may be invalid because of this bug, or "none".
     Do not delete or overwrite them; the owner re-runs and documents the fix in their handoff log. -->
