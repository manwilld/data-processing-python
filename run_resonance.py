#!/usr/bin/env python3
"""CLI: Process resonance test data.

Usage:
    python run_resonance.py --config path/to/resonance_config.yaml
"""

import argparse
import os
import numpy as np
import yaml
import pandas as pd

from functions.parse_csv import parse_resonance_csv
from functions.plot_transfer import plot_transfer
from functions.save_plot import save_plot
from functions.plot_style import setup_plot_style


def main():
    parser = argparse.ArgumentParser(description='Process resonance test data')
    parser.add_argument('--config', required=True, help='Path to resonance config YAML')
    args = parser.parse_args()

    # Load config
    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)

    # Configure plot style (font fallback, rcParams)
    setup_plot_style(config.get('plot', {}).get('font_name'))
    print(f"Processing resonance run: {config['run_name']}")
    print(f"Config: {args.config}")

    run_name = config['run_name']
    axes = config['axes']
    high_cutoff = config.get('high_cutoff', 35.1)
    plot_only = config.get('plot_only', True)
    accels_config = config.get('accels', [])
    column_mapping = config.get('column_mapping', {})
    natural_frequencies = config.get('natural_frequencies', {})
    output_subdirs = config.get('output_subdirs', {})
    plot_options = config.get('plot', {})
    script_dir = config.get('script_dir', os.path.dirname(args.config))

    if plot_only:
        # Parse each axis file and combine into single DataFrame
        all_data = {}
        for axis in axes:
            filepath = config['files'][axis]
            axis_mapping = column_mapping.get(axis, {})

            axis_df = parse_resonance_csv(
                filepath=filepath,
                column_mapping=axis_mapping,
                high_cutoff=high_cutoff,
            )

            if 'Frequency' not in all_data:
                all_data['Frequency'] = axis_df['Frequency'].values

            for col in axis_df.columns:
                if col != 'Frequency':
                    all_data[col] = axis_df[col].values

        resonance_data = pd.DataFrame(all_data)
    else:
        # Process transfer function from time-domain data
        from functions.parse_csv import parse_seismic_csv
        from functions.process_transfer_function import process_transfer_function

        # For non-plot-only mode, parse time-domain CSV and compute transfer functions
        trimmed_data = parse_seismic_csv(
            filepath=config['files'],
            column_mapping=column_mapping,
            time_unit=config.get('time_unit', 'ms'),
            duration=config.get('duration'),
        )
        resonance_data = process_transfer_function(axes, accels_config, trimmed_data)

    # Save trimmed resonance data
    trimmed_csv = os.path.join(script_dir, f'{run_name}_resonance_trimmed.csv')
    resonance_data.to_csv(trimmed_csv, index=False)
    print(f'Resonance data saved to {trimmed_csv}')

    # Get unique UUTs
    uuts = list(dict.fromkeys(a['uut'] for a in accels_config))

    # Global plot counter across all UUTs (matches MATLAB behavior)
    plot_number = 1

    # Generate transfer function plots for each UUT
    for uut in uuts:
        uut_output_subdir = output_subdirs.get(uut, f'{uut}_Plots_Resonance')
        uut_output_dir = os.path.join(script_dir, uut_output_subdir)
        os.makedirs(uut_output_dir, exist_ok=True)

        uut_accels = [a for a in accels_config if a['uut'] == uut]

        for accel_info in uut_accels:
            accel_name = accel_info['name']
            uut_map_x = accel_info.get('uut_map_x', 'SS')

            for axis in axes:
                # Determine UUT axis label based on orientation mapping
                if uut_map_x == 'FB':
                    axis_map = {'X': 'FB', 'Y': 'SS', 'Z': 'V'}
                else:  # SS
                    axis_map = {'X': 'SS', 'Y': 'FB', 'Z': 'V'}
                axis_uut = axis_map.get(axis, axis)

                # Get column names
                uut_accel_col = f'{uut}_{accel_name}_{axis}'
                table_col = f'Table_{axis}'

                if uut_accel_col not in resonance_data.columns:
                    print(f'Warning: {uut_accel_col} not found, skipping')
                    continue
                if table_col not in resonance_data.columns:
                    print(f'Warning: {table_col} not found, skipping')
                    continue

                frequency = resonance_data['Frequency'].values
                uut_data = resonance_data[uut_accel_col].values
                table_data = resonance_data[table_col].values

                # Compute transmissibility
                transfer_response = uut_data / table_data

                # Get natural frequency from config
                nat_freq_key = f'{accel_name}_{axis}'
                nat_freq = natural_frequencies.get(uut, {}).get(nat_freq_key, 33.3)

                fig = plot_transfer(
                    run_name, uut, accel_name, axis, axis_uut,
                    frequency, transfer_response, nat_freq, plot_options,
                )

                plot_name = f'Res_{accel_name}_{axis}_{axis_uut}'
                plot_number = save_plot(fig, plot_name, uut, plot_number,
                                        uut_output_dir)

    print('\nResonance processing complete!')


if __name__ == '__main__':
    main()
