# backend/benchmark.py

from algorithms import (
    insertion_sort_count,
    linear_search_count,
    binary_search_count,
)


# =========================================================
# CREATE REALISTIC TASK RECORDS
# =========================================================

def create_tasks(size):
    priorities = ["low", "medium", "high"]

    tasks = []

    for i in range(size):
        tasks.append(
            {
                "id": i + 1,
                "title": f"Task {i + 1}",
                "priority": priorities[i % 3],
                "due_date": f"2026-12-{(i % 28) + 1:02d}",
                "status": "pending",
                "project_id": 1,
            }
        )

    return tasks


# =========================================================
# RUN BENCHMARK
# =========================================================

def run_benchmark(size):
    tasks = create_tasks(size)

    # ------------------------------------------
    # INSERTION SORT
    # Sort by task title
    # ------------------------------------------

    sort_records = [task.copy() for task in tasks]

    sort_comparisons = insertion_sort_count(
        sort_records,
        "title",
    )

    # ------------------------------------------
    # LINEAR SEARCH
    # ------------------------------------------

    linear_records = [task.copy() for task in tasks]

    linear_result = linear_search_count(
        linear_records,
        f"Task {size}",
        "title",
    )

    # ------------------------------------------
    # BINARY SEARCH
    # Records are already sorted by title
    # ------------------------------------------

    binary_result = binary_search_count(
        sort_records,
        f"Task {size}",
        "title",
    )

    # ------------------------------------------
    # RESULT
    # ------------------------------------------

    print()
    print("=" * 60)
    print(f"BENCHMARK - {size} TASK RECORDS")
    print("=" * 60)

    print(f"Insertion Sort comparisons : {sort_comparisons}")
    print(
        f"Linear Search comparisons   : "
        f"{linear_result['comparison_count']}"
    )
    print(
        f"Binary Search comparisons   : "
        f"{binary_result['comparison_count']}"
    )

    print(
        f"Linear Search index         : "
        f"{linear_result['index']}"
    )
    print(
        f"Binary Search index         : "
        f"{binary_result['index']}"
    )


# =========================================================
# MAIN
# =========================================================

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