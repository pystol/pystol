# CRD Settings
CRD_GROUP = 'pystol.org'
CRD_VERSION = 'v1'
CRD_PLURAL = 'pystols'

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
