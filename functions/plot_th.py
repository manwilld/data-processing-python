"""Time history plot."""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from . import plot_style as S


def plot_th(run_name, accel_name, time, accel, Arig_90, plot_options):
    """Create time history plot matching MATLAB plotTH.m output."""
    TH_factor = np.max(np.abs(accel)) / Arig_90 if Arig_90 > 0 else float('inf')
    print(f'TH factor for {accel_name} = {TH_factor:.2f}')

    # --- Figure size (from plot_style; YAML config can override) ---
    wide      = plot_options.get('wide', S.FIG_WIDTH)
    is_table  = 'Table' in accel_name
    tall      = plot_options.get('tall_th_table' if is_table else 'tall_th_uut',
                                 S.FIG_TALL_TH_TABLE if is_table else S.FIG_TALL_TH_UUT)
    font_name = plot_options.get('font_name', S.FONT_FAMILY)

    # --- Y-axis range and ticks (matching MATLAB plotTH.m logic) ---
    accel_max = np.max(np.abs(accel))
    upper_y   = max(accel_max, 1.1 * Arig_90)

    if upper_y <= 1:
        increment = 0.5
    elif upper_y <= 3:
        increment = 1
    elif upper_y <= 6:
        increment = 2
    elif upper_y <= 12:
        increment = 3
    elif upper_y <= 25:
        increment = 5
    else:
        increment = 10

    y_limit = int(np.ceil((1.1 * max(accel_max, Arig_90)) / increment) * increment)
    y_max   = 1.1 * y_limit
    y_ticks = np.arange(-y_limit, y_limit + increment / 2, increment)

    # --- Figure and axes ---
    fig = plt.figure(figsize=(wide, tall))
    fig.patch.set_facecolor(S.BG_FIGURE)
    ax = fig.add_subplot(111)
    ax.set_facecolor(S.BG_AXES)

    # --- Signal trace ---
    ax.plot(time, accel, color=S.TH_SIGNAL_COLOR, linewidth=S.TH_SIGNAL_LW)

    # --- Arig_90 threshold lines (Table channels only) ---
    if is_table:
        ax.axhline(y= Arig_90, color=S.TH_ARIG_COLOR,
                   linestyle=S.TH_ARIG_STYLE, linewidth=S.TH_ARIG_LW)
        ax.axhline(y=-Arig_90, color=S.TH_ARIG_COLOR,
                   linestyle=S.TH_ARIG_STYLE, linewidth=S.TH_ARIG_LW)

        # Arig_90 value annotation (matching MATLAB y_offset logic)
        if y_limit / Arig_90 > 20:
            y_offset = 3
        elif y_limit / Arig_90 > 5:
            y_offset = 2
        elif y_limit / Arig_90 > 2:
            y_offset = 1.5
        else:
            y_offset = 1.2
        ax.text(0.3,  y_offset * Arig_90, f'{Arig_90}',
                color=S.TH_ARIG_TEXT_COLOR, ha='left', fontsize=S.FONT_SIZE_TICKS)
        ax.text(0.3, -y_offset * Arig_90, f'{-Arig_90}',
                color=S.TH_ARIG_TEXT_COLOR, ha='left', fontsize=S.FONT_SIZE_TICKS)

    # --- Grid ---
    ax.grid(S.TH_GRID)

    # --- Title and labels ---
    title_text = f"Time History: {accel_name.replace('_', ' ')} ({run_name.replace('_', ' ')})"
    ax.set_title(title_text, fontname=font_name,
                 fontsize=S.FONT_SIZE_TITLE, fontweight=S.FONT_WEIGHT_TITLE)
    ax.set_ylabel('Acceleration (g)', fontname=font_name, fontsize=S.FONT_SIZE_AXES)
    ax.set_xlabel('Time (s)',          fontname=font_name, fontsize=S.FONT_SIZE_AXES)

    # --- Axis ranges and ticks ---
    ax.set_xlim(S.TH_X_LIM)
    ax.set_ylim([-y_max, y_max])
    ax.set_xticks(S.TH_X_TICKS)
    ax.set_yticks(y_ticks)

    # --- Tick style: inward on all 4 sides ---
    ax.tick_params(axis='both', which='both', direction=S.TICK_DIRECTION,
                   top=S.TICK_TOP, right=S.TICK_RIGHT,
                   length=S.TICK_MAJOR_LENGTH, width=S.TICK_MAJOR_WIDTH,
                   labelsize=S.FONT_SIZE_TICKS)
    ax.spines['top'].set_visible(True)
    ax.spines['right'].set_visible(True)

    # --- Max acceleration annotation (bottom right) ---
    ax.text(time[-1], -y_limit, f'Max. Accel. = {accel_max:.2f}g ',
            ha='right', va='bottom', fontname=font_name,
            color=S.TH_ANNOT_COLOR, fontsize=S.FONT_SIZE_TICKS)

    # --- Margins (pixel-based: top=33px, bottom=64px, measured from MATLAB baseline) ---
    fig.subplots_adjust(
        left   = S.MARGINS_LEFT,
        right  = S.MARGINS_RIGHT,
        top    = 1 - S.MARGINS_TH_TOP_PX / tall / S.FIG_DPI,
        bottom = 1 - (tall * S.FIG_DPI - S.MARGINS_TH_BOTTOM_PX) / tall / S.FIG_DPI,
    )
    return fig
