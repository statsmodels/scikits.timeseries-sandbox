# pylint: disable-msg=W0611, W0612, W0511,R0201
"""Tests suite for MaskedArray.
Adapted from the original test_ma by Pierre Gerard-Marchant

:author: Pierre Gerard-Marchant & Matt Knox
:contact: pierregm_at_uga_dot_edu & mattknox_ca_at_hotmail_dot_com
:version: $Id: test_extras.py 3836 2008-01-15 13:09:03Z matthew.brett@gmail.com $
"""
__author__ = "Pierre GF Gerard-Marchant & Matt Knox ($Author: matthew.brett@gmail.com $)"
__version__ = '1.0'
__revision__ = "$Revision: 3836 $"
__date__     = '$Date: 2008-01-15 08:09:03 -0500 (Tue, 15 Jan 2008) $'


import numpy
from scipy.testing import *
from numpy.ma import masked
from numpy.ma.testutils import assert_equal, assert_almost_equal

from scikits.timeseries import time_series, Date, extras
from scikits.timeseries.extras import *

#..............................................................................
class TestMisc(TestCase):
    "Base test class for MaskedArrays."
    def __init__(self, *args, **kwds):
        TestCase.__init__(self, *args, **kwds)
    #
    def test_leapyear(self):
        leap = isleapyear([1900,1901,1902,1903,1904,2000,2001,2002,2003,2004])
        assert_equal(leap, [0,0,0,0,1,1,0,0,0,1])

#..............................................................................
class TestCountmissing(TestCase):
    #
    def __init__(self, *args, **kwds):
        TestCase.__init__(self, *args, **kwds)
        data = time_series(numpy.arange(731),
                           start_date=Date(string='2003-01-01', freq='D'),
                           freq='D')
        self.data = data

    def test_count_missing(self):
        data = self.data
        assert_equal(count_missing(data), 0)
        assert_equal(count_missing(data.convert('A')), (0,0))
        assert_equal(count_missing(data.convert('M')), [0]*24)
        #
        series = data.copy()
        series[numpy.logical_not(data.day % 10)] = masked
        assert_equal(count_missing(series), 70)
        assert_equal(count_missing(series.convert('A')), (35,35))
        assert_equal(count_missing(series.convert('M')),
                     [3,2,3,3,3,3,3,3,3,3,3,3]*2)
        #
        series[series.day == 31] = masked
        assert_equal(count_missing(series), 84)
        assert_equal(count_missing(series.convert('A')), (42,42))
        assert_equal(count_missing(series.convert('M')),
                     [4,2,4,3,4,3,4,4,3,4,3,4]*2)
    #
    def test_accept_atmost_missing(self):
        series = self.data.copy()
        series[numpy.logical_not(self.data.day % 10)] = masked
        result = accept_atmost_missing(series.convert('M'),3,True)
        assert_equal(result._mask.all(-1), [0]*24)
        result = accept_atmost_missing(series.convert('M'),3,False)
        assert_equal(result._mask.all(-1), [1,0,1,1,1,1,1,1,1,1,1,1]*2)
        result = accept_atmost_missing(series.convert('M'),0.1,True)
        assert_equal(result._mask.all(-1), [0]*24)
        result = accept_atmost_missing(series.convert('A'),35,True)
        assert_equal(result._mask.all(-1), [0,0])
        result = accept_atmost_missing(series.convert('A'),35,False)
        assert_equal(result._mask.all(-1), [1,1])
        result = accept_atmost_missing(series.convert('A'),0.05,True)
        assert_equal(result._mask.all(-1), [1,1])


###############################################################################
#------------------------------------------------------------------------------
if __name__ == "__main__":
    nose.run(argv=['', __file__])