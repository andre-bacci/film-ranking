def are_elements_contiguous(array: list) -> bool:
    array.sort()
    for i in range(1, len(array)):
        diff = array[i] - array[i - 1]
        if diff != 1:
            return False
    return True


def first_element_is_valid(array: list, expected_first_element) -> bool:
    array.sort()
    if not len(array):
        return True
    return array[0] == expected_first_element
