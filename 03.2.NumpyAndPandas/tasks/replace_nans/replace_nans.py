import numpy as np
import numpy.typing as npt


def replace_nans(matrix: npt.NDArray[np.float_]) -> npt.NDArray[np.float_]:
    """
    Replace all nans in matrix with average of other values.
    If all values are nans, then return zero matrix of the same size.
    :param matrix: matrix,
    :return: replaced matrix
    """
    not_nan_mask = ~np.isnan(matrix)

    if np.any(not_nan_mask):
        mean_value = np.nanmean(matrix[not_nan_mask])
    else:
        return np.zeros_like(matrix)

    matrix[np.isnan(matrix)] = mean_value
    return matrix
