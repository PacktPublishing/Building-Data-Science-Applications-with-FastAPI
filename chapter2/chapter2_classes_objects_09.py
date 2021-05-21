class A:
    def f(self):
        return "A"


class B:
    def f(self):
        return "B"


class Child(A, B):
    pass


c = Child()
print(c.f())  # "A"
