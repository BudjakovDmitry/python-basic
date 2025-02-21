from random import choice, randint
from string import ascii_letters

from src.model import Contact


def generate_random_id(from_: int = 1, to: int = 100_000) -> int:
    return randint(from_, to)


def generate_unique_ids(how_many: int = 10):
    ids = set()
    ids_counter = 0
    while ids_counter < how_many:
        id_ = generate_random_id()
        if id_ in ids:
            continue
        ids.add(id_)
        yield id_
        ids_counter += 1


def generate_random_string(length: int = 10) -> str:
    return ''.join((choice(ascii_letters) for _ in range(length)))


def generate_random_phone() -> str:
    phone_len = randint(6, 15)
    return ''.join(str(randint(0, 9)) for _ in range(phone_len))


def generate_contact():
    return Contact(
        id_=generate_random_id(),
        name=generate_random_string(),
        phone=generate_random_phone(),
        comment=generate_random_string(),
    )


def generate_contacts(how_many: int = 10):
    for _ in range(how_many):
        yield generate_contact()


def get_substring_from(origin_string: str, length: int = 1) -> str:
    if length > len(origin_string):
        return origin_string
    first_index_min = 0
    first_index_max = len(origin_string) - length
    first_index = randint(first_index_min, first_index_max)
    last_index = first_index + length
    return origin_string[first_index:last_index]


def generate_different_string(*args):
    min_len = min(map(len, args))
    while True:
        result = generate_random_string(length=min_len)
        if not any((result in s for s in args)):
            return result


def generate_different_id(*args):
    while True:
        id_ = generate_random_id()
        if id_ not in args:
            return id_


def generate_contacts_storage(how_many: int = 10):
    return [
        {
            "id": uid,
            "name": generate_random_string(),
            "phone": generate_random_phone(),
            "comment": generate_random_string(),
        }
        for uid in generate_unique_ids(how_many)
    ]
