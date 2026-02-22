"""TRS vs RRS all-axes overlay plot matching MATLAB style."""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from . import plot_style as S


def plot_trs_all(run_name, accel_name, axes, freq72, RRS_h, RRS_v,
                 Aflx_h, Aflx_v, Arig_h, Arig_v, damping, low_cutoff,
                 freq06_dict, TRS06_dict, plot_options):
    """Create TRS vs RRS overlay plot for all axes."""
    # --- Figure size ---
    wide      = plot_options.get('wide', S.FIG_WIDTH)
    tall      = plot_options.get('tall_trs', S.FIG_TALL_TRS)
    font_name = plot_options.get('font_name', S.FONT_FAMILY)

    # --- Y-axis range ---
    max_trs  = max((np.max(TRS06_dict[a]) for a in axes if a in TRS06_dict), default=1.0)
    is_table = 'Table' in accel_name
    upper_y  = max(max_trs, 1.3 * Aflx_h)

    if upper_y < 3:
        y_max = 4
    elif upper_y < 5:
        y_max = 6.5
    elif upper_y < 7.5:
        y_max = 9
    elif upper_y < 10:
        y_max = 12
    else:
        y_max = np.ceil(max_trs * 1.2)

    y_min = min(np.floor(Arig_v * 0.85 * 10) / 10, 0.9)

    # --- Figure and axes ---
    fig = plt.figure(figsize=(wide, tall))
    fig.patch.set_facecolor(S.BG_FIGURE)
    ax = fig.add_subplot(111)
    ax.set_facecolor(S.BG_AXES)

    ax.set_xscale('log')
    ax.set_yscale('log')

    # ── TRS curves per axis ────────────────────────────────────────────────────
    for axis in axes:
        if axis in freq06_dict and axis in TRS06_dict:
            color = S.TRS_ALL_COLORS.get(axis, 'black')
            ax.plot(freq06_dict[axis], TRS06_dict[axis],
                    color=color, linewidth=S.TRS_LW, label=f'TRS_{axis}')

    if is_table:
        # RRS horizontal and vertical
        ax.plot(freq72, RRS_h,
                color=S.RRS_COLOR, linestyle=S.RRS_STYLE, linewidth=S.RRS_LW,
                label='RRS_h')
        ax.plot(freq72, RRS_v,
                color=S.RRS_COLOR, linestyle=S.RRS_STYLE, linewidth=S.RRS_LW,
                label='RRS_v')
        ax.plot(freq72, 0.9 * RRS_h,
                color=S.RRS_90_COLOR, linestyle=S.RRS_90_STYLE, linewidth=S.RRS_90_LW)
        ax.plot(freq72, 0.9 * RRS_v,
                color=S.RRS_90_COLOR, linestyle=S.RRS_90_STYLE, linewidth=S.RRS_90_LW)
        ax.plot(freq72, 1.3 * RRS_h,
                color=S.RRS_130_COLOR, linestyle=S.RRS_130_STYLE, linewidth=S.RRS_130_LW)

        # Aflx_h — text + light blue line (left segment)
        ax.plot([freq72[0], 1.3], [Aflx_h, Aflx_h],
                color=S.REF_LINE_COLOR, linestyle=S.REF_LINE_STYLE, linewidth=S.REF_LINE_LW)
        ax.text(S.TRS_X_LIM[0] * 1.1, Aflx_h, f'Aflx_h = {Aflx_h:.2f}',
                color=S.REF_TEXT_COLOR, ha='left', va='top', fontsize=S.FONT_SIZE_TEXT)

        # Aflx_v — text + light blue line (left segment)
        ax.plot([freq72[0], 1.3], [Aflx_v, Aflx_v],
                color=S.REF_LINE_COLOR, linestyle=S.REF_LINE_STYLE, linewidth=S.REF_LINE_LW)
        ax.text(S.TRS_X_LIM[0] * 1.1, Aflx_v, f'Aflx_v = {Aflx_v:.2f}',
                color=S.REF_TEXT_COLOR, ha='left', va='bottom', fontsize=S.FONT_SIZE_TEXT)

        # Arig_h — text + light blue line (right segment)
        ax.plot([8.3, freq72[-1]], [Arig_h, Arig_h],
                color=S.REF_LINE_COLOR, linestyle=S.REF_LINE_STYLE, linewidth=S.REF_LINE_LW)
        ax.text(10, Arig_h, f'Arig_h = {Arig_h:.2f}',
                color=S.REF_TEXT_COLOR, ha='left', va='top', fontsize=S.FONT_SIZE_TEXT)

        # Arig_v — text + light blue line (right segment)
        ax.plot([8.3, freq72[-1]], [Arig_v, Arig_v],
                color=S.REF_LINE_COLOR, linestyle=S.REF_LINE_STYLE, linewidth=S.REF_LINE_LW)
        ax.text(10, Arig_v, f'Arig_v = {Arig_v:.2f}',
                color=S.REF_TEXT_COLOR, ha='left', va='bottom', fontsize=S.FONT_SIZE_TEXT)

        # Low cutoff — vertical light blue line + blue text
        ax.plot([low_cutoff, low_cutoff], [0.1, 100],
                color=S.LOW_CUTOFF_LINE_COLOR, linestyle=S.LOW_CUTOFF_LINE_STYLE,
                linewidth=S.LOW_CUTOFF_LINE_LW)
        ax.text(low_cutoff, y_min, f' {low_cutoff:.1f}-Hz Lower Limit',
                color=S.REF_TEXT_COLOR, ha='left', va='bottom', fontsize=S.FONT_SIZE_TEXT)

    # --- Axis limits ---
    ax.set_xlim(S.TRS_X_LIM)
    ax.set_ylim([y_min, y_max])

    # --- Grid ---
    ax.grid(True, which='major', color=S.TRS_GRID_MAJOR_COLOR, linewidth=S.TRS_GRID_MAJOR_LW)
    ax.grid(True, which='minor', color=S.TRS_GRID_MINOR_COLOR, linewidth=S.TRS_GRID_MINOR_LW)

    # ── Tick labels set AFTER all plotting ────────────────────────────────────
    ax.set_xticks(S.TRS_X_TICKS)
    ax.xaxis.set_major_formatter(ticker.FixedFormatter([str(t) for t in S.TRS_X_TICKS]))
    ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())

    ax.set_yticks(S.TRS_Y_TICKS)
    ax.yaxis.set_major_formatter(ticker.FixedFormatter([str(t) for t in S.TRS_Y_TICKS]))
    ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())

    ax.tick_params(axis='both', which='major', direction=S.TICK_DIRECTION,
                   top=S.TICK_TOP, right=S.TICK_RIGHT,
                   length=S.TICK_MAJOR_LENGTH_TRS, width=S.TICK_MAJOR_WIDTH,
                   labelsize=S.FONT_SIZE_TICKS)
    ax.tick_params(axis='both', which='minor', direction=S.TICK_DIRECTION,
                   top=S.TICK_TOP, right=S.TICK_RIGHT,
                   length=S.TICK_MINOR_LENGTH, width=S.TICK_MINOR_WIDTH)
    ax.spines['top'].set_visible(True)
    ax.spines['right'].set_visible(True)

    # --- Title and labels ---
    if is_table:
        title = (f"TRS vs. RRS: {accel_name.replace('_', ' ')} "
                 f"({run_name.replace('_', ' ')})")
    else:
        title = f"TRS: {accel_name.replace('_', ' ')} ({run_name.replace('_', ' ')})"
    ax.set_title(title, fontsize=S.FONT_SIZE_TITLE, fontweight=S.FONT_WEIGHT_TITLE)

    ax.set_xlabel('Frequency (Hz)', fontsize=S.FONT_SIZE_AXES)
    ax.set_ylabel(f'Spectral Acceleration (g)\n{int(damping * 100)}% Damping',
                  fontsize=S.FONT_SIZE_AXES)
    ax.legend(loc='upper left', fontsize=S.FONT_SIZE_LEGEND, frameon=True)

    # --- Margins ---
    fig.subplots_adjust(
        left=S.MARGINS_LEFT, right=S.MARGINS_RIGHT,
        top=S.MARGINS_TRS_TOP, bottom=S.MARGINS_TRS_BOTTOM,
    )
    return fig
