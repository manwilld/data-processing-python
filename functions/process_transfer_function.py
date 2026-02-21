"""Process transfer function for resonance data."""

import numpy as np
from scipy.signal import csd, welch


def process_transfer_function(run_axes, accels, trimmed_data):
    """Compute transfer functions between table and UUT accelerometers.

    Parameters
    ----------
    run_axes : list of str
        e.g. ['X', 'Y', 'Z']
    accels : list of dict
        Each dict has 'name', 'uut' keys.
    trimmed_data : pandas.DataFrame
        Columns: Time, Table_X, Table_Y, ..., accel columns.

    Returns
    -------
    pandas.DataFrame
        Columns: Frequency, Table_X, ..., UUT_accel_axis columns.
    """
    import pandas as pd

    time = trimmed_data['Time'].values
    Fs = 1.0 / np.mean(np.diff(time))

    results = {}

    for axis in run_axes:
        table_col = f'Table_{axis}'
        if table_col not in trimmed_data.columns:
            print(f'Warning: {table_col} not in data, skipping axis {axis}')
            continue

        table_accel = trimmed_data[table_col].values

        for accel_info in accels:
            accel_name = accel_info['name']
            uut = accel_info['uut']
            accel_col = f'{accel_name}_{axis}'
            uut_accel_col = f'{uut}_{accel_name}_{axis}'

            # Try different column name patterns
            if uut_accel_col in trimmed_data.columns:
                accel_data = trimmed_data[uut_accel_col].values
            elif accel_col in trimmed_data.columns:
                accel_data = trimmed_data[accel_col].values
            else:
                print(f'Warning: {uut_accel_col} not found, skipping')
                continue

            # Transfer function via CSD / PSD
            f, Pxy = csd(table_accel, accel_data, fs=Fs)
            f, Pxx = welch(table_accel, fs=Fs)
            Txy = np.abs(Pxy / Pxx)

            if 'Frequency' not in results:
                results['Frequency'] = f
            results[uut_accel_col] = Txy

    # Add Table columns as ones
    df = pd.DataFrame(results)
    for axis in run_axes:
        table_col = f'Table_{axis}'
        if table_col not in df.columns:
            df[table_col] = 1.0

    return df
