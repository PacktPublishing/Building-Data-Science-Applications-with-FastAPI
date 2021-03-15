class Temperature:
    def __init__(self, value, scale):
        self.value = value
        self.scale = scale

    def __repr__(self):
        return f"Temperature({self.value}, {self.scale!r})"

    def __str__(self):
        return f"Temperature is {self.value} °{self.scale}"


t = Temperature(25, "C")
assert repr(t) == "Temperature(25, 'C')"
assert str(t) == "Temperature is 25 °C"
print(t)
