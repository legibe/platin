from directive import Directive

class Desk(Directive):
    pass

class Office(Directive):
    pass

c = Office(
    location = "Reading",
    desk = [
        Desk(
            owner = "Claude",
            location = 102,
            colour = "blue"
        ),
        Desk(
            owner = "John",
            location = 189,
        ),
        Desk(
            owner = "Jim",
            location = 123,
            colour = "red"
        ),
    ]
)
print c
print
