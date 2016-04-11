import logging
from platin.core.date import Date
from zuoraobject import ZuoraObject
from productrateplanchargetier import ProductRateChargeTier

#logging.basicConfig(level=logging.INFO)
#logging.getLogger('suds.client').setLevel(logging.DEBUG)
#logging.getLogger('suds.transport').setLevel(logging.DEBUG)
#logging.getLogger('suds.xsd.schema').setLevel(logging.DEBUG)

class OveragePricing(ZuoraObject):
    class_name = 'ProductRatePlanCharge'

    def __init__(self,name,*args,**kwargs):
        if not 'ChargeModel' in kwargs:
            kwargs['ChargeModel'] = 'Overage Pricing'
        self._tiers = args
        super(OveragePricing,self).__init__(name,**kwargs)

    def create(self,client):
        p = super(OveragePricing,self).create(client)
        for tier in self._tiers:
            charge = ProductRateChargeTier(None,IsOveragePrice = True,PriceFormat = 'PerUnit',**tier)
            p.ProductRatePlanChargeTierData.ProductRatePlanChargeTier.append(charge.create(client))

if __name__=="__main__":
    from product import Product
    from productrateplan import ProductRatePlan
    from zuora.client import Zuora
    client = Zuora()

    p = Product('Auto - test')
    p.createAndSend(client)
    pr = ProductRatePlan('Product Rate 1',id = p.id())
    pr.createAndSend(client)
    entries = [
        dict(price=0.0002,currency='USD'),
        dict(Price=0.0001,currency='EUR')
    ]
    ff = OveragePricing('sub',
        *entries,
        id=pr.id(),
        ChargeType="Usage",
        IncludedUnits=25000,
        UOM='Interaction')
    ff.createAndSend(client)
