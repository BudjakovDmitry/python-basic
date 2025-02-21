import json
import os
import random
import unittest

from src.model import PhonebookModel, Contact, ContactNotFound
from .utils import (
    generate_random_string,
    generate_random_phone,
    generate_random_id,
    generate_different_string,
    get_substring_from,
    generate_contacts_storage,
    generate_different_id,
)


class TestAddContact(unittest.TestCase):
    def setUp(self):
        self.phonebook = PhonebookModel()

    def test_return_contact_instance(self):
        new_contact = self.phonebook.add_contact(
            name=generate_random_string(),
            phone=generate_random_phone(),
            comment=generate_random_string(),
        )
        self.assertIsInstance(new_contact, Contact)

    def test_return_contact_values(self):
        name = generate_random_string()
        phone = generate_random_phone()
        comment = generate_random_string()
        new_contact = self.phonebook.add_contact(
            name=name, phone=phone, comment=comment
        )
        self.assertEqual(name, new_contact.name)
        self.assertEqual(phone, new_contact.phone)
        self.assertEqual(comment, new_contact.comment)

    def test_add_contact_to_cache(self):
        new_contact = self.phonebook.add_contact(
            name=generate_random_string(),
            phone=generate_random_phone(),
            comment=generate_random_string(),
        )
        self.assertIn(new_contact.id, self.phonebook._cache)

    def test_added_contact_values(self):
        new_contact = self.phonebook.add_contact(
            name=generate_random_string(),
            phone=generate_random_phone(),
            comment=generate_random_string(),
        )
        cached_contact = self.phonebook._cache[new_contact.id]
        self.assertDictEqual(new_contact.as_dict(), cached_contact.as_dict())

    def test_add_without_comment(self):
        new_contact = self.phonebook.add_contact(
            name=generate_random_string(), phone=generate_random_phone()
        )
        cached_contact = self.phonebook._cache[new_contact.id]
        self.assertIsNone(new_contact.comment)
        self.assertIsNone(cached_contact.comment)


class TestDeleteContact(unittest.TestCase):
    def setUp(self):
        self.phonebook = PhonebookModel()
        self.added_contact = self.phonebook.add_contact(
            name=generate_random_string(),
            phone=generate_random_phone(),
            comment=generate_random_string()
        )

    def tearDown(self):
        if os.path.exists(PhonebookModel.STORAGE):
            os.remove(PhonebookModel.STORAGE)

    def test_delete_existing_contact(self):
        self.phonebook.delete_contact(self.added_contact.id)
        self.assertNotIn(self.added_contact.id, self.phonebook._cache)

    def test_delete_not_existing_contact(self):
        not_existing_id = generate_random_id(from_=1000)
        self.phonebook.delete_contact(not_existing_id)
        self.assertEqual(len(self.phonebook._cache), 1)


class TestFindContact(unittest.TestCase):
    def setUp(self):
        self.contacts = generate_contacts_storage(how_many=10)
        with open(PhonebookModel.STORAGE, "w") as file:
            json.dump(self.contacts, file)

        self.phonebook = PhonebookModel()
        self.searching_contact = random.choice(self.contacts)

    def tearDown(self):
        if os.path.exists(self.phonebook.STORAGE):
            os.remove(self.phonebook.STORAGE)

    def test_search_using_name(self):
        search_field = self.searching_contact["name"]
        search_string_len = random.randint(1, len(search_field)-1)
        search_string = get_substring_from(search_field, length=search_string_len)
        result = self.phonebook.find_contacts(search_string)
        self.assertIn(self.searching_contact["id"], [row.id for row in result])

    def test_search_using_phone(self):
        search_field = self.searching_contact["phone"]
        search_string_len = random.randint(1, len(search_field)-1)
        searching_string = get_substring_from(search_field, length=search_string_len)
        result = self.phonebook.find_contacts(searching_string)
        self.assertIn(self.searching_contact["id"], [row.id for row in result])

    def test_search_using_comment(self):
        search_field = self.searching_contact["comment"]
        search_string_len = random.randint(1, len(search_field)-1)
        searching_string = get_substring_from(search_field, length=search_string_len)
        result = self.phonebook.find_contacts(searching_string)
        self.assertIn(self.searching_contact["id"], [row.id for row in result])

    def test_empty_search(self):
        existing = []
        for contact in self.contacts:
            existing.extend([contact["name"], contact["phone"], contact["comment"]])
        search_string = generate_different_string(*existing)
        result = self.phonebook.find_contacts(search_string)
        self.assertListEqual(result, [])


class TestGetContact(unittest.TestCase):
    def setUp(self):
        self.contacts = generate_contacts_storage(how_many=10)
        with open(PhonebookModel.STORAGE, "w") as file:
            json.dump(self.contacts, file)
        self.phonebook = PhonebookModel()

    def tearDown(self):
        if os.path.exists(PhonebookModel.STORAGE):
            os.remove(PhonebookModel.STORAGE)

    def test_get_contact(self):
        searching_id = random.choice(self.contacts)["id"]
        contact = self.phonebook.get(searching_id)
        self.assertIsNotNone(contact)

    def test_get_not_existing_contact(self):
        existing_ids = [c["id"] for c in self.contacts]
        searching_id = generate_different_id(*existing_ids)
        self.assertRaises(ContactNotFound, self.phonebook.get, searching_id)
