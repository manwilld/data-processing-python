"""Tests for optimize_trs module."""

import numpy as np
import pytest
from functions.optimize_trs import analyze_set, optimize_trs


def test_analyze_set_basic():
    """TRS factor should be positive for valid inputs."""
    freq = np.array([1.0, 2.0, 5.0, 10.0, 20.0, 33.3])
    TRS = np.array([1.0, 3.5, 3.5, 3.5, 2.0, 1.2])
    RRS = np.array([0.5, 3.2, 3.2, 3.2, 2.0, 1.0])
    factor = analyze_set(freq, TRS, RRS, 1.3, 33.3)
    assert factor > 0


def test_optimize_trs_table():
    """Table accels should use optimization (12 starting indices)."""
    np.random.seed(42)
    freq72 = 0.1 * (2 ** (np.arange(620) / 72))
    TRS72 = np.random.uniform(1.0, 5.0, len(freq72))
    RRS = np.full(len(freq72), 3.0)

    freq06, TRS06 = optimize_trs('Table_X', freq72, TRS72, RRS, 1.3, 33.3)

    # Should subsample at 1/6 octave (every 12th point)
    assert len(freq06) == len(freq72[0::12])
    assert len(TRS06) == len(freq06)


def test_optimize_trs_non_table():
    """Non-table accels should always use starting index 0."""
    freq72 = 0.1 * (2 ** (np.arange(620) / 72))
    TRS72 = np.ones(len(freq72))
    RRS = np.ones(len(freq72))

    freq06, TRS06 = optimize_trs('UUT_1_Controller_X', freq72, TRS72, RRS, 1.3, 33.3)

    # Should use starting index 0
    np.testing.assert_array_equal(freq06, freq72[0::12])
    np.testing.assert_array_equal(TRS06, TRS72[0::12])
