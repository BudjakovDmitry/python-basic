import os
import unittest
import json

from src.model import JsonStorage
from .utils import generate_contacts_storage, generate_contact, generate_contacts


class TestStorageCreation(unittest.TestCase):
    def setUp(self):
        self.storage = "phonebook.json"
        if os.path.exists(self.storage):
            os.remove(self.storage)

    def tearDown(self):
        if os.path.exists(self.storage):
            os.remove(self.storage)

    def test_file_created(self):
        JsonStorage()
        self.assertTrue(os.path.exists(self.storage))

    def test_file_init_structure(self):
        JsonStorage()
        with open(self.storage, "r") as file:
            data = json.load(file)
            self.assertListEqual([], data)


class TestExistingStorageOpen(unittest.TestCase):
    def setUp(self):
        self.storage = "phonebook.json"
        self.data = generate_contacts_storage(how_many=10)
        with open(self.storage, "w") as file:
            json.dump(self.data, file)

    def tearDown(self):
        if os.path.exists(self.storage):
            os.remove(self.storage)

    def test_cache_length(self):
        storage = JsonStorage()
        self.assertEqual(len(self.data), len(storage._cache))

    def test_cache_ids(self):
        storage = JsonStorage()
        expected_ids = [row["id"] for row in self.data]
        real_ids = [id_ for id_ in storage._cache]
        self.assertListEqual(expected_ids, real_ids)

    def test_cache_contact(self):
        storage = JsonStorage()
        values = [row.as_dict() for row in storage._cache.values()]
        for expected, real in zip(self.data, values):
            self.assertDictEqual(expected, real)


class TestStorageAddToCache(unittest.TestCase):

    def tearDown(self):
        storage = "phonebook.json"
        if os.path.exists(storage):
            os.remove(storage)

    def test_add_to_cache(self):
        storage = JsonStorage()
        contact = generate_contact()
        storage.add_to_cache(contact)
        self.assertIn(contact.id, storage._cache)

    def test_cache_values(self):
        storage = JsonStorage()
        contact = generate_contact()
        storage.add_to_cache(contact)
        cached_contact = storage._cache[contact.id]
        self.assertDictEqual(contact.as_dict(), cached_contact.as_dict())


class TestSaveStorage(unittest.TestCase):
    def setUp(self):
        self.storage = JsonStorage()
        for contact in generate_contacts(how_many=10):
            self.storage.add_to_cache(contact)

    def tearDown(self):
        if os.path.exists(self.storage.STORAGE):
            os.remove(self.storage.STORAGE)

    def test_length(self):
        self.storage.save()
        expected = len(self.storage._cache)
        with open(self.storage.STORAGE, "r") as file:
            real_file_rows = len(json.load(file))
        self.assertEqual(expected, real_file_rows)

    def test_save(self):
        self.storage.save()
        cached_values = self.storage._cache.values()
        with open(self.storage.STORAGE, "r") as file:
            jsoned_file_values = json.load(file)
            for f, c in zip(jsoned_file_values, cached_values):
                self.assertDictEqual(f, c.as_dict())


class TestRawStorage(unittest.TestCase):
    def setUp(self):
        self.storage_contacts = generate_contacts_storage(how_many=10)
        with open(JsonStorage.STORAGE, "w") as file:
            json.dump(self.storage_contacts, file)

    def tearDown(self):
        if os.path.exists(JsonStorage.STORAGE):
            os.remove(JsonStorage.STORAGE)

    def test_len(self):
        storage = JsonStorage()
        expected_len = len(self.storage_contacts)
        raw_data = storage.raw_storage()
        real_len = len(raw_data)
        self.assertEqual(expected_len, real_len)

    def test_values(self):
        storage = JsonStorage()
        raw_data = storage.raw_storage()
        for expected, real in zip(self.storage_contacts, raw_data):
            self.assertDictEqual(expected, real)


if __name__ == "__main__":
    unittest.main()
