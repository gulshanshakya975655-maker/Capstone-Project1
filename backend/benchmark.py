from algorithms import (
    insertion_sort_with_comparisons,
    linear_search_with_comparisons,
    binary_search_with_comparisons,
)


def create_numbers(size):
    return list(range(size))


def run_benchmark(size):
    numbers = create_numbers(size)

    # ------------------------------------------
    # INSERTION SORT
    # ------------------------------------------

    sorted_numbers, sort_comparisons = (
        insertion_sort_with_comparisons(numbers.copy())
    )

    # ------------------------------------------
    # LINEAR SEARCH
    # ------------------------------------------

    linear_index, linear_comparisons = (
        linear_search_with_comparisons(
            sorted_numbers,
            size - 1
        )
    )

    # ------------------------------------------
    # BINARY SEARCH
    # ------------------------------------------

    binary_index, binary_comparisons = (
        binary_search_with_comparisons(
            sorted_numbers,
            size - 1
        )
    )

    # ------------------------------------------
    # RESULT
    # ------------------------------------------

    print()
    print("=" * 60)
    print(f"BENCHMARK - {size} RECORDS")
    print("=" * 60)

    print(f"Insertion Sort comparisons : {sort_comparisons}")
    print(f"Linear Search comparisons   : {linear_comparisons}")
    print(f"Binary Search comparisons   : {binary_comparisons}")
    print(f"Linear Search index         : {linear_index}")
    print(f"Binary Search index         : {binary_index}")


def main():
    print("TaskFlow Algorithm Benchmark")
    print()

    sizes = [10, 500, 3000]

    for size in sizes:
        run_benchmark(size)

    print()
    print("=" * 60)
    print("BENCHMARK COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()