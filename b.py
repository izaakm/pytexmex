#!/usr/bin/env python3

import scipy.integrate, scipy.stats, scipy.optimize
import numpy as np

def poilog_exp_integrand(x, n, mu, sigma):
    '''the part of the poilog integral that is inside the exponent'''
    return n * x - np.exp(x) - 0.5 * ((x - mu) / sigma) ** 2

def poilog_exp_integrand_max(n, mu, sigma):
    '''find the maximum value and position of the exponential part of the integrand'''
    f = lambda x: -poilog_exp_integrand(x, n, mu, sigma)
    fprime = lambda x: -(n - np.exp(x) - (x - mu) / sigma ** 2)
    res = scipy.optimize.fmin_bfgs(f, 0.0, fprime, disp=False, full_output=True)
    xopt, fopt, gopt, Bopt, func_calls, grad_calls, warnflag = res

    return xopt, -fopt

def poilog_bounds(n, mu, sigma, fold=1e-9, guess=1.0, guess_multiplier=2.0):
    '''
    Pick reasonable bounds for the poilog integral. Start at the place where
    the integrand is maximized, then go out left and right until the integrand
    falls to some fold of its maximum value.
    '''

    xopt, fopt = poilog_exp_integrand_max(n, mu, sigma)
    f = lambda x: poilog_exp_integrand(x, n, mu, sigma) - fopt - np.log(fold)


    while f(xopt - guess) > 0 or f(xopt + guess) > 0:
        guess *= guess_multiplier

    lb = scipy.optimize.brentq(f, xopt - guess, xopt)
    ub = scipy.optimize.brentq(f, xopt, xopt + guess)

    return lb, ub

def poilog_pmf_notrunc(n, mu, sigma):
    '''probability mass function, no truncation'''

    if n < 0:
        raise ValueError("poilog takes nonnegative integers")

    lb, ub = poilog_bounds(n, mu, sigma)

    # I put the factorial inside the exponent because it helps the whole thing behave better
    constant = 1.0 / (sigma * np.sqrt(2 * np.pi))
    fac = scipy.special.gammaln(n + 1)
    f = lambda x: constant * np.exp(n * x - np.exp(x) - 0.5 * ((x - mu) / sigma) ** 2 - fac)

    val, error = scipy.integrate.quad(f, lb, ub)
    return val

def poilog_pmf(n, mu, sigma, trunc=True):
    '''probability mass function'''

    if not trunc:
        return poilog_pmf_notrunc(n, mu, sigma)
    else:
        if n == 0:
            return 0.0
        else:
            return poilog_pmf_notrunc(n, mu, sigma) / (1.0 - poilog_pmf_notrunc(0, mu, sigma))

def poilog_cdf(ns, mu, sigma, trunc=True):
    '''cumulative distribution function'''

    # compute all the values up to the biggest n
    all_pmfs = [poilog_pmf(n, mu, sigma, trunc) for n in range(max(ns) + 1)]
    all_cdfs = np.cumsum(all_pmfs)

    return [all_cdfs[n] for n in ns]

def poilog_ll(ns, mu, sigma, trunc=True, threshold=1e-120):
    '''log likelihood'''

    ll = 0.0
    for n, counts in scipy.stats.itemfreq(ns):
        pmf = poilog_pmf(n, mu, sigma, trunc)

        # log function complains if it sees very small values, so we make our own cutoff
        if pmf > threshold:
            ll += counts * np.log(pmf)

    return ll

def poilog_fit(ns, trunc=True, x0=None):
    '''
    Maximum likelihood estimation fit
    
    x0: (float, float)
      The starting mu and sigma for the MLE optimization. If None, then a guess will be supplied.
    ''' 

    ns = np.array(ns)
    if trunc:
        ns = ns[ns > 0]

    if x0 is None:
        x0 = [np.mean(np.log(ns)), np.log(np.std(np.log(ns)))]

    f = lambda x: -poilog_ll(ns, x[0], np.exp(x[1]), trunc)

    mu_opt, log_sigma_opt = scipy.optimize.fmin(f, x0)
    sigma_opt = np.exp(log_sigma_opt)
    return mu_opt, sigma_opt
