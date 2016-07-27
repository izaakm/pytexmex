import pytest
from pytexmex.helpers import *
import math

def assert_almost_equal(x, y, precision=5):
    assert round(float(x), precision) == round(float(y), precision)

class TestPoilogFit:
    def test1(self):
        ns = [1] * 100 + [2] * 25 + [3] * 10 + [4] * 3 + [5] * 1 + [10, 100, 1000]
        mu, sigma = poilog_fit(ns)
        assert_almost_equal(mu, -9.223053141925663)
        assert_almost_equal(sigma, 3.2622741227487895)
