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

import kubernetes

from pystol.const import CRD_GROUP, CRD_PLURAL, CRD_VERSION

__all__ = [
    'load_crd',
]


def load_crd(namespace, name):
    """
    Load the CRD.

    It is used to get the object's watching settings.
    """
    client = kubernetes.client.ApiClient()
    custom_api = kubernetes.client.CustomObjectsApi(client)

    crd = custom_api.get_namespaced_custom_object(
        CRD_GROUP,
        CRD_VERSION,
        namespace,
        CRD_PLURAL,
        name,
    )
    return {x: crd[x] for x in ('ruleType', 'selector', 'namespace')}
