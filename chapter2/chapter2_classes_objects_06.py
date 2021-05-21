class A:
    def f(self):
        return "A"


class Child(A):
    pass


c = Child()
print(c.f())  # "A"
