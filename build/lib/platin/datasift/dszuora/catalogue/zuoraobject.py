import os
from platin.core.basic import classNameOf
from platin.core.date import Date
from platin.language.language import Language

"""
    Ancestor Object which does most of the work. To implement a specific Zuora object
    inherit from this class
"""
class ZuoraObject(object):

    schema_path = os.path.join(os.path.dirname(__file__),'schema')
    class_name = ''

    def __init__(self,name,**kwargs):
        self._object = {}
        if name is not None:
            self._object['Name'] = name
        for k,i in kwargs.items():
            self._object[k] = i

    def createAndSend(self,client):
        self.create(client)
        self.send(client)

    """
        Creates an SOAP object in memory
    """
    def create(self,client):
        self._object = self.validateObject(self._object)
        self._soap = client.instanciate('ns2:' + self.class_name)
        for k,i in self._object.items():
            setattr(self._soap,k,i)
        return self._soap

    """
        Calls the create method of the API with the SOAP object
    """
    def send(self,client):
        result = client.create(self._soap)
        if result[0]['Success']:
            self._id = result[0]['Id']
        else:
            raise IOError(result[0]['Errors'])

    """
        Returns the Id of the object which was just sent
    """
    def id(self):
        return self._id

    def validateObject(self,obj):
        language = Language(self.class_name.lower(),self.schema_path)
        return language.validate(obj)
