"""Process a complete seismic run: filter, TRS, plots."""

import numpy as np
from .filter_data import filter_th
from .calc_trs import calc_trs
from .optimize_trs import optimize_trs
from .plot_th import plot_th
from .plot_trs import plot_trs
from .plot_trs_all import plot_trs_all
from .plot_cc import plot_cc
from .plot_ch import plot_ch
from .calc_cc import calc_cc
from .calc_ch import calc_ch
from .save_plot import save_plot
from .save_trs import save_trs


def process_seismic_run(seismic, config, seismic_data, output_dir, script_dir=None):
    """Process seismic run: filter, compute TRS, generate all plots.

    Parameters
    ----------
    seismic : dict
        Output from calc_seismic_parameters.
    config : dict
        Full config from YAML.
    seismic_data : pandas.DataFrame
        Trimmed seismic data (Time + accel columns).
    output_dir : str
        Directory for output plots.
    """
    run_name = config['run_name']
    axes = config['axes']
    damping = config['damping']
    window_size = config.get('window_size', 1.25)
    filters_config = config.get('filters', {})
    accels_config = config.get('accels', [])
    plot_options = config.get('plot', {})

    freq72 = seismic['freq72']
    RRS_h = seismic['RRS_h']
    RRS_v = seismic['RRS_v']
    low_cutoff = seismic['lowCutoff']
    high_cutoff = seismic['highCutoff']

    time = seismic_data['Time'].values
    dt = time[1] - time[0]
    sample_rate = 1.0 / dt

    plot_number = 1

    # Apply filters and store filtered data
    filtered_data = {'Time': time}
    for col in seismic_data.columns:
        if col == 'Time':
            continue
        accel = seismic_data[col].values
        filt = filters_config.get(col)
        if filt is not None:
            accel = filter_th(accel, sample_rate, filt['order'], filt['cutoff_hz'])
        filtered_data[col] = accel

    # Storage for TRS results per column
    freq06_all = {}
    TRS06_all = {}

    # Process Table axes first, then accels
    all_accel_names = ['Table'] + [a['name'] for a in accels_config]

    for accel_label in all_accel_names:
        is_table = accel_label == 'Table'

        for axis in axes:
            if is_table:
                col_name = f'Table_{axis}'
            else:
                col_name = f'{accel_label}_{axis}'

            if col_name not in filtered_data:
                print(f'Warning: column {col_name} not found, skipping')
                continue

            accel = filtered_data[col_name]

            # Determine Arig_90 for time history plot
            if axis == 'Z':
                Arig_90 = seismic['Arig_v90']
                RRS = RRS_v
                Aflx = seismic['Aflx_v']
                Arig = seismic['Arig_v']
            else:
                Arig_90 = seismic['Arig_h90']
                RRS = RRS_h
                Aflx = seismic['Aflx_h']
                Arig = seismic['Arig_h']

            # Time history plot
            fig = plot_th(run_name, col_name, time, accel, Arig_90, plot_options)
            plot_number = save_plot(fig, f'TH_{col_name}', run_name,
                                   plot_number, output_dir)

            # TRS calculation
            TRS72 = calc_trs(time, accel, freq72, damping)
            freq06, TRS06 = optimize_trs(col_name, freq72, TRS72, RRS,
                                         low_cutoff, high_cutoff)

            freq06_all[col_name] = freq06
            TRS06_all[col_name] = TRS06

            # TRS plot
            fig = plot_trs(run_name, col_name, freq72, RRS, Aflx, Arig,
                           freq06, TRS06, damping, low_cutoff, plot_options)
            plot_number = save_plot(fig, f'TRS_{col_name}', run_name,
                                   plot_number, output_dir)

    # TRS all-axes overlay plots
    for accel_label in all_accel_names:
        is_table = accel_label == 'Table'
        accel_name_full = accel_label

        freq06_per_axis = {}
        TRS06_per_axis = {}
        for axis in axes:
            if is_table:
                col_name = f'Table_{axis}'
            else:
                col_name = f'{accel_label}_{axis}'
            if col_name in freq06_all:
                freq06_per_axis[axis] = freq06_all[col_name]
                TRS06_per_axis[axis] = TRS06_all[col_name]

        if freq06_per_axis:
            fig = plot_trs_all(run_name, accel_name_full, axes, freq72,
                               RRS_h, RRS_v,
                               seismic['Aflx_h'], seismic['Aflx_v'],
                               seismic['Arig_h'], seismic['Arig_v'],
                               damping, low_cutoff,
                               freq06_per_axis, TRS06_per_axis, plot_options)
            plot_number = save_plot(fig, f'TRSvsRRS_All_{accel_name_full}',
                                   run_name, plot_number, output_dir)

    # Save TRS to Excel (in script_dir to match MATLAB, falls back to output_dir)
    excel_dir = script_dir if script_dir else output_dir
    save_trs(run_name, axes, freq06_all, TRS06_all, seismic, excel_dir)

    # Cross-correlation
    table_data = {k: v for k, v in filtered_data.items() if k.startswith('Table_')}
    cc_result = calc_cc(table_data, dt)
    fig = plot_cc(cc_result, run_name, plot_options)
    plot_number = save_plot(fig, 'CC', run_name, plot_number, output_dir)

    # Coherence
    ch_result = calc_ch(table_data, sample_rate, window_size)
    fig = plot_ch(ch_result, run_name, plot_options)
    plot_number = save_plot(fig, 'CH', run_name, plot_number, output_dir)

    print(f'\nSeismic processing complete. {plot_number - 1} plots saved to {output_dir}')
