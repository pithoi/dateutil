import datetime

utc_offset_range_error = 'UTC offset must be a whole number of minutes in the range -1439 to 1439 inclusive'


class tzbase(datetime.tzinfo):
    def __init__(self):
        self._offset = None  # Offset of local time from UTC, in minutes east of UTC, negative if west, None if unknown

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, value):
        limit = datetime.timedelta(days=1)  # The magnitude of the offset must be less than one day
        value = datetime.timedelta(minutes=value)
        if -limit < value < limit:
            self._offset = value
        else:
            raise ValueError(utc_offset_range_error)

    def utcoffset(self, dt):
        """
        Return offset of local time from UTC, in minutes east of UTC. If local time is west of UTC, this should be
        negative. Note that this is intended to be the total offset from UTC; for example, if a tzinfo object
        represents both time zone and DST adjustments, utcoffset() should return their sum. If the UTC offset
        isn't known, return None. Else the value returned must be a timedelta object specifying a whole number of
        minutes in the range -1439 to 1439 inclusive (1440 = 24*60; the magnitude of the offset must be less than
        one day). Most implementations of utcoffset() will probably look like one of these two:

        return CONSTANT                 # fixed-offset class
        return CONSTANT + self.dst(dt)  # daylight-aware class

        If utcoffset() does not return None, dst() should not return None either.

        The default implementation of utcoffset() raises NotImplementedError.
        """
        # If the offset from UTC is not known, return None
        if self.offset is None:
            assert self.dst(dt) is None  # If the UTC offset is None confirm dst() also returns None
            return None
        else:
            # It the class is not daylight-aware, the result is the standard offset
            result = self.offset

            dst_adj = self.dst(dt)  # Get the daylight savings time adjustment
            if dst_adj:  # If the class is daylight-aware...
                result += dst_adj  # ...add the daylight savings time adjustment to the standard offset

            limit = datetime.timedelta(days=1)  # The magnitude of the offset must be less than one day
            if -limit < result < limit:
                return result
            else:
                raise ValueError('UTC offset must be a whole number of minutes in the range -1439 to 1439 inclusive')
