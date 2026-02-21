"""Time history plot."""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def plot_th(run_name, accel_name, time, accel, Arig_90, plot_options):
    """Create time history plot matching MATLAB plotTH.m output."""
    TH_factor = np.max(np.abs(accel)) / Arig_90 if Arig_90 > 0 else float('inf')
    print(f'TH factor for {accel_name} = {TH_factor:.2f}')

    wide = plot_options.get('wide', 6.5)
    is_table = 'Table' in accel_name
    if is_table:
        tall = plot_options.get('tall_th_table', 2.0)
    else:
        tall = plot_options.get('tall_th_uut', 1.8)
    font_name = plot_options.get('font_name', 'Arial')
    font_size_title = plot_options.get('font_size_title', 11)
    font_size_axes = plot_options.get('font_size_axes', 11)
    font_size_ticks = plot_options.get('font_size_ticks', 10)

    accel_max = np.max(np.abs(accel))
    upper_y = max(accel_max, 1.1 * Arig_90)

    # Determine y-tick increment (matching MATLAB plotTH.m)
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

    x_ticks = [0, 5, 10, 15, 20, 25, 30, 35]
    y_limit = int(np.ceil((1.1 * max(accel_max, Arig_90)) / increment) * increment)
    y_max = 1.1 * y_limit
    y_ticks = np.arange(-y_limit, y_limit + increment / 2, increment)

    fig = plt.figure(figsize=(wide, tall))
    fig.patch.set_facecolor('white')
    ax = fig.add_subplot(111)
    ax.set_facecolor('white')

    ax.plot(time, accel, 'k', linewidth=1)

    if is_table:
        ax.axhline(y=Arig_90, color='blue', linestyle='--', linewidth=1.0)
        ax.axhline(y=-Arig_90, color='blue', linestyle='--', linewidth=1.0)

        # Text position (matching MATLAB y_offset logic)
        if y_limit / Arig_90 > 20:
            y_offset = 3
        elif y_limit / Arig_90 > 5:
            y_offset = 2
        elif y_limit / Arig_90 > 2:
            y_offset = 1.5
        else:
            y_offset = 1.2
        ax.text(0.3, y_offset * Arig_90, f'{Arig_90}', color='blue',
                ha='left', fontsize=font_size_ticks)
        ax.text(0.3, -y_offset * Arig_90, f'{-Arig_90}', color='blue',
                ha='left', fontsize=font_size_ticks)

    ax.grid(True)
    title_text = f"Time History: {accel_name.replace('_', ' ')} ({run_name.replace('_', ' ')})"
    ax.set_title(title_text, fontname=font_name, fontsize=font_size_title,
                 fontweight='bold')
    ax.set_xlim([0, time[-1]])
    ax.set_ylim([-y_max, y_max])
    ax.set_xticks(x_ticks)
    ax.set_yticks(y_ticks)
    ax.set_ylabel('Acceleration (g)', fontname=font_name, fontsize=font_size_axes,
                   fontweight='bold')
    ax.set_xlabel('Time (s)', fontname=font_name, fontsize=font_size_axes,
                   fontweight='bold')

    # Tick direction: inward on all 4 sides, full box
    ax.tick_params(axis='both', which='both', direction='in',
                   top=True, right=True, length=4, width=0.5,
                   labelsize=font_size_ticks)
    ax.spines['top'].set_visible(True)
    ax.spines['right'].set_visible(True)

    # Max acceleration text at bottom right
    ax.text(time[-1], -y_limit, f'Max. Accel. = {accel_max:.2f}g ',
            ha='right', va='bottom', fontname=font_name, fontsize=font_size_ticks)

    # Margins measured from MATLAB baseline: 33px top, 64px bottom, 127px left, 94px right
    fig.subplots_adjust(left=0.130, right=0.904, top=1-33/tall/150, bottom=1-(tall*150-64)/tall/150)
    return fig
