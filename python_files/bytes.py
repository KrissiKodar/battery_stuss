

class P:
    def __init__(self, x):
        # wait for Arduino to be ready
        self.x = x

    def f(self):
        return self.x


parent = P(100)

# make child class C that inherits the specific instance of P (parent)
class C(P):
    def __init__(self, parent_instance):
        self.x = parent_instance.x + 1
        
child_test = C(200)

print(child_test.x)