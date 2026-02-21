"""TRS optimization - find best 1/6-octave starting index."""

import numpy as np


def analyze_set(freq, TRS, RRS, low_cutoff, high_cutoff):
    """Compute TRS factor for a given 1/6-octave set.

    Three-step factor computation:
    1. Normalize minimum dip to 0.9*RRS
    2. Handle consecutive dips below 1.0
    3. Handle >=3 dips in low/high frequency ranges
    """
    # Find indices for one point below and above the cutoffs
    below_idx = np.where(freq < low_cutoff)[0]
    above_idx = np.where(freq > high_cutoff)[0]

    valid = (freq >= low_cutoff) & (freq <= high_cutoff)
    if len(below_idx) > 0:
        valid[below_idx[-1]] = True
    if len(above_idx) > 0:
        valid[above_idx[0]] = True

    freq = freq[valid]
    TRS = TRS[valid]
    RRS = RRS[valid]

    # Factor 1: normalize minimum dip to 0.9*RRS
    dip_ratios = TRS / RRS
    TRS_factor1 = np.min(dip_ratios) / 0.9

    # Factor 2: consecutive dips below 1.0
    RRS1 = RRS * TRS_factor1
    dip_ratios1 = TRS / RRS1

    consecutive_factors = []
    for i in range(len(dip_ratios1) - 1):
        if dip_ratios1[i] < 1 and dip_ratios1[i + 1] < 1:
            consecutive_factors.append(max(dip_ratios1[i], dip_ratios1[i + 1]))

    TRS_factor2 = min(consecutive_factors) if consecutive_factors else 1.0

    # Factor 3: >=3 dips in frequency ranges split at 8.3 Hz
    RRS2 = RRS1 * TRS_factor2
    dip_ratios2 = TRS / RRS2

    is_low = freq <= 8.3
    is_high = freq > 8.3

    low_dips = dip_ratios2[is_low]
    high_dips = dip_ratios2[is_high]

    low_below_one = np.sort(low_dips[low_dips < 1])
    high_below_one = np.sort(high_dips[high_dips < 1])

    TRS_factor3 = 1.0
    if len(low_below_one) >= 3:
        TRS_factor3 = min(TRS_factor3, low_below_one[2])
    if len(high_below_one) >= 3:
        TRS_factor3 = min(TRS_factor3, high_below_one[2])

    return TRS_factor1 * TRS_factor2 * TRS_factor3


def optimize_trs(accel_name, freq72, TRS72, RRS, low_cutoff, high_cutoff):
    """Find optimal 1/6-octave TRS subsampling.

    For Table accels, tests 12 starting indices and picks the best.
    For non-Table accels, always uses index 0.

    Parameters
    ----------
    accel_name : str
        Name of the accelerometer (used to detect 'Table').
    freq72 : numpy.ndarray
        Frequency array at 1/72 octave.
    TRS72 : numpy.ndarray
        TRS at 1/72 octave.
    RRS : numpy.ndarray
        RRS at 1/72 octave.
    low_cutoff : float
        Lower frequency cutoff (Hz).
    high_cutoff : float
        Upper frequency cutoff (Hz).

    Returns
    -------
    tuple of (freq06, TRS06)
        Optimized 1/6-octave frequency and TRS arrays.
    """
    optimal_factor = 0
    optimal_index = 0

    if 'Table' in accel_name:
        for start_index in range(12):
            freq06 = freq72[start_index::12]
            TRS06 = TRS72[start_index::12]
            RRS06 = RRS[start_index::12]

            current_factor = analyze_set(freq06, TRS06, RRS06, low_cutoff, high_cutoff)
            if current_factor > optimal_factor:
                optimal_factor = current_factor
                optimal_index = start_index

        optimal_factor = round(optimal_factor, 2)
        print(f'TRS factor for {accel_name} = {optimal_factor:.2f}')
    else:
        optimal_index = 0

    freq06 = freq72[optimal_index::12]
    TRS06 = TRS72[optimal_index::12]

    return freq06, TRS06
