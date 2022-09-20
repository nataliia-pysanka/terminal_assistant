from src.repository import create_contact, add_group, get_groups
from faker import Faker
from random import randint, choices

fake = Faker()


def seed_groups():
    groups = ['family', 'friends', 'services', 'job']
    for group in groups:
        add_group(group)


def seed_contacts():
    groups_id = [group.id for group in get_groups()]
    for _ in range(50):
        first_name = fake.first_name()
        last_name = fake.last_name()
        phones = [fake.msisdn() for _ in range(randint(1, 3))]
        emails = [fake.email() for _ in range(randint(0, 2))]
        adress = fake.address().replace('\n', ' ')
        birth = fake.date_between(start_date='-60y', end_date='-18y')
        groups = choices(groups_id, k=randint(0, 2))
        create_contact(first_name=first_name,
                       last_name=last_name,
                       phones=phones,
                       emails=emails,
                       adress=adress,
                       birth=birth,
                       groups=groups)
