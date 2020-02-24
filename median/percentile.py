from typing import Union, Tuple


def sgn(value: int, percentile: Union[int, float]) -> int:
    """Сигма-функция
    :param int value: Текущее число
    :param percentile: Текущее значение перцентиля
    :return int: Результат сигма-функции
    """
    if value > percentile:
        return 1
    if value < percentile:
        return -1
    if value == percentile:
        return 0


def calculate_percentiles(delta: Union[int, float], value: int, percentile25: Union[int, float],
                          median: Union[int, float], percentile75: Union[int, float]) -> Tuple[float, float, float]:
    """Функция, вычисляющая значения перцентилей
    :param delta: Точность
    :param int value: Текущее число
    :param percentile25: Текущее значение 25-ого перцентеля
    :param median: Текущее значение медианы
    :param percentile75: Текущее значение 75-ого перцентиля
    :return: Новое значение 25-ого перцентеля
    :return: Новое значение медианы
    :return: Новое значение 75-ого перцентеля
    """
    percentile25 += delta * (sgn(value, percentile25) + 2 * 0.25 - 1)
    median += delta * (sgn(value, median) + 2 * 0.5 - 1)
    percentile75 += delta * (sgn(value, percentile75) + 2 * 0.75 - 1)
    return percentile25, median, percentile75
