set -e

echo "Setting up test environment"

virtualenv testenv --python=$(which python3.6)
source testenv/bin/activate
pip install -Ur requirements.txt
pip install -Ur dev-requirements.txt

echo "Running tests"
pytest -v test/

echo "Tearing down test environment"
deactivate
rm -rf testenv
