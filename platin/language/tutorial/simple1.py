from directive import Directive

"""
Simple example showing encapsulation, validation of keywords and default values
"""

class Client(Directive):
    pass

c = Client(
    surname = "Poquelin",
    age = 12
)
print c
print
c = Client(
    surname = "Poquelin",
    firstname = "Jean-Baptiste",
    gender = "male",
    age = "12"
)
print c
