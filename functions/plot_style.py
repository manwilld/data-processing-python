"""Configure matplotlib defaults to match MATLAB plot style.

Sets font family with proper fallback: Arial → Liberation Sans → DejaVu Sans.
Call setup_plot_style() once at the start of any runner script.
"""

import matplotlib
import matplotlib.font_manager as fm
import warnings


def get_best_font(preferred='Arial'):
    """Return the best available font family matching the preferred font."""
    available = {f.name for f in fm.fontManager.ttflist}
    candidates = [preferred, 'Liberation Sans', 'FreeSans', 'Helvetica',
                  'Nimbus Sans', 'DejaVu Sans', 'sans-serif']
    for font in candidates:
        if font in available:
            return font
    return 'sans-serif'


def setup_plot_style(font_name=None):
    """Configure matplotlib rcParams for engineering plot style.

    Parameters
    ----------
    font_name : str or None
        Preferred font. If None or not available, falls back gracefully.
    """
    # Suppress font-not-found warnings
    warnings.filterwarnings('ignore', message='.*findfont.*')
    warnings.filterwarnings('ignore', category=UserWarning,
                            module='matplotlib.font_manager')

    best_font = get_best_font(font_name or 'Arial')

    matplotlib.rcParams.update({
        'font.family': 'sans-serif',
        'font.sans-serif': [best_font, 'Liberation Sans', 'FreeSans',
                            'DejaVu Sans', 'sans-serif'],
        'axes.unicode_minus': False,
        'figure.dpi': 100,
        'savefig.dpi': 150,
        'svg.fonttype': 'none',   # embed fonts as text in SVG (not paths)
    })

    return best_font
