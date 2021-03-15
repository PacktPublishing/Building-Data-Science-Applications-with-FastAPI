class Counter:
    def __init__(self):
        self.counter = 0

    def __call__(self, inc=1):
        self.counter += inc


c = Counter()
assert c.counter == 0
c()
assert c.counter == 1
c(10)
assert c.counter == 11
