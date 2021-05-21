numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
even = []

for number in numbers:
    if number % 2 == 0:
        even.append(number)

print(even)  # [2, 4, 6, 8, 10]
