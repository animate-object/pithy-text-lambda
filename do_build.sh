#!/usr/bin/env bash
hr() {
        printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
}
hr
echo Running build
echo 0 -- run tests
echo 1 -- install dependencies
echo 2 -- bundle code and dependencies
echo 3 -- zip it up
hr

set -e

./do_test.sh

rm -rf build.zip

hr
echo Installing dependencies
hr

mkdir build
virtualenv venv --python=$(which python3.6)
source venv/bin/activate
pip install -Ur requirements.txt
deactivate

hr
echo Bundling code
hr

cp -r src/*.py build/
cp -r venv/lib/python3.6/site-packages/* build/

hr
echo Compressing
hr

zip -r build.zip build
rm -rf venv build

hr
echo Build complete -- check build.zip
hr

