import math
import time
import datetime


class Series:
    """This class provides easy computation of the mean, the standard deviation and the 95% confidence range of any
    sample of values."""
    def __init__(self, values=()):
        self._values = tuple(values)
        self._mean = None
        self._standard_deviation = None
        self._confidence_range = (None, None)  # 95% confidence range

    @property
    def values(self):
        return self._values

    @values.setter
    def values(self, new_values):
        self.reset()
        self._values = tuple(new_values)

    @property
    def mean(self):
        if self._mean is None:
            self.calculate_estimators()
        return self._mean

    @property
    def standard_deviation(self):
        if self._standard_deviation is None:
            self.calculate_estimators()
        return self._standard_deviation

    std = standard_deviation  # alias

    @property
    def confidence_range(self):
        if self._confidence_range == (None, None):
            self.calculate_estimators()
        return self._confidence_range

    def __str__(self):
        return "Series: mean={} ; std={} ; range={}".format(self.mean, self.standard_deviation, self.confidence_range)

    def reset(self):
        self._values = ()
        self._mean = None
        self._standard_deviation = None
        self._confidence_range = (None, None)

    def calculate_estimators(self):
        """Computes the mean, the standard deviation and the 95% confidence range."""
        n = len(self._values)
        values_sum = sum(self._values)
        squares_sum = sum(v**2 for v in self._values)
        self._mean = values_sum / n
        self._standard_deviation = math.sqrt(math.fabs(squares_sum/n - self._mean**2))
        half_range = 1.96 * self._standard_deviation / math.sqrt(n)
        self._confidence_range = (self._mean-half_range, self._mean+half_range)


class Clock:
    """A simple class for quick measurements of elapsed times across multiple files and functions."""
    # last_time is shared across all instances of Clock
    last_time = time.perf_counter()  # float. Time elapsed in seconds since last call.

    @staticmethod
    def elapsed(print_time=True):
        """
        Returns a tuple (time_since_start, time_since_last_call) where:
        - 'time_since_start' represents the time elapsed (in seconds) since the first import of the class Clock. float.
        - 'time_since_last_call' represents the time elapsed (in seconds) since the last call to this functions. float.
        :param print_time: boolean
            If True, the timings are printed in a format like this:
            'Since start: 01h:23m:48.320s - Since last call: 12m:32.876s'
        :return (time_since_start, time_since_last_call): (float, float)
        """
        time_since_start = time.perf_counter()
        time_since_last_call = time_since_start - Clock.last_time
        Clock.last_time = time_since_start
        if print_time:
            since_start = sec2time(time_since_start)
            since_last_call = sec2time(time_since_last_call)
            print("Since start: {} - Since last call: {}".format(since_start, since_last_call))
        return time_since_start, time_since_last_call


def sec2time(time_in_sec):
    """
    Turns a time expressed in seconds to a string formatted like 'days hours:minutes:seconds.microseconds'
    :param time_in_sec: float.
    :return ret_str: string.
    """
    return "{:0>8}".format(str(datetime.timedelta(seconds=time_in_sec)))
