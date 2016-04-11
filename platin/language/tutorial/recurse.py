from directive import Directive

class Partner(Directive):
    pass

c = Partner(
    surname = "Poquelin",
    firstname = "Jean-Baptiste",
    gender = "male",
    age = 12,
    partner = Partner(
        surname = "Moliere",
        gender = 'male',
        age = 14,
        partner = Partner(
            surname = "The Man",
            gender = 'male',
            age = 16,
        )
    )
)
print c
