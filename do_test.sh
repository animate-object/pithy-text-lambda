#!/usr/bin/env bash

hr() {
    printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
}

cleanup() {
    exit_code=$?
    hr
    echo Tearing down test env
    hr
    deactivate
    rm -rf testenv
    [ $exit_code -eq 0 ] & echo Test run successful & hr
    exit $exit_code
}

trap 'cleanup' INT TERM EXIT

set -e
hr
echo "Setting up test environment"
hr
virtualenv testenv --python=$(which python3.6)
source testenv/bin/activate
pip install -Ur requirements.txt
pip install -Ur dev-requirements.txt
hr
echo "Running tests"
hr
pytest -vv test/

