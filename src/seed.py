from src.repository import create_contact, add_group, get_groups
from faker import Faker
from random import randint, choices
from datetime import datetime

fake = Faker()


def seed_groups():
    groups = ['family', 'friends', 'services', 'job']
    for group in groups:
        add_group(group)


def seed_contacts(num: int = 50):
    groups_id = [group.id for group in get_groups()]
    for _ in range(num):
        first_name = fake.first_name()
        last_name = fake.last_name()
        phones = [fake.msisdn() for _ in range(randint(1, 3))]
        emails = [fake.email() for _ in range(randint(0, 2))]
        adress = fake.address().replace('\n', ' ')
        birth = fake.date(pattern='%d-%m-%Y', end_datetime='-18y')
        birth = datetime.strptime(birth, '%d-%m-%Y')
        groups = choices(groups_id, k=randint(0, 2))
        create_contact(first_name=first_name,
                       last_name=last_name,
                       phones=phones,
                       emails=emails,
                       adress=adress,
                       birth=birth,
                       groups=groups)
