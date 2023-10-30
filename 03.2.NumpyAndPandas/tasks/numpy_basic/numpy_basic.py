import numpy as np
import numpy.typing as npt


def construct_array(
        matrix: npt.NDArray[np.int_],
        row_indices: npt.NDArray[np.int_] | list[int],
        col_indices: npt.NDArray[np.int_] | list[int]
) -> npt.NDArray[np.int_]:
    """
    Construct slice of given matrix by indices row_indices and col_indices:
    [matrix[row_indices[0], col_indices[0]], ... , matrix[row_indices[N-1], col_indices[N-1]]]
    :param matrix: input matrix
    :param row_indices: list of row indices
    :param col_indices: list of column indices
    :return: matrix slice
    """

    if isinstance(row_indices, list):
        row_indices = np.array(row_indices)
    if isinstance(col_indices, list):
        col_indices = np.array(col_indices)

    if len(row_indices) == 0 or len(col_indices) == 0:
        return np.array([])

    selected_elements = matrix[row_indices, col_indices]
    return selected_elements

    return selected_elements


def detect_identic(
        lhs_array: npt.ArrayLike,
        rhs_array: npt.ArrayLike
) -> bool:
    """
    Check whether two arrays are equal or not
    :param lhs_array: first array
    :param rhs_array: second array
    :return: True if input arrays are equal, False otherwise
    """
    lhs_array = np.asarray(lhs_array)
    rhs_array = np.asarray(rhs_array)

    return np.array_equal(lhs_array, rhs_array)


def mean_channel(X: npt.NDArray[np.float_]) -> npt.NDArray[np.float_]:
    """
    Given color image (3-dimensional vector of size (n, m, 3).
    Compute average value for all 3 channels
    :param X: color image
    :return: array of size 3 with average values
    """
    mean_values = np.mean(X, axis=(0, 1))
    return mean_values


def get_unique_rows(X: npt.NDArray[np.int_]) -> npt.NDArray[np.int_]:
    """
    Compute unique rows of matrix
    :param X: matrix
    :return: matrix of unique rows
    """
    X_1d = X.view([('', X.dtype)] * X.shape[1])

    # Используем np.unique для получения уникальных строк
    unique_rows = np.unique(X_1d)

    # Возвращаем уникальные строки в исходном формате
    return unique_rows.view(X.dtype).reshape(-1, X.shape[1])


def construct_matrix(
        first_array: npt.NDArray[np.int_], second_array: npt.NDArray[np.int_]
) -> npt.NDArray[np.int_]:
    """
    Construct matrix from pair of arrays
    :param first_array: first array
    :param second_array: second array
    :return: constructed matrix
    """
    result_matrix = np.column_stack((first_array, second_array))
    return result_matrix
