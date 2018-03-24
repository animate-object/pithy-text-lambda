#!/usr/bin/env bash

set -e

rm -rf build.zip
mkdir build

virtualenv venv --python=$(which python3.6)
source venv/bin/activate
pip install -Ur requirements.txt
deactivate

cp -r src/*.py build/
cp -r venv/lib/python3.6/site-packages/* build/

zip -r build.zip build

rm -rf venv build
