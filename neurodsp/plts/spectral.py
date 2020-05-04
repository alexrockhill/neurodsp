"""Plotting functions for neurodsp.spectral."""

from itertools import repeat

import numpy as np
import matplotlib.pyplot as plt

from neurodsp.plts.style import style_plot
from neurodsp.plts.utils import check_ax, savefig

###################################################################################################
###################################################################################################

@savefig
@style_plot
def plot_power_spectra(freqs, powers, labels=None, colors=None, ax=None):
    """Plot power spectra.

    Parameters
    ----------
    freqs : 1d array or list of 1d array
        Frequency vector.
    powers : 1d array or list of 1d array
        Power values.
    labels : str or list of str, optional
        Labels for each time series.
    colors : str or list of str
        Colors to use to plot lines.
    ax : matplotlib.Axes, optional
        Figure axes upon which to plot.

    Examples
    --------
    Plot the power spectrum of a simulated signal:

    >>> from neurodsp.sim import sim_combined
    >>> from neurodsp.spectral import compute_spectrum
    >>> n_seconds = 10
    >>> fs = 500
    >>> sig = sim_combined(n_seconds, fs, components={'sim_synaptic_current': {},
    ...                                               'sim_bursty_oscillation' : {'freq': 10}},
    ...                    component_variances=(0.01, 0.9))
    >>> freqs, powers = compute_spectrum(sig, fs)
    >>> plot_power_spectra(freqs, powers)

    """

    ax = check_ax(ax, (6, 6))

    freqs = repeat(freqs) if isinstance(freqs, np.ndarray) else freqs
    powers = [powers] if isinstance(powers, np.ndarray) else powers

    if labels is not None:
        labels = [labels] if not isinstance(labels, list) else labels
    else:
        labels = repeat(labels)

    if colors is not None:
        colors = repeat(colors) if not isinstance(colors, list) else cycle(colors)

    for freq, power, label in zip(freqs, powers, labels):
        ax.loglog(freq, power, label=label)

    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Power (V^2/Hz)')


@savefig
@style_plot
def plot_scv(freqs, scv, ax=None):
    """Plot spectral coefficient of variation.

    Parameters
    ----------
    freqs : 1d array
        Frequency vector.
    scv : 1d array
        Spectral coefficient of variation.
    ax : matplotlib.Axes, optional
        Figure axes upon which to plot.

    Examples
    --------
    Plot the power spectral coefficient of variation of a simulated signal:

    >>> from neurodsp.sim import sim_combined
    >>> from neurodsp.spectral import compute_scv
    >>> n_seconds = 10
    >>> fs = 500
    >>> sig = sim_combined(n_seconds, fs, components={'sim_synaptic_current': {},
    ...                                               'sim_bursty_oscillation' : {'freq': 10}},
    ...                    component_variances=(0.01, 0.9))
    >>> freqs, scv = compute_scv(sig, fs)
    >>> plot_scv(freqs, scv)

    """

    ax = check_ax(ax, (5, 5))

    ax.loglog(freqs, scv)

    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('SCV')


@savefig
@style_plot
def plot_scv_rs_lines(freqs, scv_rs, ax=None):
    """Plot spectral coefficient of variation, from the resampling method, as lines.

    Parameters
    ----------
    freqs : 1d array
        Frequency vector.
    scv_rs : 2d array
        Spectral coefficient of variation, from resampling procedure.
    ax : matplotlib.Axes, optional
        Figure axes upon which to plot.

    Examples
    --------
    Plot the power spectral coefficient of variation of a simulated signal:

    >>> from neurodsp.sim import sim_combined
    >>> from neurodsp.spectral import compute_scv_rs
    >>> n_seconds = 10
    >>> fs = 500
    >>> sig = sim_combined(n_seconds, fs, components={'sim_synaptic_current': {},
    ...                                               'sim_bursty_oscillation' : {'freq': 10}},
    ...                    component_variances=(0.01, 0.9))
    >>> freqs, t_inds, scv_rs = compute_scv_rs(sig, fs, nperseg=fs, method='bootstrap',
    ...                                        rs_params=(5, 200))
    >>> plot_scv_rs_lines(freqs, scv_rs)

    """

    ax = check_ax(ax, (8, 8))

    ax.loglog(freqs, scv_rs, 'k', alpha=0.1)
    ax.loglog(freqs, np.mean(scv_rs, axis=1), lw=2)
    ax.loglog(freqs, len(freqs)*[1.])

    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('SCV')


@savefig
@style_plot
def plot_scv_rs_matrix(freqs, t_inds, scv_rs):
    """Plot spectral coefficient of variation, from the resampling method, as a matrix.

    Parameters
    ----------
    freqs : 1d array
        Frequency vector.
    t_inds : 1d array
        Time indices.
    scv_rs : 1d array
        Spectral coefficient of variation, from resampling procedure.

    Examples
    --------
    Plot a SCV matrix from a simulated signal with a high probability of bursting at 10Hz:

    >>> from neurodsp.sim import sim_combined
    >>> from neurodsp.spectral import compute_scv_rs
    >>> n_seconds = 100
    >>> fs = 500
    >>> sig = sim_combined(n_seconds, fs,
    ...                    components={'sim_synaptic_current': {},
    ...                                'sim_bursty_oscillation' : {'freq': 10,
    ...                                                            'enter_burst':0.75}},
    ...                    component_variances=(0.001, 0.9))
    >>> freqs, t_inds, scv_rs = compute_scv_rs(sig, fs, method='rolling', rs_params=(10, 2))
    >>> plot_scv_rs_matrix(freqs[:21], t_inds, scv_rs[:21])

    """

    fig, ax = plt.subplots(figsize=(10, 5))

    plt.imshow(np.log10(scv_rs), aspect='auto',
               extent=(t_inds[0], t_inds[-1], freqs[-1], freqs[0]))
    plt.colorbar(label='SCV')

    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')


@savefig
@style_plot
def plot_spectral_hist(freqs, power_bins, spectral_hist, spectrum_freqs=None, spectrum=None):
    """Plot spectral histogram.

    Parameters
    ----------
    freqs : 1d array
        Frequencies over which the histogram is calculated.
    power_bins : 1d array
        Power bins within which histogram is aggregated.
    spectral_hist : 2d array
        Spectral histogram to be plotted.
    spectrum_freqs : 1d array, optional
        Frequency axis of the power spectrum to be plotted.
    spectrum : 1d array, optional
        Spectrum to be plotted over the histograms.

    Examples
    --------
    Plot a spectral histogram for a simulated signal:

    >>> from neurodsp.sim import sim_combined
    >>> from neurodsp.spectral import compute_spectral_hist
    >>> n_seconds = 100
    >>> fs = 500
    >>> sig = sim_combined(n_seconds, fs, components={'sim_synaptic_current': {},
    ...                                               'sim_bursty_oscillation' : {'freq': 10}},
    ...                    component_variances=(0.01, 0.9))
    >>> freqs, bins, spect_hist = compute_spectral_hist(sig, fs, nbins=40, f_range=(0, 80),
    ...                                                 cut_pct=(0.1, 99.9))
    >>> plot_spectral_hist(freqs, bins, spect_hist)

    """

    # Automatically scale figure height based on number of bins
    plt.figure(figsize=(8, 12 * len(power_bins) / len(freqs)))

    # Plot histogram intensity as image and automatically adjust aspect ratio
    plt.imshow(spectral_hist, extent=[freqs[0], freqs[-1], power_bins[0], power_bins[-1]], aspect='auto')
    plt.xlabel('Frequency (Hz)', fontsize=15)
    plt.ylabel('Log10 Power', fontsize=15)
    plt.colorbar(label='Probability')

    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Log10 Power')

    # If a PSD is provided, plot over the histogram data
    if spectrum is not None:
        plt_inds = np.logical_and(spectrum_freqs >= freqs[0], spectrum_freqs <= freqs[-1])
        plt.plot(spectrum_freqs[plt_inds], np.log10(spectrum[plt_inds]), color='w', alpha=0.8)
