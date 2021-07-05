from sklearn.datasets import load_digits
from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import GaussianNB

digits = load_digits()

data = digits.data
targets = digits.target

# Create the model
model = GaussianNB()

# Run cross-validation
score = cross_val_score(model, data, targets)

print(score)
print(score.mean())
