from typing import List, Dict
from dataclasses import dataclass


@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int


@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int


def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    """
    Оптимізує чергу 3D-друку згідно з пріоритетами та обмеженнями принтера

    Args:
        print_jobs: Список завдань на друк
        constraints: Обмеження принтера

    Returns:
        Dict з порядком друку та загальним часом
    """
    jobs = [PrintJob(**job) for job in print_jobs]
    jobs.sort(key=lambda job: (job.priority, job.volume / job.print_time))

    printer_constraints = PrinterConstraints(**constraints)

    total_print_time = 0
    print_schedule = []

    current_batch_volume = 0
    current_batch_items = 0
    max_batch_time = 0

    for job in jobs:
        if (
            current_batch_items == printer_constraints.max_items
            or current_batch_volume + job.volume > printer_constraints.max_volume
        ):
            current_batch_items = 0
            current_batch_volume = 0
            total_print_time += max_batch_time
            max_batch_time = 0

        if (
            current_batch_items < printer_constraints.max_items
            and current_batch_volume + job.volume <= printer_constraints.max_volume
        ):
            print_schedule.append(job.id)
            current_batch_items += 1
            current_batch_volume += job.volume
            max_batch_time = max(max_batch_time, job.print_time)

    total_print_time += max_batch_time

    return {"print_order": print_schedule, "total_time": total_print_time}


def test_printing_optimization():
    test1_jobs = [
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 1, "print_time": 150},
    ]

    test2_jobs = [
        {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {
            "id": "M3",
            "volume": 120,
            "priority": 3,
            "print_time": 150,
        },
    ]

    test3_jobs = [
        {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
        {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
        {"id": "M3", "volume": 180, "priority": 2, "print_time": 120},
    ]

    constraints = {"max_volume": 300, "max_items": 2}

    print("Тест 1 (однаковий пріоритет):")
    result1 = optimize_printing(test1_jobs, constraints)
    print(f"Порядок друку: {result1['print_order']}")
    print(f"Загальний час: {result1['total_time']} хвилин")

    print("\nТест 2 (різні пріоритети):")
    result2 = optimize_printing(test2_jobs, constraints)
    print(f"Порядок друку: {result2['print_order']}")
    print(f"Загальний час: {result2['total_time']} хвилин")

    print("\nТест 3 (перевищення обмежень):")
    result3 = optimize_printing(test3_jobs, constraints)
    print(f"Порядок друку: {result3['print_order']}")
    print(f"Загальний час: {result3['total_time']} хвилин")


if __name__ == "__main__":
    test_printing_optimization()