from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

from src.db import Base


class Contact(Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)
    phones = relationship('Phone', back_populates='contact')
    emails = relationship('Email', back_populates='contact')
    adress = Column('address', String(100), nullable=True)
    birth = Column('birth', Date, nullable=True)
    groups = relationship('Group', secondary='contacts_to_groups',
                          back_populates='contacts')


class Phone(Base):
    __tablename__ = 'phones'
    id = Column(Integer, primary_key=True)
    phone = Column('phone', String(20), nullable=False)
    contact_id = Column('contact_id',
                        ForeignKey('contacts.id', ondelete='CASCADE'),
                        nullable=False)
    contact = relationship('Contact', back_populates='phones')


class Email(Base):
    __tablename__ = 'emails'
    id = Column(Integer, primary_key=True)
    email = Column('email', String(50), nullable=False)
    contact_id = Column('contact_id',
                        ForeignKey('contacts.id', ondelete='CASCADE'),
                        nullable=False)
    contact = relationship('Contact', back_populates='emails')


class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    contacts = relationship('Contact', secondary='contacts_to_groups',
                            back_populates='groups')


class ContactGroup(Base):
    __tablename__ = 'contacts_to_groups'
    id = Column(Integer, primary_key=True)
    group_id = Column('group_id', ForeignKey('groups.id', ondelete='CASCADE'))
    contact_id = Column('contact_id', ForeignKey('contacts.id',
                                                 ondelete='CASCADE'))
