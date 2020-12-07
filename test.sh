#!/bin/bash -e

echo "Linting YAML..."
yamllint . --strict

echo "Sorting Python import definitions..."
if [[ "${ci:=}" == "true" ]]; then
  isort . --check-only --diff
else
  isort .
fi

echo "Applying opinionated Python code style..."
if [[ "${ci:=}" == "true" ]]; then
  black . --check --diff
else
  black .
fi

echo "Checking PEP8 compliance..."
flake8 .

echo "Checking Python types..."
mypy wev

echo "Testing..."
coverage run
coverage report -m

if [[ "${ci:=}" != "true" ]]; then
  coverage html
fi
