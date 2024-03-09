from collections import UserDict, defaultdict
from datetime import datetime
import json


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
            super().__init__(value)
        except ValueError:
            raise ValueError("Incorrect date format, should be DD.MM.YYYY")


class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be 10 digits.")
        super().__init__(value)


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = filter(lambda p: p.value != phone, self.phones)

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                return
        raise ValueError("Phone not found.")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        return f"Contact name: {self.name}, phones: {'; '.join(str(p) for p in self.phones)}, birthday: {self.birthday}"


FILE_NAME = 'address-book.json'


class AddressBook(UserDict):
    def __init__(self):
        self.data = {}

    def save_to_file(self):
        data_to_save = {}
        for name, record in self.data.items():
            record_data = {
                "name": record.name.value,
                "phones": [phone.value for phone in record.phones],
                "birthday": record.birthday.value if record.birthday else None
            }
            data_to_save[name] = record_data

        with open(FILE_NAME, 'w') as file:
            json.dump(data_to_save, file, indent=4)

    def load_from_file(self):
        with open(FILE_NAME, 'r') as file:
            loaded_data = json.load(file)

        for name, record_data in loaded_data.items():
            record = Record(name)
            for phone in record_data["phones"]:
                record.add_phone(phone)
            if record_data["birthday"]:
                record.add_birthday(record_data["birthday"])
            self.add_record(record)

    def add_record(self, record: Record):
        self.data[record.name.value] = record
        self.save_to_file()

    def change_phone(self, name, old_phone, new_phone):
        if name not in self.data:
            raise KeyError
        self.data[name].edit_phone(old_phone, new_phone)
        self.save_to_file()

    def find(self, name):
        contact = self.data[name]
        if contact:
            return contact
        else:
            raise KeyError

    def all(self):
        return self.data

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            self.save_to_file()
        else:
            raise ValueError("Record not found.")

    def get_birthdays_per_week(self):
        birthdays = defaultdict(list)
        today = datetime.today().date()

        for name, record in self.data.items():
            if record.birthday and record.birthday.value:
                try:
                    birthday_date = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
                    birthday_this_year = birthday_date.replace(year=today.year)

                    if birthday_this_year < today:
                        birthday_this_year = birthday_this_year.replace(year=today.year + 1)

                    delta_days = (birthday_this_year - today).days
                    if 0 <= delta_days <= 7:
                        day_of_week = birthday_this_year.strftime('%A')

                        if day_of_week in ["Saturday", "Sunday"]:
                            day_of_week = "Monday"
                        birthdays[day_of_week].append(record.name.value)

                except ValueError:
                    print(f"Incorrect birthday format for {name}")
        result = []
        for day, names in birthdays.items():
            result.append(f"{day}: {', '.join(names)}")
        return result


if __name__ == "__main__":
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    book.delete("Jane")
