from contextlib import contextmanager
import sys
import traceback
import typing as tp


@contextmanager
def supresser(*types_: tp.Type[BaseException]) -> tp.Iterator[None]:
    try:
        yield
    except types_:
        pass


@contextmanager
def retyper(type_from: tp.Type[BaseException], type_to: tp.Type[BaseException]) -> tp.Iterator[None]:
    try:
        yield
    except type_from as exception:
        raise type_to(*exception.args)


@contextmanager
def dumper(stream: tp.TextIO | None = None) -> tp.Iterator[None]:
    if stream is None:
        stream = sys.stderr
    try:
        yield
    except Exception as excepion:
        i = traceback.format_exception_only(type(excepion), excepion)
        res = ""
        for elem in i:
            res += elem
        stream.write(res)
        raise
