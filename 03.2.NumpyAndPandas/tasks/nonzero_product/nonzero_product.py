import numpy as np
import numpy.typing as npt


def nonzero_product(matrix: npt.NDArray[np.int_]) -> int | None:
    """
    Compute product of nonzero diagonal elements of matrix
    If all diagonal elements are zeros, then return None
    :param matrix: array,
    :return: product value or None
    """
    diag = np.diagonal(matrix) != 0

    nonzero_elements = np.diagonal(matrix)[diag]

    if len(nonzero_elements) == 0:
        return None
    else:
        return np.prod(nonzero_elements)
