import numpy as np
import pandas as pd
import os
import tempfile


def generate(path, rows: int, columns: int):
    """Генерирует матрицу заданного размера
    :param str path: Имя файла для генерации
    :param int rows: Количсетво строк
    :param int columns: Количество столбцов
    """
    mode = 'w'
    while rows > 0:
        if rows >= 8:
            matrix = pd.DataFrame(np.random.randint(10, 100, size=(8, columns), dtype=np.int32))
        else:
            matrix = pd.DataFrame(np.random.randint(10, 100, size=(rows, columns), dtype=np.int32))
        rows -= 8
        matrix.to_csv(path_or_buf=path, sep=' ', mode=mode, header=False, index=False)
        mode = 'a'


def read_column(matrix_path, index_col):
    return pd.read_csv(filepath_or_buffer=matrix_path, sep=' ', header=None, usecols=[index_col], squeeze=True,
                       dtype=np.int32)


def fast_sort_matrix(matrix_path, sorted_matrix_path):
    """Функция сортировки матрицы по столбцам
    :param str matrix_path: Путь к файлу с матрицей
    :param sorted_matrix_path: Путь к файлу для отсортированной матрицы
    """
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file_name = temp_file.name
    header = False
    row = pd.read_csv(filepath_or_buffer=matrix_path, nrows=1, sep=' ', header=None)
    for i in range(row.shape[1]):
        col = read_column(matrix_path, i)
        col = col.sort_values()
        col = col.to_frame().transpose()
        col.to_csv(path_or_buf=temp_file_name, mode='a', sep=' ', header=header, index=False)
    mode = 'w'
    row = pd.read_csv(filepath_or_buffer=temp_file, nrows=1, sep=' ', header=None)
    for i in range(row.shape[1]):
        col = read_column(temp_file_name, i)
        col = col.to_frame().transpose()
        col.to_csv(path_or_buf=sorted_matrix_path, mode=mode, sep=' ', header=False, index=False)
        mode = 'a'
    os.remove(temp_file_name)
