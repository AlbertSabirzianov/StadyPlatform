# actions во вьюсетах, направленные исключительно на get запросы
SAFE_ACTIONS = [
    'list',
    'retrieve'
]


def get_percentage(first: int, second: int) -> float:
    """Процентное соотношение первого числа ко второму."""

    if second == 0:
        raise ValueError(
            'Нельзя получить процентное соотношение к нулю!'
        )

    return (first / second) * 100
