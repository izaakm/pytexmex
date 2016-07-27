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

def transform_table(table, transform, trunc=True):
    '''
    Transform a table, column by column

    table: pandas.DataFrame
      the OTU table; all its columns should be the integer counts
    transform: function :: list of integers -> list of integers
      the data transformation to be applied to each column. must have
      mu, sigma, and trunc as parameters

    returns: pandas.DataFrame
    '''

    def f(ns):
        mu, sigma = poilog_fit(ns, trunc)
        transformed_ns = transform(ns, mu=mu, sigma=sigma, trunc=trunc)
        return transformed_ns

    return table.apply(f, axis=0)

def z_transform_table(table, trunc=True):
    return transform_table(table, transform=z_transform_sample, trunc=trunc)

def f_transform_table(table, trunc=True):
    return transform_table(table, transform=f_transform_sample, trunc=trun)

def pp_plot_data(ns, trunc=True):
    '''
    Generate data for visualizing the quality of the poilog fit. One day I should use
    scipy's `scipy.stats.probplot` for this (which would require writing a `poilog`
    distribution).

    Returns: (list of floats, list of floats)
      the empirical and theoretical cdfs
    '''

    # create a table of the number of times each value appears
    counts, values = np.histogram(ns, bins=range(max(ns) + 1))
    cumulative_counts = np.cumsum(counts)
    empirical_cdf = cumulative_counts / cumulative_counts[-1]

    mu, sigma = poilog_fit(ns, trunc)
    theoretical_cdf = poilog_cdf(range(max(ns)), mu, sigma, trunc)

    return empirical, theoretical
