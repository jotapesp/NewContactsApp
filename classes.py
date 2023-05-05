from functools import total_ordering

class UniqueList:
    def __init__(self, elem_class):
        self.lista = []
        self.elem_class = elem_class

    def __len__(self):
        return len(self.lista)

    def __iter__(self):
        return iter(self.lista)

    def __getitem__(self, p):
        return self.lista[p]

    def validIndex(self, i):
        return i >= 0 and i < len(self.lista)

    def addElem(self, elem):
        if self.searchElem(elem) == -1:
            self.lista.append(elem)

    def removeElem(self, elem):
        self.lista.remove(elem)

    def searchElem(self, elem):
        self.verifyType(elem)
        try:
            return self.lista.index(elem)
        except ValueError:
            return -1

    def verifyType(self, elem):
        if not isinstance(elem, self.elem_class):
            raise TypeError("Invalid type")

    def order(self, key=None):
        self.lista.sort(key=key)

@total_ordering
class Name:
    def __init__(self, name):
        self.name = name
        # self.key = Name.CreateKey(name)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Class {type(self).__name__} at 0x{id(self):x} Name: {self.__name} Key: {self.__key}>"

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        return self.name < other.name

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if value is None or not value.strip():
            raise ValueError("Name can't be blank or None")
        self.__name = value
        self.__key = Name.CreateKey(value)

    @property
    def key(self):
        return self.__key

    @staticmethod
    def CreateKey(name):
        return name.strip().lower()

@total_ordering
class TelephoneType:
    def __init__(self, type):
        self.type = type

    def __str__(self):
        return f"({self.tipo })"

    def __eq__(self, other):
        if other is None:
            return False
        return self.type == other.type

    def __lt__(self, other):
        return self.type < other.type

@total_ordering
class TelephoneType:
    def __init__(self, type):
        self.type = type

    def __str__(self):
        return f"({self.type })"

    def __eq__(self, other):
        if other is None:
            return False
        return self.type == other.type

    def __lt__(self, other):
        return self.type < other.type

class Telephone:
    def __init__(self, number, type=None):
        self.number = number
        self.type = type

    def __str__(self):
        if self.type is not None:
            type = self.type
        else:
            type = ""

        return f"{self.number} {type}"

    def __eq__(self, other):
        return self.number == other.number and (
                (self.type == other.type) or (
                self.type is None or other.type is None))

    @property
    def number(self):
        return self.__number

    @number.setter
    def number(self, value):
        if value is None or not value.strip():
            raise ValueError("Number can't be None or blank")
        self.__number = value

class Telephones(UniqueList):
    def __init__(self):
        super().__init__(Telephone)

class ContactData:
    def __init__(self, name):
        self.name = name
        self.telephones = Telephones()
    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self, value):
        if not isinstance(value, Name):
            raise TypeError("name should be a Name class instance")
        self.__name = value
    def searchTelephone(self, telephone):
        position = self.telephones.searchElem(Telephone(telephone))
        if position == -1:
            return None
        else:
            return self.telephones[position]

class TelephoneTypes(UniqueList):
    def __init__(self):
        super().__init__(TelephoneType)

class Contacts(UniqueList):
    def __init__(self):
        super().__init__(ContactData)
        self.telephoneTypes = TelephoneTypes()
    def addType(self, type):
        self.telephoneTypes.addElem(TelephoneType(type))
    def searchName(self, name):
        if isinstance(name, str):
            name = Name(name)
        for data in self.lista:
            if data.name == name:
                return data

        else:
            return None
    def order(self):
        super().order(lambda data: str(data.name))
