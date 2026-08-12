from algorithms import (
    insertion_sort,
    binary_search,
    linear_search,
    insertion_sort_count,
    binary_search_count,
    linear_search_count,
)


def check(case_name, result, expected):
    if result == expected:
        print(f"PASS: {case_name}")
        return True
    else:
        print(
            f"FAIL: {case_name} — expected {expected}, got {result}"
        )
        return False


def main():
    passed = 0
    total = 0

    # ==========================================
    # 1. INSERTION SORT - EMPTY LIST
    # ==========================================

    records = []

    insertion_sort(records, "title")

    total += 1
    if check(
        "Insertion sort empty list",
        records,
        []
    ):
        passed += 1

    # ==========================================
    # 2. INSERTION SORT - SINGLE ELEMENT
    # ==========================================

    records = [
        {"title": "Only Task"}
    ]

    insertion_sort(records, "title")

    total += 1
    if check(
        "Insertion sort single element",
        records,
        [{"title": "Only Task"}]
    ):
        passed += 1

    # ==========================================
    # 3. INSERTION SORT - NORMAL CASE
    # ==========================================

    records = [
        {"title": "Banana"},
        {"title": "Apple"},
        {"title": "Cherry"},
    ]

    insertion_sort(records, "title")

    expected = [
        {"title": "Apple"},
        {"title": "Banana"},
        {"title": "Cherry"},
    ]

    total += 1
    if check(
        "Insertion sort normal case",
        records,
        expected
    ):
        passed += 1

    # ==========================================
    # 4. BINARY SEARCH - FIRST INDEX
    # ==========================================

    records = [
        {"title": "Apple"},
        {"title": "Banana"},
        {"title": "Cherry"},
        {"title": "Mango"},
        {"title": "Orange"},
    ]

    result = binary_search(
        records,
        "Apple",
        "title"
    )

    total += 1
    if check(
        "Binary search first index",
        result,
        0
    ):
        passed += 1

    # ==========================================
    # 5. BINARY SEARCH - LAST INDEX
    # ==========================================

    result = binary_search(
        records,
        "Orange",
        "title"
    )

    total += 1
    if check(
        "Binary search last index",
        result,
        4
    ):
        passed += 1

    # ==========================================
    # 6. BINARY SEARCH - MIDDLE INDEX
    # ==========================================

    result = binary_search(
        records,
        "Cherry",
        "title"
    )

    total += 1
    if check(
        "Binary search middle index",
        result,
        2
    ):
        passed += 1

    # ==========================================
    # 7. BINARY SEARCH - NOT FOUND
    # ==========================================

    result = binary_search(
        records,
        "Watermelon",
        "title"
    )

    total += 1
    if check(
        "Binary search not found",
        result,
        -1
    ):
        passed += 1

    # ==========================================
    # 8. LINEAR SEARCH - FOUND
    # ==========================================

    records = [
        {"title": "Apple"},
        {"title": "Banana"},
        {"title": "Cherry"},
    ]

    result = linear_search(
        records,
        "Banana",
        "title"
    )

    total += 1
    if check(
        "Linear search found",
        result,
        1
    ):
        passed += 1

    # ==========================================
    # 9. LINEAR SEARCH - NOT FOUND
    # ==========================================

    result = linear_search(
        records,
        "Mango",
        "title"
    )

    total += 1
    if check(
        "Linear search not found",
        result,
        -1
    ):
        passed += 1

    # ==========================================
    # 10. INSERTION SORT COUNT
    # ==========================================

    records = [
        {"value": 5},
        {"value": 1},
        {"value": 3},
        {"value": 2},
        {"value": 4},
    ]

    comparison_count = insertion_sort_count(
        records,
        "value"
    )

    expected_records = [
        {"value": 1},
        {"value": 2},
        {"value": 3},
        {"value": 4},
        {"value": 5},
    ]

    total += 1
    if check(
        "Insertion sort count sorted result",
        records,
        expected_records
    ):
        passed += 1

    # comparison_count must be int > 0
    total += 1

    if (
        type(comparison_count) == int
        and comparison_count > 0
    ):
        print(
            f"PASS: Insertion sort comparison count "
            f"({comparison_count})"
        )
        passed += 1
    else:
        print(
            "FAIL: Insertion sort comparison count"
        )

    # ==========================================
    # 11. BINARY SEARCH COUNT
    # ==========================================

    records = [
        {"value": 1},
        {"value": 2},
        {"value": 3},
        {"value": 4},
        {"value": 5},
    ]

    result = binary_search_count(
        records,
        3,
        "value"
    )

    total += 1

    if (
        type(result) == dict
        and result.get("index") == 2
        and type(result.get("comparison_count")) == int
        and result.get("comparison_count") > 0
    ):
        print(
            f"PASS: Binary search count "
            f"({result})"
        )
        passed += 1
    else:
        print(
            f"FAIL: Binary search count — "
            f"got {result}"
        )

    # ==========================================
    # 12. LINEAR SEARCH COUNT - ABSENT VALUE
    # ==========================================

    records = [
        {"value": 1},
        {"value": 2},
        {"value": 3},
        {"value": 4},
        {"value": 5},
    ]

    result = linear_search_count(
        records,
        99,
        "value"
    )

    total += 1

    expected = {
        "index": -1,
        "comparison_count": 5
    }

    if check(
        "Linear search count absent value",
        result,
        expected
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