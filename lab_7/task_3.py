import numpy as np


def estimate_pi(n):
    """
    Returns estimated value of pi.

    Funkcja szacuje wartość pi metodą probabilistyczną.
    Wygenerujmy m punktów z obszaru [-1,1]^2. Niech k określa liczbę punktów
    odległych od punku (0,0) o nie więcej niż 1. Proporcja 4k/m
    powinna szacować wartość pi.
    (1pkt).

    :param n: Number of points to made estimation.
    :type xy: int
    :return: Estimated Pi value
    :rtype: float
    """
    x = np.random.rand(n) * 2 - 1 #losujemy liczbę z przedziału -1 do 1 dla x
    y = np.random.rand(n) * 2 - 1 #losujemy liczbę z przedziału -1 do 1 dla y
    r = x ** 2 + y ** 2
    r = r ** 0.5
    k = (r <= 1).sum()
    pi = 4 * k / n
    return pi


if __name__ == '__main__':
    np.testing.assert_approx_equal(estimate_pi(int(1e2)), np.pi, 1)
    np.testing.assert_approx_equal(estimate_pi(int(1e3)), np.pi, 2)
