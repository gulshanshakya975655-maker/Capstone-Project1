from algorithms import (
    insertion_sort,
    insertion_sort_with_comparisons,
    linear_search,
    linear_search_with_comparisons,
    binary_search,
    binary_search_with_comparisons,
)


def check(name, actual, expected):
    if actual == expected:
        print(f"PASS - {name}")
        return True

    print(f"FAIL - {name}")
    print(f"Expected: {expected}")
    print(f"Actual:   {actual}")
    return False


def main():
    passed = 0
    total = 0

    records = [
        {"title": "ramesh", "priority": "high"},
        {"title": "cow story", "priority": "low"},
        {"title": "Frontend Test", "priority": "medium"},
        {"title": "Apple", "priority": "high"},
        {"title": "Banana", "priority": "low"},
    ]

    # ==========================================
    # INSERTION SORT
    # ==========================================

    total += 1

    sorted_records = insertion_sort(
        records,
        "title"
    )

    sorted_titles = [
        record["title"]
        for record in sorted_records
    ]

    expected_titles = [
        "Apple",
        "Banana",
        "Frontend Test",
        "cow story",
        "ramesh",
    ]

    if check(
        "Insertion Sort",
        sorted_titles,
        expected_titles
    ):
        passed += 1

    # ==========================================
    # INPUT NOT MUTATED
    # ==========================================

    original_records = [record.copy() for record in records]

    insertion_sort(
        records,
        "title"
    )

    total += 1

    if check(
        "Input Not Mutated",
        records,
        original_records
    ):
        passed += 1

    # ==========================================
    # INSERTION SORT WITH COMPARISONS
    # ==========================================

    sorted_records, comparisons = (
        insertion_sort_with_comparisons(
            records,
            "title"
        )
    )

    total += 1

    if check(
        "Insertion Sort Comparison Result",
        [
            record["title"]
            for record in sorted_records
        ],
        expected_titles
    ):
        passed += 1

    total += 1

    if comparisons > 0:
        print(
            f"PASS - Insertion Sort Comparisons ({comparisons})"
        )
        passed += 1
    else:
        print("FAIL - Insertion Sort Comparisons")

    # ==========================================
    # LINEAR SEARCH - FOUND
    # ==========================================

    index, comparisons = linear_search(
        records,
        "ramesh",
        "title"
    )

    total += 1

    if check(
        "Linear Search Found",
        index,
        0
    ):
        passed += 1

    total += 1

    if comparisons > 0:
        print(
            f"PASS - Linear Search Comparisons ({comparisons})"
        )
        passed += 1
    else:
        print("FAIL - Linear Search Comparisons")

    # ==========================================
    # LINEAR SEARCH - NOT FOUND
    # ==========================================

    index, comparisons = linear_search(
        records,
        "Not Found",
        "title"
    )

    total += 1

    if check(
        "Linear Search Not Found",
        index,
        -1
    ):
        passed += 1

    # ==========================================
    # LINEAR SEARCH WITH COMPARISONS
    # ==========================================

    index, comparisons = (
        linear_search_with_comparisons(
            records,
            "Frontend Test",
            "title"
        )
    )

    total += 1

    if check(
        "Linear Search With Comparisons",
        index,
        2
    ):
        passed += 1

    # ==========================================
    # BINARY SEARCH
    # ==========================================

    binary_records = insertion_sort(
        records,
        "title"
    )

    index, comparisons = binary_search(
        binary_records,
        "Frontend Test",
        "title"
    )

    total += 1

    if check(
        "Binary Search Found",
        index,
        2
    ):
        passed += 1

    total += 1

    if comparisons > 0:
        print(
            f"PASS - Binary Search Comparisons ({comparisons})"
        )
        passed += 1
    else:
        print("FAIL - Binary Search Comparisons")

    # ==========================================
    # BINARY SEARCH - NOT FOUND
    # ==========================================

    index, comparisons = binary_search(
        binary_records,
        "ZZZZ",
        "title"
    )

    total += 1

    if check(
        "Binary Search Not Found",
        index,
        -1
    ):
        passed += 1

    # ==========================================
    # BINARY SEARCH WITH COMPARISONS
    # ==========================================

    index, comparisons = (
        binary_search_with_comparisons(
            binary_records,
            "ramesh",
            "title"
        )
    )

    total += 1

    if check(
        "Binary Search With Comparisons",
        index,
        4
    ):
        passed += 1

    # ==========================================
    # FINAL RESULT
    # ==========================================

    print()
    print("=" * 55)
    print(f"RESULT: {passed}/{total} checks passed")

    if passed == total:
        print("ALL ALGORITHM CHECKS PASSED")
    else:
        print("SOME ALGORITHM CHECKS FAILED")


if __name__ == "__main__":
    main()