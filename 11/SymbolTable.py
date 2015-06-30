from sys import exit

class SymbolTable:

    def __init__(self):
        self.table = dict()
        self.subEntrys = set()

        self.staticCounter = 0
        self.fieldCounter = 0
        self.argumentCounter = 0
        self.localCounter = 0

    def startSubroutine(self):
        for item in self.subEntrys:
            self.table.pop(item)
        self.subCounter = 0

    def define(self, name, type, kind):
        """
        Defines a new identifier of a given name, type and kind and assigns it a running index.
        STATIC and FIELD identifiers have a class scope, while ARG and VAR identifiers have a subroutine scope
        """

        if kind is "FIELD":
            index = self.fieldCounter
            self.fieldCounter += 1
        elif kind is "STATIC":
            index = self.staticCounter
            self.staticCounter += 1
        elif kind is "ARG":
            index = self.argumentCounter
            self.argumentCounter += 1
            self.subEntrys.add(name)
        elif kind is "VAR":
            index = self.localCounter
            self.localCounter += 1
            self.subEntrys.add(name)
        else:
            print("Error: unknown kind of variable tried to place in the symbol-table: {}".format(name))
            exit(-1)

        self.table[name] = (type, kind, index)

    def varCount(self, k):
        return len(entry for (type, kind, index) in table if kind is k)

    def kindOf(self, name):
        (type, kind, index) = self.table[name]
        return kind

    def typeOf(self, name):
        (type, kind, index) = self.table[name]
        return type

    def indexOf(self, name):
        (type, kind, index) = self.table[name]
        return index

    def getTripel(self, name):
        return self.table[name]