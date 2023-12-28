import numpy as np
import numpy.typing as npt


def max_element(array: npt.NDArray[np.int_]) -> int | None:
    """
    Return the maximum element in the input array preceded by a zero.
    If no such element is found, return None.
    :param array: array,
    :return: max element value or None
    """
