from random import randint, seed

seed(10)  # Set random seed to make examples reproducible
random_unique_elements = {randint(1, 10) for i in range(5)}
print(random_unique_elements)  # {8, 1, 10, 7}
