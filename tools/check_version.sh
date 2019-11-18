#!/bin/bash

PYSTOL_OPERATOR_VERSION=$(cat ./pystol-operator/setup.py | grep "_REVISION = '" | cut -d"'" -f2)
PYSTOL_HELM_VERSION=$(cat ./helm/Chart.yaml | grep version | cut -d"'" -f2)
PYSTOL_UI_VERSION=$(cat ./pystol-ui/package.json | grep version | cut -d'"' -f4)

if [[ "$PYSTOL_OPERATOR_VERSION" == "$PYSTOL_HELM_VERSION" && "$PYSTOL_OPERATOR_VERSION" == "$PYSTOL_UI_VERSION" ]]; then
    echo "Version match"
else
    echo "Version do not match"
    exit 1
fi
