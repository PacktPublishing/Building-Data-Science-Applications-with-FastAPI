def even_numbers(max):
    for i in range(2, max + 1):
        if i % 2 == 0:
            yield i


even = list(even_numbers(10))
print(even)  # [2, 4, 6, 8, 10]
