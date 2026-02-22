# Data Processing Python — Project Status
_Last updated: 2026-02-22_

---

## What This Is

A Python port of Derek's MATLAB shake table test data processing pipeline. Takes raw accelerometer CSV data from shake table runs, processes it, and produces:
- Trimmed/filtered CSV files
- TRS (Test Response Spectrum) plots and Excel tables
- Time history plots (per channel)
- Capacity curve (CC) and channel response (CH) plots
- Transfer function / resonance plots
- Complete Word test report (`.docx`) via `build_report.py`

Mirrors the MATLAB pipeline at `/root/data-processing/` exactly. Outputs go to Dropbox at `/mnt/dropbox/_OpenClaw/data-processing-example/`. MATLAB baseline for comparison lives at `./_matlab_baseline/` (do not modify).

---

## Project Structure

```
/root/data-processing-python/
├── build_report.py             # Report dispatcher: --project --type
├── run_seismic.py              # Main runner: seismic runs
├── run_resonance.py            # Main runner: resonance/transfer function runs
├── builders/
│   ├── __init__.py
│   └── test_report_builder.py  # Thin run() module for test report type
├── functions/
│   ├── parse_csv.py
│   ├── filter_data.py
│   ├── calc_trs.py
│   ├── calc_cc.py
│   ├── calc_ch.py
│   ├── calc_seismic_parameters.py
│   ├── optimize_trs.py
│   ├── process_seismic_run.py
│   ├── process_transfer_function.py
│   ├── plot_th.py
│   ├── plot_trs.py
│   ├── plot_trs_all.py
│   ├── plot_cc.py
│   ├── plot_ch.py
│   ├── plot_transfer.py
│   ├── plot_style.py           # Shared plot styling constants (all 6 plot fns import this)
│   ├── save_trs.py
│   ├── save_plot.py
│   └── test_report_generator.py  # TestReportGenerator class
├── compare/
│   └── run_comparison.py       # Validation script vs MATLAB baseline
├── tests/
│   ├── test_calc_trs.py
│   ├── test_optimize_trs.py
│   ├── test_calc_seismic_parameters.py
│   └── test_parse_csv.py
├── examples/
│   └── WCC_Booster/
│       ├── project_config.py   # Single source of truth for all report types
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
| Test report generator — runs clean | ✅ |
| 5 visual bugs fixed | ✅ `8db3578` |
| Photo grid support | ✅ `aa7d87e` |
| Git: committed + pushed to main | ✅ |

---

## Report Generator

### How to Run

```bash
cd /root/data-processing-python
python3 build_report.py --project examples/WCC_Booster --type test_report
# Output: /tmp/dp-test/25075TR1.0_Test_Report.docx
```

### Architecture

- `build_report.py` — dispatches to the correct builder, loads `project_config.py`, resolves paths
- `builders/test_report_builder.py` — thin `run()` module (one per report type)
- `functions/test_report_generator.py` — `TestReportGenerator` class; full section logic
- `examples/WCC_Booster/project_config.py` — single config for all report types; `reports` dict holds type-specific overrides

### Sections (in order)
1. Cover page
2. Test Results Summary (seismic levels table, UUT table, resonance results, run results, lab equipment)
3. Test Procedure
4. UUT Summary × N (resonance plots per UUT)
5. Seismic Run × N (levels table, pre/post photos, TRS plots, TRS data table, TH plots, CC/CH, UUT accel plots, run results table)
6. Appendix — Laboratory Accreditation

### Photo Support

- `_select_photos(dir, max_photos)` — sorted, evenly-spaced sample; handles any count
- `_resize_photo(path, max_px=900)` — Pillow resize before embedding; keeps file small
- `_build_photo_grid(photos, cols=2)` — 2-column table, auto-pads last row
- Config per run:
  ```python
  'pre_test_photos':  {'dir': '...', 'max': 12},   # 12 of N evenly sampled
  'post_test_photos': {'dir': '...', 'max': 16},   # 16 of N evenly sampled
  ```

### Multi-Run Support

Fully loop-based — add entries to `runs` list and `run_plots` dict in config. Each run gets its own seismic level table, photo sections, TRS plots, data table, and run results table.

### Current Output (WCC Booster)
- 41 pages, 4.6MB
- 12 pre-test photos (sampled from 129), 16 post-test photos (sampled from 53)
- 49 plots (TRS, TH, CC/CH, resonance)
- 1 run × 2 UUTs

---

## Key Design Decisions

- **SVG output** instead of EMF (MATLAB default). SVG is Word 2016+ compatible.
- **Font**: Liberation Sans on Linux; Arial auto-selected on Windows.
- **Filter values** from YAML config. Correct values from `Run_1_filters.mat`: X/Y=699.5Hz order=3, Z=200Hz order=3.
- **Natural frequency marker**: auto-detected peak (not user-click like MATLAB).
- **Plot dimensions**: exact match to MATLAB PaperPosition at 150 DPI.
- **PNG over SVG for report embedding**: python-docx SVG support is complex; PNGs exist alongside every SVG. Upgrade is a one-method change later.
- **Photo resize**: photos resized to max 900px longest side before embedding to keep docx file size manageable.
- **One `project_config.py` per project**: used for all report types; `reports` dict holds type-specific overrides.

---

## How to Run (Data Pipeline)

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

## Known Acceptable Differences from MATLAB

- Pixel diff 10–18 mean (font: Liberation Sans on Linux vs MATLAB's Helvetica)
- SVG vs EMF format
- Natural frequency annotation: auto-detected vs user-clicked
- Config-driven filter presets vs `.mat`-file-driven
- **TH plots: grid intentionally OFF** — cross-engine grid line positions push diff higher

---

## What's Still Outstanding

1. **SVG embedding in report** — currently PNG fallback; upgrade is one-method change in `_embed_plot()`
2. **Photo captions** — photos embedded without captions; reference report has none either, but could add filename or sequential number
3. **Windows test** — all dev on Linux; font rendering may shift slightly on Windows
4. **No CI** — tests run manually; GitHub Action would catch regressions
5. **Production paths** — `project_config.py` output path is `/tmp/dp-test/`; change `output` key to real project path when ready to produce a deliverable

---

## Git / Repo

- Local: `/root/data-processing-python/`
- Remote: `manwilld/data-processing-python`
- Branch: `main` — clean, up to date
- Key commits:
  - `e30367c` — plot_style.py refactor (113/113 still pass)
  - `5031d32` — initial test report builder
  - `8db3578` — fix 5 visual bugs
  - `aa7d87e` — photo grid support + Dropbox paths
