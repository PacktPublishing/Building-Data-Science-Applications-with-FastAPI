class Greetings:
    def greet(self, name):
        return f"Hello, {name}"


c = Greetings()
assert c.greet("John") == "Hello, John"
