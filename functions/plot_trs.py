"""TRS vs RRS plot (single accelerometer) matching MATLAB plotTRS.m."""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def plot_trs(run_name, accel_name, freq72, RRS, Aflx, Arig,
             freq06, TRS06, damping, low_cutoff, plot_options):
    """Create TRS vs RRS plot matching MATLAB plotTRS.m output."""
    wide = plot_options.get('wide', 6.5)
    tall = plot_options.get('tall_trs', 2.7)
    font_name = plot_options.get('font_name', 'Arial')
    font_size_title = plot_options.get('font_size_title', 11)
    font_size_axes = plot_options.get('font_size_axes', 11)
    font_size_ticks = plot_options.get('font_size_ticks', 10)
    font_size_text = plot_options.get('font_size_text', 7)
    font_size_legend = plot_options.get('font_size_legend', 6)

    max_trs = np.max(TRS06)
    x_ticks = [0.5, 1, 1.3, 8.3, 10, 20, 35]
    x_min, x_max = 0.5, 35
    y_ticks = [0.1, 0.5, 1, 5, 10, 50]

    is_table = 'Table' in accel_name
    upper_y = max(max_trs, 1.3 * Aflx) if is_table else max_trs

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

    y_min = min(np.floor(Arig * 0.85 * 10) / 10, 0.9)

    fig = plt.figure(figsize=(wide, tall))
    fig.patch.set_facecolor('white')
    ax = fig.add_subplot(111)
    ax.set_facecolor('white')

    ax.set_xscale('log')
    ax.set_yscale('log')

    # Set custom ticks and suppress minor ticks
    ax.set_xticks(x_ticks)
    ax.set_xticklabels([str(t) for t in x_ticks], fontsize=font_size_ticks)
    ax.xaxis.set_minor_locator(ticker.NullLocator())
    ax.set_yticks(y_ticks)
    ax.set_yticklabels([str(t) for t in y_ticks], fontsize=font_size_ticks)
    ax.yaxis.set_minor_locator(ticker.NullLocator())

    ax.grid(True, which='major', linewidth=0.5)

    # Plot TRS — black solid (DisplayName = accelName with underscores)
    ax.loglog(freq06, TRS06, 'k', linewidth=1, label=accel_name)

    if is_table:
        # RRS — blue dashed
        ax.loglog(freq72, RRS, '--b', linewidth=1.5, label='RRS')
        # 0.9*RRS — red dashed
        ax.loglog(freq72, 0.9 * RRS, '--r', linewidth=0.5, label='0.9*RRS')
        # 1.3*RRS — yellow dashed (no legend)
        ax.loglog(freq72, 1.3 * RRS, '--y', linewidth=0.5)

        # Aflx text and line (light blue)
        ax.text(x_min * 1.1, Aflx, f'Aflx = {Aflx:.2f}', color='blue',
                ha='left', va='top', fontsize=font_size_text)
        ax.plot([freq72[0], 1.3], [Aflx, Aflx], '--',
                color=[0.7, 0.7, 1], linewidth=0.25)

        # Arig text and line (light blue)
        ax.text(10, Arig, f'Arig = {Arig:.2f}', color='blue',
                ha='left', va='top', fontsize=font_size_text)
        ax.plot([8.3, freq72[-1]], [Arig, Arig], '--',
                color=[0.7, 0.7, 1], linewidth=0.25)

        # Low cutoff vertical (light blue)
        ax.axvline(x=low_cutoff, color=[0.7, 0.7, 1], linestyle='--', linewidth=0.25)
        ax.text(low_cutoff, y_min, f' {low_cutoff:.1f}-Hz Lower Limit',
                color='blue', ha='left', va='bottom', fontsize=font_size_text)

    ax.set_xlim([x_min, x_max])
    ax.set_ylim([y_min, y_max])

    if is_table:
        title = f"TRS vs. RRS: {accel_name.replace('_', ' ')} ({run_name.replace('_', ' ')})"
    else:
        title = f"TRS: {accel_name.replace('_', ' ')} ({run_name.replace('_', ' ')})"
    ax.set_title(title, fontname=font_name, fontsize=font_size_title,
                 fontweight='bold')
    ax.set_xlabel('Frequency (Hz)', fontname=font_name, fontsize=font_size_axes,
                   fontweight='bold')
    ylabel = f'Spectral Acceleration (g)\n{int(damping*100)}% Damping'
    ax.set_ylabel(ylabel, fontname=font_name, fontsize=font_size_axes,
                   fontweight='bold')
    ax.legend(loc='upper left', fontsize=font_size_legend)

    # Tick direction: inward on all 4 sides, full box
    ax.tick_params(axis='both', which='both', direction='in',
                   top=True, right=True, length=4, width=0.5)
    ax.spines['top'].set_visible(True)
    ax.spines['right'].set_visible(True)

    fig.subplots_adjust(left=0.130, right=0.904, top=0.919, bottom=0.160)
    return fig
