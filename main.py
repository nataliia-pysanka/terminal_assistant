import argparse
import sys
from sqlalchemy.exc import SQLAlchemyError
from src.repository import get_groups, get_contacts, add_group, \
    get_group, create_contact, remove_contact, update_contact, \
    get_contact_by_name, get_contact_by_birth, get_contact_by_groups
import re
from datetime import datetime
from src.models import Contact
from src.db import session
from src.seed import seed_groups, seed_contacts


parser = argparse.ArgumentParser(description='ContactBook APP')
parser.add_argument('--action', '-a',
                   help='Command: create, update, list, remove')
parser.add_argument('--search', '-s',
                   help='Command: name, birth, groups')
parser.add_argument('--date',
                    nargs='?',
                    const=datetime.now().strftime("%d.%m.%Y"),
                    type=str)

arguments = parser.parse_args()
my_arg = vars(arguments)

action = my_arg.get('action')
search = my_arg.get('search')
birthday = my_arg.get('date')


def input_name(text: str):
    while True:
        name = input(f'Input {text} > ')
        if len(name) > 0:
            return name


def input_phone():
    numbers = []
    while True:
        num = input('Input phone number (to skip press Enter) > ')
        if len(num) == 0:
            break
        num = (num.strip().removeprefix('+')
               .replace("(", '')
               .replace(")", '')
               .replace(" ", '')
               .replace("-", ''))
        if not num.isdigit():
            print("Phone should contain numbers")
            continue
        numbers.append(num)
    return numbers


def input_email():
    emails = []
    while True:
        email = input('Input email (to skip press Enter) > ')
        if len(email) == 0:
            break
        pattern = r"[a-zA-Z]+[a-zA-Z0-9._]+@[a-z]+\.[a-z]{2,}"
        if re.match(pattern, email):
            emails.append(email)
            continue
        else:
            print("Email pattern doesn't match. Try again")
            continue
    return emails


def input_adress():
    adress = input('Input adress (to skip press Enter) > ')
    if len(adress) == 0:
        return None
    return adress


def input_birth():
    while True:
        birth = input("Input birth day '%d.%m.%Y' (to skip press Enter) > ")
        if len(birth) == 0:
            return None
        try:
            birth = datetime.strptime(birth, '%d.%m.%Y')
        except ValueError:
            print("Incorrect date format. Please try again")
            continue
        return birth


def input_group():
    contact_groups = []
    groups = get_groups()
    group_list = [group.name for group in groups]
    while True:
        print('Available groups:', ' '.join(group_list))
        group = input("Input group (to skip press Enter) > ")
        if len(group) == 0:
            break
        if group not in group_list:
            group = add_group(group)
        else:
            group = get_group(group)
        contact_groups.append(group.id)
        group_list.append(group.name)
    return contact_groups


def print_contact(item: Contact):
    print(f'>>>>> {item.first_name + " " + item.last_name:<60}')
    if item.phones:
        print('PHONES:')
        for phone in item.phones:
            print('\t', phone.phone)
    if item.emails:
        print('EMAILS:')
        for email in item.emails:
            print('\t', email.email)
    if item.adress:
        print('ADRESS:')
        print('\t', item.adress)
    if item.birth:
        print('BIRTH:')
        print('\t', item.birth.strftime("%m.%d.%Y"))
    if item.groups:
        lst = [group.name for group in item.groups]
        print(f'GROUPS: {",".join(lst)}')
    print()


def create():
    contact = {}
    first_name = input_name('first name')
    if first_name:
        contact['first_name'] = first_name

    last_name = input_name('last name')
    if last_name:
        contact['last_name'] = last_name

    phone = input_phone()
    if phone:
        contact['phones'] = phone
    else:
        contact['phones'] = []

    email = input_email()
    if email:
        contact['emails'] = email
    else:
        contact['emails'] = []

    adress = input_adress()
    if adress:
        contact['adress'] = adress
    else:
        contact['adress'] = None
    birth = input_birth()
    if birth:
        contact['birth'] = birth
    else:
        contact['birth'] = None
    groups = input_group()
    if groups:
        contact['groups'] = groups
    else:
        contact['groups'] = []

    res = create_contact(**contact)
    if res:
        print_contact(res)


def update():
    return {}


def search_name():
    first_name = input('Input first name > ')
    last_name = input('Input last name > ')
    contacts = get_contact_by_name(first_name=first_name, last_name=last_name)
    if contacts:
        for item in contacts:
            print_contact(item)
    else:
        print('Not found')


def search_birth():
    birth = input("Input birthday date in format '%d.%m.%Y' > ")
    if not birth:
        birth = datetime.now().strftime("%d.%m.%Y")
    contacts = get_contact_by_birth(day=birth)
    if contacts:
        for item in contacts:
            print_contact(item)
    else:
        print('Not found')


def search_group():
    group_name = input("Input group name > ")
    group = get_contact_by_groups(group=group_name)
    if group:
        for item in group.contacts:
            print_contact(item)
    else:
        print('Not found')


def list_all():
    contacts = get_contacts()
    for item in contacts:
        print_contact(item)


def remove():
    return {}


def birth_on_date():
    print(type(action.date))


def action_scope():
    match action:
        case 'create':
            create()
        # case 'update':
        #     update()
        case 'list':
            list_all()
        # case 'remove':
        #     remove()
        case _:
            print("Error: Incorrect inputted data")


def search_scope():
    match search:
        case 'name':
            search_name()
        case 'birth':
            search_birth()
        case 'group':
            search_group()


if __name__ == '__main__':
    try:
        # seed_groups()
        # seed_contacts()
        # main()
        if action:
            action_scope()
        elif search:
            search_scope()
        elif birthday:
            birth_on_date()
    except SQLAlchemyError as err:
        print(err)

    sys.exit()


