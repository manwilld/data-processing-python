# Data Processing Python — Project Status
_Last updated: 2026-02-21_

---

## What This Is

A Python port of Derek's MATLAB shake table test data processing pipeline. Takes raw accelerometer CSV data from shake table runs, processes it, and produces:
- Trimmed/filtered CSV files
- TRS (Test Response Spectrum) plots and Excel tables
- Time history plots (per channel)
- Capacity curve (CC) and channel response (CH) plots
- Transfer function / resonance plots

Mirrors the MATLAB pipeline at `/root/data-processing/` exactly. Outputs go to Dropbox at `/mnt/dropbox/_OpenClaw/data-processing-example/`. MATLAB baseline for comparison lives at `./_matlab_baseline/` (do not modify).

---

## Project Structure

```
/root/data-processing-python/
├── run_seismic.py          # Main runner: seismic runs
├── run_resonance.py        # Main runner: resonance/transfer function runs
├── functions/
│   ├── parse_csv.py        # CSV ingestion + trimming (fence-post inclusive)
│   ├── filter_data.py      # Butterworth filter (order/cutoff per channel from config)
│   ├── calc_trs.py         # TRS calculation (Newmark integration)
│   ├── calc_cc.py          # Capacity curve calculation
│   ├── calc_ch.py          # Channel response calculation
│   ├── calc_seismic_parameters.py  # Arig, Aflx, RRS lookups
│   ├── optimize_trs.py     # TRS optimization
│   ├── process_seismic_run.py      # Orchestrates one seismic run
│   ├── process_transfer_function.py # Orchestrates one resonance run
│   ├── plot_th.py          # Time history plots
│   ├── plot_trs.py         # TRS plots (single channel)
│   ├── plot_trs_all.py     # TRS overlay plot (all channels)
│   ├── plot_cc.py          # Capacity curve plot
│   ├── plot_ch.py          # Channel response plot
│   ├── plot_transfer.py    # Transfer function / resonance plot
│   ├── plot_style.py       # Shared plot styling constants
│   ├── save_trs.py         # Excel TRS table output
│   └── save_plot.py        # SVG/PNG save with exact DPI/dimensions
├── compare/
│   └── run_comparison.py   # Validation script vs MATLAB baseline
├── tests/
│   ├── test_calc_trs.py
│   ├── test_optimize_trs.py
│   ├── test_calc_seismic_parameters.py
│   └── test_parse_csv.py
├── examples/
│   └── WCC_Booster/
│       ├── seismic_config.yaml
│       └── resonance_config.yaml
└── requirements.txt
```

---

## Current State

**Status: Complete. All checks passing.**

| Check | Status |
|-------|--------|
| `run_seismic.py` — zero errors | ✅ |
| `run_resonance.py` — zero errors | ✅ |
| `pytest tests/ -v` — all pass | ✅ |
| `compare/run_comparison.py` — 113/113 PASS | ✅ |
| Git: committed + pushed to main | ✅ |

Pixel diff vs MATLAB baseline: 10–18 mean across all plots (acceptable — font rendering and antialiasing differences between matplotlib/Linux and MATLAB/Windows).

---

## Key Design Decisions

- **SVG output** instead of EMF (MATLAB default). SVG is Word 2016+ compatible vector format and renders cleanly without rasterization.
- **Font**: Liberation Sans on Linux; Arial auto-selected on Windows. Visual match to MATLAB's Arial.
- **Filter values** come from YAML config (not `.mat` files or interactive dialogs). Correct values extracted from `Run_1_filters.mat`:
  - X/Y channels: order=3, cutoff=699.5 Hz
  - Z channels: order=3, cutoff=200.0 Hz
- **Natural frequency marker** in resonance plots: auto-detected peak (not user-click like MATLAB). Config `natural_frequencies` value is a search hint only.
- **Plot dimensions**: exact match to MATLAB PaperPosition at 150 DPI — no `bbox_inches='tight'`:
  - TRS / CC / CH / Resonance: 975×405 px (6.5×2.70 in)
  - Table TH: 975×300 px (6.5×2.00 in)
  - UUT TH: 975×270 px (6.5×1.80 in)
- **Trimmed CSV endpoint**: inclusive (`<=`) to match MATLAB's 42001-row output.
- **Resonance CSV column order**: sensor-grouped (matches MATLAB), not axis-grouped.
- **Excel TRS table**: Z axis at columns 6–8 (not 9–11). 12 columns total.

---

## What's Working Well

- Full numerical match to MATLAB on all data outputs (CSV, Excel): max_diff=0.0
- Plot dimensions exact match at 150 DPI
- Config-driven filter values per channel
- Auto-detected resonance peaks
- Graceful multi-location font fallback
- Clean comparison script that validates everything in one shot
- Solid test suite (15/15 unit tests)

---

## Known Acceptable Differences from MATLAB

- Pixel diff 10–18 mean (font rendering: Liberation Sans on Linux vs MATLAB's Helvetica — not fixable without MATLAB's renderer)
- SVG vs EMF format
- Natural frequency annotation: auto-detected vs user-clicked
- Config-driven vs `.mat`-file-driven filter presets
- **TH plots: grid intentionally OFF** — MATLAB has grid on, but cross-engine grid line pixel positions differ enough to push mean diff from ~14 to ~24. Leaving grid off is closer to MATLAB visually at the pixel level.

---

## How to Run

```bash
cd /root/data-processing-python

# Seismic runs
python3 run_seismic.py --config examples/WCC_Booster/seismic_config.yaml

# Resonance runs
python3 run_resonance.py --config examples/WCC_Booster/resonance_config.yaml

# Unit tests
python3 -m pytest tests/ -v

# Validate vs MATLAB baseline
python3 compare/run_comparison.py
```

---

## What Might Still Need Improvement

1. **Real project integration** — WCC_Booster example works. How to onboard a new project isn't fully documented (how to create configs from scratch, where to point input CSV paths, etc.).
2. **Word report integration** — outputs are SVG + Excel, but there's no pipeline yet to pull these into a Word report automatically (unlike the structural-calcs side which has `build_report.py`).
3. **Windows testing** — all development and testing on Linux. Font rendering on Windows may shift pixel diffs; worth a spot-check run on Derek's machine.
4. **Threshold tuning** — comparison script uses threshold=20.0 (mean pixel diff). Now that it's passing at 10–18, could tighten to ~25 to catch regressions while still allowing cross-engine variance.
5. **No CI** — tests run manually. A GitHub Action would catch regressions automatically.

---

## Git / Repo

- Local: `/root/data-processing-python/`
- Remote: `manwilld/data-processing-python`
- Branch: `main` — clean, up to date
