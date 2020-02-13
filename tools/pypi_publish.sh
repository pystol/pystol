#!/bin/bash

PARAMS=""
while (( "$#" )); do
    case "$1" in
        -k|--pypi-key)
            KARG=$2
            shift 2
            ;;
        --) # end argument parsing
            shift
            break
            ;;
        -*|--*=) # unsupported flags
            echo "Error: Unsupported flag $1" >&2
            echo "Please use ./pypi_publish.sh [-k <pypi key> | --pypi-key <pypi key>]" >&2
            exit 1
            ;;
        *) # preserve positional arguments
        PARAMS="$PARAMS $1"
        shift
        ;;
    esac
done

#
# Initial variables
#

all_published_versions=$(curl -L https://pypi.python.org/pypi/pystol/json | jq -r '.releases' | jq 'keys[]')
current_pystol_version=$(cat pystol-operator/setup.py | grep "_REVISION = '" | cut -d "'" -f 2)

publish="1"

#
# Check all the current published versions and if the
# packaged to be created has a different version, then
# we publish it to Galaxy Ansible
#

for ver in $all_published_versions; do
    echo "--"
    echo "Published: "$ver
    echo "Built: "$current_pystol_version
    echo ""
    if [[ $ver == \"$current_pystol_version\" ]]; then
        echo "The current version $current_pystol_version is already published"
        echo "Proceed to update the setup.py file with a newer version"
        echo "After the version change, when the commit is merged, then the package"
        echo "will be published automatically."
        publish="0"
    fi
done

if [ "$publish" == "1" ]; then
    echo 'This version is not published, publishing!...'
    cd ./pystol-operator
    python3 setup.py sdist
    twine check dist/*

cat <<EOF > ~/.pypirc
[distutils]
index-servers =
    pypi
    testpypi
    pystol

[pypi]
username = __token__

[testpypi]
username = __token__

[pystol]
repository = https://upload.pypi.org/legacy/
username = __token__
password = $KARG
EOF

    twine upload --verbose --repository pystol dist/*
fi
