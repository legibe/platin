from platin.core.date import Date
from zuoraobject import ZuoraObject

class Product(ZuoraObject):

    class_name = 'Product'

if __name__=="__main__":
    from zuora.client import Zuora
    client = Zuora()
    p = Product('Auto - test')
    p.create(client)
