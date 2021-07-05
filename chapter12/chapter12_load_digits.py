from sklearn.datasets import load_digits

digits = load_digits()

data = digits.data
targets = digits.target

print(data[0].reshape((8, 8)))  # First handwritten digit 8 x 8 matrix
print(targets[0])  # Label of first handwritten digit
