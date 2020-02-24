import socket
import datetime
import time
import numpy as np


def sock_init():
    """Инициализирует сокет"""
    sock = socket.socket()
    sock.bind(('', 9090))
    sock.listen(1)
    conn, addr = sock.accept()
    print('connected:', addr)
    return conn


def send_value(conn):
    """Функция генерации и отправки сообщения
    :param conn: Сокет
    :return:
    """
    while True:
        generation_datetime = datetime.datetime.now()
        number = np.random.randint(-9223372036854775808, 9223372036854775807, dtype=np.int64)
        data = '_'.join((str(generation_datetime), str(number)))
        try:
            conn.send(data.encode())
            time.sleep(0.01 - (datetime.datetime.now() - generation_datetime).total_seconds())
        except ValueError:
            continue
        except Exception:
            conn.close()
            return


if __name__ == '__main__':
    conn = sock_init()
    send_value(conn)
