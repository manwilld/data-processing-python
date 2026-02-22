"""Plot formatting configuration for data-processing-python.

This is the single source of truth for all plot appearance.
Edit values here to change how plots look across the entire pipeline.

ORGANIZATION
  FONT             — family, sizes
  FIGURE SIZE      — width, heights per plot type, DPI
  MARGINS          — subplots_adjust per plot type
  BACKGROUND       — figure and axes colors
  TICK STYLE       — direction, length, width, top/right visibility
  GRID             — on/off, color, linewidth per plot type
  TRS / TRS_ALL    — curve colors, linewidths, reference lines
  TIME HISTORY     — signal color, Arig threshold lines, annotations
  CC / CH          — pair colors, signal weights, threshold lines
  RESONANCE        — transmissibility curve, peak marker
  AXIS RANGES      — x/y limits and tick values per plot type
"""

import matplotlib
import matplotlib.font_manager as fm
import warnings


# ──────────────────────────────────────────────────────────────────────────────
# FONT
# ──────────────────────────────────────────────────────────────────────────────

FONT_FAMILY = 'Arial'          # Preferred font. Falls back to Liberation Sans → DejaVu Sans.
                               # Change to match whatever font you have installed.

FONT_SIZE_TITLE  = 11          # Plot title
FONT_SIZE_AXES   = 11          # Axis labels (x and y)
FONT_SIZE_TICKS  = 10          # Tick mark labels
FONT_SIZE_TEXT   =  7          # In-plot annotations (Aflx=, Arig=, nat freq label)
FONT_SIZE_LEGEND =  6          # Legend (TRS and TRS overlay plots)
FONT_SIZE_LEGEND_CC_CH = 7     # Legend (CC and CH plots — MATLAB uses slightly larger)

FONT_WEIGHT_TITLE = 'bold'     # Title weight: 'bold' or 'normal'
FONT_WEIGHT_AXES  = 'normal'   # Axis label weight ('bold' on CC/CH/resonance, 'normal' on TRS/TH)
                               # Note: MATLAB is inconsistent here — CC/CH/resonance use bold,
                               # TRS/TH do not. Override per-plot if you want uniformity.


# ──────────────────────────────────────────────────────────────────────────────
# FIGURE SIZE
# ──────────────────────────────────────────────────────────────────────────────
# All sizes in inches at FIG_DPI. Current values match MATLAB PaperPosition exactly.
#   975 px wide = 6.5 in × 150 DPI
#   405 px tall = 2.70 in × 150 DPI   (TRS, CC, CH, resonance)
#   300 px tall = 2.00 in × 150 DPI   (Table time history)
#   270 px tall = 1.80 in × 150 DPI   (UUT time history)

FIG_DPI           = 150        # Save DPI. Changing this rescales everything.
FIG_WIDTH         = 6.5        # Width of all plots (inches)

FIG_TALL_TRS      = 2.70       # TRS (single axis) and TRS overlay
FIG_TALL_TH_TABLE = 2.00       # Time history — Table channels
FIG_TALL_TH_UUT   = 1.80       # Time history — UUT channels
FIG_TALL_CC       = 2.70       # Cross-correlation
FIG_TALL_CH       = 2.70       # Magnitude squared coherence
FIG_TALL_RES      = 2.70       # Transmissibility (resonance)


# ──────────────────────────────────────────────────────────────────────────────
# MARGINS  (subplots_adjust: fractions of figure size)
# ──────────────────────────────────────────────────────────────────────────────
# Left and right are shared across all plot types (same pixel offsets).
# Top and bottom differ by plot type.
# TH margins are pixel-based (computed dynamically in plot_th.py because
# the figure height varies between table and UUT plots).

MARGINS_LEFT  = 0.130          # Left margin (all plots)
MARGINS_RIGHT = 0.904          # Right margin (all plots)

# TH: top/bottom expressed in pixels (applied as fractions at render time)
MARGINS_TH_TOP_PX    = 33     # Top margin in pixels (Table and UUT share this)
MARGINS_TH_BOTTOM_PX = 64     # Bottom margin in pixels

# Fixed top/bottom for other plot types
MARGINS_TRS_TOP    = 0.880
MARGINS_TRS_BOTTOM = 0.160

MARGINS_CC_TOP     = 0.919
MARGINS_CC_BOTTOM  = 0.160

MARGINS_CH_TOP     = 0.919
MARGINS_CH_BOTTOM  = 0.160

MARGINS_RES_TOP    = 0.880
MARGINS_RES_BOTTOM = 0.160


# ──────────────────────────────────────────────────────────────────────────────
# BACKGROUND
# ──────────────────────────────────────────────────────────────────────────────

BG_FIGURE = 'white'            # Figure background (outside axes)
BG_AXES   = 'white'            # Axes background


# ──────────────────────────────────────────────────────────────────────────────
# TICK STYLE
# ──────────────────────────────────────────────────────────────────────────────

TICK_DIRECTION    = 'in'       # 'in', 'out', or 'inout'
TICK_TOP          = True       # Show ticks on top spine
TICK_RIGHT        = True       # Show ticks on right spine
TICK_MAJOR_LENGTH = 4          # Major tick length (points) — TRS uses 5 (see below)
TICK_MAJOR_WIDTH  = 0.5        # Major tick line width
TICK_MINOR_LENGTH = 3          # Minor tick length (TRS/TRS_all only)
TICK_MINOR_WIDTH  = 0.5        # Minor tick line width

# TRS major ticks are slightly longer than other plots (matching MATLAB)
TICK_MAJOR_LENGTH_TRS = 5


# ──────────────────────────────────────────────────────────────────────────────
# GRID
# ──────────────────────────────────────────────────────────────────────────────

# Time history
TH_GRID = False                # MATLAB has grid on, but cross-engine pixel positions
                               # differ enough to increase mean diff from ~14 to ~24.
                               # Intentionally off. Change to True if you prefer visual
                               # accuracy over pixel-comparison score.

# TRS / TRS overlay
TRS_GRID_MAJOR_COLOR = 'lightgray'
TRS_GRID_MAJOR_LW    = 0.4
TRS_GRID_MINOR_COLOR = 'lightgray'
TRS_GRID_MINOR_LW    = 0.2

# Cross-correlation (CC)
CC_GRID_COLOR = 'lightgray'
CC_GRID_LW    = 0.4

# Coherence (CH)
CH_GRID_LW    = 0.5            # Color not set — matplotlib default

# Resonance / transmissibility (dotted grid matching MATLAB)
RES_GRID_STYLE = ':'
RES_GRID_LW    = 0.5
RES_GRID_COLOR = 'gray'
RES_GRID_ALPHA = 0.7


# ──────────────────────────────────────────────────────────────────────────────
# TRS / TRS_ALL  —  colors, linewidths, reference lines
# ──────────────────────────────────────────────────────────────────────────────

# Main TRS curve (measured data)
TRS_COLOR = 'black'
TRS_LW    = 1.0

# RRS reference spectrum
RRS_COLOR = 'blue'
RRS_LW    = 1.5
RRS_STYLE = '--'

# 0.9 × RRS  (lower bound — TRS must exceed this)
RRS_90_COLOR = 'red'
RRS_90_LW    = 0.5
RRS_90_STYLE = '--'

# 1.3 × RRS  (upper bound callout)
RRS_130_COLOR = 'yellow'
RRS_130_LW    = 0.5
RRS_130_STYLE = '--'

# Aflx / Arig horizontal reference lines  (light blue — MATLAB [0.7 0.7 1])
REF_LINE_COLOR = [0.7, 0.7, 1.0]
REF_LINE_LW    = 0.25
REF_LINE_STYLE = '--'

# lowCutoff vertical reference line  (same light blue)
LOW_CUTOFF_LINE_COLOR = [0.7, 0.7, 1.0]
LOW_CUTOFF_LINE_LW    = 0.25
LOW_CUTOFF_LINE_STYLE = '--'

# Text annotations (Aflx=, Arig=, lowCutoff Hz label)
REF_TEXT_COLOR = 'blue'

# TRS overlay: color per axis
TRS_ALL_COLORS = {
    'X': 'black',
    'Y': 'magenta',
    'Z': 'cyan',
    'D': 'green',
}


# ──────────────────────────────────────────────────────────────────────────────
# TIME HISTORY (TH)
# ──────────────────────────────────────────────────────────────────────────────

TH_SIGNAL_COLOR = 'black'      # Time history trace
TH_SIGNAL_LW    = 1.0

TH_ARIG_COLOR = 'blue'         # ±Arig_90 threshold dashed lines
TH_ARIG_LW    = 1.0
TH_ARIG_STYLE = '--'

TH_ARIG_TEXT_COLOR = 'blue'    # Arig_90 value label (e.g. "1.94")
TH_ANNOT_COLOR     = 'black'   # "Max. Accel. = X.XXg" annotation


# ──────────────────────────────────────────────────────────────────────────────
# CC / CH  —  cross-correlation and coherence
# ──────────────────────────────────────────────────────────────────────────────

# Signal pair colors: [XY, XZ, YZ]  (MATLAB: k, c, m)
CC_CH_PAIR_COLORS = ['k', 'c', 'm']

CC_SIGNAL_LW = 0.5             # Cross-correlation line weight
CH_SIGNAL_LW = 0.75            # Coherence line weight

# CC threshold lines (±0.3 horizontal, red dashed)
CC_THRESHOLD       = 0.3
CC_THRESHOLD_COLOR = 'r'
CC_THRESHOLD_LW    = 1.0
CC_THRESHOLD_STYLE = '--'

# CH threshold line (0.5 horizontal, red dashed)
CH_THRESHOLD       = 0.5
CH_THRESHOLD_COLOR = 'r'
CH_THRESHOLD_LW    = 1.0
CH_THRESHOLD_STYLE = '--'


# ──────────────────────────────────────────────────────────────────────────────
# RESONANCE / TRANSMISSIBILITY
# ──────────────────────────────────────────────────────────────────────────────

RES_CURVE_COLOR = 'black'
RES_CURVE_LW    = 1.0

# Natural frequency peak marker (open circle)
RES_PEAK_COLOR   = 'blue'
RES_PEAK_MARKER  = 'o'
RES_PEAK_SIZE    = 8           # markersize
RES_PEAK_EDGE_LW = 2           # markeredgewidth
RES_PEAK_TEXT_COLOR = 'blue'


# ──────────────────────────────────────────────────────────────────────────────
# AXIS RANGES AND TICK VALUES
# ──────────────────────────────────────────────────────────────────────────────

# TRS / TRS overlay
TRS_X_TICKS = [0.5, 1, 1.3, 8.3, 10, 20, 35]
TRS_X_LIM   = [0.5, 35]
TRS_Y_TICKS = [0.1, 0.5, 1, 5, 10, 50]

# Time history
TH_X_LIM   = [0, 30]
TH_X_TICKS = [0, 5, 10, 15, 20, 25, 30]

# Cross-correlation (CC)
CC_X_TICK_STEP = 5             # x-ticks every N seconds  (ticks = range(-65, 66, step))
CC_X_LIM   = [-65, 65]
CC_Y_TICKS = [-0.5, -0.3, -0.1, 0, 0.1, 0.3, 0.5]
CC_Y_LIM   = [-0.5, 0.5]

# Coherence (CH)
CH_X_TICKS = [1.3, 10, 20, 33.3]
CH_X_LIM   = [1.3, 33.3]
CH_Y_TICKS = [0.0, 0.25, 0.5, 0.75, 1.0]
CH_Y_LIM   = [0, 1]

# Resonance
RES_X_TICKS = [1.3, 5, 10, 20, 30]
RES_X_LIM   = [1.0, 35]
RES_Y_TICKS = [1, 10, 50]
RES_Y_LIM   = [0.3, 55]


# ──────────────────────────────────────────────────────────────────────────────
# FONT DETECTION (runtime — do not edit)
# ──────────────────────────────────────────────────────────────────────────────

def get_best_font(preferred=None):
    """Return the best available font matching preferred (or FONT_FAMILY)."""
    preferred = preferred or FONT_FAMILY
    available = {f.name for f in fm.fontManager.ttflist}
    candidates = [preferred, 'Liberation Sans', 'FreeSans', 'Helvetica',
                  'Nimbus Sans', 'DejaVu Sans', 'sans-serif']
    for font in candidates:
        if font in available:
            return font
    return 'sans-serif'


def setup_plot_style(font_name=None):
    """Configure matplotlib rcParams. Call once at the start of each runner script.

    Parameters
    ----------
    font_name : str or None
        Preferred font. Defaults to FONT_FAMILY if None.

    Returns
    -------
    str
        The font name actually selected (use this when passing font_name to plot functions).
    """
    warnings.filterwarnings('ignore', message='.*findfont.*')
    warnings.filterwarnings('ignore', category=UserWarning,
                            module='matplotlib.font_manager')

    best_font = get_best_font(font_name)

    matplotlib.rcParams.update({
        'font.family':      'sans-serif',
        'font.sans-serif':  [best_font, 'Liberation Sans', 'FreeSans',
                             'DejaVu Sans', 'sans-serif'],
        'axes.unicode_minus': False,
        'figure.dpi':       100,
        'savefig.dpi':      FIG_DPI,
        'svg.fonttype':     'none',    # embed fonts as text in SVG (not paths)
    })

    return best_font
