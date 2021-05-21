class Greetings:
    def __init__(self, default_name):
        self.default_name = default_name

    def greet(self, name=None):
        return f"Hello, {name if name else self.default_name}"


c = Greetings("Alan")
print(c.default_name)  # "Alan"
print(c.greet())  # "Hello, Alan"
print(c.greet("John"))  # "Hello, John"
