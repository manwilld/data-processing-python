"""TRS vs RRS all-axes overlay plot matching MATLAB style."""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def plot_trs_all(run_name, accel_name, axes, freq72, RRS_h, RRS_v,
                 Aflx_h, Aflx_v, Arig_h, Arig_v, damping, low_cutoff,
                 freq06_dict, TRS06_dict, plot_options):
    """Create TRS vs RRS overlay plot for all axes."""
    wide = plot_options.get('wide', 6.5)
    tall = plot_options.get('tall_trs', 2.7)
    font_name = plot_options.get('font_name', 'Arial')
    font_size_title = plot_options.get('font_size_title', 11)
    font_size_axes = plot_options.get('font_size_axes', 11)
    font_size_ticks = plot_options.get('font_size_ticks', 10)
    font_size_text = plot_options.get('font_size_text', 7)
    font_size_legend = plot_options.get('font_size_legend', 6)

    max_trs = max((np.max(TRS06_dict[a]) for a in axes if a in TRS06_dict), default=1.0)

    x_ticks = [0.5, 1, 1.3, 8.3, 10, 20, 35]
    x_min, x_max = 0.5, 35
    y_ticks = [0.1, 0.5, 1, 5, 10, 50]

    is_table = 'Table' in accel_name
    upper_y = max(max_trs, 1.3 * Aflx_h)

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

    fig = plt.figure(figsize=(wide, tall))
    fig.patch.set_facecolor('white')
    ax = fig.add_subplot(111)
    ax.set_facecolor('white')

    ax.set_xscale('log')
    ax.set_yscale('log')

    # --- TRS lines per axis (use ax.plot not loglog) ---
    line_colors = {'X': 'black', 'Y': 'magenta', 'D': 'green', 'Z': 'cyan'}
    for axis in axes:
        if axis in freq06_dict and axis in TRS06_dict:
            color = line_colors.get(axis, 'black')
            ax.plot(freq06_dict[axis], TRS06_dict[axis],
                    color=color, linewidth=1.0, label=f'TRS_{axis}')

    if is_table:
        light_blue = [0.7, 0.7, 1.0]

        ax.plot(freq72, RRS_h, color='blue', linestyle='--', linewidth=1.5, label='RRS_h')
        ax.plot(freq72, RRS_v, color='blue', linestyle='--', linewidth=1.5, label='RRS_v')
        ax.plot(freq72, 0.9 * RRS_h, color='red', linestyle='--', linewidth=0.5)
        ax.plot(freq72, 0.9 * RRS_v, color='red', linestyle='--', linewidth=0.5)
        ax.plot(freq72, 1.3 * RRS_h, color='yellow', linestyle='--', linewidth=0.5)

        # Aflx_h line and text (light blue line, blue text)
        ax.plot([freq72[0], 1.3], [Aflx_h, Aflx_h], color=light_blue, linestyle='--', linewidth=0.25)
        ax.text(x_min * 1.1, Aflx_h, f'Aflx_h = {Aflx_h:.2f}', color='blue',
                ha='left', va='top', fontsize=font_size_text)

        # Aflx_v line and text
        ax.plot([freq72[0], 1.3], [Aflx_v, Aflx_v], color=light_blue, linestyle='--', linewidth=0.25)
        ax.text(x_min * 1.1, Aflx_v, f'Aflx_v = {Aflx_v:.2f}', color='blue',
                ha='left', va='bottom', fontsize=font_size_text)

        # Arig_h line and text
        ax.plot([8.3, freq72[-1]], [Arig_h, Arig_h], color=light_blue, linestyle='--', linewidth=0.25)
        ax.text(10, Arig_h, f'Arig_h = {Arig_h:.2f}', color='blue',
                ha='left', va='top', fontsize=font_size_text)

        # Arig_v line and text
        ax.plot([8.3, freq72[-1]], [Arig_v, Arig_v], color=light_blue, linestyle='--', linewidth=0.25)
        ax.text(10, Arig_v, f'Arig_v = {Arig_v:.2f}', color='blue',
                ha='left', va='bottom', fontsize=font_size_text)

        # Low cutoff vertical and text (light blue line, blue text)
        ax.plot([low_cutoff, low_cutoff], [0.1, 100], color=light_blue, linestyle='--', linewidth=0.25)
        ax.text(low_cutoff, y_min, f' {low_cutoff:.1f}-Hz Lower Limit', color='blue',
                ha='left', va='bottom', fontsize=font_size_text)

    ax.set_xlim([x_min, x_max])
    ax.set_ylim([y_min, y_max])

    # Grid on (MATLAB grid on after hold off)
    ax.grid(True, which='major', color='lightgray', linewidth=0.4)
    ax.grid(True, which='minor', color='lightgray', linewidth=0.2)

    # Custom tick labels AFTER all plotting
    ax.set_xticks(x_ticks)
    ax.xaxis.set_major_formatter(ticker.FixedFormatter([str(t) for t in x_ticks]))
    ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())

    ax.set_yticks(y_ticks)
    ax.yaxis.set_major_formatter(ticker.FixedFormatter([str(t) for t in y_ticks]))
    ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())

    ax.tick_params(axis='both', which='major', direction='in',
                   top=True, right=True, length=5, width=0.5,
                   labelsize=font_size_ticks)
    ax.tick_params(axis='both', which='minor', direction='in',
                   top=True, right=True, length=3, width=0.5)
    ax.spines['top'].set_visible(True)
    ax.spines['right'].set_visible(True)

    if is_table:
        title = (f"TRS vs. RRS: {accel_name.replace('_',' ')} "
                 f"({run_name.replace('_',' ')})")
    else:
        title = f"TRS: {accel_name.replace('_',' ')} ({run_name.replace('_',' ')})"
    ax.set_title(title, fontsize=font_size_title, fontweight='bold')
    ax.set_xlabel('Frequency (Hz)', fontsize=font_size_axes)
    ylabel = f'Spectral Acceleration (g)\n{int(damping*100)}% Damping'
    ax.set_ylabel(ylabel, fontsize=font_size_axes)
    ax.legend(loc='upper left', fontsize=font_size_legend, frameon=True)

    fig.subplots_adjust(left=0.130, right=0.904, top=0.880, bottom=0.160)
    return fig
