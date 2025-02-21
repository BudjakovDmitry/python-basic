import unittest

from src.model import Contact
from .utils import (
    generate_random_id,
    generate_random_string,
    generate_random_phone,
    get_substring_from,
    generate_different_string,
    generate_contact
)


class TestContact(unittest.TestCase):

    def test_is_instance(self):
        contact = generate_contact()
        self.assertIsInstance(contact, Contact)

    def test_id(self):
        id_ = generate_random_id()
        contact = Contact(
            id_=id_,
            name=generate_random_string(),
            phone=generate_random_phone(),
            comment=generate_random_string(),
        )
        self.assertEqual(id_, contact.id)

    def test_id_type(self):
        contact = generate_contact()
        self.assertIsInstance(contact.id, int)

    def test_name(self):
        name = generate_random_string()
        contact = Contact(
            id_=generate_random_id(),
            name=name,
            phone=generate_random_phone(),
            comment=generate_random_string(),
        )
        self.assertEqual(name, contact.name)

    def test_name_type(self):
        contact = generate_contact()
        self.assertIsInstance(contact.name, str)

    def test_phone(self):
        phone = generate_random_phone()
        contact = Contact(
            id_=generate_random_id(),
            name=generate_random_string(),
            phone=phone,
            comment=generate_random_string(),
        )
        self.assertEqual(phone, contact.phone)


    def test_phone_type(self):
        contact = generate_contact()
        self.assertIsInstance(contact.phone, str)

    def test_comment(self):
        comment = generate_random_string()
        contact = Contact(
            id_=generate_random_id(),
            name=generate_random_string(),
            phone=generate_random_phone(),
            comment=comment
        )
        self.assertEqual(comment, contact.comment)

    def test_comment_type(self):
        contact = generate_contact()
        self.assertIsInstance(contact.comment, str)

    def test_contact_without_comment(self):
        contact = Contact(
            id_=generate_random_id(),
            name=generate_random_string(),
            phone=generate_random_phone(),
        )
        self.assertIsNone(contact.comment)


class TestContactHas(unittest.TestCase):
    def setUp(self):
        self.contact = Contact(
            id_=generate_random_id(),
            name=generate_random_string(length=15),
            phone=generate_random_phone(),
            comment=generate_random_string(length=15),
        )

    def test_found_in_name(self):
        search_string = get_substring_from(self.contact.name, length=5)
        self.assertTrue(self.contact.has(search_string))

    def test_name_uppercase(self):
        search_string = get_substring_from(self.contact.name, length=5)
        self.assertTrue(self.contact.has(search_string.upper()))

    def test_found_in_phone(self):
        ss_length = len(self.contact.phone) - 3
        search_string = get_substring_from(self.contact.phone, length=ss_length)
        self.assertTrue(self.contact.has(search_string))

    def test_found_in_comment(self):
        search_string = get_substring_from(self.contact.comment, length=5)
        self.assertTrue(self.contact.has(search_string))

    def test_comment_uppercase(self):
        search_string = get_substring_from(self.contact.comment, length=5)
        self.assertTrue(self.contact.has(search_string.upper()))

    def test_not_found(self):
        search_string = generate_different_string(
            self.contact.name, self.contact.phone, self.contact.phone
        )
        self.assertFalse(self.contact.has(search_string))


class TestContactUpdate(unittest.TestCase):
    def setUp(self):
        self.contact = generate_contact()

    def test_update_name(self):
        new_name = generate_random_string()
        self.contact.update_name(new_name)
        self.assertEqual(self.contact.name, new_name)

    def test_empty_name(self):
        old_name = self.contact.name
        self.contact.update_name("")
        self.assertEqual(self.contact.name, old_name)

    def test_update_phone(self):
        new_phone = generate_random_phone()
        self.contact.update_phone(new_phone)
        self.assertEqual(self.contact.phone, new_phone)

    def test_empty_phone(self):
        old_phone = self.contact.phone
        self.contact.update_phone("")
        self.assertEqual(self.contact.phone, old_phone)

    def test_update_comment(self):
        new_comment = generate_random_phone()
        self.contact.update_comment(new_comment)
        self.assertEqual(self.contact.comment, new_comment)

    def test_empty_comment(self):
        old_comment = self.contact.comment
        self.contact.update_comment("")
        self.assertEqual(self.contact.comment, old_comment)

    def test_clear_comment(self):
        self.contact.clear_comment()
        self.assertIsNone(self.contact.comment)


class TestContactAsDict(unittest.TestCase):
    def setUp(self):
        self.contact = generate_contact()

    def test_as_dict(self):
        expected = {
            "id": self.contact.id,
            "name": self.contact.name,
            "phone": self.contact.phone,
            "comment": self.contact.comment,
        }
        self.assertDictEqual(expected, self.contact.as_dict())


if __name__ == '__main__':
    unittest.main()
