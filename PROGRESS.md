# Progress

## Phase 1: Config schema + example configs + requirements.txt
- [x] Created directory structure
- [x] Created requirements.txt
- [x] Created example configs (seismic + resonance)

## Phase 2: Core math modules + tests
- [x] calc_trs.py - Smallwood TRS algorithm
- [x] calc_seismic_parameters.py - ASCE7-16/22 parameters, freq72, RRS
- [x] optimize_trs.py - 1/6 octave optimization with analyzeSet
- [x] filter_data.py - Butterworth lowpass filtfilt
- [x] calc_cc.py - Cross-correlation
- [x] calc_ch.py - Magnitude squared coherence
- [x] Tests (15 tests, all passing)

## Phase 3: CSV parsing
- [x] parse_csv.py - Seismic + resonance CSV parsing

## Phase 4: Plotting
- [x] plot_th.py - Time history
- [x] plot_trs.py - TRS vs RRS (single accel)
- [x] plot_trs_all.py - TRS all-axes overlay
- [x] plot_transfer.py - Transmissibility plot
- [x] plot_cc.py - Cross-correlation plot
- [x] plot_ch.py - Coherence plot
- [x] save_plot.py - SVG + PNG output

## Phase 5: Excel output
- [x] save_trs.py - TRS vs RRS Excel table

## Phase 6: Runner scripts
- [x] run_seismic.py - End-to-end seismic processing (37 plots + Excel)
- [x] run_resonance.py - End-to-end resonance processing (12 plots)

## Verification
- [x] All 15 unit tests pass
- [x] Seismic pipeline produces 37 SVG + 37 PNG + 1 Excel
- [x] Resonance pipeline produces 12 SVG + 12 PNG per UUT pair
- [x] Output structure matches MATLAB example project
