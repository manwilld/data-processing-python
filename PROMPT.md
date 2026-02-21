# Data Processing Python — Build Task

## Goal
Port the MATLAB seismic/resonance data processing pipeline to a fully headless Python library.
Replace all GUI interactions with YAML config files. Plots saved as SVG (vector) and PNG.

## Source Reference
- MATLAB source code: `/root/data-processing/` (read this for algorithms and plot styles)
- MATLAB library path: `/root/structural-calcs-python/` (Python lib already exists, for style reference)
- Example project: `/mnt/dropbox/_OpenClaw/data-processing-example/`
  - Input files: `Seismic_WCC_Booster_ETL.m`, `Resonance_WCC_Booster_ETL.m`, 3 resonance CSVs, 1 seismic CSV
  - Output files: numbered plots (PNG + SVG), trimmed CSVs, Excel TRS table
  - **Study these `.m` scripts to understand the config structure** — they define all parameters

## Repo Location
`/root/data-processing-python/`

## Completion Criteria
The task is DONE when all of the following are true:
1. `python run_resonance.py --config examples/WCC_Booster/resonance_config.yaml` runs without errors
2. `python run_seismic.py --config examples/WCC_Booster/seismic_config.yaml` runs without errors
3. Both produce output plots (SVG + PNG) and trimmed CSVs matching the example project structure
4. Seismic run produces the Excel TRS table
5. All unit tests pass: `python -m pytest tests/ -v`
6. `git add -A && git commit -m "..." && git push` succeeds

If you encounter an error, fix it and continue. Do not stop.
When done, run: `openclaw system event --text "Done: data-processing-python initial build complete" --mode now`

---

## Architecture

```
data-processing-python/
├── run_resonance.py          # CLI: python run_resonance.py --config path/to/config.yaml
├── run_seismic.py            # CLI: python run_seismic.py --config path/to/config.yaml
├── functions/
│   ├── __init__.py
│   ├── parse_csv.py          # Parse multi-section raw CSVs from shake table
│   ├── calc_seismic_parameters.py
│   ├── calc_trs.py           # Smallwood algorithm
│   ├── optimize_trs.py       # TRS vs RRS optimization (best 1/6-octave set)
│   ├── filter_data.py        # Butterworth lowpass + filtfilt
│   ├── calc_cc.py            # Cross-correlation (statistical independence)
│   ├── calc_ch.py            # Magnitude squared coherence
│   ├── process_seismic_run.py
│   ├── process_transfer_function.py
│   ├── plot_th.py            # Time history plot
│   ├── plot_trs.py           # TRS vs RRS plot (single accel)
│   ├── plot_trs_all.py       # TRS vs RRS all-axes overlay
│   ├── plot_transfer.py      # Transmissibility plot
│   ├── plot_cc.py            # Cross-correlation plot
│   ├── plot_ch.py            # Coherence plot
│   ├── save_trs.py           # Write TRS data to Excel via openpyxl
│   └── save_plot.py          # Save figure as both SVG and PNG with sequential numbering
├── examples/
│   └── WCC_Booster/
│       ├── seismic_config.yaml
│       └── resonance_config.yaml
└── tests/
    ├── test_calc_trs.py
    ├── test_optimize_trs.py
    ├── test_calc_seismic_parameters.py
    └── test_parse_csv.py
```

---

## Config File Schema

### seismic_config.yaml
```yaml
# Project info
run_name: "Run_1"
script_dir: "/mnt/dropbox/_OpenClaw/data-processing-example"
output_subdir: "Run_1 Plots_Seismic"

# Input files
seismic_file: "/mnt/dropbox/_OpenClaw/data-processing-example/Seismic_2026Jan05-1409-0001.csv"

# Seismic parameters (from ASCE 7)
seismic_version: "ASCE7-16"   # or "ASCE7-22"
Sds: 1.26
Ip: 1.0
ap: 2.5
Rp: 2.5
z_h: 1.0
Omega0: 2.5   # only needed for FpAFomega

# Run config
axes: ["X", "Y", "Z"]
time_unit: "ms"   # "ms" or "s"
duration: 30.0    # seconds of data to use
damping: 0.05
window_size: 1.25  # seconds, for coherence (CH) calc

# Trim: start time in seconds (from the raw time column after unit conversion)
trim_start: 5.0   # adjust per run

# Column mapping: maps output column names to raw CSV column names
# Raw CSV column names are what appear in the header row of the seismic CSV
# Time column is always first
column_mapping:
  Table_X: "Control1 (G)"
  Table_Y: "Control2 (G)"
  Table_Z: "Control3 (G)"
  UUT_1_Controller_X: "Ch1 (G)"
  UUT_1_Controller_Y: "Ch2 (G)"
  UUT_1_Controller_Z: "Ch3 (G)"
  UUT_1_Pump_X: "Ch4 (G)"
  UUT_1_Pump_Y: "Ch5 (G)"
  UUT_1_Pump_Z: "Ch6 (G)"
  UUT_2_Controller_X: "Ch7 (G)"
  UUT_2_Controller_Y: "Ch8 (G)"
  UUT_2_Controller_Z: "Ch9 (G)"
  UUT_2_Pump_X: "Ch10 (G)"
  UUT_2_Pump_Y: "Ch11 (G)"
  UUT_2_Pump_Z: "Ch12 (G)"

# Accelerometers and which UUT they belong to
# Each entry: accel_name (matches column_mapping prefix) -> UUT name
accels:
  - name: "UUT_1_Controller"
    uut: "UUT_1"
  - name: "UUT_1_Pump"
    uut: "UUT_1"
  - name: "UUT_2_Controller"
    uut: "UUT_2"
  - name: "UUT_2_Pump"
    uut: "UUT_2"

# Filter options per channel (or use null for unfiltered)
# Format: column_name: {order: N, cutoff_hz: F}
filters:
  Table_X: null
  Table_Y: null
  Table_Z: null
  UUT_1_Controller_X: {order: 3, cutoff_hz: 100}
  UUT_1_Controller_Y: {order: 3, cutoff_hz: 100}
  UUT_1_Controller_Z: {order: 3, cutoff_hz: 100}
  UUT_1_Pump_X: {order: 3, cutoff_hz: 100}
  UUT_1_Pump_Y: {order: 3, cutoff_hz: 100}
  UUT_1_Pump_Z: {order: 3, cutoff_hz: 100}
  UUT_2_Controller_X: {order: 3, cutoff_hz: 100}
  UUT_2_Controller_Y: {order: 3, cutoff_hz: 100}
  UUT_2_Controller_Z: {order: 3, cutoff_hz: 100}
  UUT_2_Pump_X: {order: 3, cutoff_hz: 100}
  UUT_2_Pump_Y: {order: 3, cutoff_hz: 100}
  UUT_2_Pump_Z: {order: 3, cutoff_hz: 100}

# Plot options
plot:
  wide: 6.5    # inches
  tall: 4.5    # inches
  tall_th: 4.5
  tall_th_unit: 3.5
  font_name: "Arial"
  font_size_title: 10
  font_size_axes: 9
  font_size_ticks: 8
  font_size_text: 8
  font_size_legend: 8
```

### resonance_config.yaml
```yaml
run_name: "Run_1"
script_dir: "/mnt/dropbox/_OpenClaw/data-processing-example"

# Input files - one per axis (keys must match axes list)
files:
  X: "/mnt/dropbox/_OpenClaw/data-processing-example/Resonance_X_2026Jan05-1323-0001.csv"
  Y: "/mnt/dropbox/_OpenClaw/data-processing-example/Resonance_Y_2026Jan05-1327-0001.csv"
  Z: "/mnt/dropbox/_OpenClaw/data-processing-example/Resonance_Z_2026Jan05-1331-0001.csv"

axes: ["X", "Y", "Z"]
high_cutoff: 33.3   # Hz, trim resonance data above this
plot_only: true     # true = CSVs already have frequency data (from controller)

# Column mapping for each axis file
# The resonance CSV header row defines the column names
# Map: output name -> raw CSV column name (per axis)
column_mapping:
  X:
    Table_X: "Control1 (G)"   # adjust to match actual header
    UUT_1_Controller_X: "Ch1 (G)"
    UUT_1_Pump_X: "Ch4 (G)"
    UUT_2_Controller_X: "Ch7 (G)"
    UUT_2_Pump_X: "Ch10 (G)"
  Y:
    Table_Y: "Control2 (G)"
    UUT_1_Controller_Y: "Ch2 (G)"
    UUT_1_Pump_Y: "Ch5 (G)"
    UUT_2_Controller_Y: "Ch8 (G)"
    UUT_2_Pump_Y: "Ch11 (G)"
  Z:
    Table_Z: "Control3 (G)"
    UUT_1_Controller_Z: "Ch3 (G)"
    UUT_1_Pump_Z: "Ch6 (G)"
    UUT_2_Controller_Z: "Ch9 (G)"
    UUT_2_Pump_Z: "Ch12 (G)"

# Accelerometers
accels:
  - name: "Controller"
    uut: "UUT_1"
    uut_map_x: "SS"   # "SS" or "FB" - orientation mapping in plotTransfer
  - name: "Pump"
    uut: "UUT_1"
    uut_map_x: "SS"
  - name: "Controller"
    uut: "UUT_2"
    uut_map_x: "SS"
  - name: "Pump"
    uut: "UUT_2"
    uut_map_x: "SS"

# Natural frequency selections (Hz) per UUT/accel/axis
# These replace the interactive ginput() click in MATLAB
# Format: uut -> accel -> axis -> frequency_hz
natural_frequencies:
  UUT_1:
    Controller_X: 33.3
    Controller_Y: 33.3
    Controller_Z: 33.3
    Pump_X: 33.3
    Pump_Y: 33.3
    Pump_Z: 33.3
  UUT_2:
    Controller_X: 33.3
    Controller_Y: 33.3
    Controller_Z: 33.3
    Pump_X: 33.3
    Pump_Y: 33.3
    Pump_Z: 33.3

# Output subdirectory for each UUT
output_subdirs:
  UUT_1: "UUT_1_Plots_Resonance"
  UUT_2: "UUT_2_Plots_Resonance"

plot:
  wide: 6.5
  tall: 4.5
  font_name: "Arial"
  font_size_title: 10
  font_size_axes: 9
  font_size_ticks: 8
  font_size_text: 8
```

---

## Critical Implementation Notes

### CSV Parsing (parse_csv.py)
The raw shake table CSV files are multi-section. Look at the raw CSV:
- `/mnt/dropbox/_OpenClaw/data-processing-example/Seismic_2026Jan05-1409-0001.csv`
The structure: a header row followed by data, then another header row, etc.
The header row containing `"Time (ms)"` is the start of the time-domain section.
Parse by scanning for the row where the first column matches `"Time (ms)"` or similar time-domain header.
Extract only the columns specified in `column_mapping`.
Output a clean DataFrame with renamed columns matching `column_mapping` keys.

For resonance CSVs (`plot_only: true`):
- The first column is the frequency axis (look for "Frequency (Hz)" or similar in the header)
- Just rename the first column to "Frequency", extract mapped columns, trim to `high_cutoff`

### Smallwood TRS (calc_trs.py)
Exact port of `/root/data-processing/Functions/calcTRS.m`.
Use `scipy.signal.lfilter(b, a, accel)` where b=[b1,b2,b3], a=[1,-a1,-a2].
Vectorize over frequencies using a loop (or numpy for speed).
Returns array of peak absolute response at each frequency.

```python
import numpy as np
from scipy.signal import lfilter

def calc_trs(time, accel, freq72, damping):
    delta_t = time[1] - time[0]
    trs = np.zeros(len(freq72))
    for j, f in enumerate(freq72):
        omega = 2 * np.pi * f
        omega_d = omega * np.sqrt(1 - damping**2)
        E = np.exp(-damping * omega * delta_t)
        K = omega_d * delta_t
        C = E * np.cos(K)
        S = E * np.sin(K)
        Sp = S / K
        a1 = 2 * C
        a2 = -(E**2)
        b1 = 1 - Sp
        b2 = 2 * (Sp - C)
        b3 = (E**2) - Sp
        resp = lfilter([b1, b2, b3], [1, -a1, -a2], accel)
        trs[j] = np.max(np.abs(resp))
    return trs
```

### Seismic Parameters (calc_seismic_parameters.py)
Port `/root/data-processing/Functions/calcSeismicParameters.m`.
Read that file carefully — it computes:
- freq72: frequency array at 1/72 octave spacing from ~1.3 Hz to 33.3 Hz
- RRS_h, RRS_v: required response spectra for horizontal and vertical
- Aflx_h/v, Arig_h/v, Arig_h90/v90: flexible/rigid zone boundaries

### Butterworth Filter (filter_data.py)
```python
from scipy.signal import butter, filtfilt
def filter_th(accel, sample_rate, order, cutoff_hz):
    Wn = cutoff_hz / (sample_rate / 2)
    b, a = butter(order, Wn, btype='low')
    return filtfilt(b, a, accel)
```

### Optimize TRS (optimize_trs.py)
Exact port of `/root/data-processing/Functions/optimizeTRS.m`.
The algorithm tries 12 starting indices (1:12) for 1/6-octave sub-sampling.
For Table accels, picks the starting index that gives best TRS factor.
For non-Table accels, always uses index 0.
The TRS factor logic is in `analyzeSet()` in the MATLAB code — port it exactly.

### Transfer Function (process_transfer_function.py)
Port `/root/data-processing/Resonance Functions/processTransferFunction.m`.
Use `scipy.signal.csd` and `scipy.signal.welch` to compute tfestimate equivalent:
```python
from scipy.signal import csd, welch
f, Pxy = csd(table_accel, uut_accel, fs=Fs, ...)
f, Pxx = welch(table_accel, fs=Fs, ...)
Txy = np.abs(Pxy / Pxx)
```

### Cross-Correlation (calc_cc.py)
```python
from scipy.signal import correlate, correlation_lags
# For each pair (X,Y), (X,Z), (Y,Z):
corr = correlate(sig1, sig2, mode='full') / (np.std(sig1) * np.std(sig2) * len(sig1))
```
CC factor = 0.3 / max(|correlation|)

### Coherence (calc_ch.py)
```python
from scipy.signal import coherence
fch = # frequency array from 1.3 to 33.3 Hz at 1/72 octave
CH, f = coherence(sig1[5*sr:-5*sr], sig2[5*sr:-5*sr], fs=sr, nperseg=window_samples, noverlap=overlap)
```
CH factor = 0.5 / max(CH)

### Plotting
- All matplotlib figures saved as both `.svg` AND `.png`
- SVG is for Word/PDF (vector), PNG is for quick viewing
- Use sequential numbering: `{n:02d}_{run_name}_{plot_type}_{accel}.svg`
- Match the MATLAB plot styles closely (log scales, tick marks, colors)
- TRS plots: x-axis log 0.5-35 Hz, y-axis log; gridlines; TRS in black, RRS in blue dashed, Aflx/Arig markers
- TH plots: x-axis 0-30s linear; y-axis symmetric; black time history; blue dashed ±Arig_90 lines for Table
- Transmissibility plots: x-axis log 1-35 Hz, y-axis log 0.1-55

### Excel Output (save_trs.py)
Use openpyxl. Copy template from `/root/data-processing/Tables/TRSvsRRS_Template.xlsx`.
Write Freq06, RRS, TRS06 data to columns A-L (X=A:C, Y=D:F, Z=G:I, D=J:L if applicable).
Write lowResonance to N3, lowCutoff to N4.
Filter: only write rows where frequency > 1.0 Hz.
Round all values to 2 decimal places.

### Plot Save (save_plot.py)
```python
import matplotlib.pyplot as plt

def save_plot(fig, name, run_name, plot_number, output_dir):
    filename = f"{plot_number:02d}_{run_name}_{name}"
    fig.savefig(f"{output_dir}/{filename}.svg", format='svg', bbox_inches='tight')
    fig.savefig(f"{output_dir}/{filename}.png", dpi=150, bbox_inches='tight')
    plt.close(fig)
    return plot_number + 1
```

### Runner Script (run_seismic.py)
```
1. Load config YAML
2. Parse raw seismic CSV -> trimmed DataFrame
3. Save trimmed CSV
4. calc_seismic_parameters -> Seismic struct
5. For each column in trimmed data:
   a. Apply filter if configured
   b. calc_trs -> TRS72
   c. optimize_trs -> freq06, TRS06
   d. plot_th -> save
   e. plot_trs -> save
6. For each accel (Table + all accels):
   a. plot_trs_all -> save
7. save_trs -> Excel
8. calc_cc + plot_cc -> save
9. calc_ch + plot_ch -> save
```

---

## Study These Files First
Before writing any code, read:
1. `/root/data-processing/Functions/calcSeismicParameters.m` — seismic params, freq72 construction
2. `/root/data-processing/Functions/calcTRS.m` — Smallwood algorithm
3. `/root/data-processing/Functions/optimizeTRS.m` — TRS optimization (analyzeSet)
4. `/mnt/dropbox/_OpenClaw/data-processing-example/Seismic_WCC_Booster_ETL.m` — the actual config
5. `/mnt/dropbox/_OpenClaw/data-processing-example/Resonance_WCC_Booster_ETL.m` — resonance config
6. `/root/data-processing/Functions/saveTRS.m` — Excel template column layout
7. `/root/data-processing/Resonance Functions/processTransferFunction.m` — tf calc
8. Sample of the raw CSVs to understand their structure

The example `.m` files tell you the ACTUAL column names used in the WCC Booster project — use those in the example configs.

## Dependencies (requirements.txt)
```
numpy
scipy
pandas
matplotlib
openpyxl
pyyaml
pytest
```

## Progress Tracking
Maintain a `PROGRESS.md` in the repo root. Update it after each major step. If you crash and restart, check PROGRESS.md to know where you left off.

## Git Discipline
Commit after each phase:
- Phase 1: config schema + example configs
- Phase 2: core math modules + tests
- Phase 3: CSV parsing
- Phase 4: plotting
- Phase 5: Excel output
- Phase 6: runner scripts working end-to-end

Use: `git add -A && git commit -m "phase N: description" && git push`
