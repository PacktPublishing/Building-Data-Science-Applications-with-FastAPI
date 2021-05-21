class A:
    def f(self):
        return "A"


class Child(A):
    def f(self):
        parent_result = super().f()
        return f"Child {parent_result}"


c = Child()
print(c.f())  # "Child A"
