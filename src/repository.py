from sqlalchemy import and_
from sqlalchemy.orm import joinedload

from src.db import session
from src.models import Group, Contact, Phone, Email, ContactGroup
from typing import List
from sqlalchemy.exc import SQLAlchemyError


def get_contact(first_name: str = None, last_name: str = None) -> Contact:
    contacts = session.query(Contact).filter(
        and_(Contact.first_name == first_name,
             Contact.last_name == last_name)).all()

    return contacts


def get_contacts() -> List[Contact]:
    contacts = session.query(Contact).options(joinedload('groups'),
                                              joinedload('phones'),
                                              joinedload('emails')).all()

    return contacts


def create_contact(**kwargs) -> Contact:
    try:
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
    except SQLAlchemyError as err:
        print(err)
        session.rollback()
    session.close()
    return contact


def update_contact(contact: Contact, **kwargs) -> Contact:
    try:
        for field in kwargs:
            setattr(contact, field, kwargs[field])
    except AttributeError:
        return None

    session.add(contact)
    session.commit()
    session.refresh(contact)
    return contact


def remove_contact(contact: Contact) -> int:
    contact.delete()
    session.commit()
    session.close()
    return contact


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
