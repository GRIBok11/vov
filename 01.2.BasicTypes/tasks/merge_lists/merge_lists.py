def merge_iterative(lst_a: list[int], lst_b: list[int]) -> list[int]:
    """
    Merge two sorted lists in one sorted list
    :param lst_a: first sorted list
    :param lst_b: second sorted list
    :return: merged sorted list
    """

    merged = []
    i, j = 0, 0

    while i < len(lst_a) and j < len(lst_b):
        if lst_a[i] < lst_b[j]:
            merged.append(lst_a[i])
            i += 1
        else:
            merged.append(lst_b[j])
            j += 1

    while i < len(lst_a):
        merged.append(lst_a[i])
        i += 1

    while j < len(lst_b):
        merged.append(lst_b[j])
        j += 1
    return merged


def merge_sorted(lst_a: list[int], lst_b: list[int]) -> list[int]:
    """
    Merge two sorted lists in one sorted list using `sorted`
    :param lst_a: first sorted list
    :param lst_b: second sorted list
    :return: merged sorted list
    """
    return sorted(lst_a + lst_b)
