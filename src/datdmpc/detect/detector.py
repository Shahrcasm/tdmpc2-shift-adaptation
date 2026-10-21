"""Calibrated online shift detector (EWMA / CUSUM). Owner: M3 · Task: T302 (stub created in T001).

Calibrated only on nominal calibration seeds (1000-1099), disjoint from test seeds; thresholds
for H4 are pre-registered in docs/PROJECT_PLAN.md before T303 runs.
"""

from __future__ import annotations


class Detector:
    def __init__(self, config):
        raise NotImplementedError("datdmpc.detect.detector.Detector - task T302 (owner M3)")

    def calibrate(self, nominal_signals):
        raise NotImplementedError("datdmpc.detect.detector.Detector.calibrate - task T302 (owner M3)")

    def update(self, signals) -> bool:
        raise NotImplementedError("datdmpc.detect.detector.Detector.update - task T302 (owner M3)")
