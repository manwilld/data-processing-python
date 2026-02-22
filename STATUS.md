# Data Processing Python — Project Status
_Last updated: 2026-02-22_

---

## What This Is

A Python port of Derek's MATLAB shake table test data processing pipeline. Takes raw accelerometer CSV data from shake table runs, processes it, and produces:
- Trimmed/filtered CSV files
- TRS (Test Response Spectrum) plots and Excel tables
- Time history plots, CC/CH plots, resonance/transfer function plots
- Complete Word test report (`.docx`) via `build_report.py`

Mirrors the MATLAB pipeline at `/root/data-processing/` exactly.

---

## Project Structure

```
/root/data-processing-python/
├── build_report.py                   # Report dispatcher: --project --type
├── run_seismic.py                    # Main runner: seismic runs
├── run_resonance.py                  # Main runner: resonance runs
├── builders/
│   ├── __init__.py
│   └── test_report_builder.py        # Thin run() module for test report type
├── functions/
│   ├── parse_csv.py
│   ├── filter_data.py
│   ├── calc_trs.py / calc_cc.py / calc_ch.py
│   ├── calc_seismic_parameters.py
│   ├── optimize_trs.py
│   ├── process_seismic_run.py / process_transfer_function.py
│   ├── plot_th.py / plot_trs.py / plot_trs_all.py
│   ├── plot_cc.py / plot_ch.py / plot_transfer.py
│   ├── plot_style.py                 # Shared plot styling (all plot fns import this)
│   ├── save_trs.py / save_plot.py
│   └── test_report_generator.py     # TestReportGenerator class
├── compare/
│   └── run_comparison.py             # 113/113 validation vs MATLAB baseline
├── tests/                            # 15 unit tests (pytest)
├── examples/
│   └── WCC_Booster/
│       ├── project_config.py         # Single source of truth for all report types
│       ├── seismic_config.yaml
│       └── resonance_config.yaml
└── requirements.txt
```

---

## Current State

| Check | Status |
|-------|--------|
| Data pipeline — zero errors | ✅ |
| `pytest tests/ -v` — 15/15 pass | ✅ |
| `compare/run_comparison.py` — 113/113 PASS | ✅ |
| Test report generator — runs clean, 36 pages | ✅ |
| Structural alignment with reference report | ✅ `84145fe` |
| Git: clean, pushed to `manwilld/data-processing-python` | ✅ |

---

## Report Generator

### How to Run

```bash
cd /root/data-processing-python
python3 build_report.py --project examples/WCC_Booster --type test_report
# Output: /mnt/dropbox/_OpenClaw/data-processing-example/25075TR1.0_Test_Report.docx
```

### Architecture

- `build_report.py` — dispatcher; loads `project_config.py`; resolves paths
- `builders/test_report_builder.py` — thin `run()` module (one per report type)
- `functions/test_report_generator.py` — `TestReportGenerator` class; all section logic
- `examples/WCC_Booster/project_config.py` — one config for all report types; `reports` dict holds type-specific overrides

### Document Structure (matches reference `25075TR1.0 Test Report.docx`)

```
Cover
  Title / Subtitle
  [Manufacturer | Testing Laboratory] table
  Testing Scope header + text
  [Seismic Levels] table
  Test Units header
  [UUT dimensions/weight] table
  Certification company
  Revision history

Test Results Summary
  Intro + level description
  [Resonance results] table
  "As shown below..." text
  [Run results / peak accels] table

Test Procedure
  Sub-sections (inspection, mounting, resonance search, etc.)
  Test Witnesses
  Shake Table Information
  [Lab equipment / calibration] table

UUT Summary × N
  Info block (model, dimensions, nat freq, mounting)
  Construction / Subcomponents / Function Testing / Notes
  Resonance plots

Seismic Run × N (per run)
  [Seismic Levels] table
  Pre-Test Pictures (2-col grid with "Pre-test" header row)
  Post-Test Pictures (2-col grid with "Post-test" header row)
  Response Spectra Plots
  Response Spectra Data (text + [TRS] table)
  Acceleration Time History Plots
    [Run results / peak accels] table   ← sits here per reference
    TH plots
  Statistical Independence Plots (CC/CH)
  Unit Accelerometer Plots

Appendix – Laboratory Accreditation
```

### Photo Support

```python
'pre_test_photos':  {'dir': '/path/to/photos/', 'max': 12},   # 12 of N evenly sampled
'post_test_photos': {'dir': '/path/to/photos/', 'max': 16},   # 16 of N evenly sampled
# max: None → embed all
```

- `_select_photos()` — evenly-spaced sample; always includes first and last
- `_resize_photo()` — Pillow resize to 900px max before embed (keeps docx ~5MB)
- `_build_photo_section()` — 2-col table with labeled header row

### Multi-Run Support

Fully loop-based. Add entries to `runs` list and `run_plots` dict in `project_config.py`. Each run gets its own seismic table, photo sections, plots, TRS data, and run results table.

### Current Output (WCC Booster)

- **36 pages, 4.8MB**
- 12 pre-test photos (sampled from 129), 16 post-test photos (sampled from 53)
- 49 plots (TRS, TH, CC/CH, resonance)
- 1 run × 2 UUTs

---

## Key Design Decisions

- **PNG over SVG** for report embedding — python-docx SVG support is complex; PNGs exist alongside every SVG; upgrade is a one-method change
- **Photo resize** — 900px max before embed; drops 277MB → 4.8MB
- **One `project_config.py` per project** — `reports` dict holds type-specific overrides
- **TH grid intentionally OFF** — cross-engine grid lines push pixel diff from 14→24
- **Filter values from YAML** — X/Y=699.5Hz order=3, Z=200Hz order=3 (from `Run_1_filters.mat`)

---

## Outstanding / Future Work

1. **Deeper content polish** — text wording, table formatting details, style tweaks
2. **SVG embedding** — one-method change in `_build_plot_section()`; low priority
3. **Photo captions** — sequential numbering or filename labels under each photo
4. **Windows test run** — all dev on Linux; font rendering may shift
5. **CI** — no GitHub Actions yet; tests run manually
6. **Production path workflow** — flip `output` key in `project_config.py` to real project folder when delivering

---

## Key Commits

| Hash | Description |
|------|-------------|
| `e30367c` | plot_style.py refactor (113/113 still pass) |
| `5031d32` | initial test report builder |
| `8db3578` | fix 5 visual bugs (Hf/Rμ, weight comma, level para, levels-in-run, run-results-in-run) |
| `aa7d87e` | photo grid + Dropbox paths |
| `16ca69c` | STATUS.md update |
| `c8f0997` | output path → _OpenClaw/data-processing-example/ |
| `84145fe` | structural alignment with reference (cover, TRS, test procedure, run section) |

---

## Git / Repo

- Local: `/root/data-processing-python/`
- Remote: `manwilld/data-processing-python` — branch `main`, clean, up to date
