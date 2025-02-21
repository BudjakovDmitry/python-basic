"""Phonebook models"""

import json
import os
from typing import Generator, List


class ContactNotFound(Exception):
    """Raises if contact with specified parameters not found."""
    def __init__(self, id_: int):
        self.id_ = id_

    def __str__(self):
        return f"Contact with ID={self.id_} not found"


class Contact:
    """Represents contact data and logic."""

    def __init__(self, id_: int, name: str, phone: str, comment: str | None = None):
        self.id = id_
        self.name = name
        self.phone = phone
        self.comment = comment

    def has(self, search: str) -> bool:
        """
        Returns True if contact contains substring
        :param search: search substring
        :return: True if one of contact's attributes contain search substring
                 False otherwise
        """
        for value in (self.name, self.phone, self.comment):
            if value is not None and search.lower() in value.lower():
                return True
        return False

    def update_name(self, new_name: str):
        """Update contact's name"""
        if new_name:
            self.name = new_name

    def update_phone(self, new_phone: str):
        """Update contact's phone"""
        if new_phone:
            self.phone = new_phone

    def update_comment(self, new_comment: str):
        if new_comment:
            self.comment = new_comment

    def clear_comment(self):
        """Clear contact's comment"""
        self.comment = None

    def as_dict(self):
        return self.__dict__


class JsonStorage:
    """Represents json-based file storage of the Phonebook."""

    STORAGE = "phonebook.json"

    def __init__(self):
        self._cache = {}

        # create file if needed or load data from existing file
        if os.path.isfile(self.STORAGE):
            with open(self.STORAGE, "r") as storage:
                for row in json.load(storage):
                    row["id_"] = row.pop("id")  # replace key "id_" to "id"
                    contact = Contact(**row)
                    self._cache[contact.id] = contact
        else:
            with open(self.STORAGE, "w") as storage:
                json.dump([], storage)

    def save(self):
        """Save contacts to the file storage."""
        with open(self.STORAGE, "w") as storage:
            json.dump([contact.as_dict() for contact in self._cache.values()], storage)

    def raw_storage(self) -> dict:
        """Returns raw storage data."""
        with open(self.STORAGE, "r") as file:
            return json.load(file)

    def add_to_cache(self, value: Contact):
        self._cache[value.id] = value


class PhonebookModel(JsonStorage):
    """Represents data and business logic of Phonebook."""

    def __init__(self):
        self._cache = {}
        super().__init__()

    def add_contact(self, name: str, phone: str, comment: str = None) -> Contact:
        """Add contact to phonebook."""
        contact_id = self._next_cache_id()

        contact = Contact(id_=contact_id, name=name, phone=phone, comment=comment)
        super().add_to_cache(contact)
        return contact

    def delete_contact(self, id_: int):
        """
        Delete contact from the phonebook.
        :param id_: contact ID
        """
        if id_ not in self._cache:
            return
        self._cache.pop(id_)

    def find_contacts(self, search: str) -> List[Contact]:
        """Returns contacts that satisfy search."""
        return [
            contact for contact in self._cache.values() if contact.has(search)
        ]

    def get(self, id_: int) -> Contact:
        """Return contact via its ID."""
        contact = self._cache.get(id_)
        if not contact:
            raise ContactNotFound(id_)
        return contact

    def contacts(self) -> Generator[Contact, None, None]:
        """Return contacts one by one."""
        for contact in self._cache.values():
            yield contact

    def _next_cache_id(self) -> int:
        """Returns next contact id or 1 if there are no contacts."""
        if not self._cache:
            return 1
        return int(max(self._cache.keys())) + 1

    def has_unsaved_changes(self) -> bool:
        """Returns True if there are unsaved changes in the cache."""
        storage_values = self.raw_storage()

        storage_ids = list(map(int, storage_values.keys()))
        cache_keys = list(self._cache.keys())
        if sorted(storage_ids) != sorted(cache_keys):
            return True

        for id_, contact in self._cache.items():
            contact_id = str(id_)
            if any((
                    contact.name != storage_values[contact_id]["name"],
                    contact.phone != storage_values[contact_id]["phone"],
                    contact.comment != storage_values[contact_id]["comment"],
            )):
                return True

        return False
