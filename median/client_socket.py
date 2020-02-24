import socket
import datetime
import numpy as np
import pandas as pd

from median.percentile import calculate_percentiles
from typing import Union, Tuple


def create_record(timestamp: datetime.datetime, p25: float, median: float, p75: float):
    """Добавляет запись в таблицу
    :param datetime timestamp: Дата последнего значения
    :param float p25: Текущее значение 25-ого перцентеля
    :param float median: Текущее значение медианы
    :param float p75: Текущее значение 75-ого перцентеля
    :return:
    """
    record = pd.DataFrame(np.array([timestamp, p25, median, p75])).transpose()
    record.to_csv(path_or_buf='median/result.csv', mode='a', header=False, index=False, sep=' ')


def rcv_msg(sock) -> str:
    """Принимает сообщение на сокете
    :param sock: Сокет
    :return str: Сообщение
    """
    try:
        message = sock.recv(1024).decode()
        return message
    except:
        sock.close()


def process_message(message: str, delta: Union[int, float], last_record, p25: float, median: float, p75: float) -> \
                    Tuple[datetime.datetime, float, float, float]:
    """Функция для обработки сообщения
    :param str message: Сообщение для обработки
    :param delta: Точность
    :param last_record: Дата последней записи
    :param float p25: Текущее значение 25-ого перцентеля
    :param float median: Текущее значение медианы
    :param float p75: Текущее значение 75-ого перцентеля
    :return: Дата последней записи
    :return float: Новое значение 25-ого перцентеля
    :return float: Новое значение медианы
    :return float: Новое значение 75-ого перцентеля
    """
    generation_datetime, value = message.split('_')
    p25, median, p75 = calculate_percentiles(delta, int(value), p25, median, p75)
    generation_datetime = datetime.datetime.strptime(generation_datetime, '%Y-%m-%d %H:%M:%S.%f')
    if (generation_datetime - last_record).total_seconds() >= 5:
        last_record = generation_datetime
        create_record(generation_datetime, p25, median, p75)
        print(generation_datetime, p25, median, p75)
    return last_record, p25, median, p75


def main(sock, delta):
    """
    :param sock: Сокет
    :param delta: Точность
    :return:
    """
    p25 = median = p75 = 0
    last_record = datetime.datetime.now()
    while True:
        message = rcv_msg(sock)
        if message:
            last_record, p25, median, p75 = process_message(message, delta, last_record, p25, median, p75)


if __name__ == '__main__':
    sock = socket.socket()
    sock.connect(('localhost', 9090))
    delta = 0.1
    main(sock, delta)
