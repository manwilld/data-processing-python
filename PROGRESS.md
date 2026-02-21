# Progress

## Phase 1: Config schema + example configs + requirements.txt ✅
- [x] Created directory structure
- [x] Created requirements.txt
- [x] Created example configs (seismic + resonance) for WCC_Booster

## Phase 2: Core math modules + tests ✅
- [x] calc_trs.py — Smallwood recursive digital filter
- [x] calc_seismic_parameters.py — ASCE 7-16/22, freq72, RRS, Aflx/Arig
- [x] optimize_trs.py — 1/6-octave TRS optimization (12-start-index search)
- [x] filter_data.py — Butterworth lowpass + filtfilt
- [x] calc_cc.py — Cross-correlation (statistical independence)
- [x] calc_ch.py — Magnitude squared coherence
- [x] Tests — 15/15 passing

## Phase 3: CSV parsing ✅
- [x] parse_csv.py — multi-section seismic + resonance CSV parser

## Phase 4: Plotting ✅
- [x] plot_th.py — time history
- [x] plot_trs.py — TRS vs RRS (single accel)
- [x] plot_trs_all.py — TRS vs RRS all-axes overlay
- [x] plot_transfer.py — transmissibility
- [x] plot_cc.py — cross-correlation
- [x] plot_ch.py — coherence
- [x] save_plot.py — saves both SVG + PNG with sequential numbering
- [x] plot_style.py — font fallback (Arial → Liberation Sans → DejaVu Sans)

## Phase 5: Excel output ✅
- [x] save_trs.py — writes freq06/RRS/TRS06 to xlsx via openpyxl

## Phase 6: Runner scripts ✅
- [x] run_seismic.py — headless seismic pipeline
- [x] run_resonance.py — headless resonance pipeline

## Verification (2026-02-21) ✅
- Seismic: 37 plots (PNG + SVG), trimmed CSV, Excel — all match MATLAB naming
- Resonance: 12 plots (6 UUT_1 + 6 UUT_2), global counter 1-12 — matches MATLAB
- Excel saved to script_dir (not output_subdir) — matches MATLAB behavior
- No font warnings — Liberation Sans fallback active on droplet
- On Windows/Mac with Arial installed, Arial will be used automatically
- 15/15 unit tests pass

## Known Differences from MATLAB
- SVG instead of EMF (vector format, Word 2016+ compatible)
- Font: Liberation Sans on Linux, Arial on Windows (same metrics)
- No `.mat` filter preset files (filters specified in YAML config)
- No `selectedNaturalFrequencies.mat` (natural freqs in YAML config)
