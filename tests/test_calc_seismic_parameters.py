"""Tests for calc_seismic_parameters module."""

import numpy as np
import pytest
from functions.calc_seismic_parameters import (
    calc_frequency, calc_rrs, calc_seismic_parameters,
)


def test_calc_frequency_basic():
    """Frequency array should start at 0.1 Hz and increase geometrically."""
    freq = calc_frequency(0.1, 38.0, 1/72)
    assert freq[0] == 0.1
    assert freq[-1] <= 38.0
    # Check geometric spacing: ratio between consecutive should be 2^(1/72)
    ratio = freq[1] / freq[0]
    expected_ratio = 2 ** (1/72)
    assert abs(ratio - expected_ratio) < 1e-10


def test_calc_frequency_length():
    """Should produce expected number of frequency points."""
    freq = calc_frequency()
    # From 0.1 to 38 Hz at 1/72 octave: log2(38/0.1) * 72 ≈ 612
    assert len(freq) > 600
    assert len(freq) < 650


def test_calc_rrs_shape():
    """RRS should have same length as frequency array."""
    freq = calc_frequency()
    rrs = calc_rrs(freq, 3.2, 1.08)
    assert len(rrs) == len(freq)


def test_calc_rrs_frequency_ranges():
    """RRS should follow AC156 piecewise definition."""
    freq = np.array([0.5, 1.0, 1.3, 5.0, 8.3, 15.0, 33.3, 35.0])
    Aflx = 3.2
    Arig = 1.08
    rrs = calc_rrs(freq, Aflx, Arig)

    # Below 1.3 Hz: increasing
    assert rrs[0] < rrs[1] < rrs[2]
    # At 1.3 to 8.3 Hz: constant = Aflx
    assert abs(rrs[2] - Aflx) < 0.01
    assert abs(rrs[3] - Aflx) < 0.01
    assert abs(rrs[4] - Aflx) < 0.01
    # 8.3 to 33.3 Hz: decreasing
    assert rrs[5] < Aflx
    assert rrs[5] > Arig
    # At 33.3 Hz: should be near Arig
    assert abs(rrs[6] - Arig) < 0.01
    # Above 33.3 Hz: constant = Arig
    assert abs(rrs[7] - Arig) < 0.01


def test_calc_seismic_parameters_asce7_22():
    """Test ASCE 7-22 parameter calculation matching WCC Booster example."""
    config = {
        'Sds1': 2.00,
        'z_h1': 1.0,
        'Sds2': 2.50,
        'z_h2': 0.0,
        'low_resonance': 5.0,
        'seismic_version': 'ASCE7-22',
    }
    result = calc_seismic_parameters(config)

    # Verify key values
    assert result['Aflx_h'] == 3.2  # min(1.6*2.0, 2.0*3.5/1.3) = min(3.2, 5.38) = 3.2
    assert result['lowCutoff'] == 3.5
    assert result['highCutoff'] == 33.3

    # Vertical
    assert result['Aflx_v'] == round(0.67 * 2.50, 2)  # max(1.34, 1.675) = 1.68
    assert result['Arig_v'] == round(0.27 * 2.50, 2)   # max(0.54, 0.675) = 0.68

    # 90% values
    assert result['Arig_h90'] == round(0.9 * result['Arig_h'], 2)
    assert result['Arig_v90'] == round(0.9 * result['Arig_v'], 2)

    # freq72 and RRS should exist
    assert len(result['freq72']) > 600
    assert len(result['RRS_h']) == len(result['freq72'])
    assert len(result['RRS_v']) == len(result['freq72'])


def test_calc_seismic_parameters_asce7_16():
    """Test ASCE 7-16 parameter calculation."""
    config = {
        'Sds1': 1.26,
        'z_h1': 1.0,
        'low_resonance': 5.0,
        'seismic_version': 'ASCE7-16',
    }
    result = calc_seismic_parameters(config)

    # ASCE 7-16: Aflx_h = min(1.6*1.26, 1.26*(1+2*1)) = min(2.016, 3.78) = 2.02
    assert result['Aflx_h'] == round(min(1.6 * 1.26, 1.26 * (1 + 2 * 1.0)), 2)
    # Arig_h = 0.4 * 1.26 * (1 + 2*1) = 1.512
    assert result['Arig_h'] == round(0.4 * 1.26 * (1 + 2 * 1.0), 2)
