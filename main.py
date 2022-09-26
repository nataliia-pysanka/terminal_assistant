import argparse
import sys
from sqlalchemy.exc import SQLAlchemyError
from src.repository import get_groups, get_contacts, add_group, \
    get_group, create_contact, remove_contact, update_contact, \
    get_contacts_by_name, get_contact_by_birth, get_contact_by_groups, \
    get_contact_by_date, get_contacts_joined, get_contact_by_id
import re
from datetime import datetime
from src.models import Contact
from src.seed import seed_groups, seed_contacts


parser = argparse.ArgumentParser(description='ContactBook APP')
parser.add_argument('--action', '-a',
                   help='Command: create, update, list, remove')
parser.add_argument('--search', '-s',
                   help='Command: name, date, groups')
parser.add_argument('--birth',
                    '-b',
                    nargs='?',
                    const=datetime.now().strftime("%d.%m"),
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
        print('\t', item.birth.strftime("%d.%m.%Y"))
    if item.groups:
        lst = [group.name for group in item.groups]
        print(f'GROUPS: {",".join(lst)}')
    print()


def input_data():
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

    return contact


def create():
    contact = input_data()
    create_contact(**contact)


def get_list_by_name():
    first_name = input('Input first name > ')
    last_name = input('Input last name > ')
    contacts = get_contacts(first_name=first_name, last_name=last_name)

    if not contacts:
        print('Not found')
        return None
    return contacts


def clear_dict(dictionary: dict):
    key_lst = [key for key in dictionary if not dictionary[key]]

    for key in key_lst:
        del dictionary[key]

    return dictionary


def update():
    contacts = get_list_by_name()

    if not contacts:
        return

    for contact in contacts:
        print_contact(contact)
        while True:
            button = input('Continue editing this contact ? (Y/n)')
            if button == 'Y':
                new_data = input_data()
                new_data = clear_dict(new_data)
                update_contact(contact, **new_data)
                break
            elif button == 'n':
                break


def search_name():
    first_name = input('Input first name > ')
    last_name = input('Input last name > ')
    contacts = get_contacts_by_name(first_name=first_name, last_name=last_name)
    if contacts:
        for item in contacts:
            print_contact(item)
    else:
        print('Not found')


def get_date(str_date: str):
    """
    Parses the inputted string and returns datetime object
    """
    date_formats = ['%d-%m', '%d/%m', '%d%m', '%d %m', '%d.%m',
                    '%d-%m-%Y', '%d/%m/%Y', '%d%m%Y', '%d %m %Y', '%d.%m.%Y',
                    '%d-%b-%Y', '%d/%b/%Y', '%d%b%Y', '%d %b %Y', '%d.%b.%Y',
                    '%d-%B-%Y', '%d/%B/%Y', '%d%B%Y', '%d %B %Y', '%d.%b.%Y',
                    '%d-%m-%y', '%d/%m/%y', '%d%m%y', '%d %m %y', '%d.%m.%y',
                    '%d-%b-%y', '%d/%b/%y', '%d%b%y', '%d %b %y', '%d.%b.%y',
                    '%d-%B-%y', '%d/%B/%y', '%d%B%y', '%d %B %y', '%d.%b.%y']

    if str_date is None:
        return datetime.now()

    for d_f in date_formats:
        try:
            date_ = datetime.strptime(str_date, d_f)
            return date_
        except ValueError:
            continue
    return datetime.now()


def search_date():
    date = input('Input date and month (year if necessary)" > ')
    date = get_date(date)
    if date.year == 1900:
        contacts = get_contact_by_date(day=date.day, month=date.month)
    else:
        birth = datetime(day=date.day, month=date.month, year=date.year)
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
    contacts = get_contacts_joined()
    for item in contacts:
        print_contact(item)


def remove():
    contacts = get_list_by_name()
    contacts = [contact.id for contact in contacts]
    if not contacts:
        return

    for contact_id in contacts:
        contact = get_contact_by_id(contact_id)
        print_contact(contact)
        while True:
            button = input('Are you sure to delete? (Y/n) > ')
            if button == 'Y':
                remove_contact(contact.id)
                break
            elif button == 'n':
                break


def birth_on_date():
    day = datetime.now().day
    month = datetime.now().month
    contacts = get_contact_by_date(day, month)
    if contacts:
        for item in contacts:
            print_contact(item)
    else:
        print('No birthdays today')


def action_scope():
    match action:
        case 'create':
            create()
        case 'update':
            update()
        case 'list':
            list_all()
        case 'remove':
            remove()
        case _:
            print("Error: Incorrect inputted data")


def search_scope():
    match search:
        case 'name':
            search_name()
        case 'date':
            search_date()
        case 'group':
            search_group()
        case _:
            print("Error: Incorrect inputted data")


def main():
    try:
        # seed_groups()
        # seed_contacts()
        if action:
            action_scope()
        if search:
            search_scope()
        if birthday:
            birth_on_date()
    except SQLAlchemyError as err:
        print(f'Error: {err}')

    sys.exit()


if __name__ == '__main__':
    main()


