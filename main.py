from database_manager import DatabaseManager
import re

#TODO:
#1. Fix crash when empty database
#2. Add docstrings
#3. Make tests

database_manager = DatabaseManager()

current_page: int = 0
records: list
alphabetical_sort: bool = False

def print_entry(entry_num: int ,entry: list):
     print(str(entry_num) + ".  " + entry[0] + "    " + entry[1] + "    " + entry[2] + "    " + entry[3])

def has_next_page(page_num: int, records: list) -> bool:
    if len(records) > (page_num + 1) * 10:
        return True
    return False

def print_entries_menu(page_num: int, records: list):
    current_entry_in_page = 0
    while True:
        current_entry: int = page_num * 10 + current_entry_in_page
        current_page_record: list = records[current_entry]
        
        print_entry(current_entry_in_page, current_page_record)
        
        if (len(records) - 1) != current_entry and current_entry_in_page < 9:
            current_entry_in_page += 1
        else:
            break
    print()
    if page_num != 0:
        print("p. Previous page.")
    if has_next_page(page_num, records):
        print("n. Next page.")

def records_menu(page_num: int, records: list) -> str:
    print("===RECORDS===")
    print()
    print()
    print("""   NAME    PHONE NUMBER    EMAIL   NOTES""")
    print_entries_menu(page_num, records)
    print('Commands: "SEARCH", "SORT", "NEW"')
    return(input())

def search_menu(records: list):
    entries_list: list = []
    while True:
        print("===SEARCH===")
        print()
        user_input = input("Search for the desired contact's name: ")
        for entry in records:
            if user_input.casefold() in entry[0].casefold():
                entries_list.append(entry)
        if not entries_list:
            print("No such entry found.")
        else:
            return entries_list

def sort_menu():
    while True:
        print("===SORT OPTIONS===")
        print()
        print("0. Sort by order of entry creation.")
        print("1. Sort alphabetically.")
        user_input = input()
        if user_input == "0":
            return False
        elif user_input == "1":
            return True
        else:
            print("INVALID INPUT.")

def name_entry_input():
    user_input = input("Name: ")
    return user_input

def notes_entry_input():
    user_input = input("Notes: ")
    return user_input

def number_entry_input():
    while True:
        user_input = input("Number: ")
        try:
            int(user_input)
        except :
            print("Invalid number.")
        else:
            if len(user_input) > 15:
                print("Number too long")
            else:
                return user_input

def email_entry_input():
    pattern = r"^\S+@\S+\.\S+$"
    while True:
        user_input = input("Email: ")
        if not re.fullmatch(pattern, user_input):
            print("Invalid Email.")
        else:
            return user_input

def entry_creation_menu(): #probably broken?
    print("===NEW ENTRY===")
    entry: list = []
    entry.append(name_entry_input())
    entry.append(number_entry_input())
    entry.append(email_entry_input())
    entry.append(notes_entry_input())
    records = database_manager.get_all_records()
    records.append(entry)
    database_manager.write_to_database(records)
   
def confirmation() -> bool:
    print("Are you sure you want to proceed with this action?")
    print()
    print("0. Yes")
    print("1. No")
    user_input = input()
    try:
        int(user_input)
    except:
        print("INVALID INPUT. RETURNING.")
        return False
    else:
        if int(user_input) == 0:
            return True
        elif int(user_input) == 1:
            return False
        else:
            print("INVALID INPUT. RETURNING.")
            return False

def selected_entry_menu(entry: list):
    print(entry)
    print()
    print("0. Back")
    print("1. Delete entry")
    print("2. Edit name")
    print("3. Edit number")
    print("4. Edit email")
    print("5. Edit notes")
    user_input = input()
    try:
        int(user_input)
    except :
        print("INVALID INPUT.")
    else:
        user_input = int(user_input)
        if user_input == 0:
            return
        elif user_input > 5:
            print("INVALID INPUT.")
        else:
            edited_entry: list = entry.copy()
            if user_input == 1: #Back
                if confirmation():
                    database_manager.delete_entry(entry)
            else:
                if user_input == 2: #Edit name
                    edited_entry[0] = name_entry_input()
                elif user_input == 3: #Edit number
                    edited_entry[1] = number_entry_input()
                elif user_input == 4: #Edit email
                    edited_entry[2] = email_entry_input()
                elif user_input == 5: 
                    edited_entry[3] = notes_entry_input()
                if confirmation():
                    database_manager.replace_entry(entry, edited_entry)

def invalid_input():
    print("INVALID INPUT.")
    return database_manager.get_all_records()

#Runtime:
records = database_manager.get_all_records()
while True:
    if alphabetical_sort:
        records.sort()
    user_input: str = records_menu(current_page, records)
    try:
        int(user_input)
    except:
        user_input = user_input.casefold()
        if user_input == "p":
            current_page -= 1
            records = database_manager.get_all_records()
        elif user_input == "n" and has_next_page(current_page, records):
            current_page += 1
            records = database_manager.get_all_records()
        elif user_input == "SEARCH".casefold():
            records = search_menu(records)
        elif user_input == "SORT".casefold():
            alphabetical_sort = sort_menu()
            records = database_manager.get_all_records()
        elif user_input == "NEW".casefold():
            entry_creation_menu()
            records = database_manager.get_all_records()
        else:
            records = invalid_input()
    else:
        user_input_int = int(user_input)
        if user_input_int <= 9 and current_page + user_input_int <= (len(records) - 1):
            selected_entry_menu(records[current_page * 10 + user_input_int])
            records = database_manager.get_all_records()
        else:
            records = invalid_input()