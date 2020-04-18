#!/usr/bin/env python

"""
Copyright 2019 Pystol (pystol.org).

Licensed under the Apache License, Version 2.0 (the "License"); you may
not use this file except in compliance with the License. You may obtain
a copy of the License at:

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
License for the specific language governing permissions and limitations
under the License.
"""


from app import db, login_manager
from app.base.util import hash_pass

from flask_login import UserMixin

from sqlalchemy import Binary, Column, Integer, String


class User(db.Model, UserMixin):
    """
    The user model definition.

    This is a main class
    """

    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(Binary)

    def __init__(self, **kwargs):
        """
        Return the user.

        This is a main method
        """
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass(value)  # We need bytes here (not plain str)

            setattr(self, property, value)

    def __repr__(self):
        """
        Return the username.

        This is a main method
        """
        return str(self.username)


@login_manager.user_loader
def user_loader(id):
    """
    Load the username.

    This is a main method
    """
    return User.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    """
    Load the user request.

    This is a main method
    """
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    return user if user else None
