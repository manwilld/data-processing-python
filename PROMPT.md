# Data Processing Python — Fidelity Pass

## Goal
Make the Python output match the MATLAB baseline as closely as possible.
The MATLAB baseline lives at:
`/mnt/dropbox/_OpenClaw/data-processing-example/_matlab_baseline/`
**DO NOT modify or delete anything in _matlab_baseline/.**

The Python output goes to:
`/mnt/dropbox/_OpenClaw/data-processing-example/`

## Completion Criteria
DONE when ALL of the following pass:
1. `python3 run_seismic.py --config examples/WCC_Booster/seismic_config.yaml` — zero errors
2. `python3 run_resonance.py --config examples/WCC_Booster/resonance_config.yaml` — zero errors
3. `python3 -m pytest tests/ -v` — all tests pass
4. `python3 compare/run_comparison.py` — ALL checks PASS (this script must be created as part of this task)
5. `git add -A && git commit && git push` — succeeds

When done, run: `openclaw system event --text "Done: data-processing fidelity pass complete" --mode now`

---

## Comparison Script to Create

Create `compare/run_comparison.py`. This script compares Python outputs vs MATLAB baseline and prints PASS/FAIL for each check. It must:
- Compare trimmed CSV values and row counts
- Compare resonance CSV column order and values
- Compare Excel column layout, row count, and values
- Compare image pixel dimensions
- Compute per-plot mean pixel difference (report actual value, FAIL if > 8.0)
- Print a final summary: N passed, M failed

---

## Confirmed Issues — Fix All of These

### 1. Filter Config — WRONG VALUES (critical)
Read the actual MATLAB filter presets from:
`/mnt/dropbox/_OpenClaw/data-processing-example/_matlab_baseline/Run_1_filters.mat`
using `scipy.io.loadmat`. The actual presets are:
- Table_X, Table_Y, UUT_1_Controller_X, UUT_1_Controller_Y, UUT_1_Pump_X, UUT_1_Pump_Y,
  UUT_2_Controller_X, UUT_2_Controller_Y, UUT_2_Pump_X, UUT_2_Pump_Y:
  → order=3, cutoff_hz=699.5
- Table_Z, UUT_1_Controller_Z, UUT_1_Pump_Z, UUT_2_Controller_Z, UUT_2_Pump_Z:
  → order=3, cutoff_hz=200.0

Update `examples/WCC_Booster/seismic_config.yaml` with these exact values.
The current config incorrectly has cutoff_hz=100 for everything.

### 2. Seismic Trimmed CSV — Off-by-one (minor)
MATLAB: 42001 rows (includes endpoint at t=30.000 s)
Python:  42000 rows (stops at t=29.9999 s)
Fix: use `<=` (inclusive) when selecting rows up to `trim_start + duration`.
In `functions/parse_csv.py`, the time slicing condition should include the endpoint.

### 3. Resonance Trimmed CSV — Column Order
MATLAB order: Frequency, Table_X, Table_Y, Table_Z, UUT_1_Controller_X, UUT_1_Controller_Y,
  UUT_1_Controller_Z, UUT_1_Pump_X, UUT_1_Pump_Y, UUT_1_Pump_Z, UUT_2_Controller_X, ...
Python groups by axis (all X first, then all Y, then all Z).
Fix: write columns in the MATLAB order (grouped by sensor, interleaved axes) in
`run_resonance.py` when building the DataFrame to save.

### 4. Excel Column Mapping — Z in Wrong Position
MATLAB layout (0-indexed columns):
  0-2: X Direction (Freq_X, RRS_X, TRS_X)
  3-5: Y Direction (Freq_Y, RRS_Y, TRS_Y)
  6-8: Z Direction (Freq_Z, RRS_Z, TRS_Z)   ← Z IS HERE, not at 9-11
  9-11: D Direction (empty if no diagonal axis)
  10 (K): Low resonance value = 5
  11 (L): Text "<- Lowest Resonance"
  11 (K row 4): Cutoff value = 3.5
  11 (L row 4): Text "<- Cuttoff Frequency"   ← note MATLAB typo "Cuttoff"

MATLAB header rows:
  Row 1: ['X Direction', None, None, 'Y Direction', None, None, 'Z Direction', None, None, None, None, None]
  Row 2: ['Freq.\n(Hz)', 'RRS\n(g)', 'TRS\n(g)', 'Freq.\n(Hz)', 'RRS\n(g)', 'TRS\n(g)',
          'Freq.\n(Hz)', 'RRS\n(g)', 'TRS\n(g)', None, None, None]

Fix in `functions/save_trs.py`:
  axis_to_col = {'X': 0, 'Y': 3, 'Z': 6, 'D': 9}   # Z at 6, not 9
  Low resonance value at cell(3, 11), text at cell(3, 12)
  Cutoff value at cell(4, 11), text "<- Cuttoff Frequency" at cell(4, 12)
  Only 12 columns total (not 14)
  Write proper header rows matching MATLAB exactly.

### 5. Figure Dimensions — Must Match MATLAB Exactly
MATLAB saves at 150 DPI with these exact PaperPosition sizes:
  TRS plots:        6.5 × 2.70 inches  → 975 × 405 px at 150 DPI
  Table TH plots:   6.5 × 2.00 inches  → 975 × 300 px at 150 DPI
  UUT TH plots:     6.5 × 1.80 inches  → 975 × 270 px at 150 DPI
  Resonance plots:  6.5 × 2.70 inches  → 975 × 405 px at 150 DPI
  CC/CH plots:      6.5 × 2.70 inches  → 975 × 405 px at 150 DPI

Fix in ALL plot functions:
  - Use `fig = plt.figure(figsize=(6.5, 2.70))` (or appropriate height)
  - Save with `fig.savefig(path, dpi=150)` — NO `bbox_inches='tight'`
  - Use `fig.subplots_adjust(left=0.08, right=0.97, top=0.88, bottom=0.15)` as starting point
    (tune margins until output pixel dimensions match MATLAB within ±2px)
  - Set figure background color: `fig.patch.set_facecolor('#F0F0F0')` (MATLAB default light gray)
  - Set axes background: `ax.set_facecolor('white')`

Update `seismic_config.yaml` plot options:
  wide: 6.5
  tall_trs: 2.70       # TRS plots
  tall_th_table: 2.00  # Table TH plots
  tall_th_uut: 1.80    # UUT TH plots
  tall_res: 2.70       # Resonance plots
  tall_cc: 2.70        # CC plot
  tall_ch: 2.70        # CH plot

### 6. ALL Plots — Tick Direction and Full Box
Apply to every single plot function:
```python
ax.tick_params(axis='both', which='both', direction='in',
               top=True, right=True,
               length=4, width=0.5)  # inward ticks on all 4 sides
ax.spines['top'].set_visible(True)
ax.spines['right'].set_visible(True)
```

### 7. ALL Plots — Title Bold, Axes Labels Bold
```python
ax.set_title('...', fontsize=fontSizeTitle, fontweight='bold')
ax.set_xlabel('...', fontsize=fontSizeAxes, fontweight='bold')
ax.set_ylabel('...', fontsize=fontSizeAxes, fontweight='bold')
```

### 8. TH Plots — Multiple Fixes
a) ±Arig_90 dashed lines MUST BE BLUE, not gray:
   ```python
   ax.axhline(Arig_90, color='blue', linestyle='--', linewidth=1.0, dashes=(6,3))
   ax.axhline(-Arig_90, color='blue', linestyle='--', linewidth=1.0, dashes=(6,3))
   ```
   Also add blue text annotations for the Arig_90 value (e.g. "1.94") near the line
   at the left side of the plot.

b) X-axis range: always 0 to 30 (matching MATLAB `duration` = 30s), NOT auto-scaled:
   ```python
   ax.set_xlim([0, 30])
   ax.set_xticks([0, 5, 10, 15, 20, 25, 30])
   ```

c) Y-axis range: symmetric, based on max absolute value of signal, rounded to next integer.
   Match MATLAB's logic from `plotTH.m` exactly:
   ```python
   maxAccel = np.max(np.abs(accel))
   yLim = max(ceil(maxAccel), ceil(Arig_90) + 1)
   ax.set_ylim([-yLim, yLim])
   ax.set_yticks(range(-yLim, yLim+1, 1))  # every 1g
   ```
   (Read the actual MATLAB `plotTH.m` code for the exact yLim calculation)

d) "Max. Accel. = Xg" annotation: black text in lower-right area.

e) Figure height for Table channels (those starting with "Table_"): use `tall_th_table`
   Figure height for all other channels: use `tall_th_uut`

### 9. TRS Plots — Multiple Fixes
a) X-axis custom tick labels (CRITICAL — currently shows 10^0, 10^1 instead of readable values):
   ```python
   xTicks = [0.5, 1, 1.3, 8.3, 10, 20, 35]
   ax.set_xscale('log')
   ax.set_xlim([0.5, 35])
   ax.set_xticks(xTicks)
   ax.set_xticklabels([str(x) for x in xTicks], fontsize=fontSizeTicks)
   ax.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
   ```

b) Y-axis custom tick labels:
   ```python
   yTicks = [0.1, 0.5, 1, 5, 10, 50]
   ax.set_yscale('log')
   ax.set_ylim([yMin, yMax])  # match MATLAB plotTRS.m yMin/yMax logic
   ax.set_yticks(yTicks)
   ax.set_yticklabels([str(y) for y in yTicks], fontsize=fontSizeTicks)
   ax.yaxis.set_minor_locator(matplotlib.ticker.NullLocator())
   ```

c) 0.9×RRS line: RED dashed (currently gray):
   ```python
   ax.plot(freq72, 0.9*RRS, color='red', linestyle='--', linewidth=0.75, label='0.9*RRS')
   ```

d) Read `plotTRS.m` carefully and replicate ALL line styles exactly:
   - TRS curve: black solid
   - RRS curve: blue dashed, linewidth ~2.0
   - 0.9×RRS: red dashed
   - Aflx horizontal line: red dashed, left segment only (0.5 to 1.3 Hz)
   - Arig horizontal line: red dashed, right segment only (8.3 Hz to 35 Hz)
   - 1.3 Hz vertical: gray dashed
   - 8.3 Hz vertical: gray dashed
   - lowCutoff vertical line: cyan dashed with cyan text label
   - 1.1×RRS yellow dashed line (if present in MATLAB)

e) Legend: use underscore in channel name label (e.g. "Table_X" not "Table X")

### 10. Resonance (Transfer Function) Plots — Multiple Fixes
a) CRITICAL BUG — Natural frequency marker is placed at config value (33.3 Hz default)
   instead of the actual peak. Fix:
   ```python
   # Find the actual peak in the transmissibility data near the config nat_freq
   # Use the peak closest to nat_freq, or the global maximum
   peak_idx = np.argmax(transfer_response)
   nat_freq_actual = frequency[peak_idx]
   nat_freq_value = transfer_response[peak_idx]
   # Plot marker at actual peak
   ax.plot(nat_freq_actual, nat_freq_value, 'o', color='blue',
           markersize=8, markerfacecolor='none', markeredgewidth=1.5)
   ax.text(nat_freq_actual * 0.85, nat_freq_value,
           f'{nat_freq_actual:.1f}-Hz', color='blue', fontsize=fontSizeText,
           ha='right', va='center')
   ```
   The config `natural_frequencies` value is a HINT, not the exact value.
   Find the peak automatically.

b) X-axis range: 1.0 to highCutoff (33.3 Hz), NOT 1-100 Hz
   ```python
   ax.set_xlim([1.0, 33.3])
   xTicks = [1.3, 5, 10, 20, 30]
   ax.set_xticks(xTicks)
   ax.set_xticklabels([str(x) for x in xTicks])
   ax.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
   ```

c) Y-axis range: 0.1 to ~50 (log), matching MATLAB
   ```python
   yTicks = [1, 10, 50]
   ax.set_yscale('log')
   ax.set_ylim([0.1, 55])
   ax.set_yticks(yTicks)
   ax.set_yticklabels([str(y) for y in yTicks])
   ax.yaxis.set_minor_locator(matplotlib.ticker.NullLocator())
   ```

d) Grid: dotted style (MATLAB uses dotted, Python is using solid):
   ```python
   ax.grid(True, which='major', linestyle=':', linewidth=0.5, color='gray', alpha=0.7)
   ax.grid(False, which='minor')
   ```

e) Read `plotTransfer.m` from MATLAB source carefully for all details.

### 11. CC Plot — Multiple Fixes
a) X vs Z line: MUST BE CYAN, currently gray:
   ```python
   colors = {'XY': 'black', 'XZ': 'cyan', 'YZ': 'magenta'}
   ```
   (Read MATLAB `plotCC.m` for exact color definitions and legend labels)

b) X-axis ticks: every 5 units (MATLAB): `ax.set_xticks(range(-30, 31, 5))`

c) Threshold lines: bright red dashed, prominent:
   ```python
   ax.axhline(threshold, color='red', linestyle='--', linewidth=1.0)
   ax.axhline(-threshold, color='red', linestyle='--', linewidth=1.0)
   ```
   CC threshold = 0.3 / cc_factor

d) Read `plotCC.m` and `calcCC.m` from MATLAB source and replicate exactly.

### 12. CH Plot — Apply Standard Fixes
Read `plotCH.m` from `/root/data-processing/` and replicate tick labels, colors, line styles.
Apply tick direction, full box, bold title/labels.

---

## Working Method

1. Read EACH MATLAB function from `/root/data-processing/Functions/` and
   `/root/data-processing/Resonance Functions/` before modifying its Python equivalent.
2. Fix one function at a time. After each fix, run the full pipeline and update PROGRESS.md.
3. After all fixes, run `compare/run_comparison.py`. Fix anything still failing.
4. Run `python3 -m pytest tests/ -v` and fix any broken tests.
5. Commit when all checks pass.

## Do NOT
- Modify or delete anything in `_matlab_baseline/`
- Change the MATLAB source files in `/root/data-processing/`
- Break existing passing functionality

## PROGRESS.md
Update after each fix. If you restart, read PROGRESS.md first to know where you left off.

## Files to Read Before Starting
1. `/root/data-processing/Functions/plotTH.m` — TH plot details (yLim logic, colors, line styles)
2. `/root/data-processing/Functions/plotTRS.m` — TRS plot details (all lines, ticks, colors)
3. `/root/data-processing/Functions/plotCC.m` — CC colors, threshold, tick labels
4. `/root/data-processing/Functions/plotCH.m` — CH details
5. `/root/data-processing/Resonance Functions/plotTransfer.m` — transmissibility plot
6. `/root/data-processing/Functions/saveTRS.m` — Excel layout and header rows
7. `/root/data-processing/Functions/filterData.m` — understand filter presets
8. `examples/WCC_Booster/seismic_config.yaml` — current (incorrect) filter values to update

## Summary of Files to Modify
- `examples/WCC_Booster/seismic_config.yaml` — filter values, tall dimensions
- `functions/parse_csv.py` — fence-post fix (include endpoint row)
- `functions/save_trs.py` — Z column position, header rows, annotation cells
- `functions/save_plot.py` — remove bbox_inches='tight', set exact DPI
- `functions/plot_th.py` — blue Arig lines, x/y range, figure height, tick direction, box
- `functions/plot_trs.py` — custom tick labels, 0.9*RRS red, figure height, tick direction
- `functions/plot_trs_all.py` — same tick/box fixes
- `functions/plot_transfer.py` — peak detection, x/y range, grid dotted, tick direction
- `functions/plot_cc.py` — cyan color for XZ, x-ticks every 5, threshold lines
- `functions/plot_ch.py` — tick direction, box, labels
- `run_resonance.py` — fix column order in resonance trimmed CSV output
- `compare/run_comparison.py` — CREATE THIS (comparison/validation script)
