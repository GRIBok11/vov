import time
import typing as tp


class TimeoutException(BaseException):
    pass


class SoftTimeoutException(TimeoutException):
    pass


class HardTimeoutException(TimeoutException):
    pass


class TimeCatcher:
    def __init__(self, soft_timeout=None, hard_timeout=None) -> None:  # type: ignore

        assert (soft_timeout is None or
                hard_timeout is None or
                hard_timeout >= soft_timeout)

        if soft_timeout is not None:
            assert soft_timeout > 0
        if hard_timeout is not None:
            assert hard_timeout > 0
        self.tt = soft_timeout
        self.td = hard_timeout

    def __enter__(self) -> tp.Any:
        self.start = time.time()
        return self

    def __float__(self) -> tp.Any:
        self.__exit__(None, None, None)
        return self.rt

    def __str__(self) -> str:
        self.__exit__(None, None, None)
        return f"Time consumed: {self.__float__():.4f}"

    def __exit__(self, ar1: tp.Any, ar2: tp.Any, ar3: tp.Any) -> None:
        self.rt = time.time() - self.start
        if self.tt is not None and self.rt > self.tt:
            raise SoftTimeoutException
        if self.td is not None and self.rt > self.td:
            raise HardTimeoutException
        return
