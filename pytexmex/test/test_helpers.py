import pytest
from pytexmex.helpers import *
import math, numpy as np

def assert_almost_equal(x, y, precision=5):
    assert round(float(x), precision) == round(float(y), precision)

class TestPoilogFit:
    def test1(self):
        ns = [1] * 100 + [2] * 25 + [3] * 10 + [4] * 3 + [5] * 1 + [10, 100, 1000]
        mu, sigma = poilog_fit(ns, x0=[-9.2, 3.3])
        assert_almost_equal(mu, -9.223, 3)
        assert_almost_equal(sigma, 3.262, 3)


class TestFTransformSample:
    def test_list_of_ints(self):
        ns = [1] * 10 + [2] * 5 + [3] * 2 + [5, 10, 100, 1000]
        fs = f_transform_sample(ns)

    def test_array(self):
        ns = np.array([1] * 10 + [2] * 5 + [3] * 2 + [5, 10, 100, 1000])
        fs = f_transform_sample(ns)
