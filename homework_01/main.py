import os
import json


# Commands
ADD = "add"
HELP = "help"
SHOW_ALL = "all"
FIND_CONTACT = "find"
EDIT_CONTACT = "edit"
DELETE_CONTACT = "delete"
SAVE = "save"
SHOW_STORAGE = "show_storage"
EXIT = "exit"

STORAGE = "phonebook.json"

# Common messages
NOT_FOUND_MESSAGE = "Contact with ID {contact_id} not found"


def input_required(field_name):
    """Input for required fields. Prints error hint if field is empty."""
    value = input(f"{field_name} (required): ")
    if not value:
        print(f"{field_name} is required")
    return value


def input_integer(field_name):
    """Input for integer fields. Prints error hint if field is empty."""
    value = input(f"{field_name}: ")
    if not value.isdigit():
        print(f"Incorrect {field_name}. It must be an integer.")
        return
    return int(value)


def get_next_id():
    """Returns next contact id or 1 if there are no contacts."""
    if not contacts_buffer:
        return 1
    return int(max(contacts_buffer.keys())) + 1


def print_help():
    """Prints help."""
    help_hint = f"""
    Commands:
    - '{ADD}' - add contact;
    - '{FIND_CONTACT}' - find contact;
    - '{SHOW_ALL}' - show all contacts;
    - '{EDIT_CONTACT}' - edit contact;
    - '{DELETE_CONTACT}' - delete contact;
    - '{SAVE}' - save changes to file;
    - '{SHOW_STORAGE}' - show raw storage;
    - '{HELP}' - get help;
    - '{EXIT}' - exit; 
    """
    print(help_hint)


def show_storage():
    with open(STORAGE, 'r') as file:
        raw_data = json.load(file)
        print(raw_data)


def add_contact(name, phone, comment=None):
    """Add contact to phonebook."""
    contact_id = get_next_id()
    values = {
        "name": name,
        "phone": phone,
        "comment": comment,
    }
    contacts_buffer[contact_id] = values
    return contact_id, name, phone, comment


def find_contact(search):
    """Try to find contact using search string."""
    search_result = {}
    for contact_id, row in contacts_buffer.items():
        for value in row.values():
            if search in value:
                search_result[contact_id] = row
                break
    return search_result


def edit_contact(contact_id):
    """Update contact via its ID."""
    contact = contacts_buffer.get(contact_id)
    if not contact:
        return

    prompt = "New {field} (keep empty if do not want to change it): "
    new_name = input(prompt.format(field="name"))
    new_phone = input(prompt.format(field="phone"))
    new_comment = input(prompt.format(field="comment"))

    if new_name and new_name != contact["name"]:
        contact["name"] = new_name
    if new_phone and new_phone != contact["phone"]:
        contact["phone"] = new_phone
    if new_comment and new_comment != contact["comment"]:
        contact["comment"] = new_comment

    return contact

def delete_contact(contact_id):
    """Delete contact via its ID if exists."""
    if contact_id not in contacts_buffer:
        return

    return contacts_buffer.pop(contact_id)


def print_contacts(contacts):
    """Pretty print for contacts info"""
    for contact_id, row in contacts.items():
        values = [row["name"], row["phone"]]
        comment = row["comment"]
        if comment:
            values.append(comment)

        print(f"ID: {contact_id}.", " ".join(values))


def buffer_data_changed():
    """Returns True if there is diff between buffer and storage"""
    with open(STORAGE, 'r') as storage:
        storage_values = json.load(storage)

    storage_ids = list(map(int, storage_values.keys()))
    buffer_keys = list(contacts_buffer.keys())
    if sorted(storage_ids) != sorted(buffer_keys):
        return True

    for contact_id, buffer_value in contacts_buffer.items():
        contact_id = str(contact_id)
        if any((
            buffer_value["name"] != storage_values[contact_id]["name"],
            buffer_value["phone"] != storage_values[contact_id]["phone"],
            buffer_value["comment"] != storage_values[contact_id]["comment"],
        )):
            return True

    return False


def save_changes():
    """Save changes to from buffer to storage."""
    with open(STORAGE, 'w') as storage:
        json.dump(contacts_buffer, storage)

contacts_buffer = {}
if os.path.isfile(STORAGE):
    with open(STORAGE, 'r') as storage:
        contacts_buffer = json.load(storage)
else:
    with open(STORAGE, 'w') as storage:
        json.dump({}, storage)


command = None


# Main cycle
while command != EXIT:
    command = input(f"Enter command or type '{HELP}' to get help: ")

    if command == HELP:
        print_help()
    elif command == ADD:
        name = input_required("Name")
        if not name:
            continue

        phone = input_required("Phone")
        if not phone:
            continue

        comment = input("Comment (optional): ")

        contact_id, *_ = add_contact(name, phone, comment)
        print("Contact added: " + f"{contact_id}. " + " ".join((name, phone, comment)))
    elif command == SHOW_ALL:
        print_contacts(contacts_buffer)
    elif command == FIND_CONTACT:
        search = input_required("Search")
        found_contacts = find_contact(search)
        print_contacts(found_contacts)
    elif command == EDIT_CONTACT:
        contact_id = input_integer("Contact ID")
        if contact_id is None:
            continue

        updated_contact = edit_contact(contact_id)
        if updated_contact is None:
            print(NOT_FOUND_MESSAGE.format(contact_id=contact_id))
    elif command == DELETE_CONTACT:
        contact_id = input_integer("Contact ID")
        if contact_id is None:
            continue

        deleted_contact = delete_contact(contact_id)
        if not deleted_contact:
            print(NOT_FOUND_MESSAGE.format(contact_id=contact_id))
    elif command == SAVE:
        save_changes()
    elif command == SHOW_STORAGE:
        show_storage()


# Save changes to storage if needed
YES = "y"
NO = "n"
DEFAULT = YES

if buffer_data_changed():
    save = input(f"Save changes [{YES}/{NO}] (Default: {DEFAULT})? ") or DEFAULT
    if save == YES:
        save_changes()
