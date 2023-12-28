from collections.abc import Sequence


def find_median(nums1: Sequence[int], nums2: Sequence[int]) -> float:
    """
    Find median of two sorted sequences. At least one of sequences should be not empty.
    :param nums1: sorted sequence of integers
    :param nums2: sorted sequence of integers
    :return: middle value if sum of sequences' lengths is odd
             average of two middle values if sum of sequences' lengths is even
    """

    c = []

    i, j = 0, 0

    while i < len(nums1) and j < len(nums2):
        if nums1[i] < nums2[j]:
            c.append(nums1[i])
            i += 1
        else:
            c.append(nums2[j])
            j += 1

    c.extend(nums1[i:])
    c.extend(nums2[j:])

    ll = len(c)

    if ll % 2 == 1:
        return float(c[ll // 2])
    else:
        m1 = c[(ll - 1) // 2]
        m2 = c[ll // 2]
        return (m1 + m2) / 2.0
