from algorithms import (
    insertion_sort_with_comparisons,
    linear_search_with_comparisons,
    binary_search_with_comparisons,
)


def create_records(size):
    records = []

    for i in range(size):
        records.append({
            "title": f"Task {i}",
            "priority": "medium"
        })

    return records


def run_benchmark(size):
    records = create_records(size)

    # ------------------------------------------
    # INSERTION SORT
    # ------------------------------------------

    sorted_records, sort_comparisons = (
        insertion_sort_with_comparisons(
            records,
            "title"
        )
    )

    # ------------------------------------------
    # LINEAR SEARCH
    # ------------------------------------------

    linear_index, linear_comparisons = (
        linear_search_with_comparisons(
            records,
            f"Task {size - 1}",
            "title"
        )
    )

    # ------------------------------------------
    # BINARY SEARCH
    # ------------------------------------------

    binary_index, binary_comparisons = (
        binary_search_with_comparisons(
            sorted_records,
            f"Task {size - 1}",
            "title"
        )
    )

    # ------------------------------------------
    # RESULT
    # ------------------------------------------

    print()
    print("=" * 60)
    print(f"BENCHMARK - {size} RECORDS")
    print("=" * 60)

    print(
        f"Insertion Sort comparisons : "
        f"{sort_comparisons}"
    )

    print(
        f"Linear Search comparisons   : "
        f"{linear_comparisons}"
    )

    print(
        f"Binary Search comparisons   : "
        f"{binary_comparisons}"
    )

    print(
        f"Linear Search index         : "
        f"{linear_index}"
    )

    print(
        f"Binary Search index         : "
        f"{binary_index}"
    )


def main():

    print("TaskFlow Algorithm Benchmark")
    print()

    # Required benchmark sizes
    sizes = [10, 500, 3000]

    for size in sizes:
        run_benchmark(size)

    print()
    print("=" * 60)
    print("BENCHMARK COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()