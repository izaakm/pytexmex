#!/usr/bin/env python3

import scipy.integrate, scipy.stats, scipy.optimize
import numpy as np

def poilog_exp_integrand(x, n, mu, sigma):
    '''the part of the poilog integral that is inside the exponent'''
    return n * x - np.exp(x) - 0.5 * ((x - mu) / sigma) ** 2

def poilog_exp_integrand_max(n, mu, sigma):
    '''find the maximum value and position of the integrand'''
    f = lambda x: -poilog_exp_integrand(x, n, mu, sigma)
    fprime = lambda x: -(n - np.exp(x) - (x - mu) / sigma ** 2)
    res = scipy.optimize.fmin_bfgs(f, 0.0, fprime, disp=False, full_output=True)
    xopt, fopt, gopt, Bopt, func_calls, grad_calls, warnflag = res

    return xopt, fopt

def poilog_bounds(n, mu, sigma, fold=1e-6, guess=20.0):
    xopt, fopt = poilog_exp_integrand_max(n, mu, sigma)
    f = lambda x: poilog_exp_integrand(x, n, mu, sigma) - fopt - np.log(fold)
    lb = scipy.optimize.brentq(f, xopt - guess, xopt)
    ub = scipy.optimize.brentq(f, xopt, xopt + guess)

    return lb, ub

def poilog(n, mu, sigma):
    lb, ub = poilog_bounds(n, mu, sigma)

    # I put the factorial inside the exponent because it helps the whole thing behave better
    constant = 1.0 / (sigma * np.sqrt(2 * np.pi))
    fac = scipy.special.gammaln(n + 1)
    f = lambda x: constant * np.exp(n * x - np.exp(x) - 0.5 * ((x - mu) / sigma) ** 2 - fac)

    val, error = scipy.integrate.quad(f, lb, ub)
    return val
