from sqlalchemy import and_, extract
from sqlalchemy.orm import joinedload

from src.db import session
from src.models import Group, Contact, Phone, Email, ContactGroup
from typing import List
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime


def get_contacts(first_name: str = None,
                 last_name: str = None) -> List[Contact]:
    contacts = session.query(Contact).filter(
        and_(Contact.first_name == first_name,
             Contact.last_name == last_name)).all()
    return contacts


def get_contact_by_id(contact_id: int) -> Contact:
    contact = session.query(Contact).filter(
             Contact.id == contact_id).one()
    return contact


def get_contacts_by_name(first_name: str = None,
                        last_name: str = None) -> List[Contact]:
    contacts = session.query(Contact).filter(
        and_(Contact.first_name == first_name,
             Contact.last_name == last_name)). \
        options(joinedload('groups'),
                joinedload('phones'),
                joinedload('emails')).all()

    return contacts


def get_contact_by_birth(day: datetime) \
        -> List[Contact]:
    contacts = session.query(Contact).filter(
        Contact.birth == day). \
        options(joinedload('groups'),
                joinedload('phones'),
                joinedload('emails')).all()

    return contacts


def get_contact_by_date(day: int, month: int) -> List[Contact]:
    contacts = session.query(Contact).filter(
        and_(extract('month', Contact.birth) == month,
             extract('day', Contact.birth) == day)). \
        options(joinedload('groups'),
                joinedload('phones'),
                joinedload('emails')).all()

    return contacts


def get_contact_by_groups(group: str) -> List[Contact]:
    group = session.query(Group).filter(Group.name == group). \
        options(joinedload('contacts')).one()

    return group


def get_contacts_joined() -> List[Contact]:
    contacts = session.query(Contact).options(joinedload('groups'),
                                              joinedload('phones'),
                                              joinedload('emails')).all()

    return contacts


# def set_joined_fields(**kwargs):

def create_contact(**kwargs) -> Contact:
    contact = Contact(
        first_name=kwargs['first_name'],
        last_name=kwargs['last_name'],
        adress=kwargs['adress'],
        birth=kwargs['birth'])

    session.add(contact)
    session.commit()

    if kwargs.get('phones'):
        for phone in kwargs['phones']:
            session.add(Phone(phone=phone, contact_id=contact.id))
            session.commit()
    if kwargs.get('emails'):
        for email in kwargs['emails']:
            session.add(Email(email=email, contact_id=contact.id))
            session.commit()
    if kwargs.get('groups'):
        for group in kwargs['groups']:
            session.add(
                ContactGroup(group_id=group, contact_id=contact.id))
            session.commit()
    session.refresh(contact)
    session.close()


def update_contact(contact: Contact, **kwargs) -> Contact:
    try:
        for field in kwargs:
            print(getattr(contact, field))
            # setattr(contact, field, kwargs[field])
    except AttributeError:
        print('Cant update')
        return None
    # contact.update(kwargs)
    session.add(contact)
    session.commit()
    session.refresh(contact)
    return contact


def remove_contact(contact_id: int):
    session.query(Contact).filter(Contact.id == contact_id).delete()
    session.commit()
    session.close()


def get_groups() -> List[Group]:
    groups = session.query(Group).all()
    return groups


def get_group(name: str) -> Group:
    group = session.query(Group).filter(Group.name == name).one()
    return group


def add_group(name: str) -> Group:
    group = Group(name=name)
    session.add(group)
    session.commit()
    session.close()
    return group
