"""Save TRS data to Excel using openpyxl."""

import os
import numpy as np
from openpyxl import Workbook


def save_trs(run_name, axes, freq06_all, TRS06_all, seismic, output_dir):
    """Save TRS vs RRS data to Excel file.

    Layout matches MATLAB baseline:
      Cols A-C: X Direction (Freq, RRS, TRS)
      Cols D-F: Y Direction
      Cols G-I: Z Direction
      Cols J:   (empty / D Direction if present)
      Col K:    Low resonance (row 3), Cutoff (row 4)
      Col L:    Text labels (rows 3, 4)
    """
    # Column mapping: axis -> starting column (0-indexed)
    axis_to_col = {'X': 0, 'Y': 3, 'Z': 6, 'D': 9}

    output_file = os.path.join(output_dir, f'{run_name}_Table_TRSvsRRS.xlsx')

    wb = Workbook()
    ws = wb.active

    # Direction labels for header row 1
    direction_labels = {'X': 'X Direction', 'Y': 'Y Direction',
                        'Z': 'Z Direction', 'D': 'D Direction'}

    # Write header row 1
    for axis in axes:
        col_start = axis_to_col.get(axis, 0)
        ws.cell(row=1, column=col_start + 1, value=direction_labels.get(axis))

    # Write header row 2
    for axis in axes:
        col_start = axis_to_col.get(axis, 0)
        ws.cell(row=2, column=col_start + 1, value='Freq.\n(Hz)')
        ws.cell(row=2, column=col_start + 2, value='RRS\n(g)')
        ws.cell(row=2, column=col_start + 3, value='TRS\n(g)')

    freq72 = seismic['freq72']

    for axis in axes:
        table_col = f'Table_{axis}'
        if table_col not in freq06_all:
            continue

        current_freq06 = freq06_all[table_col]
        current_TRS06 = TRS06_all[table_col]

        # Get RRS at the 1/6 octave frequencies
        if axis in ('X', 'Y', 'D'):
            RRS_full = seismic['RRS_h']
        else:
            RRS_full = seismic['RRS_v']

        # Match frequencies
        current_RRS = np.interp(current_freq06, freq72, RRS_full)

        # Filter: only include frequencies > 1.0 Hz
        valid = current_freq06 > 1.0
        current_freq06 = current_freq06[valid]
        current_RRS = current_RRS[valid]
        current_TRS06 = current_TRS06[valid]

        # Round to 2 decimal places
        current_freq06 = np.round(current_freq06, 2)
        current_RRS = np.round(current_RRS, 2)
        current_TRS06 = np.round(current_TRS06, 2)

        # Write to Excel
        col_start = axis_to_col.get(axis, 0)
        row_start = 3

        for i in range(len(current_freq06)):
            ws.cell(row=row_start + i, column=col_start + 1,
                    value=float(current_freq06[i]))
            ws.cell(row=row_start + i, column=col_start + 2,
                    value=float(current_RRS[i]))
            ws.cell(row=row_start + i, column=col_start + 3,
                    value=float(current_TRS06[i]))

    # Write low resonance and cutoff annotations (K/L columns, matching baseline)
    ws.cell(row=3, column=11, value=seismic['lowResonance'])
    ws.cell(row=3, column=12, value='<- Lowest Resonance')
    ws.cell(row=4, column=11, value=seismic['lowCutoff'])
    ws.cell(row=4, column=12, value='<- Cuttoff Frequency')

    os.makedirs(output_dir, exist_ok=True)
    wb.save(output_file)
    print(f'TRS data saved to {output_file}')
