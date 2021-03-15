class A:
    def f(self):
        return "A"


class B:
    def g(self):
        return "B"


class Child(A, B):
    pass


c = Child()
assert c.f() == "A"
assert c.g() == "B"
