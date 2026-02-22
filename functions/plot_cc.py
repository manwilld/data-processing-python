"""Cross-correlation plot matching MATLAB plotCC.m."""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from . import plot_style as S


def plot_cc(cc_result, run_name, plot_options):
    """Create cross-correlation plot matching MATLAB plotCC.m output."""
    # --- Figure size ---
    wide      = plot_options.get('wide', S.FIG_WIDTH)
    tall      = plot_options.get('tall_cc', S.FIG_TALL_CC)
    font_name = plot_options.get('font_name', S.FONT_FAMILY)

    # --- X ticks (range from CC_X_LIM with step CC_X_TICK_STEP) ---
    x_ticks = list(range(S.CC_X_LIM[0], S.CC_X_LIM[1] + 1, S.CC_X_TICK_STEP))

    # --- Figure and axes ---
    fig = plt.figure(figsize=(wide, tall))
    fig.patch.set_facecolor(S.BG_FIGURE)
    ax = fig.add_subplot(111)
    ax.set_facecolor(S.BG_AXES)

    # --- Correlation pair traces ---
    legend_entries = []
    for k, pair in enumerate(cc_result['pairs']):
        color = S.CC_CH_PAIR_COLORS[k % len(S.CC_CH_PAIR_COLORS)]
        ax.plot(pair['lag_time'], pair['corr'], color, linewidth=S.CC_SIGNAL_LW)
        legend_entries.append(pair['axes'])

    # --- Threshold lines (±CC_THRESHOLD, red dashed) ---
    if cc_result['pairs']:
        lag = cc_result['pairs'][0]['lag_time']
        ax.plot([lag[0], lag[-1]], [ S.CC_THRESHOLD,  S.CC_THRESHOLD],
                color=S.CC_THRESHOLD_COLOR, linestyle=S.CC_THRESHOLD_STYLE,
                linewidth=S.CC_THRESHOLD_LW)
        ax.plot([lag[0], lag[-1]], [-S.CC_THRESHOLD, -S.CC_THRESHOLD],
                color=S.CC_THRESHOLD_COLOR, linestyle=S.CC_THRESHOLD_STYLE,
                linewidth=S.CC_THRESHOLD_LW)

    # --- Grid ---
    ax.grid(True, which='major', color=S.CC_GRID_COLOR, linewidth=S.CC_GRID_LW)

    # --- Axis ranges and ticks ---
    ax.set_xlim(S.CC_X_LIM)
    ax.set_ylim(S.CC_Y_LIM)
    ax.set_xticks(x_ticks)
    ax.set_yticks(S.CC_Y_TICKS)

    # --- Title and labels ---
    title = f"Cross Correlation ({run_name.replace('_', ' ')})"
    ax.set_title(title, fontname=font_name,
                 fontsize=S.FONT_SIZE_TITLE, fontweight=S.FONT_WEIGHT_TITLE)
    ax.legend(legend_entries, loc='upper left', fontsize=S.FONT_SIZE_LEGEND_CC_CH)

    max_cc = cc_result['max_cc']
    xlabel_text = (f'{"":>46s}Time Lag (s) '
                   f'{"":>11s}Max. Corr. = {max_cc:.2f}')
    ax.set_xlabel(xlabel_text, fontname=font_name,
                  fontsize=S.FONT_SIZE_AXES, fontweight='bold')
    ax.set_ylabel('Correlation', fontname=font_name,
                  fontsize=S.FONT_SIZE_AXES, fontweight='bold')

    # --- Tick style ---
    ax.tick_params(axis='both', which='both', direction=S.TICK_DIRECTION,
                   top=S.TICK_TOP, right=S.TICK_RIGHT,
                   length=S.TICK_MAJOR_LENGTH, width=S.TICK_MAJOR_WIDTH,
                   labelsize=S.FONT_SIZE_TICKS)
    ax.spines['top'].set_visible(True)
    ax.spines['right'].set_visible(True)

    # --- Margins ---
    fig.subplots_adjust(
        left=S.MARGINS_LEFT, right=S.MARGINS_RIGHT,
        top=S.MARGINS_CC_TOP, bottom=S.MARGINS_CC_BOTTOM,
    )
    return fig
