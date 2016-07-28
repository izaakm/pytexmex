import pytest
from pytexmex.core import *
import math, numpy as np

def assert_almost_equal(x, y, precision=5):
    assert round(float(x), precision) == round(float(y), precision)

class TestPoilogExpIntegrand:
    def test1(self):
        assert poilog_exp_integrand(0, 0, 1.0, 1.0) == -1.5
        assert poilog_exp_integrand(5, 0, 1.0, 1.0) == -math.exp(5.0) - 8.0
        assert poilog_exp_integrand(0, 3, 1.0, 1.0) == -1.5
        assert poilog_exp_integrand(5, 3, 1.0, 1.0) == 7.0 - math.exp(5.0)
        assert poilog_exp_integrand(5, 3, -3.0, 1.0) == -17.0 - math.exp(5.0)


class TestPoilogExpIntegrandMax:
    def test1(self):
        xopt, fopt = poilog_exp_integrand_max(0, 1.0, 1.0)
        assert xopt == 0.0
        assert fopt == -1.5

    def test2(self):
        xopt, fopt = poilog_exp_integrand_max(1, 2.0, 3.0)
        assert_almost_equal(xopt, 0.18381879)
        assert_almost_equal(fopt, -1.2012300237407563)

    def test3(self):
        xopt, fopt = poilog_exp_integrand_max(100, -5.0, 5.0)
        assert_almost_equal(xopt, 4.60132226)
        assert_almost_equal(fopt, 358.6725714379426)


class TestPoilogBounds:
    pass


class TestPoilogPmfNotrunc:
    def test1(self):
        assert_almost_equal(poilog_pmf_notrunc(0, -10.0, 5.0), 0.96553838064684505)

    def test2(self):
        assert_almost_equal(poilog_pmf_notrunc(100, -1.0, 2.0), 3.990999e-5)

    def test3(self):
        assert_almost_equal(poilog_pmf_notrunc(2, -4.0, 3.0), 0.02320258)


class TestPoilogCdf:
    def test_list_of_ints(self):
        ns = [1, 2, 3]
        poilog_cdf(ns, 1.0, 1.0)

    def test_array(self):
        ns = np.array([1.0, 2.0, 3.0])
        poilog_cdf(ns, 1.0, 1.0)
