from math import floor


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    else:
        for i in range(2, floor(n**0.5) + 1):
            if n % i == 0:
                return False
    return True
