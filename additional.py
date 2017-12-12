from functools import reduce
from random import randint

def gcdlist(elements):
    gcd_res = 0
    for i in range(len(elements)-1):
        gcd_res = gcd(gcd_res, elements[i])
    return gcd_res

def gcd(a, b):
    """
    :param a:
    :param b:
    :return: greatest common divisor of a and b
    """
    if b == 0:
        return a
    else:
        return gcd(b, a % b)

def lcm(a,b):
    """
    :param a:
    :param b:
    :return: least common multiple of a and b
    """
    return a*b//gcd(a,b)

def lcmArray(args):
    """
    :param args: list of int
    :return: return the least common multiple of all values in args list
    """
    return reduce(lcm, args)

def getRandValue(min_value, top_value):
    value = randint(min_value,top_value)
    actual_value = value*10
    return actual_value
