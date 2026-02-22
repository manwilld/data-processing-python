"""Coherence plot matching MATLAB plotCH.m."""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from . import plot_style as S


def plot_ch(ch_result, run_name, plot_options):
    """Create magnitude squared coherence plot matching MATLAB plotCH.m output."""
    # --- Figure size ---
    wide      = plot_options.get('wide', S.FIG_WIDTH)
    tall      = plot_options.get('tall_ch', S.FIG_TALL_CH)
    font_name = plot_options.get('font_name', S.FONT_FAMILY)

    # --- Figure and axes ---
    fig = plt.figure(figsize=(wide, tall))
    fig.patch.set_facecolor(S.BG_FIGURE)
    ax = fig.add_subplot(111)
    ax.set_facecolor(S.BG_AXES)

    ax.set_xscale('log')
    ax.set_xticks(S.CH_X_TICKS)
    ax.set_xticklabels([str(t) for t in S.CH_X_TICKS], fontsize=S.FONT_SIZE_TICKS)

    # --- Coherence pair traces ---
    legend_entries = []
    for k, pair in enumerate(ch_result['pairs']):
        color = S.CC_CH_PAIR_COLORS[k % len(S.CC_CH_PAIR_COLORS)]
        ax.semilogx(pair['frequencies'], pair['coherence'], color,
                    linewidth=S.CH_SIGNAL_LW)
        legend_entries.append(pair['axes'])

    # --- Threshold line ---
    if ch_result['pairs']:
        f = ch_result['pairs'][0]['frequencies']
        ax.semilogx([f[0], f[-1]], [S.CH_THRESHOLD, S.CH_THRESHOLD],
                    color=S.CH_THRESHOLD_COLOR, linestyle=S.CH_THRESHOLD_STYLE,
                    linewidth=S.CH_THRESHOLD_LW)

    # --- Axis limits ---
    ax.set_xlim(S.CH_X_LIM)
    ax.set_ylim(S.CH_Y_LIM)
    ax.set_yticks(S.CH_Y_TICKS)

    # --- Grid ---
    ax.grid(True, which='major', linewidth=S.CH_GRID_LW)

    # --- Title and labels ---
    title = f"Magnitude Squared Coherence ({run_name.replace('_', ' ')})"
    ax.set_title(title, fontname=font_name,
                 fontsize=S.FONT_SIZE_TITLE, fontweight=S.FONT_WEIGHT_TITLE)
    ax.legend(legend_entries, loc='upper left', fontsize=S.FONT_SIZE_LEGEND_CC_CH)

    max_ch = ch_result['max_ch']
    xlabel_text = (f'{"":>46s}Frequency (Hz) '
                   f'{"":>11s}Max. Coher. = {max_ch:.2f}')
    ax.set_xlabel(xlabel_text, fontname=font_name,
                  fontsize=S.FONT_SIZE_AXES, fontweight='bold')
    ax.set_ylabel('Coherence', fontname=font_name,
                  fontsize=S.FONT_SIZE_AXES, fontweight='bold')

    # --- Tick style ---
    ax.tick_params(axis='both', which='both', direction=S.TICK_DIRECTION,
                   top=S.TICK_TOP, right=S.TICK_RIGHT,
                   length=S.TICK_MAJOR_LENGTH, width=S.TICK_MAJOR_WIDTH)
    ax.spines['top'].set_visible(True)
    ax.spines['right'].set_visible(True)

    # --- Margins ---
    fig.subplots_adjust(
        left=S.MARGINS_LEFT, right=S.MARGINS_RIGHT,
        top=S.MARGINS_CH_TOP, bottom=S.MARGINS_CH_BOTTOM,
    )
    return fig
