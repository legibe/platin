from directive import Directive

class Rectangle(Directive):
    def draw(self):
        pass

class Circle(Directive):
    def draw(self):
        pass

r = Rectangle(
    x = 12,
    y = 25,
    width = 50,
    height = 80,
    colours = "blue"
)
print r
print

c = Circle(
    radius = 50,
    x = 23,
    y = 100,
)
print c
print

c = Circle(
    radius = 50,
    x = 23,
    y = 100,
    opacity = 70
)
print c
print
