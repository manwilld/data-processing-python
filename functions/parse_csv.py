"""Parse multi-section raw CSV files from shake table controller."""

import pandas as pd
import numpy as np


def parse_seismic_csv(filepath, column_mapping, time_unit='ms',
                      trim_start=None, duration=None):
    """Parse raw seismic CSV and return clean DataFrame.

    The raw CSV has multiple sections. We find the time-domain section
    by scanning for a row where the first column header contains 'Time'.

    Parameters
    ----------
    filepath : str
        Path to raw seismic CSV.
    column_mapping : dict
        Maps output column names to raw CSV column names.
        e.g. {'Table_X': 'Ch1 (G)', 'UUT_1_Controller_X': 'Ch4 (G)'}
    time_unit : str
        'ms' or 's' for the time column in the raw CSV.
    trim_start : float or None
        Start time in seconds. Data before this is discarded.
    duration : float or None
        Duration in seconds to keep after trim_start.

    Returns
    -------
    pandas.DataFrame
        Columns: Time (seconds, starting at 0) + mapped column names.
    """
    # Read full CSV to find the time-domain header
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        first_line = f.readline()

    # Parse header to find column positions
    header_cols = [h.strip().strip('"') for h in first_line.split(',')]

    # Find the 'Time' column (should be first)
    time_col_name = None
    for col in header_cols:
        if 'Time' in col:
            time_col_name = col
            break

    if time_col_name is None:
        raise ValueError(f"Could not find 'Time' column in {filepath}")

    # Read the CSV with pandas
    df = pd.read_csv(filepath, encoding='utf-8-sig')

    # Clean column names (strip whitespace and quotes)
    df.columns = [c.strip().strip('"') for c in df.columns]

    # Extract time column
    time_raw = df[time_col_name].values.astype(float)

    # Convert time to seconds
    if time_unit == 'ms':
        time_seconds = time_raw / 1000.0
    else:
        time_seconds = time_raw.copy()

    # Build output DataFrame
    result = pd.DataFrame()
    result['Time'] = time_seconds

    for output_name, raw_name in column_mapping.items():
        raw_name_clean = raw_name.strip()
        if raw_name_clean not in df.columns:
            # Try to find a close match
            matches = [c for c in df.columns if raw_name_clean in c]
            if matches:
                raw_name_clean = matches[0]
            else:
                raise ValueError(
                    f"Column '{raw_name}' not found in CSV. "
                    f"Available: {list(df.columns[:40])}"
                )
        result[output_name] = df[raw_name_clean].values.astype(float)

    # Trim to start time
    if trim_start is not None:
        mask = result['Time'] >= trim_start
        result = result[mask].reset_index(drop=True)

    # Reset time to start at 0
    if len(result) > 0:
        t0 = result['Time'].iloc[0]
        result['Time'] = result['Time'] - t0

    # Normalize time to uniform spacing using integer sample rate
    if len(result) > 1:
        dt_raw = result['Time'].iloc[1] - result['Time'].iloc[0]
        sample_rate = round(1.0 / dt_raw)
        dt = 1.0 / sample_rate
        result['Time'] = np.arange(len(result)) * dt

    # Trim to duration (use sample count to avoid floating-point fence-post)
    if duration is not None and len(result) > 1:
        dt = result['Time'].iloc[1] - result['Time'].iloc[0]
        n_pts = int(round(duration / dt)) + 1
        result = result.iloc[:min(n_pts, len(result))].reset_index(drop=True)
    elif duration is not None and len(result) > 0:
        mask = result['Time'] <= duration
        result = result[mask].reset_index(drop=True)

    return result


def parse_resonance_csv(filepath, column_mapping, high_cutoff=None):
    """Parse resonance CSV (frequency-domain, plot_only mode).

    The first column is frequency (Hz). Just rename columns and
    optionally trim to high_cutoff.

    Parameters
    ----------
    filepath : str
        Path to resonance CSV.
    column_mapping : dict
        Maps output column names to raw CSV column names.
    high_cutoff : float or None
        Maximum frequency to keep.

    Returns
    -------
    pandas.DataFrame
        Columns: Frequency + mapped column names.
    """
    df = pd.read_csv(filepath, encoding='utf-8-sig')
    df.columns = [c.strip().strip('"') for c in df.columns]

    # Find frequency column
    freq_col = None
    for col in df.columns:
        if 'Frequency' in col or 'freq' in col.lower():
            freq_col = col
            break

    if freq_col is None:
        raise ValueError(f"Could not find 'Frequency' column in {filepath}")

    result = pd.DataFrame()
    result['Frequency'] = df[freq_col].values.astype(float)

    for output_name, raw_name in column_mapping.items():
        raw_name_clean = raw_name.strip()
        if raw_name_clean not in df.columns:
            matches = [c for c in df.columns if raw_name_clean in c]
            if matches:
                raw_name_clean = matches[0]
            else:
                raise ValueError(
                    f"Column '{raw_name}' not found in CSV. "
                    f"Available: {list(df.columns[:40])}"
                )
        result[output_name] = df[raw_name_clean].values.astype(float)

    # Trim to high_cutoff
    if high_cutoff is not None:
        result = result[result['Frequency'] <= high_cutoff].reset_index(drop=True)

    return result
