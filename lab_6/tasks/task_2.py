"""
Na (1 pkt.):
Napisz program do sprawdzenia poprawności skompresowanego wyjścia poprzedniej
funkcji.
Funkcja MUSI w swej implementacji korzystać z wyrażeń regularnych.

Funkcja na wejściu przyjmuje nazwę pliku do sprawdzenia, na wyjściu zwraca
dwuelementową tuplę zawierającą liczbę poprawnych wierszy:
- na indeksie 0 płeć F
- na indeksie 1 płeć M
"""
import re


def check_existence(pattern, line):
    return bool(re.fullmatch(pattern, line))


def check_animal_list(file_path):
    with open(file_path) as _input:
        lines = _input.readlines()
    f_count = 0
    m_count = 0

    f = r'^[a-fA-F\d]{8}\-[a-fA-F\d]{4}\-[a-fA-F\d]{4}\-[a-fA-F\d]{4}\-[a-fA-F\d]{12}_F_[\d]\.[\d]{3}e[\-\+][\d]{2}$'
    m = r'^[a-fA-F\d]{8}\-[a-fA-F\d]{4}\-[a-fA-F\d]{4}\-[a-fA-F\d]{4}\-[a-fA-F\d]{12}_M_[\d]\.[\d]{3}e[\-\+][\d]{2}$'

    for line in lines:
        line = line.strip()
        m_count += check_existence(m, line)
        f_count += check_existence(f, line)
    return f_count, m_count


if __name__ == '__main__':
    assert check_animal_list('s_animals_sce.txt') == (2, 2)
    assert check_animal_list('animals_sc_corrupted.txt') == (5, 1)
