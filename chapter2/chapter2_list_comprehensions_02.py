from random import randint, seed

seed(10)  # Set random seed to make examples reproducible
random_elements = [randint(1, 10) for i in range(5)]
print(random_elements)  # [10, 1, 7, 8, 10]
