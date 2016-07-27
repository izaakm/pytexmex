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

    Returns: list of floats
    '''

    mu, sigma = poilog_fit(ns, trunc)
    cdf = poilog_cdf(ns, mu, sigma, trunc)
    return cdf

def z_transform_table(table, trunc=True):
    '''
    Transform an OTU table in a table of z values

    table: pandas.DataFrame

    returns: pandas.DataFrame
    '''

    fun = lambda x: z_transform_sample(x, trunc=trunc)
    return table.apply(fun, axis=0)

def f_transform_table(table, trunc=True):
    '''
    Transform an OTU table in a table of F values

    table: pandas.DataFrame

    returns: pandas.DataFrame
    '''

    fun = lambda x: f_transform_sample(x, trunc=trunc)
    return table.apply(fun, axis=0)

def pp_plot_data(ns, trunc=True):
    '''
    Generate data for visualizing the quality of the poilog fit. One day I should use
    scipy's `scipy.stats.probplot` for this (which would require writing a `poilog`
    distribution).

    ns : list of floats

    returns: (list of floats, list of floats)
      the empirical and theoretical cdf values, going from 0 up to the maximum
      of the input ns
    '''

    if trunc:
        ns = [n for n in ns if n > 0]

    counts, values = np.histogram(ns, bins=range(max(ns) + 1))
    cumulative_counts = np.cumsum(counts)
    empirical_cdf = cumulative_counts / cumulative_counts[-1]

    mu, sigma = poilog_fit(ns, trunc)
    theoretical_cdf = poilog_cdf(range(max(ns)), mu, sigma, trunc)

    return empirical_cdf, theoretical_cdf
