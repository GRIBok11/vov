def filter_list_by_list(lst_a: list[int] | range, lst_b: list[int] | range) -> list[int]:
    """
    Filter first sorted list by other sorted list
    :param lst_a: first sorted list
    :param lst_b: second sorted list
    :return: filtered sorted list
    """

    ans = []
    i, j = 0, 0

    while i < len(lst_a):
        if j >= len(lst_b) or lst_a[i] < lst_b[j]:
            ans.append(lst_a[i])
            i += 1
        elif lst_a[i] == lst_b[j]:
            tmp_a = lst_a[i]
            while lst_a[i] == tmp_a:
                i += 1
                if i >= len(lst_a):
                    return ans
            j += 1
        else:
            j += 1

    return ans
