"""Tests for calc_trs module."""

import numpy as np
import pytest
from functions.calc_trs import calc_trs


def test_calc_trs_basic():
    """TRS of a pure sine wave should peak near the sine frequency."""
    freq = 10.0  # Hz
    duration = 5.0
    dt = 0.001
    time = np.arange(0, duration, dt)
    accel = np.sin(2 * np.pi * freq * time)

    freq72 = np.array([5.0, 8.0, 10.0, 12.0, 15.0, 20.0])
    damping = 0.05

    trs = calc_trs(time, accel, freq72, damping)

    assert trs.shape == (6,)
    # Peak should be at or near 10 Hz (index 2)
    peak_idx = np.argmax(trs)
    assert peak_idx == 2, f"Expected peak at 10 Hz, got peak at {freq72[peak_idx]} Hz"
    # TRS at resonance should be amplified (Q factor ~ 1/(2*damping) = 10)
    assert trs[2] > 5.0, f"Expected amplification at resonance, got {trs[2]}"


def test_calc_trs_zeros():
    """TRS of zero signal should be all zeros."""
    time = np.arange(0, 1.0, 0.001)
    accel = np.zeros_like(time)
    freq72 = np.array([1.0, 5.0, 10.0])
    damping = 0.05

    trs = calc_trs(time, accel, freq72, damping)
    np.testing.assert_array_equal(trs, 0.0)


def test_calc_trs_output_shape():
    """TRS output should match freq72 length."""
    time = np.arange(0, 2.0, 0.001)
    accel = np.random.randn(len(time)) * 0.1
    freq72 = np.logspace(np.log10(1), np.log10(33), 50)
    damping = 0.05

    trs = calc_trs(time, accel, freq72, damping)
    assert len(trs) == len(freq72)
    assert np.all(trs >= 0)
