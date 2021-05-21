def euclidean_division(dividend, divisor):
    quotient = dividend // divisor
    remainder = dividend % divisor
    return (quotient, remainder)


t = euclidean_division(3, 2)
print(t[0])  # 1
print(t[1])  # 1

q, r = euclidean_division(42, 4)
print(q)  # 10
print(r)  # 2
