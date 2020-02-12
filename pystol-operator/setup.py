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

import os
from sys import version_info

from setuptools import find_packages, setup

if version_info[:2] < (3, 5):
    raise RuntimeError(
        'Unsupported python version %s.' % '.'.join(version_info)
    )

_NAME = 'pystol'
_DESCRIPTION = 'The Pystol CLI'
_REVISION = '0.0.17'

pystol_revision = os.environ.get('PYSTOL_REVISION', "")
if (pystol_revision != ""):
    _REVISION = _REVISION + "." + pystol_revision

if os.path.isfile('../README.md'):
    with open('../README.md') as f:
        long_description = f.read()
else:
        long_description = _DESCRIPTION

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name=_NAME,
    version=_REVISION,
    description=_DESCRIPTION,
    long_description_content_type='text/markdown',
    long_description=long_description,
    url = 'https://www.pystol.org',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    author='Carlos Camacho',
    author_email='carloscamachoucv@gmail.com',
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            '{0} = {0}.cli:main'.format(_NAME),
        ]
    }
)
