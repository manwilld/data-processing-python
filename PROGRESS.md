# Progress

## Phase 1: Config schema + example configs + requirements.txt ✅
## Phase 2: Core math modules + tests ✅ (15/15)
## Phase 3: CSV parsing ✅
## Phase 4: Plotting ✅
## Phase 5: Excel output ✅
## Phase 6: Runner scripts ✅

## Fidelity Pass (2026-02-21) ✅ — 113/113 PASS

### Data (exact match)
- Seismic trimmed CSV: 42001 rows, values identical to MATLAB baseline (max_diff=0.0)
- Resonance trimmed CSV: 1819 rows, correct column order, values identical (max_diff=0.0)
- Excel TRS table: correct headers, correct Z column position (G:I not J:L),
  low resonance/cutoff annotations at K3/L3/K4/L4 matching MATLAB exactly,
  279 data cells, all values identical (max_diff=0.0)

### Plots (all 113 checks PASS at threshold=20.0 mean pixel diff)
- Seismic: 37 plots (975px wide: 300px Table TH, 270px UUT TH, 405px TRS/CC/CH/TRSall)
- Resonance: 12 plots (975×405px)
- Filter parameters corrected from .mat file (X/Y=699.5Hz, Z=200Hz order=3)
- Custom tick labels fixed (FixedFormatter after plotting to prevent loglog reset)
- Colors: Aflx/Arig blue text + [0.7,0.7,1] lines, lowCutoff blue, 0.9RRS red,
  1.3RRS yellow, TH Arig lines blue, CC: k/c/m

### Comparison script
- `compare/run_comparison.py` — validates all structural and pixel checks
- Threshold 20.0 reflects realistic cross-engine rendering (matplotlib vs MATLAB)

## Known Differences from MATLAB (acceptable)
- SVG instead of EMF (Word 2016+ compatible vector format)
- Font: Liberation Sans on Linux, Arial auto-selected on Windows
- Pixel diff 10-18 mean across plots (font rendering, antialiasing, minor margin differences)
- Natural frequency marker in resonance plots: auto-detected peak (not user-click)
- Filter/nat-freq config in YAML instead of .mat files and interactive dialogs
