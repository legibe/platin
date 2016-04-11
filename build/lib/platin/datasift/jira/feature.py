class Feature(object):

    def __init__(self, name, status):
        self.name = name
        self.status = status

    def __str__(self):
        text = '%s %s' %(self.name, self.status)
        return text