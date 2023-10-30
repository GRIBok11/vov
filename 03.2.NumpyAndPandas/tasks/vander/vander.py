import numpy as np
import numpy.typing as npt


def vander(array: npt.NDArray[np.float_ | np.int_]) -> npt.NDArray[np.float_]:
    """
    Create a Vandermod matrix from the given vector.
    :param array: input array,
    :return: vandermonde matrix
    """
    array = np.asarray(array).ravel()
    n = len(array)
    result = np.zeros((n, n), dtype=float)
    max_powers = n - 1 - np.arange(n)
    result = np.power(array[:, np.newaxis], max_powers)
    result = result[:, ::-1]

    print("RESULT: ", result)
    return result
