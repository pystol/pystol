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


from os import environ
from sys import exit

from app import create_app, db

from config import config_dict

from flask_migrate import Migrate

get_config_mode = environ.get('PYSTOL_CONFIG_MODE', 'Debug')

try:
    config_mode = config_dict[get_config_mode.capitalize()]
except KeyError:
    exit('Error: Invalid PYSTOL_CONFIG_MODE environment variable entry.')

app = create_app(config_mode)
Migrate(app, db)

if __name__ == "__main__":
    app.run()
