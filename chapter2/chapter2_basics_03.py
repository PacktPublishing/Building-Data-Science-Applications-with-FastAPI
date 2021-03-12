def euclidean_division(dividend, divisor):
    quotient = dividend // divisor
    remainder = dividend % divisor
    return (quotient, remainder)


t = euclidean_division(3, 2)
assert t[0] == 1
assert t[1] == 1

q, r = euclidean_division(42, 4)
assert q == 10
assert r == 2
