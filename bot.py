from abc import ABC, abstractmethod
from collections import UserDict
import os
import pickle


class Command(ABC):
    @abstractmethod
    def execute(self):
        pass


class AddCommand(Command):
    def __init__(self, address_book, name, phone):
        self.address_book = address_book
        self.name = name
        self.phone = phone

    def execute(self):
        self.address_book.add_record(self.name, self.phone)
        return f"Contact {self.name} with phone {self.phone} saved"


class ExitCommand(Command):
    def execute(self):
        return "Good bye"


class EnterCommand(Command):
    def execute(self):
        return "How can I help you?"


class ChangePhoneCommand(Command):
    def __init__(self, address_book, name, phone):
        self.address_book = address_book
        self.name = name
        self.phone = phone

    def execute(self):
        self.address_book.change_phone(self.name, self.phone)
        return f"Phone number for contact {self.name} has been updated to {self.phone}."


class GetPhoneCommand(Command):
    def __init__(self, address_book, name):
        self.address_book = address_book
        self.name = name

    def execute(self):
        return f"The phone number for contact {self.name} is {self.address_book.get_phone(self.name)}"


class ShowAllContactsCommand(Command):
    def __init__(self, address_book):
        self.address_book = address_book

    def execute(self):
        return self.address_book.show_all_contacts()


class AddressBook(UserDict):
    def __init__(self, file):
        super().__init__()
        self.file = file
        self.load()

    def dump(self):
        with open(self.file, 'wb') as file:
            pickle.dump((self.data, self.last_record_id, self.records), file)

    def load(self):
        if not os.path.exists(self.file):
            self.data = {}
            self.last_record_id = 0
            self.records = []
        else:
            with open(self.file, 'rb') as file:
                self.data, self.last_record_id, self.records = pickle.load(file)

    def add_record(self, name, phone):
        name = name.title()
        self[name] = phone

    def change_phone(self, name, phone):
        name = name.title()
        if name in self:
            self[name] = phone
        else:
            raise KeyError("Contact not found. Please enter a valid name.")

    def get_phone(self, name):
        name = name.title()
        if name in self:
            return self[name]
        else:
            raise KeyError("Contact not found. Please enter a valid name.")

    def show_all_contacts(self):
        if not self:
            return "No contacts found."
        result = "Addressbook:\n"
        for name, phone in self.items():
            result += f"{name}: {phone}\n"
        return result


def main():
    file_path = "addressbook.pickle"

    address_book = AddressBook(file_path)
    commands = {
        "add": AddCommand,
        "good bye": ExitCommand,
        "close": ExitCommand,
        "exit": ExitCommand,
        "hello": EnterCommand,
        "change": ChangePhoneCommand,
        "show": ShowAllContactsCommand,
        "show all": ShowAllContactsCommand,
        "show all contacts": ShowAllContactsCommand,
        "get": GetPhoneCommand,
        "get phone": GetPhoneCommand,
    }

    while True:
        user_input = input(">>> ")
        if not user_input:
            continue
        elements = user_input.split()
        command_key = elements[0].lower()
        if command_key in commands:
            command_cls = commands[command_key]
            args = elements[1:]
            command = command_cls(address_book, *args)
            result = command.execute()
            print(result)
            if isinstance(command, ExitCommand):
                break
        else:
            print("Invalid command. Please try again.")


if __name__ == "__main__":
    main()
