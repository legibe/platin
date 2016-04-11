from directive import Directive

class Client(Directive):
    pass

c = Client(
    surname = "Poquelin",
    firstname = "Jean-Baptiste",
    gender = "not sure",
    age = 12
)
print c
