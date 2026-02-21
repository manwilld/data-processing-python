#!/usr/bin/env python3
"""CLI: Process seismic test data.

Usage:
    python run_seismic.py --config path/to/seismic_config.yaml
"""

import argparse
import os
import yaml

from functions.parse_csv import parse_seismic_csv
from functions.calc_seismic_parameters import calc_seismic_parameters
from functions.process_seismic_run import process_seismic_run


def main():
    parser = argparse.ArgumentParser(description='Process seismic test data')
    parser.add_argument('--config', required=True, help='Path to seismic config YAML')
    args = parser.parse_args()

    # Load config
    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)

    print(f"Processing seismic run: {config['run_name']}")
    print(f"Config: {args.config}")

    # Calculate seismic parameters
    seismic = calc_seismic_parameters(config)

    # Parse raw CSV
    seismic_data = parse_seismic_csv(
        filepath=config['seismic_file'],
        column_mapping=config['column_mapping'],
        time_unit=config.get('time_unit', 'ms'),
        trim_start=config.get('trim_start'),
        duration=config.get('duration'),
    )

    # Save trimmed CSV
    script_dir = config.get('script_dir', os.path.dirname(args.config))
    output_subdir = config.get('output_subdir', f"{config['run_name']} Plots_Seismic")
    output_dir = os.path.join(script_dir, output_subdir)
    os.makedirs(output_dir, exist_ok=True)

    trimmed_csv = os.path.join(script_dir, f"{config['run_name']}_trimmed.csv")
    seismic_data.to_csv(trimmed_csv, index=False)
    print(f'Trimmed data saved to {trimmed_csv}')

    # Process seismic run (filter, TRS, plots, Excel)
    process_seismic_run(seismic, config, seismic_data, output_dir)

    print('\nDone!')


if __name__ == '__main__':
    main()
