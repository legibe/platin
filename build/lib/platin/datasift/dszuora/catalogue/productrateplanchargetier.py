from platin.core.date import Date
from zuoraobject import ZuoraObject

class ProductRateChargeTier(ZuoraObject):
    class_name = 'ProductRatePlanChargeTier'

    def create(self,client):
        self._object = self.validateObject(self._object)
        p = client.instanciate(self.class_name)
        for k,i in self._object.items():
            setattr(p,k,i)
        return p
