from collections import defaultdict


class Accumulator(defaultdict):
    def __init__(self, factory):
        super(Accumulator, self).__init__(factory)

    def add(self, name, value):
        self[name] += value
        return self[name]

    def store(self, name, value):
        self[name] = value
        return self[name]

    def get(self, name):
        return self[name]
