"""Magnitude Squared Coherence calculation."""

import numpy as np
from scipy.signal import coherence


def calc_ch(table_data, sample_rate, window_size):
    """Calculate magnitude squared coherence between table axes.

    Parameters
    ----------
    table_data : dict
        Keys like 'Table_X', 'Table_Y', 'Table_Z' with acceleration arrays.
    sample_rate : float
        Sampling rate in Hz.
    window_size : float
        Window size in seconds for coherence calculation.

    Returns
    -------
    dict with keys:
        ch_factor : float
        max_ch : float
        pairs : list of dicts with 'axes', 'coherence', 'frequencies'
    """
    sr = int(round(sample_rate))

    # Frequency array from 1.3 to 33.3 Hz at 1/72 octave
    fch = [1.3]
    j = 1
    while True:
        next_f = 1.3 * (2.0 ** (j * (1.0 / 72.0)))
        if next_f > 33.3:
            break
        fch.append(next_f)
        j += 1
    fch = np.array(fch)

    # Window and overlap
    ch_window = int(round(sr * window_size))
    ch_overlap = ch_window // 2

    available_axes = []
    for axis in ['X', 'Y', 'Z']:
        key = f'Table_{axis}'
        if key in table_data:
            available_axes.append(axis)

    pairs = []
    max_ch_values = []

    for i in range(len(available_axes)):
        for j_idx in range(i + 1, len(available_axes)):
            axis1 = available_axes[i]
            axis2 = available_axes[j_idx]
            sig1 = table_data[f'Table_{axis1}']
            sig2 = table_data[f'Table_{axis2}']

            # Trim first and last 5 seconds
            trim = 5 * sr
            if trim >= len(sig1) // 2:
                trim = 0
            sig1_trimmed = sig1[trim:len(sig1) - trim] if trim > 0 else sig1
            sig2_trimmed = sig2[trim:len(sig2) - trim] if trim > 0 else sig2

            f_out, coh = coherence(sig1_trimmed, sig2_trimmed,
                                   fs=sr, nperseg=ch_window,
                                   noverlap=ch_overlap)

            # Interpolate coherence at fch frequencies
            coh_at_fch = np.interp(fch, f_out, coh)

            max_coh = np.max(coh_at_fch)
            max_ch_values.append(max_coh)

            pairs.append({
                'axes': f'{axis1} vs. {axis2}',
                'coherence': coh_at_fch,
                'frequencies': fch,
            })

    overall_max = max(max_ch_values) if max_ch_values else 0
    ch_factor = 0.5 / overall_max if overall_max > 0 else float('inf')

    print(f'CH factor: {ch_factor:.2f}')
    print(f'Maximum coherence: {overall_max:.2f}')

    return {
        'ch_factor': ch_factor,
        'max_ch': overall_max,
        'pairs': pairs,
    }
