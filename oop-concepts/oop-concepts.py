class Person:

    def __init__(self, name):
        self.name = name

    def say_hello(self):
        print(id(self))
        print("Hello, " + self.name)

p1 = Person("Walter")
p2 = Person("Alex")
print(id(p1))
print(id(p2))
p1.say_hello()
