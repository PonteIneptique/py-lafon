from math import factorial
from typing import Union
from fractions import Fraction


def x_over_y(x: int, y: int) -> Fraction:
    """ Computes (T t) kind of calculus

    >>> x_over_y(5, 3)
    Fraction(10, 1)
    """
    return Fraction(factorial(x), (factorial(y) * factorial(x-y)))


def prob_x(f: int, k: int, T: int, t: int) -> Fraction:
    """ Computes probability of X = k in Lafon's paper

    Parameters are renamed but they are basically:
    - f = global_freq
    - k = local_freq
    - T = corpus_size
    - t = sample size

    Examples from the paper in p. 139

    Prob(AAA)
    >>> prob_x(f=3, k=3, T=5, t=3)
    Fraction(1, 10)

    Prob(AAB)
    >>> prob_x(f=3, k=2, T=5, t=3)
    Fraction(6, 10)

    Prob(ABB)
    >>> prob_x(f=3, k=1, T=5, t=3)
    Fraction(3, 10)

    """
    return (
            x_over_y(f, k) *
            x_over_y((T - f), (t - k))
    ) / (
        x_over_y(T, t)
    )


def valeur_modale_target(f: int, t: int, T: int) -> Fraction:
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
