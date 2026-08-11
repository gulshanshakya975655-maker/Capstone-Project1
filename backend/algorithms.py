def insertion_sort(records, key):
    records = records.copy()
    comparisons = 0

    for i in range(1, len(records)):
        current = records[i]
        j = i - 1

        while j >= 0:
            comparisons += 1

            if records[j][key] > current[key]:
                records[j + 1] = records[j]
                j -= 1
            else:
                break

        records[j + 1] = current

    return records


def linear_search(records, target_value, key):
    comparisons = 0

    for index, record in enumerate(records):
        comparisons += 1

        if str(record[key]).lower() == str(target_value).lower():
            return index, comparisons

    return -1, comparisons


def binary_search(records, target_value, key):
    left = 0
    right = len(records) - 1
    comparisons = 0

    target = str(target_value).lower()

    while left <= right:
        middle = (left + right) // 2

        current_value = str(
            records[middle][key]
        ).lower()

        comparisons += 1

        if current_value == target:
            return middle, comparisons

        if current_value < target:
            left = middle + 1
        else:
            right = middle - 1

    return -1, comparisons


def insertion_sort_with_comparisons(records, key):
    sorted_records = insertion_sort(records, key)

    comparisons = 0

    for i in range(1, len(records)):
        current = records[i]
        j = i - 1

        while j >= 0:
            comparisons += 1

            if records[j][key] > current[key]:
                j -= 1
            else:
                break

    return sorted_records, comparisons


def linear_search_with_comparisons(
    records,
    target_value,
    key
):
    return linear_search(
        records,
        target_value,
        key
    )


def binary_search_with_comparisons(
    records,
    target_value,
    key
):
    return binary_search(
        records,
        target_value,
        key
    )