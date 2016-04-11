import collections

class Release:

    def __init__(self, name, duedate):
        self.name = name
        self.duedate = duedate
        self.features = []
        self.total = 0
        self.statuses = {
            "Backlog"    : 0,
            "Blocked"    : 0,
            "Scoping"    : 0,
            "Developing" : 0,
            "Testing"    : 0,
            "Released"   : 0
        }

        self.status_counts = collections.OrderedDict(sorted(self.statuses.items()))

    def __str__(self):
        text = '%s\n' %(self.name)

        for status in self.status_counts:
            text = text + "%s : %d\n" %(status, self.status_counts[status])

        text = text + "Total : %d\n\n" %(self.features.__len__())

        return text

    def add_feature(self, feature):
        if feature.status in self.status_counts:
            self.features.append(feature)
            self.status_counts[feature.status] += 1
            self.total = len(self.features)


        #print("> added status %s (%s) of %d count to %s" %(feature.status, feature.name, self.status_counts[feature.status], self.name))
