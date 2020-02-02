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

# CRD Settings
CRD_DOMAIN = 'pystol.org'
CRD_VERSION = 'v1alpha1'
CRD_PLURAL = 'pystolactions'

# Type methods maps
LIST_TYPES_MAP = {
    'configmap': 'list_namespaced_config_map',
    'secret': 'list_namespaced_secret',
}

CREATE_TYPES_MAP = {
    'configmap': 'create_namespaced_config_map',
    'secret': 'create_namespaced_secret',
}

# Allowed events
ALLOWED_EVENT_TYPES = {'ADDED', 'UPDATED'}
