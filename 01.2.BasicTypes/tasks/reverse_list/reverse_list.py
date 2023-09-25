def reverse_iterative(lst: list[int]) -> list[int]:
    """
    Return reversed list. You can use only iteration
    :param lst: input list
    :return: reversed list
    """
    reversed = []
    for i in range(len(lst) - 1, -1, -1):
        reversed.append(lst[i])
    return reversed


def reverse_inplace_iterative(lst: list[int]) -> None:
    """
    Revert list inplace. You can use only iteration
    :param lst: input list
    :return: None
    """
    ll = 0
    r = len(lst) - 1

    while ll < r:
        # Swap the elements at the start and end indices
        lst[ll], lst[r] = lst[r], lst[ll]

        # Move the start and end indices closer to the middle
        ll += 1
        r -= 1


def reverse_inplace(lst: list[int]) -> None:
    """
    Revert list inplace with reverse method
    :param lst: input list
    :return: None
    """
    lst.reverse()


def reverse_reversed(lst: list[int]) -> list[int]:
    """
    Revert list with `reversed`
    :param lst: input list
    :return: reversed list
    """
    return list(reversed(lst))


def reverse_slice(lst: list[int]) -> list[int]:
    """
    Revert list with slicing
    :param lst: input list
    :return: reversed list
    """
    return lst[::-1]
