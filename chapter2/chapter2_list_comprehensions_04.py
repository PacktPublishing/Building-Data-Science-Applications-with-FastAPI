from random import randint, seed

seed(10)  # Set random seed to make examples reproducible
random_dictionary = {i: randint(1, 10) for i in range(5)}
print(random_dictionary)  # {0: 10, 1: 1, 2: 7, 3: 8, 4: 10}
