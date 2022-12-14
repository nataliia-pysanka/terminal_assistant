from sqlalchemy import and_, extract
from sqlalchemy.orm import joinedload

from src.db import session
from src.models import Group, Contact, Phone, Email, ContactGroup
from typing import List
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime


def get_contacts(first_name: str = None,
                 last_name: str = None) -> List[Contact]:
    """Return contacts by name without loading joined information"""
    contacts = session.query(Contact).filter(
        and_(Contact.first_name == first_name,
             Contact.last_name == last_name)).all()
    return contacts


def get_contact_by_id(contact_id: int) -> Contact:
    """Return contact by id"""
    contact = session.query(Contact).filter(
             Contact.id == contact_id).one()
    return contact


def get_contacts_by_name(first_name: str = None,
                        last_name: str = None) -> List[Contact]:
    """Return contacts by name with joined information"""
    contacts = session.query(Contact).filter(
        and_(Contact.first_name == first_name,
             Contact.last_name == last_name)). \
        options(joinedload('groups'),
                joinedload('phones'),
                joinedload('emails')).all()

    return contacts


def get_contact_by_birth(day: datetime) -> List[Contact]:
    """Return contacts by full date of birth with joined information"""
    contacts = session.query(Contact).filter(
        Contact.birth == day). \
        options(joinedload('groups'),
                joinedload('phones'),
                joinedload('emails')).all()

    return contacts


def get_contact_by_date(day: int, month: int) -> List[Contact]:
    """Return contacts by day and month of birth with joined information"""
    contacts = session.query(Contact).filter(
        and_(extract('month', Contact.birth) == month,
             extract('day', Contact.birth) == day)). \
        options(joinedload('groups'),
                joinedload('phones'),
                joinedload('emails')).all()

    return contacts


def get_contact_by_groups(group: str) -> List[Contact]:
    """Return group with joined contacts"""
    group = session.query(Group).filter(Group.name == group). \
        options(joinedload('contacts')).one()

    return group


def get_contacts_joined() -> List[Contact]:
    """Return all contacts with joined information"""
    contacts = session.query(Contact).options(joinedload('groups'),
                                              joinedload('phones'),
                                              joinedload('emails')).all()

    return contacts


def create_joined_phones(contact: Contact, **kwargs):
    """Creates new Phone object in current session
    which join to inputted contact """
    if kwargs.get('phones'):
        for phone in kwargs['phones']:
            session.add(Phone(phone=phone, contact_id=contact.id))
            session.commit()


def create_joined_emails(contact: Contact, **kwargs):
    """Creates new Email object in current session
        which join to inputted contact """
    if kwargs.get('emails'):
        for email in kwargs['emails']:
            session.add(Email(email=email, contact_id=contact.id))
            session.commit()


def create_joined_groups(contact: Contact, **kwargs):
    """Creates new Group object in current session
        which join to inputted contact """
    if kwargs.get('groups'):
        for group in kwargs['groups']:
            session.add(
                ContactGroup(group_id=group, contact_id=contact.id))
            session.commit()


def delete_joined_phones(contact: Contact):
    """Deletes all phones joined to current contact"""
    session.query(Phone).filter(Phone.contact_id == contact.id).delete()
    session.commit()


def delete_joined_emails(contact: Contact):
    """Deletes all emails joined to current contact"""
    session.query(Email).filter(Email.contact_id == contact.id).delete()
    session.commit()


def delete_joined_groups(contact: Contact):
    """Deletes all groups joined to current contact"""
    session.query(Group).filter(Group.contact_id == contact.id).delete()
    session.commit()


def create_contact(**kwargs) -> Contact:
    """Creates new Contact object and joined objectes"""
    contact = Contact(
        first_name=kwargs['first_name'],
        last_name=kwargs['last_name'],
        adress=kwargs['adress'],
        birth=kwargs['birth'])

    session.add(contact)
    session.commit()

    create_joined_phones(contact, **kwargs)
    create_joined_emails(contact, **kwargs)
    create_joined_groups(contact, **kwargs)

    session.refresh(contact)
    session.close()


def update_contact(contact: Contact, **kwargs) -> Contact:
    """Updates current object and joined objects"""
    if kwargs.get('first_name'):
        contact.first_name = kwargs['first_name']
        session.commit()
    if kwargs.get('last_name'):
        contact.last_name = kwargs['last_name']
        session.commit()
    if kwargs.get('adress'):
        contact.adress = kwargs['adress']
        session.commit()
    if kwargs.get('birth'):
        contact.birth = kwargs['birth']
        session.commit()

    if kwargs.get('phones'):
        delete_joined_phones(contact)
        create_joined_phones(contact, **kwargs)

    if kwargs.get('emails'):
        delete_joined_emails(contact)
        create_joined_emails(contact, **kwargs)

    if kwargs.get('groups'):
        delete_joined_groups(contact)
        create_joined_groups(contact, **kwargs)

    session.refresh(contact)
    session.close()
    return contact


def remove_contact(contact_id: int):
    """Removes contact by id"""
    session.query(Contact).filter(Contact.id == contact_id).delete()
    session.commit()
    session.close()


def get_groups() -> List[Group]:
    """Returns all groups"""
    groups = session.query(Group).all()
    return groups


def get_group(name: str) -> Group:
    """Return group by name"""
    group = session.query(Group).filter(Group.name == name).one()
    return group


def add_group(name: str) -> Group:
    """Create new Group object"""
    group = Group(name=name)
    session.add(group)
    session.commit()
    session.close()
    return group
