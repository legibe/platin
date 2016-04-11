from directive import Directive

class ShoppingList(Directive):
    pass

c = ShoppingList(
    company = "Ocado",
    when = "2015-12-25",
    items = [
        "potatoes",
        "carrots",
        "turnips",
        12
    ]
)
print c
print dict(c)

c = ShoppingList(
    company = "Ocado",
    when = "2015-12-25",
    items = "beef",
)
print c
print dict(c)
