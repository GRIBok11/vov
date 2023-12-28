import numpy as np
import numpy.typing as npt


def nearest_value(matrix: npt.NDArray[np.float_], value: float) -> float | None:
    """
    Find nearest value in matrix.
    If matrix is empty return None
    :param matrix: input matrix
    :param value: value to find
    :return: nearest value in matrix or None
    """
    flat_matrix = matrix.flatten()

    if flat_matrix.size == 0:
        return None
    idx = np.argmin(np.abs(flat_matrix - value))

    return flat_matrix[idx]
