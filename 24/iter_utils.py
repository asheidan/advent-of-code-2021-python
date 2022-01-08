import itertools


def grouper(iterable, n: int, fillvalue=None):
    """Return iterator over groups of n elements taken from iterable.

    Arguments:
        iterable: something iterable
        n: group size
        fillvalue: something to pad the last group to size n
    """
    args = [iter(iterable)] * n
    return itertools.zip_longest(fillvalue=fillvalue, *args)
