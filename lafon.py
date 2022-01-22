from typing import Union
from fractions import Fraction
from decimal import Decimal, getcontext
from math import exp, pi, floor, factorial, sqrt, pow, log, e
import numpy as np


getcontext().prec = 10


def st(n):
    """ Stirling approximation

    Source: https://www.geeksforgeeks.org/calculating-factorials-using-stirling-approximation/
    """
    if n == 1:
        return 1

    # evaluating factorial using
    # stirling approximation
    n = np.array([n], dtype=np.float32)
    return np.sqrt(2*np.pi * n) * (n / np.e) ** n
    z = (sqrt(2 * pi * n) * pow((n / e), n))
    return floor(z)


def x_over_y(x: int, y: int) -> Decimal:
    """ Computes (T t) kind of calculus

    :param x: Factorial Nominator
    :param y: Factorial Denominator

    >>> x_over_y(5, 3, s=False)
    Fraction(10, 1)

    >>> x_over_y(5, 3, s=True)
    0.1
    """
    return st(x) / (st(y) * st(x - y))


def prob_x_form_1(f: int, k: int, T: int, t: int) -> Decimal:
    """ Computes probability of X = k in Lafon's paper

    Parameters are renamed but they are basically:
    - f = global_freq
    - k = local_freq
    - T = corpus_size
    - t = sample size

    Examples from the paper in p. 139

    Prob(AAA)
    >>> prob_x_form_1(f=3, k=3, T=5, t=3)
    Fraction(1, 10)

    Prob(AAB)
    >>> prob_x_form_1(f=3, k=2, T=5, t=3)
    Fraction(6, 10)

    Prob(ABB)
    >>> prob_x_form_1(f=3, k=1, T=5, t=3)
    Fraction(3, 10)

    """
    return (
            x_over_y(f, k) *
            x_over_y((T - f), (t - k))
    ) / (
        x_over_y(T, t)
    )


def prob_x(f: int, k: int, T: int, t: int) -> Decimal:
    """ Computes probability of X = k in Lafon's paper

    Parameters are renamed but they are basically:
    - f = global_freq
    - k = local_freq
    - T = corpus_size
    - t = sample size

    Examples from the paper in p. 139

    Prob(AAA)
    >>> prob_x(f=296, k=5, T=61449, t=1084)
    Fraction(1, 10)

    Prob(AAB)
    >>> prob_x(f=3, k=2, T=5, t=3)
    Fraction(6, 10)

    Prob(ABB)
    >>> prob_x(f=3, k=1, T=5, t=3)
    Fraction(3, 10)

    """
    log_prob = (
        log(st(f)) +
        log(st(T-f)) +
        log(st(t)) +
        log(st(T-t)) -
        st(T) -
        st(k) -
        log(st(f-k)) -
        log(st(t-k)) -
        log(st(T-f-t+k))
    )
    return np.exp(log_prob)[0]


def valeur_modale_target(f: int, t: int, T: int) -> Decimal:
    """ Calcule la valeur cible pour la valeur modale

    >>> valeur_modale_target(f=296, t=1084, T=61449)
    Fraction(320864, 61449)

    """
    return Fraction(f*t, T)


def define_max_k(t: int, f: int) -> int:
    """ Définit la valeur maximale de k en fonction de f et de t

    La fréquence trouvée dans un échantillon ne peut pas être supérieure à la taille de l'échantillon
    ni ne peut être supérieure à la fréquence réelle de F dans le corpus T.

    >>> define_max_k(t=100, f=5)
    5
    >>> define_max_k(t=5, f=100)
    5
    """
    return min(t, f)


def fonction_cumulative(f: int, K: int, T: int, t: int) -> float:
    """ Calcule toutes les Prob(X = k) pour k <= K

    >>> fonction_cumulative(f=296, K=5, T=61449, t=1084)
    0.576705764428563

    """
    return float(sum([
        prob_x(f=f, k=k, t=t, T=T)
        for k in range(K+1)
    ]))


def fonction_cumulative_comp(f: int, K: int, T: int, t: int) -> float:
    """

    >>> fonction_cumulative_comp(f=296, K=5, T=61449, t=1084)
    0.42329423557143697

    """
    return 1 - fonction_cumulative(f=f, K=K, T=T, t=t)
