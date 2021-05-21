numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
even_generator = (number for number in numbers if number % 2 == 0)
even = list(even_generator)
even_bis = list(even_generator)

print(even)  # [2, 4, 6, 8, 10]
print(even_bis)  # []
