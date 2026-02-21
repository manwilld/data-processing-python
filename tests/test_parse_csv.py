"""Tests for parse_csv module."""

import os
import tempfile
import numpy as np
import pandas as pd
import pytest
from functions.parse_csv import parse_seismic_csv, parse_resonance_csv


def test_parse_seismic_csv_basic():
    """Test basic seismic CSV parsing."""
    # Create a temporary CSV
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write('"Time (ms)","Control1 (G)","Ch1 (G)","Ch2 (G)"\n')
        for i in range(100):
            t = i * 10.0  # 10ms intervals
            f.write(f'{t},{np.sin(t/100):.6f},{np.cos(t/100):.6f},{0.5:.6f}\n')
        tmp_path = f.name

    try:
        column_mapping = {
            'Table_X': 'Ch1 (G)',
            'Sensor_1': 'Ch2 (G)',
        }
        result = parse_seismic_csv(tmp_path, column_mapping, time_unit='ms')

        assert 'Time' in result.columns
        assert 'Table_X' in result.columns
        assert 'Sensor_1' in result.columns
        # Time should start at 0 (in seconds)
        assert abs(result['Time'].iloc[0]) < 1e-10
        # Time should be in seconds
        assert result['Time'].iloc[1] < 0.02  # 10ms = 0.01s
    finally:
        os.unlink(tmp_path)


def test_parse_seismic_csv_trim():
    """Test trimming by start time and duration."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write('"Time (ms)","Ch1 (G)"\n')
        for i in range(1000):
            t = -100 + i * 1.0  # 1ms intervals, starting at -100ms
            f.write(f'{t},{np.sin(t/100):.6f}\n')
        tmp_path = f.name

    try:
        result = parse_seismic_csv(
            tmp_path, {'Accel': 'Ch1 (G)'},
            time_unit='ms', trim_start=0.0, duration=0.5
        )
        # Time should start at 0
        assert abs(result['Time'].iloc[0]) < 1e-10
        # Duration should be <= 0.5s
        assert result['Time'].iloc[-1] <= 0.5 + 1e-6
    finally:
        os.unlink(tmp_path)


def test_parse_resonance_csv_basic():
    """Test basic resonance CSV parsing."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write('"Frequency (Hz)","Control1 (G)","Ch1 (G)","Ch2 (G)"\n')
        for i in range(100):
            freq = 1.0 + i * 0.5
            f.write(f'{freq},{0.1:.6f},{0.2:.6f},{0.15:.6f}\n')
        tmp_path = f.name

    try:
        column_mapping = {
            'Table_X': 'Ch1 (G)',
            'Sensor_1': 'Ch2 (G)',
        }
        result = parse_resonance_csv(tmp_path, column_mapping, high_cutoff=35.0)

        assert 'Frequency' in result.columns
        assert 'Table_X' in result.columns
        assert result['Frequency'].max() <= 35.0
    finally:
        os.unlink(tmp_path)
