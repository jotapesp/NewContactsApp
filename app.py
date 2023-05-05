from classes import *
from utilities import validate_integer_range, nul_or_blank, validate_integer_range_or_blank
import sys
import pickle

class Menu:
    def __init__(self):
        self.options = [["Exit", None]]
    def addOption(self, name, function):
        self.options.append([name, function])
    def show(self):
        print("====")
        print("Menu")
        print("====\n")
        for i, option in enumerate(self.options):
            print(f"[{i}] - {option[0]}")
        print()
    def execute(self):
        while True:
            self.show()
            choice = validate_integer_range("Choose an option: ", 0, len(self.options) - 1)
            if choice == 0:
                break
            self.options[choice][1]()

class AppContacts:
    @staticmethod
    def ask_name():
        return input('Name: ')
    @staticmethod
    def ask_telephone_number():
        return input('Telephone number: ')
    @staticmethod
    def show_data(data):
        print(f"Name: {data.name}")
        for telephone in data.telephones:
            print(f"Telephone: {telephone}")
        print()
    @staticmethod
    def show_data_telephone(data):
        print(f"Name: {data.name}")
        for i, telephone in enumerate(data.telephones):
            print(f"{i} - Telephone: {telephone}")
        print()
    @staticmethod
    def ask_file_name():
        return input("File name: ")
    def __init__(self):
        self.contacts = Contacts()
        self.contacts.addType("Mobile")
        self.contacts.addType("Landline")
        self.contacts.addType("Work")
        self.contacts.addType("Fax")
        self.menu = Menu()
        self.menu.addOption("New", self.new)
        self.menu.addOption("Edit", self.edit)
        self.menu.addOption("Erase", self.erase)
        self.menu.addOption("List", self.lista)
        self.menu.addOption("Save", self.save)
        self.menu.addOption("Read", self.read)
        self.menu.addOption("Sort", self.sort)
        self.last_name = None
    def ask_telephone_type(self, default=None):
        for i, type in enumerate(self.contacts.telephoneTypes):
            print(f" {i} - {type} ", end=None)
        t = validate_integer_range("Type: ", 0, len(self.contacts.telephoneTypes) - 1)
        return self.contacts.telephoneTypes[t]
    def searchContact(self, name):
        data = self.contacts.searchName(name)
        return data
    def new(self):
        new = AppContacts.ask_name()
        if nul_or_blank(new):
            return
        name = Name(new)
        if self.searchContact(name) is not None:
            print("Name already exists!")
            return
        registry = ContactData(name)
        self.menu_telephones(registry)
        self.contacts.addElem(registry)
    def erase(self):
        if len(self.contacts) == 0:
            print("Empty contacts list, nothing to erase.")
        name = AppContacts.ask_name()
        if nul_or_blank(name):
            return
        p = self.searchContact(name)
        if p is not None:
            self.contacts.removeElem(p)
            print(f"Erased. The contacts list has now only: {len(self.contacts)} entries")
        else:
            print("Name not found.")
    def edit(self):
        if len(self.contacts) == 0:
            print("Empty contacts list, nothing to edit.")
        name = AppContacts.ask_name()
        if nul_or_blank(name):
            return
        p = self.searchContact(name)
        if p is not None:
            print("\nFound:\n")
            AppContacts.show_data(p)
            print("Hit 'Enter'/'Return' key if you do not want to edit name information")
            new = AppContacts.ask_name()
            if not nul_or_blank(new):
                p.name = Name(new)
            self.menu_telephones(p)
        else:
            print("Name not found.")
    def menu_telephones(self, data):
        while True:
            print("\nEditing telephones\n")
            AppContacts.show_data_telephone(data)
            if len(data.telephones) > 0:
                print("\n[E] - edit\n[D] - delete\n", end="")
            print("\n[N] - new\n[Q] - quit\n")
            operation = input("Choose an option: ")
            operation = operation.lower()
            if operation not in ["e", "d", "n", "q"]:
                print("Invalid option. Enter E, D, N, or Q.")
                continue
            if operation == 'e' and len(data.telephones) > 0:
                self.edit_telephones(data)
            elif operation == 'd' and len(data.telephones) > 0:
                self.erase_telephone(data)
            elif operation == 'n':
                self.new_telephone(data)
            elif operation == 'q':
                break
    def new_telephone(self, data):
        telephone = AppContacts.ask_telephone_number()
        if nul_or_blank(telephone):
            return
        if data.searchTelephone(telephone) is not None:
            print("Telephone already exists")
        type = self.ask_telephone_type()
        data.telephones.addElem(Telephone(telephone, type))
    def erase_telephone(self, data):
        t = validate_integer_range_or_blank(
            "Enter the number position you want to edit, or hit 'Enter'/'Return' to quit: ",
            0, len(data.telephones) - 1)
        if t is None:
            return
        data.telephones.removeElem(data.telephones[t])
    def edit_telephones(self, data):
        t = validate_integer_range_or_blank(
            "Enter the number position you want to edit, or hit 'Enter'/'Return' to quit: ",
            0, len(data.telephones) - 1)
        if t is None:
            return
        telephone = data.telephones[t]
        print(f"Telephone: {telephone}")
        print(f"Press 'Enter'/'Return' in case you do not want to edit this number")
        newtelephone = AppContacts.ask_telephone_number()
        if not nul_or_blank(newtelephone):
            telephone.number = newtelephone
        print("Press 'Enter'/'Return' in case you do not want to edit the type")
        telephone.type = self.ask_telephone_type(
            self.contacts.telephoneTypes.searchElem(telephone.type))
    def lista(self):
        print("\nContacts List")
        print("-" * 60)
        for e in self.contacts:
            AppContacts.show_data(e)
        print("-" * 60)
    def read(self, file_name=None):
        if file_name is None:
            file_name = AppContacts.ask_file_name()
        if nul_or_blank(file_name):
            return
        with open(file_name, "rb") as file:
            self.contacts = pickle.load(file)
        self.last_name = file_name
    def sort(self):
        self.contacts.order()
        print("\nContacts list sorted\n")
    def save(self):
        if self.last_name is not None:
            print(f"Previous name was '{self.last_name}'")
            print("Press 'Enter'/'Return' in case you want to use the same name")
        file_name = AppContacts.ask_file_name()
        if nul_or_blank(file_name):
            if self.last_name is not None:
                file_name = self.last_name
            else:
                return
        with open(file_name, "wb") as file:
            pickle.dump(self.contacts, file)
    def execute(self):
        self.menu.execute()
if __name__ == "__main__":
    app = AppContacts()
    if len(sys.argv) > 1:
        app.read(sys.argv[1])
    app.execute()
