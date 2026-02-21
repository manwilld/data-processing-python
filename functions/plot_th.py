"""Time history plot."""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def plot_th(run_name, accel_name, time, accel, Arig_90, plot_options):
    """Create time history plot.

    Parameters
    ----------
    run_name : str
    accel_name : str
    time : array-like
    accel : array-like
    Arig_90 : float
        90% of Arig (horizontal or vertical).
    plot_options : dict

    Returns
    -------
    matplotlib.figure.Figure
    """
    TH_factor = np.max(np.abs(accel)) / Arig_90 if Arig_90 > 0 else float('inf')
    print(f'TH factor for {accel_name} = {TH_factor:.2f}')

    wide = plot_options.get('wide', 6.5)
    is_table = 'Table' in accel_name
    if is_table:
        tall = plot_options.get('tall_th', 2.0)
    else:
        tall = plot_options.get('tall_th_unit', 1.8)
    font_name = plot_options.get('font_name', 'Arial')
    font_size_title = plot_options.get('font_size_title', 11)
    font_size_axes = plot_options.get('font_size_axes', 11)
    font_size_ticks = plot_options.get('font_size_ticks', 10)

    accel_max = np.max(np.abs(accel))
    upper_y = max(accel_max, 1.1 * Arig_90)

    # Determine y-tick increment
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
    y_limit = np.ceil((1.1 * max(accel_max, Arig_90)) / increment) * increment
    y_max = 1.1 * y_limit
    y_ticks = np.arange(-y_limit, y_limit + increment / 2, increment)

    fig, ax = plt.subplots(figsize=(wide, tall))
    ax.set_box_aspect(None)

    ax.plot(time, accel, 'k', linewidth=1)

    if is_table:
        ax.axhline(y=Arig_90, color='b', linestyle='--', linewidth=0.5)
        ax.axhline(y=-Arig_90, color='b', linestyle='--', linewidth=0.5)

        # Text position
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
    ax.set_title(title_text, fontname=font_name, fontsize=font_size_title)
    ax.set_xlim([0, time[-1]])
    ax.set_ylim([-y_max, y_max])
    ax.set_xticks(x_ticks)
    ax.set_yticks(y_ticks)
    ax.tick_params(labelsize=font_size_ticks)
    ax.set_ylabel('Acceleration (g)', fontname=font_name, fontsize=font_size_axes)
    ax.set_xlabel('Time (s)', fontname=font_name, fontsize=font_size_axes)

    # Max acceleration text at bottom right
    ax.text(time[-1], -y_limit, f'Max. Accel. = {accel_max:.2f}g ',
            ha='right', va='bottom', fontname=font_name, fontsize=font_size_ticks)

    fig.set_size_inches(wide, tall)
    fig.tight_layout()
    return fig
