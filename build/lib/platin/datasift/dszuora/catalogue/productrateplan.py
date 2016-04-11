from platin.core.date import Date
from zuoraobject import ZuoraObject

class ProductRatePlan(ZuoraObject):
    class_name = 'ProductRatePlan'
    
if __name__=="__main__":
    from product import Product
    from zuora.client import Zuora
    client = Zuora()
    p = Product('Auto - test')
    p.create(client)
    pr = ProductRatePlan('Product Rate 1',ProductId=p.id())
    pr.create(client)
