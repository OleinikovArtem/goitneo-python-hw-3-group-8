from utils import input_error, parse_input
from address_book import AddressBook, Record

book = AddressBook()


@input_error
def add_contact(args):
    name, phone = args
    contact = Record(name)
    contact.add_phone(phone)
    book.add_record(contact)

    return "Contact added."


@input_error
def change_contact(args):
    name, old_phone, new_phone = args
    book.change_phone(name, old_phone, new_phone)
    return "Contact updated."


@input_error
def show_phone(args):
    name = args[0]
    return book.find(name)


def show_all():
    contacts = book.all()
    if not contacts:
        return "No contacts found."
    return '\n'.join(f"{name}: {phone}" for name, phone in contacts.items())


@input_error
def add_birthday(args):
    name, birthday = args
    contact = book.find(name)
    contact.add_birthday(birthday)
    return f"Birthday for {name} added."


@input_error
def show_birthday(args):
    name = args[0]
    contact = book.find(name)
    return f"Birthday for {contact.name} is {contact.birthday}"


def show_birthdays():
    birthdays = book.get_birthdays_per_week()
    return birthdays


def main():
    print("Welcome to the assistant bot! Type 'exit' or 'close' to quit.")

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args))
        elif command == "change":
            print(change_contact(args))
        elif command == "phone":
            print(show_phone(args))
        elif command == "all":
            print(show_all())
        elif command == "add-birthday":
            print(add_birthday(args))
        elif command == "show-birthday":
            print(show_birthday(args))
        elif command == "birthdays":
            print(show_birthdays())
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
