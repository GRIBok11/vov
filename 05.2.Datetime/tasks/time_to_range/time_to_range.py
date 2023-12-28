import datetime
import enum
import typing as tp

class GranularityEnum(enum.Enum):
    DAY = datetime.timedelta(days=1)
    TWELVE_HOURS = datetime.timedelta(hours=12)
    HOUR = datetime.timedelta(hours=1)
    THIRTY_MIN = datetime.timedelta(minutes=30)
    FIVE_MIN = datetime.timedelta(minutes=5)

def truncate_to_granularity(dt: tp.Any, gtd: tp.Any) -> tp.Any:
    dif = (dt - dt.replace(hour=0,
                               minute=0,
                               second=0,
                               microsecond=0)).seconds

    s = gtd.value.total_seconds()

    se = dif % s
    insec = datetime.timedelta(seconds=se)
    dt -= insec

    return dt.replace(second=0,
                      microsecond=0)


class DtRange:
    def __init__(self, before: tp.Any, after: tp.Any, shift: tp.Any, gtd: tp.Any) -> None:
        self._b = before
        self._a = after
        self._s = shift
        self._g = gtd

    def __call__(self, dt: tp.Any) -> tp.Any:
        dt = truncate_to_granularity(dt, self._g)
        return [dt + (self._s + i) * self._g.value for i in range(-self._b, self._a + 1)]


def get_interval(
        start_time: tp.Any,
        end_time: tp.Any,
        gtd: tp.Any
) -> tp.Any:

    s = truncate_to_granularity(start_time, gtd)
    f = truncate_to_granularity(end_time, gtd)
    if s == f:
        return []
    res = []

    if s == start_time:
        mult = 0
    else:
        mult = 1

    while True:
        dt = s + mult * gtd.value
        if dt > f:
            break
        res.append(dt.replace(second=0, microsecond=0))
        mult += 1

    return res
