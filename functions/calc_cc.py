"""Cross-correlation calculation for statistical independence."""

import numpy as np
from scipy.signal import correlate, correlation_lags


def calc_cc(table_data, dt):
    """Calculate cross-correlation between table axes.

    Parameters
    ----------
    table_data : dict
        Keys like 'Table_X', 'Table_Y', 'Table_Z' with acceleration arrays.
    dt : float
        Time step in seconds.

    Returns
    -------
    dict with keys:
        cc_factor : float
        max_cc : float
        pairs : list of dicts with 'axes', 'corr', 'lag_time'
    """
    available_axes = []
    for axis in ['X', 'Y', 'Z']:
        key = f'Table_{axis}'
        if key in table_data:
            available_axes.append(axis)

    pairs = []
    max_cc_values = []

    for i in range(len(available_axes)):
        for j in range(i + 1, len(available_axes)):
            axis1 = available_axes[i]
            axis2 = available_axes[j]
            sig1 = table_data[f'Table_{axis1}']
            sig2 = table_data[f'Table_{axis2}']

            xc = correlate(sig1, sig2, mode='full')
            # Normalize: divide by N * std1 * std2
            n = len(sig1)
            xc = xc / (np.std(sig1) * np.std(sig2) * n)

            lags = correlation_lags(n, len(sig2), mode='full')
            lag_time = lags * dt

            max_abs = np.max(np.abs(xc))
            max_cc_values.append(max_abs)

            pairs.append({
                'axes': f'{axis1} vs. {axis2}',
                'corr': xc,
                'lag_time': lag_time,
            })

    overall_max = max(max_cc_values) if max_cc_values else 0
    cc_factor = 0.3 / overall_max if overall_max > 0 else float('inf')

    print(f'CC factor: {cc_factor:.2f}')
    print(f'Maximum correlation: {overall_max:.2f}')

    return {
        'cc_factor': cc_factor,
        'max_cc': overall_max,
        'pairs': pairs,
    }
