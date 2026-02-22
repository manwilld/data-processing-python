"""Transmissibility (transfer function) plot matching MATLAB plotTransfer.m."""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from . import plot_style as S


def plot_transfer(run_name, uut, accel_name, axis, axis_uut,
                  frequency, transfer_response, natural_freq,
                  plot_options):
    """Create transmissibility plot matching MATLAB plotTransfer.m output."""
    # --- Figure size ---
    wide      = plot_options.get('wide', S.FIG_WIDTH)
    tall      = plot_options.get('tall_res', S.FIG_TALL_RES)
    font_name = plot_options.get('font_name', S.FONT_FAMILY)

    # --- Figure and axes ---
    fig = plt.figure(figsize=(wide, tall))
    fig.patch.set_facecolor(S.BG_FIGURE)
    ax = fig.add_subplot(111)
    ax.set_facecolor(S.BG_AXES)

    ax.set_xscale('log')
    ax.set_yscale('log')

    # --- Grid (dotted, matching MATLAB) ---
    ax.grid(True, which='major',
            linestyle=S.RES_GRID_STYLE, linewidth=S.RES_GRID_LW,
            color=S.RES_GRID_COLOR, alpha=S.RES_GRID_ALPHA)
    ax.grid(False, which='minor')

    # --- Transmissibility curve (ax.plot not loglog — avoids formatter reset) ---
    ax.plot(frequency, transfer_response,
            color=S.RES_CURVE_COLOR, linewidth=S.RES_CURVE_LW)

    # --- Natural frequency peak marker ---
    # Config value is a search hint only; actual peak auto-detected from data.
    if natural_freq is not None and natural_freq > 0:
        peak_idx       = np.argmax(transfer_response)
        nat_freq_actual = frequency[peak_idx]
        nat_freq_value  = transfer_response[peak_idx]

        ax.plot(nat_freq_actual, nat_freq_value,
                color=S.RES_PEAK_COLOR, marker=S.RES_PEAK_MARKER,
                markersize=S.RES_PEAK_SIZE, markeredgewidth=S.RES_PEAK_EDGE_LW,
                markerfacecolor='none')

        label_text = f'{np.ceil(nat_freq_actual * 10) / 10:.1f}-Hz'
        ax.text(nat_freq_actual * np.exp(-0.1), nat_freq_value, label_text,
                ha='right', va='bottom', fontname=font_name,
                fontsize=S.FONT_SIZE_TEXT, color=S.RES_PEAK_TEXT_COLOR)

    # --- Axis limits ---
    ax.set_xlim(S.RES_X_LIM)
    ax.set_ylim(S.RES_Y_LIM)

    # ── Tick labels set AFTER all plotting (prevents loglog formatter reset) ───
    ax.set_xticks(S.RES_X_TICKS)
    ax.xaxis.set_major_formatter(ticker.FixedFormatter([str(t) for t in S.RES_X_TICKS]))
    ax.xaxis.set_minor_locator(ticker.NullLocator())

    ax.set_yticks(S.RES_Y_TICKS)
    ax.yaxis.set_major_formatter(ticker.FixedFormatter([str(t) for t in S.RES_Y_TICKS]))
    ax.yaxis.set_minor_locator(ticker.NullLocator())

    ax.tick_params(axis='both', which='both', direction=S.TICK_DIRECTION,
                   top=S.TICK_TOP, right=S.TICK_RIGHT,
                   length=S.TICK_MAJOR_LENGTH, width=S.TICK_MAJOR_WIDTH,
                   labelsize=S.FONT_SIZE_TICKS)
    ax.spines['top'].set_visible(True)
    ax.spines['right'].set_visible(True)

    # --- Title and labels ---
    title = (f"Transmissibility: {uut.replace('_', ' ')} "
             f"({accel_name.replace('_', ' ')}) {axis_uut} / Table {axis}")
    ax.set_title(title, fontsize=S.FONT_SIZE_TITLE, fontweight=S.FONT_WEIGHT_TITLE)
    ax.set_xlabel('Frequency (Hz)', fontsize=S.FONT_SIZE_AXES, fontweight='bold')
    ax.set_ylabel('Ratio (g/g)',    fontsize=S.FONT_SIZE_AXES, fontweight='bold')

    # --- Margins ---
    fig.subplots_adjust(
        left=S.MARGINS_LEFT, right=S.MARGINS_RIGHT,
        top=S.MARGINS_RES_TOP, bottom=S.MARGINS_RES_BOTTOM,
    )
    return fig
