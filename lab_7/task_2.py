import numpy as np


def calculate_neighbours(board):
    """
    W odpowiedzi chcemy dostać macierz 6x6
    Skorzystać z calculate neighbour
    Returns number of neighbours of board cells.

    Funkcja zwraca tablicę która w polu [R, C] zwraca liczbę sąsiadów którą
    ma komórka board[R, C].
    Obowiązuje sąsiedztwo Moore'a tzn. za sąsiada uznajemy żywą komórkę
    stykającą się bokiem bokach lub na ukos od danej komórki,
    więc maksymalna ilość sąsiadów danej komórki wynosi 8.
    Funkcja ta powinna być zwektoryzowana, tzn. liczba operacji w bytecodzie
    Pythona nie powinna zależeć od rozmiaru macierzy.
    (1 pkt.)

    Podpowiedź: Czy jest możliwe obliczenie ilości np. lewych sąsiadów
    których ma każda z komórek w macierzy, następnie liczby prawych sąsiadów
    itp.
    Podpowiedź II: Proszę uważać na komówki na bokach i rogach planszy.

    :param board: 2D array of agents states.
    :type board: np.ndarray
    :param periodic
    """
    neighbours = np.zeros(board.shape, int)
    neighbours[:, 1:] += board[:, :-1]  # sasiedzi na lewo, bez pierwszej kolumny bo tam nie ma na lewo
    neighbours[:, :-1] += board[:, 1:]  # sąsiedzi na prawo, bez ostatniej kolumny bo tam nie ma na prawo
    neighbours[:-1, :] += board[1:, :]  # sasiedzi na dole, bez ostatniego wiersza bo tam nie ma na dół
    neighbours[1:, :] += board[:-1, :]  # sasiedzi na górze, bez pierwszego wiersza bo tam nie ma na góry
    neighbours[:-1, :-1] += board[1:, 1:]  # sasiedzi skos dół-prawo
    neighbours[:-1, 1:] += board[1:, :-1]  # sasiedzi skos dół-lewo
    neighbours[1:, :-1] += board[:-1, 1:]  # sasiedzi skos góra-prawo
    neighbours[1:, 1:] += board[:-1, :-1]  # sasiedzi skos góra-lewo
    return neighbours


def iterate(board):
    """
    Returns next iteration step of given board.

    Funkcja pobiera planszę game of life i zwraca jej następną iterację.
    Zasady Game of life są takie:
    1. Komórka może być albo żywa (True) albo martwa (False).
    2. Jeśli komórka jest martwa i ma trzech sąsiadów to ożywa.
    3. Jeśli komórka jest żywa i ma mniej niż dwóch sąsiadów to umiera,
       jeśli ma więcej niż trzech sąsiadów również umiera.
       W przeciwnym wypadku (dwóch lub trzech sąsiadów) to żyje dalej.
    (1 pkt.)

    :param board: 2D array of agents states.
    :type board: np.ndarray
    :return: next board state
    :rtype: np.ndarray
    """
    neighbours = calculate_neighbours(board)
    new_board = np.zeros_like(board) #tworzymy tablice na wartości true i false o takim samym wymiarze
    new_board[board] = np.logical_or(neighbours[board] == 2, neighbours[board] == 3) #jeżeli ma 2 lub 3 sąsiadów to zwraca true żyje, dla mniej niż 2 będzie FALSE, dla więcej niż 3 też FALSE
    new_board[np.logical_not(board)] = neighbours[np.logical_not(board)] == 3 #Jeśli komórka jest martwa i ma trzech sąsiadów to ożywa.

    return new_board


if __name__ == '__main__':
    _board = np.array([
        [False, False, False,  True, False,  True],
        [ True, False,  True, False, False,  True],
        [ True,  True, False,  True,  True,  True],
        [False,  True,  True, False, False,  True],
        [False, False, False,  True, False, False],
        [False,  True,  True,  True, False,  True]
    ])
    assert (calculate_neighbours(_board) == np.array([
        [1, 2, 2, 1, 3, 1,],
        [2, 4, 3, 4, 6, 3,],
        [3, 5, 5, 3, 4, 3,],
        [3, 3, 4, 4, 5, 2,],
        [2, 4, 6, 3, 4, 2,],
        [1, 1, 3, 2, 3, 0,],
    ])).all()
    assert (iterate(_board) == np.array([
        [False, False, False, False, True, False],
        [ True, False,  True, False, False,  True],
        [ True, False, False,  True, False,  True],
        [True,  True, False, False, False,  True],
        [False, False, False,  True, False, False],
        [False, False,  True,  True, True, False],
    ])).all()

