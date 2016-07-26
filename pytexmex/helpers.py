from pytexmex.core import *
import numpy as np
import scipy.stats

def z_transform_sample(ns, trunc=True):
    '''
    Transform a list of counts into their z values

    Returns: np.array
    '''

    mu, sigma = poilog_fit(ns, trunc)
    z = (np.log(np.array(ns)) - mu) / sigma
    return z

def f_transform_sample(ns, trunc=True):
    '''
    Transform a list of counts into their F values

    Returns: list
    '''

    mu, sigma = poilog_fit(ns, trunc)
    cdf = poilog_cdf(ns, mu, sigma, trunc)
    return cdf

def pp_plot_data(ns, trunc=True):
    '''
    Generate data for visualizing the quality of the poilog fit. One day I should use
    scipy's `scipy.stats.probplot` for this (which would require writing a `poilog`
    distribution).

    Returns: (list of floats, list of floats)
      the empirical and theoretical cdfs
    '''

    # compute the empirical fit
    # generate a list of pairs [n, # of times n appears in the ns]
    freqs = scipy.stats.itemfreq(ns)

    # freqs does not have zero entries; add them here
    # this should now look like [0, whatever], [1, whatever], etc.
    for i in range(max(ns)):
        if freqs[i][0] < i:
            freqs = np.insert(freqs, i, [i, 0], axis=0)

    empirical = np.cumsum(freqs, axis=0)

    mu, sigma = poilog_fit(ns, trunc)
    theoretical = poilog_cdf(range(max(ns)), mu, sigma, trunc)

    return empirical, theoretical
