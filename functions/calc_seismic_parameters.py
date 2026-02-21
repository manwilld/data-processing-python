"""Calculate seismic parameters per ICC-ES AC156."""

import math
import numpy as np


def calc_frequency(start_frequency=0.1, end_frequency=38.0, octave=1/72):
    """Generate frequency array at 1/72 octave spacing."""
    freqs = [start_frequency]
    j = 1
    while True:
        next_freq = start_frequency * (2 ** (j * octave))
        if next_freq > end_frequency:
            break
        freqs.append(next_freq)
        j += 1
    return np.array(freqs)


def calc_rrs(freq, Aflx, Arig):
    """Calculate Required Response Spectrum (RRS) per AC156.

    Uses natural log (matching MATLAB log()).
    """
    k1 = 0.79015395365231482071
    n1 = 0.89771171750262309292
    n2 = 0.71978596791944049081

    RRS = np.zeros(len(freq))
    for i, f in enumerate(freq):
        if f <= 1.3:
            RRS[i] = k1 * Aflx * f ** n1
        elif f <= 8.3:
            RRS[i] = Aflx
        elif f <= 33.3:
            C_zpa = 33.3 ** (n2 * math.log(Aflx / Arig)) * Arig
            RRS[i] = C_zpa * f ** (-n2 * math.log(Aflx / Arig))
        else:
            RRS[i] = Arig
    return RRS


def calc_seismic_parameters(config):
    """Calculate Aflx, Arig, freq72, RRS from seismic config.

    Parameters
    ----------
    config : dict
        Must contain: Sds1, z_h1, low_resonance
        Optional: Sds2, z_h2, seismic_version

    Returns
    -------
    dict with keys: Aflx_h, Arig_h, Aflx_v, Arig_v, Arig_h90, Arig_v90,
                    freq72, RRS_h, RRS_v, lowCutoff, highCutoff
    """
    Sds1 = config['Sds1']
    z_h1 = config['z_h1']
    Sds2 = config.get('Sds2')
    z_h2 = config.get('z_h2')
    low_resonance = config['low_resonance']
    asce7_22 = config.get('seismic_version', 'ASCE7-16') == 'ASCE7-22'

    high_cutoff = 33.3

    # Low cutoff frequency
    low_cutoff = max(1.3, min(3.5, 0.75 * low_resonance))
    low_cutoff = math.ceil(low_cutoff * 10) / 10
    print(f'Low Resonance Frequency: {low_resonance:.1f} Hz')
    print(f'Low Cutoff Frequency: {low_cutoff:.1f} Hz')

    # Aflx and Arig per ICC-ES AC156
    if asce7_22:
        Hf1 = round(1 + 2.5 * z_h1, 2)
        Ru1 = 1.3 if z_h1 > 0 else 1.0
        print(f'Hf1: {Hf1:.2f}')
        print(f'Ru1: {Ru1:.2f}')
        Aflx_h = round(min(1.6 * Sds1, Sds1 * Hf1 / Ru1), 2)
        Arig_h = round(min(1.6 * Sds1, 0.4 * Sds1 * Hf1 / Ru1), 2)

        if Sds2 is not None:
            Hf2 = round(1 + 2.5 * z_h2, 2)
            Ru2 = 1.3 if z_h2 > 0 else 1.0
            Aflx_h = round(max(Aflx_h, min(1.6 * Sds2, Sds2 * Hf2 / Ru2)), 2)
            Arig_h = round(max(Arig_h, 0.4 * Sds2 * Hf2 / Ru2), 2)
    else:
        Aflx_h = round(min(1.6 * Sds1, Sds1 * (1 + 2 * z_h1)), 2)
        Arig_h = round(0.4 * Sds1 * (1 + 2 * z_h1), 2)
        if Sds2 is not None:
            Aflx_h = round(max(Aflx_h, min(1.6 * Sds2, Sds2 * (1 + 2 * z_h2))), 2)
            Arig_h = round(max(Arig_h, 0.4 * Sds2 * (1 + 2 * z_h2)), 2)

    Aflx_v = round(0.67 * Sds1, 2)
    Arig_v = round(0.27 * Sds1, 2)
    if Sds2 is not None:
        Aflx_v = round(max(Aflx_v, 0.67 * Sds2), 2)
        Arig_v = round(max(Arig_v, 0.27 * Sds2), 2)

    Arig_h90 = round(0.9 * Arig_h, 2)
    Arig_v90 = round(0.9 * Arig_v, 2)

    print(f'Aflx_h={Aflx_h}, Arig_h={Arig_h}, Aflx_v={Aflx_v}, Arig_v={Arig_v}')
    print(f'Arig_h90={Arig_h90}, Arig_v90={Arig_v90}')

    # Frequency array
    freq72 = calc_frequency()

    # RRS
    RRS_h = calc_rrs(freq72, Aflx_h, Arig_h)
    RRS_v = calc_rrs(freq72, Aflx_v, Arig_v)

    return {
        'Aflx_h': Aflx_h,
        'Arig_h': Arig_h,
        'Aflx_v': Aflx_v,
        'Arig_v': Arig_v,
        'Arig_h90': Arig_h90,
        'Arig_v90': Arig_v90,
        'freq72': freq72,
        'RRS_h': RRS_h,
        'RRS_v': RRS_v,
        'lowCutoff': low_cutoff,
        'highCutoff': high_cutoff,
        'lowResonance': low_resonance,
    }
