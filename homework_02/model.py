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
        self.id_ = id_
        self.name = name
        self.phone = phone
        self.comment = comment

    @staticmethod
    def from_dict(dict_args: dict):
        """
        Returns new Contact instance from dict.
        :param dict_args: dict with valid contact arguments
        """
        return Contact(
            id_=int(dict_args["id_"]),
            name=dict_args["name"],
            phone=dict_args["phone"],
            comment=dict_args["comment"],
        )

    def has(self, search: str) -> bool:
        """
        Returns True if contact contains substring
        :param search: search substring
        :return: True if one of contact's attributes contain search substring
                 False otherwise
        """
        for value in (self.name, self.phone, self.comment):
            if search in value.lower():
                return True
        return False

    def update(
        self,
        new_name: str | None = None,
        new_phone: str | None = None,
        new_comment: str | None = None,
    ):
        """Update contact's parameters."""
        if new_name:
            self.name = new_name
        if new_phone:
            self.phone = new_phone
        self.comment = new_comment


class JsonStorage:
    """Represents json-based file storage of the Phonebook."""

    def __init__(self):
        self.STORAGE = "phonebook.json"

        # create file if needed or load data from existing file
        if os.path.isfile(self.STORAGE):
            with open(self.STORAGE, "r") as storage:
                for row in json.load(storage).values():
                    contact = Contact.from_dict(row)
                    self._cache[contact.id_] = contact
        else:
            with open(self.STORAGE, "w") as storage:
                json.dump({}, storage)

    def save(self):
        """Save contacts to the file storage."""
        cache_as_json = {id_: contact.__dict__ for id_, contact in self._cache.items()}
        with open(self.STORAGE, "w") as storage:
            json.dump(cache_as_json, storage)

    def raw_storage(self) -> dict:
        """Returns raw storage data."""
        with open(self.STORAGE, "r") as file:
            return json.load(file)


class PhonebookModel(JsonStorage):
    """Represents data and business logic of Phonebook."""

    def __init__(self):
        self._cache = {}
        super().__init__()

    def add_contact(self, name: str, phone: str, comment: str = None) -> Contact:
        """Add contact to phonebook."""
        contact_id = self._next_cache_id()

        contact = Contact(id_=contact_id, name=name, phone=phone, comment=comment)
        self._cache[contact_id] = contact
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
