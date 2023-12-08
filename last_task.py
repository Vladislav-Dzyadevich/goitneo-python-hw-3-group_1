from datetime import datetime, timedelta

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Invalid command format."

    return inner 
  
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Birthday(Field):
    def __init__(self, value):
        self.value = self.validate(value)

    def validate(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
            return value
        except ValueError:
            raise ValueError("Invalid date format. Please use DD.MM.YYYY.")

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Invalid phone number format. Must be 10 digits.")
        super().__init__(value)

class Record:
    def __init__(self, name, phone=None, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

        if phone:
            self.add_phone(phone)

        if birthday:
            self.add_birthday(birthday)

    def add_birthday(self, date):
        if not self.birthday:
            self.birthday = Birthday(date)
        else:
            raise ValueError("Birthday already set.")

    def show_birthday(self):
        return f"Birthday: {self.birthday}" if self.birthday else "No birthday set."

    def add_phone(self, phone):
        try:
            phone_obj = Phone(phone)
            self.phones.append(phone_obj)
            return f"Phone {phone_obj} added."
        except ValueError as e:
            return str(e)

    def remove_phone(self, phone):
        for phone_obj in self.phones:
            if phone_obj.value == phone:
                self.phones.remove(phone_obj)
                return f"Phone {phone} removed."
        return f"Phone {phone} not found."

    def edit_phone(self, old_phone, new_phone):
        for i, phone_obj in enumerate(self.phones):
            if phone_obj.value == old_phone:
                try:
                    new_phone_obj = Phone(new_phone)
                    self.phones[i] = new_phone_obj
                    return f"Phone {old_phone} edited to {new_phone}."
                except ValueError as e:
                    return str(e)
        return f"Phone {old_phone} not found."

    def find_phone(self, phone):
        for phone_obj in self.phones:
            if phone_obj.value == phone:
                return phone_obj
        return None

    def __str__(self):
        phones_str = "; ".join(str(phone) for phone in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones_str}{self.show_birthday()}"

class AddressBook:
    def __init__(self):
        self.data = {}

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return f"Contact {name} deleted."
        return f"Contact {name} not found."
    
    def get_birthdays_per_week(self):
        today = datetime.now()
        next_week_start = today + timedelta(days=(6 - today.weekday()) + 7)
        next_week_end = next_week_start + timedelta(days=6)
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday:
                birthday_date = datetime.strptime(record.birthday.value, "%d.%m.%Y")
                if next_week_start <= birthday_date <= next_week_end:
                    upcoming_birthdays.append((record.name.value, record.birthday.value))

        return upcoming_birthdays

@input_error
def add_contact(args, book):
    if len(args) == 2:
        name, phone = args
        record = Record(name, phone)
        book.add_record(record)
        return "Contact added."
    else:
        raise ValueError("Give me name and phone please.")

@input_error
def change_contact(args, book):
    if len(args) == 2:
        name, new_phone = args
        contact = book.find(name)
        if contact:
            contact.phones[0] = Phone(new_phone)
            return "Contact updated."
        else:
            raise KeyError
    else:
        raise IndexError

@input_error
def show_phone(args, book):
    if len(args) == 1:
        name = args[0]
        contact = book.find(name)
        if contact and contact.phones:
            return contact.phones[0].value
        else:
            raise KeyError
    else:
        raise ValueError("Enter the contact name.")

@input_error
def show_all(book):
    if book.data:
        result = ""
        for record in book.data.values():
            result += str(record) + "\n"
        return result.rstrip()
    else:
        return "No contacts available."

@input_error
def add_birthday(args, book):
    if len(args) == 2:
        name, date = args
        contact = book.find(name)
        if contact:
            try:
                contact.add_birthday(date)
                return f"Birthday added for {name}."
            except ValueError as e:
                return str(e)
        else:
            return f"Contact {name} not found."
    else:
        return "Invalid command format. Use 'add_birthday [name] [DD.MM.YYYY]'."

@input_error
def show_birthday(args, book):
    name, = args
    contact = book.find(name)
    if contact:
        return contact.show_birthday()
    else:
        return f"Contact {name} not found."

@input_error
def birthdays(book):
    upcoming_birthdays = book.get_birthdays_per_week()
    if upcoming_birthdays:
        return "\n".join([f"{name}: {date}" for name, date in upcoming_birthdays])
    else:
        return "No upcoming birthdays in the next week."

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Goodbye!")
            break

        if command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all(book))

        elif command == "add_birthday":
            print(add_birthday(args, book))

        elif command == "show_birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(book))

        else:
            print("Invalid command.")

if __name__ == "__main__":
    book = AddressBook()
    main()
