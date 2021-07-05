from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB

digits = load_digits()

data = digits.data
targets = digits.target

# Split into training and testing sets
training_data, testing_data, training_targets, testing_targets = train_test_split(
    data, targets, random_state=0
)

# Train the model
model = GaussianNB()
model.fit(training_data, training_targets)

# Print mean and standard deviation of digit zero
print("Mean of each pixel for digit zero")
print(model.theta_[0])

print("Standard deviation of each pixel for digit zero")
print(model.sigma_[0])
